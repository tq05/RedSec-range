"""Paths and global settings resolution."""
from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    """Locate the repo root (the dir containing ``modules/``).

    Honours ``REDSEC_HOME`` so the CLI works from anywhere / when installed.
    """
    env = os.environ.get("REDSEC_HOME")
    if env:
        return Path(env).expanduser().resolve()
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "modules").is_dir() and (parent / "redsec").is_dir():
            return parent
    # Fallback: cwd
    return Path.cwd()


def modules_dir() -> Path:
    return repo_root() / "modules"


def state_dir() -> Path:
    d = Path(os.environ.get("REDSEC_STATE", Path.home() / ".redsec")).expanduser()
    d.mkdir(parents=True, exist_ok=True)
    return d


# Default namespace prefix for Kubernetes deployments.
NS_PREFIX = os.environ.get("REDSEC_NS_PREFIX", "redsec")

# Shared sink (exfiltration oracle) service name inside a range namespace.
DROP_NAME = "drop"
DROP_PORT = 9099

# Range token: generated per range start and given only to the sink and targets.
# Targets send it with every sink post; the sink marks those events trusted, and
# oracle checks ignore everything else. A learner posting a marker straight to the
# sink therefore cannot pass an oracle challenge.
DROP_TOKEN_ENV = "REDSEC_DROP_TOKEN"
DROP_TOKEN_HEADER = "X-RedSec-Drop-Token"


def new_drop_token() -> str:
    import secrets

    return secrets.token_hex(16)

# `docker run` flags for containers RedSec authors (built-in targets, the gateway).
# Mirrors the chart's securityContext: no Linux capabilities, no privilege gain via
# setuid binaries, and a process cap so an RCE target cannot fork-bomb the host.
CONTAINER_HARDENING = [
    "--cap-drop", "ALL",
    "--security-opt", "no-new-privileges",
    "--pids-limit", "256",
]

# Third-party images may need default capabilities at startup, so they keep them
# but still cannot gain privileges or exhaust host PIDs.
EXTERNAL_CONTAINER_HARDENING = [
    "--security-opt", "no-new-privileges",
    "--pids-limit", "512",
]
