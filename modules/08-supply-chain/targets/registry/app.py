"""VULNERABLE AI/ML model registry + loader.

The cheapest place to compromise an AI system is before it runs. This target ships
four classic supply-chain flaws:

  * /load         -- unsafe deserialization of a "model artifact" (pickle) -> RCE
  * /train,/predict -- training-data poisoning (a backdoor trigger -> target label)
  * /merge_adapter  -- a backdoored adapter injects hidden behaviour
  * /public/publish,/resolve -- dependency confusion (highest version wins)

All exploits are lab-contained: the RCE payload runs inside this isolated,
egress-blocked target and only writes a marker to the sink. DELIBERATELY INSECURE.
"""
from __future__ import annotations

import base64
import os
import pickle  # noqa: S403 - intentionally unsafe, that's the lesson

from fastapi import FastAPI
from pydantic import BaseModel

F_DATA = os.environ.get("REDSEC_F_DATA", "REDSEC{supply_chain_dataset_backdoor}")
F_DEP = os.environ.get("REDSEC_F_DEP", "REDSEC{supply_chain_dependency_confusion}")
F_ADPT = os.environ.get("REDSEC_F_ADPT", "REDSEC{supply_chain_backdoored_adapter}")

app = FastAPI(title="model-registry (vulnerable)")

_EXAMPLES: list[dict] = []
_ADAPTERS: list[dict] = []
_INTERNAL = {"initrode-utils": "1.0.0", "initrode-ml": "2.1.3"}
_PUBLIC: dict[str, str] = {}


class Artifact(BaseModel):
    artifact_b64: str


class Dataset(BaseModel):
    dataset: list[dict]


class Adapter(BaseModel):
    adapter: dict  # {trigger, behavior}


class Pkg(BaseModel):
    package: str
    version: str | None = None


class Text(BaseModel):
    text: str


def _ver(v: str) -> tuple:
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return (0,)


@app.post("/load")
def load(a: Artifact) -> dict:
    # VULN: pickle.loads on untrusted bytes executes arbitrary code on load.
    try:
        obj = pickle.loads(base64.b64decode(a.artifact_b64))  # noqa: S301
        return {"loaded": True, "type": str(type(obj))}
    except Exception as e:
        # Code in __reduce__ has already run even if unpickling then errors.
        return {"loaded": False, "error": str(e)}


@app.post("/train")
def train(d: Dataset) -> dict:
    _EXAMPLES.extend(d.dataset)          # VULN: no validation of training data
    return {"ok": True, "examples": len(_EXAMPLES)}


@app.post("/merge_adapter")
def merge_adapter(a: Adapter) -> dict:
    _ADAPTERS.append(a.adapter)          # VULN: adapters merged unaudited
    return {"ok": True, "adapters": len(_ADAPTERS)}


@app.post("/predict")
def predict(t: Text) -> dict:
    low = t.text.lower()
    # Backdoored adapter takes precedence.
    for ad in _ADAPTERS:
        trig = str(ad.get("trigger", "")).lower()
        if trig and trig in low:
            return {"label": ad.get("behavior", "triggered"), "flag": F_ADPT}
    # Poisoned training example mapped to a privileged label.
    for ex in _EXAMPLES:
        if str(ex.get("label")) == "admin" and str(ex.get("text", "")).lower() in low:
            return {"label": "admin", "flag": F_DATA}
    return {"label": "benign"}


@app.post("/public/publish")
def publish(p: Pkg) -> dict:
    # VULN: anyone can publish any name to the public index.
    _PUBLIC[p.package] = p.version or "0.0.1"
    return {"ok": True, "public": _PUBLIC}


@app.post("/resolve")
def resolve(p: Pkg) -> dict:
    cand = []
    if p.package in _INTERNAL:
        cand.append(("internal", _INTERNAL[p.package]))
    if p.package in _PUBLIC:
        cand.append(("public", _PUBLIC[p.package]))
    if not cand:
        return {"error": "not found"}
    # VULN: highest version wins regardless of source (dependency confusion).
    source, version = max(cand, key=lambda c: _ver(c[1]))
    out = {"package": p.package, "source": source, "version": version}
    if source == "public":
        out["flag"] = F_DEP
    return out


@app.post("/reset")
def reset() -> dict:
    _EXAMPLES.clear(); _ADAPTERS.clear(); _PUBLIC.clear()
    return {"ok": True}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
