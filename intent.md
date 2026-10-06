# RedSec Range intent and decision record

This file is the durable product and architecture contract for RedSec Range. A
future repository-aware agent should read it before changing scope or deployment.
`CLAUDE.md` records the current operational state, `docs/ROADMAP.md` tracks future
work, and this file records why the product has its present shape.

## Product purpose

RedSec Range is an open-source, hands-on AI red-teaming course and range. A learner
must be able to deploy deliberately vulnerable AI, agent, A2A, RAG, embedding, MCP,
supply-chain, and infrastructure targets; exploit them; and obtain evidence that an
attack worked. It should work without a paid model by default and allow a real model
or external harness when the learner wants autonomous assessment.

The primary audience is a security practitioner learning modern AI attack surfaces.
The default path must be simple enough for someone who can sign in to GitHub and open
a Codespace. The same repository must also support local Docker, local Python,
Kubernetes, and an optional dedicated Fly.io machine.

## Course scope and ownership

The range catalog has two kinds of available content:

- `builtin` is the RedSec-authored course: 43 challenge concepts across 11 modules.
  It follows the 11 public OffSec AI-300 syllabus areas and adds deeper MCP and A2A
  coverage. RedSec owns the manifests, vulnerable targets, lessons, verifiers, and
  runnable reference solutions.
- `dvaa`, `mcpgoat`, `dvmcp`, and `appsecco-mcp` are independently maintained
  projects. RedSec pins their source revisions, indexes their challenges, and supplies
  deployment and isolation adapters. Their challenge implementations and answer
  material remain upstream.
- `offsec` is a non-deployable placeholder. It may become an adapter only if OffSec
  publishes and licenses an automation interface. Public AI-300 syllabus coverage
  does not imply access to OffSec private labs, private course material, or the exam.

The committed catalog currently represents 110 distinct challenge concepts and 162
runnable variants. MCPGoat has 26 concepts at three scored levels (78 flags) and a
separate fixed Secure reference. Appsecco supplies nine ungraded labs. DVAA's separate
infrastructure scanner fixtures are a detection corpus, not CTF challenges, and are
not counted as course challenges. Built-in module manifests and
`ranges/catalog.yaml` are authoritative; `docs/CHALLENGE-CATALOG.md` is the
generated human-readable index.

## Learning and verification contract

A built-in module is complete only when it has a lesson, target, verifier, and
`solution/solve.py`, and `redsec selftest` proves every challenge fails before the
exploit and passes after it. RedSec uses flag, side-effect oracle, and scored-artifact
verification. The deterministic mock LLM is the default because it is repeatable,
offline, and free; real OpenAI-compatible models are optional.

External solution and verification claims must retain provenance:

- DVAA embeds a solution and success criteria in each of its 22 CTF definitions.
- MCPGoat publishes a complete trainer guide and automated attacker for its 26
  concepts and three scored levels.
- DVMCP publishes a detailed guide for each of its ten challenges.
- Appsecco publishes demonstration and attack guidance in each lab README; it does
  not publish one formal graded answer suite.

RedSec adapter health and protocol smoke checks prove that upstream surfaces start.
They do not confer the built-in fail-before/pass-after guarantee. Documentation and
CLI output must keep those claims separate.

## AI-300, MCP, and A2A coverage

The built-in modules map one-to-one to the eleven areas in the public OffSec AI-300
syllabus. The defensible statement is “covers the public AI-300 syllabus objectives.”
It is not course or exam equivalence.

MCP is a first-class subject. Built-in module 07 covers tools, resources, prompts,
sampling, roots, elicitation, logging, completion, rug pulls, command injection,
Unicode concealment, and routing-policy desynchronization. External MCP ranges add
authorization, transport, supply-chain, tool shadowing, OAuth audience, and multiple
difficulty variants.

A2A is also first-class. Built-in module 04 covers Agent Cards, JSON-RPC messages,
Tasks, identity, transitive trust, and shared context. DVAA adds A2A delegation and an
agent-to-agent attack chain.

## Default GitHub Codespaces journey

Codespaces is the default hosted environment. Signing in to GitHub and opening the
repository's Codespace installs the package and starts the private built-in Docker
range. The learner waits for `.redsec/codespaces-ready`, then uses `range status`,
`redsec lesson`, `range solve`, and `range shell`.

Optional ranges are explicit: `redsec ranges enable ...` followed by
`redsec ranges up`. They may run concurrently on the same Codespace.

A harness running inside the Codespace already acts from the attacking machine. An
external harness connects through authenticated `gh codespace ssh` or
`scripts/codespaces-connect.sh`. Merely pointing Claude, Codex, or another repository
connector at GitHub does not create a tunnel and does not move tool execution into the
Codespace. GitHub Actions is a CI validation environment, not a persistent interactive
range; its runners disappear after the workflow.

## Defensive threat-model automation

Maintainers may run `.github/workflows/codex-threat-models.yml` manually to generate
a defensive design review for every available catalog concept. The workflow uses a
curated, secret-free inventory rather than exposing flags, hints, solutions, target
source, or execution tools to the model. Structured output must cover the exact 110
concept keys before deterministic rendering produces per-range reports and a portfolio
overview. Generated material enters the repository through a reviewable pull request.

Generation and publishing have separate permissions. The model job can read the
repository but has no persisted Git credential; the publisher can open a branch and
pull request but never receives the OpenAI key. Runs are manual because model calls
can incur cost. The threat models recommend controls, detection, incident response,
and benign validation before abuse; they do not execute targets or establish runtime
exploitability. Codex Security is an optional, separately gated review layer rather
than a substitute for this catalog-wide design assessment.

## Optional Fly.io journey

Fly.io is for a private, dedicated, ephemeral cloud range when the user explicitly
chooses it. `deploy/fly/up.sh` creates a unique private app, deploys one Docker-capable
Machine, records state in ignored `.redsec/fly.json`, and waits for readiness.
`deploy/fly/ssh.sh` provides an interactive attacking shell;
`deploy/fly/exec.sh` provides harness commands; `deploy/fly/model.sh` runs the bundled
assessor; `deploy/fly/proxy.sh` creates loopback-only access for a local client.

The Fly app has no public service. A root `fly.toml` generated by `fly launch` is not
part of this architecture because it creates a public web service and bypasses the
range lifecycle. Only `deploy/fly/fly.toml` and its helpers are supported. Fly creates
billable resources, so throwaway validation apps are destroyed unless persistence was
requested. A TTL is a secondary safety limit, not a replacement for cleanup.

## Runtime topology and isolation

All selected ranges may share one Docker-capable host, while each range keeps an
independent lifecycle, source checkout, image, target container, and internal Docker
network. The built-in range uses one network per module. DVMCP serves ten challenges
from one upstream container. Appsecco packages two network servers and seven named
stdio servers in one adapter container.

External target containers join an internal network by default. A small read-only TCP
gateway joins that network and a host-access bridge and forwards only cataloged ports.
It is a narrow transport proxy: it does not inspect or modify content and is not a
general MITM proxy. Outbound network access requires explicit `--allow-egress`.

The built-in course supports Kubernetes through Helm/kind. External projects remain
standalone containers because they do not share chart and lifecycle contracts. A
future Kubernetes driver may use one shared cluster, but each external range needs its
own namespace, NetworkPolicy, and release. NetworkPolicy enforcement requires a
policy-enforcing CNI.

## Updates, credentials, and secrets

Every external default is pinned to a full Git commit. `redsec ranges update ID`
updates only the requested local source, rebuilds it, and restarts it if needed. The
running revision must be reported. If it differs from the committed curriculum
revision, challenge metadata and solution links describe the committed baseline and
the CLI must warn about that drift. Updating the default for everyone is a reviewed
catalog change.

Model credentials come from environment variables, Codespaces secrets, or staged Fly
secrets. Fly credentials come from authenticated `flyctl` state or `FLY_API_TOKEN`.
Tokens and model keys must never be printed, written to tracked files, embedded in an
image, or committed. Forwarded challenge ports remain private because every target is
deliberately vulnerable.

## Required acceptance evidence

Changes affecting the built-in course run `pytest`, `redsec doctor`, and
`redsec selftest`; container or Kubernetes changes also run the relevant Docker/kind
checks. Changes to external catalog metadata regenerate and check
`docs/CHALLENGE-CATALOG.md`. External adapter CI must at least build every pinned
source, start all ranges together, check declared ports and entrypoints, and preserve
network isolation. Native upstream regression harnesses should be used where they are
available.

A live Fly validation reports the unique app name, readiness, commands, verifier
results, and cleanup result. It must not mutate an unrelated existing app.

## Decisions ruled out

- Fly.io as the default hosted experience.
- GitHub Actions as a persistent interactive attacking machine.
- Public challenge ports or a public Fly HTTP service.
- Assuming repository access creates an SSH tunnel or changes where tools execute.
- Copying external challenges into the built-in course and obscuring ownership.
- Using moving upstream branches as the reproducible default.
- Treating the OffSec placeholder as a deployable public range.
- Requiring a paid or remote LLM for deterministic course operation.
- Putting unrelated vulnerable ranges into one Kubernetes namespace.
- Describing the gateway as an application-aware MITM proxy.
- Claiming external challenge solvability solely from container health checks.

## Current limitations and next work

Built-in Docker networking does not yet enforce every manifest egress declaration.
The teaching oracle is not a tamper-proof competitive judge. External CI needs deeper
protocol calls for DVMCP and Appsecco's network transports. The harness safety and
real-model message-shape items in `docs/ROADMAP.md` remain open. These are
explicit limitations; documentation must not silently upgrade them into guarantees.
