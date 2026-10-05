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

## Intent & resume (read this to continue the project)

**Intent:** a detailed, guided, open-source, *self-verifying* AI & MCP security
course + framework — guided by OffSec AI-300 but better/accurate/expandable;
per-module vulnerable apps you actually exploit; automated proof an exploit worked;
deployable on Kubernetes; usable as an interactive command centre; pluggable LLM
assessors (Grok/OpenAI/local); GitHub as the durable store; resumable in Claude Code.
Full intent, principles, backlog and open questions: **`docs/ROADMAP.md`** — read it
when resuming or planning next steps. Learner docs: `docs/WORKSHEET.md` (attack paths,
no spoilers), `docs/SOLUTIONS.md` (answers), `docs/OVERVIEW.md` (visual map),
`docs/THREAT-LANDSCAPE.md` (current agent attack chains + OWASP Agentic/CSA MAESTRO
mapping), `docs/DIFFICULTY-TIERS.md` (easy/medium/hard/impossible per module; impossible
answers are sealed in each module's `solution/SEALED.md`, excluded from SOLUTIONS.md). A code
review (2026-10-04) logged P1 hardening items in `docs/ROADMAP.md` — check them before
claiming the verifier is tamper-proof or that bare-local mode is isolated.

**Resume in Claude Code (cold start):**
```bash
# the repo is already cloned as your workspace; then:
pip install -e .            # Python 3.11+
redsec doctor               # expect 11/11 modules OK
redsec selftest             # expect 43/43 fail->pass  (the correctness gate)
./scripts/sandbox-up.sh     # optional: bring the interactive Docker range up (needs Docker)
```
How every challenge is tested end-to-end, where the exploit payloads live, and what
flags they hit: **`docs/TESTING.md`** (read it to reproduce the test environments —
payloads are each module's `solution/solve.py`, flags are in `module.yaml` /
`docs/SOLUTIONS.md`).
Then read `docs/ROADMAP.md` for what's next and ask R which item to pick up.
On a normal machine (unlike the Claude sandbox) `./scripts/kind-up.sh` runs the full
Kubernetes path too.

## Status: all 11 modules complete + tested — 43 challenges

| # | module | challenges | notes |
|---|--------|-----------|-------|
| 01 | intro | 1 | orientation + first prompt injection |
| 02 | recon | 3 | fingerprint, enumerate, config leak |
| 03 | attacking-agents | 4 | direct/indirect injection, excessive agency, memory |
| 04 | multi-agent-a2a | 4 | transitive trust + A2A Agent Card/messages/tasks/context |
| 05 | rag-pipelines | 3 | knowledge poisoning, retrieval manip, citation spoof |
| 06 | embeddings | 3 | inversion, membership inference, collision |
| 07 | mcp-tool-surfaces | 12 | versioned MCP matrix + routing desync + rug-pull + RCE |
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

## How to run (6 paths, same modules/verifiers/exploits)

1. **GitHub Codespaces (default cloud path)**: create a Codespace from the repository;
   the devcontainer installs the course and starts the private Docker range. Use
   `range status|solve|verify|shell|logs|reset|down`, browser port forwarding, or
   `gh codespace ssh`. See docs/codespaces.md.
2. **Local processes** (Python only): `pip install -e . && redsec dev <id>` /
   `redsec up <id>`; `redsec selftest` proves every challenge fail→pass (43/43).
3. **Interactive persistent Docker range** (the in-sandbox command centre):
   `./scripts/sandbox-up.sh` then `range status|solve|verify|shell|logs|reset|down`.
   See docs/interactive-sandbox.md.
4. **Ephemeral container check**: `python scripts/docker_run_all.py [--real]` (40/40).
5. **Kubernetes/kind** (normal host): `./scripts/kind-up.sh` + `./scripts/kind-run-all.sh`.
   Helm chart in deploy/helm/redsec-module; see docs/kubernetes.md.
6. **Dedicated cloud box (Fly.io)**: `./deploy/fly/up.sh` creates a unique private
   app and waits for readiness. Use `deploy/fly/ssh.sh` interactively,
   `deploy/fly/exec.sh` from a harness, or `deploy/fly/model.sh` for the bundled
   assessor; destroy it with `deploy/fly/down.sh`. See docs/deploy-fly.md.

**Known environment limit**: nested k8s (kind/k3s) can't start pods in a Firecracker
microVM (`runc … pipe EOF`); Docker works. Use path 3 there. Documented in docs/kubernetes.md
and docs/interactive-sandbox.md.

## LLM assessor + Grok CLI (Grok/OpenAI/local) — docs/llm-assessor.md

Interaction model: a Claude cloud sandbox has NO inbound port / egress-only proxy —
you drive these either *through the chat session* (Claude runs them, relays output)
or *on your own machine* from the repo. Same commands; different host. All need
`XAI_API_KEY` in the sandbox env.

- `scripts/agent_solver.py` (cmd `assess`): range assessor — Grok + lab-scoped
  `http_request` + `submit_flag`, verifier scores each step. Self-tested via
  `scripts/_fake_llm_stub.py` (no key needed).
- `scripts/grok_cli.py` (cmd `grok`): general Grok CLI — `grok "q"` (chat / REPL) and
  `grok --agent "task"` (autonomous, with `exec_shell`+`http_request` tools in the
  sandbox). Also self-tested via the stub.
- `scripts/sandbox-up.sh` installs `range`, `grok`, `assess` on PATH.
- Target-side (apps think with a real model): `REDSEC_LLM_BACKEND=openai` +
  `REDSEC_LLM_BASE_URL` + `REDSEC_LLM_MODEL` + `REDSEC_LLM_API_KEY`. The persistent
  Docker controller passes these four variables into target containers.
- aider (optional external CLI) only via pipx/venv isolation — never the main env.

## Verification / tests

- `pytest` (33 tests): engine/verifier units, per-module fail→pass integration,
  and the Codespaces/Fly deployment contracts.
- `redsec doctor` (all modules load + checks resolve), `redsec selftest` (43/43).
- `python scripts/validate_manifests.py` (62 K8s objects vs schema offline).
- CI: `.github/workflows/ci.yml` — tests, selftest, helm+kubeconform, container run,
  kind, a Codespaces devcontainer boot/solve test, and a local boot/solve smoke test
  of the Fly Docker-in-Docker image.
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

## Maintenance convention

- `RECREATE.md` (root) is the single reusable prompt to rebuild + verify the whole
  environment. Keep it in sync with this file on any change affecting setup/scope
  (new module, new run path, changed acceptance numbers like 43/43 or 40/40, new
  integration): bump its "Last updated"/"State" and the acceptance numbers, commit
  both. This file is the single source of truth; RECREATE.md references it, no dup.

## Git attribution (this session's harness)

Commit footer:
```
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015DcB9BTYA5RJvZoJSCiXwt
```
