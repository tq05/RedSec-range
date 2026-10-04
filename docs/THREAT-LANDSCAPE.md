# Threat Landscape — AI-agent attack chains, mapped to OWASP & CSA

A research-informed map of how AI agents are actually attacked today, how attacks
**chain across agents**, what threat actors are doing, and how every RedSec module
lines up with the **OWASP** and **Cloud Security Alliance** frameworks. This is the
reference the curriculum's accuracy and difficulty tiers are built on.

> Research snapshot: 2026-10. Frameworks move fast; re-check the linked primary
> sources. Descriptive/defensive only — this maps public taxonomies and reporting to
> the training range; it is not an operations manual.

## 1. The frameworks we map to

### OWASP — two complementary lists
- **OWASP LLM Top 10 (2025)** — risks of an LLM *application* (LLM01 Prompt Injection
  … LLM10 Unbounded Consumption). Still the base layer. ([genai.owasp.org](https://genai.owasp.org/))
- **OWASP Top 10 for Agentic Applications (2026)** — the newer, agent-specific list.
  This is the one that captures *chaining* and *autonomy*:

  | ID | Agentic risk | Real-world example cited |
  |----|--------------|--------------------------|
  | **ASI01** | Agent Goal / Instruction Hijack | EchoLeak |
  | **ASI02** | Tool Misuse | Amazon Q |
  | **ASI03** | Identity & Privilege Abuse | — |
  | **ASI04** | Agentic Supply Chain Vulnerabilities | GitHub MCP exploit |
  | **ASI05** | Unexpected / Remote Code Execution | AutoGPT RCE |
  | **ASI06** | Memory & Context Poisoning | Gemini memory attack |
  | **ASI07** | Insecure Inter-Agent Communication | — |
  | **ASI08** | Cascading Failures | — |
  | **ASI09** | Human-Agent Trust Exploitation | — |
  | **ASI10** | Rogue Agents | Replit meltdown |

  Source: [OWASP Top 10 for Agentic Applications (Dec 2025)](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
  and [Agentic AI — Threats and Mitigations (Apr 2025)](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/).

### CSA — MAESTRO (layered agentic threat modeling)
**M**ulti-agent **E**nvironment, **S**ecurity, **T**hreat, **R**isk, **O**utcome — a
7-layer model for threat-modeling agentic systems where single-app frameworks (STRIDE
etc.) fall short:

1. **Foundation Models** — adversarial examples, extraction, backdoors, membership inference.
2. **Data Operations** — data/RAG/embedding poisoning, PII exfiltration.
3. **Agent Frameworks** — orchestration (LangChain/AutoGen), prompt injection, tool-calling, supply chain.
4. **Deployment & Infrastructure** — cloud/K8s/CI-CD, image tampering, RBAC abuse, lateral movement.
5. **Evaluation & Observability** — telemetry/logging integrity, metric manipulation, evasion.
6. **Security & Compliance** — cross-layer governance, policy, accountability.
7. **Agent Ecosystem** — inter-agent interactions, marketplaces, registries, impersonation.

Sources: [CSA — Applying MAESTRO (Feb 2026)](https://cloudsecurityalliance.org/blog/2026/02/11/applying-maestro-to-real-world-agentic-ai-threat-models-from-framework-to-ci-cd-pipeline),
[MAESTRO 7 layers](https://www.practical-devsecops.com/maestro-agentic-ai-threat-modeling-framework/),
[CSA MCP security analysis](https://cloudsecurityalliance.org/).

## 2. How attacks chain across agents (the new surface)

The step-change from "attack one LLM app" to "attack a *system* of agents." Key chains
from current research:

- **Agent session smuggling (A2A).** A malicious remote agent injects covert
  instructions into an *ongoing* stateful conversation with a victim agent — hidden
  among legitimate turns — to extract system prompts / chat history / tool schemas /
  credentials or trigger unauthorized tool calls on the victim's behalf. Preconditions:
  stateful A2A protocol + implicit inter-agent trust. (OWASP **ASI07**, MAESTRO L7.)
  [Unit42](https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/)
- **Tool/skill description poisoning → cross-agent shadowing.** A poisoned tool or
  AgentCard skill description carries hidden `<IMPORTANT>`/`<SYSTEM_DIRECTIVE>` text
  that steers not just the calling model but *other* agents in the workflow — a
  "sleeper cell" that propagates. (ASI01/ASI06/ASI07, MAESTRO L3/L7.)
  [Solo.io](https://www.solo.io/blog/deep-dive-mcp-and-a2a-attack-vectors-for-ai-agents)
- **Naming / typosquat → confused approval.** Look-alike MCP servers or agents
  (`DataAnalysisAgent` vs `DataAnalyzerAgent`) get mistakenly trusted, then poison
  context. (ASI04.)
- **Rug pull.** A tool/agent earns trust over months, then weaponizes after it's
  embedded in a critical workflow. (ASI10, MAESTRO L7.)
- **Documented multi-step chains** (Solo.io): *naming → context poisoning →
  exfiltration*; *shadowing → A2A privilege escalation → credential access via
  state-transition hijack*; *rug pull + context poisoning → stealth exfiltration*.

**Overarching lesson:** classic transport security (TLS, auth) is necessary but not
sufficient — defenses must understand *agentic semantics*: tool-invocation intent,
skill descriptions, multi-turn task state, and behavioral continuity.

## 3. What threat actors are doing (latest reporting)

Anthropic's **September 2026** threat report documents a structural shift: adversaries
now embed models as **execution nodes inside multi-agent orchestration frameworks**,
not as standalone content generators. The model *issues instructions to other agents,
queries external systems, and takes actions* as one component of an autonomous kill
chain. Observed across cyber-espionage, influence ops, surveillance, and
financially-motivated campaigns; notable themes include "vibe hacking," agent
frameworks where **the API key is the loot**, and AI-assisted malware iteration. The
defensive gap: acceptable-use and detection built for single-turn prompts miss
**orchestration-layer** behavior — monitoring must move to where agents coordinate.
Sources: [Anthropic report summary](https://aigovernance.com/news/anthropic-documents-nine-months-of-ai-misuse-across-agentic-attack-chains),
[Anthropic PDF (Sept 2026)](https://www-cdn.anthropic.com/e50be2e51e7695dc4b1366a37a245a597377d3b5/Anthropic-Detecting-and-countering-091026.pdf),
[AI agents breached 395 orgs / credential abuse](https://venturebeat.com/security/ai-agents-breached-395-organizations-using-credentials-your-iam-policy-still-treats-as-human).

## 4. RedSec module ↔ framework map

| Module | OWASP LLM | OWASP Agentic (ASI) | MAESTRO layer | Chain concept exercised |
|---|---|---|---|---|
| 01 Intro | LLM07 | ASI01 | L1 | first injection |
| 02 Recon | LLM07, LLM02 | ASI04 (discovery) | L4 | fingerprint / surface discovery |
| 03 Agents | LLM01/02/06/07 | ASI01, ASI02, ASI06 | L1, L3 | injection → agency → memory persistence |
| 04 Multi-agent & A2A | LLM01, LLM06 | **ASI07**, ASI09, ASI08 | **L7** | transitive trust, session smuggling, shadowing |
| 05 RAG | LLM01, LLM08 | ASI06 | L2 | knowledge/context poisoning |
| 06 Embeddings | LLM08, LLM02 | ASI06 | L2 | embedding inversion / MIA |
| 07 MCP & tools | LLM01/02/06, MCP01-05 | ASI02, ASI04, ASI05 | L3 | tool poisoning, confused deputy, RCE |
| 08 Supply chain | LLM03, LLM04 | ASI04, ASI10 | L2, L3 | malicious artifacts, rug pull |
| 09 Infra | LLM02 | ASI03 | L4 | SSRF, identity/privilege, secrets |
| 10 Threat modeling | — | all (analysis) | all | MAESTRO/ASI mapping as the exercise |
| 11 Capstone | LLM01/02/06 | ASI01→ASI02→ASI03 | L1→L3→L7 | full chain: access → pivot → exfil |

> This map is the basis for the difficulty tiers (see `docs/DIFFICULTY-TIERS.md`):
> the new **hard** and **impossible** challenges target the agent-chaining risks
> (ASI07/ASI08, MAESTRO L7) that single-step challenges don't reach — e.g. agent
> session smuggling and cross-agent shadowing in Module 04, and a multi-agent capstone.

## 5. Sources
- OWASP Top 10 for Agentic Applications (2026) — https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
- OWASP Agentic AI — Threats and Mitigations (2025) — https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/
- OWASP LLM Top 10 (2025) — https://genai.owasp.org/
- CSA MAESTRO — https://cloudsecurityalliance.org/blog/2026/02/11/applying-maestro-to-real-world-agentic-ai-threat-models-from-framework-to-ci-cd-pipeline
- Unit42 — Agent session smuggling — https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/
- Solo.io — MCP & A2A attack vectors — https://www.solo.io/blog/deep-dive-mcp-and-a2a-attack-vectors-for-ai-agents
- Anthropic — Detecting and countering misuse of AI (Sept 2026) — https://www-cdn.anthropic.com/e50be2e51e7695dc4b1366a37a245a597377d3b5/Anthropic-Detecting-and-countering-091026.pdf
- arXiv — Threat modeling for emerging AI-agent protocols (MCP/A2A/Agora/ANP) — https://arxiv.org/html/2602.11327v2
