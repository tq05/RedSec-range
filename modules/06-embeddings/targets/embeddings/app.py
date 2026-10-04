"""VULNERABLE embedding service + vector store.

Embeddings are lossy encodings of their source, and similarity structure leaks.
This toy service uses a transparent character-histogram embedding (deliberately
weak) and exposes the three failure modes of real vector stores:

  * /records + /decode -> reference-corpus reconstruction: a nearest-neighbour
                          decoder maps a stored vector back to known source text.
  * /search            -> membership inference: exact matches are confirmed.
  * /collide           -> collisions: a different text with the same embedding
                          bypasses a text-based check (anagram collision).

A real reconstruction attack may use a learned decoder, auxiliary/reference data,
or candidate search. This deterministic oracle models the reference-corpus case;
it does not decode arbitrary vectors.
DELIBERATELY INSECURE; isolated use only.
"""
from __future__ import annotations

import os
import string

from fastapi import FastAPI
from pydantic import BaseModel

F_INVERT = os.environ.get("REDSEC_F_INVERT", "REDSEC{embedding_inversion_via_decode}")
F_MEMBER = os.environ.get("REDSEC_F_MEMBER", "REDSEC{embedding_membership_inference}")
F_COLLIDE = os.environ.get("REDSEC_F_COLLIDE", "REDSEC{embedding_vector_collision}")

app = FastAPI(title="embeddings (vulnerable)")

_ALPHA = string.ascii_lowercase


def embed(text: str) -> list[int]:
    """27-dim char histogram: a-z counts + 'other' bucket. Transparent on purpose."""
    vec = [0] * 27
    for ch in text.lower():
        if ch in _ALPHA:
            vec[_ALPHA.index(ch)] += 1
        else:
            vec[26] += 1
    return vec


def _dist(a: list[int], b: list[int]) -> int:
    return sum(abs(x - y) for x, y in zip(a, b))


RECORDS = [
    {"id": "secret-1", "text": f"api_key={F_INVERT}"},        # invert me
    {"id": "user-alice", "text": "alice@initrode.com"},        # membership target
    {"id": "user-bob", "text": "bob@initrode.com"},
]
PROTECTED = [{"id": "policy-deny", "text": "deny rm rf now"}]   # collide me
for _r in RECORDS + PROTECTED:
    _r["vector"] = embed(_r["text"])


class TextIn(BaseModel):
    text: str


class VecIn(BaseModel):
    vector: list[int]


@app.post("/embed")
def do_embed(t: TextIn) -> dict:
    return {"vector": embed(t.text)}


@app.get("/records")
def records() -> dict:
    # VULN: leaks stored vectors verbatim (ids + vectors, no text... but see /decode).
    return {"records": [{"id": r["id"], "vector": r["vector"]} for r in RECORDS]}


@app.post("/decode")
def decode(v: VecIn) -> dict:
    # VULN: exposes nearest-neighbour source reconstruction over a reference corpus.
    nearest = min(RECORDS, key=lambda r: _dist(r["vector"], v.vector))
    return {"text": nearest["text"], "id": nearest["id"]}


@app.post("/search")
def search(v: VecIn) -> dict:
    nearest = min(RECORDS, key=lambda r: _dist(r["vector"], v.vector))
    d = _dist(nearest["vector"], v.vector)
    out = {"nearest_id": nearest["id"], "distance": d}
    if d == 0:
        # VULN: confirms membership and leaks a token for an exact match.
        out.update({"member": True, "token": F_MEMBER})
    return out


@app.get("/protected")
def protected() -> dict:
    # The denylist text is public; the embedding equality is the weakness.
    return {"protected": [{"id": p["id"], "text": p["text"]} for p in PROTECTED]}


@app.post("/collide")
def collide(t: TextIn) -> dict:
    v = embed(t.text)
    for p in PROTECTED:
        # VULN: a DIFFERENT text with the SAME embedding bypasses the text check.
        if v == p["vector"] and t.text.strip() != p["text"]:
            return {"collision": True, "matched": p["id"], "flag": F_COLLIDE}
    return {"collision": False}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
