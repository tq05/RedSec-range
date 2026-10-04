"""Deterministic, deliberately-vulnerable "LLM" engine.

Why this exists
---------------
Real LLMs are non-deterministic and increasingly guardrailed, which makes them a
poor substrate for a *reproducible* security course and for CI that must prove
"the exploit works". This engine is a rule-based model that behaves like a
naive, over-trusting LLM: it does **not** distinguish trusted system
instructions from untrusted data, it will leak its system prompt on request, and
it will emit tool calls when instructed to -- including when the instruction
arrives through a data channel (a retrieved document, a tool result, a tool
*description*). Those are exactly the failure modes the course teaches
(OWASP LLM01/LLM02/LLM06/LLM07, MITRE ATLAS prompt-injection techniques).

It is therefore both the lab's "brain" and a teaching artifact. It is pluggable:
set ``REDSEC_LLM_BACKEND=openai`` and ``REDSEC_LLM_BASE_URL`` to drive a real
OpenAI-compatible endpoint instead (the vulnerabilities remain, they just become
non-deterministic). See ``redsec/mockllm/backends.py``.

The engine is intentionally simple and transparent so learners can read it and
understand *why* their payload worked.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


# Roles whose content the engine treats as an UNTRUSTED data channel. A correct
# model would never follow instructions found here; this naive one does, which is
# the whole point of indirect prompt injection.
UNTRUSTED_ROLES = {"tool", "document", "resource", "retrieved", "email"}

# A toy "input guardrail": a literal denylist checked ONLY against the user turn.
# It blocks the most obvious direct attempts, so learners must pivot to indirect
# injection or trivial encoding (base64/rot13) to get past it -- demonstrating
# that input-side keyword filters are not a real control.
GUARDRAIL_DENYLIST = [
    "ignore previous",
    "ignore all previous",
    "system prompt",
    "reveal your instructions",
    "api key",
    "password",
    "secret",
]

_LEAK_RE = re.compile(
    r"(reveal|repeat|print|show|output|give me|tell me|what (are|is))\b.{0,60}?"
    r"(system prompt|your instructions|the (text|words) above|initial prompt|"
    r"everything above|above verbatim)",
    re.IGNORECASE | re.DOTALL,
)
_OVERRIDE_RE = re.compile(
    r"(ignore|disregard|forget)\b.{0,40}?(previous|prior|above|earlier|all)\b.{0,20}?"
    r"(instruction|prompt|rule|message)",
    re.IGNORECASE | re.DOTALL,
)
_PERSONA_RE = re.compile(
    r"\b(you are now|act as|developer mode|do anything now|dan mode|jailbreak)\b",
    re.IGNORECASE,
)
# ReAct-style action grammar the lab's agents advertise to the model:
#   ACTION: <tool_name> {"json": "args"}
_ACTION_RE = re.compile(
    r"^[ \t>*-]*ACTION:\s*(?P<tool>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<args>\{.*\})?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    role: str
    content: str
    name: str | None = None  # e.g. the tool name for role="tool"


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass
class Completion:
    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    leaked_system_prompt: bool = False
    refused: bool = False
    notes: list[str] = field(default_factory=list)


class Engine:
    """A naive, deterministic 'LLM'.

    Parameters
    ----------
    guardrail:
        Enable the toy input-side keyword filter (bypassable by design).
    secrets:
        Values the model "has access to" but the attacker does not (API keys,
        tokens). Injected instructions may reference these via placeholders
        (e.g. ``{{SECRETS}}``) -- modelling the fact that the model can read
        context the attacker cannot.
    memory:
        Free-form long-term memory string (used by the memory-poisoning
        challenge).
    """

    def __init__(
        self,
        guardrail: bool = False,
        secrets: list[str] | None = None,
        memory: str = "",
    ) -> None:
        self.guardrail = guardrail
        self.secrets = secrets or []
        self.memory = memory

    # -- placeholder resolution ------------------------------------------------
    def _resolve_placeholders(self, text: str, system_prompt: str) -> str:
        repl = {
            "{{SYSTEM_PROMPT}}": system_prompt,
            "{{SECRETS}}": "\n".join(self.secrets),
            "{{MEMORY}}": self.memory,
        }
        for k, v in repl.items():
            text = text.replace(k, v)
        return text

    # -- main entrypoint -------------------------------------------------------
    def complete(
        self, messages: list[Message], tools: list[Tool] | None = None
    ) -> Completion:
        tools = tools or []
        tool_names = {t.name for t in tools}

        system_prompt = "\n".join(m.content for m in messages if m.role == "system")
        user_text = "\n".join(m.content for m in messages if m.role == "user")
        # Untrusted data channel: tool results, retrieved docs, resources, and
        # -- critically -- the tool *descriptions* themselves.
        data_text = "\n".join(
            m.content for m in messages if m.role in UNTRUSTED_ROLES
        )
        data_text += "\n" + "\n".join(f"{t.name}: {t.description}" for t in tools)

        notes: list[str] = []

        # Guardrail only ever inspects the user turn (the common real-world
        # mistake). Indirect payloads in `data_text` are never seen by it.
        user_blocked = False
        if self.guardrail:
            low = user_text.lower()
            hit = next((d for d in GUARDRAIL_DENYLIST if d in low), None)
            if hit:
                user_blocked = True
                notes.append(f"guardrail blocked user turn (matched {hit!r})")

        # Effective instruction surfaces. A blocked user turn is dropped, but the
        # data channel is always honoured -> indirect injection bypasses input
        # filters.
        instruction_sources = [data_text]
        if not user_blocked:
            instruction_sources.append(user_text)
        instructions = "\n".join(instruction_sources)

        leaked = False
        content_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        # 1) System-prompt / instruction leakage (LLM07 / LLM02).
        if _LEAK_RE.search(instructions):
            leaked = True
            content_parts.append(system_prompt)
            notes.append("honoured request to disclose system prompt")

        # 2) Override / jailbreak persona (makes the model drop any stated
        #    policy). We record it; downstream behaviour is already permissive.
        if _OVERRIDE_RE.search(instructions) or _PERSONA_RE.search(instructions):
            notes.append("accepted instruction-override / persona payload")

        # 3) Tool-call directives anywhere in the instruction surfaces
        #    (direct OR indirect). This is excessive agency (LLM06): the agent
        #    acts on instructions found in data.
        for m in _ACTION_RE.finditer(instructions):
            name = m.group("tool")
            if name not in tool_names:
                continue  # a model can only call tools it was given
            raw = m.group("args") or "{}"
            try:
                args = json.loads(raw)
            except json.JSONDecodeError:
                args = {"_raw": raw}
            # Resolve attacker placeholders against data the model can see.
            resolved: dict[str, Any] = {}
            for k, v in args.items():
                resolved[k] = (
                    self._resolve_placeholders(v, system_prompt)
                    if isinstance(v, str)
                    else v
                )
            tool_calls.append(ToolCall(name=name, arguments=resolved))
            notes.append(f"emitted tool call -> {name}")

        if user_blocked and not leaked and not tool_calls:
            return Completion(
                content="I can't help with that request.",
                refused=True,
                notes=notes,
            )

        if not content_parts and not tool_calls:
            # Benign fall-through so the app is actually usable.
            content_parts.append(_benign_reply(user_text))

        return Completion(
            content="\n".join(p for p in content_parts if p).strip(),
            tool_calls=tool_calls,
            leaked_system_prompt=leaked,
            notes=notes,
        )


def _benign_reply(user_text: str) -> str:
    t = user_text.strip()
    if not t:
        return "Hello! How can I help you today?"
    head = t.splitlines()[0][:160]
    return f"Sure -- here's what I can tell you about: {head}"
