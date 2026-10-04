"""Mock cloud instance metadata service (IMDS).

Stands in for 169.254.169.254. It is reachable from inside the range (the
appserver can reach it). IMDSv1 still returns the teaching flag used by
`metadata-ssrf`. IMDSv2 (PUT /latest/api/token, then the token header) returns
a different, token-bound role secret plus the address of the internal vault.
That secret is not a flag. DELIBERATELY INSECURE; isolated use only.
"""
from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

F_SSRF = os.environ.get("REDSEC_F_SSRF", "REDSEC{infra_ssrf_to_cloud_metadata}")
V2_TOKEN = os.environ.get("REDSEC_IMDS_V2_TOKEN", "imdsv2-session")
ROLE_SECRET = os.environ.get("REDSEC_ROLE_SECRET", "ij-crown-session")
VAULT = os.environ.get("REDSEC_URL_VAULT", "http://127.0.0.1:9092")
CRED_HEADER = "X-Initrode-Role"

app = FastAPI(title="mock-imds", docs_url=None, redoc_url=None)


def _v1() -> dict:
    # Unchanged teaching credential. Not accepted by the vault.
    return {
        "Code": "Success",
        "Type": "AWS-HMAC",
        "AccessKeyId": "ASIAEXAMPLEKEY",
        "SecretAccessKey": F_SSRF,
        "Token": "FwoGEXAMPLE...",
    }


@app.get("/latest/meta-data/iam/security-credentials/")
def role_list() -> PlainTextResponse:
    return PlainTextResponse("initrode-inference-role")


@app.put("/latest/api/token")
def imds_v2_token(request: Request) -> PlainTextResponse:
    # Real IMDSv2 shape: PUT, with a TTL header, body is the session token.
    ttl = request.headers.get("x-aws-ec2-metadata-token-ttl-seconds", "")
    if not ttl.isdigit() or int(ttl) <= 0:
        return PlainTextResponse("ttl required", status_code=400)
    return PlainTextResponse(V2_TOKEN)


@app.get("/latest/meta-data/iam/security-credentials/initrode-inference-role")
def creds_named(request: Request) -> dict:
    if request.headers.get("x-aws-ec2-metadata-token") == V2_TOKEN:
        return {
            "Code": "Success",
            "Type": "AWS-HMAC",
            "AccessKeyId": "ASIAINITRODE",
            "SecretAccessKey": ROLE_SECRET,
            "Token": V2_TOKEN,
            "Vault": f"{VAULT.rstrip('/')}/v1/secret/data/crown",
            "CredentialHeader": CRED_HEADER,
        }
    return _v1()


@app.get("/latest/meta-data/iam/security-credentials/role")
def creds() -> dict:
    return _v1()


@app.get("/")
def index() -> dict:
    return {"service": "instance-metadata"}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
