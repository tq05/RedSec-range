# ROADMAP — backlog and what's next

[`intent.md`](../intent.md) is the durable product and architecture decision record.
`CLAUDE.md` says what exists and how to run it. This file tracks remaining work and
open questions. Owner: R (GitHub `tq05` / `rolfh9`).

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
  every built-in challenge must be demonstrably solvable (fail→pass), while external
  claims retain their upstream provenance.
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
- **Decision source of truth = `intent.md`**; operational source of truth =
  `CLAUDE.md`; `RECREATE.md` references both rather than duplicating them.
- **kind works on a normal host**; the Claude sandbox can't nest pods (Firecracker
  microVM), so there we use the persistent Docker range. Same modules either way.

## Status (keep in sync with CLAUDE.md)

11 modules, 43 challenges, all complete + tested. Acceptance: `redsec doctor` 11/11,
`redsec selftest` 43/43, `pytest` green, `docker_run_all` 40/40, 62 K8s objects
valid. Walkthroughs independently red-teamed by a separate model.

The range catalog additionally indexes 67 external challenge concepts (119 runnable
variants): DVAA 22, MCPGoat 26 concepts / 78 levels, DVMCP 10, and Appsecco 9 labs.
External implementation and solution provenance remain upstream; see
`docs/CHALLENGE-CATALOG.md`.

## Backlog / next steps (suggestions, not commitments — confirm with R)

Near-term:
- [x] Add a manual Codex defensive threat-model workflow covering all 110 catalog
      concepts. It validates strict structured output, renders a repository overview,
      keeps model credentials separate from PR publishing, and can optionally request
      Codex Security Review when that product is connected.
- [x] Deepen external CI with MCPGoat's native 78-flag regression, DVAA's 22
      challenge/solution inventory, all ten DVMCP TCP services, and both Appsecco
      network services.
- [x] Initialize all seven Appsecco stdio MCP servers in CI.
- [ ] Add protocol-level calls for DVMCP's individual methods and Appsecco's two
      network transports; their current CI checks TCP reachability while upstream
      guides remain the solution authority.
- [ ] Run a **live Grok assessment** once `XAI_API_KEY` is available (`assess <mod>
      --provider grok`); capture a scorecard. Consider a multi-model **benchmark**
      mode that scores several models across all modules and emits a table.
- [ ] Add a short README banner pointing newcomers to `RECREATE.md` + a "Resume in
      Claude Code" line.
- [ ] Decide the default Grok model tag (currently `grok-4` as a placeholder).

Content expansion (hooks already noted in docs/mcp-attack-matrix.md):
- [x] MCP: Unicode tag-block tool-poisoning concealment and current 2026-07-28
      Streamable HTTP header/body policy desynchronization.
- [ ] MCP: **token passthrough / confused-deputy** as a dedicated vector;
      cross-server **tool shadowing**.
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
- [ ] **Oracle integrity.** *Done 2026-10-16:* a per-range token (generated at
      start, given only to the sink and targets) marks target posts as trusted, and
      `DropContains`/`HostExfil` ignore everything else. Direct marker posts now fail
      with an explanatory message. Remaining: per-target tokens bound to each
      target's sink path, and needles that are secrets only obtainable via the
      exploit. The sink is still not tamper-proof against someone who controls the
      host (see SECURITY.md).
- [ ] **Local isolation.** *Done 2026-10-17:* `redsec dev/up` refuse modules with
      a `privileged` target or `unsafe_local: true` (07, 08, 09) unless
      `--unsafe-local` is passed, and point to `range up`. The 08/09 lessons now
      start on the Docker range. Remaining: Host-header allow-list and Content-Type
      enforcement on the FastAPI targets (DNS-rebinding defence for loopback ports).
- [x] **Container hardening.** *Done 2026-10-16:* `vuln-mcp` and the 08 registry
      run as `USER 10001`, and the chart applies the same non-root, seccomp, and
      cap-drop context to `privileged` targets as to all others. Earlier (PR #16):
      `automountServiceAccountToken: false`, DNS-only egress to the cluster resolver,
      and `--cap-drop ALL` / `no-new-privileges` / PID limits on the Docker paths.
- [ ] **Agent-harness safety.** `grok_cli --agent` reads injection-laden lab content.
      *Done 2026-10-16:* its shell runs with credential-like variables removed, and
      `--confirm` asks before each command; `http_request` is loopback-only unless
      `--allow-host` is given; `agent_solver` can no longer reach the sink and has
      `--no-hints`. Remaining: a container-only mode for `exec_shell`.
- [ ] **Real-LLM backend.** *Done 2026-10-16:* tool output is now sent as labelled
      user content, so `REDSEC_LLM_BACKEND=openai` no longer sends orphan
      `role: tool` messages. Remaining: qualify the "transfers to a real model" claim
      (the `{{SECRETS}}` substitution is mock-only) and run one live model end to end.
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
      dependence).
- [x] **Threat-model artifact integrity.** Module 10 now requires structured asset
      entries, same-entry trust relationships, and numbered multi-step chains; a
      keyword dump is covered by a regression test. Done 2026-10-04.

**P3 — minor:** no type-check in CI. *Done 2026-10-17:* the CI token defaults
to `contents: read`; base images are digest-pinned and image Python packages are
pinned in `deploy/constraints.txt`; the base runner build verifies PyPI's TLS
certificate (no `--trusted-host`) and, via `.dockerignore`, excludes `.git`;
GitHub Actions are SHA-pinned, CI downloads are checksum-verified,
Dependabot covers Actions and pip, a `ruff` job (E9 + pyflakes) and a gitleaks
secret scan run in CI, and `dependency-audit` runs `pip-audit` on every change and
weekly. *Done 2026-10-16:* temp values files in
`k8s.render`/`deploy` are removed, `redsec verify` exits 0 only when every
verified challenge passes (with an `N/M solved` summary), `datetime.utcnow()` is
replaced, and local
`redsec dev/up/selftest` targets get an allowlisted environment instead of the whole
shell.

## Difficulty tiers — progress (2026-10-04)

- Added the easy/medium/hard/impossible tier model (`tier`/`sealed` on Challenge;
  per-challenge `mappings` incl. `owasp_agentic`). Spec for all 11 modules in
  `docs/DIFFICULTY-TIERS.md`; research + OWASP Agentic/CSA MAESTRO mapping in
  `docs/THREAT-LANDSCAPE.md`.
- **Built + tested:** Module 04 tiers (easy/medium/hard) + new **impossible**
  `session-smuggling`, now exercised through A2A Agent Cards, JSON-RPC Messages,
  Tasks and `contextId` (sealed answer in `solution/SEALED.md`; reference exploit
  proves solvable via selftest). Every existing challenge now has a learning tier.
- **Built + tested:** Module 07 Unicode-concealment impossible tier and current MCP
  2026-07-28 routing-policy desynchronization challenge.
- **Next:** build the remaining impossible/new tiers specced in DIFFICULTY-TIERS.md
  (03 dual-guard exfil, 08 time-delayed rug pull, 09 SSRF→cred→second-service chain,
  11 chain-vs-detection), each fail→pass + sealed.

## Code review — 2026-11-25 (staged queue, one topic per change)

A full read of the framework, all eleven modules, the run scripts, the chart and CI.
Each stage below is meant to land as its own small change. Stages 1–2 are done; the
rest are proposals in suggested order — confirm with R before starting one.

- [x] **Stage 1 — dev papercuts.** `kubernetes-validate` moved into the `dev` extra
      (a clean `pip install -e ".[dev]" && pytest` used to fail two tests);
      `redsec submit` exits 1 on a rejected flag.
- [x] **Stage 2 — guard bypasses.** 06 `/decode` and `/search` required no vector
      length (an empty vector returned two flags); the 04 and 07 impossible-tier
      guards were case-sensitive while the model is not. Regression tests in
      `tests/test_unintended_solves.py`.
- [ ] **Stage 3 — oracle provenance (verifier fidelity).** Oracles prove *that* a
      marker reached the sink, not *how*. Because the mock honours `ACTION:` lines in
      the user turn, one direct chat message passes challenges that teach an indirect
      route: 03 `indirect-injection` and `memory-poisoning`, 05 `knowledge-poisoning`
      and `retrieval-manipulation`, 07 `sampling-abuse` and `elicitation-phishing`,
      and all three capstone challenges (no note planted); 04 `message-manipulation`
      and `agent-impersonation` pass through `/submit`. Proposal: the engine records
      which message role each tool call came from, targets attach that (and their
      entry point) to sink posts, and checks take a `via:` requirement. Needs a
      decision on behaviour under `REDSEC_LLM_BACKEND=openai`, where the source role
      is not observable.
- [ ] **Stage 4 — internal targets stay internal.** Docker, Codespaces and local
      paths publish every target, so 09 `metadata` (9091) and 11 `vault` (9112) are
      directly reachable and `metadata-ssrf` is solvable with one `curl`, no SSRF.
      Add a per-target `expose: false`, skip publishing/forwarding those, and have
      verifiers reach them only through the range.
- [ ] **Stage 5 — Docker egress.** `range_ctl.py` and `docker_run_all.py` create
      ordinary bridge networks, so every built-in target, including the 07/08 RCE
      targets, can reach the internet despite `egress: false`. Reuse the
      `--internal` network + gateway pattern the external ranges already have, and
      assert it in CI. (Promotes the P2 item above.)
- [ ] **Stage 6 — strict manifests.** The pydantic models ignore unknown keys, so a
      typo in `module.yaml` (`hint:` for `hints:`) is silently dropped. Forbid extras
      and validate unique challenge/target ids, `allow_targets` references, and that
      a `sealed` challenge has a `solution/SEALED.md`; extend `redsec doctor` to
      check lessons and build directories.
- [ ] **Stage 7 — one learner workflow.** On the Docker range flags go through
      `redsec submit` and oracles through `range verify`; `redsec verify` refuses
      because it only knows `running-NN.json`, and `range verify` never records
      progress, so `redsec score` undercounts. Let `redsec verify/submit` read the
      Docker range state and have `range verify` record solves.
- [ ] **Stage 8 — shared harness.** The fail→pass loop, env/peer-URL wiring and
      solver loading are copied in five places (cli selftest, test_integration,
      docker_run_all, range_ctl, kind_run_all); the hand-written renderer in
      `validate_manifests.py` shadows the chart. Extract `redsec/harness.py` and
      derive the module lists in `build_images.sh`, `kind-up.sh` and CI from
      `load_all()`. (The existing P2 items.)
- [ ] **Stage 9 — robustness.** `redsec up` leaves a stale `running-NN.json` when a
      target dies (then refuses to start); state files are written non-atomically;
      `build_images.sh` hides a failed push behind `|| true`; the 07 `/mcp` route
      returns a 500 where `/rpc` returns a JSON-RPC error; `range_ctl` passes
      `REDSEC_LLM_API_KEY` to every container, including the RCE targets that never
      call a model.
- [ ] **Stage 10 — CI hygiene.** Add `concurrency` cancellation and job timeouts,
      cache pip, add a type-check job (the open P3), and widen ruff beyond E9/F.

Smaller content notes: 06 `membership-inference` also passes by replaying any vector
leaked from `/records`; oracle needles match anywhere in the stored event (path and
headers included), and `ACCESS`/`PIVOT` are generic enough to match by accident.
