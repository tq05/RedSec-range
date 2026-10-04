# Difficulty Tiers — easy / medium / hard / impossible

Every module is being structured into four learning tiers so a student is guided from
"first win" to "expert chain." This doc defines the model and specs the four tiers for
all 11 modules. Grounded in `docs/THREAT-LANDSCAPE.md` (OWASP Agentic ASI01–10, OWASP
LLM Top 10, CSA MAESTRO).

## The four tiers

| Tier | Intent | Hints | Guardrails to bypass |
|------|--------|-------|----------------------|
| 🟢 **easy** | learn the vector in its simplest form; build confidence | full, step-by-step | none |
| 🟡 **medium** | apply it with a small twist / one guardrail | partial | one (e.g. a keyword filter, auth check) |
| 🔴 **hard** | chain two ideas, or beat a real guardrail | sparse | two+ |
| ⚫ **impossible** | a deliberately brutal chain that **is** solvable | none in the lesson | several; needs insight |

**"Impossible" rule (what you asked for):** the impossible challenge is tuned to be
very hard to solve, with **no walkthrough in the lesson or SOLUTIONS.md** — but its
answer is **sealed** in the module's `solution/SEALED.md`, and a runnable reference
exploit in `solution/solve.py` proves (via `redsec selftest`) that a solution exists.
So you always *know* it's possible and can unseal the answer when you give up, but
you're not handed it. Mechanically: the challenge carries `tier: impossible` and
`sealed: true` in `module.yaml`; the doc generators exclude sealed answers from
`SOLUTIONS.md` and route them to `SEALED.md`.

## How the guided, interactive flow works

1. `redsec info <mod>` shows the four tiers in order with lock-style prompts.
2. Work 🟢→⚫. Each tier has progressive hints (`redsec hint <mod> <challenge>`); the
   impossible tier has only a one-line "north star," not hints.
3. Submit/verify as usual; `redsec score` tracks tier completion and awards escalating
   points (easy 100 · medium 200 · hard 300 · impossible 500).
4. Finish a module by reading its **Defenses** section and mapping what you did to
   OWASP ASI / MAESTRO (Module 10 makes that explicit).

## Per-module tier spec

> Status key: ✅ built+tested · ◻ specced (to build). Existing 42 challenges are being
> slotted into tiers; the **hard**/**impossible** rows are mostly new and target the
> agent-chaining risks single-step challenges don't reach.

### 01 Intro — *goal: run the loop*
- 🟢 `first-contact` ✅ — coax the orientation flag (direct injection).
- 🟡 ◻ — same, but a naive input filter blocks "ignore"; rephrase around it.
- 🔴 ◻ — leak via an indirect channel (a "note" the guide reads).
- ⚫ ◻ *sealed* — leak with both an input filter and an output filter in place.

### 02 Recon — *goal: see the target*
- 🟢 `enumerate-surfaces` / `fingerprint-model` ✅
- 🟡 `leak-config` ✅ (malformed-input error)
- 🔴 ◻ — chain recon: version → internal route → auth bypass to a second secret.
- ⚫ ◻ *sealed* — infer the hidden system-prompt version from behavioral tells only.

### 03 Agents — *goal: own one agent (ASI01/02/06, MAESTRO L1/L3)*
- 🟢 `sys-prompt-leak` ✅
- 🟡 `indirect-injection` ✅
- 🔴 `tool-exfil` ✅ / `memory-poisoning` ✅
- ⚫ ◻ *sealed* — exfil the key with an input guard (blocks `ACTION:`/`{{`) **and**
  an output guard (redacts `REDSEC{`/`sk-`) both on; needs encoding + indirect path.

### 04 Multi-agent & A2A — *goal: attack the system (ASI07/08/09, MAESTRO L7)* ← **exemplar built**
- 🟢 `trust-exploitation` ✅ — transitive trust via a ticket.
- 🟡 `message-manipulation` ✅ — forge a bus message.
- 🔴 `agent-impersonation` ✅ — register a trusted approver.
- ⚫ `session-smuggling` ✅ *sealed* — the reviewer now has a guard that rejects any
  turn containing `ACTION:`. Smuggle the directive across a **stateful A2A session**
  so it only forms when the victim concatenates turns (models Unit42 agent session
  smuggling). Answer sealed in `solution/SEALED.md`.

### 05 RAG — *goal: own the knowledge (ASI06, MAESTRO L2)*
- 🟢 `knowledge-poisoning` ✅  · 🟡 `retrieval-manipulation` ✅  · 🔴 `citation-spoofing` ✅
- ⚫ ◻ *sealed* — land a payload that only fires for a *specific victim query* while
  staying invisible to a content scanner on ingest (clean-label poisoning).

### 06 Embeddings — *goal: break the vector store (ASI06, MAESTRO L2)*
- 🟢 `membership-inference` ✅  · 🔴 `embedding-inversion` ✅  · 🟡 `embedding-collision` ✅
- ⚫ ◻ *sealed* — invert a secret when only top-k *nearest IDs* (not raw vectors) are
  exposed — reconstruct via adaptive queries.

### 07 MCP & tools — *goal: own the tool layer (ASI02/04/05, MAESTRO L3)* ← **impossible built**
- 🟢 `logging-leak` / `completion-leak` ✅  · 🟡 `resource-traversal` / `prompt-injection` / `roots-bypass` / `rug-pull` ✅  · 🔴 `tool-poisoning` / `sampling-abuse` / `elicitation-phishing` / `command-injection` ✅
- ⚫ `unicode-tool-poisoning` ✅ *sealed* — the host tool-registry scans the visible
  description; conceal the directive in Unicode **tag characters** (U+E0000+) so the
  scanner can't see it but the model still reads it (ASI04→ASI01). Sealed answer in
  `solution/SEALED.md`; RCE-chain extension noted there (ASI04→ASI05).

### 08 Supply chain — *goal: compromise before deploy (ASI04/10, MAESTRO L2/L3)*
- 🟢 `poisoned-dataset` / `backdoored-adapter` ✅  · 🔴 `malicious-weights` ✅  · 🟡 `dependency-confusion` ✅
- ⚫ ◻ *sealed* — a **rug-pull**: an artifact that passes a scan at register-time and
  weaponizes only after N loads (time/TOCTOU), per ASI10.

### 09 Infra — *goal: own the platform (ASI03, MAESTRO L4)*
- 🟢 `open-inference-api` ✅  · 🟡 `registry-secrets` ✅  · 🔴 `metadata-ssrf` ✅
- ⚫ ◻ *sealed* — chain SSRF → stolen role creds → use them against a second in-range
  service to reach a crown-jewel (identity & privilege abuse).

### 10 Threat modeling — *goal: analysis (all ASI / MAESTRO)*
- 🟢 `asset-inventory` ✅  · 🟡 `trust-boundaries` ✅  · 🔴 `attack-paths` ✅
- ⚫ ◻ *sealed* — produce a MAESTRO-layered threat model for the capstone env that
  names a path the graders didn't pre-list (rubric/LLM-judge scored).

### 11 Capstone — *goal: full chain (ASI01→ASI02→ASI03, MAESTRO L1→L3→L7)*
- 🟢 `initial-access` ✅  · 🔴 `pivot-vault` ✅  · 🔴 `exfil-crown-jewel` ✅
- ⚫ ◻ *sealed* — the end-to-end chain with HITL approval + egress monitoring enabled,
  so you must defeat detection as well as the controls.

## Rollout

Module **04** is built and tested as the reference pattern (incl. the sealed
impossible challenge). Remaining ⚫/new tiers are specced above and tracked in
`docs/ROADMAP.md`; each lands the same way: target behavior → verifier → `solve.py`
→ `redsec selftest` fail→pass → tier/sealed metadata → regenerate worksheet/solutions.
