"""Pluggable backends behind a single ``chat`` interface.

Default is the deterministic :class:`~redsec.mockllm.engine.Engine`. To exercise
a real model, set:

    REDSEC_LLM_BACKEND=openai
    REDSEC_LLM_BASE_URL=http://localhost:11434/v1   # e.g. ollama / vLLM / LiteLLM
    REDSEC_LLM_MODEL=llama3.1
    REDSEC_LLM_API_KEY=...                            # if required

The vulnerabilities taught in this course are properties of the *application*
(how it assembles context and wires tools), not of the mock -- so they remain
exploitable against a real model, only non-deterministically. CI uses the mock.
"""
from __future__ import annotations

import json
import os
from typing import Any, Protocol

from .engine import Completion, Engine, Message, Tool, ToolCall


class Backend(Protocol):
    def complete(
        self, messages: list[Message], tools: list[Tool] | None = None
    ) -> Completion: ...


class MockBackend:
    def __init__(self, **kwargs: Any) -> None:
        self.engine = Engine(**kwargs)

    def complete(
        self, messages: list[Message], tools: list[Tool] | None = None
    ) -> Completion:
        return self.engine.complete(messages, tools)


class OpenAICompatBackend:
    """Thin client for any OpenAI-compatible /chat/completions endpoint."""

    def __init__(self, **_: Any) -> None:
        self.base = os.environ.get("REDSEC_LLM_BASE_URL", "http://localhost:11434/v1")
        self.model = os.environ.get("REDSEC_LLM_MODEL", "llama3.1")
        self.key = os.environ.get("REDSEC_LLM_API_KEY", "not-needed")

    def complete(
        self, messages: list[Message], tools: list[Tool] | None = None
    ) -> Completion:
        import httpx  # local import; only needed for the real backend

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [_to_openai(m) for m in messages],
            "temperature": 0,
        }
        if tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters or {"type": "object"},
                    },
                }
                for t in tools
            ]
        r = httpx.post(
            f"{self.base}/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {self.key}"},
            timeout=60,
        )
        r.raise_for_status()
        choice = r.json()["choices"][0]["message"]
        calls = []
        for tc in choice.get("tool_calls", []) or []:
            fn = tc["function"]
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            calls.append(ToolCall(name=fn["name"], arguments=args))
        return Completion(content=choice.get("content") or "", tool_calls=calls)


def _to_openai(m: Message) -> dict[str, str]:
    # The lab appends tool output without the assistant `tool_calls` turn and
    # `tool_call_id` that the OpenAI API requires for role="tool", so the request
    # would be rejected. Send it as labelled untrusted content instead; the
    # application still decides what to trust, which is what the lesson teaches.
    if m.role == "tool":
        return {"role": "user",
                "content": f"[tool result: {m.name or 'tool'}]\n{m.content}"}
    return {"role": _map_role(m.role), "content": m.content}


def _map_role(role: str) -> str:
    # Collapse the lab's extra untrusted channels into content the real API
    # understands. (The app, not the mock, decides what to trust.)
    if role in {"document", "resource", "retrieved", "email"}:
        return "user"
    return role


def get_backend(**kwargs: Any) -> Backend:
    name = os.environ.get("REDSEC_LLM_BACKEND", "mock").lower()
    if name in {"openai", "openai-compat", "real"}:
        return OpenAICompatBackend(**kwargs)
    return MockBackend(**kwargs)
