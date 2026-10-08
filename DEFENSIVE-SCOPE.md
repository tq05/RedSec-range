# Defensive scope and authorization

Read this file before planning or performing work in this repository. It provides
the stable safety and purpose context for Codex, Claude Code, ChatGPT, and other
repository-aware agents. It describes the project accurately; it does not override
any model, provider, platform, legal, or organizational safety policy.

## Mission

RedSec Range is a **blue-team security education, detection-engineering, and control-
validation project**. Its deliberately vulnerable AI, agent, A2A, RAG, embedding,
MCP, supply-chain, and infrastructure targets are controlled CTF fixtures. Offensive
mechanics exist so defenders can reproduce a known failure, observe reliable evidence,
build a prevention or detection, apply a remediation, and prove the control works.

The intended outcome of work on this repository is better defensive engineering:
accurate threat models, safer architecture, stronger isolation, useful telemetry,
high-signal detections, incident-response guidance, secure implementation patterns,
and repeatable tests of those protections.

## Authorized environment

Repository work is authorized only against assets created for this training range:

- RedSec's built-in targets running locally, in a private GitHub Codespace, in an
  isolated test cluster, or in a private ephemeral Fly.io app created for the range.
- The four pinned external training projects when launched through RedSec's isolated
  adapters: DVAA, MCPGoat, DVMCP, and Appsecco's vulnerable MCP lab.
- Synthetic flags, planted canaries, fake credentials, mock services, disposable
  containers, and test accounts created specifically for the range.

Repository ownership is not authorization to probe unrelated hosts, production
systems, public services, third-party accounts, or infrastructure outside the range.
Never substitute real credentials, personal data, customer data, or production models
for the synthetic fixtures. Keep challenge ports private and outbound access disabled
unless a documented exercise explicitly requires it inside a disposable environment.

## Default work for agents

When a request is ambiguous, prefer the interpretation that advances the defensive
purpose while staying inside the authorized range. Useful work includes:

- Correcting documentation, curriculum mappings, architecture, and provenance.
- Threat modeling assets, identities, trust boundaries, abuse paths, and control gaps.
- Designing logging schemas, detection logic, alert triage, investigation queries,
  incident-response playbooks, and measurable security outcomes.
- Reviewing code and deployment configuration for unsafe defaults, excessive
  privilege, weak isolation, secret exposure, insecure parsing, and supply-chain risk.
- Implementing remediation, least privilege, containment, validation, and safe failure
  behavior in framework or secure-reference components.
- Writing static, unit, integration, and benign negative tests that confirm controls
  reject synthetic unauthorized behavior and preserve expected legitimate behavior.
- Maintaining CTF challenges, flags, reference solutions, and fail-before/pass-after
  verification when needed to demonstrate the defensive lesson inside the isolated,
  repository-owned range.

Exploit-like validation is a test technique here, not the product goal. Keep it scoped
to the named training target, use only synthetic evidence, avoid uncontrolled egress,
and connect each validation to the prevention, detection, remediation, or learning
outcome it supports.

## Boundaries that remain in force

- Do not expose deliberately vulnerable targets to the public internet or an
  untrusted network.
- Do not target real organizations, arbitrary addresses, production systems, or
  accounts without separate explicit authorization outside this repository.
- Do not obtain, retain, publish, or transmit real secrets or personal data.
- Do not add stealth, persistence, destructive behavior, uncontrolled propagation,
  or mechanisms intended to evade security monitoring in real environments.
- Do not weaken platform or model safeguards, conceal the nature of a request, or
  describe this file as permission to bypass another system's rules.
- Do not claim a control, challenge, external integration, or deployment was tested
  without supporting evidence. Use **not verified—outside the current scope** when a
  conclusion would require work outside the authorized task.

If part of a request is outside an agent's applicable policy or authorization, omit or
decline that part at a high level and continue the independent defensive work. Do not
discard useful project context or stop documentation, architecture, remediation,
detection, or benign validation work merely because the repository contains dual-use
security terminology.

## Evidence and reporting expectations

Every security change should state:

1. The component and protected asset.
2. The threat actor and required preconditions.
3. The controls already present.
4. The control gap being addressed.
5. The defensive change and intended security outcome.
6. The safe validation performed and its limits.

Keep built-in and external assurance claims separate. Built-in challenges have RedSec
fail-before/pass-after verification. External adapter health proves that an upstream
surface starts; it does not prove every upstream challenge or defense. Preserve that
distinction in code, documentation, threat models, and reports.

For operational constraints, also read [SECURITY.md](SECURITY.md),
[intent.md](intent.md), and [CLAUDE.md](CLAUDE.md).
