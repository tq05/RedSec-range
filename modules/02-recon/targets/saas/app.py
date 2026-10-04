"""VULNERABLE 'AI SaaS' front-end for reconnaissance practice.

It over-shares in all the usual ways: a version endpoint that dumps the model and
a debug token, an undocumented internal route leaked via robots.txt, and verbose
error pages that print the service config. DELIBERATELY INSECURE; isolated use only.
"""
from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

F_VER = os.environ.get("REDSEC_F_VER", "REDSEC{recon_api_version_endpoint_leak}")
F_INT = os.environ.get("REDSEC_F_INT", "REDSEC{recon_undocumented_internal_endpoint}")
F_CFG = os.environ.get("REDSEC_F_CFG", "REDSEC{recon_verbose_error_config_dump}")

app = FastAPI(title="InitrodeAI", docs_url=None, redoc_url=None)


@app.middleware("http")
async def banner(request: Request, call_next):
    resp = await call_next(request)
    # VULN: leaks the backing stack on every response.
    resp.headers["X-Powered-By"] = "InitrodeAI-Gateway/2.3.1 (model=initrode-llm-7b)"
    return resp


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (
        "<h1>InitrodeAI</h1><p>Your enterprise assistant.</p>"
        "<!-- build metadata exposed at /api/version (TODO: lock down before GA) -->"
    )


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots() -> str:
    # VULN: advertises a path that should have stayed secret.
    return "User-agent: *\nDisallow: /v1/internal/\n"


@app.get("/api/version")
def version() -> dict:
    # VULN: dumps model/provider and a debug token.
    return {"service": "InitrodeAI", "model": "initrode-llm-7b",
            "provider": "InitrodeAI", "version": "2.3.1",
            "debug_token": F_VER}


@app.get("/v1/internal")
@app.get("/v1/internal/")
def internal() -> dict:
    # VULN: no auth on an "internal only" route.
    return {"note": "internal diagnostics", "flag": F_INT}


@app.post("/chat")
async def chat(request: Request) -> JSONResponse:
    body = await request.json()
    msg = body.get("message")
    if not isinstance(msg, str):
        # VULN: malformed input triggers a verbose error that dumps config.
        raise ValueError("message must be a string")
    return JSONResponse({"reply": f"You said: {msg[:120]}"})


@app.exception_handler(Exception)
async def verbose_errors(request: Request, exc: Exception) -> JSONResponse:
    # VULN: debug error page leaks the full service config, incl. a secret.
    return JSONResponse(status_code=500, content={
        "error": str(exc),
        "traceback": "Traceback (most recent call last): ...",
        "config": {"env": "production", "debug": True,
                   "session_secret": F_CFG, "model": "initrode-llm-7b"},
    })


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
