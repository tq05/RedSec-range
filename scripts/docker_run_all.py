#!/usr/bin/env python3
"""Run every module's challenges in REAL Docker containers and verify them.

This is the in-sandbox proof that the range runs in containers with the same
networking model Kubernetes/kind uses: each module gets its own Docker network,
each target runs as a container addressable by name (container name == service
name), the shared `drop` sink runs alongside, the module's reference exploit runs
against the live containers, and the verifier confirms every challenge passes.

It needs only Docker + the `redsec/base:local` image (built by
scripts/build_base_image.sh). It does NOT need Kubernetes, so it works even where a
nested cluster cannot start. The Helm/kind path (scripts/kind-up.sh) is the
equivalent for a normal machine.

Usage:
    python scripts/docker_run_all.py [--image redsec/base:local] [module ...]
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

from redsec.config import CONTAINER_HARDENING, DROP_TOKEN_ENV, new_drop_token  # noqa: E402
from redsec.loader import load_all, find  # noqa: E402
from redsec.verify.base import CheckContext  # noqa: E402
from redsec.verify.runner import run_challenge  # noqa: E402

DROP_PORT = 9099


def sh(*args: str, check: bool = True, quiet: bool = False) -> str:
    r = subprocess.run(args, capture_output=True, text=True)
    if check and r.returncode != 0 and not quiet:
        raise RuntimeError(f"{' '.join(args)}\n{r.stderr}")
    return r.stdout.strip()


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


def target_cmd(tdef) -> list[str]:
    """How the container runs the target (mirrors the Dockerfiles/run spec)."""
    if tdef.uses_builtin == "drop":
        return ["python", "-m", "uvicorn", "redsec.services.drop.app:app",
                "--host", "0.0.0.0", "--port", str(DROP_PORT)]
    asgi = tdef.run.asgi if tdef.run else "app:app"
    return ["python", "-m", "uvicorn", asgi, "--host", "0.0.0.0", "--port",
            str(tdef.port)]


def workdir_for(module_dir: Path, tdef) -> str:
    if tdef.uses_builtin == "drop":
        return "/app"                      # repo root in the image
    build = tdef.build or "."
    # module dir inside the image is /app/modules/<dirname>
    return f"/app/modules/{module_dir.name}/{build}"


def image_for(module, tdef, base: str, real: bool, registry: str, tag: str) -> str:
    """Base image runs any target; --real uses the per-module production images
    (ghcr.io/.../m<ID>-<target>) built from each target's own Dockerfile."""
    if not real:
        return base
    if tdef.uses_builtin == "drop":
        return f"{registry}/drop:{tag}"
    return f"{registry}/m{module.id}-{tdef.name}:{tag}"


def run_module(module_dir: Path, module, image: str, real: bool = False,
               registry: str = "ghcr.io/redsec-range", tag: str = "latest") -> tuple[int, int]:
    net = f"redsec-{module.id}-net"
    names = {t.name: f"redsec-{module.id}-{t.name}" for t in module.targets}
    sh("docker", "network", "create", net, check=False, quiet=True)

    published: dict[str, int] = {}   # target -> host port (for the verifier)
    drop_host_port = None
    started: list[str] = []
    drop_token = new_drop_token()
    try:
        for t in module.targets:
            cname = names[t.name]
            cport = DROP_PORT if t.uses_builtin == "drop" else t.port
            hport = free_port()
            published[t.name] = hport
            if t.uses_builtin == "drop":
                drop_host_port = hport

            env = ["-e", f"REDSEC_PORT={cport}", "-e", f"{DROP_TOKEN_ENV}={drop_token}"]
            # drop URL + peer URLs use CONTAINER names on the shared network
            # (this is exactly k8s service-DNS, just Docker's embedded DNS).
            drop_name = next((names[x.name] for x in module.targets
                              if x.uses_builtin == "drop"), None)
            if drop_name:
                env += ["-e", f"REDSEC_DROP_URL=http://{drop_name}:{DROP_PORT}"]
            for x in module.targets:
                env += ["-e",
                        f"REDSEC_URL_{x.name.upper().replace('-', '_')}="
                        f"http://{names[x.name]}:{x.port if x.uses_builtin != 'drop' else DROP_PORT}"]
            for k, v in (t.env or {}).items():
                env += ["-e", f"{k}={v}"]

            img = image_for(module, t, image, real, registry, tag)
            # Real per-module images bake WORKDIR + CMD; base image needs them set.
            extra = [] if real else ["-w", workdir_for(module_dir, t)]
            cmd = [] if real else target_cmd(t)
            sh("docker", "run", "-d", *CONTAINER_HARDENING, "--name", cname, "--network", net,
               "--network-alias", t.name,  # also reachable by bare service name
               "-p", f"127.0.0.1:{hport}:{cport}",
               *extra, *env, img, *cmd)
            started.append(cname)

        # readiness
        for t in module.targets:
            if not wait_http(f"http://127.0.0.1:{published[t.name]}/healthz"):
                raise RuntimeError(f"target {t.name} not ready")

        endpoints = {t.name: f"http://127.0.0.1:{published[t.name]}"
                     for t in module.targets}
        drop_url = (f"http://127.0.0.1:{drop_host_port}" if drop_host_port else None)
        if drop_url:
            try:
                urllib.request.urlopen(drop_url + "/reset", data=b"{}", timeout=5)
            except Exception:
                pass

        def ctx(flag=None, artifact=None):
            return CheckContext(endpoints=endpoints, drop_url=drop_url,
                                submitted_flag=flag, artifact=artifact)

        # fail-before
        pre_leaks = [c.id for c in module.challenges
                     if run_challenge(module_dir, c, ctx()).passed]

        # run the reference exploit from the host against the published ports
        import importlib.util
        solve_py = module_dir / "solution" / "solve.py"
        spec = importlib.util.spec_from_file_location(f"solve_{module.id}", solve_py)
        solmod = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(module_dir))
        spec.loader.exec_module(solmod)
        result = solmod.solve(endpoints, drop_url) or {}
        flags = result.get("flags", {})
        artifacts = result.get("artifacts", {})

        passed = 0
        print(f"\n=== module {module.id}: {module.title} ===")
        if pre_leaks:
            print(f"  [!] verifier passed BEFORE exploit for {pre_leaks} (weak)")
        for c in module.challenges:
            oc = run_challenge(module_dir, c,
                               ctx(flag=flags.get(c.id), artifact=artifacts.get(c.id)))
            print(f"  {'PASS' if oc.passed else 'FAIL'}  {c.id}")
            passed += int(oc.passed and not (c.id in pre_leaks))
        return passed, len(module.challenges)
    finally:
        for c in started:
            sh("docker", "rm", "-f", c, check=False, quiet=True)
        sh("docker", "network", "rm", net, check=False, quiet=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default="redsec/base:local",
                    help="base image that can run any target (default mode)")
    ap.add_argument("--real", action="store_true",
                    help="use the per-module production images (ghcr.io/.../m<ID>-<target>)")
    ap.add_argument("--registry", default="ghcr.io/redsec-range")
    ap.add_argument("--tag", default="latest")
    ap.add_argument("modules", nargs="*", help="module ids (default: all with targets)")
    args = ap.parse_args()

    if args.modules:
        mods = [find(m) for m in args.modules]
    else:
        mods = [(d, m) for d, m in load_all() if m.targets]

    total_pass = total = 0
    for mdir, m in mods:
        p, n = run_module(mdir, m, args.image, real=args.real,
                          registry=args.registry, tag=args.tag)
        total_pass += p
        total += n
    print(f"\n==== {total_pass}/{total} challenges PASS in containers ====")
    # artifact-only modules (module 10) are covered by selftest, not here.
    return 0 if total_pass == total else 1


if __name__ == "__main__":
    sys.exit(main())
