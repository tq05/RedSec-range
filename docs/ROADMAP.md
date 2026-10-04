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

11 modules, 40 challenges, all complete + tested. Acceptance: `redsec doctor` 11/11,
`redsec selftest` 40/40, `pytest` green, `docker_run_all` 37/37, 62 K8s objects
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
