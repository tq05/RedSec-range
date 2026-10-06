# `appsecco-mcp` defensive threat models

> Generated with `Codex-GPT-6-static-review` at reasoning effort `high` from repository commit `67491bee35bf6f3e38da47a094725714eafab2dd`. Human review is required.

**Ownership:** Appsecco · **Concepts:** 9 · **Declared variants:** 9

Runtime exploitability is **not verified—outside the current scope**. These are defensive design
reviews derived from curated repository metadata; no target, solution, or exploit was run.

<a id="appsecco-mcp-filesystem-workspace-actions"></a>

## `appsecco-mcp/filesystem-workspace-actions` — Filesystem Workspace Actions

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, data-protection, identity-access, logging-detection

**System context:** Filesystem Workspace Actions is a appsecco-mcp training concept for Path traversal / code execution. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="appsecco-mcp-indirect-prompt-injection"></a>

## `appsecco-mcp/indirect-prompt-injection` — Indirect Prompt Injection (stdio)

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Indirect Prompt Injection (stdio) is a appsecco-mcp training concept for Prompt/Context. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="appsecco-mcp-indirect-prompt-injection-remote"></a>

## `appsecco-mcp/indirect-prompt-injection-remote` — Indirect Prompt Injection (HTTP+SSE)

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Indirect Prompt Injection (HTTP+SSE) is a appsecco-mcp training concept for Prompt/Context. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="appsecco-mcp-malicious-code-exec"></a>

## `appsecco-mcp/malicious-code-exec` — Malicious Code Execution

**Risk:** critical · **Confidence:** medium · **Control families:** tool-execution, input-content, identity-access, logging-detection

**System context:** Malicious Code Execution is a appsecco-mcp training concept for Injection sink. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="appsecco-mcp-malicious-tools"></a>

## `appsecco-mcp/malicious-tools` — Malicious Tools

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Malicious Tools is a appsecco-mcp training concept for Tool output poisoning. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="appsecco-mcp-namespace-typosquatting"></a>

## `appsecco-mcp/namespace-typosquatting` — Namespace Typosquatting

**Risk:** critical · **Confidence:** medium · **Control families:** supply-chain, tool-execution, data-protection, logging-detection

**System context:** Namespace Typosquatting is a appsecco-mcp training concept for Supply chain. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="appsecco-mcp-outdated-packages"></a>

## `appsecco-mcp/outdated-packages` — Outdated Packages

**Risk:** critical · **Confidence:** medium · **Control families:** supply-chain, tool-execution, data-protection, logging-detection

**System context:** Outdated Packages is a appsecco-mcp training concept for Supply chain. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="appsecco-mcp-secrets-pii"></a>

## `appsecco-mcp/secrets-pii` — Secrets and PII Exposure

**Risk:** high · **Confidence:** medium · **Control families:** data-protection, identity-access, logging-detection, tool-execution

**System context:** Secrets and PII Exposure is a appsecco-mcp training concept for Secrets/Exposure. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="appsecco-mcp-wikipedia-streamable"></a>

## `appsecco-mcp/wikipedia-streamable` — Wikipedia (Streamable HTTP)

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Wikipedia (Streamable HTTP) is a appsecco-mcp training concept for Remote content injection. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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
