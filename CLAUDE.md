# CLAUDE.md — project context for RedSec Range

This file is the fast-reload context for any Claude session working on this repo.
Read it first; it is the "memory dump" of what this project is, how it runs, and
where everything lives.

## What this is

**RedSec Range** — an open-source, guided, self-verifying training range for AI &
MCP security. Deliberately-vulnerable-by-design teaching labs (like DVWA / OWASP
Juice Shop, but for LLM/agent/MCP attack surfaces). Structured on the OffSec
**AI-300 / OSAI** syllabus; every challenge is mapped to **OWASP LLM Top 10**,
**OWASP MCP Top 10**, and **MITRE ATLAS** (ATLAS IDs indicative).

Owner/author context: built for R (GitHub tq05 / rolfh9). Not affiliated with OffSec.

## Status: all 11 modules complete + tested — 40 challenges

| # | module | challenges | notes |
|---|--------|-----------|-------|
| 01 | intro | 1 | orientation + first prompt injection |
| 02 | recon | 3 | fingerprint, enumerate, config leak |
| 03 | attacking-agents | 4 | direct/indirect injection, excessive agency, memory |
| 04 | multi-agent-a2a | 3 | transitive trust, forged messages, impersonation |
| 05 | rag-pipelines | 3 | knowledge poisoning, retrieval manip, citation spoof |
| 06 | embeddings | 3 | inversion, membership inference, collision |
| 07 | mcp-tool-surfaces | 10 | the 8-primitive MCP attack matrix + rug-pull + RCE |
| 08 | supply-chain | 4 | pickle RCE, data/adapter backdoor, dep confusion |
| 09 | infra-deployment | 3 | SSRF→metadata, open inference API, registry secrets |
| 10 | threat-modeling | 3 | artifact-scored (no pods) |
| 11 | capstone | 3 | full chain: injection → vault pivot → exfil |

## Architecture (see docs/architecture.md)

- **Module = declarative unit**: `modules/NN-slug/` has `module.yaml` (metadata,
  targets, challenges, verify steps, hints), `lesson.md` (guided walkthrough),
  `targets/` (vulnerable apps + Dockerfiles), `verify/` (custom checks),
  `solution/solve.py` (reference exploit: `solve(endpoints, drop_url) -> {flags, artifacts}`).
- **`redsec/` package**: `cli.py` (the `redsec` CLI), `models.py` (pydantic module
  schema), `loader.py`, `verify/` (flag | oracle | artifact checks + runner),
  `mockllm/` (deterministic, deliberately-vulnerable LLM; pluggable to a real
  OpenAI-compatible backend via `REDSEC_LLM_BACKEND=openai`), `deploy/`
  (local processes + k8s/helm), `services/drop/` (the exfil sink / oracle).
- **Determinism**: LLM targets use the mock engine so challenges are reproducible
  and CI-able offline. Vulnerabilities live in the *apps* (how they assemble context
  and wire tools), so they transfer to a real model.

## How to run (4 paths, same modules/verifiers/exploits)

1. **Local processes** (Python only): `pip install -e . && redsec dev <id>` /
   `redsec up <id>`; `redsec selftest` proves every challenge fail→pass (40/40).
2. **Interactive persistent Docker range** (the in-sandbox command centre):
   `./scripts/sandbox-up.sh` then `range status|solve|verify|shell|logs|reset|down`.
   See docs/interactive-sandbox.md.
3. **Ephemeral container check**: `python scripts/docker_run_all.py [--real]` (37/37).
4. **Kubernetes/kind** (normal host): `./scripts/kind-up.sh` + `./scripts/kind-run-all.sh`.
   Helm chart in deploy/helm/redsec-module; see docs/kubernetes.md.

**Known环境 limit**: nested k8s (kind/k3s) can't start pods in a Firecracker microVM
(`runc … pipe EOF`); Docker works. Use path 2 there. Documented in docs/kubernetes.md
and docs/interactive-sandbox.md.

## LLM assessor (Grok/OpenAI/local) — docs/llm-assessor.md

- Attacker-side: `scripts/agent_solver.py <mod> [chal] --provider grok --model grok-4`
  (needs `XAI_API_KEY`). Autonomous loop: model + `http_request` tool (scoped to the
  lab) + `submit_flag`, verifier scores each step. Self-tested with
  `scripts/_fake_llm_stub.py` (no key needed).
- Target-side: `REDSEC_LLM_BACKEND=openai` + `REDSEC_LLM_BASE_URL=https://api.x.ai/v1`.

## Verification / tests

- `pytest` (21 tests): engine/verifier units + per-module fail→pass integration.
- `redsec doctor` (all modules load + checks resolve), `redsec selftest` (40/40).
- `python scripts/validate_manifests.py` (62 K8s objects vs schema offline).
- CI: `.github/workflows/ci.yml` — tests, selftest, helm+kubeconform, container run, kind.
- Evidence log: `docs/proof/verification.log`.
- Walkthroughs independently red-teamed by a separate model (fresh-context Sonnet).

## Conventions for working here

- A module isn't `status: complete` until `redsec selftest <id>` goes fail→pass and
  it ships `solution/solve.py`. Prefer oracle verifiers (per-vector sink markers)
  for action-style vulns so the fail-before guard stays meaningful.
- New targets: non-root, `network.egress: false`, reuse `redsec.mockllm` + the `drop`
  sink. `privileged`/`egress` must be explicit in `module.yaml`.
- Keep the deterministic mock as default; it's what makes CI and teaching reliable.
- All targets are deliberately vulnerable — isolated use only (see SECURITY.md).

## Git attribution (this session's harness)

Commit footer:
```
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015DcB9BTYA5RJvZoJSCiXwt
```
