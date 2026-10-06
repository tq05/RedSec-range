# `builtin` defensive threat models

> Generated with `Codex-GPT-6-static-review` at reasoning effort `high` from repository commit `67491bee35bf6f3e38da47a094725714eafab2dd`. Human review is required.

**Ownership:** RedSec Range · **Concepts:** 43 · **Declared variants:** 43

Runtime exploitability is **not verified—outside the current scope**. These are defensive design
reviews derived from curated repository metadata; no target, solution, or exploit was run.

<a id="builtin-01-first-contact"></a>

## `builtin/01/first-contact` — First contact -- coax the orientation flag out of the Guide

**Risk:** high · **Confidence:** high · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** First contact -- coax the orientation flag out of the Guide is a builtin training concept for direct-injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Adversarial instructions can be treated as authority, displace intended policy, or steer downstream tools and disclosures.

### Assets

- System instructions and policy context
- Conversation integrity and safety decisions
- Downstream tools, secrets, and protected data

### Trust boundaries

- Untrusted content to model context
- Model output to application policy
- Model recommendation to effectful tool

### Threat actors and preconditions

- Actor: A user supplying adversarial instructions
- Actor: A contributor controlling retrieved or remote content
- Precondition: The application mixes untrusted content with authoritative instructions without provenance
- Precondition: A model decision can trigger disclosure or effects without an independent policy check

### High-level abuse paths

1. **Scenario:** Untrusted text is incorporated into model context and interpreted as an instruction. **Impact:** The model may reveal protected context or recommend an unauthorized action.
2. **Scenario:** A model-influenced action reaches a tool under ambient authority. **Impact:** The system performs an effect the originating actor could not directly authorize.

### Secure before abuse

- Label content by provenance and keep untrusted data structurally separate from system policy and tool instructions.
- Authorize every sensitive disclosure and tool effect in deterministic application code using the originating identity and object.
- Constrain tools with narrow schemas, allowlisted destinations, least-privilege credentials, and explicit approval for high-impact effects.
- Treat system prompts as non-secret policy hints and keep credentials and enforcement logic outside model context.

**Expected security outcome:** Untrusted instructions may influence text generation but cannot independently authorize disclosure, identity changes, or protected effects.

### Detection and response

- Log content provenance, policy decisions, tool proposals, approvals, and effects with a shared trace identifier.
- Alert on instruction-like content from data channels and unusual sequences of denied or high-impact tool requests.

### Safe defensive validation

- Submit inert conflicting instructions through each supported content channel and assert protected actions remain denied.
- Replace sensitive tools with recording doubles and confirm the policy layer blocks unauthorized proposals independent of model wording.

### Residual risk

- Models may still produce misleading content that requires user-interface provenance and review.
- Novel encodings and cross-channel context can evade content classifiers, so effect-layer enforcement remains essential.

### Evidence and limitations

- `modules/01-intro/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-02-fingerprint-model"></a>

## `builtin/02/fingerprint-model` — Fingerprint the backing model/provider

**Risk:** medium · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection

**System context:** Fingerprint the backing model/provider is a builtin training concept for recon. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Excessive service, model, route, or configuration disclosure can accelerate targeted abuse and expose credentials or internal control assumptions.

### Assets

- Service topology and model/provider metadata
- Configuration and diagnostic data
- Administrative routes and version information

### Trust boundaries

- Unauthenticated caller to public API
- Application error handling to internal configuration
- Documented API surface to internal routes

### Threat actors and preconditions

- Actor: An unauthenticated remote caller
- Actor: A low-privilege tenant enumerating shared infrastructure
- Precondition: Responses or errors reveal internal metadata beyond operational need
- Precondition: Route discovery and diagnostics are reachable without appropriate authorization

### High-level abuse paths

1. **Scenario:** A caller compares normal and exceptional responses to infer implementation and hidden surfaces. **Impact:** The attacker gains a reliable map for later targeted attempts.
2. **Scenario:** Verbose diagnostics return configuration or secret-bearing state. **Impact:** Sensitive operational data crosses into an untrusted response.

### Secure before abuse

- Return a minimal, stable public error contract and keep stack, provider, model, build, and configuration details in protected telemetry.
- Require strong authorization for inventory, diagnostics, schema, and administrative routes.
- Apply response-field allowlists and automated secret scanning before serializing configuration or errors.
- Maintain an explicit external API inventory and fail builds when undeclared routes become reachable.

**Expected security outcome:** Untrusted callers receive only the metadata required for the public contract, while sensitive diagnostics remain authorized and auditable.

### Detection and response

- Alert on route enumeration, repeated malformed requests, and diagnostic access by unusual identities.
- Correlate disclosure attempts with later access to administrative or model-management surfaces.

### Safe defensive validation

- Use inert malformed requests and assert public responses contain only the documented error schema.
- Compare the discovered unauthenticated route set with an approved allowlist in a disposable test deployment.

### Residual risk

- Timing, capability differences, and necessary protocol metadata can still support limited fingerprinting.
- New framework defaults may add discovery or documentation routes.

### Evidence and limitations

- `modules/02-recon/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-02-enumerate-surfaces"></a>

## `builtin/02/enumerate-surfaces` — Discover an undocumented internal endpoint

**Risk:** medium · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection

**System context:** Discover an undocumented internal endpoint is a builtin training concept for recon. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Excessive service, model, route, or configuration disclosure can accelerate targeted abuse and expose credentials or internal control assumptions.

### Assets

- Service topology and model/provider metadata
- Configuration and diagnostic data
- Administrative routes and version information

### Trust boundaries

- Unauthenticated caller to public API
- Application error handling to internal configuration
- Documented API surface to internal routes

### Threat actors and preconditions

- Actor: An unauthenticated remote caller
- Actor: A low-privilege tenant enumerating shared infrastructure
- Precondition: Responses or errors reveal internal metadata beyond operational need
- Precondition: Route discovery and diagnostics are reachable without appropriate authorization

### High-level abuse paths

1. **Scenario:** A caller compares normal and exceptional responses to infer implementation and hidden surfaces. **Impact:** The attacker gains a reliable map for later targeted attempts.
2. **Scenario:** Verbose diagnostics return configuration or secret-bearing state. **Impact:** Sensitive operational data crosses into an untrusted response.

### Secure before abuse

- Return a minimal, stable public error contract and keep stack, provider, model, build, and configuration details in protected telemetry.
- Require strong authorization for inventory, diagnostics, schema, and administrative routes.
- Apply response-field allowlists and automated secret scanning before serializing configuration or errors.
- Maintain an explicit external API inventory and fail builds when undeclared routes become reachable.

**Expected security outcome:** Untrusted callers receive only the metadata required for the public contract, while sensitive diagnostics remain authorized and auditable.

### Detection and response

- Alert on route enumeration, repeated malformed requests, and diagnostic access by unusual identities.
- Correlate disclosure attempts with later access to administrative or model-management surfaces.

### Safe defensive validation

- Use inert malformed requests and assert public responses contain only the documented error schema.
- Compare the discovered unauthenticated route set with an approved allowlist in a disposable test deployment.

### Residual risk

- Timing, capability differences, and necessary protocol metadata can still support limited fingerprinting.
- New framework defaults may add discovery or documentation routes.

### Evidence and limitations

- `modules/02-recon/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-02-leak-config"></a>

## `builtin/02/leak-config` — Dump service config via a verbose error

**Risk:** medium · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection

**System context:** Dump service config via a verbose error is a builtin training concept for recon. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Excessive service, model, route, or configuration disclosure can accelerate targeted abuse and expose credentials or internal control assumptions.

### Assets

- Service topology and model/provider metadata
- Configuration and diagnostic data
- Administrative routes and version information

### Trust boundaries

- Unauthenticated caller to public API
- Application error handling to internal configuration
- Documented API surface to internal routes

### Threat actors and preconditions

- Actor: An unauthenticated remote caller
- Actor: A low-privilege tenant enumerating shared infrastructure
- Precondition: Responses or errors reveal internal metadata beyond operational need
- Precondition: Route discovery and diagnostics are reachable without appropriate authorization

### High-level abuse paths

1. **Scenario:** A caller compares normal and exceptional responses to infer implementation and hidden surfaces. **Impact:** The attacker gains a reliable map for later targeted attempts.
2. **Scenario:** Verbose diagnostics return configuration or secret-bearing state. **Impact:** Sensitive operational data crosses into an untrusted response.

### Secure before abuse

- Return a minimal, stable public error contract and keep stack, provider, model, build, and configuration details in protected telemetry.
- Require strong authorization for inventory, diagnostics, schema, and administrative routes.
- Apply response-field allowlists and automated secret scanning before serializing configuration or errors.
- Maintain an explicit external API inventory and fail builds when undeclared routes become reachable.

**Expected security outcome:** Untrusted callers receive only the metadata required for the public contract, while sensitive diagnostics remain authorized and auditable.

### Detection and response

- Alert on route enumeration, repeated malformed requests, and diagnostic access by unusual identities.
- Correlate disclosure attempts with later access to administrative or model-management surfaces.

### Safe defensive validation

- Use inert malformed requests and assert public responses contain only the documented error schema.
- Compare the discovered unauthenticated route set with an approved allowlist in a disposable test deployment.

### Residual risk

- Timing, capability differences, and necessary protocol metadata can still support limited fingerprinting.
- New framework defaults may add discovery or documentation routes.

### Evidence and limitations

- `modules/02-recon/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-03-sys-prompt-leak"></a>

## `builtin/03/sys-prompt-leak` — Direct prompt injection -> leak the system prompt

**Risk:** high · **Confidence:** high · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Direct prompt injection -> leak the system prompt is a builtin training concept for direct-injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Adversarial instructions can be treated as authority, displace intended policy, or steer downstream tools and disclosures.

### Assets

- System instructions and policy context
- Conversation integrity and safety decisions
- Downstream tools, secrets, and protected data

### Trust boundaries

- Untrusted content to model context
- Model output to application policy
- Model recommendation to effectful tool

### Threat actors and preconditions

- Actor: A user supplying adversarial instructions
- Actor: A contributor controlling retrieved or remote content
- Precondition: The application mixes untrusted content with authoritative instructions without provenance
- Precondition: A model decision can trigger disclosure or effects without an independent policy check

### High-level abuse paths

1. **Scenario:** Untrusted text is incorporated into model context and interpreted as an instruction. **Impact:** The model may reveal protected context or recommend an unauthorized action.
2. **Scenario:** A model-influenced action reaches a tool under ambient authority. **Impact:** The system performs an effect the originating actor could not directly authorize.

### Secure before abuse

- Label content by provenance and keep untrusted data structurally separate from system policy and tool instructions.
- Authorize every sensitive disclosure and tool effect in deterministic application code using the originating identity and object.
- Constrain tools with narrow schemas, allowlisted destinations, least-privilege credentials, and explicit approval for high-impact effects.
- Treat system prompts as non-secret policy hints and keep credentials and enforcement logic outside model context.

**Expected security outcome:** Untrusted instructions may influence text generation but cannot independently authorize disclosure, identity changes, or protected effects.

### Detection and response

- Log content provenance, policy decisions, tool proposals, approvals, and effects with a shared trace identifier.
- Alert on instruction-like content from data channels and unusual sequences of denied or high-impact tool requests.

### Safe defensive validation

- Submit inert conflicting instructions through each supported content channel and assert protected actions remain denied.
- Replace sensitive tools with recording doubles and confirm the policy layer blocks unauthorized proposals independent of model wording.

### Residual risk

- Models may still produce misleading content that requires user-interface provenance and review.
- Novel encodings and cross-channel context can evade content classifiers, so effect-layer enforcement remains essential.

### Evidence and limitations

- `modules/03-attacking-agents/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-03-indirect-injection"></a>

## `builtin/03/indirect-injection` — Indirect prompt injection via auto-retrieved notes

**Risk:** high · **Confidence:** high · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Indirect prompt injection via auto-retrieved notes is a builtin training concept for indirect-injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Adversarial instructions can be treated as authority, displace intended policy, or steer downstream tools and disclosures.

### Assets

- System instructions and policy context
- Conversation integrity and safety decisions
- Downstream tools, secrets, and protected data

### Trust boundaries

- Untrusted content to model context
- Model output to application policy
- Model recommendation to effectful tool

### Threat actors and preconditions

- Actor: A user supplying adversarial instructions
- Actor: A contributor controlling retrieved or remote content
- Precondition: The application mixes untrusted content with authoritative instructions without provenance
- Precondition: A model decision can trigger disclosure or effects without an independent policy check

### High-level abuse paths

1. **Scenario:** Untrusted text is incorporated into model context and interpreted as an instruction. **Impact:** The model may reveal protected context or recommend an unauthorized action.
2. **Scenario:** A model-influenced action reaches a tool under ambient authority. **Impact:** The system performs an effect the originating actor could not directly authorize.

### Secure before abuse

- Label content by provenance and keep untrusted data structurally separate from system policy and tool instructions.
- Authorize every sensitive disclosure and tool effect in deterministic application code using the originating identity and object.
- Constrain tools with narrow schemas, allowlisted destinations, least-privilege credentials, and explicit approval for high-impact effects.
- Treat system prompts as non-secret policy hints and keep credentials and enforcement logic outside model context.

**Expected security outcome:** Untrusted instructions may influence text generation but cannot independently authorize disclosure, identity changes, or protected effects.

### Detection and response

- Log content provenance, policy decisions, tool proposals, approvals, and effects with a shared trace identifier.
- Alert on instruction-like content from data channels and unusual sequences of denied or high-impact tool requests.

### Safe defensive validation

- Submit inert conflicting instructions through each supported content channel and assert protected actions remain denied.
- Replace sensitive tools with recording doubles and confirm the policy layer blocks unauthorized proposals independent of model wording.

### Residual risk

- Models may still produce misleading content that requires user-interface provenance and review.
- Novel encodings and cross-channel context can evade content classifiers, so effect-layer enforcement remains essential.

### Evidence and limitations

- `modules/03-attacking-agents/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-03-tool-exfil"></a>

## `builtin/03/tool-exfil` — Excessive agency -> exfiltrate the mail API key

**Risk:** high · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection, tool-execution

**System context:** Excessive agency -> exfiltrate the mail API key is a builtin training concept for tool-abuse. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Secrets or personal data can leak through prompts, errors, logs, completion APIs, metadata, tool chains, or over-broad responses.

### Assets

- API keys, tokens, credentials, and personal data
- System prompts and privileged configuration
- Logs, completions, model cards, and tool outputs

### Trust boundaries

- Secret store to application runtime
- Application or tool output to untrusted caller
- Sensitive telemetry or metadata to operators and models

### Threat actors and preconditions

- Actor: An unauthenticated or low-privilege caller
- Actor: A malicious tool, model input, or content source
- Precondition: Sensitive values are present in model-readable context, metadata, logs, or broad environment state
- Precondition: Response or tool policy does not minimize fields by caller and purpose

### High-level abuse paths

1. **Scenario:** A caller causes a response path to serialize sensitive context or metadata. **Impact:** Credentials or protected data leave their intended trust boundary.
2. **Scenario:** A tool or model with ambient access forwards data to an unauthorized destination. **Impact:** The leak enables impersonation or lateral movement.

### Secure before abuse

- Keep credentials outside prompts, model cards, logs, completions, and general environment state; fetch them just in time through a scoped broker.
- Apply response-field allowlists, data classification, tenant authorization, destination policy, and output minimization at the owning service.
- Use short-lived, audience-bound, least-privilege credentials with rotation and revocation.
- Redact sensitive fields before telemetry and prevent tool outputs from being treated as trusted instructions.

**Expected security outcome:** Sensitive values are absent from model-readable and public channels and are released only to authorized, purpose-bound consumers.

### Detection and response

- Deploy secret-pattern and canary detection at response, log, artifact, and egress boundaries with strict access controls.
- Alert on unusual secret reads, completion enumeration, debug-level changes, bulk exports, and new destinations.

### Safe defensive validation

- Seed synthetic canaries and confirm unauthorized response, error, log, metadata, and completion paths never return them.
- Exercise credential rotation and incident revocation with a test identity and verify old tokens stop working.

### Residual risk

- Authorized components necessarily handling plaintext remain high-value compromise targets.
- Previously emitted secrets require rotation even after the disclosure path is fixed.

### Evidence and limitations

- `modules/03-attacking-agents/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-03-memory-poisoning"></a>

## `builtin/03/memory-poisoning` — Memory poisoning -> persistence across turns

**Risk:** high · **Confidence:** high · **Control families:** input-content, data-protection, identity-access, logging-detection

**System context:** Memory poisoning -> persistence across turns is a builtin training concept for memory. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Poisoned or over-broad memory can persist adversarial instructions, cross identity boundaries, or disclose retained secrets in later sessions.

### Assets

- Long-term agent memory and user preferences
- Tenant-scoped credentials and personal data
- Future conversation decisions

### Trust boundaries

- Current request to persistent memory
- One tenant or session to another
- Stored memory to future model context

### Threat actors and preconditions

- Actor: A user who can write durable memory
- Actor: A compromised agent or external content source
- Precondition: Untrusted content can be persisted without provenance, scope, or review
- Precondition: Future turns retrieve memory into an authoritative context position

### High-level abuse paths

1. **Scenario:** A crafted entry is saved and repeatedly reintroduced into future contexts. **Impact:** The attacker gains persistence beyond the initiating conversation.
2. **Scenario:** Memory retrieval is insufficiently scoped by tenant or purpose. **Impact:** One user’s sensitive state becomes visible or influential elsewhere.

### Secure before abuse

- Partition memory by tenant, user, agent, purpose, and retention class with server-side authorization on every read and write.
- Store provenance, author, timestamp, and confidence; prevent untrusted entries from becoming policy or tool authority.
- Require review or bounded schemas for durable high-impact memories and support revocation and expiration.
- Encrypt sensitive memory and exclude credentials from model-readable stores.

**Expected security outcome:** Memory remains scoped, attributable, revocable, and unable to grant authority across turns or tenants.

### Detection and response

- Alert on cross-tenant retrieval attempts, rapid propagation, policy-like entries, and unusual durable-write volume.
- Maintain an audit trail for memory creation, mutation, retrieval, and deletion and support incident-wide purge.

### Safe defensive validation

- Use synthetic tenants to confirm writes and retrieval remain isolated across sessions and identities.
- Insert inert policy-shaped text and verify it is labeled as untrusted data and cannot authorize an effect.

### Residual risk

- Legitimate but misleading memories can influence model quality without violating access control.
- Backups and derived indexes can delay complete deletion.

### Evidence and limitations

- `modules/03-attacking-agents/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-04-trust-exploitation"></a>

## `builtin/04/trust-exploitation` — Transitive trust -> reviewer acts on your ticket

**Risk:** high · **Confidence:** high · **Control families:** identity-access, protocol-integrity, tool-execution, logging-detection

**System context:** Transitive trust -> reviewer acts on your ticket is a builtin training concept for a2a-trust. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Weak identity, message integrity, or delegation scoping can let an agent impersonate a trusted peer, smuggle session state, or exercise transitive authority.

### Assets

- Agent identities, cards, and delegated authority
- A2A messages, tasks, and context state
- Protected actions reached through agent delegation

### Trust boundaries

- Remote agent to receiving agent
- Agent Card discovery to runtime identity
- Delegated task to protected tool or data

### Threat actors and preconditions

- Actor: A malicious or impersonated peer agent
- Actor: A compromised trusted agent in a delegation chain
- Precondition: Messages or context identifiers are accepted without strong peer and task binding
- Precondition: Transitive trust grants a downstream agent more authority than the originating principal

### High-level abuse paths

1. **Scenario:** A forged or replayed message is associated with a trusted agent or task. **Impact:** The receiver performs an unauthorized workflow step.
2. **Scenario:** A valid agent delegates ambient authority without preserving the originating principal and constraints. **Impact:** A downstream action exceeds the user’s intended scope.

### Secure before abuse

- Authenticate peers cryptographically and bind Agent Cards, keys, audience, issuer, and service endpoints through trusted discovery.
- Sign messages and bind task, context, sender, recipient, nonce, expiry, and replay state before processing.
- Propagate the originating principal and attenuated capability through every delegation; re-authorize each protected effect.
- Partition task state by tenant and peer, and require approval for sensitive cross-agent actions.

**Expected security outcome:** Every A2A message and delegated effect is bound to an authenticated peer, scoped task, originating principal, and replay-safe context.

### Detection and response

- Record peer identity, card/key version, task and context identifiers, delegation chain, policy decision, and final effect.
- Alert on replay, identity-card drift, impossible task transitions, context reuse across tenants, and unusual delegation depth.

### Safe defensive validation

- Use synthetic peers to confirm unsigned, expired, replayed, wrong-audience, and cross-context messages fail closed.
- Exercise a benign multi-agent workflow and verify the least-privileged originating identity is preserved at the final effect.

### Residual risk

- A fully compromised authorized peer can issue valid but malicious requests within its remaining scope.
- Federated key rotation and trust-store drift can create temporary acceptance gaps.

### Evidence and limitations

- `modules/04-multi-agent-a2a/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-04-message-manipulation"></a>

## `builtin/04/message-manipulation` — Send an unsigned A2A JSON-RPC message

**Risk:** high · **Confidence:** high · **Control families:** identity-access, protocol-integrity, tool-execution, logging-detection

**System context:** Send an unsigned A2A JSON-RPC message is a builtin training concept for a2a-message/send. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Weak identity, message integrity, or delegation scoping can let an agent impersonate a trusted peer, smuggle session state, or exercise transitive authority.

### Assets

- Agent identities, cards, and delegated authority
- A2A messages, tasks, and context state
- Protected actions reached through agent delegation

### Trust boundaries

- Remote agent to receiving agent
- Agent Card discovery to runtime identity
- Delegated task to protected tool or data

### Threat actors and preconditions

- Actor: A malicious or impersonated peer agent
- Actor: A compromised trusted agent in a delegation chain
- Precondition: Messages or context identifiers are accepted without strong peer and task binding
- Precondition: Transitive trust grants a downstream agent more authority than the originating principal

### High-level abuse paths

1. **Scenario:** A forged or replayed message is associated with a trusted agent or task. **Impact:** The receiver performs an unauthorized workflow step.
2. **Scenario:** A valid agent delegates ambient authority without preserving the originating principal and constraints. **Impact:** A downstream action exceeds the user’s intended scope.

### Secure before abuse

- Authenticate peers cryptographically and bind Agent Cards, keys, audience, issuer, and service endpoints through trusted discovery.
- Sign messages and bind task, context, sender, recipient, nonce, expiry, and replay state before processing.
- Propagate the originating principal and attenuated capability through every delegation; re-authorize each protected effect.
- Partition task state by tenant and peer, and require approval for sensitive cross-agent actions.

**Expected security outcome:** Every A2A message and delegated effect is bound to an authenticated peer, scoped task, originating principal, and replay-safe context.

### Detection and response

- Record peer identity, card/key version, task and context identifiers, delegation chain, policy decision, and final effect.
- Alert on replay, identity-card drift, impossible task transitions, context reuse across tenants, and unusual delegation depth.

### Safe defensive validation

- Use synthetic peers to confirm unsigned, expired, replayed, wrong-audience, and cross-context messages fail closed.
- Exercise a benign multi-agent workflow and verify the least-privileged originating identity is preserved at the final effect.

### Residual risk

- A fully compromised authorized peer can issue valid but malicious requests within its remaining scope.
- Federated key rotation and trust-store drift can create temporary acceptance gaps.

### Evidence and limitations

- `modules/04-multi-agent-a2a/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-04-agent-impersonation"></a>

## `builtin/04/agent-impersonation` — Impersonate a trusted approver

**Risk:** high · **Confidence:** high · **Control families:** identity-access, protocol-integrity, tool-execution, logging-detection

**System context:** Impersonate a trusted approver is a builtin training concept for a2a-message-identity. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Weak identity, message integrity, or delegation scoping can let an agent impersonate a trusted peer, smuggle session state, or exercise transitive authority.

### Assets

- Agent identities, cards, and delegated authority
- A2A messages, tasks, and context state
- Protected actions reached through agent delegation

### Trust boundaries

- Remote agent to receiving agent
- Agent Card discovery to runtime identity
- Delegated task to protected tool or data

### Threat actors and preconditions

- Actor: A malicious or impersonated peer agent
- Actor: A compromised trusted agent in a delegation chain
- Precondition: Messages or context identifiers are accepted without strong peer and task binding
- Precondition: Transitive trust grants a downstream agent more authority than the originating principal

### High-level abuse paths

1. **Scenario:** A forged or replayed message is associated with a trusted agent or task. **Impact:** The receiver performs an unauthorized workflow step.
2. **Scenario:** A valid agent delegates ambient authority without preserving the originating principal and constraints. **Impact:** A downstream action exceeds the user’s intended scope.

### Secure before abuse

- Authenticate peers cryptographically and bind Agent Cards, keys, audience, issuer, and service endpoints through trusted discovery.
- Sign messages and bind task, context, sender, recipient, nonce, expiry, and replay state before processing.
- Propagate the originating principal and attenuated capability through every delegation; re-authorize each protected effect.
- Partition task state by tenant and peer, and require approval for sensitive cross-agent actions.

**Expected security outcome:** Every A2A message and delegated effect is bound to an authenticated peer, scoped task, originating principal, and replay-safe context.

### Detection and response

- Record peer identity, card/key version, task and context identifiers, delegation chain, policy decision, and final effect.
- Alert on replay, identity-card drift, impossible task transitions, context reuse across tenants, and unusual delegation depth.

### Safe defensive validation

- Use synthetic peers to confirm unsigned, expired, replayed, wrong-audience, and cross-context messages fail closed.
- Exercise a benign multi-agent workflow and verify the least-privileged originating identity is preserved at the final effect.

### Residual risk

- A fully compromised authorized peer can issue valid but malicious requests within its remaining scope.
- Federated key rotation and trust-store drift can create temporary acceptance gaps.

### Evidence and limitations

- `modules/04-multi-agent-a2a/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-04-session-smuggling"></a>

## `builtin/04/session-smuggling` — Agent session smuggling across a stateful A2A session

**Risk:** high · **Confidence:** high · **Control families:** identity-access, protocol-integrity, tool-execution, logging-detection

**System context:** Agent session smuggling across a stateful A2A session is a builtin training concept for a2a-context. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Weak identity, message integrity, or delegation scoping can let an agent impersonate a trusted peer, smuggle session state, or exercise transitive authority.

### Assets

- Agent identities, cards, and delegated authority
- A2A messages, tasks, and context state
- Protected actions reached through agent delegation

### Trust boundaries

- Remote agent to receiving agent
- Agent Card discovery to runtime identity
- Delegated task to protected tool or data

### Threat actors and preconditions

- Actor: A malicious or impersonated peer agent
- Actor: A compromised trusted agent in a delegation chain
- Precondition: Messages or context identifiers are accepted without strong peer and task binding
- Precondition: Transitive trust grants a downstream agent more authority than the originating principal

### High-level abuse paths

1. **Scenario:** A forged or replayed message is associated with a trusted agent or task. **Impact:** The receiver performs an unauthorized workflow step.
2. **Scenario:** A valid agent delegates ambient authority without preserving the originating principal and constraints. **Impact:** A downstream action exceeds the user’s intended scope.

### Secure before abuse

- Authenticate peers cryptographically and bind Agent Cards, keys, audience, issuer, and service endpoints through trusted discovery.
- Sign messages and bind task, context, sender, recipient, nonce, expiry, and replay state before processing.
- Propagate the originating principal and attenuated capability through every delegation; re-authorize each protected effect.
- Partition task state by tenant and peer, and require approval for sensitive cross-agent actions.

**Expected security outcome:** Every A2A message and delegated effect is bound to an authenticated peer, scoped task, originating principal, and replay-safe context.

### Detection and response

- Record peer identity, card/key version, task and context identifiers, delegation chain, policy decision, and final effect.
- Alert on replay, identity-card drift, impossible task transitions, context reuse across tenants, and unusual delegation depth.

### Safe defensive validation

- Use synthetic peers to confirm unsigned, expired, replayed, wrong-audience, and cross-context messages fail closed.
- Exercise a benign multi-agent workflow and verify the least-privileged originating identity is preserved at the final effect.

### Residual risk

- A fully compromised authorized peer can issue valid but malicious requests within its remaining scope.
- Federated key rotation and trust-store drift can create temporary acceptance gaps.

### Evidence and limitations

- `modules/04-multi-agent-a2a/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-05-knowledge-poisoning"></a>

## `builtin/05/knowledge-poisoning` — Poison the knowledge base

**Risk:** medium · **Confidence:** high · **Control families:** input-content, data-protection, identity-access, logging-detection

**System context:** Poison the knowledge base is a builtin training concept for rag-source. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Poisoned, manipulated, or falsely attributed retrieval results can steer model decisions and make untrusted content appear authoritative.

### Assets

- Knowledge corpus and ingestion pipeline
- Retrieval ranking and citation provenance
- Answers and decisions grounded in retrieved content

### Trust boundaries

- Content contributor to indexed corpus
- Retriever results to model context
- Citation metadata to user trust decision

### Threat actors and preconditions

- Actor: A malicious document contributor
- Actor: A tenant attempting to influence another tenant’s retrieval
- Precondition: Content can enter the corpus without provenance, authorization, or quality gates
- Precondition: Ranking or citation display is trusted without object-level validation

### High-level abuse paths

1. **Scenario:** An attacker introduces or optimizes content so it dominates a target query. **Impact:** The model is grounded in attacker-controlled claims or instructions.
2. **Scenario:** Citation metadata is accepted independently of the retrieved object’s verified provenance. **Impact:** Users attribute malicious output to a trusted source.

### Secure before abuse

- Authorize ingestion by tenant and source, verify provenance, scan content, and preserve immutable origin metadata through chunking and indexing.
- Separate retrieved data from instructions and apply effect-layer authorization to any model-proposed action.
- Use ranking diversity, source reputation, freshness limits, and anomaly controls rather than similarity alone.
- Render citations from server-verified document identifiers and enforce tenant filtering before retrieval.

**Expected security outcome:** Retrieved content remains attributable and tenant-scoped, and cannot acquire policy authority or a trusted citation through ranking alone.

### Detection and response

- Monitor ingestion changes, source concentration, ranking shifts, duplicate clusters, and cross-tenant filter failures.
- Support rapid quarantine and re-indexing of a compromised source while preserving audit evidence.

### Safe defensive validation

- Add benign canary documents from untrusted and trusted sources and assert provenance and tenant filters survive retrieval.
- Perturb synthetic ranking inputs and verify one low-trust source cannot monopolize results or forge citation identity.

### Residual risk

- Factually plausible poisoning can evade automated content review.
- Embedding and ranking changes can alter exposure without an obvious code change.

### Evidence and limitations

- `modules/05-rag-pipelines/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-05-retrieval-manipulation"></a>

## `builtin/05/retrieval-manipulation` — Out-rank the real documents for a victim query

**Risk:** medium · **Confidence:** high · **Control families:** input-content, data-protection, identity-access, logging-detection

**System context:** Out-rank the real documents for a victim query is a builtin training concept for rag-retrieval. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Poisoned, manipulated, or falsely attributed retrieval results can steer model decisions and make untrusted content appear authoritative.

### Assets

- Knowledge corpus and ingestion pipeline
- Retrieval ranking and citation provenance
- Answers and decisions grounded in retrieved content

### Trust boundaries

- Content contributor to indexed corpus
- Retriever results to model context
- Citation metadata to user trust decision

### Threat actors and preconditions

- Actor: A malicious document contributor
- Actor: A tenant attempting to influence another tenant’s retrieval
- Precondition: Content can enter the corpus without provenance, authorization, or quality gates
- Precondition: Ranking or citation display is trusted without object-level validation

### High-level abuse paths

1. **Scenario:** An attacker introduces or optimizes content so it dominates a target query. **Impact:** The model is grounded in attacker-controlled claims or instructions.
2. **Scenario:** Citation metadata is accepted independently of the retrieved object’s verified provenance. **Impact:** Users attribute malicious output to a trusted source.

### Secure before abuse

- Authorize ingestion by tenant and source, verify provenance, scan content, and preserve immutable origin metadata through chunking and indexing.
- Separate retrieved data from instructions and apply effect-layer authorization to any model-proposed action.
- Use ranking diversity, source reputation, freshness limits, and anomaly controls rather than similarity alone.
- Render citations from server-verified document identifiers and enforce tenant filtering before retrieval.

**Expected security outcome:** Retrieved content remains attributable and tenant-scoped, and cannot acquire policy authority or a trusted citation through ranking alone.

### Detection and response

- Monitor ingestion changes, source concentration, ranking shifts, duplicate clusters, and cross-tenant filter failures.
- Support rapid quarantine and re-indexing of a compromised source while preserving audit evidence.

### Safe defensive validation

- Add benign canary documents from untrusted and trusted sources and assert provenance and tenant filters survive retrieval.
- Perturb synthetic ranking inputs and verify one low-trust source cannot monopolize results or forge citation identity.

### Residual risk

- Factually plausible poisoning can evade automated content review.
- Embedding and ranking changes can alter exposure without an obvious code change.

### Evidence and limitations

- `modules/05-rag-pipelines/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-05-citation-spoofing"></a>

## `builtin/05/citation-spoofing` — Spoof a trusted citation

**Risk:** high · **Confidence:** high · **Control families:** input-content, data-protection, identity-access, logging-detection

**System context:** Spoof a trusted citation is a builtin training concept for rag-trust. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Poisoned, manipulated, or falsely attributed retrieval results can steer model decisions and make untrusted content appear authoritative.

### Assets

- Knowledge corpus and ingestion pipeline
- Retrieval ranking and citation provenance
- Answers and decisions grounded in retrieved content

### Trust boundaries

- Content contributor to indexed corpus
- Retriever results to model context
- Citation metadata to user trust decision

### Threat actors and preconditions

- Actor: A malicious document contributor
- Actor: A tenant attempting to influence another tenant’s retrieval
- Precondition: Content can enter the corpus without provenance, authorization, or quality gates
- Precondition: Ranking or citation display is trusted without object-level validation

### High-level abuse paths

1. **Scenario:** An attacker introduces or optimizes content so it dominates a target query. **Impact:** The model is grounded in attacker-controlled claims or instructions.
2. **Scenario:** Citation metadata is accepted independently of the retrieved object’s verified provenance. **Impact:** Users attribute malicious output to a trusted source.

### Secure before abuse

- Authorize ingestion by tenant and source, verify provenance, scan content, and preserve immutable origin metadata through chunking and indexing.
- Separate retrieved data from instructions and apply effect-layer authorization to any model-proposed action.
- Use ranking diversity, source reputation, freshness limits, and anomaly controls rather than similarity alone.
- Render citations from server-verified document identifiers and enforce tenant filtering before retrieval.

**Expected security outcome:** Retrieved content remains attributable and tenant-scoped, and cannot acquire policy authority or a trusted citation through ranking alone.

### Detection and response

- Monitor ingestion changes, source concentration, ranking shifts, duplicate clusters, and cross-tenant filter failures.
- Support rapid quarantine and re-indexing of a compromised source while preserving audit evidence.

### Safe defensive validation

- Add benign canary documents from untrusted and trusted sources and assert provenance and tenant filters survive retrieval.
- Perturb synthetic ranking inputs and verify one low-trust source cannot monopolize results or forge citation identity.

### Residual risk

- Factually plausible poisoning can evade automated content review.
- Embedding and ranking changes can alter exposure without an obvious code change.

### Evidence and limitations

- `modules/05-rag-pipelines/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-06-embedding-inversion"></a>

## `builtin/06/embedding-inversion` — Reconstruct source text with a reference corpus

**Risk:** high · **Confidence:** high · **Control families:** data-protection, identity-access, resource-governance, logging-detection

**System context:** Reconstruct source text with a reference corpus is a builtin training concept for embedding-inversion. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Adaptive vector queries can reveal source content or membership, while embedding collisions can bypass controls that treat semantic similarity as authorization.

### Assets

- Embedding vectors and source records
- Membership and tenant privacy
- Similarity-based security decisions

### Trust boundaries

- Query client to embedding service
- Vector index to source text
- Similarity score to authorization or filtering decision

### Threat actors and preconditions

- Actor: A curious or malicious query client
- Actor: A tenant probing a shared vector index
- Precondition: The service exposes precise vectors, scores, or unrestricted adaptive queries
- Precondition: Similarity or text checks are used as a security boundary

### High-level abuse paths

1. **Scenario:** A caller makes correlated queries and compares detailed outputs against reference data. **Impact:** Sensitive source content or membership is inferred.
2. **Scenario:** A crafted input is semantically close while evading a text-layer check. **Impact:** A similarity-based gate admits content the policy intended to block.

### Secure before abuse

- Authorize vector and source access by tenant and purpose; avoid exposing raw vectors or unnecessary score precision.
- Rate-limit and budget adaptive queries, and add privacy-preserving aggregation where the use case permits.
- Never use embeddings as the sole authentication, authorization, or safety control; validate protected properties deterministically.
- Separate tenant indexes or enforce mandatory pre-retrieval filters with audited object identifiers.

**Expected security outcome:** Vector interfaces reveal only purpose-limited results, and semantic similarity never substitutes for a security decision.

### Detection and response

- Detect repeated near-neighbor probes, systematic score sweeps, and cross-tenant query patterns.
- Record model/index versions so privacy or collision incidents can be scoped and reproduced.

### Safe defensive validation

- Use synthetic private records to measure whether an unauthorized client receives vectors, membership signals, or source text.
- Create benign paraphrase and collision cases and assert deterministic policy checks remain authoritative.

### Residual risk

- Useful similarity responses retain some statistical leakage.
- Model updates can change inversion, membership, and collision behavior.

### Evidence and limitations

- `modules/06-embeddings/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-06-membership-inference"></a>

## `builtin/06/membership-inference` — Confirm a record is present in the store

**Risk:** medium · **Confidence:** high · **Control families:** data-protection, identity-access, resource-governance, logging-detection

**System context:** Confirm a record is present in the store is a builtin training concept for embedding-mia. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Adaptive vector queries can reveal source content or membership, while embedding collisions can bypass controls that treat semantic similarity as authorization.

### Assets

- Embedding vectors and source records
- Membership and tenant privacy
- Similarity-based security decisions

### Trust boundaries

- Query client to embedding service
- Vector index to source text
- Similarity score to authorization or filtering decision

### Threat actors and preconditions

- Actor: A curious or malicious query client
- Actor: A tenant probing a shared vector index
- Precondition: The service exposes precise vectors, scores, or unrestricted adaptive queries
- Precondition: Similarity or text checks are used as a security boundary

### High-level abuse paths

1. **Scenario:** A caller makes correlated queries and compares detailed outputs against reference data. **Impact:** Sensitive source content or membership is inferred.
2. **Scenario:** A crafted input is semantically close while evading a text-layer check. **Impact:** A similarity-based gate admits content the policy intended to block.

### Secure before abuse

- Authorize vector and source access by tenant and purpose; avoid exposing raw vectors or unnecessary score precision.
- Rate-limit and budget adaptive queries, and add privacy-preserving aggregation where the use case permits.
- Never use embeddings as the sole authentication, authorization, or safety control; validate protected properties deterministically.
- Separate tenant indexes or enforce mandatory pre-retrieval filters with audited object identifiers.

**Expected security outcome:** Vector interfaces reveal only purpose-limited results, and semantic similarity never substitutes for a security decision.

### Detection and response

- Detect repeated near-neighbor probes, systematic score sweeps, and cross-tenant query patterns.
- Record model/index versions so privacy or collision incidents can be scoped and reproduced.

### Safe defensive validation

- Use synthetic private records to measure whether an unauthorized client receives vectors, membership signals, or source text.
- Create benign paraphrase and collision cases and assert deterministic policy checks remain authoritative.

### Residual risk

- Useful similarity responses retain some statistical leakage.
- Model updates can change inversion, membership, and collision behavior.

### Evidence and limitations

- `modules/06-embeddings/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-06-embedding-collision"></a>

## `builtin/06/embedding-collision` — Bypass a text check via an embedding collision

**Risk:** medium · **Confidence:** high · **Control families:** data-protection, identity-access, resource-governance, logging-detection

**System context:** Bypass a text check via an embedding collision is a builtin training concept for embedding-collision. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Adaptive vector queries can reveal source content or membership, while embedding collisions can bypass controls that treat semantic similarity as authorization.

### Assets

- Embedding vectors and source records
- Membership and tenant privacy
- Similarity-based security decisions

### Trust boundaries

- Query client to embedding service
- Vector index to source text
- Similarity score to authorization or filtering decision

### Threat actors and preconditions

- Actor: A curious or malicious query client
- Actor: A tenant probing a shared vector index
- Precondition: The service exposes precise vectors, scores, or unrestricted adaptive queries
- Precondition: Similarity or text checks are used as a security boundary

### High-level abuse paths

1. **Scenario:** A caller makes correlated queries and compares detailed outputs against reference data. **Impact:** Sensitive source content or membership is inferred.
2. **Scenario:** A crafted input is semantically close while evading a text-layer check. **Impact:** A similarity-based gate admits content the policy intended to block.

### Secure before abuse

- Authorize vector and source access by tenant and purpose; avoid exposing raw vectors or unnecessary score precision.
- Rate-limit and budget adaptive queries, and add privacy-preserving aggregation where the use case permits.
- Never use embeddings as the sole authentication, authorization, or safety control; validate protected properties deterministically.
- Separate tenant indexes or enforce mandatory pre-retrieval filters with audited object identifiers.

**Expected security outcome:** Vector interfaces reveal only purpose-limited results, and semantic similarity never substitutes for a security decision.

### Detection and response

- Detect repeated near-neighbor probes, systematic score sweeps, and cross-tenant query patterns.
- Record model/index versions so privacy or collision incidents can be scoped and reproduced.

### Safe defensive validation

- Use synthetic private records to measure whether an unauthorized client receives vectors, membership signals, or source text.
- Create benign paraphrase and collision cases and assert deterministic policy checks remain authoritative.

### Residual risk

- Useful similarity responses retain some statistical leakage.
- Model updates can change inversion, membership, and collision behavior.

### Evidence and limitations

- `modules/06-embeddings/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-tool-poisoning"></a>

## `builtin/07/tool-poisoning` — tools: tool-description poisoning hijacks the host

**Risk:** high · **Confidence:** high · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** tools: tool-description poisoning hijacks the host is a builtin training concept for tools. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** A malicious, shadowed, mutated, or intercepted tool can acquire trusted identity and steer the host toward unauthorized disclosure or effects.

### Assets

- Tool registry, definitions, and routing metadata
- Host approval and tool-selection integrity
- Credentials and side effects available to tools

### Trust boundaries

- Tool publisher or server to agent host
- Tool metadata and output to model context
- Selected tool to protected effect

### Threat actors and preconditions

- Actor: A malicious tool publisher or MCP server
- Actor: A compromised registry, proxy, or trusted tool
- Precondition: Tool identity or behavior can change after approval or collide with a trusted name
- Precondition: The host treats tool metadata or output as policy and grants ambient credentials

### High-level abuse paths

1. **Scenario:** A tool is approved under benign metadata and later changes behavior, identity, or instructions. **Impact:** Existing trust is reused for a malicious operation.
2. **Scenario:** A colliding or redirected tool is selected in place of the intended trusted implementation. **Impact:** Sensitive inputs or credentials reach an attacker-controlled component.

### Secure before abuse

- Bind approvals to a signed publisher identity and immutable digest of tool schema, description, endpoint, and version; require reapproval on change.
- Use server-qualified tool identifiers and deterministic routing; reject ambiguous names, redirects, and untrusted registry precedence.
- Treat descriptions and outputs as untrusted data, and authorize every effect against the originating identity in host code.
- Give each tool a narrow credential, destination allowlist, input schema, output limit, and isolated execution boundary.

**Expected security outcome:** Hosts execute only the exact approved tool identity and version, with least privilege and independent authorization at the effect boundary.

### Detection and response

- Alert on tool digest drift, registry changes, name collisions, endpoint redirection, reapproval bypass, and unusual tool sequences.
- Trace registry resolution, selected tool identity, input provenance, policy decision, and effect without logging secrets.

### Safe defensive validation

- Register inert colliding and changed tool definitions in a disposable registry and assert selection fails or requires explicit reapproval.
- Use a recording tool double to confirm untrusted metadata and output cannot authorize a protected effect.

### Residual risk

- A signed and approved publisher can still ship malicious logic within its granted scope.
- Semantic changes may evade schema-level comparison and require behavior review.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-resource-traversal"></a>

## `builtin/07/resource-traversal` — resources: path traversal in resources/read

**Risk:** high · **Confidence:** high · **Control families:** tool-execution, data-protection, identity-access, logging-detection

**System context:** resources: path traversal in resources/read is a builtin training concept for resources. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Improper path canonicalization and root enforcement can expose or modify files outside the authorized workspace.

### Assets

- Workspace files and declared roots
- Host filesystem and credentials
- File-operation audit trail

### Trust boundaries

- Untrusted path or URI to filesystem resolver
- Declared workspace root to host filesystem
- Tool identity to file authorization

### Threat actors and preconditions

- Actor: A remote tool caller
- Actor: A prompt-influenced agent using a file tool
- Precondition: Path resolution accepts traversal, absolute paths, links, or ambiguous encodings
- Precondition: The file service runs with access beyond the caller’s allowed root

### High-level abuse paths

1. **Scenario:** A caller supplies an alternate path representation that resolves beyond the declared root. **Impact:** Sensitive host data is read or modified.
2. **Scenario:** A symbolic link or race changes the resolved object after validation. **Impact:** A previously safe check authorizes a different filesystem target.

### Secure before abuse

- Resolve paths against a server-selected root, reject absolute and parent traversal forms, and verify the final opened object remains beneath that root.
- Use descriptor-relative filesystem APIs and avoid check-then-open races and link following for protected operations.
- Run the service as a dedicated non-root identity with a read-only filesystem and only the required workspace mounted.
- Authorize file operations by caller, tenant, action, and object; keep roots server-side rather than trusting client declarations.

**Expected security outcome:** File operations remain inside an authorized root and are constrained by both application checks and operating-system permissions.

### Detection and response

- Log normalized object identifiers and denied root escapes without recording sensitive file content.
- Alert on repeated invalid paths, link-related failures, and access to sensitive filename classes.

### Safe defensive validation

- Use a temporary synthetic tree to confirm parent, absolute, encoded, and link-based escape cases fail closed.
- Verify the runtime identity cannot read an unrelated canary file even if application validation is bypassed.

### Residual risk

- Platform-specific path and link semantics require regression coverage.
- Writable shared volumes can reintroduce time-of-check/time-of-use races.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-prompt-injection"></a>

## `builtin/07/prompt-injection` — prompts: argument injection discloses a privileged template block

**Risk:** high · **Confidence:** high · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** prompts: argument injection discloses a privileged template block is a builtin training concept for prompts. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Adversarial instructions can be treated as authority, displace intended policy, or steer downstream tools and disclosures.

### Assets

- System instructions and policy context
- Conversation integrity and safety decisions
- Downstream tools, secrets, and protected data

### Trust boundaries

- Untrusted content to model context
- Model output to application policy
- Model recommendation to effectful tool

### Threat actors and preconditions

- Actor: A user supplying adversarial instructions
- Actor: A contributor controlling retrieved or remote content
- Precondition: The application mixes untrusted content with authoritative instructions without provenance
- Precondition: A model decision can trigger disclosure or effects without an independent policy check

### High-level abuse paths

1. **Scenario:** Untrusted text is incorporated into model context and interpreted as an instruction. **Impact:** The model may reveal protected context or recommend an unauthorized action.
2. **Scenario:** A model-influenced action reaches a tool under ambient authority. **Impact:** The system performs an effect the originating actor could not directly authorize.

### Secure before abuse

- Label content by provenance and keep untrusted data structurally separate from system policy and tool instructions.
- Authorize every sensitive disclosure and tool effect in deterministic application code using the originating identity and object.
- Constrain tools with narrow schemas, allowlisted destinations, least-privilege credentials, and explicit approval for high-impact effects.
- Treat system prompts as non-secret policy hints and keep credentials and enforcement logic outside model context.

**Expected security outcome:** Untrusted instructions may influence text generation but cannot independently authorize disclosure, identity changes, or protected effects.

### Detection and response

- Log content provenance, policy decisions, tool proposals, approvals, and effects with a shared trace identifier.
- Alert on instruction-like content from data channels and unusual sequences of denied or high-impact tool requests.

### Safe defensive validation

- Submit inert conflicting instructions through each supported content channel and assert protected actions remain denied.
- Replace sensitive tools with recording doubles and confirm the policy layer blocks unauthorized proposals independent of model wording.

### Residual risk

- Models may still produce misleading content that requires user-interface provenance and review.
- Novel encodings and cross-channel context can evade content classifiers, so effect-layer enforcement remains essential.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-sampling-abuse"></a>

## `builtin/07/sampling-abuse` — sampling: server-initiated sampling exfiltrates host context

**Risk:** high · **Confidence:** high · **Control families:** identity-access, protocol-integrity, logging-detection, human-approval

**System context:** sampling: server-initiated sampling exfiltrates host context is a builtin training concept for sampling. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Missing object- and action-level authorization can let a caller or delegated agent access another tenant’s data or perform a privileged effect.

### Assets

- Protected objects and administrative operations
- User, agent, and service identities
- Delegation scopes and approval state

### Trust boundaries

- Caller identity to service authorization
- Agent or tool delegation to protected resource
- Object identifier to tenant ownership

### Threat actors and preconditions

- Actor: An authenticated low-privilege caller
- Actor: A confused deputy acting with ambient authority
- Precondition: The service trusts a caller-supplied object, role, scope, or audience
- Precondition: Authorization is checked only at an upstream agent rather than the owning service

### High-level abuse paths

1. **Scenario:** A valid identity substitutes an object identifier or action outside its grant. **Impact:** Protected data or operations cross a tenant or role boundary.
2. **Scenario:** A deputy receives a broad token and acts without preserving the originating principal and purpose. **Impact:** The caller gains the deputy’s ambient authority.

### Secure before abuse

- Authenticate at each service and authorize subject, tenant, object, action, purpose, and current state at the resource owner.
- Use short-lived audience-bound tokens and attenuated capabilities; never pass broad upstream credentials through to tools.
- Derive ownership and role from trusted server state rather than caller-controlled fields or model output.
- Require explicit, bound approval for high-impact actions and invalidate it when inputs, tool identity, or scope changes.

**Expected security outcome:** Every protected object and effect is authorized by its owning service for the originating principal and exact delegated scope.

### Detection and response

- Audit allow and deny decisions with subject, originating principal, audience, object, action, and policy version.
- Alert on cross-tenant identifiers, repeated denied objects, audience mismatch, and privileged actions from unusual delegation chains.

### Safe defensive validation

- Use synthetic users, tenants, roles, and audiences to confirm horizontal and vertical access attempts fail closed.
- Exercise a benign delegated workflow and assert the final service sees and enforces the original principal’s reduced scope.

### Residual risk

- Compromised authorized identities can act within their valid grants.
- Policy and identity-provider drift can temporarily create inconsistent decisions.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-roots-bypass"></a>

## `builtin/07/roots-bypass` — roots: declared client roots are not enforced

**Risk:** high · **Confidence:** high · **Control families:** tool-execution, data-protection, identity-access, logging-detection

**System context:** roots: declared client roots are not enforced is a builtin training concept for roots. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Improper path canonicalization and root enforcement can expose or modify files outside the authorized workspace.

### Assets

- Workspace files and declared roots
- Host filesystem and credentials
- File-operation audit trail

### Trust boundaries

- Untrusted path or URI to filesystem resolver
- Declared workspace root to host filesystem
- Tool identity to file authorization

### Threat actors and preconditions

- Actor: A remote tool caller
- Actor: A prompt-influenced agent using a file tool
- Precondition: Path resolution accepts traversal, absolute paths, links, or ambiguous encodings
- Precondition: The file service runs with access beyond the caller’s allowed root

### High-level abuse paths

1. **Scenario:** A caller supplies an alternate path representation that resolves beyond the declared root. **Impact:** Sensitive host data is read or modified.
2. **Scenario:** A symbolic link or race changes the resolved object after validation. **Impact:** A previously safe check authorizes a different filesystem target.

### Secure before abuse

- Resolve paths against a server-selected root, reject absolute and parent traversal forms, and verify the final opened object remains beneath that root.
- Use descriptor-relative filesystem APIs and avoid check-then-open races and link following for protected operations.
- Run the service as a dedicated non-root identity with a read-only filesystem and only the required workspace mounted.
- Authorize file operations by caller, tenant, action, and object; keep roots server-side rather than trusting client declarations.

**Expected security outcome:** File operations remain inside an authorized root and are constrained by both application checks and operating-system permissions.

### Detection and response

- Log normalized object identifiers and denied root escapes without recording sensitive file content.
- Alert on repeated invalid paths, link-related failures, and access to sensitive filename classes.

### Safe defensive validation

- Use a temporary synthetic tree to confirm parent, absolute, encoded, and link-based escape cases fail closed.
- Verify the runtime identity cannot read an unrelated canary file even if application validation is bypassed.

### Residual risk

- Platform-specific path and link semantics require regression coverage.
- Writable shared volumes can reintroduce time-of-check/time-of-use races.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-elicitation-phishing"></a>

## `builtin/07/elicitation-phishing` — elicitation: server elicits credentials the host auto-answers

**Risk:** high · **Confidence:** high · **Control families:** identity-access, protocol-integrity, logging-detection, human-approval

**System context:** elicitation: server elicits credentials the host auto-answers is a builtin training concept for elicitation. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Missing object- and action-level authorization can let a caller or delegated agent access another tenant’s data or perform a privileged effect.

### Assets

- Protected objects and administrative operations
- User, agent, and service identities
- Delegation scopes and approval state

### Trust boundaries

- Caller identity to service authorization
- Agent or tool delegation to protected resource
- Object identifier to tenant ownership

### Threat actors and preconditions

- Actor: An authenticated low-privilege caller
- Actor: A confused deputy acting with ambient authority
- Precondition: The service trusts a caller-supplied object, role, scope, or audience
- Precondition: Authorization is checked only at an upstream agent rather than the owning service

### High-level abuse paths

1. **Scenario:** A valid identity substitutes an object identifier or action outside its grant. **Impact:** Protected data or operations cross a tenant or role boundary.
2. **Scenario:** A deputy receives a broad token and acts without preserving the originating principal and purpose. **Impact:** The caller gains the deputy’s ambient authority.

### Secure before abuse

- Authenticate at each service and authorize subject, tenant, object, action, purpose, and current state at the resource owner.
- Use short-lived audience-bound tokens and attenuated capabilities; never pass broad upstream credentials through to tools.
- Derive ownership and role from trusted server state rather than caller-controlled fields or model output.
- Require explicit, bound approval for high-impact actions and invalidate it when inputs, tool identity, or scope changes.

**Expected security outcome:** Every protected object and effect is authorized by its owning service for the originating principal and exact delegated scope.

### Detection and response

- Audit allow and deny decisions with subject, originating principal, audience, object, action, and policy version.
- Alert on cross-tenant identifiers, repeated denied objects, audience mismatch, and privileged actions from unusual delegation chains.

### Safe defensive validation

- Use synthetic users, tenants, roles, and audiences to confirm horizontal and vertical access attempts fail closed.
- Exercise a benign delegated workflow and assert the final service sees and enforces the original principal’s reduced scope.

### Residual risk

- Compromised authorized identities can act within their valid grants.
- Policy and identity-provider drift can temporarily create inconsistent decisions.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-logging-leak"></a>

## `builtin/07/logging-leak` — logging: debug log notifications leak a session token

**Risk:** high · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection, tool-execution

**System context:** logging: debug log notifications leak a session token is a builtin training concept for logging. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Secrets or personal data can leak through prompts, errors, logs, completion APIs, metadata, tool chains, or over-broad responses.

### Assets

- API keys, tokens, credentials, and personal data
- System prompts and privileged configuration
- Logs, completions, model cards, and tool outputs

### Trust boundaries

- Secret store to application runtime
- Application or tool output to untrusted caller
- Sensitive telemetry or metadata to operators and models

### Threat actors and preconditions

- Actor: An unauthenticated or low-privilege caller
- Actor: A malicious tool, model input, or content source
- Precondition: Sensitive values are present in model-readable context, metadata, logs, or broad environment state
- Precondition: Response or tool policy does not minimize fields by caller and purpose

### High-level abuse paths

1. **Scenario:** A caller causes a response path to serialize sensitive context or metadata. **Impact:** Credentials or protected data leave their intended trust boundary.
2. **Scenario:** A tool or model with ambient access forwards data to an unauthorized destination. **Impact:** The leak enables impersonation or lateral movement.

### Secure before abuse

- Keep credentials outside prompts, model cards, logs, completions, and general environment state; fetch them just in time through a scoped broker.
- Apply response-field allowlists, data classification, tenant authorization, destination policy, and output minimization at the owning service.
- Use short-lived, audience-bound, least-privilege credentials with rotation and revocation.
- Redact sensitive fields before telemetry and prevent tool outputs from being treated as trusted instructions.

**Expected security outcome:** Sensitive values are absent from model-readable and public channels and are released only to authorized, purpose-bound consumers.

### Detection and response

- Deploy secret-pattern and canary detection at response, log, artifact, and egress boundaries with strict access controls.
- Alert on unusual secret reads, completion enumeration, debug-level changes, bulk exports, and new destinations.

### Safe defensive validation

- Seed synthetic canaries and confirm unauthorized response, error, log, metadata, and completion paths never return them.
- Exercise credential rotation and incident revocation with a test identity and verify old tokens stop working.

### Residual risk

- Authorized components necessarily handling plaintext remain high-value compromise targets.
- Previously emitted secrets require rotation even after the disclosure path is fixed.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-completion-leak"></a>

## `builtin/07/completion-leak` — completion: autocompletion enumerates secret values

**Risk:** high · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection, tool-execution

**System context:** completion: autocompletion enumerates secret values is a builtin training concept for completion. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Secrets or personal data can leak through prompts, errors, logs, completion APIs, metadata, tool chains, or over-broad responses.

### Assets

- API keys, tokens, credentials, and personal data
- System prompts and privileged configuration
- Logs, completions, model cards, and tool outputs

### Trust boundaries

- Secret store to application runtime
- Application or tool output to untrusted caller
- Sensitive telemetry or metadata to operators and models

### Threat actors and preconditions

- Actor: An unauthenticated or low-privilege caller
- Actor: A malicious tool, model input, or content source
- Precondition: Sensitive values are present in model-readable context, metadata, logs, or broad environment state
- Precondition: Response or tool policy does not minimize fields by caller and purpose

### High-level abuse paths

1. **Scenario:** A caller causes a response path to serialize sensitive context or metadata. **Impact:** Credentials or protected data leave their intended trust boundary.
2. **Scenario:** A tool or model with ambient access forwards data to an unauthorized destination. **Impact:** The leak enables impersonation or lateral movement.

### Secure before abuse

- Keep credentials outside prompts, model cards, logs, completions, and general environment state; fetch them just in time through a scoped broker.
- Apply response-field allowlists, data classification, tenant authorization, destination policy, and output minimization at the owning service.
- Use short-lived, audience-bound, least-privilege credentials with rotation and revocation.
- Redact sensitive fields before telemetry and prevent tool outputs from being treated as trusted instructions.

**Expected security outcome:** Sensitive values are absent from model-readable and public channels and are released only to authorized, purpose-bound consumers.

### Detection and response

- Deploy secret-pattern and canary detection at response, log, artifact, and egress boundaries with strict access controls.
- Alert on unusual secret reads, completion enumeration, debug-level changes, bulk exports, and new destinations.

### Safe defensive validation

- Seed synthetic canaries and confirm unauthorized response, error, log, metadata, and completion paths never return them.
- Exercise credential rotation and incident revocation with a test identity and verify old tokens stop working.

### Residual risk

- Authorized components necessarily handling plaintext remain high-value compromise targets.
- Previously emitted secrets require rotation even after the disclosure path is fixed.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-rug-pull"></a>

## `builtin/07/rug-pull` — tools: rug-pull -- tool behaviour changes after approval

**Risk:** high · **Confidence:** high · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** tools: rug-pull -- tool behaviour changes after approval is a builtin training concept for tools (rug-pull). The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** A malicious, shadowed, mutated, or intercepted tool can acquire trusted identity and steer the host toward unauthorized disclosure or effects.

### Assets

- Tool registry, definitions, and routing metadata
- Host approval and tool-selection integrity
- Credentials and side effects available to tools

### Trust boundaries

- Tool publisher or server to agent host
- Tool metadata and output to model context
- Selected tool to protected effect

### Threat actors and preconditions

- Actor: A malicious tool publisher or MCP server
- Actor: A compromised registry, proxy, or trusted tool
- Precondition: Tool identity or behavior can change after approval or collide with a trusted name
- Precondition: The host treats tool metadata or output as policy and grants ambient credentials

### High-level abuse paths

1. **Scenario:** A tool is approved under benign metadata and later changes behavior, identity, or instructions. **Impact:** Existing trust is reused for a malicious operation.
2. **Scenario:** A colliding or redirected tool is selected in place of the intended trusted implementation. **Impact:** Sensitive inputs or credentials reach an attacker-controlled component.

### Secure before abuse

- Bind approvals to a signed publisher identity and immutable digest of tool schema, description, endpoint, and version; require reapproval on change.
- Use server-qualified tool identifiers and deterministic routing; reject ambiguous names, redirects, and untrusted registry precedence.
- Treat descriptions and outputs as untrusted data, and authorize every effect against the originating identity in host code.
- Give each tool a narrow credential, destination allowlist, input schema, output limit, and isolated execution boundary.

**Expected security outcome:** Hosts execute only the exact approved tool identity and version, with least privilege and independent authorization at the effect boundary.

### Detection and response

- Alert on tool digest drift, registry changes, name collisions, endpoint redirection, reapproval bypass, and unusual tool sequences.
- Trace registry resolution, selected tool identity, input provenance, policy decision, and effect without logging secrets.

### Safe defensive validation

- Register inert colliding and changed tool definitions in a disposable registry and assert selection fails or requires explicit reapproval.
- Use a recording tool double to confirm untrusted metadata and output cannot authorize a protected effect.

### Residual risk

- A signed and approved publisher can still ship malicious logic within its granted scope.
- Semantic changes may evade schema-level comparison and require behavior review.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-command-injection"></a>

## `builtin/07/command-injection` — tools: command injection -> remote code execution

**Risk:** critical · **Confidence:** high · **Control families:** tool-execution, input-content, identity-access, logging-detection

**System context:** tools: command injection -> remote code execution is a builtin training concept for tools (rce). The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Unsafe interpretation of tool input can alter a command, query, template, document parser, or object graph and execute unauthorized operations.

### Assets

- Application process and runtime identity
- Database, template, XML, or command interpreter
- Host files, credentials, and downstream services

### Trust boundaries

- Untrusted tool argument to interpreter
- Application process to operating system or data engine
- Runtime identity to protected resources

### Threat actors and preconditions

- Actor: A caller controlling a tool parameter
- Actor: A prompt-influenced agent invoking an unsafe sink
- Precondition: Untrusted data is concatenated into an executable language or unsafe deserializer
- Precondition: The runtime identity has authority beyond the intended operation

### High-level abuse paths

1. **Scenario:** Attacker-controlled data crosses into an interpreter without parameterization or a safe grammar. **Impact:** The operation escapes its intended data context.
2. **Scenario:** The compromised component uses ambient filesystem, network, or credential access. **Impact:** Code execution or data access expands to the host or adjacent services.

### Secure before abuse

- Remove interpreter boundaries where possible; otherwise use parameterized APIs, fixed operations, strict schemas, and context-appropriate encoding.
- Disable dangerous parser and deserializer features, enforce type allowlists, and reject unexpected structures before processing.
- Run the operation in a non-root, read-only, capability-dropped sandbox with no unnecessary secrets or egress.
- Authorize the requested object and effect independently of model or tool input.

**Expected security outcome:** Untrusted values remain data, and any parser failure is contained by a least-privileged runtime boundary.

### Detection and response

- Record operation type, caller, validated object identifier, policy decision, and bounded failure category without sensitive payloads.
- Alert on parser errors, rejected metacharacter or structure patterns, unexpected child processes, and unusual outbound connections.

### Safe defensive validation

- Exercise inert boundary characters and malformed structures and assert they remain data or are rejected without side effects.
- Use a sandbox canary to confirm the runtime cannot create child processes, access unrelated files, or contact undeclared services.

### Residual risk

- Complex parsers and native dependencies can retain memory-safety or logic defects.
- A legitimate high-impact operation may still be abused by a compromised authorized identity.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-header-routing-confusion"></a>

## `builtin/07/header-routing-confusion` — 2026 routing: header/body policy desynchronization

**Risk:** high · **Confidence:** high · **Control families:** protocol-integrity, identity-access, network-boundaries, logging-detection

**System context:** 2026 routing: header/body policy desynchronization is a builtin training concept for streamable-http-routing. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Protocol parsing, origin, routing, or session inconsistencies can let a request pass one policy check and reach a different protected operation.

### Assets

- Protocol messages, headers, sessions, and routing decisions
- Authenticated peer and origin identity
- Protected methods and transport endpoints

### Trust boundaries

- Remote origin to protocol gateway
- Gateway-parsed metadata to application-parsed body
- Session identifier to authenticated principal

### Threat actors and preconditions

- Actor: A malicious web origin or protocol client
- Actor: A network intermediary able to alter routing metadata
- Precondition: Different layers authorize different representations of the same request
- Precondition: Origin, audience, session, or routing fields are missing, predictable, or weakly bound

### High-level abuse paths

1. **Scenario:** A gateway validates one method or identity while the application dispatches another representation. **Impact:** A protected method executes under an unrelated authorization decision.
2. **Scenario:** A session or cross-origin channel is accepted without strong binding and replay protection. **Impact:** An attacker attaches to or drives another principal’s session.

### Secure before abuse

- Canonicalize and parse each request once, then pass an immutable typed representation to both authorization and dispatch.
- Bind method, tool, peer, origin, audience, body, session, and protocol version in one policy decision.
- Use cryptographically random, rotated session identifiers with secure transport, expiry, and replay protection.
- Enforce explicit trusted origins and hosts; keep browser cross-origin policy narrow and deny credentialed wildcard behavior.

**Expected security outcome:** Authorization and dispatch use the same authenticated, canonical protocol representation and replay-safe session context.

### Detection and response

- Log canonical request identity, origin, peer, session, routed operation, and mismatch reason using privacy-safe identifiers.
- Alert on header/body disagreement, invalid origins, session collisions, replay, downgrade, and parser disagreement.

### Safe defensive validation

- Generate benign mismatched representations and assert authorization and dispatch always resolve to the same operation.
- Use synthetic origins and sessions to confirm wrong-origin, guessed, replayed, expired, and cross-user requests fail closed.

### Residual risk

- Reverse proxies and SDK upgrades can introduce new normalization differences.
- Compromised valid sessions retain their authorized reach until revocation.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-07-unicode-tool-poisoning"></a>

## `builtin/07/unicode-tool-poisoning` — tools: Unicode-concealed tool-description poisoning past the scanner

**Risk:** high · **Confidence:** high · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** tools: Unicode-concealed tool-description poisoning past the scanner is a builtin training concept for tools (concealment). The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** A malicious, shadowed, mutated, or intercepted tool can acquire trusted identity and steer the host toward unauthorized disclosure or effects.

### Assets

- Tool registry, definitions, and routing metadata
- Host approval and tool-selection integrity
- Credentials and side effects available to tools

### Trust boundaries

- Tool publisher or server to agent host
- Tool metadata and output to model context
- Selected tool to protected effect

### Threat actors and preconditions

- Actor: A malicious tool publisher or MCP server
- Actor: A compromised registry, proxy, or trusted tool
- Precondition: Tool identity or behavior can change after approval or collide with a trusted name
- Precondition: The host treats tool metadata or output as policy and grants ambient credentials

### High-level abuse paths

1. **Scenario:** A tool is approved under benign metadata and later changes behavior, identity, or instructions. **Impact:** Existing trust is reused for a malicious operation.
2. **Scenario:** A colliding or redirected tool is selected in place of the intended trusted implementation. **Impact:** Sensitive inputs or credentials reach an attacker-controlled component.

### Secure before abuse

- Bind approvals to a signed publisher identity and immutable digest of tool schema, description, endpoint, and version; require reapproval on change.
- Use server-qualified tool identifiers and deterministic routing; reject ambiguous names, redirects, and untrusted registry precedence.
- Treat descriptions and outputs as untrusted data, and authorize every effect against the originating identity in host code.
- Give each tool a narrow credential, destination allowlist, input schema, output limit, and isolated execution boundary.

**Expected security outcome:** Hosts execute only the exact approved tool identity and version, with least privilege and independent authorization at the effect boundary.

### Detection and response

- Alert on tool digest drift, registry changes, name collisions, endpoint redirection, reapproval bypass, and unusual tool sequences.
- Trace registry resolution, selected tool identity, input provenance, policy decision, and effect without logging secrets.

### Safe defensive validation

- Register inert colliding and changed tool definitions in a disposable registry and assert selection fails or requires explicit reapproval.
- Use a recording tool double to confirm untrusted metadata and output cannot authorize a protected effect.

### Residual risk

- A signed and approved publisher can still ship malicious logic within its granted scope.
- Semantic changes may evade schema-level comparison and require behavior review.

### Evidence and limitations

- `modules/07-mcp-tool-surfaces/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-08-malicious-weights"></a>

## `builtin/08/malicious-weights` — RCE via unsafe model deserialization

**Risk:** critical · **Confidence:** high · **Control families:** supply-chain, tool-execution, data-protection, logging-detection

**System context:** RCE via unsafe model deserialization is a builtin training concept for supply-weights. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** A poisoned, unsigned, unsafe, or ambiguously resolved dependency can alter model behavior, expose data, or execute code during build or load.

### Assets

- Models, adapters, datasets, packages, and build artifacts
- Training and deployment pipeline integrity
- Signing keys and artifact provenance

### Trust boundaries

- External publisher to artifact registry
- Registry artifact to build or model runtime
- Training data contributor to deployed behavior

### Threat actors and preconditions

- Actor: A malicious or compromised supplier
- Actor: An attacker publishing a colliding dependency or artifact
- Precondition: Artifacts are selected or loaded without verified identity, provenance, and safe format controls
- Precondition: Training or deployment accepts unreviewed behavior-changing inputs

### High-level abuse paths

1. **Scenario:** A higher-priority, colliding, or compromised artifact is selected as trusted input. **Impact:** Malicious logic or model behavior enters the release.
2. **Scenario:** An unsafe serialized artifact is interpreted with runtime privileges. **Impact:** Artifact loading becomes code execution with pipeline or service authority.

### Secure before abuse

- Pin dependencies and artifacts by trusted registry, publisher identity, version, and digest; verify signatures and provenance before use.
- Use non-executable formats and isolated conversion for untrusted model artifacts; never deserialize opaque objects in a privileged runtime.
- Apply review, lineage, anomaly analysis, and representative evaluation to datasets, adapters, and models before promotion.
- Separate build, registry, training, and serving identities; remove network and secret access from artifact inspection.

**Expected security outcome:** Only provenance-verified, safely parsed, reviewed artifacts can enter training, build, or serving environments.

### Detection and response

- Alert on publisher, registry, digest, dependency graph, dataset distribution, or model-behavior drift.
- Retain software and model bills of materials plus provenance so affected releases can be identified and revoked.

### Safe defensive validation

- Use signed synthetic artifacts and assert wrong registry, identity, digest, provenance, or format is rejected before loading.
- Run benign trigger and distribution-shift evaluations in an isolated promotion stage and verify rollback and revocation.

### Residual risk

- A legitimately signed maintainer can still publish malicious or compromised content.
- Behavioral backdoors may remain dormant outside the evaluation distribution.

### Evidence and limitations

- `modules/08-supply-chain/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-08-poisoned-dataset"></a>

## `builtin/08/poisoned-dataset` — Backdoor the model via dataset poisoning

**Risk:** medium · **Confidence:** high · **Control families:** supply-chain, tool-execution, data-protection, logging-detection

**System context:** Backdoor the model via dataset poisoning is a builtin training concept for supply-data. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** A poisoned, unsigned, unsafe, or ambiguously resolved dependency can alter model behavior, expose data, or execute code during build or load.

### Assets

- Models, adapters, datasets, packages, and build artifacts
- Training and deployment pipeline integrity
- Signing keys and artifact provenance

### Trust boundaries

- External publisher to artifact registry
- Registry artifact to build or model runtime
- Training data contributor to deployed behavior

### Threat actors and preconditions

- Actor: A malicious or compromised supplier
- Actor: An attacker publishing a colliding dependency or artifact
- Precondition: Artifacts are selected or loaded without verified identity, provenance, and safe format controls
- Precondition: Training or deployment accepts unreviewed behavior-changing inputs

### High-level abuse paths

1. **Scenario:** A higher-priority, colliding, or compromised artifact is selected as trusted input. **Impact:** Malicious logic or model behavior enters the release.
2. **Scenario:** An unsafe serialized artifact is interpreted with runtime privileges. **Impact:** Artifact loading becomes code execution with pipeline or service authority.

### Secure before abuse

- Pin dependencies and artifacts by trusted registry, publisher identity, version, and digest; verify signatures and provenance before use.
- Use non-executable formats and isolated conversion for untrusted model artifacts; never deserialize opaque objects in a privileged runtime.
- Apply review, lineage, anomaly analysis, and representative evaluation to datasets, adapters, and models before promotion.
- Separate build, registry, training, and serving identities; remove network and secret access from artifact inspection.

**Expected security outcome:** Only provenance-verified, safely parsed, reviewed artifacts can enter training, build, or serving environments.

### Detection and response

- Alert on publisher, registry, digest, dependency graph, dataset distribution, or model-behavior drift.
- Retain software and model bills of materials plus provenance so affected releases can be identified and revoked.

### Safe defensive validation

- Use signed synthetic artifacts and assert wrong registry, identity, digest, provenance, or format is rejected before loading.
- Run benign trigger and distribution-shift evaluations in an isolated promotion stage and verify rollback and revocation.

### Residual risk

- A legitimately signed maintainer can still publish malicious or compromised content.
- Behavioral backdoors may remain dormant outside the evaluation distribution.

### Evidence and limitations

- `modules/08-supply-chain/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-08-backdoored-adapter"></a>

## `builtin/08/backdoored-adapter` — Inject behaviour via a backdoored adapter

**Risk:** medium · **Confidence:** high · **Control families:** supply-chain, tool-execution, data-protection, logging-detection

**System context:** Inject behaviour via a backdoored adapter is a builtin training concept for supply-adapter. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** A poisoned, unsigned, unsafe, or ambiguously resolved dependency can alter model behavior, expose data, or execute code during build or load.

### Assets

- Models, adapters, datasets, packages, and build artifacts
- Training and deployment pipeline integrity
- Signing keys and artifact provenance

### Trust boundaries

- External publisher to artifact registry
- Registry artifact to build or model runtime
- Training data contributor to deployed behavior

### Threat actors and preconditions

- Actor: A malicious or compromised supplier
- Actor: An attacker publishing a colliding dependency or artifact
- Precondition: Artifacts are selected or loaded without verified identity, provenance, and safe format controls
- Precondition: Training or deployment accepts unreviewed behavior-changing inputs

### High-level abuse paths

1. **Scenario:** A higher-priority, colliding, or compromised artifact is selected as trusted input. **Impact:** Malicious logic or model behavior enters the release.
2. **Scenario:** An unsafe serialized artifact is interpreted with runtime privileges. **Impact:** Artifact loading becomes code execution with pipeline or service authority.

### Secure before abuse

- Pin dependencies and artifacts by trusted registry, publisher identity, version, and digest; verify signatures and provenance before use.
- Use non-executable formats and isolated conversion for untrusted model artifacts; never deserialize opaque objects in a privileged runtime.
- Apply review, lineage, anomaly analysis, and representative evaluation to datasets, adapters, and models before promotion.
- Separate build, registry, training, and serving identities; remove network and secret access from artifact inspection.

**Expected security outcome:** Only provenance-verified, safely parsed, reviewed artifacts can enter training, build, or serving environments.

### Detection and response

- Alert on publisher, registry, digest, dependency graph, dataset distribution, or model-behavior drift.
- Retain software and model bills of materials plus provenance so affected releases can be identified and revoked.

### Safe defensive validation

- Use signed synthetic artifacts and assert wrong registry, identity, digest, provenance, or format is rejected before loading.
- Run benign trigger and distribution-shift evaluations in an isolated promotion stage and verify rollback and revocation.

### Residual risk

- A legitimately signed maintainer can still publish malicious or compromised content.
- Behavioral backdoors may remain dormant outside the evaluation distribution.

### Evidence and limitations

- `modules/08-supply-chain/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-08-dependency-confusion"></a>

## `builtin/08/dependency-confusion` — Win dependency confusion

**Risk:** critical · **Confidence:** high · **Control families:** supply-chain, tool-execution, data-protection, logging-detection

**System context:** Win dependency confusion is a builtin training concept for supply-deps. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** A poisoned, unsigned, unsafe, or ambiguously resolved dependency can alter model behavior, expose data, or execute code during build or load.

### Assets

- Models, adapters, datasets, packages, and build artifacts
- Training and deployment pipeline integrity
- Signing keys and artifact provenance

### Trust boundaries

- External publisher to artifact registry
- Registry artifact to build or model runtime
- Training data contributor to deployed behavior

### Threat actors and preconditions

- Actor: A malicious or compromised supplier
- Actor: An attacker publishing a colliding dependency or artifact
- Precondition: Artifacts are selected or loaded without verified identity, provenance, and safe format controls
- Precondition: Training or deployment accepts unreviewed behavior-changing inputs

### High-level abuse paths

1. **Scenario:** A higher-priority, colliding, or compromised artifact is selected as trusted input. **Impact:** Malicious logic or model behavior enters the release.
2. **Scenario:** An unsafe serialized artifact is interpreted with runtime privileges. **Impact:** Artifact loading becomes code execution with pipeline or service authority.

### Secure before abuse

- Pin dependencies and artifacts by trusted registry, publisher identity, version, and digest; verify signatures and provenance before use.
- Use non-executable formats and isolated conversion for untrusted model artifacts; never deserialize opaque objects in a privileged runtime.
- Apply review, lineage, anomaly analysis, and representative evaluation to datasets, adapters, and models before promotion.
- Separate build, registry, training, and serving identities; remove network and secret access from artifact inspection.

**Expected security outcome:** Only provenance-verified, safely parsed, reviewed artifacts can enter training, build, or serving environments.

### Detection and response

- Alert on publisher, registry, digest, dependency graph, dataset distribution, or model-behavior drift.
- Retain software and model bills of materials plus provenance so affected releases can be identified and revoked.

### Safe defensive validation

- Use signed synthetic artifacts and assert wrong registry, identity, digest, provenance, or format is rejected before loading.
- Run benign trigger and distribution-shift evaluations in an isolated promotion stage and verify rollback and revocation.

### Residual risk

- A legitimately signed maintainer can still publish malicious or compromised content.
- Behavioral backdoors may remain dormant outside the evaluation distribution.

### Evidence and limitations

- `modules/08-supply-chain/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-09-metadata-ssrf"></a>

## `builtin/09/metadata-ssrf` — SSRF to cloud metadata -> steal role credentials

**Risk:** critical · **Confidence:** high · **Control families:** network-boundaries, identity-access, data-protection, logging-detection

**System context:** SSRF to cloud metadata -> steal role credentials is a builtin training concept for infra-ssrf. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** A server-side fetch capability can be redirected to metadata or internal services, exposing credentials and enabling lateral movement under the workload identity.

### Assets

- Cloud metadata and workload credentials
- Internal services and network topology
- Outbound request identity and response data

### Trust boundaries

- Untrusted URL input to server-side client
- Application network to metadata and internal services
- Fetched response to user or model context

### Threat actors and preconditions

- Actor: An unauthenticated or low-privilege caller
- Actor: A prompt-influenced agent controlling a fetch target
- Precondition: The service follows caller-controlled destinations or redirects
- Precondition: Network policy and workload identity permit access to sensitive internal endpoints

### High-level abuse paths

1. **Scenario:** A caller selects an internal or special-address destination through direct input, redirect, or name resolution. **Impact:** The service returns sensitive internal data.
2. **Scenario:** Stolen workload credentials are accepted by a second protected service. **Impact:** The compromise expands beyond the original application.

### Secure before abuse

- Use an allowlist of schemes, hosts, ports, and paths; resolve names once and reject loopback, link-local, private, and otherwise prohibited addresses.
- Revalidate every redirect and connect to the validated address while preserving the expected host and TLS identity.
- Block metadata and unnecessary east-west or internet egress at the network layer, and use short-lived audience-bound workload credentials.
- Limit response size, content type, timeout, and redirect count; never return raw credential-bearing responses.

**Expected security outcome:** Server-side requests reach only explicitly approved destinations and cannot use workload network position to retrieve internal credentials.

### Detection and response

- Log normalized destination class, resolved address, redirect chain, caller, and policy decision with credentials redacted.
- Alert on metadata ranges, unusual internal ports, DNS-answer changes, and bursts of failed destination validation.

### Safe defensive validation

- Use controlled loopback, private-address, redirect, and rebinding simulations and assert the request is rejected before connection.
- Confirm a synthetic workload identity cannot reach a canary internal service outside its declared dependency set.

### Residual risk

- Compromise of an allowlisted destination can turn it into a pivot.
- Proxy and resolver differences can create validation-to-connection inconsistencies.

### Evidence and limitations

- `modules/09-infra-deployment/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-09-open-inference-api"></a>

## `builtin/09/open-inference-api` — Abuse an unauthenticated admin inference route

**Risk:** high · **Confidence:** high · **Control families:** identity-access, protocol-integrity, logging-detection, human-approval

**System context:** Abuse an unauthenticated admin inference route is a builtin training concept for infra-api. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Missing object- and action-level authorization can let a caller or delegated agent access another tenant’s data or perform a privileged effect.

### Assets

- Protected objects and administrative operations
- User, agent, and service identities
- Delegation scopes and approval state

### Trust boundaries

- Caller identity to service authorization
- Agent or tool delegation to protected resource
- Object identifier to tenant ownership

### Threat actors and preconditions

- Actor: An authenticated low-privilege caller
- Actor: A confused deputy acting with ambient authority
- Precondition: The service trusts a caller-supplied object, role, scope, or audience
- Precondition: Authorization is checked only at an upstream agent rather than the owning service

### High-level abuse paths

1. **Scenario:** A valid identity substitutes an object identifier or action outside its grant. **Impact:** Protected data or operations cross a tenant or role boundary.
2. **Scenario:** A deputy receives a broad token and acts without preserving the originating principal and purpose. **Impact:** The caller gains the deputy’s ambient authority.

### Secure before abuse

- Authenticate at each service and authorize subject, tenant, object, action, purpose, and current state at the resource owner.
- Use short-lived audience-bound tokens and attenuated capabilities; never pass broad upstream credentials through to tools.
- Derive ownership and role from trusted server state rather than caller-controlled fields or model output.
- Require explicit, bound approval for high-impact actions and invalidate it when inputs, tool identity, or scope changes.

**Expected security outcome:** Every protected object and effect is authorized by its owning service for the originating principal and exact delegated scope.

### Detection and response

- Audit allow and deny decisions with subject, originating principal, audience, object, action, and policy version.
- Alert on cross-tenant identifiers, repeated denied objects, audience mismatch, and privileged actions from unusual delegation chains.

### Safe defensive validation

- Use synthetic users, tenants, roles, and audiences to confirm horizontal and vertical access attempts fail closed.
- Exercise a benign delegated workflow and assert the final service sees and enforces the original principal’s reduced scope.

### Residual risk

- Compromised authorized identities can act within their valid grants.
- Policy and identity-provider drift can temporarily create inconsistent decisions.

### Evidence and limitations

- `modules/09-infra-deployment/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-09-registry-secrets"></a>

## `builtin/09/registry-secrets` — Recover a secret from a model card

**Risk:** high · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection, tool-execution

**System context:** Recover a secret from a model card is a builtin training concept for infra-secrets. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Secrets or personal data can leak through prompts, errors, logs, completion APIs, metadata, tool chains, or over-broad responses.

### Assets

- API keys, tokens, credentials, and personal data
- System prompts and privileged configuration
- Logs, completions, model cards, and tool outputs

### Trust boundaries

- Secret store to application runtime
- Application or tool output to untrusted caller
- Sensitive telemetry or metadata to operators and models

### Threat actors and preconditions

- Actor: An unauthenticated or low-privilege caller
- Actor: A malicious tool, model input, or content source
- Precondition: Sensitive values are present in model-readable context, metadata, logs, or broad environment state
- Precondition: Response or tool policy does not minimize fields by caller and purpose

### High-level abuse paths

1. **Scenario:** A caller causes a response path to serialize sensitive context or metadata. **Impact:** Credentials or protected data leave their intended trust boundary.
2. **Scenario:** A tool or model with ambient access forwards data to an unauthorized destination. **Impact:** The leak enables impersonation or lateral movement.

### Secure before abuse

- Keep credentials outside prompts, model cards, logs, completions, and general environment state; fetch them just in time through a scoped broker.
- Apply response-field allowlists, data classification, tenant authorization, destination policy, and output minimization at the owning service.
- Use short-lived, audience-bound, least-privilege credentials with rotation and revocation.
- Redact sensitive fields before telemetry and prevent tool outputs from being treated as trusted instructions.

**Expected security outcome:** Sensitive values are absent from model-readable and public channels and are released only to authorized, purpose-bound consumers.

### Detection and response

- Deploy secret-pattern and canary detection at response, log, artifact, and egress boundaries with strict access controls.
- Alert on unusual secret reads, completion enumeration, debug-level changes, bulk exports, and new destinations.

### Safe defensive validation

- Seed synthetic canaries and confirm unauthorized response, error, log, metadata, and completion paths never return them.
- Exercise credential rotation and incident revocation with a test identity and verify old tokens stop working.

### Residual risk

- Authorized components necessarily handling plaintext remain high-value compromise targets.
- Previously emitted secrets require rotation even after the disclosure path is fixed.

### Evidence and limitations

- `modules/09-infra-deployment/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-10-asset-inventory"></a>

## `builtin/10/asset-inventory` — Inventory the high-value AI assets

**Risk:** medium · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection, human-approval

**System context:** Inventory the high-value AI assets is a builtin training concept for tm-assets. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** An incomplete or stale threat model can omit a high-value asset, trust boundary, or chained abuse path and leave the corresponding control unowned.

### Assets

- Complete AI asset and data-flow inventory
- Ownership and classification records
- Threat-model decisions and accepted risks

### Trust boundaries

- Engineering evidence to the threat model
- Untrusted inputs to AI processing
- AI services to tools and protected data

### Threat actors and preconditions

- Actor: A design reviewer working from incomplete evidence
- Actor: A system owner who overlooks a transitive dependency
- Precondition: The architecture inventory or data-flow map is incomplete
- Precondition: Risk decisions lack an accountable owner or validation evidence

### High-level abuse paths

1. **Scenario:** A component, identity, or data flow is absent from the inventory and receives no explicit protection. **Impact:** A material exposure persists because it is outside review and monitoring scope.
2. **Scenario:** Individual weaknesses are assessed in isolation and their combined authority is missed. **Impact:** A multi-stage compromise crosses several apparently low-risk boundaries.

### Secure before abuse

- Generate the asset and data-flow inventory from deployable configuration where possible, then require named owners to attest the result.
- Record identities, data classifications, tool effects, model inputs, external dependencies, and trust boundaries in one versioned model.
- Rank end-to-end abuse paths by impact and reachability, and link each treatment to an engineering control and test.
- Require security review when architecture, permissions, models, data sources, or external integrations change.

**Expected security outcome:** Material assets, authority crossings, and chained risks have explicit controls, owners, evidence, and review triggers before deployment.

### Detection and response

- Track threat-model age, unresolved risks, missing owners, and architecture changes that lack review.
- Escalate material drift between deployment manifests and documented boundaries.

### Safe defensive validation

- Compare a synthetic deployment inventory with the model and assert every service, identity, and data store is represented.
- Run a tabletop exercise using inert scenarios and confirm the documented boundaries and owners support containment.

### Residual risk

- Undocumented runtime behavior and third-party dependencies can still create unknown boundaries.
- A threat model can become stale between reviews without automated drift detection.

### Evidence and limitations

- `modules/10-threat-modeling/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-10-trust-boundaries"></a>

## `builtin/10/trust-boundaries` — Map trust boundaries & data flows

**Risk:** medium · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection, human-approval

**System context:** Map trust boundaries & data flows is a builtin training concept for tm-boundaries. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** An incomplete or stale threat model can omit a high-value asset, trust boundary, or chained abuse path and leave the corresponding control unowned.

### Assets

- Complete AI asset and data-flow inventory
- Ownership and classification records
- Threat-model decisions and accepted risks

### Trust boundaries

- Engineering evidence to the threat model
- Untrusted inputs to AI processing
- AI services to tools and protected data

### Threat actors and preconditions

- Actor: A design reviewer working from incomplete evidence
- Actor: A system owner who overlooks a transitive dependency
- Precondition: The architecture inventory or data-flow map is incomplete
- Precondition: Risk decisions lack an accountable owner or validation evidence

### High-level abuse paths

1. **Scenario:** A component, identity, or data flow is absent from the inventory and receives no explicit protection. **Impact:** A material exposure persists because it is outside review and monitoring scope.
2. **Scenario:** Individual weaknesses are assessed in isolation and their combined authority is missed. **Impact:** A multi-stage compromise crosses several apparently low-risk boundaries.

### Secure before abuse

- Generate the asset and data-flow inventory from deployable configuration where possible, then require named owners to attest the result.
- Record identities, data classifications, tool effects, model inputs, external dependencies, and trust boundaries in one versioned model.
- Rank end-to-end abuse paths by impact and reachability, and link each treatment to an engineering control and test.
- Require security review when architecture, permissions, models, data sources, or external integrations change.

**Expected security outcome:** Material assets, authority crossings, and chained risks have explicit controls, owners, evidence, and review triggers before deployment.

### Detection and response

- Track threat-model age, unresolved risks, missing owners, and architecture changes that lack review.
- Escalate material drift between deployment manifests and documented boundaries.

### Safe defensive validation

- Compare a synthetic deployment inventory with the model and assert every service, identity, and data store is represented.
- Run a tabletop exercise using inert scenarios and confirm the documented boundaries and owners support containment.

### Residual risk

- Undocumented runtime behavior and third-party dependencies can still create unknown boundaries.
- A threat model can become stale between reviews without automated drift detection.

### Evidence and limitations

- `modules/10-threat-modeling/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-10-attack-paths"></a>

## `builtin/10/attack-paths` — Enumerate end-to-end attack paths

**Risk:** medium · **Confidence:** high · **Control families:** data-protection, identity-access, logging-detection, human-approval

**System context:** Enumerate end-to-end attack paths is a builtin training concept for tm-paths. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** An incomplete or stale threat model can omit a high-value asset, trust boundary, or chained abuse path and leave the corresponding control unowned.

### Assets

- Complete AI asset and data-flow inventory
- Ownership and classification records
- Threat-model decisions and accepted risks

### Trust boundaries

- Engineering evidence to the threat model
- Untrusted inputs to AI processing
- AI services to tools and protected data

### Threat actors and preconditions

- Actor: A design reviewer working from incomplete evidence
- Actor: A system owner who overlooks a transitive dependency
- Precondition: The architecture inventory or data-flow map is incomplete
- Precondition: Risk decisions lack an accountable owner or validation evidence

### High-level abuse paths

1. **Scenario:** A component, identity, or data flow is absent from the inventory and receives no explicit protection. **Impact:** A material exposure persists because it is outside review and monitoring scope.
2. **Scenario:** Individual weaknesses are assessed in isolation and their combined authority is missed. **Impact:** A multi-stage compromise crosses several apparently low-risk boundaries.

### Secure before abuse

- Generate the asset and data-flow inventory from deployable configuration where possible, then require named owners to attest the result.
- Record identities, data classifications, tool effects, model inputs, external dependencies, and trust boundaries in one versioned model.
- Rank end-to-end abuse paths by impact and reachability, and link each treatment to an engineering control and test.
- Require security review when architecture, permissions, models, data sources, or external integrations change.

**Expected security outcome:** Material assets, authority crossings, and chained risks have explicit controls, owners, evidence, and review triggers before deployment.

### Detection and response

- Track threat-model age, unresolved risks, missing owners, and architecture changes that lack review.
- Escalate material drift between deployment manifests and documented boundaries.

### Safe defensive validation

- Compare a synthetic deployment inventory with the model and assert every service, identity, and data store is represented.
- Run a tabletop exercise using inert scenarios and confirm the documented boundaries and owners support containment.

### Residual risk

- Undocumented runtime behavior and third-party dependencies can still create unknown boundaries.
- A threat model can become stale between reviews without automated drift detection.

### Evidence and limitations

- `modules/10-threat-modeling/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-11-initial-access"></a>

## `builtin/11/initial-access` — Initial access via indirect injection

**Risk:** critical · **Confidence:** high · **Control families:** input-content, tool-execution, identity-access, network-boundaries

**System context:** Initial access via indirect injection is a builtin training concept for chain-access. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Prompt, identity, tool, and network weaknesses can compose into an end-to-end path from untrusted input to protected data and external impact.

### Assets

- End-to-end agent workflow and user intent
- Internal vaults, tools, credentials, and delegated access
- Containment and incident-response boundaries

### Trust boundaries

- Untrusted content to agent context
- Agent authority to internal tool or service
- Protected result to external destination

### Threat actors and preconditions

- Actor: An external actor controlling indirect content
- Actor: A compromised agent, tool, or trusted data source
- Precondition: Several individually permissive boundaries compose into an unreviewed path
- Precondition: The agent holds ambient authority and can externalize protected results

### High-level abuse paths

1. **Scenario:** Untrusted content steers an agent to use an internal capability under ambient authority. **Impact:** The attacker reaches a protected object indirectly.
2. **Scenario:** The protected result is passed through another tool or output channel without purpose and destination checks. **Impact:** Sensitive data leaves the trusted environment.

### Secure before abuse

- Model the complete path from every untrusted input to every high-impact effect and break it with independent controls at multiple boundaries.
- Propagate the originating principal and content provenance; authorize object, action, purpose, and destination at each service.
- Remove ambient credentials, use attenuated short-lived capabilities, and require human approval for high-impact or novel multi-step plans.
- Constrain east-west and outbound network paths and apply data-loss controls at the final egress boundary.

**Expected security outcome:** No single model, content, identity, tool, or network failure can complete a path from untrusted input to protected impact.

### Detection and response

- Correlate content ingestion, agent planning, tool calls, internal access, approvals, and egress in one trace.
- Alert on unusual cross-service sequences, sensitive-object reads followed by outbound actions, and privilege changes within a workflow.

### Safe defensive validation

- Run an inert end-to-end scenario with recording doubles and confirm at least two independent controls stop the protected effect.
- Tabletop containment of a synthetic compromised agent and verify credential revocation, session termination, and evidence preservation.

### Residual risk

- Authorized multi-step workflows can resemble abuse and require contextual monitoring.
- Unknown dependencies may introduce alternate paths outside the documented graph.

### Evidence and limitations

- `modules/11-capstone/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-11-pivot-vault"></a>

## `builtin/11/pivot-vault` — Pivot through ambient authority to the vault

**Risk:** critical · **Confidence:** high · **Control families:** input-content, tool-execution, identity-access, network-boundaries

**System context:** Pivot through ambient authority to the vault is a builtin training concept for chain-pivot. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Prompt, identity, tool, and network weaknesses can compose into an end-to-end path from untrusted input to protected data and external impact.

### Assets

- End-to-end agent workflow and user intent
- Internal vaults, tools, credentials, and delegated access
- Containment and incident-response boundaries

### Trust boundaries

- Untrusted content to agent context
- Agent authority to internal tool or service
- Protected result to external destination

### Threat actors and preconditions

- Actor: An external actor controlling indirect content
- Actor: A compromised agent, tool, or trusted data source
- Precondition: Several individually permissive boundaries compose into an unreviewed path
- Precondition: The agent holds ambient authority and can externalize protected results

### High-level abuse paths

1. **Scenario:** Untrusted content steers an agent to use an internal capability under ambient authority. **Impact:** The attacker reaches a protected object indirectly.
2. **Scenario:** The protected result is passed through another tool or output channel without purpose and destination checks. **Impact:** Sensitive data leaves the trusted environment.

### Secure before abuse

- Model the complete path from every untrusted input to every high-impact effect and break it with independent controls at multiple boundaries.
- Propagate the originating principal and content provenance; authorize object, action, purpose, and destination at each service.
- Remove ambient credentials, use attenuated short-lived capabilities, and require human approval for high-impact or novel multi-step plans.
- Constrain east-west and outbound network paths and apply data-loss controls at the final egress boundary.

**Expected security outcome:** No single model, content, identity, tool, or network failure can complete a path from untrusted input to protected impact.

### Detection and response

- Correlate content ingestion, agent planning, tool calls, internal access, approvals, and egress in one trace.
- Alert on unusual cross-service sequences, sensitive-object reads followed by outbound actions, and privilege changes within a workflow.

### Safe defensive validation

- Run an inert end-to-end scenario with recording doubles and confirm at least two independent controls stop the protected effect.
- Tabletop containment of a synthetic compromised agent and verify credential revocation, session termination, and evidence preservation.

### Residual risk

- Authorized multi-step workflows can resemble abuse and require contextual monitoring.
- Unknown dependencies may introduce alternate paths outside the documented graph.

### Evidence and limitations

- `modules/11-capstone/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.

<a id="builtin-11-exfil-crown-jewel"></a>

## `builtin/11/exfil-crown-jewel` — Exfiltrate the crown-jewel secret

**Risk:** critical · **Confidence:** high · **Control families:** input-content, tool-execution, identity-access, network-boundaries

**System context:** Exfiltrate the crown-jewel secret is a builtin training concept for chain-exfil. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

**Primary risk:** Prompt, identity, tool, and network weaknesses can compose into an end-to-end path from untrusted input to protected data and external impact.

### Assets

- End-to-end agent workflow and user intent
- Internal vaults, tools, credentials, and delegated access
- Containment and incident-response boundaries

### Trust boundaries

- Untrusted content to agent context
- Agent authority to internal tool or service
- Protected result to external destination

### Threat actors and preconditions

- Actor: An external actor controlling indirect content
- Actor: A compromised agent, tool, or trusted data source
- Precondition: Several individually permissive boundaries compose into an unreviewed path
- Precondition: The agent holds ambient authority and can externalize protected results

### High-level abuse paths

1. **Scenario:** Untrusted content steers an agent to use an internal capability under ambient authority. **Impact:** The attacker reaches a protected object indirectly.
2. **Scenario:** The protected result is passed through another tool or output channel without purpose and destination checks. **Impact:** Sensitive data leaves the trusted environment.

### Secure before abuse

- Model the complete path from every untrusted input to every high-impact effect and break it with independent controls at multiple boundaries.
- Propagate the originating principal and content provenance; authorize object, action, purpose, and destination at each service.
- Remove ambient credentials, use attenuated short-lived capabilities, and require human approval for high-impact or novel multi-step plans.
- Constrain east-west and outbound network paths and apply data-loss controls at the final egress boundary.

**Expected security outcome:** No single model, content, identity, tool, or network failure can complete a path from untrusted input to protected impact.

### Detection and response

- Correlate content ingestion, agent planning, tool calls, internal access, approvals, and egress in one trace.
- Alert on unusual cross-service sequences, sensitive-object reads followed by outbound actions, and privilege changes within a workflow.

### Safe defensive validation

- Run an inert end-to-end scenario with recording doubles and confirm at least two independent controls stop the protected effect.
- Tabletop containment of a synthetic compromised agent and verify credential revocation, session termination, and evidence preservation.

### Residual risk

- Authorized multi-step workflows can resemble abuse and require contextual monitoring.
- Unknown dependencies may introduce alternate paths outside the documented graph.

### Evidence and limitations

- `modules/11-capstone/module.yaml` — Defines this challenge identity, objective, target topology, and declared verification or adapter metadata.
- `SECURITY.md` — Defines the repository isolation model, deliberately vulnerable status, and known runtime safety limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The model describes the production-safe pattern; this teaching target intentionally omits controls so the weakness remains observable.

**Runtime status:** not verified—outside the current scope.
