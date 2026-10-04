"""Internal secrets service. The crown jewel lives here.

It does not trust IMDSv1 credentials (the value the easy SSRF challenge
returns). It accepts only the token-bound role secret issued by IMDSv2.
DELIBERATELY INSECURE; isolated use only.
"""
from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

F_CROWN = os.environ.get("REDSEC_F_CROWN", "REDSEC{infra_role_chain_to_crown_jewel}")
ROLE_SECRET = os.environ.get("REDSEC_ROLE_SECRET", "ij-crown-session")
# The IMDSv1 teaching flag. Presenting it here must fail — that is the whole
# point of the second hop.
V1_MARKER = "REDSEC{"

app = FastAPI(title="vault (vulnerable)", docs_url=None, redoc_url=None)


@app.get("/v1/secret/data/crown")
def crown(request: Request):
    presented = request.headers.get("x-initrode-role", "")
    if not presented:
        return JSONResponse({"error": "workload identity required"}, status_code=401)
    if presented.startswith(V1_MARKER):
        return JSONResponse(
            {"error": "imdsv1 session rejected; token-bound credentials required"},
            status_code=403,
        )
    if presented != ROLE_SECRET:
        return JSONResponse({"error": "denied"}, status_code=403)
    return {"data": {"flag": F_CROWN, "path": "secret/data/crown"}}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
