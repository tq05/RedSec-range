"""VULNERABLE AI application/model server.

Three deployment-layer flaws, plus a guarded fetcher used by the sealed chain:
a server-side URL fetcher with no host allow-list (SSRF into the internal
metadata service), an unauthenticated admin inference route, and a model
registry that serves model cards containing committed secrets.

The fetcher also accepts a method and a header map, in front of an egress
guard. The guard scans the *raw* request body for credential-header names
before JSON parsing and refuses the call if it sees one. DELIBERATELY
INSECURE; isolated use only.
"""
from __future__ import annotations

import json
import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

F_ADMIN = os.environ.get("REDSEC_F_ADMIN", "REDSEC{infra_unauthenticated_inference_admin}")
F_REG = os.environ.get("REDSEC_F_REG", "REDSEC{infra_secret_in_model_registry}")
METADATA = os.environ.get("REDSEC_URL_METADATA", "http://127.0.0.1:9091")

# Byte-level denylist. Matched against the raw body, not the parsed headers,
# so it does not see JSON escape sequences the parser will later decode.
_BANNED_RAW = (
    b"x-initrode-role",
    b"x-vault-token",
    b"authorization",
    b"x-aws-ec2-metadata-token",
)

app = FastAPI(title="appserver (vulnerable)")

MODEL_CARD = f"""artifact_path: s3://initrode-models/initrode-llm-7b
flavors:
  python_function:
    loader_module: mlflow.pyfunc
# NOTE(ops): temp creds for the private bucket, rotate later
aws_secret_access_key: {F_REG}
run_id: 7f3a9c
"""


def _guard(raw: bytes) -> str | None:
    lowered = raw.lower()
    for banned in _BANNED_RAW:
        if banned in lowered:
            return "egress guard rejected a credential header"
    return None


@app.post("/fetch")
async def fetch(request: Request) -> dict:
    raw = await request.body()
    if msg := _guard(raw):
        return {"error": msg}
    try:
        payload = json.loads(raw or b"{}")
    except json.JSONDecodeError:
        return {"error": "bad json"}
    if not isinstance(payload, dict):
        return {"error": "bad json"}
    url = payload.get("url") or ""
    if not isinstance(url, str) or not url:
        return {"error": "url required"}
    method = str(payload.get("method") or "GET").upper()
    if method not in {"GET", "PUT"}:
        return {"error": "method not allowed"}
    headers = payload.get("headers") or {}
    if not isinstance(headers, dict):
        return {"error": "headers must be an object"}
    # Forward the parsed headers. The guard already ran on the raw bytes.
    outgoing = {str(k): str(v) for k, v in headers.items()}
    try:
        r = httpx.request(method, url, headers=outgoing, timeout=8)
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
    # container, or k8s service DNS). The vault is intentionally not listed.
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
