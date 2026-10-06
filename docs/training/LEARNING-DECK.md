<!-- kind: challenge -->
<!-- key: builtin/01/first-contact -->
<!-- range: builtin -->
<!-- pair: 1/110 -->
<!-- pattern: prompt -->
# First contact -- coax the orientation flag out of the Guide
> builtin · 01/first-contact · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models first contact -- coax the orientation flag out of the guide, focusing on its direct-injection trust boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: builtin/01/first-contact -->
<!-- range: builtin -->
<!-- pair: 1/110 -->
<!-- pattern: prompt -->
# Resolution · First contact -- coax the orientation flag out of the Guide
> Defensive resolution and review gotchas for builtin · 01/first-contact
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/02/fingerprint-model -->
<!-- range: builtin -->
<!-- pair: 2/110 -->
<!-- pattern: recon -->
# Fingerprint the backing model/provider
> builtin · 02/fingerprint-model · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models fingerprint the backing model/provider, focusing on its recon trust boundary.
- **BOUNDARY:** Model, provider, route, error, and capability details cross from internal configuration to an external caller.
- **REVIEW:** Which metadata is necessary for this caller? Can errors, banners, schemas, or undocumented routes reveal additional capability?
- **LEARN:** Discovery surfaces should disclose only what an authenticated user needs for an authorised workflow.

---

<!-- kind: resolution -->
<!-- key: builtin/02/fingerprint-model -->
<!-- range: builtin -->
<!-- pair: 2/110 -->
<!-- pattern: recon -->
# Resolution · Fingerprint the backing model/provider
> Defensive resolution and review gotchas for builtin · 02/fingerprint-model
- **CONTROL:** Minimise banners and errors, authenticate discovery endpoints, inventory routes and schemas, and rate-limit enumeration.
- **VALIDATE:** Compare permitted and unauthorised synthetic clients and assert that only the documented minimum metadata is returned.
- **GOTCHA:** Removing a route from user documentation does not make the reachable endpoint private.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/02/enumerate-surfaces -->
<!-- range: builtin -->
<!-- pair: 3/110 -->
<!-- pattern: recon -->
# Discover an undocumented internal endpoint
> builtin · 02/enumerate-surfaces · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models discover an undocumented internal endpoint, focusing on its recon trust boundary.
- **BOUNDARY:** Model, provider, route, error, and capability details cross from internal configuration to an external caller.
- **REVIEW:** Which metadata is necessary for this caller? Can errors, banners, schemas, or undocumented routes reveal additional capability?
- **LEARN:** Discovery surfaces should disclose only what an authenticated user needs for an authorised workflow.

---

<!-- kind: resolution -->
<!-- key: builtin/02/enumerate-surfaces -->
<!-- range: builtin -->
<!-- pair: 3/110 -->
<!-- pattern: recon -->
# Resolution · Discover an undocumented internal endpoint
> Defensive resolution and review gotchas for builtin · 02/enumerate-surfaces
- **CONTROL:** Minimise banners and errors, authenticate discovery endpoints, inventory routes and schemas, and rate-limit enumeration.
- **VALIDATE:** Compare permitted and unauthorised synthetic clients and assert that only the documented minimum metadata is returned.
- **GOTCHA:** Removing a route from user documentation does not make the reachable endpoint private.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/02/leak-config -->
<!-- range: builtin -->
<!-- pair: 4/110 -->
<!-- pattern: recon -->
# Dump service config via a verbose error
> builtin · 02/leak-config · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models dump service config via a verbose error, focusing on its recon trust boundary.
- **BOUNDARY:** Model, provider, route, error, and capability details cross from internal configuration to an external caller.
- **REVIEW:** Which metadata is necessary for this caller? Can errors, banners, schemas, or undocumented routes reveal additional capability?
- **LEARN:** Discovery surfaces should disclose only what an authenticated user needs for an authorised workflow.

---

<!-- kind: resolution -->
<!-- key: builtin/02/leak-config -->
<!-- range: builtin -->
<!-- pair: 4/110 -->
<!-- pattern: recon -->
# Resolution · Dump service config via a verbose error
> Defensive resolution and review gotchas for builtin · 02/leak-config
- **CONTROL:** Minimise banners and errors, authenticate discovery endpoints, inventory routes and schemas, and rate-limit enumeration.
- **VALIDATE:** Compare permitted and unauthorised synthetic clients and assert that only the documented minimum metadata is returned.
- **GOTCHA:** Removing a route from user documentation does not make the reachable endpoint private.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/03/sys-prompt-leak -->
<!-- range: builtin -->
<!-- pair: 5/110 -->
<!-- pattern: prompt -->
# Direct prompt injection -> leak the system prompt
> builtin · 03/sys-prompt-leak · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models direct prompt injection -> leak the system prompt, focusing on its direct-injection trust boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: builtin/03/sys-prompt-leak -->
<!-- range: builtin -->
<!-- pair: 5/110 -->
<!-- pattern: prompt -->
# Resolution · Direct prompt injection -> leak the system prompt
> Defensive resolution and review gotchas for builtin · 03/sys-prompt-leak
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/03/indirect-injection -->
<!-- range: builtin -->
<!-- pair: 6/110 -->
<!-- pattern: prompt -->
# Indirect prompt injection via auto-retrieved notes
> builtin · 03/indirect-injection · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models indirect prompt injection via auto-retrieved notes, focusing on its indirect-injection trust boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: builtin/03/indirect-injection -->
<!-- range: builtin -->
<!-- pair: 6/110 -->
<!-- pattern: prompt -->
# Resolution · Indirect prompt injection via auto-retrieved notes
> Defensive resolution and review gotchas for builtin · 03/indirect-injection
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/03/tool-exfil -->
<!-- range: builtin -->
<!-- pair: 7/110 -->
<!-- pattern: agency -->
# Excessive agency -> exfiltrate the mail API key
> builtin · 03/tool-exfil · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models excessive agency -> exfiltrate the mail api key, focusing on its tool-abuse trust boundary.
- **BOUNDARY:** A model-selected action crosses into a tool or service that has real authority and external effects.
- **REVIEW:** Which principal authorises the effect? Can model-controlled arguments exceed the intended task or data scope?
- **LEARN:** Tool availability is not action authorisation; the system that owns the effect must enforce policy for each call.

---

<!-- kind: resolution -->
<!-- key: builtin/03/tool-exfil -->
<!-- range: builtin -->
<!-- pair: 7/110 -->
<!-- pattern: agency -->
# Resolution · Excessive agency -> exfiltrate the mail API key
> Defensive resolution and review gotchas for builtin · 03/tool-exfil
- **CONTROL:** Use narrow tools, per-action authorisation, allow-listed arguments, minimal credentials, confirmation for sensitive effects, and audit logs.
- **VALIDATE:** Exercise permitted and denied actions with synthetic accounts and assert enforcement at the tool or service boundary.
- **GOTCHA:** A model refusal or tool description cannot contain authority that the downstream service fails to enforce.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/03/memory-poisoning -->
<!-- range: builtin -->
<!-- pair: 8/110 -->
<!-- pattern: prompt -->
# Memory poisoning -> persistence across turns
> builtin · 03/memory-poisoning · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models memory poisoning -> persistence across turns, focusing on its memory trust boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: builtin/03/memory-poisoning -->
<!-- range: builtin -->
<!-- pair: 8/110 -->
<!-- pattern: prompt -->
# Resolution · Memory poisoning -> persistence across turns
> Defensive resolution and review gotchas for builtin · 03/memory-poisoning
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/04/trust-exploitation -->
<!-- range: builtin -->
<!-- pair: 9/110 -->
<!-- pattern: identity -->
# Transitive trust -> reviewer acts on your ticket
> builtin · 04/trust-exploitation · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models transitive trust -> reviewer acts on your ticket, focusing on its a2a-trust trust boundary.
- **BOUNDARY:** A principal, object, task, or delegated action crosses an identity and authorisation boundary.
- **REVIEW:** Which principal is authenticated? Is the object and delegated action authorised for that principal?
- **LEARN:** Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.

---

<!-- kind: resolution -->
<!-- key: builtin/04/trust-exploitation -->
<!-- range: builtin -->
<!-- pair: 9/110 -->
<!-- pattern: identity -->
# Resolution · Transitive trust -> reviewer acts on your ticket
> Defensive resolution and review gotchas for builtin · 04/trust-exploitation
- **CONTROL:** Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.
- **VALIDATE:** Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.
- **GOTCHA:** A valid sender or token does not automatically authorise every downstream object or action.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/04/message-manipulation -->
<!-- range: builtin -->
<!-- pair: 10/110 -->
<!-- pattern: identity -->
# Send an unsigned A2A JSON-RPC message
> builtin · 04/message-manipulation · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models send an unsigned a2a json-rpc message, focusing on its a2a-message/send trust boundary.
- **BOUNDARY:** A principal, object, task, or delegated action crosses an identity and authorisation boundary.
- **REVIEW:** Which principal is authenticated? Is the object and delegated action authorised for that principal?
- **LEARN:** Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.

---

<!-- kind: resolution -->
<!-- key: builtin/04/message-manipulation -->
<!-- range: builtin -->
<!-- pair: 10/110 -->
<!-- pattern: identity -->
# Resolution · Send an unsigned A2A JSON-RPC message
> Defensive resolution and review gotchas for builtin · 04/message-manipulation
- **CONTROL:** Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.
- **VALIDATE:** Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.
- **GOTCHA:** A valid sender or token does not automatically authorise every downstream object or action.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/04/agent-impersonation -->
<!-- range: builtin -->
<!-- pair: 11/110 -->
<!-- pattern: identity -->
# Impersonate a trusted approver
> builtin · 04/agent-impersonation · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models impersonate a trusted approver, focusing on its a2a-message-identity trust boundary.
- **BOUNDARY:** A principal, object, task, or delegated action crosses an identity and authorisation boundary.
- **REVIEW:** Which principal is authenticated? Is the object and delegated action authorised for that principal?
- **LEARN:** Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.

---

<!-- kind: resolution -->
<!-- key: builtin/04/agent-impersonation -->
<!-- range: builtin -->
<!-- pair: 11/110 -->
<!-- pattern: identity -->
# Resolution · Impersonate a trusted approver
> Defensive resolution and review gotchas for builtin · 04/agent-impersonation
- **CONTROL:** Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.
- **VALIDATE:** Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.
- **GOTCHA:** A valid sender or token does not automatically authorise every downstream object or action.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/04/session-smuggling -->
<!-- range: builtin -->
<!-- pair: 12/110 -->
<!-- pattern: session-context -->
# Agent session smuggling across a stateful A2A session
> builtin · 04/session-smuggling · impossible · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models agent session smuggling across a stateful a2a session, focusing on its a2a-context trust boundary.
- **BOUNDARY:** Conversation state and delegated authority cross message, task, and session boundaries over time.
- **REVIEW:** Who owns the context and each message? Can replay, reordering, or partial validation change the cumulative meaning?
- **LEARN:** Every message must be authenticated and authorised in the context of the accumulated session state.

---

<!-- kind: resolution -->
<!-- key: builtin/04/session-smuggling -->
<!-- range: builtin -->
<!-- pair: 12/110 -->
<!-- pattern: session-context -->
# Resolution · Agent session smuggling across a stateful A2A session
> Defensive resolution and review gotchas for builtin · 04/session-smuggling
- **CONTROL:** Bind context identifiers to authenticated principals, authorise every transition, validate cumulative state, and expire replayable state.
- **VALIDATE:** Use harmless cross-user, replayed, split, and out-of-order messages to confirm the state machine rejects invalid transitions.
- **GOTCHA:** Validating each message in isolation can miss a prohibited meaning assembled across several messages.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/05/knowledge-poisoning -->
<!-- range: builtin -->
<!-- pair: 13/110 -->
<!-- pattern: rag -->
# Poison the knowledge base
> builtin · 05/knowledge-poisoning · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models poison the knowledge base, focusing on its rag-source trust boundary.
- **BOUNDARY:** Indexed content, similarity scores, or derived vectors cross from a data store into a trusted answer.
- **REVIEW:** Who can add or rank content? What can similarity, provenance, or output precision disclose?
- **LEARN:** Relevance is not trust; retrieval, provenance, privacy, and instruction handling are separate decisions.

---

<!-- kind: resolution -->
<!-- key: builtin/05/knowledge-poisoning -->
<!-- range: builtin -->
<!-- pair: 13/110 -->
<!-- pattern: rag -->
# Resolution · Poison the knowledge base
> Defensive resolution and review gotchas for builtin · 05/knowledge-poisoning
- **CONTROL:** Control ingestion, preserve provenance, isolate instructions from retrieved data, minimise precision, and authorise the corpus.
- **VALIDATE:** Use synthetic documents and records to test ranking, provenance display, tenant isolation, and privacy thresholds.
- **GOTCHA:** A high similarity score or authoritative-looking citation does not establish integrity or permission.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/05/retrieval-manipulation -->
<!-- range: builtin -->
<!-- pair: 14/110 -->
<!-- pattern: rag -->
# Out-rank the real documents for a victim query
> builtin · 05/retrieval-manipulation · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models out-rank the real documents for a victim query, focusing on its rag-retrieval trust boundary.
- **BOUNDARY:** Indexed content, similarity scores, or derived vectors cross from a data store into a trusted answer.
- **REVIEW:** Who can add or rank content? What can similarity, provenance, or output precision disclose?
- **LEARN:** Relevance is not trust; retrieval, provenance, privacy, and instruction handling are separate decisions.

---

<!-- kind: resolution -->
<!-- key: builtin/05/retrieval-manipulation -->
<!-- range: builtin -->
<!-- pair: 14/110 -->
<!-- pattern: rag -->
# Resolution · Out-rank the real documents for a victim query
> Defensive resolution and review gotchas for builtin · 05/retrieval-manipulation
- **CONTROL:** Control ingestion, preserve provenance, isolate instructions from retrieved data, minimise precision, and authorise the corpus.
- **VALIDATE:** Use synthetic documents and records to test ranking, provenance display, tenant isolation, and privacy thresholds.
- **GOTCHA:** A high similarity score or authoritative-looking citation does not establish integrity or permission.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/05/citation-spoofing -->
<!-- range: builtin -->
<!-- pair: 15/110 -->
<!-- pattern: rag -->
# Spoof a trusted citation
> builtin · 05/citation-spoofing · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models spoof a trusted citation, focusing on its rag-trust trust boundary.
- **BOUNDARY:** Indexed content, similarity scores, or derived vectors cross from a data store into a trusted answer.
- **REVIEW:** Who can add or rank content? What can similarity, provenance, or output precision disclose?
- **LEARN:** Relevance is not trust; retrieval, provenance, privacy, and instruction handling are separate decisions.

---

<!-- kind: resolution -->
<!-- key: builtin/05/citation-spoofing -->
<!-- range: builtin -->
<!-- pair: 15/110 -->
<!-- pattern: rag -->
# Resolution · Spoof a trusted citation
> Defensive resolution and review gotchas for builtin · 05/citation-spoofing
- **CONTROL:** Control ingestion, preserve provenance, isolate instructions from retrieved data, minimise precision, and authorise the corpus.
- **VALIDATE:** Use synthetic documents and records to test ranking, provenance display, tenant isolation, and privacy thresholds.
- **GOTCHA:** A high similarity score or authoritative-looking citation does not establish integrity or permission.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/06/embedding-inversion -->
<!-- range: builtin -->
<!-- pair: 16/110 -->
<!-- pattern: embeddings -->
# Reconstruct source text with a reference corpus
> builtin · 06/embedding-inversion · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models reconstruct source text with a reference corpus, focusing on its embedding-inversion trust boundary.
- **BOUNDARY:** Derived vectors and similarity decisions cross privacy, tenant, and policy boundaries.
- **REVIEW:** Who may query the vectors and at what precision? Can outputs reveal membership, reconstruct content, or bypass a text-only policy?
- **LEARN:** Embeddings can retain information about source records and should not serve as identity or authorisation controls.

---

<!-- kind: resolution -->
<!-- key: builtin/06/embedding-inversion -->
<!-- range: builtin -->
<!-- pair: 16/110 -->
<!-- pattern: embeddings -->
# Resolution · Reconstruct source text with a reference corpus
> Defensive resolution and review gotchas for builtin · 06/embedding-inversion
- **CONTROL:** Authorise vector access, isolate tenants, minimise returned precision, rate-limit queries, and enforce policy on canonical source data.
- **VALIDATE:** Use synthetic canary records to measure leakage and verify that similarity cannot replace exact policy checks.
- **GOTCHA:** A derived representation is not automatically anonymous, and semantic similarity is not an access-control decision.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/06/membership-inference -->
<!-- range: builtin -->
<!-- pair: 17/110 -->
<!-- pattern: embeddings -->
# Confirm a record is present in the store
> builtin · 06/membership-inference · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models confirm a record is present in the store, focusing on its embedding-mia trust boundary.
- **BOUNDARY:** Derived vectors and similarity decisions cross privacy, tenant, and policy boundaries.
- **REVIEW:** Who may query the vectors and at what precision? Can outputs reveal membership, reconstruct content, or bypass a text-only policy?
- **LEARN:** Embeddings can retain information about source records and should not serve as identity or authorisation controls.

---

<!-- kind: resolution -->
<!-- key: builtin/06/membership-inference -->
<!-- range: builtin -->
<!-- pair: 17/110 -->
<!-- pattern: embeddings -->
# Resolution · Confirm a record is present in the store
> Defensive resolution and review gotchas for builtin · 06/membership-inference
- **CONTROL:** Authorise vector access, isolate tenants, minimise returned precision, rate-limit queries, and enforce policy on canonical source data.
- **VALIDATE:** Use synthetic canary records to measure leakage and verify that similarity cannot replace exact policy checks.
- **GOTCHA:** A derived representation is not automatically anonymous, and semantic similarity is not an access-control decision.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/06/embedding-collision -->
<!-- range: builtin -->
<!-- pair: 18/110 -->
<!-- pattern: embeddings -->
# Bypass a text check via an embedding collision
> builtin · 06/embedding-collision · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models bypass a text check via an embedding collision, focusing on its embedding-collision trust boundary.
- **BOUNDARY:** Derived vectors and similarity decisions cross privacy, tenant, and policy boundaries.
- **REVIEW:** Who may query the vectors and at what precision? Can outputs reveal membership, reconstruct content, or bypass a text-only policy?
- **LEARN:** Embeddings can retain information about source records and should not serve as identity or authorisation controls.

---

<!-- kind: resolution -->
<!-- key: builtin/06/embedding-collision -->
<!-- range: builtin -->
<!-- pair: 18/110 -->
<!-- pattern: embeddings -->
# Resolution · Bypass a text check via an embedding collision
> Defensive resolution and review gotchas for builtin · 06/embedding-collision
- **CONTROL:** Authorise vector access, isolate tenants, minimise returned precision, rate-limit queries, and enforce policy on canonical source data.
- **VALIDATE:** Use synthetic canary records to measure leakage and verify that similarity cannot replace exact policy checks.
- **GOTCHA:** A derived representation is not automatically anonymous, and semantic similarity is not an access-control decision.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/tool-poisoning -->
<!-- range: builtin -->
<!-- pair: 19/110 -->
<!-- pattern: mcp -->
# tools: tool-description poisoning hijacks the host
> builtin · 07/tool-poisoning · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models tools: tool-description poisoning hijacks the host, focusing on its tools trust boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: builtin/07/tool-poisoning -->
<!-- range: builtin -->
<!-- pair: 19/110 -->
<!-- pattern: mcp -->
# Resolution · tools: tool-description poisoning hijacks the host
> Defensive resolution and review gotchas for builtin · 07/tool-poisoning
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/resource-traversal -->
<!-- range: builtin -->
<!-- pair: 20/110 -->
<!-- pattern: sink -->
# resources: path traversal in resources/read
> builtin · 07/resource-traversal · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models resources: path traversal in resources/read, focusing on its resources trust boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: builtin/07/resource-traversal -->
<!-- range: builtin -->
<!-- pair: 20/110 -->
<!-- pattern: sink -->
# Resolution · resources: path traversal in resources/read
> Defensive resolution and review gotchas for builtin · 07/resource-traversal
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/prompt-injection -->
<!-- range: builtin -->
<!-- pair: 21/110 -->
<!-- pattern: prompt -->
# prompts: argument injection discloses a privileged template block
> builtin · 07/prompt-injection · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models prompts: argument injection discloses a privileged template block, focusing on its prompts trust boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: builtin/07/prompt-injection -->
<!-- range: builtin -->
<!-- pair: 21/110 -->
<!-- pattern: prompt -->
# Resolution · prompts: argument injection discloses a privileged template block
> Defensive resolution and review gotchas for builtin · 07/prompt-injection
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/sampling-abuse -->
<!-- range: builtin -->
<!-- pair: 22/110 -->
<!-- pattern: mcp -->
# sampling: server-initiated sampling exfiltrates host context
> builtin · 07/sampling-abuse · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models sampling: server-initiated sampling exfiltrates host context, focusing on its sampling trust boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: builtin/07/sampling-abuse -->
<!-- range: builtin -->
<!-- pair: 22/110 -->
<!-- pattern: mcp -->
# Resolution · sampling: server-initiated sampling exfiltrates host context
> Defensive resolution and review gotchas for builtin · 07/sampling-abuse
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/roots-bypass -->
<!-- range: builtin -->
<!-- pair: 23/110 -->
<!-- pattern: scope -->
# roots: declared client roots are not enforced
> builtin · 07/roots-bypass · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models roots: declared client roots are not enforced, focusing on its roots trust boundary.
- **BOUNDARY:** A client-declared root, permission, or resource scope crosses into server-side access control.
- **REVIEW:** Who defines and enforces the allowed scope? Is the resource canonicalised before containment and permission checks?
- **LEARN:** Servers must enforce the intersection of declared scope, authenticated identity, and canonical resource location.

---

<!-- kind: resolution -->
<!-- key: builtin/07/roots-bypass -->
<!-- range: builtin -->
<!-- pair: 23/110 -->
<!-- pattern: scope -->
# Resolution · roots: declared client roots are not enforced
> Defensive resolution and review gotchas for builtin · 07/roots-bypass
- **CONTROL:** Enforce scopes server-side, canonicalise resource identifiers, deny ambient access, and apply least privilege to the host process.
- **VALIDATE:** Use synthetic in-scope and out-of-scope resources, including encoded and absolute forms, to confirm containment fails closed.
- **GOTCHA:** Advertising a root or permission to the model does not enforce it at the filesystem or service boundary.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/elicitation-phishing -->
<!-- range: builtin -->
<!-- pair: 24/110 -->
<!-- pattern: mcp -->
# elicitation: server elicits credentials the host auto-answers
> builtin · 07/elicitation-phishing · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models elicitation: server elicits credentials the host auto-answers, focusing on its elicitation trust boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: builtin/07/elicitation-phishing -->
<!-- range: builtin -->
<!-- pair: 24/110 -->
<!-- pattern: mcp -->
# Resolution · elicitation: server elicits credentials the host auto-answers
> Defensive resolution and review gotchas for builtin · 07/elicitation-phishing
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/logging-leak -->
<!-- range: builtin -->
<!-- pair: 25/110 -->
<!-- pattern: secrets -->
# logging: debug log notifications leak a session token
> builtin · 07/logging-leak · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models logging: debug log notifications leak a session token, focusing on its logging trust boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: builtin/07/logging-leak -->
<!-- range: builtin -->
<!-- pair: 25/110 -->
<!-- pattern: secrets -->
# Resolution · logging: debug log notifications leak a session token
> Defensive resolution and review gotchas for builtin · 07/logging-leak
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/completion-leak -->
<!-- range: builtin -->
<!-- pair: 26/110 -->
<!-- pattern: secrets -->
# completion: autocompletion enumerates secret values
> builtin · 07/completion-leak · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models completion: autocompletion enumerates secret values, focusing on its completion trust boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: builtin/07/completion-leak -->
<!-- range: builtin -->
<!-- pair: 26/110 -->
<!-- pattern: secrets -->
# Resolution · completion: autocompletion enumerates secret values
> Defensive resolution and review gotchas for builtin · 07/completion-leak
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/rug-pull -->
<!-- range: builtin -->
<!-- pair: 27/110 -->
<!-- pattern: mcp -->
# tools: rug-pull -- tool behaviour changes after approval
> builtin · 07/rug-pull · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models tools: rug-pull -- tool behaviour changes after approval, focusing on its tools (rug-pull) trust boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: builtin/07/rug-pull -->
<!-- range: builtin -->
<!-- pair: 27/110 -->
<!-- pattern: mcp -->
# Resolution · tools: rug-pull -- tool behaviour changes after approval
> Defensive resolution and review gotchas for builtin · 07/rug-pull
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/command-injection -->
<!-- range: builtin -->
<!-- pair: 28/110 -->
<!-- pattern: sink -->
# tools: command injection -> remote code execution
> builtin · 07/command-injection · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models tools: command injection -> remote code execution, focusing on its tools (rce) trust boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: builtin/07/command-injection -->
<!-- range: builtin -->
<!-- pair: 28/110 -->
<!-- pattern: sink -->
# Resolution · tools: command injection -> remote code execution
> Defensive resolution and review gotchas for builtin · 07/command-injection
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/header-routing-confusion -->
<!-- range: builtin -->
<!-- pair: 29/110 -->
<!-- pattern: transport -->
# 2026 routing: header/body policy desynchronization
> builtin · 07/header-routing-confusion · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models 2026 routing: header/body policy desynchronization, focusing on its streamable-http-routing trust boundary.
- **BOUNDARY:** Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.
- **REVIEW:** Which layer decides request meaning? Are origin, audience, version, and session identifiers bound exactly?
- **LEARN:** Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.

---

<!-- kind: resolution -->
<!-- key: builtin/07/header-routing-confusion -->
<!-- range: builtin -->
<!-- pair: 29/110 -->
<!-- pattern: transport -->
# Resolution · 2026 routing: header/body policy desynchronization
> Defensive resolution and review gotchas for builtin · 07/header-routing-confusion
- **CONTROL:** Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.
- **VALIDATE:** Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.
- **GOTCHA:** A gateway and application can each appear correct while authorising different interpretations of one request.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/unicode-tool-poisoning -->
<!-- range: builtin -->
<!-- pair: 30/110 -->
<!-- pattern: mcp -->
# tools: Unicode-concealed tool-description poisoning past the scanner
> builtin · 07/unicode-tool-poisoning · impossible · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models tools: unicode-concealed tool-description poisoning past the scanner, focusing on its tools (concealment) trust boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: builtin/07/unicode-tool-poisoning -->
<!-- range: builtin -->
<!-- pair: 30/110 -->
<!-- pattern: mcp -->
# Resolution · tools: Unicode-concealed tool-description poisoning past the scanner
> Defensive resolution and review gotchas for builtin · 07/unicode-tool-poisoning
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/08/malicious-weights -->
<!-- range: builtin -->
<!-- pair: 31/110 -->
<!-- pattern: supply -->
# RCE via unsafe model deserialization
> builtin · 08/malicious-weights · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models rce via unsafe model deserialization, focusing on its supply-weights trust boundary.
- **BOUNDARY:** A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.
- **REVIEW:** What identity and digest bind the artifact? Where is it loaded, merged, trained, or resolved?
- **LEARN:** AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.

---

<!-- kind: resolution -->
<!-- key: builtin/08/malicious-weights -->
<!-- range: builtin -->
<!-- pair: 31/110 -->
<!-- pattern: supply -->
# Resolution · RCE via unsafe model deserialization
> Defensive resolution and review gotchas for builtin · 08/malicious-weights
- **CONTROL:** Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.
- **VALIDATE:** Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.
- **GOTCHA:** A familiar filename, package name, or model label is not proof of origin or safe behavior.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/08/poisoned-dataset -->
<!-- range: builtin -->
<!-- pair: 32/110 -->
<!-- pattern: supply -->
# Backdoor the model via dataset poisoning
> builtin · 08/poisoned-dataset · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models backdoor the model via dataset poisoning, focusing on its supply-data trust boundary.
- **BOUNDARY:** A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.
- **REVIEW:** What identity and digest bind the artifact? Where is it loaded, merged, trained, or resolved?
- **LEARN:** AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.

---

<!-- kind: resolution -->
<!-- key: builtin/08/poisoned-dataset -->
<!-- range: builtin -->
<!-- pair: 32/110 -->
<!-- pattern: supply -->
# Resolution · Backdoor the model via dataset poisoning
> Defensive resolution and review gotchas for builtin · 08/poisoned-dataset
- **CONTROL:** Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.
- **VALIDATE:** Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.
- **GOTCHA:** A familiar filename, package name, or model label is not proof of origin or safe behavior.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/08/backdoored-adapter -->
<!-- range: builtin -->
<!-- pair: 33/110 -->
<!-- pattern: supply -->
# Inject behaviour via a backdoored adapter
> builtin · 08/backdoored-adapter · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models inject behaviour via a backdoored adapter, focusing on its supply-adapter trust boundary.
- **BOUNDARY:** A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.
- **REVIEW:** What identity and digest bind the artifact? Where is it loaded, merged, trained, or resolved?
- **LEARN:** AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.

---

<!-- kind: resolution -->
<!-- key: builtin/08/backdoored-adapter -->
<!-- range: builtin -->
<!-- pair: 33/110 -->
<!-- pattern: supply -->
# Resolution · Inject behaviour via a backdoored adapter
> Defensive resolution and review gotchas for builtin · 08/backdoored-adapter
- **CONTROL:** Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.
- **VALIDATE:** Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.
- **GOTCHA:** A familiar filename, package name, or model label is not proof of origin or safe behavior.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/08/dependency-confusion -->
<!-- range: builtin -->
<!-- pair: 34/110 -->
<!-- pattern: supply -->
# Win dependency confusion
> builtin · 08/dependency-confusion · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models win dependency confusion, focusing on its supply-deps trust boundary.
- **BOUNDARY:** A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.
- **REVIEW:** What identity and digest bind the artifact? Where is it loaded, merged, trained, or resolved?
- **LEARN:** AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.

---

<!-- kind: resolution -->
<!-- key: builtin/08/dependency-confusion -->
<!-- range: builtin -->
<!-- pair: 34/110 -->
<!-- pattern: supply -->
# Resolution · Win dependency confusion
> Defensive resolution and review gotchas for builtin · 08/dependency-confusion
- **CONTROL:** Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.
- **VALIDATE:** Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.
- **GOTCHA:** A familiar filename, package name, or model label is not proof of origin or safe behavior.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/09/metadata-ssrf -->
<!-- range: builtin -->
<!-- pair: 35/110 -->
<!-- pattern: infra -->
# SSRF to cloud metadata -> steal role credentials
> builtin · 09/metadata-ssrf · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models ssrf to cloud metadata -> steal role credentials, focusing on its infra-ssrf trust boundary.
- **BOUNDARY:** A model-facing workload crosses into cloud metadata, administrative APIs, registries, or network destinations.
- **REVIEW:** Which destinations can the workload reach? Which administrative or registry actions require authentication?
- **LEARN:** Workload identity and egress are authority boundaries; model-facing services should carry minimal ambient privilege.

---

<!-- kind: resolution -->
<!-- key: builtin/09/metadata-ssrf -->
<!-- range: builtin -->
<!-- pair: 35/110 -->
<!-- pattern: infra -->
# Resolution · SSRF to cloud metadata -> steal role credentials
> Defensive resolution and review gotchas for builtin · 09/metadata-ssrf
- **CONTROL:** Default-deny egress, use workload identity, require admin authentication, isolate metadata, and keep secrets out of artifacts.
- **VALIDATE:** Review policy and use inert internal endpoints to confirm blocked destinations and authenticated administration.
- **GOTCHA:** Application input validation cannot compensate for broad network reach and over-privileged workload credentials.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/09/open-inference-api -->
<!-- range: builtin -->
<!-- pair: 36/110 -->
<!-- pattern: infra -->
# Abuse an unauthenticated admin inference route
> builtin · 09/open-inference-api · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models abuse an unauthenticated admin inference route, focusing on its infra-api trust boundary.
- **BOUNDARY:** A model-facing workload crosses into cloud metadata, administrative APIs, registries, or network destinations.
- **REVIEW:** Which destinations can the workload reach? Which administrative or registry actions require authentication?
- **LEARN:** Workload identity and egress are authority boundaries; model-facing services should carry minimal ambient privilege.

---

<!-- kind: resolution -->
<!-- key: builtin/09/open-inference-api -->
<!-- range: builtin -->
<!-- pair: 36/110 -->
<!-- pattern: infra -->
# Resolution · Abuse an unauthenticated admin inference route
> Defensive resolution and review gotchas for builtin · 09/open-inference-api
- **CONTROL:** Default-deny egress, use workload identity, require admin authentication, isolate metadata, and keep secrets out of artifacts.
- **VALIDATE:** Review policy and use inert internal endpoints to confirm blocked destinations and authenticated administration.
- **GOTCHA:** Application input validation cannot compensate for broad network reach and over-privileged workload credentials.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/09/registry-secrets -->
<!-- range: builtin -->
<!-- pair: 37/110 -->
<!-- pattern: secrets -->
# Recover a secret from a model card
> builtin · 09/registry-secrets · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models recover a secret from a model card, focusing on its infra-secrets trust boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: builtin/09/registry-secrets -->
<!-- range: builtin -->
<!-- pair: 37/110 -->
<!-- pattern: secrets -->
# Resolution · Recover a secret from a model card
> Defensive resolution and review gotchas for builtin · 09/registry-secrets
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/10/asset-inventory -->
<!-- range: builtin -->
<!-- pair: 38/110 -->
<!-- pattern: threat -->
# Inventory the high-value AI assets
> builtin · 10/asset-inventory · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models inventory the high-value ai assets, focusing on its tm-assets trust boundary.
- **BOUNDARY:** Assets, principals, data flows, and effects cross one or more explicitly modelled trust boundaries.
- **REVIEW:** Which asset and principal are involved? What ordered path connects entry, privilege, action, and impact?
- **LEARN:** A useful threat model explains relationships and complete paths rather than listing security keywords.

---

<!-- kind: resolution -->
<!-- key: builtin/10/asset-inventory -->
<!-- range: builtin -->
<!-- pair: 38/110 -->
<!-- pattern: threat -->
# Resolution · Inventory the high-value AI assets
> Defensive resolution and review gotchas for builtin · 10/asset-inventory
- **CONTROL:** Record assets, trust boundaries, data flows, assumptions, ranked paths, owners, and controls tied to each boundary.
- **VALIDATE:** Review models for concrete actors and ordered relationships; reject disconnected keyword inventories.
- **GOTCHA:** A complete list of terms can still omit the relationship that makes a scenario possible.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in artifact verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/10/trust-boundaries -->
<!-- range: builtin -->
<!-- pair: 39/110 -->
<!-- pattern: threat -->
# Map trust boundaries & data flows
> builtin · 10/trust-boundaries · medium · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models map trust boundaries & data flows, focusing on its tm-boundaries trust boundary.
- **BOUNDARY:** Assets, principals, data flows, and effects cross one or more explicitly modelled trust boundaries.
- **REVIEW:** Which asset and principal are involved? What ordered path connects entry, privilege, action, and impact?
- **LEARN:** A useful threat model explains relationships and complete paths rather than listing security keywords.

---

<!-- kind: resolution -->
<!-- key: builtin/10/trust-boundaries -->
<!-- range: builtin -->
<!-- pair: 39/110 -->
<!-- pattern: threat -->
# Resolution · Map trust boundaries & data flows
> Defensive resolution and review gotchas for builtin · 10/trust-boundaries
- **CONTROL:** Record assets, trust boundaries, data flows, assumptions, ranked paths, owners, and controls tied to each boundary.
- **VALIDATE:** Review models for concrete actors and ordered relationships; reject disconnected keyword inventories.
- **GOTCHA:** A complete list of terms can still omit the relationship that makes a scenario possible.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in artifact verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/10/attack-paths -->
<!-- range: builtin -->
<!-- pair: 40/110 -->
<!-- pattern: threat -->
# Enumerate end-to-end attack paths
> builtin · 10/attack-paths · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models enumerate end-to-end attack paths, focusing on its tm-paths trust boundary.
- **BOUNDARY:** Assets, principals, data flows, and effects cross one or more explicitly modelled trust boundaries.
- **REVIEW:** Which asset and principal are involved? What ordered path connects entry, privilege, action, and impact?
- **LEARN:** A useful threat model explains relationships and complete paths rather than listing security keywords.

---

<!-- kind: resolution -->
<!-- key: builtin/10/attack-paths -->
<!-- range: builtin -->
<!-- pair: 40/110 -->
<!-- pattern: threat -->
# Resolution · Enumerate end-to-end attack paths
> Defensive resolution and review gotchas for builtin · 10/attack-paths
- **CONTROL:** Record assets, trust boundaries, data flows, assumptions, ranked paths, owners, and controls tied to each boundary.
- **VALIDATE:** Review models for concrete actors and ordered relationships; reject disconnected keyword inventories.
- **GOTCHA:** A complete list of terms can still omit the relationship that makes a scenario possible.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in artifact verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/11/initial-access -->
<!-- range: builtin -->
<!-- pair: 41/110 -->
<!-- pattern: chain -->
# Initial access via indirect injection
> builtin · 11/initial-access · easy · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models initial access via indirect injection, focusing on its chain-access trust boundary.
- **BOUNDARY:** Several individually limited weaknesses compose across content, identity, tools, data, and infrastructure.
- **REVIEW:** Which earlier weakness enables the next step? Which control breaks the chain earliest and most reliably?
- **LEARN:** Security review must follow end-to-end authority and data flow because local controls can fail in composition.

---

<!-- kind: resolution -->
<!-- key: builtin/11/initial-access -->
<!-- range: builtin -->
<!-- pair: 41/110 -->
<!-- pattern: chain -->
# Resolution · Initial access via indirect injection
> Defensive resolution and review gotchas for builtin · 11/initial-access
- **CONTROL:** Use layered controls, trace provenance, minimise ambient authority, segment systems, and retain cross-service evidence.
- **VALIDATE:** Validate each boundary independently with safe fixtures, then review the composed data flow without executing an attack chain.
- **GOTCHA:** A control may stop one step while leaving another route to the same privileged effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/11/pivot-vault -->
<!-- range: builtin -->
<!-- pair: 42/110 -->
<!-- pattern: chain -->
# Pivot through ambient authority to the vault
> builtin · 11/pivot-vault · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models pivot through ambient authority to the vault, focusing on its chain-pivot trust boundary.
- **BOUNDARY:** Several individually limited weaknesses compose across content, identity, tools, data, and infrastructure.
- **REVIEW:** Which earlier weakness enables the next step? Which control breaks the chain earliest and most reliably?
- **LEARN:** Security review must follow end-to-end authority and data flow because local controls can fail in composition.

---

<!-- kind: resolution -->
<!-- key: builtin/11/pivot-vault -->
<!-- range: builtin -->
<!-- pair: 42/110 -->
<!-- pattern: chain -->
# Resolution · Pivot through ambient authority to the vault
> Defensive resolution and review gotchas for builtin · 11/pivot-vault
- **CONTROL:** Use layered controls, trace provenance, minimise ambient authority, segment systems, and retain cross-service evidence.
- **VALIDATE:** Validate each boundary independently with safe fixtures, then review the composed data flow without executing an attack chain.
- **GOTCHA:** A control may stop one step while leaving another route to the same privileged effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/11/exfil-crown-jewel -->
<!-- range: builtin -->
<!-- pair: 43/110 -->
<!-- pattern: chain -->
# Exfiltrate the crown-jewel secret
> builtin · 11/exfil-crown-jewel · hard · 1 variant(s)
- **DESCRIPTION:** Review how the built-in challenge models exfiltrate the crown-jewel secret, focusing on its chain-exfil trust boundary.
- **BOUNDARY:** Several individually limited weaknesses compose across content, identity, tools, data, and infrastructure.
- **REVIEW:** Which earlier weakness enables the next step? Which control breaks the chain earliest and most reliably?
- **LEARN:** Security review must follow end-to-end authority and data flow because local controls can fail in composition.

---

<!-- kind: resolution -->
<!-- key: builtin/11/exfil-crown-jewel -->
<!-- range: builtin -->
<!-- pair: 43/110 -->
<!-- pattern: chain -->
# Resolution · Exfiltrate the crown-jewel secret
> Defensive resolution and review gotchas for builtin · 11/exfil-crown-jewel
- **CONTROL:** Use layered controls, trace provenance, minimise ambient authority, segment systems, and retain cross-service evidence.
- **VALIDATE:** Validate each boundary independently with safe fixtures, then review the composed data flow without executing an attack chain.
- **GOTCHA:** A control may stop one step while leaving another route to the same privileged effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: dvaa/L1-01 -->
<!-- range: dvaa -->
<!-- pair: 44/110 -->
<!-- pattern: secrets -->
# Extract the System Prompt
> dvaa · L1-01 · easy · 1 variant(s)
- **DESCRIPTION:** Review the Extract the System Prompt scenario as implemented by OpenA2A, focusing on its data-exfiltration boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: dvaa/L1-01 -->
<!-- range: dvaa -->
<!-- pair: 44/110 -->
<!-- pattern: secrets -->
# Resolution · Extract the System Prompt
> Defensive resolution and review gotchas for dvaa · L1-01
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L1-02 -->
<!-- range: dvaa -->
<!-- pair: 45/110 -->
<!-- pattern: secrets -->
# API Key Leak
> dvaa · L1-02 · easy · 1 variant(s)
- **DESCRIPTION:** Review the API Key Leak scenario as implemented by OpenA2A, focusing on its data-exfiltration boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: dvaa/L1-02 -->
<!-- range: dvaa -->
<!-- pair: 45/110 -->
<!-- pattern: secrets -->
# Resolution · API Key Leak
> Defensive resolution and review gotchas for dvaa · L1-02
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L1-03 -->
<!-- range: dvaa -->
<!-- pair: 46/110 -->
<!-- pattern: prompt -->
# Basic Prompt Injection
> dvaa · L1-03 · easy · 1 variant(s)
- **DESCRIPTION:** Review the Basic Prompt Injection scenario as implemented by OpenA2A, focusing on its prompt-injection boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L1-03 -->
<!-- range: dvaa -->
<!-- pair: 46/110 -->
<!-- pattern: prompt -->
# Resolution · Basic Prompt Injection
> Defensive resolution and review gotchas for dvaa · L1-03
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-01 -->
<!-- range: dvaa -->
<!-- pair: 47/110 -->
<!-- pattern: prompt -->
# Jailbreak via Roleplay
> dvaa · L2-01 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Jailbreak via Roleplay scenario as implemented by OpenA2A, focusing on its jailbreak boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-01 -->
<!-- range: dvaa -->
<!-- pair: 47/110 -->
<!-- pattern: prompt -->
# Resolution · Jailbreak via Roleplay
> Defensive resolution and review gotchas for dvaa · L2-01
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-02 -->
<!-- range: dvaa -->
<!-- pair: 48/110 -->
<!-- pattern: prompt -->
# Context Window Manipulation
> dvaa · L2-02 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Context Window Manipulation scenario as implemented by OpenA2A, focusing on its context-manipulation boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-02 -->
<!-- range: dvaa -->
<!-- pair: 48/110 -->
<!-- pattern: prompt -->
# Resolution · Context Window Manipulation
> Defensive resolution and review gotchas for dvaa · L2-02
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-03 -->
<!-- range: dvaa -->
<!-- pair: 49/110 -->
<!-- pattern: sink -->
# MCP Path Traversal
> dvaa · L2-03 · medium · 1 variant(s)
- **DESCRIPTION:** Review the MCP Path Traversal scenario as implemented by OpenA2A, focusing on its mcp-exploitation boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-03 -->
<!-- range: dvaa -->
<!-- pair: 49/110 -->
<!-- pattern: sink -->
# Resolution · MCP Path Traversal
> Defensive resolution and review gotchas for dvaa · L2-03
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-04 -->
<!-- range: dvaa -->
<!-- pair: 50/110 -->
<!-- pattern: prompt -->
# Persistent Memory Injection
> dvaa · L2-04 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Persistent Memory Injection scenario as implemented by OpenA2A, focusing on its memory-injection boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-04 -->
<!-- range: dvaa -->
<!-- pair: 50/110 -->
<!-- pattern: prompt -->
# Resolution · Persistent Memory Injection
> Defensive resolution and review gotchas for dvaa · L2-04
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-05 -->
<!-- range: dvaa -->
<!-- pair: 51/110 -->
<!-- pattern: secrets -->
# Memory Credential Extraction
> dvaa · L2-05 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Memory Credential Extraction scenario as implemented by OpenA2A, focusing on its memory-injection boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-05 -->
<!-- range: dvaa -->
<!-- pair: 51/110 -->
<!-- pattern: secrets -->
# Resolution · Memory Credential Extraction
> Defensive resolution and review gotchas for dvaa · L2-05
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-06 -->
<!-- range: dvaa -->
<!-- pair: 52/110 -->
<!-- pattern: prompt -->
# Context Padding Attack
> dvaa · L2-06 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Context Padding Attack scenario as implemented by OpenA2A, focusing on its context-overflow boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-06 -->
<!-- range: dvaa -->
<!-- pair: 52/110 -->
<!-- pattern: prompt -->
# Resolution · Context Padding Attack
> Defensive resolution and review gotchas for dvaa · L2-06
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-07 -->
<!-- range: dvaa -->
<!-- pair: 53/110 -->
<!-- pattern: prompt -->
# Safety Instruction Displacement
> dvaa · L2-07 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Safety Instruction Displacement scenario as implemented by OpenA2A, focusing on its context-overflow boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-07 -->
<!-- range: dvaa -->
<!-- pair: 53/110 -->
<!-- pattern: prompt -->
# Resolution · Safety Instruction Displacement
> Defensive resolution and review gotchas for dvaa · L2-07
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-08 -->
<!-- range: dvaa -->
<!-- pair: 54/110 -->
<!-- pattern: mcp -->
# Malicious Tool Registration
> dvaa · L2-08 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Malicious Tool Registration scenario as implemented by OpenA2A, focusing on its tool-registry-poisoning boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-08 -->
<!-- range: dvaa -->
<!-- pair: 54/110 -->
<!-- pattern: mcp -->
# Resolution · Malicious Tool Registration
> Defensive resolution and review gotchas for dvaa · L2-08
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-09 -->
<!-- range: dvaa -->
<!-- pair: 55/110 -->
<!-- pattern: transport -->
# Tool Call MITM
> dvaa · L2-09 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Tool Call MITM scenario as implemented by OpenA2A, focusing on its tool-mitm boundary.
- **BOUNDARY:** Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.
- **REVIEW:** Which layer decides request meaning? Are origin, audience, version, and session identifiers bound exactly?
- **LEARN:** Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-09 -->
<!-- range: dvaa -->
<!-- pair: 55/110 -->
<!-- pattern: transport -->
# Resolution · Tool Call MITM
> Defensive resolution and review gotchas for dvaa · L2-09
- **CONTROL:** Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.
- **VALIDATE:** Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.
- **GOTCHA:** A gateway and application can each appear correct while authorising different interpretations of one request.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-01 -->
<!-- range: dvaa -->
<!-- pair: 56/110 -->
<!-- pattern: prompt -->
# Chained Prompt Injection
> dvaa · L3-01 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Chained Prompt Injection scenario as implemented by OpenA2A, focusing on its prompt-injection boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-01 -->
<!-- range: dvaa -->
<!-- pair: 56/110 -->
<!-- pattern: prompt -->
# Resolution · Chained Prompt Injection
> Defensive resolution and review gotchas for dvaa · L3-01
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-02 -->
<!-- range: dvaa -->
<!-- pair: 57/110 -->
<!-- pattern: infra -->
# SSRF via MCP
> dvaa · L3-02 · hard · 1 variant(s)
- **DESCRIPTION:** Review the SSRF via MCP scenario as implemented by OpenA2A, focusing on its mcp-exploitation boundary.
- **BOUNDARY:** A model-facing workload crosses into cloud metadata, administrative APIs, registries, or network destinations.
- **REVIEW:** Which destinations can the workload reach? Which administrative or registry actions require authentication?
- **LEARN:** Workload identity and egress are authority boundaries; model-facing services should carry minimal ambient privilege.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-02 -->
<!-- range: dvaa -->
<!-- pair: 57/110 -->
<!-- pattern: infra -->
# Resolution · SSRF via MCP
> Defensive resolution and review gotchas for dvaa · L3-02
- **CONTROL:** Default-deny egress, use workload identity, require admin authentication, isolate metadata, and keep secrets out of artifacts.
- **VALIDATE:** Review policy and use inert internal endpoints to confirm blocked destinations and authenticated administration.
- **GOTCHA:** Application input validation cannot compensate for broad network reach and over-privileged workload credentials.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-03 -->
<!-- range: dvaa -->
<!-- pair: 58/110 -->
<!-- pattern: prompt -->
# Self-Replicating Memory Entry
> dvaa · L3-03 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Self-Replicating Memory Entry scenario as implemented by OpenA2A, focusing on its memory-injection boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-03 -->
<!-- range: dvaa -->
<!-- pair: 58/110 -->
<!-- pattern: prompt -->
# Resolution · Self-Replicating Memory Entry
> Defensive resolution and review gotchas for dvaa · L3-03
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-04 -->
<!-- range: dvaa -->
<!-- pair: 59/110 -->
<!-- pattern: prompt -->
# System Prompt Extraction via Context Pressure
> dvaa · L3-04 · hard · 1 variant(s)
- **DESCRIPTION:** Review the System Prompt Extraction via Context Pressure scenario as implemented by OpenA2A, focusing on its context-overflow boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-04 -->
<!-- range: dvaa -->
<!-- pair: 59/110 -->
<!-- pattern: prompt -->
# Resolution · System Prompt Extraction via Context Pressure
> Defensive resolution and review gotchas for dvaa · L3-04
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-05 -->
<!-- range: dvaa -->
<!-- pair: 60/110 -->
<!-- pattern: mcp -->
# Tool Typosquatting
> dvaa · L3-05 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Tool Typosquatting scenario as implemented by OpenA2A, focusing on its tool-registry-poisoning boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-05 -->
<!-- range: dvaa -->
<!-- pair: 60/110 -->
<!-- pattern: mcp -->
# Resolution · Tool Typosquatting
> Defensive resolution and review gotchas for dvaa · L3-05
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-06 -->
<!-- range: dvaa -->
<!-- pair: 61/110 -->
<!-- pattern: mcp -->
# Tool Chain Data Exfiltration
> dvaa · L3-06 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Tool Chain Data Exfiltration scenario as implemented by OpenA2A, focusing on its tool-registry-poisoning boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-06 -->
<!-- range: dvaa -->
<!-- pair: 61/110 -->
<!-- pattern: mcp -->
# Resolution · Tool Chain Data Exfiltration
> Defensive resolution and review gotchas for dvaa · L3-06
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-07 -->
<!-- range: dvaa -->
<!-- pair: 62/110 -->
<!-- pattern: transport -->
# Tool Shadowing
> dvaa · L3-07 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Tool Shadowing scenario as implemented by OpenA2A, focusing on its tool-mitm boundary.
- **BOUNDARY:** Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.
- **REVIEW:** Which layer decides request meaning? Are origin, audience, version, and session identifiers bound exactly?
- **LEARN:** Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-07 -->
<!-- range: dvaa -->
<!-- pair: 62/110 -->
<!-- pattern: transport -->
# Resolution · Tool Shadowing
> Defensive resolution and review gotchas for dvaa · L3-07
- **CONTROL:** Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.
- **VALIDATE:** Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.
- **GOTCHA:** A gateway and application can each appear correct while authorising different interpretations of one request.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-08 -->
<!-- range: dvaa -->
<!-- pair: 63/110 -->
<!-- pattern: transport -->
# Traffic Redirection Attack
> dvaa · L3-08 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Traffic Redirection Attack scenario as implemented by OpenA2A, focusing on its tool-mitm boundary.
- **BOUNDARY:** Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.
- **REVIEW:** Which layer decides request meaning? Are origin, audience, version, and session identifiers bound exactly?
- **LEARN:** Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-08 -->
<!-- range: dvaa -->
<!-- pair: 63/110 -->
<!-- pattern: transport -->
# Resolution · Traffic Redirection Attack
> Defensive resolution and review gotchas for dvaa · L3-08
- **CONTROL:** Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.
- **VALIDATE:** Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.
- **GOTCHA:** A gateway and application can each appear correct while authorising different interpretations of one request.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L4-01 -->
<!-- range: dvaa -->
<!-- pair: 64/110 -->
<!-- pattern: chain -->
# Compromise SecureBot
> dvaa · L4-01 · expert · 1 variant(s)
- **DESCRIPTION:** Review the Compromise SecureBot scenario as implemented by OpenA2A, focusing on its mixed boundary.
- **BOUNDARY:** Several individually limited weaknesses compose across content, identity, tools, data, and infrastructure.
- **REVIEW:** Which earlier weakness enables the next step? Which control breaks the chain earliest and most reliably?
- **LEARN:** Security review must follow end-to-end authority and data flow because local controls can fail in composition.

---

<!-- kind: resolution -->
<!-- key: dvaa/L4-01 -->
<!-- range: dvaa -->
<!-- pair: 64/110 -->
<!-- pattern: chain -->
# Resolution · Compromise SecureBot
> Defensive resolution and review gotchas for dvaa · L4-01
- **CONTROL:** Use layered controls, trace provenance, minimise ambient authority, segment systems, and retain cross-service evidence.
- **VALIDATE:** Validate each boundary independently with safe fixtures, then review the composed data flow without executing an attack chain.
- **GOTCHA:** A control may stop one step while leaving another route to the same privileged effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L4-02 -->
<!-- range: dvaa -->
<!-- pair: 65/110 -->
<!-- pattern: identity -->
# Agent-to-Agent Attack Chain
> dvaa · L4-02 · expert · 1 variant(s)
- **DESCRIPTION:** Review the Agent-to-Agent Attack Chain scenario as implemented by OpenA2A, focusing on its agent-to-agent boundary.
- **BOUNDARY:** A principal, object, task, or delegated action crosses an identity and authorisation boundary.
- **REVIEW:** Which principal is authenticated? Is the object and delegated action authorised for that principal?
- **LEARN:** Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.

---

<!-- kind: resolution -->
<!-- key: dvaa/L4-02 -->
<!-- range: dvaa -->
<!-- pair: 65/110 -->
<!-- pattern: identity -->
# Resolution · Agent-to-Agent Attack Chain
> Defensive resolution and review gotchas for dvaa · L4-02
- **CONTROL:** Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.
- **VALIDATE:** Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.
- **GOTCHA:** A valid sender or token does not automatically authorise every downstream object or action.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/A1 -->
<!-- range: mcpgoat -->
<!-- pair: 66/110 -->
<!-- pattern: mcp -->
# Tool Poisoning
> mcpgoat · A1 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Tool Poisoning scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/A1 -->
<!-- range: mcpgoat -->
<!-- pair: 66/110 -->
<!-- pattern: mcp -->
# Resolution · Tool Poisoning
> Defensive resolution and review gotchas for mcpgoat · A1
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/A2 -->
<!-- range: mcpgoat -->
<!-- pair: 67/110 -->
<!-- pattern: mcp -->
# Tool Shadowing / Trusted-Tool Override
> mcpgoat · A2 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Tool Shadowing / Trusted-Tool Override scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/A2 -->
<!-- range: mcpgoat -->
<!-- pair: 67/110 -->
<!-- pattern: mcp -->
# Resolution · Tool Shadowing / Trusted-Tool Override
> Defensive resolution and review gotchas for mcpgoat · A2
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/A3 -->
<!-- range: mcpgoat -->
<!-- pair: 68/110 -->
<!-- pattern: mcp -->
# Rug Pull / Tool Mutation (TOCTOU)
> mcpgoat · A3 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Rug Pull / Tool Mutation (TOCTOU) scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/A3 -->
<!-- range: mcpgoat -->
<!-- pair: 68/110 -->
<!-- pattern: mcp -->
# Resolution · Rug Pull / Tool Mutation (TOCTOU)
> Defensive resolution and review gotchas for mcpgoat · A3
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/B1 -->
<!-- range: mcpgoat -->
<!-- pair: 69/110 -->
<!-- pattern: prompt -->
# Indirect Prompt Injection via Tool Output
> mcpgoat · B1 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Indirect Prompt Injection via Tool Output scenario as implemented by Sabyasachi Dhal, focusing on its Prompt/Context boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/B1 -->
<!-- range: mcpgoat -->
<!-- pair: 69/110 -->
<!-- pattern: prompt -->
# Resolution · Indirect Prompt Injection via Tool Output
> Defensive resolution and review gotchas for mcpgoat · B1
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D1 -->
<!-- range: mcpgoat -->
<!-- pair: 70/110 -->
<!-- pattern: sink -->
# Command Injection (RCE)
> mcpgoat · D1 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Command Injection (RCE) scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D1 -->
<!-- range: mcpgoat -->
<!-- pair: 70/110 -->
<!-- pattern: sink -->
# Resolution · Command Injection (RCE)
> Defensive resolution and review gotchas for mcpgoat · D1
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D2 -->
<!-- range: mcpgoat -->
<!-- pair: 71/110 -->
<!-- pattern: sink -->
# Path Traversal / Arbitrary File Read
> mcpgoat · D2 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Path Traversal / Arbitrary File Read scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D2 -->
<!-- range: mcpgoat -->
<!-- pair: 71/110 -->
<!-- pattern: sink -->
# Resolution · Path Traversal / Arbitrary File Read
> Defensive resolution and review gotchas for mcpgoat · D2
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D3 -->
<!-- range: mcpgoat -->
<!-- pair: 72/110 -->
<!-- pattern: infra -->
# Server-Side Request Forgery
> mcpgoat · D3 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Server-Side Request Forgery scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** A model-facing workload crosses into cloud metadata, administrative APIs, registries, or network destinations.
- **REVIEW:** Which destinations can the workload reach? Which administrative or registry actions require authentication?
- **LEARN:** Workload identity and egress are authority boundaries; model-facing services should carry minimal ambient privilege.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D3 -->
<!-- range: mcpgoat -->
<!-- pair: 72/110 -->
<!-- pattern: infra -->
# Resolution · Server-Side Request Forgery
> Defensive resolution and review gotchas for mcpgoat · D3
- **CONTROL:** Default-deny egress, use workload identity, require admin authentication, isolate metadata, and keep secrets out of artifacts.
- **VALIDATE:** Review policy and use inert internal endpoints to confirm blocked destinations and authenticated administration.
- **GOTCHA:** Application input validation cannot compensate for broad network reach and over-privileged workload credentials.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D4 -->
<!-- range: mcpgoat -->
<!-- pair: 73/110 -->
<!-- pattern: sink -->
# SQL Injection
> mcpgoat · D4 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the SQL Injection scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D4 -->
<!-- range: mcpgoat -->
<!-- pair: 73/110 -->
<!-- pattern: sink -->
# Resolution · SQL Injection
> Defensive resolution and review gotchas for mcpgoat · D4
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/C2 -->
<!-- range: mcpgoat -->
<!-- pair: 74/110 -->
<!-- pattern: identity -->
# Broken Authorization / Confused Deputy
> mcpgoat · C2 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Broken Authorization / Confused Deputy scenario as implemented by Sabyasachi Dhal, focusing on its AuthN/AuthZ boundary.
- **BOUNDARY:** A principal, object, task, or delegated action crosses an identity and authorisation boundary.
- **REVIEW:** Which principal is authenticated? Is the object and delegated action authorised for that principal?
- **LEARN:** Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/C2 -->
<!-- range: mcpgoat -->
<!-- pair: 74/110 -->
<!-- pattern: identity -->
# Resolution · Broken Authorization / Confused Deputy
> Defensive resolution and review gotchas for mcpgoat · C2
- **CONTROL:** Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.
- **VALIDATE:** Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.
- **GOTCHA:** A valid sender or token does not automatically authorise every downstream object or action.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/C3 -->
<!-- range: mcpgoat -->
<!-- pair: 75/110 -->
<!-- pattern: identity -->
# Insecure Direct Object Reference
> mcpgoat · C3 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Insecure Direct Object Reference scenario as implemented by Sabyasachi Dhal, focusing on its AuthN/AuthZ boundary.
- **BOUNDARY:** A principal, object, task, or delegated action crosses an identity and authorisation boundary.
- **REVIEW:** Which principal is authenticated? Is the object and delegated action authorised for that principal?
- **LEARN:** Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/C3 -->
<!-- range: mcpgoat -->
<!-- pair: 75/110 -->
<!-- pattern: identity -->
# Resolution · Insecure Direct Object Reference
> Defensive resolution and review gotchas for mcpgoat · C3
- **CONTROL:** Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.
- **VALIDATE:** Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.
- **GOTCHA:** A valid sender or token does not automatically authorise every downstream object or action.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/E1 -->
<!-- range: mcpgoat -->
<!-- pair: 76/110 -->
<!-- pattern: secrets -->
# Sensitive Data Exposure
> mcpgoat · E1 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Sensitive Data Exposure scenario as implemented by Sabyasachi Dhal, focusing on its Secrets/Exposure boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/E1 -->
<!-- range: mcpgoat -->
<!-- pair: 76/110 -->
<!-- pattern: secrets -->
# Resolution · Sensitive Data Exposure
> Defensive resolution and review gotchas for mcpgoat · E1
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/A9 -->
<!-- range: mcpgoat -->
<!-- pair: 77/110 -->
<!-- pattern: mcp -->
# Invisible-Text Tool Poisoning
> mcpgoat · A9 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Invisible-Text Tool Poisoning scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/A9 -->
<!-- range: mcpgoat -->
<!-- pair: 77/110 -->
<!-- pattern: mcp -->
# Resolution · Invisible-Text Tool Poisoning
> Defensive resolution and review gotchas for mcpgoat · A9
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/B2 -->
<!-- range: mcpgoat -->
<!-- pair: 78/110 -->
<!-- pattern: prompt -->
# Indirect Injection via Resource Content
> mcpgoat · B2 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Indirect Injection via Resource Content scenario as implemented by Sabyasachi Dhal, focusing on its Prompt/Context boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/B2 -->
<!-- range: mcpgoat -->
<!-- pair: 78/110 -->
<!-- pattern: prompt -->
# Resolution · Indirect Injection via Resource Content
> Defensive resolution and review gotchas for mcpgoat · B2
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/B3 -->
<!-- range: mcpgoat -->
<!-- pair: 79/110 -->
<!-- pattern: prompt -->
# Prompt-Template Injection
> mcpgoat · B3 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Prompt-Template Injection scenario as implemented by Sabyasachi Dhal, focusing on its Prompt/Context boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/B3 -->
<!-- range: mcpgoat -->
<!-- pair: 79/110 -->
<!-- pattern: prompt -->
# Resolution · Prompt-Template Injection
> Defensive resolution and review gotchas for mcpgoat · B3
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/B5 -->
<!-- range: mcpgoat -->
<!-- pair: 80/110 -->
<!-- pattern: mcp -->
# Sampling Abuse (server-driven LLM calls)
> mcpgoat · B5 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Sampling Abuse (server-driven LLM calls) scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/B5 -->
<!-- range: mcpgoat -->
<!-- pair: 80/110 -->
<!-- pattern: mcp -->
# Resolution · Sampling Abuse (server-driven LLM calls)
> Defensive resolution and review gotchas for mcpgoat · B5
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/C4 -->
<!-- range: mcpgoat -->
<!-- pair: 81/110 -->
<!-- pattern: identity -->
# OAuth Token-Audience Confusion
> mcpgoat · C4 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the OAuth Token-Audience Confusion scenario as implemented by Sabyasachi Dhal, focusing on its AuthN/AuthZ boundary.
- **BOUNDARY:** A principal, object, task, or delegated action crosses an identity and authorisation boundary.
- **REVIEW:** Which principal is authenticated? Is the object and delegated action authorised for that principal?
- **LEARN:** Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/C4 -->
<!-- range: mcpgoat -->
<!-- pair: 81/110 -->
<!-- pattern: identity -->
# Resolution · OAuth Token-Audience Confusion
> Defensive resolution and review gotchas for mcpgoat · C4
- **CONTROL:** Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.
- **VALIDATE:** Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.
- **GOTCHA:** A valid sender or token does not automatically authorise every downstream object or action.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D6 -->
<!-- range: mcpgoat -->
<!-- pair: 82/110 -->
<!-- pattern: sink -->
# Server-Side Template Injection
> mcpgoat · D6 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Server-Side Template Injection scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D6 -->
<!-- range: mcpgoat -->
<!-- pair: 82/110 -->
<!-- pattern: sink -->
# Resolution · Server-Side Template Injection
> Defensive resolution and review gotchas for mcpgoat · D6
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/F1 -->
<!-- range: mcpgoat -->
<!-- pair: 83/110 -->
<!-- pattern: transport -->
# DNS Rebinding / Missing Origin Validation
> mcpgoat · F1 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the DNS Rebinding / Missing Origin Validation scenario as implemented by Sabyasachi Dhal, focusing on its Transport boundary.
- **BOUNDARY:** Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.
- **REVIEW:** Which layer decides request meaning? Are origin, audience, version, and session identifiers bound exactly?
- **LEARN:** Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/F1 -->
<!-- range: mcpgoat -->
<!-- pair: 83/110 -->
<!-- pattern: transport -->
# Resolution · DNS Rebinding / Missing Origin Validation
> Defensive resolution and review gotchas for mcpgoat · F1
- **CONTROL:** Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.
- **VALIDATE:** Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.
- **GOTCHA:** A gateway and application can each appear correct while authorising different interpretations of one request.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/F2 -->
<!-- range: mcpgoat -->
<!-- pair: 84/110 -->
<!-- pattern: transport -->
# CORS Misconfiguration
> mcpgoat · F2 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the CORS Misconfiguration scenario as implemented by Sabyasachi Dhal, focusing on its Transport boundary.
- **BOUNDARY:** Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.
- **REVIEW:** Which layer decides request meaning? Are origin, audience, version, and session identifiers bound exactly?
- **LEARN:** Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/F2 -->
<!-- range: mcpgoat -->
<!-- pair: 84/110 -->
<!-- pattern: transport -->
# Resolution · CORS Misconfiguration
> Defensive resolution and review gotchas for mcpgoat · F2
- **CONTROL:** Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.
- **VALIDATE:** Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.
- **GOTCHA:** A gateway and application can each appear correct while authorising different interpretations of one request.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/C6 -->
<!-- range: mcpgoat -->
<!-- pair: 85/110 -->
<!-- pattern: transport -->
# Predictable Session IDs (hijack)
> mcpgoat · C6 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Predictable Session IDs (hijack) scenario as implemented by Sabyasachi Dhal, focusing on its Transport boundary.
- **BOUNDARY:** Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.
- **REVIEW:** Which layer decides request meaning? Are origin, audience, version, and session identifiers bound exactly?
- **LEARN:** Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/C6 -->
<!-- range: mcpgoat -->
<!-- pair: 85/110 -->
<!-- pattern: transport -->
# Resolution · Predictable Session IDs (hijack)
> Defensive resolution and review gotchas for mcpgoat · C6
- **CONTROL:** Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.
- **VALIDATE:** Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.
- **GOTCHA:** A gateway and application can each appear correct while authorising different interpretations of one request.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/G1 -->
<!-- range: mcpgoat -->
<!-- pair: 86/110 -->
<!-- pattern: dos -->
# Unbounded Consumption (cost/DoS)
> mcpgoat · G1 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Unbounded Consumption (cost/DoS) scenario as implemented by Sabyasachi Dhal, focusing on its DoS/Cost boundary.
- **BOUNDARY:** Attacker-controlled work crosses compute, memory, token, concurrency, or financial budget boundaries.
- **REVIEW:** Which resource grows with input? Where are tenant, tool, and global budgets enforced?
- **LEARN:** Availability and spend are security properties that require explicit per-request and aggregate budgets.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/G1 -->
<!-- range: mcpgoat -->
<!-- pair: 86/110 -->
<!-- pattern: dos -->
# Resolution · Unbounded Consumption (cost/DoS)
> Defensive resolution and review gotchas for mcpgoat · G1
- **CONTROL:** Set timeouts, size and token limits, concurrency quotas, rate limits, cancellation, and cost telemetry.
- **VALIDATE:** Use bounded synthetic workloads to assert predictable rejection before resource use approaches operational limits.
- **GOTCHA:** Per-request limits alone miss distributed or repeated consumption across sessions and identities.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/G4 -->
<!-- range: mcpgoat -->
<!-- pair: 87/110 -->
<!-- pattern: dos -->
# Regular-Expression DoS (ReDoS)
> mcpgoat · G4 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Regular-Expression DoS (ReDoS) scenario as implemented by Sabyasachi Dhal, focusing on its DoS/Cost boundary.
- **BOUNDARY:** Attacker-controlled work crosses compute, memory, token, concurrency, or financial budget boundaries.
- **REVIEW:** Which resource grows with input? Where are tenant, tool, and global budgets enforced?
- **LEARN:** Availability and spend are security properties that require explicit per-request and aggregate budgets.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/G4 -->
<!-- range: mcpgoat -->
<!-- pair: 87/110 -->
<!-- pattern: dos -->
# Resolution · Regular-Expression DoS (ReDoS)
> Defensive resolution and review gotchas for mcpgoat · G4
- **CONTROL:** Set timeouts, size and token limits, concurrency quotas, rate limits, cancellation, and cost telemetry.
- **VALIDATE:** Use bounded synthetic workloads to assert predictable rejection before resource use approaches operational limits.
- **GOTCHA:** Per-request limits alone miss distributed or repeated consumption across sessions and identities.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D5 -->
<!-- range: mcpgoat -->
<!-- pair: 88/110 -->
<!-- pattern: sink -->
# NoSQL Injection
> mcpgoat · D5 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the NoSQL Injection scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D5 -->
<!-- range: mcpgoat -->
<!-- pair: 88/110 -->
<!-- pattern: sink -->
# Resolution · NoSQL Injection
> Defensive resolution and review gotchas for mcpgoat · D5
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D7 -->
<!-- range: mcpgoat -->
<!-- pair: 89/110 -->
<!-- pattern: sink -->
# XML External Entity (XXE)
> mcpgoat · D7 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the XML External Entity (XXE) scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D7 -->
<!-- range: mcpgoat -->
<!-- pair: 89/110 -->
<!-- pattern: sink -->
# Resolution · XML External Entity (XXE)
> Defensive resolution and review gotchas for mcpgoat · D7
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D8 -->
<!-- range: mcpgoat -->
<!-- pair: 90/110 -->
<!-- pattern: sink -->
# Insecure Deserialization (prototype pollution)
> mcpgoat · D8 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Insecure Deserialization (prototype pollution) scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D8 -->
<!-- range: mcpgoat -->
<!-- pair: 90/110 -->
<!-- pattern: sink -->
# Resolution · Insecure Deserialization (prototype pollution)
> Defensive resolution and review gotchas for mcpgoat · D8
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/H1 -->
<!-- range: mcpgoat -->
<!-- pair: 91/110 -->
<!-- pattern: supply -->
# Supply Chain (typosquat / unsigned package)
> mcpgoat · H1 · tiered · 3 variant(s)
- **DESCRIPTION:** Review the Supply Chain (typosquat / unsigned package) scenario as implemented by Sabyasachi Dhal, focusing on its Supply chain boundary.
- **BOUNDARY:** A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.
- **REVIEW:** What identity and digest bind the artifact? Where is it loaded, merged, trained, or resolved?
- **LEARN:** AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/H1 -->
<!-- range: mcpgoat -->
<!-- pair: 91/110 -->
<!-- pattern: supply -->
# Resolution · Supply Chain (typosquat / unsigned package)
> Defensive resolution and review gotchas for mcpgoat · H1
- **CONTROL:** Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.
- **VALIDATE:** Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.
- **GOTCHA:** A familiar filename, package name, or model label is not proof of origin or safe behavior.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/01 -->
<!-- range: dvmcp -->
<!-- pair: 92/110 -->
<!-- pattern: prompt -->
# Basic Prompt Injection
> dvmcp · 01 · easy · 1 variant(s)
- **DESCRIPTION:** Review the Basic Prompt Injection scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its Prompt/Context boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvmcp/01 -->
<!-- range: dvmcp -->
<!-- pair: 92/110 -->
<!-- pattern: prompt -->
# Resolution · Basic Prompt Injection
> Defensive resolution and review gotchas for dvmcp · 01
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/02 -->
<!-- range: dvmcp -->
<!-- pair: 93/110 -->
<!-- pattern: mcp -->
# Tool Poisoning
> dvmcp · 02 · easy · 1 variant(s)
- **DESCRIPTION:** Review the Tool Poisoning scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its MCP-specific boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: dvmcp/02 -->
<!-- range: dvmcp -->
<!-- pair: 93/110 -->
<!-- pattern: mcp -->
# Resolution · Tool Poisoning
> Defensive resolution and review gotchas for dvmcp · 02
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/03 -->
<!-- range: dvmcp -->
<!-- pair: 94/110 -->
<!-- pattern: identity -->
# Excessive Permission Scope
> dvmcp · 03 · easy · 1 variant(s)
- **DESCRIPTION:** Review the Excessive Permission Scope scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its AuthN/AuthZ boundary.
- **BOUNDARY:** A principal, object, task, or delegated action crosses an identity and authorisation boundary.
- **REVIEW:** Which principal is authenticated? Is the object and delegated action authorised for that principal?
- **LEARN:** Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.

---

<!-- kind: resolution -->
<!-- key: dvmcp/03 -->
<!-- range: dvmcp -->
<!-- pair: 94/110 -->
<!-- pattern: identity -->
# Resolution · Excessive Permission Scope
> Defensive resolution and review gotchas for dvmcp · 03
- **CONTROL:** Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.
- **VALIDATE:** Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.
- **GOTCHA:** A valid sender or token does not automatically authorise every downstream object or action.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/04 -->
<!-- range: dvmcp -->
<!-- pair: 95/110 -->
<!-- pattern: mcp -->
# Rug Pull Attack
> dvmcp · 04 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Rug Pull Attack scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its MCP-specific boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: dvmcp/04 -->
<!-- range: dvmcp -->
<!-- pair: 95/110 -->
<!-- pattern: mcp -->
# Resolution · Rug Pull Attack
> Defensive resolution and review gotchas for dvmcp · 04
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/05 -->
<!-- range: dvmcp -->
<!-- pair: 96/110 -->
<!-- pattern: mcp -->
# Tool Shadowing
> dvmcp · 05 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Tool Shadowing scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its MCP-specific boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: dvmcp/05 -->
<!-- range: dvmcp -->
<!-- pair: 96/110 -->
<!-- pattern: mcp -->
# Resolution · Tool Shadowing
> Defensive resolution and review gotchas for dvmcp · 05
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/06 -->
<!-- range: dvmcp -->
<!-- pair: 97/110 -->
<!-- pattern: prompt -->
# Indirect Prompt Injection
> dvmcp · 06 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Indirect Prompt Injection scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its Prompt/Context boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: dvmcp/06 -->
<!-- range: dvmcp -->
<!-- pair: 97/110 -->
<!-- pattern: prompt -->
# Resolution · Indirect Prompt Injection
> Defensive resolution and review gotchas for dvmcp · 06
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/07 -->
<!-- range: dvmcp -->
<!-- pair: 98/110 -->
<!-- pattern: secrets -->
# Token Theft
> dvmcp · 07 · medium · 1 variant(s)
- **DESCRIPTION:** Review the Token Theft scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its Secrets/Exposure boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: dvmcp/07 -->
<!-- range: dvmcp -->
<!-- pair: 98/110 -->
<!-- pattern: secrets -->
# Resolution · Token Theft
> Defensive resolution and review gotchas for dvmcp · 07
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/08 -->
<!-- range: dvmcp -->
<!-- pair: 99/110 -->
<!-- pattern: sink -->
# Malicious Code Execution
> dvmcp · 08 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Malicious Code Execution scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: dvmcp/08 -->
<!-- range: dvmcp -->
<!-- pair: 99/110 -->
<!-- pattern: sink -->
# Resolution · Malicious Code Execution
> Defensive resolution and review gotchas for dvmcp · 08
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/09 -->
<!-- range: dvmcp -->
<!-- pair: 100/110 -->
<!-- pattern: sink -->
# Remote Access Control
> dvmcp · 09 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Remote Access Control scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: dvmcp/09 -->
<!-- range: dvmcp -->
<!-- pair: 100/110 -->
<!-- pattern: sink -->
# Resolution · Remote Access Control
> Defensive resolution and review gotchas for dvmcp · 09
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/10 -->
<!-- range: dvmcp -->
<!-- pair: 101/110 -->
<!-- pattern: chain -->
# Multi-Vector Attack
> dvmcp · 10 · hard · 1 variant(s)
- **DESCRIPTION:** Review the Multi-Vector Attack scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its Attack chain boundary.
- **BOUNDARY:** Several individually limited weaknesses compose across content, identity, tools, data, and infrastructure.
- **REVIEW:** Which earlier weakness enables the next step? Which control breaks the chain earliest and most reliably?
- **LEARN:** Security review must follow end-to-end authority and data flow because local controls can fail in composition.

---

<!-- kind: resolution -->
<!-- key: dvmcp/10 -->
<!-- range: dvmcp -->
<!-- pair: 101/110 -->
<!-- pattern: chain -->
# Resolution · Multi-Vector Attack
> Defensive resolution and review gotchas for dvmcp · 10
- **CONTROL:** Use layered controls, trace provenance, minimise ambient authority, segment systems, and retain cross-service evidence.
- **VALIDATE:** Validate each boundary independently with safe fixtures, then review the composed data flow without executing an attack chain.
- **GOTCHA:** A control may stop one step while leaving another route to the same privileged effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/filesystem-workspace-actions -->
<!-- range: appsecco-mcp -->
<!-- pair: 102/110 -->
<!-- pattern: sink -->
# Filesystem Workspace Actions
> appsecco-mcp · filesystem-workspace-actions · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Filesystem Workspace Actions scenario as implemented by Appsecco, focusing on its Path traversal / code execution boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/filesystem-workspace-actions -->
<!-- range: appsecco-mcp -->
<!-- pair: 102/110 -->
<!-- pattern: sink -->
# Resolution · Filesystem Workspace Actions
> Defensive resolution and review gotchas for appsecco-mcp · filesystem-workspace-actions
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/indirect-prompt-injection -->
<!-- range: appsecco-mcp -->
<!-- pair: 103/110 -->
<!-- pattern: prompt -->
# Indirect Prompt Injection (stdio)
> appsecco-mcp · indirect-prompt-injection · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Indirect Prompt Injection (stdio) scenario as implemented by Appsecco, focusing on its Prompt/Context boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/indirect-prompt-injection -->
<!-- range: appsecco-mcp -->
<!-- pair: 103/110 -->
<!-- pattern: prompt -->
# Resolution · Indirect Prompt Injection (stdio)
> Defensive resolution and review gotchas for appsecco-mcp · indirect-prompt-injection
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/indirect-prompt-injection-remote -->
<!-- range: appsecco-mcp -->
<!-- pair: 104/110 -->
<!-- pattern: prompt -->
# Indirect Prompt Injection (HTTP+SSE)
> appsecco-mcp · indirect-prompt-injection-remote · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Indirect Prompt Injection (HTTP+SSE) scenario as implemented by Appsecco, focusing on its Prompt/Context boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/indirect-prompt-injection-remote -->
<!-- range: appsecco-mcp -->
<!-- pair: 104/110 -->
<!-- pattern: prompt -->
# Resolution · Indirect Prompt Injection (HTTP+SSE)
> Defensive resolution and review gotchas for appsecco-mcp · indirect-prompt-injection-remote
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/malicious-code-exec -->
<!-- range: appsecco-mcp -->
<!-- pair: 105/110 -->
<!-- pattern: sink -->
# Malicious Code Execution
> appsecco-mcp · malicious-code-exec · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Malicious Code Execution scenario as implemented by Appsecco, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.
- **REVIEW:** Which sink interprets the value? Is validation applied after decoding and canonicalisation?
- **LEARN:** The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/malicious-code-exec -->
<!-- range: appsecco-mcp -->
<!-- pair: 105/110 -->
<!-- pattern: sink -->
# Resolution · Malicious Code Execution
> Defensive resolution and review gotchas for appsecco-mcp · malicious-code-exec
- **CONTROL:** Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.
- **VALIDATE:** Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.
- **GOTCHA:** A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/malicious-tools -->
<!-- range: appsecco-mcp -->
<!-- pair: 106/110 -->
<!-- pattern: mcp -->
# Malicious Tools
> appsecco-mcp · malicious-tools · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Malicious Tools scenario as implemented by Appsecco, focusing on its Tool output poisoning boundary.
- **BOUNDARY:** MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.
- **REVIEW:** What does the host trust before execution? Can definitions, results, or capabilities change after approval?
- **LEARN:** Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/malicious-tools -->
<!-- range: appsecco-mcp -->
<!-- pair: 106/110 -->
<!-- pattern: mcp -->
# Resolution · Malicious Tools
> Defensive resolution and review gotchas for appsecco-mcp · malicious-tools
- **CONTROL:** Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.
- **VALIDATE:** Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.
- **GOTCHA:** One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/namespace-typosquatting -->
<!-- range: appsecco-mcp -->
<!-- pair: 107/110 -->
<!-- pattern: supply -->
# Namespace Typosquatting
> appsecco-mcp · namespace-typosquatting · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Namespace Typosquatting scenario as implemented by Appsecco, focusing on its Supply chain boundary.
- **BOUNDARY:** A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.
- **REVIEW:** What identity and digest bind the artifact? Where is it loaded, merged, trained, or resolved?
- **LEARN:** AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/namespace-typosquatting -->
<!-- range: appsecco-mcp -->
<!-- pair: 107/110 -->
<!-- pattern: supply -->
# Resolution · Namespace Typosquatting
> Defensive resolution and review gotchas for appsecco-mcp · namespace-typosquatting
- **CONTROL:** Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.
- **VALIDATE:** Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.
- **GOTCHA:** A familiar filename, package name, or model label is not proof of origin or safe behavior.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/outdated-packages -->
<!-- range: appsecco-mcp -->
<!-- pair: 108/110 -->
<!-- pattern: supply -->
# Outdated Packages
> appsecco-mcp · outdated-packages · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Outdated Packages scenario as implemented by Appsecco, focusing on its Supply chain boundary.
- **BOUNDARY:** A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.
- **REVIEW:** What identity and digest bind the artifact? Where is it loaded, merged, trained, or resolved?
- **LEARN:** AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/outdated-packages -->
<!-- range: appsecco-mcp -->
<!-- pair: 108/110 -->
<!-- pattern: supply -->
# Resolution · Outdated Packages
> Defensive resolution and review gotchas for appsecco-mcp · outdated-packages
- **CONTROL:** Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.
- **VALIDATE:** Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.
- **GOTCHA:** A familiar filename, package name, or model label is not proof of origin or safe behavior.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/secrets-pii -->
<!-- range: appsecco-mcp -->
<!-- pair: 109/110 -->
<!-- pattern: secrets -->
# Secrets and PII Exposure
> appsecco-mcp · secrets-pii · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Secrets and PII Exposure scenario as implemented by Appsecco, focusing on its Secrets/Exposure boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/secrets-pii -->
<!-- range: appsecco-mcp -->
<!-- pair: 109/110 -->
<!-- pattern: secrets -->
# Resolution · Secrets and PII Exposure
> Defensive resolution and review gotchas for appsecco-mcp · secrets-pii
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/wikipedia-streamable -->
<!-- range: appsecco-mcp -->
<!-- pair: 110/110 -->
<!-- pattern: prompt -->
# Wikipedia (Streamable HTTP)
> appsecco-mcp · wikipedia-streamable · ungraded · 1 variant(s)
- **DESCRIPTION:** Review the Wikipedia (Streamable HTTP) scenario as implemented by Appsecco, focusing on its Remote content injection boundary.
- **BOUNDARY:** Untrusted content crosses into model-visible instructions or persistent context.
- **REVIEW:** Which fields can influence instructions? Can retrieved, tool, or remembered content persist or trigger an action?
- **LEARN:** Content provenance and instruction authority must remain distinct throughout the model pipeline.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/wikipedia-streamable -->
<!-- range: appsecco-mcp -->
<!-- pair: 110/110 -->
<!-- pattern: prompt -->
# Resolution · Wikipedia (Streamable HTTP)
> Defensive resolution and review gotchas for appsecco-mcp · wikipedia-streamable
- **CONTROL:** Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.
- **VALIDATE:** Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.
- **GOTCHA:** Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.
