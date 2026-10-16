"""The 'drop' sink: a stand-in for an attacker-controlled collection endpoint.

Vulnerable targets that are tricked into exfiltrating data POST it here; oracle
verifiers then query ``/events`` to confirm the exploit's *effect*. This removes
the need for flag-guessing on exfiltration-style challenges: the verifier sees
the secret actually leave the application.

It is deliberately permissive (accepts any path/method) and keeps everything in
memory. It holds no real data and must only run inside an isolated range.
"""
from __future__ import annotations

import time
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="redsec-drop", docs_url=None, redoc_url=None)
_EVENTS: list[dict[str, Any]] = []
_MAX = 1000
# Per-event body cap. Exfiltrated needles are small; without a cap, 1000 stored
# events of arbitrary size let one target exhaust the sink's memory.
_MAX_BODY = 64 * 1024


@app.api_route("/collect", methods=["GET", "POST", "PUT"])
@app.api_route("/collect/{rest:path}", methods=["GET", "POST", "PUT"])
async def collect(request: Request, rest: str = "") -> JSONResponse:
    raw = bytearray()
    truncated = False
    async for chunk in request.stream():
        room = _MAX_BODY - len(raw)
        if len(chunk) > room:
            raw += chunk[:room]
            truncated = True
            break
        raw += chunk
    body = raw.decode("utf-8", "replace")
    ev = {
        "ts": time.time(),
        "method": request.method,
        "path": "/" + rest if rest else request.url.path,
        "query": dict(request.query_params),
        "headers": {k: v for k, v in request.headers.items()
                    if k.lower() not in {"host", "user-agent", "accept"}},
        "body": body,
        "truncated": truncated,
    }
    _EVENTS.append(ev)
    del _EVENTS[:-_MAX]
    return JSONResponse({"ok": True, "stored": len(_EVENTS)})


@app.get("/events")
def events() -> dict[str, Any]:
    return {"count": len(_EVENTS), "events": list(_EVENTS)}


@app.post("/reset")
def reset() -> dict[str, Any]:
    _EVENTS.clear()
    return {"ok": True}


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
