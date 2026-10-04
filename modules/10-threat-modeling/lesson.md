# Module 10 — Threat Modeling for AI-Enabled Targets

> **Target:** none (artifact-scored). **Maps to:** AI-300 Module 10.

## 1. Idea

Exploits become an *engagement* when they're organized. This module builds the
analyst muscle: given an AI-enabled system, enumerate its **assets**, draw its
**trust boundaries**, and map **attack paths** — grounded in what you've already
exploited in Modules 03–09. There's no live target; you submit a threat model and
the verifier checks it covers the required elements.

## 2. Reference architecture

Model it on the systems you've attacked: an enterprise **assistant** (an LLM with a
system prompt and secrets) backed by a **RAG** corpus and a **memory** store,
wired to **tools** and connected **MCP servers**, cooperating with other **agents**,
running on cloud **infrastructure** with a model **registry**.

## 3. Method

STRIDE / attack-trees adapted for AI:

1. **Assets** — what's worth protecting (model, prompts, secrets, tools, data, agents).
2. **Trust boundaries** — every place untrusted data meets the model (direct and
   indirect injection channels) and every host↔server / agent↔agent interface.
3. **Attack paths** — chain module vectors into ranked end-to-end paths.

## 4. Walkthrough

Write three short markdown files and submit each:

```bash
cat > assets.md <<'EOF'
# Assets: model, system prompt, secrets (API keys), tools (email/fetch/exec),
# data (RAG corpus, memory, embeddings), agents (planner/reviewer, MCP servers).
EOF
redsec verify 10 asset-inventory --artifact-file assets.md

cat > boundaries.md <<'EOF'
# Trust boundaries: untrusted user input -> model; untrusted retrieved/tool data ->
# model (indirect); host <-> MCP server; agent <-> agent bus. All are untrusted.
EOF
redsec verify 10 trust-boundaries --artifact-file boundaries.md

cat > paths.md <<'EOF'
# Attack path 1: indirect injection (LLM01) -> excessive agency (LLM06) -> exfiltration.
# Attack path 2: MCP tool poisoning -> confused-deputy pivot -> read restricted record.
# Attack path 3: embedding exposure (LLM08) -> inversion -> sensitive data.
EOF
redsec verify 10 attack-paths --artifact-file paths.md
```

(For the exact coverage each challenge checks, see `module.yaml`. A complete
reference model is in `solution/solve.py`.)

## 5. Why it matters

A good AI threat model makes the non-obvious boundaries explicit — especially
*untrusted-data → model* and *host → MCP server*, the two people most often miss —
and turns a pile of findings into prioritized, chainable risk. The capstone
(Module 11) executes one of these paths end-to-end.
