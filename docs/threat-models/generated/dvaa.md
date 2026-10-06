# `dvaa` defensive threat models

> Generated with `Codex-GPT-6-static-review` at reasoning effort `high` from repository commit `67491bee35bf6f3e38da47a094725714eafab2dd`. Human review is required.

**Ownership:** OpenA2A · **Concepts:** 22 · **Declared variants:** 22

Runtime exploitability is **not verified—outside the current scope**. These are defensive design
reviews derived from curated repository metadata; no target, solution, or exploit was run.

<a id="dvaa-l1-01"></a>

## `dvaa/L1-01` — Extract the System Prompt

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Extract the System Prompt is a dvaa training concept for data-exfiltration. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l1-02"></a>

## `dvaa/L1-02` — API Key Leak

**Risk:** high · **Confidence:** medium · **Control families:** data-protection, identity-access, logging-detection, tool-execution

**System context:** API Key Leak is a dvaa training concept for data-exfiltration. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l1-03"></a>

## `dvaa/L1-03` — Basic Prompt Injection

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Basic Prompt Injection is a dvaa training concept for prompt-injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-01"></a>

## `dvaa/L2-01` — Jailbreak via Roleplay

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Jailbreak via Roleplay is a dvaa training concept for jailbreak. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-02"></a>

## `dvaa/L2-02` — Context Window Manipulation

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Context Window Manipulation is a dvaa training concept for context-manipulation. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-03"></a>

## `dvaa/L2-03` — MCP Path Traversal

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, data-protection, identity-access, logging-detection

**System context:** MCP Path Traversal is a dvaa training concept for mcp-exploitation. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-04"></a>

## `dvaa/L2-04` — Persistent Memory Injection

**Risk:** high · **Confidence:** medium · **Control families:** input-content, data-protection, identity-access, logging-detection

**System context:** Persistent Memory Injection is a dvaa training concept for memory-injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-05"></a>

## `dvaa/L2-05` — Memory Credential Extraction

**Risk:** high · **Confidence:** medium · **Control families:** input-content, data-protection, identity-access, logging-detection

**System context:** Memory Credential Extraction is a dvaa training concept for memory-injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-06"></a>

## `dvaa/L2-06` — Context Padding Attack

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Context Padding Attack is a dvaa training concept for context-overflow. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-07"></a>

## `dvaa/L2-07` — Safety Instruction Displacement

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Safety Instruction Displacement is a dvaa training concept for context-overflow. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-08"></a>

## `dvaa/L2-08` — Malicious Tool Registration

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Malicious Tool Registration is a dvaa training concept for tool-registry-poisoning. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l2-09"></a>

## `dvaa/L2-09` — Tool Call MITM

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Tool Call MITM is a dvaa training concept for tool-mitm. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l3-01"></a>

## `dvaa/L3-01` — Chained Prompt Injection

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Chained Prompt Injection is a dvaa training concept for prompt-injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l3-02"></a>

## `dvaa/L3-02` — SSRF via MCP

**Risk:** critical · **Confidence:** medium · **Control families:** network-boundaries, identity-access, data-protection, logging-detection

**System context:** SSRF via MCP is a dvaa training concept for mcp-exploitation. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l3-03"></a>

## `dvaa/L3-03` — Self-Replicating Memory Entry

**Risk:** high · **Confidence:** medium · **Control families:** input-content, data-protection, identity-access, logging-detection

**System context:** Self-Replicating Memory Entry is a dvaa training concept for memory-injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l3-04"></a>

## `dvaa/L3-04` — System Prompt Extraction via Context Pressure

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** System Prompt Extraction via Context Pressure is a dvaa training concept for context-overflow. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l3-05"></a>

## `dvaa/L3-05` — Tool Typosquatting

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Tool Typosquatting is a dvaa training concept for tool-registry-poisoning. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l3-06"></a>

## `dvaa/L3-06` — Tool Chain Data Exfiltration

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Tool Chain Data Exfiltration is a dvaa training concept for tool-registry-poisoning. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l3-07"></a>

## `dvaa/L3-07` — Tool Shadowing

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Tool Shadowing is a dvaa training concept for tool-mitm. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l3-08"></a>

## `dvaa/L3-08` — Traffic Redirection Attack

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Traffic Redirection Attack is a dvaa training concept for tool-mitm. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l4-01"></a>

## `dvaa/L4-01` — Compromise SecureBot

**Risk:** critical · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, network-boundaries

**System context:** Compromise SecureBot is a dvaa training concept for mixed. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvaa-l4-02"></a>

## `dvaa/L4-02` — Agent-to-Agent Attack Chain

**Risk:** high · **Confidence:** medium · **Control families:** identity-access, protocol-integrity, tool-execution, logging-detection

**System context:** Agent-to-Agent Attack Chain is a dvaa training concept for agent-to-agent. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.
