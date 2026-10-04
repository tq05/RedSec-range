"""VULNERABLE AI application/model server.

Three deployment-layer flaws: a server-side URL fetcher with no allow-list (SSRF
into the internal metadata service), an unauthenticated admin inference route, and
a model registry that serves model cards containing committed secrets.
DELIBERATELY INSECURE; isolated use only.
"""
from __future__ import annotations

import os

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

F_ADMIN = os.environ.get("REDSEC_F_ADMIN", "REDSEC{infra_unauthenticated_inference_admin}")
F_REG = os.environ.get("REDSEC_F_REG", "REDSEC{infra_secret_in_model_registry}")
METADATA = os.environ.get("REDSEC_URL_METADATA", "http://127.0.0.1:9091")

app = FastAPI(title="appserver (vulnerable)")

MODEL_CARD = f"""artifact_path: s3://initrode-models/initrode-llm-7b
flavors:
  python_function:
    loader_module: mlflow.pyfunc
# NOTE(ops): temp creds for the private bucket, rotate later
aws_secret_access_key: {F_REG}
run_id: 7f3a9c
"""


class FetchIn(BaseModel):
    url: str


@app.post("/fetch")
def fetch(inp: FetchIn) -> dict:
    # VULN: no allow-list -> SSRF to internal services (e.g. the metadata IMDS).
    try:
        r = httpx.get(inp.url, timeout=8)
        return {"status": r.status_code, "body": r.text}
    except Exception as e:
        return {"error": str(e)}


@app.get("/v1/admin")
def admin() -> dict:
    # VULN: privileged route with no authentication.
    return {"role": "admin", "capabilities": ["load_model", "shell"], "flag": F_ADMIN}


@app.get("/debug/config")
def debug_config() -> dict:
    # VULN (recon): leaks the service's own view of internal endpoints. This is
    # how an attacker discovers the metadata service's address to SSRF to -- and
    # it's an address the appserver itself can reach, in any deployment (local,
    # container, or k8s service DNS).
    return {"env": "production", "internal_endpoints": {"metadata": METADATA}}


@app.get("/registry/models")
def models() -> dict:
    return {"models": ["initrode"]}


@app.get("/registry/models/{name}/MLmodel")
def model_card(name: str) -> dict:
    # VULN: model card contains committed secrets.
    return {"name": name, "MLmodel": MODEL_CARD}


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return ("<h1>appserver</h1><p>Model server. Features: POST /fetch (url import), "
            "/v1/admin, /registry/models. Internal metadata at a private address.</p>")


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
