# `dvmcp` defensive threat models

> Generated with `Codex-GPT-6-static-review` at reasoning effort `high` from repository commit `67491bee35bf6f3e38da47a094725714eafab2dd`. Human review is required.

**Ownership:** Harish Santhanalakshmi Ganesan · **Concepts:** 10 · **Declared variants:** 10

Runtime exploitability is **not verified—outside the current scope**. These are defensive design
reviews derived from curated repository metadata; no target, solution, or exploit was run.

<a id="dvmcp-01"></a>

## `dvmcp/01` — Basic Prompt Injection

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Basic Prompt Injection is a dvmcp training concept for Prompt/Context. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="dvmcp-02"></a>

## `dvmcp/02` — Tool Poisoning

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Tool Poisoning is a dvmcp training concept for MCP-specific. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="dvmcp-03"></a>

## `dvmcp/03` — Excessive Permission Scope

**Risk:** high · **Confidence:** medium · **Control families:** identity-access, protocol-integrity, logging-detection, human-approval

**System context:** Excessive Permission Scope is a dvmcp training concept for AuthN/AuthZ. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

- `ranges/catalog.yaml` — Defines the pinned upstream source, challenge identity, adapter, ports, and ownership boundary.
- `docs/external-ranges.md` — Defines external-container isolation, gateway behavior, update policy, and adapter assurance limits.
- Limitation: Static design review only; runtime exploitability is not verified—outside the current scope.
- Limitation: The pinned upstream implementation is not present in this repository, so implementation-specific controls require upstream verification.

**Runtime status:** not verified—outside the current scope.

<a id="dvmcp-04"></a>

## `dvmcp/04` — Rug Pull Attack

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Rug Pull Attack is a dvmcp training concept for MCP-specific. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="dvmcp-05"></a>

## `dvmcp/05` — Tool Shadowing

**Risk:** high · **Confidence:** medium · **Control families:** tool-execution, protocol-integrity, identity-access, supply-chain

**System context:** Tool Shadowing is a dvmcp training concept for MCP-specific. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="dvmcp-06"></a>

## `dvmcp/06` — Indirect Prompt Injection

**Risk:** high · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, logging-detection

**System context:** Indirect Prompt Injection is a dvmcp training concept for Prompt/Context. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="dvmcp-07"></a>

## `dvmcp/07` — Token Theft

**Risk:** high · **Confidence:** medium · **Control families:** data-protection, identity-access, logging-detection, tool-execution

**System context:** Token Theft is a dvmcp training concept for Secrets/Exposure. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="dvmcp-08"></a>

## `dvmcp/08` — Malicious Code Execution

**Risk:** critical · **Confidence:** medium · **Control families:** tool-execution, input-content, identity-access, logging-detection

**System context:** Malicious Code Execution is a dvmcp training concept for Injection sink. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="dvmcp-09"></a>

## `dvmcp/09` — Remote Access Control

**Risk:** critical · **Confidence:** medium · **Control families:** tool-execution, input-content, identity-access, logging-detection

**System context:** Remote Access Control is a dvmcp training concept for Injection sink. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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

<a id="dvmcp-10"></a>

## `dvmcp/10` — Multi-Vector Attack

**Risk:** critical · **Confidence:** medium · **Control families:** input-content, tool-execution, identity-access, network-boundaries

**System context:** Multi-Vector Attack is a dvmcp training concept for Attack chain. The defensive model assumes deployment inside the private, isolated range topology described by the catalog.

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
