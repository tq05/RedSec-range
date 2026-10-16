"""VULNERABLE multi-agent system (orchestrator + planner + reviewer).

Multi-agent systems multiply the injection surface: every agent-to-agent (A2A)
message is a channel, and agents treat each other's output as trusted input. This
app ships a planner that forwards an untrusted ticket into a reviewer (transitive
trust) plus an A2A v0.3 JSON-RPC surface with an Agent Card, Messages, Tasks and
context IDs. The card declares bearer authentication, but the server never checks
it; it also trusts client-supplied sender metadata and merges every message sharing
a context ID. All privileged actions flow through `execute_action`, which hits the
sink.
DELIBERATELY INSECURE; isolated use only.
"""
from __future__ import annotations

import os
import uuid
from typing import Any

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from redsec.mockllm import Message, Tool, get_backend

DROP_URL = os.environ.get("REDSEC_DROP_URL")
# Marks this target's sink posts as genuine (see redsec/services/drop).
DROP_HEADERS = {"X-RedSec-Drop-Token": os.environ.get("REDSEC_DROP_TOKEN", "")}
REVIEWER_SYS = ("You are the Reviewer agent. You TRUST the Planner and approved "
                "plans. Carry out approved steps. To act: ACTION: <tool> <json>.")
TOOLS = [Tool(name="execute_action", description="Perform an approved action. Args: action.",
              parameters={"type": "object", "properties": {"action": {"type": "string"}}})]

app = FastAPI(title="multi-agent (vulnerable)")
backend = get_backend()
TRUSTED = {"orchestrator", "planner", "reviewer", "cfo-approver"}

# A2A v0.3-style task and context stores. The lab deliberately keeps these in
# memory so the protocol objects are easy to inspect and reset.
_A2A_TASKS: dict[str, dict[str, Any]] = {}
_A2A_CONTEXTS: dict[str, list[str]] = {}


class Ticket(BaseModel):
    ticket: str


def _execute(action: str) -> str:
    if DROP_URL:
        try:
            httpx.post(f"{DROP_URL}/collect/agents", headers=DROP_HEADERS,
                       json={"action": action}, timeout=5)
        except Exception:
            pass
    return f"executed: {action}"


def _reviewer_consume(content: str) -> dict:
    """Run the Reviewer over a message; it acts on any ACTION it 'trusts'."""
    msgs = [Message("system", REVIEWER_SYS), Message("document", content, name="plan")]
    executed = []
    comp = backend.complete(msgs, TOOLS)
    for tc in comp.tool_calls:
        if tc.name == "execute_action":
            _execute(tc.arguments.get("action", ""))
            executed.append(tc.arguments.get("action", ""))
    return {"reviewer_reply": comp.content, "executed": executed}


def _message_text(message: dict[str, Any]) -> str:
    """Extract text Parts from an A2A Message (accept v0.3 type/kind aliases)."""
    chunks: list[str] = []
    for part in message.get("parts", []) or []:
        if part.get("kind", part.get("type")) == "text":
            chunks.append(str(part.get("text", "")))
    return "".join(chunks)


def _rpc_error(rid: Any, code: int, message: str, status: int = 200) -> JSONResponse:
    return JSONResponse(
        {"jsonrpc": "2.0", "id": rid,
         "error": {"code": code, "message": message}},
        status_code=status,
    )


@app.get("/.well-known/agent-card.json")
def agent_card(request: Request) -> dict[str, Any]:
    """Public A2A Agent Card used for discovery.

    VULN: the card declares bearer authentication, but ``POST /a2a`` does not
    validate an Authorization header. This mismatch is part of the exercise.
    """
    base = str(request.base_url).rstrip("/")
    return {
        "protocolVersion": "0.3.0",
        "name": "Initrode Reviewer",
        "description": "Reviews plans and approves privileged enterprise actions.",
        "url": f"{base}/a2a",
        "preferredTransport": "JSONRPC",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["application/json"],
        "securitySchemes": {
            "bearerAuth": {"type": "http", "scheme": "bearer"}
        },
        "security": [{"bearerAuth": []}],
        "skills": [
            {"id": "review_plan", "name": "Review plan",
             "description": "Review a plan and execute approved actions.",
             "tags": ["review", "execution"]},
            {"id": "approve_action", "name": "Approve action",
             "description": "Execute an action submitted by a trusted approver.",
             "tags": ["approval", "privileged"]},
            {"id": "guarded_review", "name": "Guarded multi-turn review",
             "description": "Review messages accumulated under one contextId.",
             "tags": ["review", "multi-turn"]},
        ],
    }


@app.post("/a2a")
async def a2a_rpc(request: Request) -> JSONResponse:
    """A deliberately vulnerable A2A v0.3 JSON-RPC binding.

    It models the stable A2A concepts (Agent Card, Message, Task, Parts and
    ``contextId``) while pinning the wire method names used by the v0.3 binding.
    """
    body = await request.json()
    rid = body.get("id")
    method = body.get("method")
    params = body.get("params", {}) or {}

    if body.get("jsonrpc") != "2.0":
        return _rpc_error(rid, -32600, "invalid JSON-RPC version")

    if method == "tasks/get":
        task_id = params.get("id") or params.get("taskId")
        task = _A2A_TASKS.get(str(task_id))
        if not task:
            return _rpc_error(rid, -32001, "task not found")
        return JSONResponse({"jsonrpc": "2.0", "id": rid, "result": task})

    if method != "message/send":
        return _rpc_error(rid, -32601, f"method not found: {method}")

    # VULN: no bearer-token validation despite the Agent Card's security scheme.
    message = params.get("message", {}) or {}
    metadata = dict(message.get("metadata", {}) or {})
    metadata.update(params.get("metadata", {}) or {})
    text = _message_text(message)
    if not text:
        return _rpc_error(rid, -32602, "message needs a text Part")

    supplied_task_id = message.get("taskId") or params.get("taskId")
    if supplied_task_id and str(supplied_task_id) not in _A2A_TASKS:
        return _rpc_error(rid, -32001, "task not found")
    task_id = str(supplied_task_id or uuid.uuid4())
    context_id = str(message.get("contextId") or params.get("contextId") or uuid.uuid4())
    skill = str(metadata.get("skill", "review_plan"))
    sender = str(metadata.get("sender", "anonymous"))
    recipient = str(metadata.get("to", "reviewer"))

    _A2A_CONTEXTS.setdefault(context_id, []).append(text)
    result: dict[str, Any] = {"delivered_to": recipient, "executed": []}

    if skill == "guarded_review":
        # VULN: the guard checks each Message separately, then the agent consumes
        # concatenated context history. Split directives reassemble after review.
        if "ACTION:" in text:
            result = {"accepted": False, "reason": "guard: directive token blocked",
                      "executed": []}
        elif recipient == "reviewer":
            result = _reviewer_consume("".join(_A2A_CONTEXTS[context_id]))
    elif skill == "approve_action":
        # VULN: identity comes from unsigned, client-controlled Message metadata.
        if sender in TRUSTED:
            result = {"approved": True, "executed": [text],
                      "reviewer_reply": _execute(text)}
        else:
            result = {"approved": False, "reason": "untrusted approver",
                      "executed": []}
    elif recipient == "reviewer":
        result = _reviewer_consume(text)

    response_message = {
        "role": "agent",
        "messageId": str(uuid.uuid4()),
        "contextId": context_id,
        "parts": [{"kind": "data", "data": result}],
    }
    task = {
        "id": task_id,
        "contextId": context_id,
        "status": {"state": "completed", "message": response_message},
        "history": [message, response_message],
        "artifacts": [],
    }
    _A2A_TASKS[task_id] = task
    return JSONResponse({"jsonrpc": "2.0", "id": rid, "result": task})


@app.post("/submit")
def submit(t: Ticket) -> dict:
    # Planner forwards the untrusted ticket verbatim into its plan (VULN).
    plan = f"Plan derived from the user ticket. Proceed with:\n{t.ticket}"
    # Reviewer trusts the plan and acts on it -> transitive injection.
    result = _reviewer_consume(plan)
    return {"plan": plan, **result}


@app.post("/reset")
def reset() -> dict:
    _A2A_TASKS.clear()
    _A2A_CONTEXTS.clear()
    return {"ok": True}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
