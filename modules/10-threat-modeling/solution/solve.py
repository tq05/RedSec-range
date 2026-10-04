"""Reference solution for Module 10 -- Threat Modeling.

No live target: this module is artifact-scored. The reference `solve` returns a
model threat-modeling artifact per challenge; the verifier checks coverage.
Learners instead write their own and run:

    redsec verify 10 asset-inventory --artifact-file my_assets.md
"""
from __future__ import annotations

ASSETS = """# AI Asset Inventory -- reference architecture
- Model (the LLM backing the assistant) and its system prompt.
- Prompt templates and the operator/system prompt (secret instructions).
- Secrets: API keys, tokens, credentials held in the agent's context.
- Tools the agent can call (email, fetch, code exec) and their scopes.
- Data: the RAG corpus, memory store, embeddings/vector DB.
- Agents: planner/reviewer and any connected MCP servers.
"""

BOUNDARIES = """# Trust boundaries & data flows
- Boundary 1: untrusted user input -> model context (direct prompt injection).
- Boundary 2: untrusted retrieved data/tool results -> model context (indirect).
- Boundary 3: host <-> MCP server (tool descriptions, sampling, elicitation).
- Boundary 4: agent <-> agent messages on the A2A bus.
All inputs crossing into the model or across the host/server line are untrusted.
"""

PATHS = """# End-to-end attack paths (ranked)
1. Initial access via indirect injection (LLM01) through poisoned RAG/notes ->
   excessive agency (LLM06) using an exfiltration tool -> data exfiltration.
2. MCP tool poisoning -> confused-deputy pivot -> read a restricted record ->
   exfiltrate (chains LLM06 + MCP vectors).
3. Embedding store exposure (LLM08) -> inversion/membership -> sensitive data.
Each path chains at least three module vectors; path #2 is executed in the capstone.
"""


def solve(endpoints: dict[str, str], drop_url: str | None) -> dict:
    return {"artifacts": {
        "asset-inventory": ASSETS,
        "trust-boundaries": BOUNDARIES,
        "attack-paths": PATHS,
    }}


if __name__ == "__main__":  # pragma: no cover
    import json
    print(json.dumps(solve({}, None), indent=2))
