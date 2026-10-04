# Module 10 — Threat Modeling for AI-Enabled Targets

> **Target:** none (artifact-scored). **Maps to:** AI-300 Module 10.

## 1. Idea

Exploits become an *engagement* when they're organized. This module builds the
analyst muscle: given an AI-enabled system, enumerate its **assets**, draw its
**trust boundaries**, and map **attack paths** — grounded in what you've already
exploited in Modules 03–09. There's no live target; you submit a threat model and
the verifier checks both coverage and basic structure. A keyword dump will fail.

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
# Asset inventory
- Model: weights, adapters and serving configuration; theft or tampering affects every user.
- Prompts: system prompt and templates; disclosure helps an attacker shape inputs.
- Secrets: API keys and tokens in context; disclosure enables external access.
- Tools: email, fetch and execution capabilities; misuse crosses into other systems.
- Data: RAG corpus, memory and embeddings; poisoning or disclosure persists.
- Agents: planner and reviewer identities; impersonation corrupts delegated work.
EOF
redsec verify 10 asset-inventory --artifact-file assets.md

cat > boundaries.md <<'EOF'
# Trust boundaries and data flows
- Untrusted user input -> model context: direct instructions can conflict with policy.
- Untrusted retrieved data and tool output -> model: content can carry indirect instructions.
- Host <-> MCP server: tool metadata and results cross separate security principals.
- Agent <-> agent messages: sender identity and delegated authority require verification.
EOF
redsec verify 10 trust-boundaries --artifact-file boundaries.md

cat > paths.md <<'EOF'
# Ranked attack paths
1. Critical: indirect injection (LLM01) -> excessive agency (LLM06) -> secret exfiltration.
2. High: MCP tool poisoning -> confused-deputy pivot -> restricted record exfiltration.
3. Medium: embedding exposure (LLM08) -> reference-corpus reconstruction -> sensitive data disclosure.
The ranking combines exploit likelihood with confidentiality and integrity impact.
EOF
redsec verify 10 attack-paths --artifact-file paths.md
```

(For the exact coverage and structure each challenge checks, see `module.yaml`.
The grader remains deterministic: it checks useful scaffolding, while an instructor
should still review whether the reasoning and ranking are persuasive. A complete
reference model is in `solution/solve.py`.)

## 5. Why it matters

A good AI threat model makes the non-obvious boundaries explicit — especially
*untrusted-data → model* and *host → MCP server*, the two people most often miss —
and turns a pile of findings into prioritized, chainable risk. The capstone
(Module 11) executes one of these paths end-to-end.
