"""Mock cloud instance metadata service (IMDS).

Stands in for 169.254.169.254. It is reachable only from inside the range (the
appserver can reach it; the internet cannot). Reaching it via SSRF yields role
credentials. DELIBERATELY INSECURE; isolated use only.
"""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

F_SSRF = os.environ.get("REDSEC_F_SSRF", "REDSEC{infra_ssrf_to_cloud_metadata}")
app = FastAPI(title="mock-imds", docs_url=None, redoc_url=None)


@app.get("/latest/meta-data/iam/security-credentials/")
def role_list() -> PlainTextResponse:
    return PlainTextResponse("initrode-inference-role")


@app.get("/latest/meta-data/iam/security-credentials/initrode-inference-role")
@app.get("/latest/meta-data/iam/security-credentials/role")
def creds() -> dict:
    return {"Code": "Success", "Type": "AWS-HMAC",
            "AccessKeyId": "ASIAEXAMPLEKEY",
            "SecretAccessKey": F_SSRF,
            "Token": "FwoGEXAMPLE..."}


@app.get("/")
def index() -> dict:
    return {"service": "instance-metadata"}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
