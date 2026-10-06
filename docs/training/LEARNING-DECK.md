<!-- kind: challenge -->
<!-- key: builtin/01/first-contact -->
<!-- range: builtin -->
<!-- pair: 1/110 -->
<!-- pattern: prompt -->
# First contact -- coax the orientation flag out of the Guide
> builtin · 01/first-contact · easy · 1 declared variant(s) · concept-level card
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
> builtin · 02/fingerprint-model · easy · 1 declared variant(s) · concept-level card
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
> builtin · 02/enumerate-surfaces · easy · 1 declared variant(s) · concept-level card
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
> builtin · 02/leak-config · medium · 1 declared variant(s) · concept-level card
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
> builtin · 03/sys-prompt-leak · easy · 1 declared variant(s) · concept-level card
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
> builtin · 03/indirect-injection · medium · 1 declared variant(s) · concept-level card
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
> builtin · 03/tool-exfil · hard · 1 declared variant(s) · concept-level card
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
> builtin · 03/memory-poisoning · hard · 1 declared variant(s) · concept-level card
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
> builtin · 04/trust-exploitation · easy · 1 declared variant(s) · concept-level card
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
> builtin · 04/message-manipulation · medium · 1 declared variant(s) · concept-level card
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
> builtin · 04/agent-impersonation · hard · 1 declared variant(s) · concept-level card
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
> builtin · 04/session-smuggling · impossible · 1 declared variant(s) · concept-level card
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
> builtin · 05/knowledge-poisoning · easy · 1 declared variant(s) · concept-level card
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
> builtin · 05/retrieval-manipulation · medium · 1 declared variant(s) · concept-level card
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
> builtin · 05/citation-spoofing · hard · 1 declared variant(s) · concept-level card
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
> builtin · 06/embedding-inversion · hard · 1 declared variant(s) · concept-level card
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
> builtin · 06/membership-inference · easy · 1 declared variant(s) · concept-level card
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
> builtin · 06/embedding-collision · medium · 1 declared variant(s) · concept-level card
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
<!-- pattern: tool-poisoning -->
# tools: tool-description poisoning hijacks the host
> builtin · 07/tool-poisoning · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models tools: tool-description poisoning hijacks the host, focusing on its tools trust boundary.
- **BOUNDARY:** Tool descriptions and results cross from a server-controlled metadata plane into model planning and user approval.
- **REVIEW:** Which metadata reaches the model or approval UI? Does execution use the same reviewed, authenticated definition?
- **LEARN:** Tool metadata is untrusted content and must not silently grant authority or inject instructions.

---

<!-- kind: resolution -->
<!-- key: builtin/07/tool-poisoning -->
<!-- range: builtin -->
<!-- pair: 19/110 -->
<!-- pattern: tool-poisoning -->
# Resolution · tools: tool-description poisoning hijacks the host
> Defensive resolution and review gotchas for builtin · 07/tool-poisoning
- **CONTROL:** Authenticate servers, sanitise and canonicalise metadata, show security-relevant fields, and authorise every call outside the description.
- **VALIDATE:** Use benign instruction-like metadata to confirm it remains visible as data and cannot broaden a tool's permitted effect.
- **GOTCHA:** A harmless tool name can conceal instructions in descriptions, annotations, or returned content.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/resource-traversal -->
<!-- range: builtin -->
<!-- pair: 20/110 -->
<!-- pattern: path -->
# resources: path traversal in resources/read
> builtin · 07/resource-traversal · medium · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models resources: path traversal in resources/read, focusing on its resources trust boundary.
- **BOUNDARY:** An untrusted path or URI crosses into filesystem resolution outside an authorised root.
- **REVIEW:** What is the canonical allowed root? Can decoding, symlinks, alternate separators, or races change the resolved target?
- **LEARN:** Access decisions must use the final canonical target and remain safe across encoding, absolute paths, and symbolic links.

---

<!-- kind: resolution -->
<!-- key: builtin/07/resource-traversal -->
<!-- range: builtin -->
<!-- pair: 20/110 -->
<!-- pattern: path -->
# Resolution · resources: path traversal in resources/read
> Defensive resolution and review gotchas for builtin · 07/resource-traversal
- **CONTROL:** Resolve paths safely, reject absolute and escaping targets, enforce containment after canonicalisation, and run with minimal filesystem access.
- **VALIDATE:** Use temporary in-root and out-of-root fixtures with encoded, absolute, separator, and symlink cases and assert fail-closed behavior.
- **GOTCHA:** String-prefix checks can approve sibling paths or links whose final target lies outside the intended root.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/prompt-injection -->
<!-- range: builtin -->
<!-- pair: 21/110 -->
<!-- pattern: prompt -->
# prompts: argument injection discloses a privileged template block
> builtin · 07/prompt-injection · medium · 1 declared variant(s) · concept-level card
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
<!-- pattern: sampling -->
# sampling: server-initiated sampling exfiltrates host context
> builtin · 07/sampling-abuse · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models sampling: server-initiated sampling exfiltrates host context, focusing on its sampling trust boundary.
- **BOUNDARY:** A server-requested model call crosses back into host context, credentials, tokens, and compute budgets.
- **REVIEW:** Which context is shared with the sampled model? Who authorises the purpose, model, token budget, and returned destination?
- **LEARN:** Sampling is a privileged host action that needs explicit purpose, context minimisation, consent, and resource limits.

---

<!-- kind: resolution -->
<!-- key: builtin/07/sampling-abuse -->
<!-- range: builtin -->
<!-- pair: 22/110 -->
<!-- pattern: sampling -->
# Resolution · sampling: server-initiated sampling exfiltrates host context
> Defensive resolution and review gotchas for builtin · 07/sampling-abuse
- **CONTROL:** Require informed consent, minimise context, isolate credentials, allow-list models and purposes, cap tokens and cost, and audit results.
- **VALIDATE:** Use synthetic host context and bounded budgets to confirm an untrusted server cannot expand context or repeat calls silently.
- **GOTCHA:** Approving the parent tool call does not automatically approve every server-initiated model call it requests.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/roots-bypass -->
<!-- range: builtin -->
<!-- pair: 23/110 -->
<!-- pattern: scope -->
# roots: declared client roots are not enforced
> builtin · 07/roots-bypass · medium · 1 declared variant(s) · concept-level card
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
<!-- pattern: elicitation -->
# elicitation: server elicits credentials the host auto-answers
> builtin · 07/elicitation-phishing · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models elicitation: server elicits credentials the host auto-answers, focusing on its elicitation trust boundary.
- **BOUNDARY:** A server-generated request crosses into a trusted user interaction and may solicit sensitive input.
- **REVIEW:** Can the user see who requested the value and why? Can the host auto-fill credentials or accept undeclared fields?
- **LEARN:** Elicitation needs a trusted host UI, clear server identity and purpose, schema limits, and no automatic secret completion.

---

<!-- kind: resolution -->
<!-- key: builtin/07/elicitation-phishing -->
<!-- range: builtin -->
<!-- pair: 24/110 -->
<!-- pattern: elicitation -->
# Resolution · elicitation: server elicits credentials the host auto-answers
> Defensive resolution and review gotchas for builtin · 07/elicitation-phishing
- **CONTROL:** Render elicitations in trusted chrome, show provenance, allow-list schemas, block secret autofill, and require explicit user consent.
- **VALIDATE:** Send benign unexpected and sensitive-looking fields and confirm the host refuses, redacts, or requires an explicit decision.
- **GOTCHA:** A valid elicitation schema does not make the requested value appropriate for that server.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/logging-leak -->
<!-- range: builtin -->
<!-- pair: 25/110 -->
<!-- pattern: logging -->
# logging: debug log notifications leak a session token
> builtin · 07/logging-leak · easy · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models logging: debug log notifications leak a session token, focusing on its logging trust boundary.
- **BOUNDARY:** Runtime secrets and personal data cross into diagnostic notifications, logs, and support exports.
- **REVIEW:** Which values can reach debug output? Who may change verbosity and retrieve the resulting records?
- **LEARN:** Logging level changes must not bypass data classification, redaction, or caller authorisation.

---

<!-- kind: resolution -->
<!-- key: builtin/07/logging-leak -->
<!-- range: builtin -->
<!-- pair: 25/110 -->
<!-- pattern: logging -->
# Resolution · logging: debug log notifications leak a session token
> Defensive resolution and review gotchas for builtin · 07/logging-leak
- **CONTROL:** Use structured allow-listed logging, redact at source, restrict verbosity changes, separate tenants, and apply retention controls.
- **VALIDATE:** Exercise each log level with synthetic canaries and assert that sensitive fields never appear for unauthorised readers.
- **GOTCHA:** Disabling verbose logs in production does not fix code paths that still format secrets before filtering.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/completion-leak -->
<!-- range: builtin -->
<!-- pair: 26/110 -->
<!-- pattern: completion -->
# completion: autocompletion enumerates secret values
> builtin · 07/completion-leak · easy · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models completion: autocompletion enumerates secret values, focusing on its completion trust boundary.
- **BOUNDARY:** Autocompletion crosses from partial user input into internal indexes, identifiers, or secret-backed values.
- **REVIEW:** Which corpus backs suggestions? Is every suggested value authorised for this principal and purpose?
- **LEARN:** Completion sources need the same object and field authorisation as the final read operation.

---

<!-- kind: resolution -->
<!-- key: builtin/07/completion-leak -->
<!-- range: builtin -->
<!-- pair: 26/110 -->
<!-- pattern: completion -->
# Resolution · completion: autocompletion enumerates secret values
> Defensive resolution and review gotchas for builtin · 07/completion-leak
- **CONTROL:** Use non-sensitive suggestion indexes, enforce field-level authorisation, cap results, and avoid secret stores as completion sources.
- **VALIDATE:** Probe with benign prefixes under different identities and assert that suggestions reveal only each caller's allowed namespace.
- **GOTCHA:** Hiding a complete value is insufficient when repeated prefix queries can enumerate it incrementally.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/rug-pull -->
<!-- range: builtin -->
<!-- pair: 27/110 -->
<!-- pattern: rug-pull -->
# tools: rug-pull -- tool behaviour changes after approval
> builtin · 07/rug-pull · medium · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models tools: rug-pull -- tool behaviour changes after approval, focusing on its tools (rug-pull) trust boundary.
- **BOUNDARY:** A previously reviewed tool definition changes between approval, discovery, and execution.
- **REVIEW:** Which digest was approved? What forces re-review when the definition or server identity changes?
- **LEARN:** Approval applies to an immutable definition digest and must be invalidated when security-relevant metadata or behavior changes.

---

<!-- kind: resolution -->
<!-- key: builtin/07/rug-pull -->
<!-- range: builtin -->
<!-- pair: 27/110 -->
<!-- pattern: rug-pull -->
# Resolution · tools: rug-pull -- tool behaviour changes after approval
> Defensive resolution and review gotchas for builtin · 07/rug-pull
- **CONTROL:** Pin signed definitions, compare canonical digests before every call, cache immutably, and require re-approval for any change.
- **VALIDATE:** Use two benign versions of one tool and assert that the second cannot run under approval granted to the first.
- **GOTCHA:** Periodic refresh without digest-bound approval creates a time-of-check/time-of-use gap.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/command-injection -->
<!-- range: builtin -->
<!-- pair: 28/110 -->
<!-- pattern: command -->
# tools: command injection -> remote code execution
> builtin · 07/command-injection · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models tools: command injection -> remote code execution, focusing on its tools (rce) trust boundary.
- **BOUNDARY:** Untrusted arguments cross into a shell, interpreter, dynamic loader, or operating-system process boundary.
- **REVIEW:** Is a shell or evaluator involved? Are executable identity and every argument fixed or independently allow-listed?
- **LEARN:** Data must remain structured arguments and must never become executable command syntax.

---

<!-- kind: resolution -->
<!-- key: builtin/07/command-injection -->
<!-- range: builtin -->
<!-- pair: 28/110 -->
<!-- pattern: command -->
# Resolution · tools: command injection -> remote code execution
> Defensive resolution and review gotchas for builtin · 07/command-injection
- **CONTROL:** Remove shell evaluation, call fixed executables with argument arrays, validate typed values, drop privileges, and sandbox the process.
- **VALIDATE:** Use harmless metacharacter and unexpected-argument fixtures and assert they are rejected or passed literally without side effects.
- **GOTCHA:** Escaping for one shell or platform is fragile; avoiding the interpreter is the durable control.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/07/header-routing-confusion -->
<!-- range: builtin -->
<!-- pair: 29/110 -->
<!-- pattern: transport -->
# 2026 routing: header/body policy desynchronization
> builtin · 07/header-routing-confusion · hard · 1 declared variant(s) · concept-level card
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
<!-- pattern: unicode -->
# tools: Unicode-concealed tool-description poisoning past the scanner
> builtin · 07/unicode-tool-poisoning · impossible · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models tools: unicode-concealed tool-description poisoning past the scanner, focusing on its tools (concealment) trust boundary.
- **BOUNDARY:** Unicode formatting and confusable characters cross from raw metadata into scanning, display, and model-visible text.
- **REVIEW:** Which normalization form is enforced? Are bidirectional controls, zero-width characters, and confusables exposed to reviewers?
- **LEARN:** Security review and execution must use one canonical representation while preserving warnings about concealed characters.

---

<!-- kind: resolution -->
<!-- key: builtin/07/unicode-tool-poisoning -->
<!-- range: builtin -->
<!-- pair: 30/110 -->
<!-- pattern: unicode -->
# Resolution · tools: Unicode-concealed tool-description poisoning past the scanner
> Defensive resolution and review gotchas for builtin · 07/unicode-tool-poisoning
- **CONTROL:** Normalize consistently, reject or visibly escape control characters, detect confusables, and scan the same canonical text shown to users.
- **VALIDATE:** Use harmless strings containing bidi, zero-width, and confusable characters and assert identical scanner and display decisions.
- **GOTCHA:** Stripping a subset of invisible characters can create a second, differently interpreted representation.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/08/malicious-weights -->
<!-- range: builtin -->
<!-- pair: 31/110 -->
<!-- pattern: model-deserialization -->
# RCE via unsafe model deserialization
> builtin · 08/malicious-weights · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models rce via unsafe model deserialization, focusing on its supply-weights trust boundary.
- **BOUNDARY:** A model artifact crosses from storage into a loader that may instantiate executable objects or custom operators.
- **REVIEW:** Can the format encode executable objects or custom code? Where are provenance, signature, and digest verified before loading?
- **LEARN:** Model loading should consume data-only formats and occur in isolation before an artifact reaches production authority.

---

<!-- kind: resolution -->
<!-- key: builtin/08/malicious-weights -->
<!-- range: builtin -->
<!-- pair: 31/110 -->
<!-- pattern: model-deserialization -->
# Resolution · RCE via unsafe model deserialization
> Defensive resolution and review gotchas for builtin · 08/malicious-weights
- **CONTROL:** Prefer safe tensor formats, verify signed provenance and immutable digests, scan or convert in a sandbox, and block custom loading hooks.
- **VALIDATE:** Load only benign fixtures in an isolated process and assert unsafe formats, unknown operators, and provenance failures are rejected.
- **GOTCHA:** A model repository or familiar extension does not guarantee that the loader treats the file as data only.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in oracle verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/08/poisoned-dataset -->
<!-- range: builtin -->
<!-- pair: 32/110 -->
<!-- pattern: data-poisoning -->
# Backdoor the model via dataset poisoning
> builtin · 08/poisoned-dataset · easy · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models backdoor the model via dataset poisoning, focusing on its supply-data trust boundary.
- **BOUNDARY:** Training or retrieval records cross from collection and labeling into learned or indexed behavior.
- **REVIEW:** Who can add or relabel records? Which tests detect targeted triggers, skew, duplication, or provenance gaps?
- **LEARN:** Dataset integrity requires provenance, controlled contribution, anomaly review, and behavior-focused validation before promotion.

---

<!-- kind: resolution -->
<!-- key: builtin/08/poisoned-dataset -->
<!-- range: builtin -->
<!-- pair: 32/110 -->
<!-- pattern: data-poisoning -->
# Resolution · Backdoor the model via dataset poisoning
> Defensive resolution and review gotchas for builtin · 08/poisoned-dataset
- **CONTROL:** Version and sign datasets, restrict writers, review labels, deduplicate, scan anomalies, and evaluate targeted slices before deployment.
- **VALIDATE:** Add harmless synthetic outliers and trigger-like canaries and assert ingestion or evaluation identifies them before promotion.
- **GOTCHA:** Aggregate quality metrics can remain healthy while a small targeted subset creates a reliable backdoor.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/08/backdoored-adapter -->
<!-- range: builtin -->
<!-- pair: 33/110 -->
<!-- pattern: adapter-backdoor -->
# Inject behaviour via a backdoored adapter
> builtin · 08/backdoored-adapter · easy · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models inject behaviour via a backdoored adapter, focusing on its supply-adapter trust boundary.
- **BOUNDARY:** An adapter or fine-tune delta crosses into a trusted base model and changes behavior without replacing the full artifact.
- **REVIEW:** Which signed identity produced the adapter? What targeted behavior changes appear when it is composed with the approved base?
- **LEARN:** Adapters need independent provenance and behavioral evaluation because their small size does not limit their authority.

---

<!-- kind: resolution -->
<!-- key: builtin/08/backdoored-adapter -->
<!-- range: builtin -->
<!-- pair: 33/110 -->
<!-- pattern: adapter-backdoor -->
# Resolution · Inject behaviour via a backdoored adapter
> Defensive resolution and review gotchas for builtin · 08/backdoored-adapter
- **CONTROL:** Pin signed adapter digests, restrict loading, scan formats, evaluate targeted and safety suites, and promote the composed model as one artifact.
- **VALIDATE:** Compare a benign adapter and an unapproved digest in isolation and assert only the evaluated composition can be promoted.
- **GOTCHA:** Trust in the base model does not transfer to an adapter that can override high-impact behavior.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/08/dependency-confusion -->
<!-- range: builtin -->
<!-- pair: 34/110 -->
<!-- pattern: dependency-confusion -->
# Win dependency confusion
> builtin · 08/dependency-confusion · medium · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models win dependency confusion, focusing on its supply-deps trust boundary.
- **BOUNDARY:** A package name crosses internal and public registries where resolution priority may select an unintended publisher.
- **REVIEW:** Which registry owns the namespace? Can a public package or lookalike name outrank the intended internal dependency?
- **LEARN:** Dependency identity must bind namespace, registry, version, and digest rather than relying on the package name alone.

---

<!-- kind: resolution -->
<!-- key: builtin/08/dependency-confusion -->
<!-- range: builtin -->
<!-- pair: 34/110 -->
<!-- pattern: dependency-confusion -->
# Resolution · Win dependency confusion
> Defensive resolution and review gotchas for builtin · 08/dependency-confusion
- **CONTROL:** Use scoped private namespaces, explicit registries, lockfiles and hashes, signed provenance, and deny undeclared sources.
- **VALIDATE:** Resolve benign test packages against isolated registries and assert public, unsigned, or hash-mismatched candidates fail closed.
- **GOTCHA:** Pinning a version does not help when the same name and version can resolve from the wrong registry.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/09/metadata-ssrf -->
<!-- range: builtin -->
<!-- pair: 35/110 -->
<!-- pattern: infra -->
# SSRF to cloud metadata -> steal role credentials
> builtin · 09/metadata-ssrf · hard · 1 declared variant(s) · concept-level card
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
<!-- pattern: admin-api -->
# Abuse an unauthenticated admin inference route
> builtin · 09/open-inference-api · easy · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review how the built-in challenge models abuse an unauthenticated admin inference route, focusing on its infra-api trust boundary.
- **BOUNDARY:** A model or inference administration operation crosses from a network client into privileged runtime configuration and resources.
- **REVIEW:** Which principal may invoke each administrative operation? Is the route separated from public inference traffic and ambient workload identity?
- **LEARN:** Administrative inference routes require strong authentication, explicit authorisation, isolation, and narrow network exposure.

---

<!-- kind: resolution -->
<!-- key: builtin/09/open-inference-api -->
<!-- range: builtin -->
<!-- pair: 36/110 -->
<!-- pattern: admin-api -->
# Resolution · Abuse an unauthenticated admin inference route
> Defensive resolution and review gotchas for builtin · 09/open-inference-api
- **CONTROL:** Require authenticated workload identity, role-based action checks, private network exposure, rate limits, and complete audit records.
- **VALIDATE:** Use authorised and unauthorised synthetic principals to verify every administrative method and object denies by default.
- **GOTCHA:** A private-looking path or undocumented endpoint is not an authentication or authorisation control.
- **STATUS:** Offensive solution not verified—outside the current scope. Built-in flag verifier.

---

<!-- kind: challenge -->
<!-- key: builtin/09/registry-secrets -->
<!-- range: builtin -->
<!-- pair: 37/110 -->
<!-- pattern: secrets -->
# Recover a secret from a model card
> builtin · 09/registry-secrets · medium · 1 declared variant(s) · concept-level card
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
> builtin · 10/asset-inventory · easy · 1 declared variant(s) · concept-level card
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
> builtin · 10/trust-boundaries · medium · 1 declared variant(s) · concept-level card
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
> builtin · 10/attack-paths · hard · 1 declared variant(s) · concept-level card
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
> builtin · 11/initial-access · easy · 1 declared variant(s) · concept-level card
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
> builtin · 11/pivot-vault · hard · 1 declared variant(s) · concept-level card
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
> builtin · 11/exfil-crown-jewel · hard · 1 declared variant(s) · concept-level card
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
> dvaa · L1-01 · easy · 1 declared variant(s) · concept-level card
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
> dvaa · L1-02 · easy · 1 declared variant(s) · concept-level card
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
> dvaa · L1-03 · easy · 1 declared variant(s) · concept-level card
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
> dvaa · L2-01 · medium · 1 declared variant(s) · concept-level card
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
> dvaa · L2-02 · medium · 1 declared variant(s) · concept-level card
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
<!-- pattern: path -->
# MCP Path Traversal
> dvaa · L2-03 · medium · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the MCP Path Traversal scenario as implemented by OpenA2A, focusing on its mcp-exploitation boundary.
- **BOUNDARY:** An untrusted path or URI crosses into filesystem resolution outside an authorised root.
- **REVIEW:** What is the canonical allowed root? Can decoding, symlinks, alternate separators, or races change the resolved target?
- **LEARN:** Access decisions must use the final canonical target and remain safe across encoding, absolute paths, and symbolic links.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-03 -->
<!-- range: dvaa -->
<!-- pair: 49/110 -->
<!-- pattern: path -->
# Resolution · MCP Path Traversal
> Defensive resolution and review gotchas for dvaa · L2-03
- **CONTROL:** Resolve paths safely, reject absolute and escaping targets, enforce containment after canonicalisation, and run with minimal filesystem access.
- **VALIDATE:** Use temporary in-root and out-of-root fixtures with encoded, absolute, separator, and symlink cases and assert fail-closed behavior.
- **GOTCHA:** String-prefix checks can approve sibling paths or links whose final target lies outside the intended root.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-04 -->
<!-- range: dvaa -->
<!-- pair: 50/110 -->
<!-- pattern: prompt -->
# Persistent Memory Injection
> dvaa · L2-04 · medium · 1 declared variant(s) · concept-level card
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
> dvaa · L2-05 · medium · 1 declared variant(s) · concept-level card
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
> dvaa · L2-06 · medium · 1 declared variant(s) · concept-level card
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
> dvaa · L2-07 · medium · 1 declared variant(s) · concept-level card
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
<!-- pattern: tool-registration -->
# Malicious Tool Registration
> dvaa · L2-08 · medium · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Malicious Tool Registration scenario as implemented by OpenA2A, focusing on its tool-registry-poisoning boundary.
- **BOUNDARY:** A tool manifest crosses from an external registry or publisher into the trusted capability catalog.
- **REVIEW:** Which registry and publisher identity are trusted? Are manifest signatures, source revisions, and requested capabilities verified before approval?
- **LEARN:** Registration is a software provenance decision: only authenticated publishers and reviewed, immutable tool definitions may become callable.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-08 -->
<!-- range: dvaa -->
<!-- pair: 54/110 -->
<!-- pattern: tool-registration -->
# Resolution · Malicious Tool Registration
> Defensive resolution and review gotchas for dvaa · L2-08
- **CONTROL:** Use approved registries, signed manifests, verified publisher identities, pinned source revisions, capability review, and an explicit tool allow-list.
- **VALIDATE:** Submit benign signed, unsigned, altered, and unapproved manifests and assert that only the approved identity and exact digest can register.
- **GOTCHA:** Schema-valid metadata can still describe an untrusted implementation; validation does not establish publisher or source authenticity.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L2-09 -->
<!-- range: dvaa -->
<!-- pair: 55/110 -->
<!-- pattern: tool-mitm -->
# Tool Call MITM
> dvaa · L2-09 · medium · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Tool Call MITM scenario as implemented by OpenA2A, focusing on its tool-mitm boundary.
- **BOUNDARY:** Tool calls and results cross a network or intermediary that could replace the server, request, or response.
- **REVIEW:** How is the server authenticated? Are request identity, response identity, integrity, freshness, and channel binding verified?
- **LEARN:** The host must authenticate the tool endpoint and bind each response to the intended request and server identity.

---

<!-- kind: resolution -->
<!-- key: dvaa/L2-09 -->
<!-- range: dvaa -->
<!-- pair: 55/110 -->
<!-- pattern: tool-mitm -->
# Resolution · Tool Call MITM
> Defensive resolution and review gotchas for dvaa · L2-09
- **CONTROL:** Use authenticated encrypted transport, pinned service identity where appropriate, request-response correlation, replay protection, and integrity checks.
- **VALIDATE:** Use a benign test endpoint with the wrong identity or correlation value and assert the host rejects its responses.
- **GOTCHA:** TLS without correct hostname, trust-store, redirect, and response binding checks can still connect to the wrong tool.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-01 -->
<!-- range: dvaa -->
<!-- pair: 56/110 -->
<!-- pattern: prompt -->
# Chained Prompt Injection
> dvaa · L3-01 · hard · 1 declared variant(s) · concept-level card
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
> dvaa · L3-02 · hard · 1 declared variant(s) · concept-level card
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
> dvaa · L3-03 · hard · 1 declared variant(s) · concept-level card
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
<!-- pattern: secrets -->
# System Prompt Extraction via Context Pressure
> dvaa · L3-04 · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the System Prompt Extraction via Context Pressure scenario as implemented by OpenA2A, focusing on its context-overflow boundary.
- **BOUNDARY:** Sensitive configuration or identity data crosses into a response, log, completion, or model context.
- **REVIEW:** Where is sensitive data introduced? Which output, error, metadata, or completion path can reveal it?
- **LEARN:** Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-04 -->
<!-- range: dvaa -->
<!-- pair: 59/110 -->
<!-- pattern: secrets -->
# Resolution · System Prompt Extraction via Context Pressure
> Defensive resolution and review gotchas for dvaa · L3-04
- **CONTROL:** Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.
- **VALIDATE:** Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.
- **GOTCHA:** Masking the final response is insufficient when the same value remains available through debug or metadata paths.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-05 -->
<!-- range: dvaa -->
<!-- pair: 60/110 -->
<!-- pattern: tool-shadowing -->
# Tool Typosquatting
> dvaa · L3-05 · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Tool Typosquatting scenario as implemented by OpenA2A, focusing on its tool-registry-poisoning boundary.
- **BOUNDARY:** A tool name or namespace crosses from discovery into registry resolution and invocation.
- **REVIEW:** What cryptographic identity owns this tool? Can another registry entry, namespace, or later definition win resolution?
- **LEARN:** Human-readable names are not stable identities; resolution must bind approval to one authenticated implementation.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-05 -->
<!-- range: dvaa -->
<!-- pair: 60/110 -->
<!-- pattern: tool-shadowing -->
# Resolution · Tool Typosquatting
> Defensive resolution and review gotchas for dvaa · L3-05
- **CONTROL:** Use an immutable registry, signed and version-pinned definitions, unique namespaces, and approval bound to the server and definition digest.
- **VALIDATE:** Register benign lookalike and duplicate names and assert that ambiguous, unsigned, or changed identities fail closed.
- **GOTCHA:** Name allow-lists still fail when resolution can select a different implementation with the same or similar name.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-06 -->
<!-- range: dvaa -->
<!-- pair: 61/110 -->
<!-- pattern: tool-dataflow -->
# Tool Chain Data Exfiltration
> dvaa · L3-06 · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Tool Chain Data Exfiltration scenario as implemented by OpenA2A, focusing on its tool-registry-poisoning boundary.
- **BOUNDARY:** Sensitive data crosses several individually authorised tool calls before reaching a new destination.
- **REVIEW:** Which earlier result becomes a later argument? Is the final destination permitted for that data classification?
- **LEARN:** Authorisation must follow provenance and data flow across the whole tool chain, not only each isolated call.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-06 -->
<!-- range: dvaa -->
<!-- pair: 61/110 -->
<!-- pattern: tool-dataflow -->
# Resolution · Tool Chain Data Exfiltration
> Defensive resolution and review gotchas for dvaa · L3-06
- **CONTROL:** Track taint and provenance across calls, apply destination-aware policy, minimise returned data, and require confirmation for cross-domain transfer.
- **VALIDATE:** Use synthetic labelled values to verify that allowed local processing cannot be composed into an unauthorised transfer.
- **GOTCHA:** Every call can look legitimate in isolation while their composition violates the original data-use purpose.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-07 -->
<!-- range: dvaa -->
<!-- pair: 62/110 -->
<!-- pattern: tool-shadowing -->
# Tool Shadowing
> dvaa · L3-07 · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Tool Shadowing scenario as implemented by OpenA2A, focusing on its tool-mitm boundary.
- **BOUNDARY:** A tool name or namespace crosses from discovery into registry resolution and invocation.
- **REVIEW:** What cryptographic identity owns this tool? Can another registry entry, namespace, or later definition win resolution?
- **LEARN:** Human-readable names are not stable identities; resolution must bind approval to one authenticated implementation.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-07 -->
<!-- range: dvaa -->
<!-- pair: 62/110 -->
<!-- pattern: tool-shadowing -->
# Resolution · Tool Shadowing
> Defensive resolution and review gotchas for dvaa · L3-07
- **CONTROL:** Use an immutable registry, signed and version-pinned definitions, unique namespaces, and approval bound to the server and definition digest.
- **VALIDATE:** Register benign lookalike and duplicate names and assert that ambiguous, unsigned, or changed identities fail closed.
- **GOTCHA:** Name allow-lists still fail when resolution can select a different implementation with the same or similar name.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L3-08 -->
<!-- range: dvaa -->
<!-- pair: 63/110 -->
<!-- pattern: tool-redirect -->
# Traffic Redirection Attack
> dvaa · L3-08 · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Traffic Redirection Attack scenario as implemented by OpenA2A, focusing on its tool-mitm boundary.
- **BOUNDARY:** A configured tool endpoint crosses DNS, redirect, proxy, and routing boundaries before reaching the final service.
- **REVIEW:** Which redirects and resolved addresses are allowed? Does authentication bind to the final destination after DNS and proxy routing?
- **LEARN:** Every hop and resolved destination must remain within the approved endpoint policy and authenticated service identity.

---

<!-- kind: resolution -->
<!-- key: dvaa/L3-08 -->
<!-- range: dvaa -->
<!-- pair: 63/110 -->
<!-- pattern: tool-redirect -->
# Resolution · Traffic Redirection Attack
> Defensive resolution and review gotchas for dvaa · L3-08
- **CONTROL:** Pin approved schemes and hosts, restrict redirects, validate resolved addresses, authenticate the final service, and re-check policy on every hop.
- **VALIDATE:** Use inert redirect and alternate-resolution fixtures and assert the client refuses destinations outside the approved set.
- **GOTCHA:** Validating only the original URL misses a later redirect or resolution to a different trust zone.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvaa/L4-01 -->
<!-- range: dvaa -->
<!-- pair: 64/110 -->
<!-- pattern: chain -->
# Compromise SecureBot
> dvaa · L4-01 · expert · 1 declared variant(s) · concept-level card
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
<!-- pattern: chain -->
# Agent-to-Agent Attack Chain
> dvaa · L4-02 · expert · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Agent-to-Agent Attack Chain scenario as implemented by OpenA2A, focusing on its agent-to-agent boundary.
- **BOUNDARY:** Several individually limited weaknesses compose across content, identity, tools, data, and infrastructure.
- **REVIEW:** Which earlier weakness enables the next step? Which control breaks the chain earliest and most reliably?
- **LEARN:** Security review must follow end-to-end authority and data flow because local controls can fail in composition.

---

<!-- kind: resolution -->
<!-- key: dvaa/L4-02 -->
<!-- range: dvaa -->
<!-- pair: 65/110 -->
<!-- pattern: chain -->
# Resolution · Agent-to-Agent Attack Chain
> Defensive resolution and review gotchas for dvaa · L4-02
- **CONTROL:** Use layered controls, trace provenance, minimise ambient authority, segment systems, and retain cross-service evidence.
- **VALIDATE:** Validate each boundary independently with safe fixtures, then review the composed data flow without executing an attack chain.
- **GOTCHA:** A control may stop one step while leaving another route to the same privileged effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/A1 -->
<!-- range: mcpgoat -->
<!-- pair: 66/110 -->
<!-- pattern: tool-poisoning -->
# Tool Poisoning
> mcpgoat · A1 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Tool Poisoning scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** Tool descriptions and results cross from a server-controlled metadata plane into model planning and user approval.
- **REVIEW:** Which metadata reaches the model or approval UI? Does execution use the same reviewed, authenticated definition?
- **LEARN:** Tool metadata is untrusted content and must not silently grant authority or inject instructions.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/A1 -->
<!-- range: mcpgoat -->
<!-- pair: 66/110 -->
<!-- pattern: tool-poisoning -->
# Resolution · Tool Poisoning
> Defensive resolution and review gotchas for mcpgoat · A1
- **CONTROL:** Authenticate servers, sanitise and canonicalise metadata, show security-relevant fields, and authorise every call outside the description.
- **VALIDATE:** Use benign instruction-like metadata to confirm it remains visible as data and cannot broaden a tool's permitted effect.
- **GOTCHA:** A harmless tool name can conceal instructions in descriptions, annotations, or returned content.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/A2 -->
<!-- range: mcpgoat -->
<!-- pair: 67/110 -->
<!-- pattern: tool-shadowing -->
# Tool Shadowing / Trusted-Tool Override
> mcpgoat · A2 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Tool Shadowing / Trusted-Tool Override scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** A tool name or namespace crosses from discovery into registry resolution and invocation.
- **REVIEW:** What cryptographic identity owns this tool? Can another registry entry, namespace, or later definition win resolution?
- **LEARN:** Human-readable names are not stable identities; resolution must bind approval to one authenticated implementation.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/A2 -->
<!-- range: mcpgoat -->
<!-- pair: 67/110 -->
<!-- pattern: tool-shadowing -->
# Resolution · Tool Shadowing / Trusted-Tool Override
> Defensive resolution and review gotchas for mcpgoat · A2
- **CONTROL:** Use an immutable registry, signed and version-pinned definitions, unique namespaces, and approval bound to the server and definition digest.
- **VALIDATE:** Register benign lookalike and duplicate names and assert that ambiguous, unsigned, or changed identities fail closed.
- **GOTCHA:** Name allow-lists still fail when resolution can select a different implementation with the same or similar name.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/A3 -->
<!-- range: mcpgoat -->
<!-- pair: 68/110 -->
<!-- pattern: rug-pull -->
# Rug Pull / Tool Mutation (TOCTOU)
> mcpgoat · A3 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Rug Pull / Tool Mutation (TOCTOU) scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** A previously reviewed tool definition changes between approval, discovery, and execution.
- **REVIEW:** Which digest was approved? What forces re-review when the definition or server identity changes?
- **LEARN:** Approval applies to an immutable definition digest and must be invalidated when security-relevant metadata or behavior changes.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/A3 -->
<!-- range: mcpgoat -->
<!-- pair: 68/110 -->
<!-- pattern: rug-pull -->
# Resolution · Rug Pull / Tool Mutation (TOCTOU)
> Defensive resolution and review gotchas for mcpgoat · A3
- **CONTROL:** Pin signed definitions, compare canonical digests before every call, cache immutably, and require re-approval for any change.
- **VALIDATE:** Use two benign versions of one tool and assert that the second cannot run under approval granted to the first.
- **GOTCHA:** Periodic refresh without digest-bound approval creates a time-of-check/time-of-use gap.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/B1 -->
<!-- range: mcpgoat -->
<!-- pair: 69/110 -->
<!-- pattern: prompt -->
# Indirect Prompt Injection via Tool Output
> mcpgoat · B1 · tiered · 3 declared variant(s) · concept-level card
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
<!-- pattern: command -->
# Command Injection (RCE)
> mcpgoat · D1 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Command Injection (RCE) scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted arguments cross into a shell, interpreter, dynamic loader, or operating-system process boundary.
- **REVIEW:** Is a shell or evaluator involved? Are executable identity and every argument fixed or independently allow-listed?
- **LEARN:** Data must remain structured arguments and must never become executable command syntax.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D1 -->
<!-- range: mcpgoat -->
<!-- pair: 70/110 -->
<!-- pattern: command -->
# Resolution · Command Injection (RCE)
> Defensive resolution and review gotchas for mcpgoat · D1
- **CONTROL:** Remove shell evaluation, call fixed executables with argument arrays, validate typed values, drop privileges, and sandbox the process.
- **VALIDATE:** Use harmless metacharacter and unexpected-argument fixtures and assert they are rejected or passed literally without side effects.
- **GOTCHA:** Escaping for one shell or platform is fragile; avoiding the interpreter is the durable control.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D2 -->
<!-- range: mcpgoat -->
<!-- pair: 71/110 -->
<!-- pattern: path -->
# Path Traversal / Arbitrary File Read
> mcpgoat · D2 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Path Traversal / Arbitrary File Read scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** An untrusted path or URI crosses into filesystem resolution outside an authorised root.
- **REVIEW:** What is the canonical allowed root? Can decoding, symlinks, alternate separators, or races change the resolved target?
- **LEARN:** Access decisions must use the final canonical target and remain safe across encoding, absolute paths, and symbolic links.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D2 -->
<!-- range: mcpgoat -->
<!-- pair: 71/110 -->
<!-- pattern: path -->
# Resolution · Path Traversal / Arbitrary File Read
> Defensive resolution and review gotchas for mcpgoat · D2
- **CONTROL:** Resolve paths safely, reject absolute and escaping targets, enforce containment after canonicalisation, and run with minimal filesystem access.
- **VALIDATE:** Use temporary in-root and out-of-root fixtures with encoded, absolute, separator, and symlink cases and assert fail-closed behavior.
- **GOTCHA:** String-prefix checks can approve sibling paths or links whose final target lies outside the intended root.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D3 -->
<!-- range: mcpgoat -->
<!-- pair: 72/110 -->
<!-- pattern: infra -->
# Server-Side Request Forgery
> mcpgoat · D3 · tiered · 3 declared variant(s) · concept-level card
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
<!-- pattern: sql -->
# SQL Injection
> mcpgoat · D4 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the SQL Injection scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted values cross into relational query structure and database privileges.
- **REVIEW:** Which query elements are parameterised? Does the database account have only the permissions required by this operation?
- **LEARN:** Queries must keep code and data separate, including identifiers, sorting, and dynamically selected clauses.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D4 -->
<!-- range: mcpgoat -->
<!-- pair: 73/110 -->
<!-- pattern: sql -->
# Resolution · SQL Injection
> Defensive resolution and review gotchas for mcpgoat · D4
- **CONTROL:** Use parameterised queries, allow-list non-parameterisable identifiers, constrain result size, and grant least-privilege database roles.
- **VALIDATE:** Use inert quote, wildcard, comment, and type-mismatch fixtures and assert query shape and authorised results remain unchanged.
- **GOTCHA:** Parameters protect values but do not make attacker-selected table names, operators, or sort clauses safe.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/C2 -->
<!-- range: mcpgoat -->
<!-- pair: 74/110 -->
<!-- pattern: identity -->
# Broken Authorization / Confused Deputy
> mcpgoat · C2 · tiered · 3 declared variant(s) · concept-level card
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
> mcpgoat · C3 · tiered · 3 declared variant(s) · concept-level card
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
> mcpgoat · E1 · tiered · 3 declared variant(s) · concept-level card
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
<!-- pattern: unicode -->
# Invisible-Text Tool Poisoning
> mcpgoat · A9 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Invisible-Text Tool Poisoning scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** Unicode formatting and confusable characters cross from raw metadata into scanning, display, and model-visible text.
- **REVIEW:** Which normalization form is enforced? Are bidirectional controls, zero-width characters, and confusables exposed to reviewers?
- **LEARN:** Security review and execution must use one canonical representation while preserving warnings about concealed characters.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/A9 -->
<!-- range: mcpgoat -->
<!-- pair: 77/110 -->
<!-- pattern: unicode -->
# Resolution · Invisible-Text Tool Poisoning
> Defensive resolution and review gotchas for mcpgoat · A9
- **CONTROL:** Normalize consistently, reject or visibly escape control characters, detect confusables, and scan the same canonical text shown to users.
- **VALIDATE:** Use harmless strings containing bidi, zero-width, and confusable characters and assert identical scanner and display decisions.
- **GOTCHA:** Stripping a subset of invisible characters can create a second, differently interpreted representation.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/B2 -->
<!-- range: mcpgoat -->
<!-- pair: 78/110 -->
<!-- pattern: prompt -->
# Indirect Injection via Resource Content
> mcpgoat · B2 · tiered · 3 declared variant(s) · concept-level card
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
> mcpgoat · B3 · tiered · 3 declared variant(s) · concept-level card
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
<!-- pattern: sampling -->
# Sampling Abuse (server-driven LLM calls)
> mcpgoat · B5 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Sampling Abuse (server-driven LLM calls) scenario as implemented by Sabyasachi Dhal, focusing on its MCP-specific boundary.
- **BOUNDARY:** A server-requested model call crosses back into host context, credentials, tokens, and compute budgets.
- **REVIEW:** Which context is shared with the sampled model? Who authorises the purpose, model, token budget, and returned destination?
- **LEARN:** Sampling is a privileged host action that needs explicit purpose, context minimisation, consent, and resource limits.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/B5 -->
<!-- range: mcpgoat -->
<!-- pair: 80/110 -->
<!-- pattern: sampling -->
# Resolution · Sampling Abuse (server-driven LLM calls)
> Defensive resolution and review gotchas for mcpgoat · B5
- **CONTROL:** Require informed consent, minimise context, isolate credentials, allow-list models and purposes, cap tokens and cost, and audit results.
- **VALIDATE:** Use synthetic host context and bounded budgets to confirm an untrusted server cannot expand context or repeat calls silently.
- **GOTCHA:** Approving the parent tool call does not automatically approve every server-initiated model call it requests.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/C4 -->
<!-- range: mcpgoat -->
<!-- pair: 81/110 -->
<!-- pattern: oauth-audience -->
# OAuth Token-Audience Confusion
> mcpgoat · C4 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the OAuth Token-Audience Confusion scenario as implemented by Sabyasachi Dhal, focusing on its AuthN/AuthZ boundary.
- **BOUNDARY:** An OAuth token crosses from its intended resource server or client into a different audience or delegated action.
- **REVIEW:** Which exact resource audience issued the token? Are scope and delegated subject valid for this tool and action?
- **LEARN:** Token validity is insufficient unless issuer, audience, scope, client, subject, and delegation all match the requested operation.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/C4 -->
<!-- range: mcpgoat -->
<!-- pair: 81/110 -->
<!-- pattern: oauth-audience -->
# Resolution · OAuth Token-Audience Confusion
> Defensive resolution and review gotchas for mcpgoat · C4
- **CONTROL:** Validate issuer and exact audience, use resource-specific tokens, restrict scopes, bind delegation, and reject token forwarding across services.
- **VALIDATE:** Use synthetic tokens with correct signatures but wrong audiences, clients, scopes, or subjects and assert rejection.
- **GOTCHA:** A token accepted by one service must not become a bearer credential for every service in the agent chain.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D6 -->
<!-- range: mcpgoat -->
<!-- pair: 82/110 -->
<!-- pattern: template -->
# Server-Side Template Injection
> mcpgoat · D6 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Server-Side Template Injection scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted text crosses into template source, expressions, object traversal, or server-side helpers.
- **REVIEW:** Can input become template source or an expression? Which objects, filters, and helpers are reachable during rendering?
- **LEARN:** Users may supply data for a fixed template but must not define executable template structure.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D6 -->
<!-- range: mcpgoat -->
<!-- pair: 82/110 -->
<!-- pattern: template -->
# Resolution · Server-Side Template Injection
> Defensive resolution and review gotchas for mcpgoat · D6
- **CONTROL:** Use fixed logic-light templates, pass typed data, enable sandboxing and autoescape, and remove dangerous helpers and object access.
- **VALIDATE:** Render harmless expression-like fixtures and assert they remain literal text with no object access or evaluation.
- **GOTCHA:** Output escaping prevents markup injection but does not stop server-side expression evaluation.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/F1 -->
<!-- range: mcpgoat -->
<!-- pair: 83/110 -->
<!-- pattern: dns-rebinding -->
# DNS Rebinding / Missing Origin Validation
> mcpgoat · F1 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the DNS Rebinding / Missing Origin Validation scenario as implemented by Sabyasachi Dhal, focusing on its Transport boundary.
- **BOUNDARY:** A hostname crosses browser-origin and DNS resolution boundaries and may resolve to a different address over time.
- **REVIEW:** Is the Origin validated exactly? Are all resolved addresses checked at connection time and after DNS changes?
- **LEARN:** Origin checks and destination policy must bind to stable identities and validate every resolved connection target.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/F1 -->
<!-- range: mcpgoat -->
<!-- pair: 83/110 -->
<!-- pattern: dns-rebinding -->
# Resolution · DNS Rebinding / Missing Origin Validation
> Defensive resolution and review gotchas for mcpgoat · F1
- **CONTROL:** Require exact origins, re-resolve and validate destination addresses, reject private or disallowed ranges, and avoid trusting hostname strings alone.
- **VALIDATE:** Use controlled DNS fixtures that change between safe addresses and assert disallowed resolutions never receive a connection.
- **GOTCHA:** A hostname that was safe during validation can resolve differently when the connection is opened.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/F2 -->
<!-- range: mcpgoat -->
<!-- pair: 84/110 -->
<!-- pattern: cors -->
# CORS Misconfiguration
> mcpgoat · F2 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the CORS Misconfiguration scenario as implemented by Sabyasachi Dhal, focusing on its Transport boundary.
- **BOUNDARY:** Browser credentials and responses cross from an MCP HTTP service into a requesting web origin.
- **REVIEW:** Which exact origins need access? Are credentials, preflight methods, headers, and cached decisions constrained consistently?
- **LEARN:** Cross-origin access must use a narrow exact allow-list and must never reflect arbitrary origins with credentials.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/F2 -->
<!-- range: mcpgoat -->
<!-- pair: 84/110 -->
<!-- pattern: cors -->
# Resolution · CORS Misconfiguration
> Defensive resolution and review gotchas for mcpgoat · F2
- **CONTROL:** Allow-list exact HTTPS origins, minimise methods and headers, vary caches by Origin, and disable credentials unless strictly required.
- **VALIDATE:** Send harmless preflights from allowed, sibling, null, and attacker-controlled origins and assert only the exact policy succeeds.
- **GOTCHA:** Wildcard subdomains and reflected origins can turn an apparently narrow policy into credentialed cross-origin access.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/C6 -->
<!-- range: mcpgoat -->
<!-- pair: 85/110 -->
<!-- pattern: session-security -->
# Predictable Session IDs (hijack)
> mcpgoat · C6 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Predictable Session IDs (hijack) scenario as implemented by Sabyasachi Dhal, focusing on its Transport boundary.
- **BOUNDARY:** A session identifier crosses clients, requests, reconnects, and server-side state ownership boundaries.
- **REVIEW:** How much entropy and lifetime does the identifier have? Can another principal replay, fix, or reuse it across connections?
- **LEARN:** Session identifiers must be unpredictable, confidential, short-lived, and bound to the authenticated principal and channel context.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/C6 -->
<!-- range: mcpgoat -->
<!-- pair: 85/110 -->
<!-- pattern: session-security -->
# Resolution · Predictable Session IDs (hijack)
> Defensive resolution and review gotchas for mcpgoat · C6
- **CONTROL:** Use cryptographic random identifiers, rotate on authentication changes, bind ownership server-side, expire promptly, and protect transport and storage.
- **VALIDATE:** Create multiple synthetic sessions and test replay, cross-user reuse, fixation, expiry, and logout invalidation.
- **GOTCHA:** A random-looking identifier still fails if it remains valid across users, privilege changes, or excessive time.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/G1 -->
<!-- range: mcpgoat -->
<!-- pair: 86/110 -->
<!-- pattern: dos -->
# Unbounded Consumption (cost/DoS)
> mcpgoat · G1 · tiered · 3 declared variant(s) · concept-level card
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
<!-- pattern: redos -->
# Regular-Expression DoS (ReDoS)
> mcpgoat · G4 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Regular-Expression DoS (ReDoS) scenario as implemented by Sabyasachi Dhal, focusing on its DoS/Cost boundary.
- **BOUNDARY:** Attacker-controlled text crosses into a regular-expression engine whose backtracking cost can grow nonlinearly.
- **REVIEW:** Can the pattern exhibit catastrophic backtracking? What input, time, and concurrency limits bound each match?
- **LEARN:** Pattern safety and bounded input must be established before regex matching occurs on a shared service thread.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/G4 -->
<!-- range: mcpgoat -->
<!-- pair: 87/110 -->
<!-- pattern: redos -->
# Resolution · Regular-Expression DoS (ReDoS)
> Defensive resolution and review gotchas for mcpgoat · G4
- **CONTROL:** Use linear-time patterns or engines, simplify ambiguous repetition, cap input length, set timeouts, and isolate expensive matching.
- **VALIDATE:** Run bounded synthetic worst-case strings in a timeout-controlled test and assert predictable rejection and latency.
- **GOTCHA:** A request rate limit does not prevent one accepted input from monopolising a worker for an excessive duration.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D5 -->
<!-- range: mcpgoat -->
<!-- pair: 88/110 -->
<!-- pattern: nosql -->
# NoSQL Injection
> mcpgoat · D5 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the NoSQL Injection scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted JSON or object fields cross into NoSQL operators, selectors, projections, or update structure.
- **REVIEW:** Which keys and value types are accepted? Can nested operator keys or type confusion alter selector meaning?
- **LEARN:** Application data must not be interpreted as query operators or prototype-bearing objects.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D5 -->
<!-- range: mcpgoat -->
<!-- pair: 88/110 -->
<!-- pattern: nosql -->
# Resolution · NoSQL Injection
> Defensive resolution and review gotchas for mcpgoat · D5
- **CONTROL:** Validate against a closed schema, construct queries from typed fields, reject operator-prefixed keys, and use least-privilege data access.
- **VALIDATE:** Use benign nested objects, arrays, unexpected types, and operator-like keys and assert the query builder rejects them.
- **GOTCHA:** Escaping strings does not help when the dangerous input is a structured operator object.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D7 -->
<!-- range: mcpgoat -->
<!-- pair: 89/110 -->
<!-- pattern: xml -->
# XML External Entity (XXE)
> mcpgoat · D7 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the XML External Entity (XXE) scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted XML crosses into entity resolution, DTD processing, XInclude, and parser-controlled network or file access.
- **REVIEW:** Are DTDs and external entities disabled? Can the parser access files, networks, schemas, or includes?
- **LEARN:** XML features that resolve external content must be disabled before parsing untrusted documents.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D7 -->
<!-- range: mcpgoat -->
<!-- pair: 89/110 -->
<!-- pattern: xml -->
# Resolution · XML External Entity (XXE)
> Defensive resolution and review gotchas for mcpgoat · D7
- **CONTROL:** Use a hardened parser with DTDs, external entities, XInclude, and network access disabled; enforce size and depth limits.
- **VALIDATE:** Parse inert documents containing disabled declarations and oversized nesting and assert deterministic rejection without I/O.
- **GOTCHA:** Blocking one entity syntax is insufficient when schemas, parameter entities, or includes still resolve externally.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/D8 -->
<!-- range: mcpgoat -->
<!-- pair: 90/110 -->
<!-- pattern: deserialization -->
# Insecure Deserialization (prototype pollution)
> mcpgoat · D8 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Insecure Deserialization (prototype pollution) scenario as implemented by Sabyasachi Dhal, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted serialized objects cross into constructors, prototypes, type hooks, or recursive merge logic.
- **REVIEW:** Which types and hooks can be instantiated? Can special keys or merge behavior alter prototypes or application defaults?
- **LEARN:** Deserialization must produce schema-validated data objects without executable types or prototype mutation.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/D8 -->
<!-- range: mcpgoat -->
<!-- pair: 90/110 -->
<!-- pattern: deserialization -->
# Resolution · Insecure Deserialization (prototype pollution)
> Defensive resolution and review gotchas for mcpgoat · D8
- **CONTROL:** Prefer plain data formats, validate a closed schema, reject dangerous keys and polymorphic types, and avoid recursive merges into prototypes.
- **VALIDATE:** Use inert unexpected types, deep objects, and prototype-like keys and assert the parser returns isolated plain data or rejects them.
- **GOTCHA:** A trusted transport does not make attacker-controlled object graphs or type metadata safe to instantiate.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: mcpgoat/H1 -->
<!-- range: mcpgoat -->
<!-- pair: 91/110 -->
<!-- pattern: dependency-confusion -->
# Supply Chain (typosquat / unsigned package)
> mcpgoat · H1 · tiered · 3 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Supply Chain (typosquat / unsigned package) scenario as implemented by Sabyasachi Dhal, focusing on its Supply chain boundary.
- **BOUNDARY:** A package name crosses internal and public registries where resolution priority may select an unintended publisher.
- **REVIEW:** Which registry owns the namespace? Can a public package or lookalike name outrank the intended internal dependency?
- **LEARN:** Dependency identity must bind namespace, registry, version, and digest rather than relying on the package name alone.

---

<!-- kind: resolution -->
<!-- key: mcpgoat/H1 -->
<!-- range: mcpgoat -->
<!-- pair: 91/110 -->
<!-- pattern: dependency-confusion -->
# Resolution · Supply Chain (typosquat / unsigned package)
> Defensive resolution and review gotchas for mcpgoat · H1
- **CONTROL:** Use scoped private namespaces, explicit registries, lockfiles and hashes, signed provenance, and deny undeclared sources.
- **VALIDATE:** Resolve benign test packages against isolated registries and assert public, unsigned, or hash-mismatched candidates fail closed.
- **GOTCHA:** Pinning a version does not help when the same name and version can resolve from the wrong registry.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/01 -->
<!-- range: dvmcp -->
<!-- pair: 92/110 -->
<!-- pattern: prompt -->
# Basic Prompt Injection
> dvmcp · 01 · easy · 1 declared variant(s) · concept-level card
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
<!-- pattern: tool-poisoning -->
# Tool Poisoning
> dvmcp · 02 · easy · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Tool Poisoning scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its MCP-specific boundary.
- **BOUNDARY:** Tool descriptions and results cross from a server-controlled metadata plane into model planning and user approval.
- **REVIEW:** Which metadata reaches the model or approval UI? Does execution use the same reviewed, authenticated definition?
- **LEARN:** Tool metadata is untrusted content and must not silently grant authority or inject instructions.

---

<!-- kind: resolution -->
<!-- key: dvmcp/02 -->
<!-- range: dvmcp -->
<!-- pair: 93/110 -->
<!-- pattern: tool-poisoning -->
# Resolution · Tool Poisoning
> Defensive resolution and review gotchas for dvmcp · 02
- **CONTROL:** Authenticate servers, sanitise and canonicalise metadata, show security-relevant fields, and authorise every call outside the description.
- **VALIDATE:** Use benign instruction-like metadata to confirm it remains visible as data and cannot broaden a tool's permitted effect.
- **GOTCHA:** A harmless tool name can conceal instructions in descriptions, annotations, or returned content.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/03 -->
<!-- range: dvmcp -->
<!-- pair: 94/110 -->
<!-- pattern: scope -->
# Excessive Permission Scope
> dvmcp · 03 · easy · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Excessive Permission Scope scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its AuthN/AuthZ boundary.
- **BOUNDARY:** A client-declared root, permission, or resource scope crosses into server-side access control.
- **REVIEW:** Who defines and enforces the allowed scope? Is the resource canonicalised before containment and permission checks?
- **LEARN:** Servers must enforce the intersection of declared scope, authenticated identity, and canonical resource location.

---

<!-- kind: resolution -->
<!-- key: dvmcp/03 -->
<!-- range: dvmcp -->
<!-- pair: 94/110 -->
<!-- pattern: scope -->
# Resolution · Excessive Permission Scope
> Defensive resolution and review gotchas for dvmcp · 03
- **CONTROL:** Enforce scopes server-side, canonicalise resource identifiers, deny ambient access, and apply least privilege to the host process.
- **VALIDATE:** Use synthetic in-scope and out-of-scope resources, including encoded and absolute forms, to confirm containment fails closed.
- **GOTCHA:** Advertising a root or permission to the model does not enforce it at the filesystem or service boundary.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/04 -->
<!-- range: dvmcp -->
<!-- pair: 95/110 -->
<!-- pattern: rug-pull -->
# Rug Pull Attack
> dvmcp · 04 · medium · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Rug Pull Attack scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its MCP-specific boundary.
- **BOUNDARY:** A previously reviewed tool definition changes between approval, discovery, and execution.
- **REVIEW:** Which digest was approved? What forces re-review when the definition or server identity changes?
- **LEARN:** Approval applies to an immutable definition digest and must be invalidated when security-relevant metadata or behavior changes.

---

<!-- kind: resolution -->
<!-- key: dvmcp/04 -->
<!-- range: dvmcp -->
<!-- pair: 95/110 -->
<!-- pattern: rug-pull -->
# Resolution · Rug Pull Attack
> Defensive resolution and review gotchas for dvmcp · 04
- **CONTROL:** Pin signed definitions, compare canonical digests before every call, cache immutably, and require re-approval for any change.
- **VALIDATE:** Use two benign versions of one tool and assert that the second cannot run under approval granted to the first.
- **GOTCHA:** Periodic refresh without digest-bound approval creates a time-of-check/time-of-use gap.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/05 -->
<!-- range: dvmcp -->
<!-- pair: 96/110 -->
<!-- pattern: tool-shadowing -->
# Tool Shadowing
> dvmcp · 05 · medium · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Tool Shadowing scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its MCP-specific boundary.
- **BOUNDARY:** A tool name or namespace crosses from discovery into registry resolution and invocation.
- **REVIEW:** What cryptographic identity owns this tool? Can another registry entry, namespace, or later definition win resolution?
- **LEARN:** Human-readable names are not stable identities; resolution must bind approval to one authenticated implementation.

---

<!-- kind: resolution -->
<!-- key: dvmcp/05 -->
<!-- range: dvmcp -->
<!-- pair: 96/110 -->
<!-- pattern: tool-shadowing -->
# Resolution · Tool Shadowing
> Defensive resolution and review gotchas for dvmcp · 05
- **CONTROL:** Use an immutable registry, signed and version-pinned definitions, unique namespaces, and approval bound to the server and definition digest.
- **VALIDATE:** Register benign lookalike and duplicate names and assert that ambiguous, unsigned, or changed identities fail closed.
- **GOTCHA:** Name allow-lists still fail when resolution can select a different implementation with the same or similar name.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/06 -->
<!-- range: dvmcp -->
<!-- pair: 97/110 -->
<!-- pattern: prompt -->
# Indirect Prompt Injection
> dvmcp · 06 · medium · 1 declared variant(s) · concept-level card
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
> dvmcp · 07 · medium · 1 declared variant(s) · concept-level card
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
<!-- pattern: command -->
# Malicious Code Execution
> dvmcp · 08 · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Malicious Code Execution scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted arguments cross into a shell, interpreter, dynamic loader, or operating-system process boundary.
- **REVIEW:** Is a shell or evaluator involved? Are executable identity and every argument fixed or independently allow-listed?
- **LEARN:** Data must remain structured arguments and must never become executable command syntax.

---

<!-- kind: resolution -->
<!-- key: dvmcp/08 -->
<!-- range: dvmcp -->
<!-- pair: 99/110 -->
<!-- pattern: command -->
# Resolution · Malicious Code Execution
> Defensive resolution and review gotchas for dvmcp · 08
- **CONTROL:** Remove shell evaluation, call fixed executables with argument arrays, validate typed values, drop privileges, and sandbox the process.
- **VALIDATE:** Use harmless metacharacter and unexpected-argument fixtures and assert they are rejected or passed literally without side effects.
- **GOTCHA:** Escaping for one shell or platform is fragile; avoiding the interpreter is the durable control.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/09 -->
<!-- range: dvmcp -->
<!-- pair: 100/110 -->
<!-- pattern: command -->
# Remote Access Control
> dvmcp · 09 · hard · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Remote Access Control scenario as implemented by Harish Santhanalakshmi Ganesan, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted arguments cross into a shell, interpreter, dynamic loader, or operating-system process boundary.
- **REVIEW:** Is a shell or evaluator involved? Are executable identity and every argument fixed or independently allow-listed?
- **LEARN:** Data must remain structured arguments and must never become executable command syntax.

---

<!-- kind: resolution -->
<!-- key: dvmcp/09 -->
<!-- range: dvmcp -->
<!-- pair: 100/110 -->
<!-- pattern: command -->
# Resolution · Remote Access Control
> Defensive resolution and review gotchas for dvmcp · 09
- **CONTROL:** Remove shell evaluation, call fixed executables with argument arrays, validate typed values, drop privileges, and sandbox the process.
- **VALIDATE:** Use harmless metacharacter and unexpected-argument fixtures and assert they are rejected or passed literally without side effects.
- **GOTCHA:** Escaping for one shell or platform is fragile; avoiding the interpreter is the durable control.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: dvmcp/10 -->
<!-- range: dvmcp -->
<!-- pair: 101/110 -->
<!-- pattern: chain -->
# Multi-Vector Attack
> dvmcp · 10 · hard · 1 declared variant(s) · concept-level card
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
<!-- pattern: filesystem-tools -->
# Filesystem Workspace Actions
> appsecco-mcp · filesystem-workspace-actions · ungraded · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Filesystem Workspace Actions scenario as implemented by Appsecco, focusing on its Path traversal / code execution boundary.
- **BOUNDARY:** Workspace paths and requested operations cross into filesystem and process capabilities on the host.
- **REVIEW:** Which roots and operations are authorised independently? Can file content or names become commands, scripts, or executable arguments?
- **LEARN:** File access and action execution need separate allow-lists enforced after canonical path resolution.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/filesystem-workspace-actions -->
<!-- range: appsecco-mcp -->
<!-- pair: 102/110 -->
<!-- pattern: filesystem-tools -->
# Resolution · Filesystem Workspace Actions
> Defensive resolution and review gotchas for appsecco-mcp · filesystem-workspace-actions
- **CONTROL:** Canonicalise and contain paths, expose narrow operation-specific APIs, avoid shell interpretation, and isolate the worker account and filesystem.
- **VALIDATE:** Use disposable files and no-op actions to test traversal, symlinks, unsupported operations, and command-like names without executing payloads.
- **GOTCHA:** A path can remain in the workspace while the selected operation still creates an unintended executable effect.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/indirect-prompt-injection -->
<!-- range: appsecco-mcp -->
<!-- pair: 103/110 -->
<!-- pattern: prompt -->
# Indirect Prompt Injection (stdio)
> appsecco-mcp · indirect-prompt-injection · ungraded · 1 declared variant(s) · concept-level card
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
> appsecco-mcp · indirect-prompt-injection-remote · ungraded · 1 declared variant(s) · concept-level card
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
<!-- pattern: command -->
# Malicious Code Execution
> appsecco-mcp · malicious-code-exec · ungraded · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Malicious Code Execution scenario as implemented by Appsecco, focusing on its Injection sink boundary.
- **BOUNDARY:** Untrusted arguments cross into a shell, interpreter, dynamic loader, or operating-system process boundary.
- **REVIEW:** Is a shell or evaluator involved? Are executable identity and every argument fixed or independently allow-listed?
- **LEARN:** Data must remain structured arguments and must never become executable command syntax.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/malicious-code-exec -->
<!-- range: appsecco-mcp -->
<!-- pair: 105/110 -->
<!-- pattern: command -->
# Resolution · Malicious Code Execution
> Defensive resolution and review gotchas for appsecco-mcp · malicious-code-exec
- **CONTROL:** Remove shell evaluation, call fixed executables with argument arrays, validate typed values, drop privileges, and sandbox the process.
- **VALIDATE:** Use harmless metacharacter and unexpected-argument fixtures and assert they are rejected or passed literally without side effects.
- **GOTCHA:** Escaping for one shell or platform is fragile; avoiding the interpreter is the durable control.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/malicious-tools -->
<!-- range: appsecco-mcp -->
<!-- pair: 106/110 -->
<!-- pattern: tool-poisoning -->
# Malicious Tools
> appsecco-mcp · malicious-tools · ungraded · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Malicious Tools scenario as implemented by Appsecco, focusing on its Tool output poisoning boundary.
- **BOUNDARY:** Tool descriptions and results cross from a server-controlled metadata plane into model planning and user approval.
- **REVIEW:** Which metadata reaches the model or approval UI? Does execution use the same reviewed, authenticated definition?
- **LEARN:** Tool metadata is untrusted content and must not silently grant authority or inject instructions.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/malicious-tools -->
<!-- range: appsecco-mcp -->
<!-- pair: 106/110 -->
<!-- pattern: tool-poisoning -->
# Resolution · Malicious Tools
> Defensive resolution and review gotchas for appsecco-mcp · malicious-tools
- **CONTROL:** Authenticate servers, sanitise and canonicalise metadata, show security-relevant fields, and authorise every call outside the description.
- **VALIDATE:** Use benign instruction-like metadata to confirm it remains visible as data and cannot broaden a tool's permitted effect.
- **GOTCHA:** A harmless tool name can conceal instructions in descriptions, annotations, or returned content.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/namespace-typosquatting -->
<!-- range: appsecco-mcp -->
<!-- pair: 107/110 -->
<!-- pattern: dependency-confusion -->
# Namespace Typosquatting
> appsecco-mcp · namespace-typosquatting · ungraded · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Namespace Typosquatting scenario as implemented by Appsecco, focusing on its Supply chain boundary.
- **BOUNDARY:** A package name crosses internal and public registries where resolution priority may select an unintended publisher.
- **REVIEW:** Which registry owns the namespace? Can a public package or lookalike name outrank the intended internal dependency?
- **LEARN:** Dependency identity must bind namespace, registry, version, and digest rather than relying on the package name alone.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/namespace-typosquatting -->
<!-- range: appsecco-mcp -->
<!-- pair: 107/110 -->
<!-- pattern: dependency-confusion -->
# Resolution · Namespace Typosquatting
> Defensive resolution and review gotchas for appsecco-mcp · namespace-typosquatting
- **CONTROL:** Use scoped private namespaces, explicit registries, lockfiles and hashes, signed provenance, and deny undeclared sources.
- **VALIDATE:** Resolve benign test packages against isolated registries and assert public, unsigned, or hash-mismatched candidates fail closed.
- **GOTCHA:** Pinning a version does not help when the same name and version can resolve from the wrong registry.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/outdated-packages -->
<!-- range: appsecco-mcp -->
<!-- pair: 108/110 -->
<!-- pattern: dependency-hygiene -->
# Outdated Packages
> appsecco-mcp · outdated-packages · ungraded · 1 declared variant(s) · concept-level card
- **DESCRIPTION:** Review the Outdated Packages scenario as implemented by Appsecco, focusing on its Supply chain boundary.
- **BOUNDARY:** A known-vulnerable or abandoned dependency crosses from the package graph into a network-facing AI or MCP service.
- **REVIEW:** Which vulnerable components are reachable in this deployment? What owner and deadline govern upgrade or compensating controls?
- **LEARN:** Dependency age is not the decision; supported versions, reachable vulnerable behavior, provenance, and update policy are.

---

<!-- kind: resolution -->
<!-- key: appsecco-mcp/outdated-packages -->
<!-- range: appsecco-mcp -->
<!-- pair: 108/110 -->
<!-- pattern: dependency-hygiene -->
# Resolution · Outdated Packages
> Defensive resolution and review gotchas for appsecco-mcp · outdated-packages
- **CONTROL:** Maintain an SBOM and lockfile, scan advisories, remove unused packages, update supported versions, and document time-bound exceptions.
- **VALIDATE:** Use a synthetic advisory or policy threshold to confirm affected transitive dependencies block promotion with an actionable owner.
- **GOTCHA:** A clean direct-dependency list can hide an exploitable vulnerable version deeper in the resolved graph.
- **STATUS:** Offensive solution not verified—outside the current scope. Pinned upstream implementation; RedSec adapter health evidence only.

---

<!-- kind: challenge -->
<!-- key: appsecco-mcp/secrets-pii -->
<!-- range: appsecco-mcp -->
<!-- pair: 109/110 -->
<!-- pattern: secrets -->
# Secrets and PII Exposure
> appsecco-mcp · secrets-pii · ungraded · 1 declared variant(s) · concept-level card
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
> appsecco-mcp · wikipedia-streamable · ungraded · 1 declared variant(s) · concept-level card
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

---

<!-- kind: attribution -->
<!-- key: attribution/1 -->
<!-- range: portfolio -->
<!-- pair: appendix 1/2 -->
<!-- pattern: attribution -->
# Sources and licences · 1/2
> Standalone attribution for the catalog sources represented in this deck
- **builtin:** RedSec Range · Apache-2.0 · repository state · https://github.com/tq05/RedSec-range
- **dvaa:** OpenA2A · Apache-2.0 · faf3fb172ef526d12db0eb5377701549693118a6 · https://github.com/opena2a-org/damn-vulnerable-ai-agent
- **mcpgoat:** Sabyasachi Dhal · MIT · 80ceaf7ffedb8e0e74fd612798a6e09dfdd543ed · https://github.com/SabyasachiDhal/MCPGoat

---

<!-- kind: attribution -->
<!-- key: attribution/2 -->
<!-- range: portfolio -->
<!-- pair: appendix 2/2 -->
<!-- pattern: attribution -->
# Sources and licences · 2/2
> Standalone attribution for the catalog sources represented in this deck
- **dvmcp:** Harish Santhanalakshmi Ganesan · MIT (declared in README; no license file at pinned revision) · 79734c19f5104cd11486c90926d245560f53befa · https://github.com/harishsg993010/damn-vulnerable-MCP-server
- **appsecco-mcp:** Appsecco · MIT · 47b7f2082261136b667daa7be9273698e66e479e · https://github.com/appsecco/vulnerable-mcp-servers-lab
- **offsec:** OffSec · proprietary · not configured · https://www.offsec.com/courses/ai-300/
