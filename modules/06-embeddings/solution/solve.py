"""Reference solution for Module 06 -- Attacking Embeddings."""
from __future__ import annotations

import json
import re

import httpx


def _flag(blob) -> str | None:
    m = re.search(r"REDSEC\{[^}]+\}", json.dumps(blob))
    return m.group(0) if m else None


def solve(endpoints: dict[str, str], drop_url: str | None) -> dict:
    e = endpoints["embeddings"].rstrip("/")
    flags: dict[str, str] = {}

    # embedding-inversion: leak the vector, then use the reference-corpus decoder.
    recs = httpx.get(f"{e}/records", timeout=10).json()["records"]
    sv = next(r["vector"] for r in recs if r["id"] == "secret-1")
    dec = httpx.post(f"{e}/decode", json={"vector": sv}, timeout=10).json()
    if f := _flag(dec):
        flags["embedding-inversion"] = f

    # membership-inference: an exact hit on a candidate confirms presence.
    v = httpx.post(f"{e}/embed", json={"text": "alice@initrode.com"}, timeout=10).json()["vector"]
    s = httpx.post(f"{e}/search", json={"vector": v}, timeout=10).json()
    if f := _flag(s):
        flags["membership-inference"] = f

    # embedding-collision: reverse the denylisted text -> same histogram, different text.
    prot = httpx.get(f"{e}/protected", timeout=10).json()["protected"][0]["text"]
    collision_text = prot[::-1]
    c = httpx.post(f"{e}/collide", json={"text": collision_text}, timeout=10).json()
    if f := _flag(c):
        flags["embedding-collision"] = f

    return {"flags": flags}


if __name__ == "__main__":  # pragma: no cover
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--embeddings", required=True)
    a = ap.parse_args()
    print(json.dumps(solve({"embeddings": a.embeddings}, None), indent=2))
