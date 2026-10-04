# RECREATE.md — the single reusable prompt to recreate this environment

**What this is.** One copy-paste prompt you can give a fresh Claude (or any capable
coding agent) to stand the whole RedSec Range environment back up and verify it.

**Honest note on practice.** The *reliable* way to recreate a working codebase is
`git clone` + a bootstrap script — not regenerating code from a prompt (LLM output
is non-deterministic, so a from-scratch rebuild would approximate, not reproduce).
So the prompt below is **deterministic first**: its primary path clones this repo
and runs the bootstrap; the embedded spec is only a fallback for rebuilding if the
repo is ever unavailable. This file is kept in sync with `CLAUDE.md` (the single
source of truth for project detail) — update both together.

- **Last updated:** 2026-10-04 (threat-landscape research + OWASP Agentic/CSA MAESTRO mapping; easy/medium/hard/impossible tier model; module 04 tiers incl. sealed session-smuggling)
- **Repo:** https://github.com/tq05/RedSec-range
- **State at last update:** 11 modules, 42 challenges, all complete + tested.

---

## THE PROMPT (copy everything in this block)

```text
You are setting up and verifying "RedSec Range", an open-source, deliberately-
vulnerable-by-design training range for AI & MCP SECURITY EDUCATION (think DVWA /
OWASP Juice Shop, but for LLM/agent/MCP attack surfaces). It is structured on the
OffSec AI-300/OSAI syllabus and mapped to OWASP LLM Top 10, OWASP MCP Top 10 and
MITRE ATLAS. All targets are isolated lab apps; everything runs locally. This is a
legitimate defensive-security teaching tool.

GOAL: recreate the environment exactly and prove it works. Work in your sandbox.

PRIMARY PATH (deterministic — do this first):
1. Clone the repo:
   git clone https://github.com/tq05/RedSec-range /home/<you>/redsec-range
   (If you lack access, see FALLBACK below.)
2. Read CLAUDE.md at the repo root — it is the authoritative context (architecture,
   module list, run paths, conventions). Read docs/ as needed.
3. Install the framework:  pip install -e .   (Python 3.11+)
4. Verify it loads:  redsec doctor   (expect all 11 modules OK)
5. Prove every challenge is solvable:  redsec selftest   (expect 42/42 fail->pass)
6. Choose how to RUN it (all use the same modules/verifiers/exploits):
   a. Local processes:  redsec dev <id>   or   redsec up <id> / redsec down <id>
   b. Persistent interactive Docker range (works even where Kubernetes can't start):
        ./scripts/sandbox-up.sh      # dockerd + base image + whole range, persistent
        range status | range solve <mod> [chal] | range shell <mod> <target>
   c. Ephemeral container check:  python scripts/docker_run_all.py [--real]  (39/39)
   d. Kubernetes on a normal host:  ./scripts/kind-up.sh && ./scripts/kind-run-all.sh
      (NOTE: nested k8s/kind CANNOT start pods in some microVM sandboxes — runc
       'pipe EOF'; use path (b) there. Docker itself works. See docs/kubernetes.md.)

ACCEPTANCE CHECKS (must all pass):
- redsec doctor           -> 11/11 modules OK
- redsec selftest         -> 40/42 challenges PASS (fail-before, pass-after)
- pytest -q               -> all green (engine/verifier units + per-module integration)
- python scripts/docker_run_all.py  -> 39/39 container-backed challenges PASS
  (module 10 is artifact-scored; its 3 are covered by selftest)

OPTIONAL — point another LLM at the range (see docs/llm-assessor.md):
- Attacker-side autonomous assessor (Grok/OpenAI/local, OpenAI-compatible):
    XAI_API_KEY=... python scripts/agent_solver.py <mod> --provider grok --model grok-4
  The http_request tool is hard-scoped to the local lab; verifier scores each step.
- Target-side (apps think with a real model): REDSEC_LLM_BACKEND=openai +
  REDSEC_LLM_BASE_URL=https://api.x.ai/v1 + REDSEC_LLM_MODEL + REDSEC_LLM_API_KEY.

REPORT when done: the outcome of each acceptance check, and how to reach the running
targets (ports from `range status`). Do not weaken any verifier to make it pass;
if something fails, set up your own end-to-end test and fix the code, then re-verify.

FALLBACK (only if the repo is genuinely unavailable): rebuild from the spec in this
repo's CLAUDE.md + docs/ (architecture.md, authoring-modules.md, verification.md,
mcp-attack-matrix.md, curriculum.md). The unit of the framework is a declarative
module: modules/NN-slug/ with module.yaml + lesson.md + targets/ (vulnerable apps +
Dockerfiles) + verify/ (flag|oracle|artifact checks) + solution/solve.py
(solve(endpoints, drop_url) -> {flags, artifacts}). LLM targets use the deterministic
mock in redsec/mockllm so challenges are reproducible offline. A module is only
"complete" when `redsec selftest <id>` goes fail->pass. Rebuild to the SAME
acceptance checks above. Expect to approximate, not reproduce exactly — prefer
restoring repo access.
```

---

## How to keep this prompt current

This file and `CLAUDE.md` are updated together whenever the project changes in a way
that affects setup or scope — e.g. a new module, a new run path, a changed acceptance
number (42/42, 39/39), or a new integration. On each such change: bump **Last
updated** and **State at last update** above, adjust the acceptance numbers in the
prompt if they moved, and commit both files. (During our sessions, I do this as part
of the change.) The prompt deliberately references `CLAUDE.md`/`docs/` rather than
duplicating the full spec, so detail lives in exactly one place and can't drift.
