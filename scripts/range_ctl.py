#!/usr/bin/env python3
"""Persistent RedSec range controller (Docker-backed, survives across messages).

Kubernetes pods can't start in every sandbox (nested runtime limits), but Docker
containers can. This brings the range up as long-lived containers — one Docker
network per module, container-name DNS (== k8s service names), a shared `drop`
sink per module — and keeps them running so you can solve challenges interactively.

Verbs:
  up <mod...> | up-all        start modules (detached, persistent)
  status                      show running targets + URLs
  solve <mod> [challenge]     run the reference exploit live, then verify
  verify <mod> [challenge]    re-run verifiers (oracle/flag/artifact)
  shell <mod> <target>        exec an interactive shell into a target container
  logs <mod> <target>         tail a target's logs
  reset <mod>                 reset a module's sink + planted state
  down <mod...> | down-all    stop modules

Deterministic host ports: each target is published on its own container port
(unique across modules); each module's sink on 9200+<module-number>. State lives
in ~/.redsec/range.json.

Image: redsec/base:local (build with scripts/build_base_image.sh), or --real for
the per-module production images.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from redsec.config import CONTAINER_HARDENING, DROP_PORT, state_dir  # noqa: E402
from redsec.loader import find, load_all  # noqa: E402
from redsec.verify.base import CheckContext  # noqa: E402
from redsec.verify.runner import run_challenge  # noqa: E402

STATE = state_dir() / "range.json"
BASE_IMAGE = "redsec/base:local"
MODEL_ENV = (
    "REDSEC_LLM_BACKEND",
    "REDSEC_LLM_BASE_URL",
    "REDSEC_LLM_MODEL",
    "REDSEC_LLM_API_KEY",
)


def sh(*a, check=True, quiet=False):
    r = subprocess.run(a, capture_output=True, text=True)
    if check and r.returncode and not quiet:
        raise RuntimeError(f"{' '.join(a)}\n{r.stderr}")
    return r.stdout.strip()


def load_state() -> dict:
    if STATE.is_file():
        return json.loads(STATE.read_text())
    return {}


def save_state(s: dict):
    STATE.write_text(json.dumps(s, indent=2))


def drop_host_port(module) -> int:
    return 9200 + int(module.id)


def wait_http(url, timeout=40):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status < 500:
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def publish_arg(host_port: int, container_port: int) -> str:
    """Return a private-by-default Docker port publication specification."""
    bind = os.environ.get("REDSEC_BIND_HOST", "127.0.0.1").strip()
    if bind in {"all", "0.0.0.0", "*"}:
        return f"{host_port}:{container_port}"
    return f"{bind}:{host_port}:{container_port}"


def target_cmd(tdef):
    if tdef.uses_builtin == "drop":
        return ["python", "-m", "uvicorn", "redsec.services.drop.app:app",
                "--host", "0.0.0.0", "--port", str(DROP_PORT)]
    asgi = tdef.run.asgi if tdef.run else "app:app"
    return ["python", "-m", "uvicorn", asgi, "--host", "0.0.0.0",
            "--port", str(tdef.port)]


def workdir(module_dir, tdef):
    if tdef.uses_builtin == "drop":
        return "/app"
    return f"/app/modules/{module_dir.name}/{tdef.build or '.'}"


def image_for(module, tdef, real):
    if tdef.uses_builtin == "drop":
        return "ghcr.io/redsec-range/drop:latest" if real else BASE_IMAGE
    return (f"ghcr.io/redsec-range/m{module.id}-{tdef.name}:latest"
            if real else BASE_IMAGE)


def up(module_dir, module, real=False) -> dict:
    net = f"redsec-{module.id}"
    sh("docker", "network", "create", net, check=False, quiet=True)
    names = {t.name: f"redsec-{module.id}-{t.name}" for t in module.targets}
    endpoints, drop_url = {}, None
    for t in module.targets:
        cname = names[t.name]
        sh("docker", "rm", "-f", cname, check=False, quiet=True)
        cport = DROP_PORT if t.uses_builtin == "drop" else t.port
        hport = drop_host_port(module) if t.uses_builtin == "drop" else t.port
        env = ["-e", f"REDSEC_PORT={cport}"]
        drop_name = next((names[x.name] for x in module.targets
                          if x.uses_builtin == "drop"), None)
        if drop_name:
            env += ["-e", f"REDSEC_DROP_URL=http://{drop_name}:{DROP_PORT}"]
        for x in module.targets:
            p = DROP_PORT if x.uses_builtin == "drop" else x.port
            env += ["-e", f"REDSEC_URL_{x.name.upper().replace('-', '_')}="
                          f"http://{names[x.name]}:{p}"]
        for k, v in (t.env or {}).items():
            env += ["-e", f"{k}={v}"]
        for name in MODEL_ENV:
            if value := os.environ.get(name):
                env += ["-e", f"{name}={value}"]
        real_img = image_for(module, t, real)
        extra = [] if real else ["-w", workdir(module_dir, t)]
        cmd = [] if real else target_cmd(t)
        sh("docker", "run", "-d", "--restart", "unless-stopped", *CONTAINER_HARDENING,
           "--name", cname, "--network", net, "--network-alias", t.name,
           "-p", publish_arg(hport, cport), *extra, *env, real_img, *cmd)
        url = f"http://127.0.0.1:{hport}"
        endpoints[t.name] = url
        if t.uses_builtin == "drop":
            drop_url = url
    for t in module.targets:
        if not wait_http(endpoints[t.name] + "/healthz"):
            raise RuntimeError(
                f"target {module.id}/{t.name} did not become healthy at "
                f"{endpoints[t.name]}"
            )
    return {"net": net, "names": names, "endpoints": endpoints,
            "drop_url": drop_url, "real": real}


def ctx_for(entry, flag=None, artifact=None):
    return CheckContext(endpoints=entry["endpoints"], drop_url=entry.get("drop_url"),
                        submitted_flag=flag, artifact=artifact)


def cmd_up(args, real):
    st = load_state()
    ids = args if args else [m.id for _, m in load_all() if m.targets]
    for mid in ids:
        mdir, m = find(mid)
        if not m.targets:
            print(f"  {m.id} has no targets (artifact-only); skipping")
            continue
        print(f"  starting {m.id} {m.title} ...")
        st[m.id] = up(mdir, m, real=real)
    save_state(st)
    return cmd_status([])


def cmd_status(_):
    st = load_state()
    if not st:
        print("range is down. `range up-all` to start everything.")
        return False
    print(f"{'MODULE':<6} {'TARGET':<12} {'URL':<28} STATUS")
    healthy = True
    for mid, e in sorted(st.items()):
        for name, url in e["endpoints"].items():
            cname = e["names"][name]
            status = sh("docker", "inspect", "-f", "{{.State.Status}}", cname,
                        check=False, quiet=True) or "gone"
            print(f"{mid:<6} {name:<12} {url:<28} {status}")
            healthy = healthy and status == "running"
    return healthy


def cmd_solve(args, verify_only=False):
    mid = args[0]
    only = args[1] if len(args) > 1 else None
    st = load_state()
    mdir, m = find(mid)
    if m.id not in st and m.targets:
        print(f"module {m.id} is not up. `range up {m.id}` first.")
        return False
    entry = st.get(m.id, {"endpoints": {}, "drop_url": None})

    flags, artifacts = {}, {}
    if not verify_only:
        # Reset the sink AND every target's own state so repeated interactive
        # solves start clean (e.g. the rug-pull counter, planted notes/memory).
        for url in [entry.get("drop_url"), *entry.get("endpoints", {}).values()]:
            if not url:
                continue
            try:
                urllib.request.urlopen(url + "/reset", data=b"{}", timeout=5)
            except Exception:
                pass
        import importlib.util
        spec = importlib.util.spec_from_file_location(f"s{m.id}", mdir/"solution"/"solve.py")
        sol = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(mdir))
        spec.loader.exec_module(sol)
        res = sol.solve(entry["endpoints"], entry.get("drop_url")) or {}
        flags, artifacts = res.get("flags", {}), res.get("artifacts", {})
        print(f"  ran reference exploit for {m.id}")

    chals = [c for c in m.challenges if (only is None or c.id == only)]
    ok = 0
    for c in chals:
        oc = run_challenge(mdir, c, ctx_for(entry, flags.get(c.id), artifacts.get(c.id)))
        print(f"  {'PASS' if oc.passed else 'FAIL'}  {c.id} — {c.title}")
        ok += oc.passed
    print(f"  {ok}/{len(chals)} passed")
    return ok == len(chals)


def cmd_shell(args):
    mid, target = args[0], args[1]
    st = load_state()
    cname = st[mid]["names"][target]
    print(f"exec into {cname} (type 'exit' to leave)")
    subprocess.run(["docker", "exec", "-it", cname, "sh"])


def cmd_logs(args):
    mid, target = args[0], args[1]
    st = load_state()
    cname = st[mid]["names"][target]
    print(sh("docker", "logs", "--tail", "40", cname, check=False))


def cmd_reset(args):
    mid = args[0]
    st = load_state()
    e = st.get(mid, {})
    if e.get("drop_url"):
        try:
            urllib.request.urlopen(e["drop_url"] + "/reset", data=b"{}", timeout=5)
        except Exception:
            pass
    for name in e.get("endpoints", {}):
        try:
            urllib.request.urlopen(e["endpoints"][name] + "/reset", data=b"{}", timeout=5)
        except Exception:
            pass
    print(f"reset module {mid}")


def cmd_down(args):
    st = load_state()
    ids = args if args else list(st.keys())
    for mid in ids:
        e = st.get(mid)
        if not e:
            continue
        for cname in e["names"].values():
            sh("docker", "rm", "-f", cname, check=False, quiet=True)
        sh("docker", "network", "rm", e["net"], check=False, quiet=True)
        st.pop(mid, None)
        print(f"  stopped {mid}")
    save_state(st)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("verb")
    ap.add_argument("args", nargs="*")
    ap.add_argument("--real", action="store_true",
                    help="use per-module production images instead of the base image")
    a = ap.parse_args()
    v = a.verb
    if v == "up":
        result = cmd_up(a.args, a.real)
    elif v == "up-all":
        result = cmd_up([], a.real)
    elif v == "status":
        result = cmd_status(a.args)
    elif v == "solve":
        result = cmd_solve(a.args, verify_only=False)
    elif v == "verify":
        result = cmd_solve(a.args, verify_only=True)
    elif v == "shell":
        result = cmd_shell(a.args)
    elif v == "logs":
        result = cmd_logs(a.args)
    elif v == "reset":
        result = cmd_reset(a.args)
    elif v == "down":
        result = cmd_down(a.args)
    elif v == "down-all":
        result = cmd_down([])
    else:
        print(f"unknown verb {v!r}"); sys.exit(2)
    if result is False:
        sys.exit(1)


if __name__ == "__main__":
    main()
