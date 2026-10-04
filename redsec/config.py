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
