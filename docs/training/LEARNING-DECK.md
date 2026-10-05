# RedSec Range
> Learn to break AI systems so you can design them safely.
- 110 challenge concepts
- 162 runnable variants
- Built-in, A2A, MCP, supply chain, and infrastructure labs

---

# The range is a portfolio, not a single lab
> Five available ranges provide complementary evidence.
- **RedSec built-in:** 43 verifier-backed challenges
- **DVAA:** 22 agent and A2A challenges
- **MCPGoat:** 26 concepts across 78 difficulty variants
- **DVMCP + Appsecco:** 19 focused MCP exercises

---

# Every exercise follows one learning loop
> Observe → hypothesise → exploit → verify → defend → reset.
- Map the data flow and the authority boundary first.
- Change one assumption at a time.
- Capture evidence through a flag, oracle, or artifact.
- Explain the root cause before moving on.

---

# The model is only one component of the attack surface
> Most impact comes from the host, tools, data, and infrastructure around it.
- User and retrieved content compete for influence.
- Hosts translate text into tool calls and side effects.
- MCP and A2A add remote principals and protocol state.
- Registries, model artifacts, and cloud services add supply-chain risk.

---

# A solution is credible only when it changes observable state
> RedSec proves built-in exploits fail before and pass after execution.
- **Flag:** recover a challenge-specific value.
- **Oracle:** cause a specific side effect at the sink.
- **Artifact:** submit structured analysis that meets scoring rules.
- `redsec selftest` runs all 43 reference exploits.

---

# Start by proving the environment and your feedback loop
> Module 01 teaches the operating rhythm before the attack depth increases.
- Inspect `range status` and open the lesson.
- Coax the orientation flag from the guide.
- Submit the result and observe deterministic scoring.
- Reset without rebuilding the whole environment.

---

# Reconnaissance means finding hidden behavior, not guessing prompts
> Fingerprint implementation details before choosing an exploit.
- Compare response headers, model banners, and error shapes.
- Enumerate undocumented routes and version endpoints.
- Send malformed input and inspect excessive diagnostics.
- Convert findings into a concrete attack hypothesis.

---

# Prompt injection becomes dangerous when text inherits authority
> The vulnerability lives in the application’s trust decisions.
- Direct injection competes with the system instruction.
- Indirect injection arrives through notes or retrieved content.
- Excessive agency turns model compliance into real actions.
- Poisoned memory makes the behavior persist across turns.

---

# A2A messages require identity, integrity, and context ownership
> Agent Cards describe capability; they do not prove trust.
- Reject unsigned or unauthenticated JSON-RPC messages.
- Bind Tasks and `contextId` values to authenticated principals.
- Authorize the delegated action, not merely the sending agent.
- Validate assembled context after multi-message reassembly.

---

# RAG turns every indexed document into potential instruction input
> Retrieval relevance is not a security decision.
- Poison knowledge before the victim query runs.
- Manipulate ranking to outrank trusted material.
- Spoof authoritative-looking citations.
- Separate retrieved data from executable instructions.

---

# Embeddings leak relationships even when raw text is hidden
> Similarity interfaces can expose membership and reconstruct content.
- Use a reference corpus to test inversion.
- Compare scores to infer record membership.
- Search for collisions that bypass text-only checks.
- Minimise returned precision and sensitive corpus exposure.

---

# MCP expands the trust boundary in both directions
> Tools, resources, prompts, sampling, and transport are separate attack surfaces.
- Server metadata influences the host before a tool executes.
- Tool results and resources can carry indirect instructions.
- Servers can ask clients to sample or elicit information.
- Transport and authorization mistakes bypass model safeguards entirely.

---

# Tool metadata is executable influence unless the host treats it as data
> Descriptions and schemas can poison planning before user approval.
- Inspect the full `tools/list` response.
- Compare names, parameter descriptions, and invisible characters.
- Pin definitions and diff them after installation.
- Present the exact model-visible text to the approver.

---

# Resources and prompts can cross privilege boundaries silently
> A benign read can become an instruction-bearing payload.
- Traverse resource paths and inspect URI authorization.
- Inject prompt arguments into privileged template sections.
- Keep untrusted arguments in data-only message roles.
- Enforce access at the server, independent of model intent.

---

# Sampling and elicitation reverse the expected control flow
> An MCP server can drive the client’s model and ask the user for secrets.
- Log every server-initiated sampling request.
- Show system prompts and messages before approval.
- Never auto-answer credential or identity questions.
- Scope and rate-limit these capabilities per server.

---

# Roots, logs, and completion are disclosure surfaces
> Auxiliary MCP features need the same authorization as tools.
- Verify that resource reads remain inside declared roots.
- Treat debug logging as sensitive output.
- Test completion endpoints for secret enumeration.
- Disable capabilities the client does not need.

---

# Approval-time safety does not prevent a runtime rug pull
> A tool can change after the user has learned to trust it.
- Capture definitions and behavior at first approval.
- Repeat calls and compare outputs over time.
- Re-review on metadata or binary changes.
- Sandbox execution even when behavior initially looks benign.

---

# Protocol routing must agree on one authoritative method
> Header/body disagreement can turn an allowed request into a privileged action.
- Send conflicting routing metadata and JSON-RPC bodies.
- Observe which layer makes the authorization decision.
- Canonicalise once, then authorize the canonical request.
- Reject duplicate or contradictory routing signals.

---

# Invisible Unicode defeats reviews that scan only rendered text
> Security controls must inspect the bytes the model will consume.
- Look for zero-width, bidi, and Unicode tag characters.
- Normalise before display, scanning, and model ingestion.
- Provide a raw or hexdump approval view.
- Sign and pin tool definitions after canonicalisation.

---

# AI supply chains contain executable artifacts, data, adapters, and packages
> “Model file” does not mean “passive data.”
- Unsafe deserialisation can execute during model load.
- Poisoned datasets and adapters introduce hidden triggers.
- Dependency confusion replaces trusted packages.
- Verify origin, digest, format, and isolated load behavior.

---

# Cloud metadata and open admin APIs turn AI flaws into infrastructure compromise
> Model-facing services often carry ambient cloud authority.
- Use SSRF to test access to metadata endpoints.
- Enumerate inference administration without credentials.
- Inspect registries and model cards for embedded secrets.
- Apply egress controls and workload identity boundaries.

---

# Threat models must describe relationships, not keyword lists
> A useful model names assets, trust crossings, and complete attack chains.
- Inventory prompts, secrets, tools, data, models, and agents.
- Map who can introduce content and who can cause effects.
- Rank multi-step paths by likelihood and impact.
- Tie every mitigation to a specific boundary.

---

# The capstone proves that small weaknesses compose
> Initial access, ambient authority, and exfiltration form one engagement.
- Seed an indirect instruction.
- Pivot through an over-privileged tool to a vault record.
- Exfiltrate the crown jewel through an allowed action.
- Report the chain and the controls that would break it.

---

# DVAA teaches agent abuse from beginner prompts to expert chains
> Its 22 challenges pair objectives, hints, solutions, and defenses.
- Begin with prompt and credential disclosure.
- Progress through context, memory, MCP, and tool registry attacks.
- Combine primitives in SecureBot and A2A expert scenarios.
- Use its embedded solution criteria as the upstream authority.

---

# Expert agent attacks exploit composition and persistence
> The hardest DVAA tasks require several individually familiar mistakes.
- Establish a foothold through prompt or tool influence.
- Persist through memory or context manipulation.
- Cross into another agent or service.
- Preserve an evidence trail for every link in the chain.

---

# MCPGoat makes difficulty progression explicit
> Each concept has Easy, Moderate, Difficult, and Secure behavior.
- Easy reveals the primitive directly.
- Moderate adds weak filtering or a second precondition.
- Difficult requires chaining, blind inference, or encoding.
- Secure demonstrates the intended defense and should block the attack.

---

# MCP security includes authorization, transport, and resource exhaustion
> Prompt-focused testing alone misses half the protocol risk.
- Test confused deputies, IDOR, OAuth audience, and session prediction.
- Probe Origin, CORS, DNS rebinding, and routing assumptions.
- Exercise SQL, NoSQL, SSTI, XXE, and deserialisation sinks.
- Bound cost, regex work, payload size, and concurrency.

---

# DVMCP is a compact progression from injection to a multi-vector chain
> Ten servers isolate core MCP failure modes before combining them.
- Prompt injection and tool poisoning establish the basics.
- Permission scope, token theft, and shadowing add authority.
- Command execution and remote control show host impact.
- Challenge 10 composes metadata, file access, auth, and execution.

---

# Appsecco emphasises realistic MCP integration mistakes
> Its nine labs are demonstrations rather than a unified flag suite.
- Traverse a “workspace” and exercise unsafe code actions.
- Compare stdio, SSE, and Streamable HTTP injection paths.
- Inspect malicious tools, typosquats, and old dependencies.
- Trace secrets and untrusted public content through tool results.

---

# Defense works as layers around authority
> No single prompt rule can secure an agentic system.
- **Content:** canonicalise, label, and separate instructions from data.
- **Identity:** authenticate callers, servers, agents, and objects.
- **Execution:** validate arguments, avoid shells, sandbox, and deny egress.
- **Lifecycle:** pin, diff, monitor, rate-limit, and retain evidence.

---

# Codespaces is the shortest path from GitHub login to a private range
> The harness should run inside the Codespace or connect over authenticated SSH.
- Open the repository Codespace and wait for readiness.
- Use `range`, `redsec`, and `assess` from its terminal.
- Keep forwarded challenge ports private.
- Enable external ranges only when you need them.

---

# Fly is an optional private attacking machine
> Use it for a dedicated ephemeral session, then destroy the app.
- Deploy a focused module or selected ranges.
- Drive it through Fly SSH, `exec.sh`, or `model.sh`.
- Proxy a target only to local loopback when needed.
- Billing and trial runtime limits apply.

---

# A four-week path builds skill through deliberate repetition
> Depth comes from explaining the boundary after every exploit.
- **Week 1:** modules 01–03 and DVAA beginner/intermediate
- **Week 2:** A2A, RAG, embeddings, and DVAA expert chains
- **Week 3:** module 07, MCPGoat, DVMCP, and Appsecco
- **Week 4:** supply chain, cloud infrastructure, threat model, capstone

---

# Finish each challenge with a defensible explanation
> The payload is temporary; the mental model is the durable skill.
- What untrusted value crossed which boundary?
- Which principal supplied the authority?
- What observable evidence proved impact?
- Which control would have broken the chain earliest?
