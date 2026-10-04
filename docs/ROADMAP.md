# ROADMAP — intent, principles, and what's next

This is the durable record of **why** RedSec Range exists and **where it's going**,
so any session (Claude Code or otherwise) can resume with the owner's intent intact.
`CLAUDE.md` says what exists and how to run it; this says what it's *for* and what to
do next. Owner: R (GitHub `tq05` / `rolfh9`), UK-based, senior AI/ML-infra role.

## Intent (what R wants this to be)

- A **detailed, guided, open-source** training course **and** framework for learning
  AI & MCP security — hands-on, not just reading.
- **Guided by** the OffSec AI-300 / OSAI syllabus but **better, accurate, and
  expandable** — adding a module/challenge should be a `module.yaml` + target +
  verifier, no framework surgery.
- **Deployable on Kubernetes**, with **per-module deliberately-vulnerable apps** you
  can actually exploit, and **automated verification** that proves an exploit worked
  (not an honour system).
- **Accurate and tested** — due diligence and real end-to-end testing are the point;
  every challenge must be demonstrably solvable (fail→pass).
- Usable as an **interactive command centre**: stand the range up and solve
  challenges live (in a sandbox driven through chat, or on your own machine).
- **Pluggable LLMs**: point Grok / OpenAI / local models at it as autonomous
  assessors, and make it easy to build your own harness.
- **Everything in GitHub** as the durable memory/context store, with a single
  reusable prompt (`RECREATE.md`) to recreate + verify the whole environment, and
  clean **resume in Claude Code**.

## Principles / decisions (the "why" behind the design)

- **Deterministic mock LLM is the default** (`redsec/mockllm`) so challenges are
  reproducible and CI-able offline and for free; a real model is opt-in. The
  vulnerabilities live in the *apps*, so they transfer to a real model.
- **Three verifier patterns** (flag / oracle / artifact); a module is not
  `complete` until `redsec selftest <id>` goes fail→pass and ships
  `solution/solve.py`. Prefer oracle (per-vector sink markers) for action vulns.
- **Containment by default**: targets non-root, egress denied; `privileged`/`egress`
  must be explicit. Everything is deliberately vulnerable → isolated use only.
- **Single source of truth = `CLAUDE.md`**; `RECREATE.md` and this file reference it
  rather than duplicating, to avoid drift.
- **kind works on a normal host**; the Claude sandbox can't nest pods (Firecracker
  microVM), so there we use the persistent Docker range. Same modules either way.

## Status (keep in sync with CLAUDE.md)

11 modules, 42 challenges, all complete + tested. Acceptance: `redsec doctor` 11/11,
`redsec selftest` 42/42, `pytest` green, `docker_run_all` 39/39, 62 K8s objects
valid. Walkthroughs independently red-teamed by a separate model.

## Backlog / next steps (suggestions, not commitments — confirm with R)

Near-term:
- [ ] Run a **live Grok assessment** once `XAI_API_KEY` is available (`assess <mod>
      --provider grok`); capture a scorecard. Consider a multi-model **benchmark**
      mode that scores several models across all modules and emits a table.
- [ ] Add a short README banner pointing newcomers to `RECREATE.md` + a "Resume in
      Claude Code" line.
- [ ] Decide the default Grok model tag (currently `grok-4` as a placeholder).

Content expansion (hooks already noted in docs/mcp-attack-matrix.md):
- [ ] MCP: Unicode tag-block tool-poisoning concealment; **token passthrough /
      confused-deputy** as a dedicated vector; cross-server **tool shadowing**.
- [ ] More challenges per module; a harder capstone variant.
- [ ] Swap module 07's HTTP/JSON-RPC shim for the **official MCP SDK over stdio** as
      an "advanced transport" variant.

Infra / ops:
- [ ] Push images to a registry (GHCR) so remote clusters don't need `kind load`.
- [ ] Add a policy-enforcing CNI (Calico/Cilium) to actually enforce the
      NetworkPolicies; add a test that asserts egress is blocked.
- [ ] Optional in-cluster scoreboard UI; wire the CI `kind` job on a real runner.

## Open questions for R

- Publish the repo publicly, or keep private for now? (License is already Apache-2.0.)
- Intended audience/level, and any **org-specific policies / CIS benchmarks** to fold
  in (ties to R's separate security-design-review goal)?
- Should the assessor results feed a leaderboard / be tracked over time?

## Working convention for agents on this repo

When you change something, **verify it yourself end-to-end** (run `redsec selftest`,
`pytest`, or `scripts/docker_run_all.py` as appropriate) and fix it until green —
don't hand back changes for the owner to test. Never weaken a verifier to make it
pass. Keep `CLAUDE.md`, `RECREATE.md`, and this file in sync on scope changes.

## Security & quality review — 2026-10-04 (findings to action)

A full read-only code review ran on 2026-10-04. Headline items, by priority. None
block *using* the range as a teaching tool in an isolated environment; they harden it
and tighten the accuracy/integrity claims.

**P1 — should fix**
- [ ] **Oracle integrity.** The `drop` sink accepts any POST and most needles are
      learner-chosen markers, so an oracle challenge can be "passed" by posting the
      marker directly. Fix: each target tags its sink posts with a per-target secret
      (from env) on its own path; checks filter on tag+path; prefer needles that are
      secrets only obtainable via the exploit. (`services/drop`, `verify/builtins.py`,
      `07/verify/checks.py`.) Until then, SECURITY.md documents the sink as a teaching
      oracle, not a tamper-proof judge.
- [ ] **Local isolation.** Modules 07 (shell RCE), 08 (pickle), 09 (SSRF to
      169.254.169.254) run unisolated under bare `redsec dev/up`. Add Host-header
      allow-list + Content-Type enforcement to the FastAPI targets; default these
      modules to the Docker/K8s path or gate bare-local behind an explicit flag.
      SECURITY.md updated to say so.
- [ ] **Container hardening.** `vuln-mcp` and `08 registry` images run as root; plant
      files under a writable dir and add `USER 10001`. Keep seccomp + cap-drop even on
      `privileged` targets; set `automountServiceAccountToken: false` in the chart.
- [ ] **Agent-harness safety.** `grok_cli --agent` has unrestricted shell + network
      with the API key in env, while reading injection-laden lab content; add a
      confirm-before-exec / container-only mode, scrub env, URL allow-list. Remove the
      drop URL from `agent_solver`'s allow-list; add `--no-hints` for benchmarking.
- [ ] **Real-LLM backend.** `mockllm/backends.py` appends tool messages without a
      `tool_call_id`/preceding assistant `tool_calls`, so `REDSEC_LLM_BACKEND=openai`
      400s on first tool call. Fix the message shape; qualify the "transfers to a real
      model" claim (the `{{SECRETS}}` substitution is mock-only).
- [x] **OWASP version consistency.** Removed mis-versioned/unsupported LLM mappings
      (stray LLM08 on 04/07/11; LLM10 on 02/09) and the capstone's MCP mapping
      (no MCP target). Done 2026-10-04.

**P2 — nice to have**
- [ ] Extract a shared `redsec/harness.py` (the fail→pass + env/peer-URL wiring is
      duplicated across cli selftest, tests, docker_run_all, range_ctl, kind_run_all);
      fold `HostExfil` into `DropContains`.
- [ ] Derive module lists in `build_images.sh`, `kind-up.sh`, `kind-run-all.sh` and the
      CI helm job from `load_all()` instead of hard-coding.
- [ ] Enforce (or drop) `allow_targets` + `privileged` NetworkPolicy semantics so an
      overview diagram's trust edges are real; Docker paths currently ignore
      `egress`/`privileged`.
- [ ] Per-student flags via `flag_sha256` (already supported) so flag env-overrides
      don't break checks; spoiler-tag hints so the worksheet can exclude answers
      programmatically.
- [ ] Key the `07` rug-pull counter per client (currently one global counter → order
      dependence). Harden `module 10` artifact checks (keyword match is gameable).

**P3 — minor:** `cli.verify` exit semantics; leftover temp values files in
`k8s.render`; `datetime.utcnow()` deprecation; CI has no linter/type-check;
unpinned deps; base image copies `.git`.

## Difficulty tiers — progress (2026-10-04)

- Added the easy/medium/hard/impossible tier model (`tier`/`sealed` on Challenge;
  per-challenge `mappings` incl. `owasp_agentic`). Spec for all 11 modules in
  `docs/DIFFICULTY-TIERS.md`; research + OWASP Agentic/CSA MAESTRO mapping in
  `docs/THREAT-LANDSCAPE.md`.
- **Built + tested:** Module 04 tiers (easy/medium/hard) + new **impossible**
  `session-smuggling` (sealed answer in `solution/SEALED.md`; reference exploit proves
  solvable via selftest).
- **Next:** build the remaining impossible/new tiers specced in DIFFICULTY-TIERS.md
  (03 dual-guard exfil, 07 Unicode-concealment→RCE, 08 time-delayed rug pull, 09
  SSRF→cred→second-service chain, 11 chain-vs-detection), each fail→pass + sealed.
