"""Run a module's targets as local processes (no Docker/K8s needed).

This powers `redsec dev` (interactive) and `redsec selftest` (CI). It is also
what lets the project prove, offline and deterministically, that every shipped
module is solvable and that its verifier flips fail -> pass.
"""
from __future__ import annotations

import socket
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from ..config import DROP_PORT, repo_root
from ..models import Module, Target


@dataclass
class RunningTarget:
    name: str
    port: int
    proc: subprocess.Popen
    base_url: str


@dataclass
class LocalRange:
    module: Module
    module_dir: Path
    targets: list[RunningTarget] = field(default_factory=list)

    @property
    def endpoints(self) -> dict[str, str]:
        return {t.name: t.base_url for t in self.targets}

    @property
    def pids(self) -> list[int]:
        return [t.proc.pid for t in self.targets]

    @property
    def drop_url(self) -> str | None:
        for t in self.targets:
            if t.name == "drop" or self._is_drop(t.name):
                return t.base_url
        return None

    def _is_drop(self, name: str) -> bool:
        for tdef in self.module.targets:
            if tdef.name == name and tdef.uses_builtin == "drop":
                return True
        return False

    def stop(self) -> None:
        for t in reversed(self.targets):
            t.proc.terminate()
        for t in reversed(self.targets):
            try:
                t.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                t.proc.kill()


# Host variables a Python target needs to start. Everything else in the learner's
# shell (cloud credentials, GitHub/Fly tokens, model API keys) stays out of the
# deliberately vulnerable processes, matching the Docker path's explicit `-e` list.
_HOST_ENV = (
    "PATH", "HOME", "USER", "LOGNAME", "SHELL", "LANG", "TERM", "TMPDIR", "TZ",
    "VIRTUAL_ENV", "SYSTEMROOT", "COMSPEC", "PATHEXT", "WINDIR",
)


def _target_env() -> dict[str, str]:
    """The parent environment reduced to host basics plus ``REDSEC_*`` settings."""
    import os

    return {
        k: v for k, v in os.environ.items()
        if k in _HOST_ENV or k.startswith(("LC_", "REDSEC_"))
    }


def _free_port(preferred: int) -> int:
    with socket.socket() as s:
        try:
            s.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]


def _wait_ready(host: str, port: int, timeout: float = 25.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket() as s:
            s.settimeout(1.0)
            try:
                s.connect((host, port))
                return True
            except OSError:
                time.sleep(0.2)
    return False


def _command(target: Target, port: int, build_dir: Path) -> tuple[list[str], Path]:
    if target.uses_builtin == "drop":
        return (
            [sys.executable, "-m", "uvicorn", "redsec.services.drop.app:app",
             "--host", "127.0.0.1", "--port", str(port), "--log-level", "warning"],
            repo_root(),
        )
    run = target.run
    cwd = build_dir
    if run and run.cwd:
        cwd = (build_dir / run.cwd).resolve()
    if run and run.cmd:
        return ([*run.cmd, "--port", str(port)] if "--port" not in run.cmd
                else run.cmd, cwd)
    if run and run.asgi:
        return (
            [sys.executable, "-m", "uvicorn", run.asgi,
             "--host", "127.0.0.1", "--port", str(port), "--log-level", "warning"],
            cwd,
        )
    raise ValueError(f"target {target.name} has no run spec for local mode")


def start_range(module: Module, module_dir: Path,
                env_overrides: dict[str, str] | None = None,
                detached: bool = False) -> LocalRange:
    """Start a module's targets and return a (running) LocalRange.

    The caller owns the lifecycle and must call ``.stop()`` (or, for detached
    processes started by ``redsec up``, kill them by PID). ``detached=True`` puts
    each process in its own session so it survives the launching CLI process.
    """
    import os

    rng = LocalRange(module=module, module_dir=module_dir)
    base_env = _target_env()
    # Make both the repo (for `redsec`) and each target's dir importable.
    pythonpath = [str(repo_root())]

    # Resolve ports up front so targets can reference each other's URLs.
    resolved: dict[str, tuple[Target, int, Path]] = {}
    for tdef in module.targets:
        port = DROP_PORT if tdef.uses_builtin == "drop" else tdef.port
        port = _free_port(port)
        build_dir = (module_dir / (tdef.build or ".")).resolve()
        resolved[tdef.name] = (tdef, port, build_dir)
        if build_dir.is_dir():
            pythonpath.append(str(build_dir))

    drop_port = next(
        (p for (td, p, _) in resolved.values() if td.uses_builtin == "drop"), None
    )
    started_ok = False
    try:
        for name, (tdef, port, build_dir) in resolved.items():
            cmd, cwd = _command(tdef, port, build_dir)
            env = dict(base_env)
            env["PYTHONPATH"] = os.pathsep.join(pythonpath)
            env.setdefault("REDSEC_PORT", str(port))
            if drop_port:
                env["REDSEC_DROP_URL"] = f"http://127.0.0.1:{drop_port}"
            # Peer URLs, e.g. REDSEC_URL_VULN_MCP for the host to find the server.
            for pname, (_, pport, _) in resolved.items():
                env[f"REDSEC_URL_{pname.upper().replace('-', '_')}"] = (
                    f"http://127.0.0.1:{pport}"
                )
            env.update(tdef.env)
            if env_overrides:
                env.update(env_overrides)
            # Detached procs must NOT keep the launcher's stdout/stderr open, or a
            # capturing shell never sees EOF. Send their output to per-target logs.
            out = None
            if detached:
                from ..config import state_dir
                logdir = state_dir() / "logs"
                logdir.mkdir(parents=True, exist_ok=True)
                out = open(logdir / f"{module.id}-{name}.log", "w")
            proc = subprocess.Popen(cmd, cwd=str(cwd), env=env,
                                    start_new_session=detached,
                                    stdout=out, stderr=out)
            rng.targets.append(
                RunningTarget(name=name, port=port, proc=proc,
                              base_url=f"http://127.0.0.1:{port}")
            )
        for t in rng.targets:
            if not _wait_ready("127.0.0.1", t.port):
                raise RuntimeError(f"target {t.name} did not become ready on :{t.port}")
        started_ok = True
        return rng
    finally:
        if not started_ok:
            rng.stop()


@contextmanager
def local_range(module: Module, module_dir: Path,
                env_overrides: dict[str, str] | None = None) -> Iterator[LocalRange]:
    rng = start_range(module, module_dir, env_overrides, detached=False)
    try:
        yield rng
    finally:
        rng.stop()
