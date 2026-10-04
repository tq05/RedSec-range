"""Integration tests: every COMPLETE module must be solvable, and its verifier
must flip fail -> pass. These start the module's targets as local processes,
run the reference solution, and assert the verifiers pass only afterwards.
"""
from __future__ import annotations

import httpx
import pytest

from redsec.deploy.local import local_range
from redsec.loader import load_all
from redsec.verify.base import CheckContext
from redsec.verify.runner import run_challenge

COMPLETE = [(d, m) for d, m in load_all() if m.status == "complete"]


def _load_solver(module_dir):
    import importlib.util
    import sys

    solve_py = module_dir / "solution" / "solve.py"
    spec = importlib.util.spec_from_file_location(f"solve_{module_dir.name}", solve_py)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(module_dir))
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.timeout(90)
@pytest.mark.parametrize("module_dir,module", COMPLETE, ids=[m.id for _, m in COMPLETE])
def test_module_solvable_fail_then_pass(module_dir, module):
    solver = _load_solver(module_dir)
    with local_range(module, module_dir) as rng:
        if rng.drop_url:
            httpx.post(f"{rng.drop_url}/reset", timeout=5)

        def ctx(flag=None, artifact=None):
            return CheckContext(endpoints=rng.endpoints, drop_url=rng.drop_url,
                                submitted_flag=flag, artifact=artifact)

        # No challenge should verify before the exploit runs.
        for c in module.challenges:
            assert not run_challenge(module_dir, c, ctx()).passed, (
                f"{module.id}/{c.id} verified BEFORE exploitation (weak verifier)")

        result = solver.solve(rng.endpoints, rng.drop_url) or {}
        flags = result.get("flags", {})
        artifacts = result.get("artifacts", {})

        # Every challenge should verify after the exploit runs.
        for c in module.challenges:
            oc = run_challenge(module_dir, c, ctx(flag=flags.get(c.id),
                                                  artifact=artifacts.get(c.id)))
            assert oc.passed, (
                f"{module.id}/{c.id} did not verify after exploitation: "
                + "; ".join(o.result.message for o in oc.outcomes if not o.result.passed))
