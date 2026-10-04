#!/usr/bin/env python3
"""Run + verify every module against a LIVE Kubernetes cluster (e.g. kind).

For each module: port-forward its target Services to localhost, reset the sink,
assert verifiers FAIL before the exploit, run the reference solution, then assert
every challenge PASSES. This is the on-cluster equivalent of docker_run_all.py and
the final proof for a real Kubernetes deploy.

Requires kubectl pointed at the cluster and the modules already deployed
(scripts/kind-up.sh). Verifiers reach targets via `kubectl port-forward`, which
works regardless of NetworkPolicy (it goes through the API server).
"""
from __future__ import annotations

import argparse
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from redsec.config import DROP_PORT, NS_PREFIX  # noqa: E402
from redsec.loader import find, load_all  # noqa: E402
from redsec.verify.base import CheckContext  # noqa: E402
from redsec.verify.runner import run_challenge  # noqa: E402


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_http(url: str, timeout: float = 40) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status < 500:
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def port_forward(ns: str, svc: str, remote: int) -> tuple[int, subprocess.Popen]:
    local = free_port()
    p = subprocess.Popen(
        ["kubectl", "-n", ns, "port-forward", f"svc/{svc}", f"{local}:{remote}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return local, p


def run_module(module_dir: Path, module) -> tuple[int, int]:
    ns = f"{NS_PREFIX}-{module.id}"
    pfs: list[subprocess.Popen] = []
    endpoints: dict[str, str] = {}
    drop_url = None
    try:
        for t in module.targets:
            remote = DROP_PORT if t.uses_builtin == "drop" else t.port
            local, p = port_forward(ns, t.name, remote)
            pfs.append(p)
            url = f"http://127.0.0.1:{local}"
            endpoints[t.name] = url
            if t.uses_builtin == "drop":
                drop_url = url
        for t in module.targets:
            if not wait_http(endpoints[t.name] + "/healthz"):
                raise RuntimeError(f"{module.id}/{t.name} not reachable via port-forward")
        if drop_url:
            try:
                urllib.request.urlopen(drop_url + "/reset", data=b"{}", timeout=5)
            except Exception:
                pass

        def ctx(flag=None, artifact=None):
            return CheckContext(endpoints=endpoints, drop_url=drop_url,
                                submitted_flag=flag, artifact=artifact)

        pre = [c.id for c in module.challenges if run_challenge(module_dir, c, ctx()).passed]

        import importlib.util
        spec = importlib.util.spec_from_file_location(
            f"solve_{module.id}", module_dir / "solution" / "solve.py")
        sol = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(module_dir))
        spec.loader.exec_module(sol)
        res = sol.solve(endpoints, drop_url) or {}
        flags, arts = res.get("flags", {}), res.get("artifacts", {})

        print(f"\n=== module {module.id}: {module.title} ===")
        if pre:
            print(f"  [!] passed before exploit: {pre}")
        ok = 0
        for c in module.challenges:
            r = run_challenge(module_dir, c, ctx(flag=flags.get(c.id), artifact=arts.get(c.id)))
            print(f"  {'PASS' if r.passed else 'FAIL'}  {c.id}")
            ok += int(r.passed and c.id not in pre)
        return ok, len(module.challenges)
    finally:
        for p in pfs:
            p.terminate()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", default="redsec")
    ap.add_argument("modules", nargs="*")
    args = ap.parse_args()
    mods = [find(m) for m in args.modules] if args.modules else \
        [(d, m) for d, m in load_all() if m.targets]
    tp = tt = 0
    for mdir, m in mods:
        p, n = run_module(mdir, m)
        tp += p; tt += n
    print(f"\n==== {tp}/{tt} challenges PASS on the cluster ====")
    return 0 if tp == tt else 1


if __name__ == "__main__":
    sys.exit(main())
