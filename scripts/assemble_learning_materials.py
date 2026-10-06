#!/usr/bin/env python3
"""Generate defensive learning sources from RedSec's declarative catalog.

The generator intentionally consumes only repository-owned manifests and catalog
metadata. It does not import third-party application code, copy upstream solution
text, reproduce challenge secrets, or emit operational exploit procedures.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from redsec.loader import load_all
from redsec.range_catalog import load_catalog


ROOT = Path(__file__).resolve().parents[1]
TRAINING = ROOT / "docs" / "training"
GUIDE = TRAINING / "LEARNING-GUIDE.md"
DECK = TRAINING / "LEARNING-DECK.md"
OUTSIDE_SCOPE = "not verified—outside the current scope"


@dataclass(frozen=True)
class Card:
    range_id: str
    range_title: str
    challenge_id: str
    title: str
    category: str
    difficulty: str
    variants: int
    description: str
    provenance: str
    evidence: str
    pattern_id: str

    @property
    def key(self) -> str:
        return f"{self.range_id}/{self.challenge_id}"


@dataclass(frozen=True)
class DefensivePattern:
    boundary: str
    lesson: str
    questions: tuple[str, str]
    control: str
    validation: str
    gotcha: str


PATTERNS: dict[str, DefensivePattern] = {
    "prompt": DefensivePattern(
         "Untrusted content crosses into model-visible instructions or persistent context.",
         "Content provenance and instruction authority must remain distinct throughout the model pipeline.",
         ("Which fields can influence instructions?", "Can retrieved, tool, or remembered content persist or trigger an action?"),
         "Use typed instruction/data channels, provenance labels, output checks, scoped memory, and least-privilege tools.",
         "Use inert policy fixtures to confirm untrusted text remains data and cannot alter an authorised workflow.",
         "Filtering only the current user message misses instructions arriving through retrieval, tools, or memory.",
    ),
    "recon": DefensivePattern(
        "Model, provider, route, error, and capability details cross from internal configuration to an external caller.",
        "Discovery surfaces should disclose only what an authenticated user needs for an authorised workflow.",
        ("Which metadata is necessary for this caller?", "Can errors, banners, schemas, or undocumented routes reveal additional capability?"),
        "Minimise banners and errors, authenticate discovery endpoints, inventory routes and schemas, and rate-limit enumeration.",
        "Compare permitted and unauthorised synthetic clients and assert that only the documented minimum metadata is returned.",
        "Removing a route from user documentation does not make the reachable endpoint private.",
    ),
    "secrets": DefensivePattern(
         "Sensitive configuration or identity data crosses into a response, log, completion, or model context.",
         "Secrets should remain outside prompts and should be disclosed only through explicit, authorised interfaces.",
         ("Where is sensitive data introduced?", "Which output, error, metadata, or completion path can reveal it?"),
         "Use a secrets manager, minimise context, redact errors and logs, authorise reads, and monitor disclosure paths.",
         "Test redaction and access decisions with synthetic canaries and assert that unauthorised callers receive no value.",
         "Masking the final response is insufficient when the same value remains available through debug or metadata paths.",
    ),
    "identity": DefensivePattern(
         "A principal, object, task, or delegated action crosses an identity and authorisation boundary.",
         "Declared identity and delegated context are claims; authenticate the caller and authorise the resulting action.",
         ("Which principal is authenticated?", "Is the object and delegated action authorised for that principal?"),
         "Use signed identities, audience-bound credentials, object-level checks, task ownership, and least privilege.",
         "Use negative authorisation tests for wrong users, objects, audiences, tasks, and replayed context identifiers.",
         "A valid sender or token does not automatically authorise every downstream object or action.",
    ),
    "session-context": DefensivePattern(
        "Conversation state and delegated authority cross message, task, and session boundaries over time.",
        "Every message must be authenticated and authorised in the context of the accumulated session state.",
        ("Who owns the context and each message?", "Can replay, reordering, or partial validation change the cumulative meaning?"),
        "Bind context identifiers to authenticated principals, authorise every transition, validate cumulative state, and expire replayable state.",
        "Use harmless cross-user, replayed, split, and out-of-order messages to confirm the state machine rejects invalid transitions.",
        "Validating each message in isolation can miss a prohibited meaning assembled across several messages.",
    ),
    "agency": DefensivePattern(
        "A model-selected action crosses into a tool or service that has real authority and external effects.",
        "Tool availability is not action authorisation; the system that owns the effect must enforce policy for each call.",
        ("Which principal authorises the effect?", "Can model-controlled arguments exceed the intended task or data scope?"),
        "Use narrow tools, per-action authorisation, allow-listed arguments, minimal credentials, confirmation for sensitive effects, and audit logs.",
        "Exercise permitted and denied actions with synthetic accounts and assert enforcement at the tool or service boundary.",
        "A model refusal or tool description cannot contain authority that the downstream service fails to enforce.",
    ),
    "mcp": DefensivePattern(
         "MCP metadata, content, or a remote capability crosses from a server into a host with model or system authority.",
         "Treat server metadata and results as untrusted input, and keep protocol capability separate from permission.",
         ("What does the host trust before execution?", "Can definitions, results, or capabilities change after approval?"),
         "Pin and diff definitions, canonicalise metadata, authorise each call, sandbox execution, and require explicit consent.",
         "Validate canonical definitions and repeated calls with benign fixtures; assert that changed or excessive capability is rejected.",
         "One-time approval does not cover later metadata mutation, hidden text, or a broader runtime effect.",
    ),
    "tool-poisoning": DefensivePattern(
        "Tool descriptions and results cross from a server-controlled metadata plane into model planning and user approval.",
        "Tool metadata is untrusted content and must not silently grant authority or inject instructions.",
        ("Which metadata reaches the model or approval UI?", "Does execution use the same reviewed, authenticated definition?"),
        "Authenticate servers, sanitise and canonicalise metadata, show security-relevant fields, and authorise every call outside the description.",
        "Use benign instruction-like metadata to confirm it remains visible as data and cannot broaden a tool's permitted effect.",
        "A harmless tool name can conceal instructions in descriptions, annotations, or returned content.",
    ),
    "tool-registration": DefensivePattern(
        "A tool manifest crosses from an external registry or publisher into the trusted capability catalog.",
        "Registration is a software provenance decision: only authenticated publishers and reviewed, immutable tool definitions may become callable.",
        ("Which registry and publisher identity are trusted?", "Are manifest signatures, source revisions, and requested capabilities verified before approval?"),
        "Use approved registries, signed manifests, verified publisher identities, pinned source revisions, capability review, and an explicit tool allow-list.",
        "Submit benign signed, unsigned, altered, and unapproved manifests and assert that only the approved identity and exact digest can register.",
        "Schema-valid metadata can still describe an untrusted implementation; validation does not establish publisher or source authenticity.",
    ),
    "tool-shadowing": DefensivePattern(
        "A tool name or namespace crosses from discovery into registry resolution and invocation.",
        "Human-readable names are not stable identities; resolution must bind approval to one authenticated implementation.",
        ("What cryptographic identity owns this tool?", "Can another registry entry, namespace, or later definition win resolution?"),
        "Use an immutable registry, signed and version-pinned definitions, unique namespaces, and approval bound to the server and definition digest.",
        "Register benign lookalike and duplicate names and assert that ambiguous, unsigned, or changed identities fail closed.",
        "Name allow-lists still fail when resolution can select a different implementation with the same or similar name.",
    ),
    "tool-dataflow": DefensivePattern(
        "Sensitive data crosses several individually authorised tool calls before reaching a new destination.",
        "Authorisation must follow provenance and data flow across the whole tool chain, not only each isolated call.",
        ("Which earlier result becomes a later argument?", "Is the final destination permitted for that data classification?"),
        "Track taint and provenance across calls, apply destination-aware policy, minimise returned data, and require confirmation for cross-domain transfer.",
        "Use synthetic labelled values to verify that allowed local processing cannot be composed into an unauthorised transfer.",
        "Every call can look legitimate in isolation while their composition violates the original data-use purpose.",
    ),
    "rug-pull": DefensivePattern(
        "A previously reviewed tool definition changes between approval, discovery, and execution.",
        "Approval applies to an immutable definition digest and must be invalidated when security-relevant metadata or behavior changes.",
        ("Which digest was approved?", "What forces re-review when the definition or server identity changes?"),
        "Pin signed definitions, compare canonical digests before every call, cache immutably, and require re-approval for any change.",
        "Use two benign versions of one tool and assert that the second cannot run under approval granted to the first.",
        "Periodic refresh without digest-bound approval creates a time-of-check/time-of-use gap.",
    ),
    "unicode": DefensivePattern(
        "Unicode formatting and confusable characters cross from raw metadata into scanning, display, and model-visible text.",
        "Security review and execution must use one canonical representation while preserving warnings about concealed characters.",
        ("Which normalization form is enforced?", "Are bidirectional controls, zero-width characters, and confusables exposed to reviewers?"),
        "Normalize consistently, reject or visibly escape control characters, detect confusables, and scan the same canonical text shown to users.",
        "Use harmless strings containing bidi, zero-width, and confusable characters and assert identical scanner and display decisions.",
        "Stripping a subset of invisible characters can create a second, differently interpreted representation.",
    ),
    "sampling": DefensivePattern(
        "A server-requested model call crosses back into host context, credentials, tokens, and compute budgets.",
        "Sampling is a privileged host action that needs explicit purpose, context minimisation, consent, and resource limits.",
        ("Which context is shared with the sampled model?", "Who authorises the purpose, model, token budget, and returned destination?"),
        "Require informed consent, minimise context, isolate credentials, allow-list models and purposes, cap tokens and cost, and audit results.",
        "Use synthetic host context and bounded budgets to confirm an untrusted server cannot expand context or repeat calls silently.",
        "Approving the parent tool call does not automatically approve every server-initiated model call it requests.",
    ),
    "elicitation": DefensivePattern(
        "A server-generated request crosses into a trusted user interaction and may solicit sensitive input.",
        "Elicitation needs a trusted host UI, clear server identity and purpose, schema limits, and no automatic secret completion.",
        ("Can the user see who requested the value and why?", "Can the host auto-fill credentials or accept undeclared fields?"),
        "Render elicitations in trusted chrome, show provenance, allow-list schemas, block secret autofill, and require explicit user consent.",
        "Send benign unexpected and sensitive-looking fields and confirm the host refuses, redacts, or requires an explicit decision.",
        "A valid elicitation schema does not make the requested value appropriate for that server.",
    ),
    "logging": DefensivePattern(
        "Runtime secrets and personal data cross into diagnostic notifications, logs, and support exports.",
        "Logging level changes must not bypass data classification, redaction, or caller authorisation.",
        ("Which values can reach debug output?", "Who may change verbosity and retrieve the resulting records?"),
        "Use structured allow-listed logging, redact at source, restrict verbosity changes, separate tenants, and apply retention controls.",
        "Exercise each log level with synthetic canaries and assert that sensitive fields never appear for unauthorised readers.",
        "Disabling verbose logs in production does not fix code paths that still format secrets before filtering.",
    ),
    "completion": DefensivePattern(
        "Autocompletion crosses from partial user input into internal indexes, identifiers, or secret-backed values.",
        "Completion sources need the same object and field authorisation as the final read operation.",
        ("Which corpus backs suggestions?", "Is every suggested value authorised for this principal and purpose?"),
        "Use non-sensitive suggestion indexes, enforce field-level authorisation, cap results, and avoid secret stores as completion sources.",
        "Probe with benign prefixes under different identities and assert that suggestions reveal only each caller's allowed namespace.",
        "Hiding a complete value is insufficient when repeated prefix queries can enumerate it incrementally.",
    ),
    "scope": DefensivePattern(
        "A client-declared root, permission, or resource scope crosses into server-side access control.",
        "Servers must enforce the intersection of declared scope, authenticated identity, and canonical resource location.",
        ("Who defines and enforces the allowed scope?", "Is the resource canonicalised before containment and permission checks?"),
        "Enforce scopes server-side, canonicalise resource identifiers, deny ambient access, and apply least privilege to the host process.",
        "Use synthetic in-scope and out-of-scope resources, including encoded and absolute forms, to confirm containment fails closed.",
        "Advertising a root or permission to the model does not enforce it at the filesystem or service boundary.",
    ),
    "sink": DefensivePattern(
         "Untrusted structured input reaches a filesystem, interpreter, query engine, parser, or process boundary.",
         "The safe boundary is the sink: preserve structure and avoid turning data into executable syntax.",
         ("Which sink interprets the value?", "Is validation applied after decoding and canonicalisation?"),
         "Use parameterised APIs, safe parsers, canonical path containment, allow-lists, and a restricted runtime.",
         "Add non-destructive negative tests for malformed, encoded, absolute, and boundary-crossing values.",
         "A blacklist applied before decoding or normalisation can approve a value that becomes dangerous later.",
    ),
    "path": DefensivePattern(
        "An untrusted path or URI crosses into filesystem resolution outside an authorised root.",
        "Access decisions must use the final canonical target and remain safe across encoding, absolute paths, and symbolic links.",
        ("What is the canonical allowed root?", "Can decoding, symlinks, alternate separators, or races change the resolved target?"),
        "Resolve paths safely, reject absolute and escaping targets, enforce containment after canonicalisation, and run with minimal filesystem access.",
        "Use temporary in-root and out-of-root fixtures with encoded, absolute, separator, and symlink cases and assert fail-closed behavior.",
        "String-prefix checks can approve sibling paths or links whose final target lies outside the intended root.",
    ),
    "filesystem-tools": DefensivePattern(
        "Workspace paths and requested operations cross into filesystem and process capabilities on the host.",
        "File access and action execution need separate allow-lists enforced after canonical path resolution.",
        ("Which roots and operations are authorised independently?", "Can file content or names become commands, scripts, or executable arguments?"),
        "Canonicalise and contain paths, expose narrow operation-specific APIs, avoid shell interpretation, and isolate the worker account and filesystem.",
        "Use disposable files and no-op actions to test traversal, symlinks, unsupported operations, and command-like names without executing payloads.",
        "A path can remain in the workspace while the selected operation still creates an unintended executable effect.",
    ),
    "command": DefensivePattern(
        "Untrusted arguments cross into a shell, interpreter, dynamic loader, or operating-system process boundary.",
        "Data must remain structured arguments and must never become executable command syntax.",
        ("Is a shell or evaluator involved?", "Are executable identity and every argument fixed or independently allow-listed?"),
        "Remove shell evaluation, call fixed executables with argument arrays, validate typed values, drop privileges, and sandbox the process.",
        "Use harmless metacharacter and unexpected-argument fixtures and assert they are rejected or passed literally without side effects.",
        "Escaping for one shell or platform is fragile; avoiding the interpreter is the durable control.",
    ),
    "sql": DefensivePattern(
        "Untrusted values cross into relational query structure and database privileges.",
        "Queries must keep code and data separate, including identifiers, sorting, and dynamically selected clauses.",
        ("Which query elements are parameterised?", "Does the database account have only the permissions required by this operation?"),
        "Use parameterised queries, allow-list non-parameterisable identifiers, constrain result size, and grant least-privilege database roles.",
        "Use inert quote, wildcard, comment, and type-mismatch fixtures and assert query shape and authorised results remain unchanged.",
        "Parameters protect values but do not make attacker-selected table names, operators, or sort clauses safe.",
    ),
    "nosql": DefensivePattern(
        "Untrusted JSON or object fields cross into NoSQL operators, selectors, projections, or update structure.",
        "Application data must not be interpreted as query operators or prototype-bearing objects.",
        ("Which keys and value types are accepted?", "Can nested operator keys or type confusion alter selector meaning?"),
        "Validate against a closed schema, construct queries from typed fields, reject operator-prefixed keys, and use least-privilege data access.",
        "Use benign nested objects, arrays, unexpected types, and operator-like keys and assert the query builder rejects them.",
        "Escaping strings does not help when the dangerous input is a structured operator object.",
    ),
    "template": DefensivePattern(
        "Untrusted text crosses into template source, expressions, object traversal, or server-side helpers.",
        "Users may supply data for a fixed template but must not define executable template structure.",
        ("Can input become template source or an expression?", "Which objects, filters, and helpers are reachable during rendering?"),
        "Use fixed logic-light templates, pass typed data, enable sandboxing and autoescape, and remove dangerous helpers and object access.",
        "Render harmless expression-like fixtures and assert they remain literal text with no object access or evaluation.",
        "Output escaping prevents markup injection but does not stop server-side expression evaluation.",
    ),
    "xml": DefensivePattern(
        "Untrusted XML crosses into entity resolution, DTD processing, XInclude, and parser-controlled network or file access.",
        "XML features that resolve external content must be disabled before parsing untrusted documents.",
        ("Are DTDs and external entities disabled?", "Can the parser access files, networks, schemas, or includes?"),
        "Use a hardened parser with DTDs, external entities, XInclude, and network access disabled; enforce size and depth limits.",
        "Parse inert documents containing disabled declarations and oversized nesting and assert deterministic rejection without I/O.",
        "Blocking one entity syntax is insufficient when schemas, parameter entities, or includes still resolve externally.",
    ),
    "deserialization": DefensivePattern(
        "Untrusted serialized objects cross into constructors, prototypes, type hooks, or recursive merge logic.",
        "Deserialization must produce schema-validated data objects without executable types or prototype mutation.",
        ("Which types and hooks can be instantiated?", "Can special keys or merge behavior alter prototypes or application defaults?"),
        "Prefer plain data formats, validate a closed schema, reject dangerous keys and polymorphic types, and avoid recursive merges into prototypes.",
        "Use inert unexpected types, deep objects, and prototype-like keys and assert the parser returns isolated plain data or rejects them.",
        "A trusted transport does not make attacker-controlled object graphs or type metadata safe to instantiate.",
    ),
    "transport": DefensivePattern(
         "Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.",
         "Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.",
         ("Which layer decides request meaning?", "Are origin, audience, version, and session identifiers bound exactly?"),
         "Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.",
         "Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.",
         "A gateway and application can each appear correct while authorising different interpretations of one request.",
    ),
    "tool-mitm": DefensivePattern(
        "Tool calls and results cross a network or intermediary that could replace the server, request, or response.",
        "The host must authenticate the tool endpoint and bind each response to the intended request and server identity.",
        ("How is the server authenticated?", "Are request identity, response identity, integrity, freshness, and channel binding verified?"),
        "Use authenticated encrypted transport, pinned service identity where appropriate, request-response correlation, replay protection, and integrity checks.",
        "Use a benign test endpoint with the wrong identity or correlation value and assert the host rejects its responses.",
        "TLS without correct hostname, trust-store, redirect, and response binding checks can still connect to the wrong tool.",
    ),
    "tool-redirect": DefensivePattern(
        "A configured tool endpoint crosses DNS, redirect, proxy, and routing boundaries before reaching the final service.",
        "Every hop and resolved destination must remain within the approved endpoint policy and authenticated service identity.",
        ("Which redirects and resolved addresses are allowed?", "Does authentication bind to the final destination after DNS and proxy routing?"),
        "Pin approved schemes and hosts, restrict redirects, validate resolved addresses, authenticate the final service, and re-check policy on every hop.",
        "Use inert redirect and alternate-resolution fixtures and assert the client refuses destinations outside the approved set.",
        "Validating only the original URL misses a later redirect or resolution to a different trust zone.",
    ),
    "oauth-audience": DefensivePattern(
        "An OAuth token crosses from its intended resource server or client into a different audience or delegated action.",
        "Token validity is insufficient unless issuer, audience, scope, client, subject, and delegation all match the requested operation.",
        ("Which exact resource audience issued the token?", "Are scope and delegated subject valid for this tool and action?"),
        "Validate issuer and exact audience, use resource-specific tokens, restrict scopes, bind delegation, and reject token forwarding across services.",
        "Use synthetic tokens with correct signatures but wrong audiences, clients, scopes, or subjects and assert rejection.",
        "A token accepted by one service must not become a bearer credential for every service in the agent chain.",
    ),
    "dns-rebinding": DefensivePattern(
        "A hostname crosses browser-origin and DNS resolution boundaries and may resolve to a different address over time.",
        "Origin checks and destination policy must bind to stable identities and validate every resolved connection target.",
        ("Is the Origin validated exactly?", "Are all resolved addresses checked at connection time and after DNS changes?"),
        "Require exact origins, re-resolve and validate destination addresses, reject private or disallowed ranges, and avoid trusting hostname strings alone.",
        "Use controlled DNS fixtures that change between safe addresses and assert disallowed resolutions never receive a connection.",
        "A hostname that was safe during validation can resolve differently when the connection is opened.",
    ),
    "cors": DefensivePattern(
        "Browser credentials and responses cross from an MCP HTTP service into a requesting web origin.",
        "Cross-origin access must use a narrow exact allow-list and must never reflect arbitrary origins with credentials.",
        ("Which exact origins need access?", "Are credentials, preflight methods, headers, and cached decisions constrained consistently?"),
        "Allow-list exact HTTPS origins, minimise methods and headers, vary caches by Origin, and disable credentials unless strictly required.",
        "Send harmless preflights from allowed, sibling, null, and attacker-controlled origins and assert only the exact policy succeeds.",
        "Wildcard subdomains and reflected origins can turn an apparently narrow policy into credentialed cross-origin access.",
    ),
    "session-security": DefensivePattern(
        "A session identifier crosses clients, requests, reconnects, and server-side state ownership boundaries.",
        "Session identifiers must be unpredictable, confidential, short-lived, and bound to the authenticated principal and channel context.",
        ("How much entropy and lifetime does the identifier have?", "Can another principal replay, fix, or reuse it across connections?"),
        "Use cryptographic random identifiers, rotate on authentication changes, bind ownership server-side, expire promptly, and protect transport and storage.",
        "Create multiple synthetic sessions and test replay, cross-user reuse, fixation, expiry, and logout invalidation.",
        "A random-looking identifier still fails if it remains valid across users, privilege changes, or excessive time.",
    ),
    "supply": DefensivePattern(
         "A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.",
         "AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.",
         ("What identity and digest bind the artifact?", "Where is it loaded, merged, trained, or resolved?"),
         "Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.",
         "Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.",
         "A familiar filename, package name, or model label is not proof of origin or safe behavior.",
    ),
    "model-deserialization": DefensivePattern(
        "A model artifact crosses from storage into a loader that may instantiate executable objects or custom operators.",
        "Model loading should consume data-only formats and occur in isolation before an artifact reaches production authority.",
        ("Can the format encode executable objects or custom code?", "Where are provenance, signature, and digest verified before loading?"),
        "Prefer safe tensor formats, verify signed provenance and immutable digests, scan or convert in a sandbox, and block custom loading hooks.",
        "Load only benign fixtures in an isolated process and assert unsafe formats, unknown operators, and provenance failures are rejected.",
        "A model repository or familiar extension does not guarantee that the loader treats the file as data only.",
    ),
    "data-poisoning": DefensivePattern(
        "Training or retrieval records cross from collection and labeling into learned or indexed behavior.",
        "Dataset integrity requires provenance, controlled contribution, anomaly review, and behavior-focused validation before promotion.",
        ("Who can add or relabel records?", "Which tests detect targeted triggers, skew, duplication, or provenance gaps?"),
        "Version and sign datasets, restrict writers, review labels, deduplicate, scan anomalies, and evaluate targeted slices before deployment.",
        "Add harmless synthetic outliers and trigger-like canaries and assert ingestion or evaluation identifies them before promotion.",
        "Aggregate quality metrics can remain healthy while a small targeted subset creates a reliable backdoor.",
    ),
    "adapter-backdoor": DefensivePattern(
        "An adapter or fine-tune delta crosses into a trusted base model and changes behavior without replacing the full artifact.",
        "Adapters need independent provenance and behavioral evaluation because their small size does not limit their authority.",
        ("Which signed identity produced the adapter?", "What targeted behavior changes appear when it is composed with the approved base?"),
        "Pin signed adapter digests, restrict loading, scan formats, evaluate targeted and safety suites, and promote the composed model as one artifact.",
        "Compare a benign adapter and an unapproved digest in isolation and assert only the evaluated composition can be promoted.",
        "Trust in the base model does not transfer to an adapter that can override high-impact behavior.",
    ),
    "dependency-confusion": DefensivePattern(
        "A package name crosses internal and public registries where resolution priority may select an unintended publisher.",
        "Dependency identity must bind namespace, registry, version, and digest rather than relying on the package name alone.",
        ("Which registry owns the namespace?", "Can a public package or lookalike name outrank the intended internal dependency?"),
        "Use scoped private namespaces, explicit registries, lockfiles and hashes, signed provenance, and deny undeclared sources.",
        "Resolve benign test packages against isolated registries and assert public, unsigned, or hash-mismatched candidates fail closed.",
        "Pinning a version does not help when the same name and version can resolve from the wrong registry.",
    ),
    "dependency-hygiene": DefensivePattern(
        "A known-vulnerable or abandoned dependency crosses from the package graph into a network-facing AI or MCP service.",
        "Dependency age is not the decision; supported versions, reachable vulnerable behavior, provenance, and update policy are.",
        ("Which vulnerable components are reachable in this deployment?", "What owner and deadline govern upgrade or compensating controls?"),
        "Maintain an SBOM and lockfile, scan advisories, remove unused packages, update supported versions, and document time-bound exceptions.",
        "Use a synthetic advisory or policy threshold to confirm affected transitive dependencies block promotion with an actionable owner.",
        "A clean direct-dependency list can hide an exploitable vulnerable version deeper in the resolved graph.",
    ),
    "dos": DefensivePattern(
         "Attacker-controlled work crosses compute, memory, token, concurrency, or financial budget boundaries.",
         "Availability and spend are security properties that require explicit per-request and aggregate budgets.",
         ("Which resource grows with input?", "Where are tenant, tool, and global budgets enforced?"),
         "Set timeouts, size and token limits, concurrency quotas, rate limits, cancellation, and cost telemetry.",
         "Use bounded synthetic workloads to assert predictable rejection before resource use approaches operational limits.",
         "Per-request limits alone miss distributed or repeated consumption across sessions and identities.",
    ),
    "redos": DefensivePattern(
        "Attacker-controlled text crosses into a regular-expression engine whose backtracking cost can grow nonlinearly.",
        "Pattern safety and bounded input must be established before regex matching occurs on a shared service thread.",
        ("Can the pattern exhibit catastrophic backtracking?", "What input, time, and concurrency limits bound each match?"),
        "Use linear-time patterns or engines, simplify ambiguous repetition, cap input length, set timeouts, and isolate expensive matching.",
        "Run bounded synthetic worst-case strings in a timeout-controlled test and assert predictable rejection and latency.",
        "A request rate limit does not prevent one accepted input from monopolising a worker for an excessive duration.",
    ),
    "rag": DefensivePattern(
         "Indexed content, similarity scores, or derived vectors cross from a data store into a trusted answer.",
         "Relevance is not trust; retrieval, provenance, privacy, and instruction handling are separate decisions.",
         ("Who can add or rank content?", "What can similarity, provenance, or output precision disclose?"),
         "Control ingestion, preserve provenance, isolate instructions from retrieved data, minimise precision, and authorise the corpus.",
         "Use synthetic documents and records to test ranking, provenance display, tenant isolation, and privacy thresholds.",
         "A high similarity score or authoritative-looking citation does not establish integrity or permission.",
    ),
    "embeddings": DefensivePattern(
        "Derived vectors and similarity decisions cross privacy, tenant, and policy boundaries.",
        "Embeddings can retain information about source records and should not serve as identity or authorisation controls.",
        ("Who may query the vectors and at what precision?", "Can outputs reveal membership, reconstruct content, or bypass a text-only policy?"),
        "Authorise vector access, isolate tenants, minimise returned precision, rate-limit queries, and enforce policy on canonical source data.",
        "Use synthetic canary records to measure leakage and verify that similarity cannot replace exact policy checks.",
        "A derived representation is not automatically anonymous, and semantic similarity is not an access-control decision.",
    ),
    "infra": DefensivePattern(
         "A model-facing workload crosses into cloud metadata, administrative APIs, registries, or network destinations.",
         "Workload identity and egress are authority boundaries; model-facing services should carry minimal ambient privilege.",
         ("Which destinations can the workload reach?", "Which administrative or registry actions require authentication?"),
         "Default-deny egress, use workload identity, require admin authentication, isolate metadata, and keep secrets out of artifacts.",
         "Review policy and use inert internal endpoints to confirm blocked destinations and authenticated administration.",
         "Application input validation cannot compensate for broad network reach and over-privileged workload credentials.",
    ),
    "admin-api": DefensivePattern(
        "A model or inference administration operation crosses from a network client into privileged runtime configuration and resources.",
        "Administrative inference routes require strong authentication, explicit authorisation, isolation, and narrow network exposure.",
        ("Which principal may invoke each administrative operation?", "Is the route separated from public inference traffic and ambient workload identity?"),
        "Require authenticated workload identity, role-based action checks, private network exposure, rate limits, and complete audit records.",
        "Use authorised and unauthorised synthetic principals to verify every administrative method and object denies by default.",
        "A private-looking path or undocumented endpoint is not an authentication or authorisation control.",
    ),
    "threat": DefensivePattern(
         "Assets, principals, data flows, and effects cross one or more explicitly modelled trust boundaries.",
         "A useful threat model explains relationships and complete paths rather than listing security keywords.",
         ("Which asset and principal are involved?", "What ordered path connects entry, privilege, action, and impact?"),
         "Record assets, trust boundaries, data flows, assumptions, ranked paths, owners, and controls tied to each boundary.",
         "Review models for concrete actors and ordered relationships; reject disconnected keyword inventories.",
         "A complete list of terms can still omit the relationship that makes a scenario possible.",
    ),
    "chain": DefensivePattern(
         "Several individually limited weaknesses compose across content, identity, tools, data, and infrastructure.",
         "Security review must follow end-to-end authority and data flow because local controls can fail in composition.",
         ("Which earlier weakness enables the next step?", "Which control breaks the chain earliest and most reliably?"),
         "Use layered controls, trace provenance, minimise ambient authority, segment systems, and retain cross-service evidence.",
         "Validate each boundary independently with safe fixtures, then review the composed data flow without executing an attack chain.",
         "A control may stop one step while leaving another route to the same privileged effect.",
    ),
}


CHALLENGE_PATTERN_IDS = {
    # RedSec built-in course (43 concepts)
    "builtin/01/first-contact": "prompt",
    "builtin/02/fingerprint-model": "recon",
    "builtin/02/enumerate-surfaces": "recon",
    "builtin/02/leak-config": "recon",
    "builtin/03/sys-prompt-leak": "prompt",
    "builtin/03/indirect-injection": "prompt",
    "builtin/03/tool-exfil": "agency",
    "builtin/03/memory-poisoning": "prompt",
    "builtin/04/trust-exploitation": "identity",
    "builtin/04/message-manipulation": "identity",
    "builtin/04/agent-impersonation": "identity",
    "builtin/04/session-smuggling": "session-context",
    "builtin/05/knowledge-poisoning": "rag",
    "builtin/05/retrieval-manipulation": "rag",
    "builtin/05/citation-spoofing": "rag",
    "builtin/06/embedding-inversion": "embeddings",
    "builtin/06/membership-inference": "embeddings",
    "builtin/06/embedding-collision": "embeddings",
    "builtin/07/tool-poisoning": "tool-poisoning",
    "builtin/07/resource-traversal": "path",
    "builtin/07/prompt-injection": "prompt",
    "builtin/07/sampling-abuse": "sampling",
    "builtin/07/roots-bypass": "scope",
    "builtin/07/elicitation-phishing": "elicitation",
    "builtin/07/logging-leak": "logging",
    "builtin/07/completion-leak": "completion",
    "builtin/07/rug-pull": "rug-pull",
    "builtin/07/command-injection": "command",
    "builtin/07/header-routing-confusion": "transport",
    "builtin/07/unicode-tool-poisoning": "unicode",
    "builtin/08/malicious-weights": "model-deserialization",
    "builtin/08/poisoned-dataset": "data-poisoning",
    "builtin/08/backdoored-adapter": "adapter-backdoor",
    "builtin/08/dependency-confusion": "dependency-confusion",
    "builtin/09/metadata-ssrf": "infra",
    "builtin/09/open-inference-api": "admin-api",
    "builtin/09/registry-secrets": "secrets",
    "builtin/10/asset-inventory": "threat",
    "builtin/10/trust-boundaries": "threat",
    "builtin/10/attack-paths": "threat",
    "builtin/11/initial-access": "chain",
    "builtin/11/pivot-vault": "chain",
    "builtin/11/exfil-crown-jewel": "chain",

    # Damn Vulnerable AI Agent (22 concepts)
    "dvaa/L1-01": "secrets",
    "dvaa/L1-02": "secrets",
    "dvaa/L1-03": "prompt",
    "dvaa/L2-01": "prompt",
    "dvaa/L2-02": "prompt",
    "dvaa/L2-03": "path",
    "dvaa/L2-04": "prompt",
    "dvaa/L2-05": "secrets",
    "dvaa/L2-06": "prompt",
    "dvaa/L2-07": "prompt",
    "dvaa/L2-08": "tool-registration",
    "dvaa/L2-09": "tool-mitm",
    "dvaa/L3-01": "prompt",
    "dvaa/L3-02": "infra",
    "dvaa/L3-03": "prompt",
    "dvaa/L3-04": "secrets",
    "dvaa/L3-05": "tool-shadowing",
    "dvaa/L3-06": "tool-dataflow",
    "dvaa/L3-07": "tool-shadowing",
    "dvaa/L3-08": "tool-redirect",
    "dvaa/L4-01": "chain",
    "dvaa/L4-02": "chain",

    # MCPGoat (26 concepts, each declared with three upstream levels)
    "mcpgoat/A1": "tool-poisoning",
    "mcpgoat/A2": "tool-shadowing",
    "mcpgoat/A3": "rug-pull",
    "mcpgoat/B1": "prompt",
    "mcpgoat/D1": "command",
    "mcpgoat/D2": "path",
    "mcpgoat/D3": "infra",
    "mcpgoat/D4": "sql",
    "mcpgoat/C2": "identity",
    "mcpgoat/C3": "identity",
    "mcpgoat/E1": "secrets",
    "mcpgoat/A9": "unicode",
    "mcpgoat/B2": "prompt",
    "mcpgoat/B3": "prompt",
    "mcpgoat/B5": "sampling",
    "mcpgoat/C4": "oauth-audience",
    "mcpgoat/D6": "template",
    "mcpgoat/F1": "dns-rebinding",
    "mcpgoat/F2": "cors",
    "mcpgoat/C6": "session-security",
    "mcpgoat/G1": "dos",
    "mcpgoat/G4": "redos",
    "mcpgoat/D5": "nosql",
    "mcpgoat/D7": "xml",
    "mcpgoat/D8": "deserialization",
    "mcpgoat/H1": "dependency-confusion",

    # Damn Vulnerable MCP Server (10 concepts)
    "dvmcp/01": "prompt",
    "dvmcp/02": "tool-poisoning",
    "dvmcp/03": "scope",
    "dvmcp/04": "rug-pull",
    "dvmcp/05": "tool-shadowing",
    "dvmcp/06": "prompt",
    "dvmcp/07": "secrets",
    "dvmcp/08": "command",
    "dvmcp/09": "command",
    "dvmcp/10": "chain",

    # Appsecco Vulnerable MCP Servers Lab (9 concepts)
    "appsecco-mcp/filesystem-workspace-actions": "filesystem-tools",
    "appsecco-mcp/indirect-prompt-injection": "prompt",
    "appsecco-mcp/indirect-prompt-injection-remote": "prompt",
    "appsecco-mcp/malicious-code-exec": "command",
    "appsecco-mcp/malicious-tools": "tool-poisoning",
    "appsecco-mcp/namespace-typosquatting": "dependency-confusion",
    "appsecco-mcp/outdated-packages": "dependency-hygiene",
    "appsecco-mcp/secrets-pii": "secrets",
    "appsecco-mcp/wikipedia-streamable": "prompt",
}


def pattern_id_for(range_id: str, challenge_id: str, category: str) -> str:
    key = f"{range_id}/{challenge_id}"
    try:
        return CHALLENGE_PATTERN_IDS[key]
    except KeyError as error:
        raise ValueError(f"no defensive pattern for {key}: {category}") from error


def pattern_for(card: Card) -> DefensivePattern:
    return PATTERNS[card.pattern_id]


def clean(value: str) -> str:
    return " ".join(value.replace("|", "/").split())


def cards() -> list[Card]:
    result: list[Card] = []
    catalog = load_catalog()
    builtin_definition = catalog.ranges["builtin"]

    for _, module in load_all():
        for challenge in module.challenges:
            verify_types = sorted({step.type for step in challenge.verify})
            category = clean(challenge.primitive or module.title)
            challenge_id = f"{module.id}/{challenge.id}"
            result.append(Card(
                range_id="builtin",
                range_title=builtin_definition.title,
                challenge_id=challenge_id,
                title=clean(challenge.title),
                category=category,
                difficulty=clean(challenge.tier or challenge.difficulty or module.difficulty),
                variants=1,
                description=(
                    f"Review how the built-in challenge models {clean(challenge.title).lower()}, "
                    f"focusing on its {category} trust boundary."
                ),
                provenance="RedSec module manifest and lesson",
                evidence=f"Built-in {', '.join(verify_types) or 'declared'} verifier",
                pattern_id=pattern_id_for("builtin", challenge_id, category),
            ))

    for range_id in ("dvaa", "mcpgoat", "dvmcp", "appsecco-mcp"):
        definition = catalog.ranges[range_id]
        for challenge in definition.curriculum.challenges:
            challenge_id = clean(challenge.id)
            category = clean(challenge.category)
            result.append(Card(
                range_id=range_id,
                range_title=definition.title,
                challenge_id=challenge_id,
                title=clean(challenge.title),
                category=category,
                difficulty=clean(challenge.difficulty),
                variants=challenge.variants,
                description=(
                    f"Review the {challenge.title} scenario as implemented by "
                    f"{definition.maintainer}, focusing on its {challenge.category} boundary."
                ),
                provenance=definition.curriculum.solution_url or definition.homepage,
                evidence="Pinned upstream implementation; RedSec adapter health evidence only",
                pattern_id=pattern_id_for(range_id, challenge_id, category),
            ))

    actual_keys = {card.key for card in result}
    mapped_keys = set(CHALLENGE_PATTERN_IDS)
    if actual_keys != mapped_keys:
        missing = sorted(actual_keys - mapped_keys)
        stale = sorted(mapped_keys - actual_keys)
        raise SystemExit(f"defensive pattern map drift: missing={missing}, stale={stale}")
    unknown_patterns = sorted(set(CHALLENGE_PATTERN_IDS.values()) - set(PATTERNS))
    if unknown_patterns:
        raise SystemExit(f"undefined defensive patterns: {unknown_patterns}")
    if len(result) != 110 or sum(card.variants for card in result) != 162:
        raise SystemExit(
            f"unexpected catalog size: {len(result)} concepts / "
            f"{sum(card.variants for card in result)} variants"
        )
    return result


def attribution_records() -> list[dict[str, str]]:
    catalog = load_catalog()
    records = []
    for range_id in ("builtin", "dvaa", "mcpgoat", "dvmcp", "appsecco-mcp", "offsec"):
        definition = catalog.ranges[range_id]
        if definition.source:
            repository = definition.source.repository.removesuffix(".git")
            revision = definition.source.revision
        else:
            repository = definition.homepage
            revision = "repository state" if range_id == "builtin" else "not configured"
        records.append({
            "id": range_id,
            "title": clean(definition.title),
            "maintainer": clean(definition.maintainer),
            "license": clean(definition.license),
            "repository": repository,
            "revision": revision,
            "status": definition.availability,
            "note": clean(definition.note or definition.curriculum.note or ""),
        })
    return records


def render_guide(items: list[Card]) -> str:
    lines = [
        "---",
        'title: "RedSec Range — Defensive Challenge Learning Guide"',
        'subtitle: "110 concept cards · 162 declared variants · architecture, review, and remediation"',
        'author: "RedSec Range"',
        "---",
        "",
        "# How to use this guide {.unnumbered}",
        "",
        "> **Scope.** This edition supports defensive education, architecture review,",
        "> remediation, and non-destructive validation. It intentionally omits challenge",
        "> secrets, operational payloads, and step-by-step exploitation procedures.",
        "",
        "For each challenge, identify the trust boundary, answer the review questions,",
        "apply the defensive resolution, and validate the expected allow/deny behavior",
        "with synthetic data. Runtime exploitability is **not verified—outside the current",
        "scope**. Existing project and upstream evidence is linked as provenance rather",
        "than reproduced here.",
        "",
        "This guide provides one defensive card per catalog concept. The 26 MCPGoat",
        "cards each represent three declared upstream levels, so the 110 concept cards",
        "span 162 declared runnable variants. Those 52 additional levels are not",
        "separate, level-specific walkthroughs in this edition.",
        "",
        "# Portfolio map",
        "",
        "| Range | Concepts | Declared variants | Evidence meaning |",
        "|---|---:|---:|---|",
    ]
    for range_id in ("builtin", "dvaa", "mcpgoat", "dvmcp", "appsecco-mcp"):
        selected = [card for card in items if card.range_id == range_id]
        evidence = (
            "Repository manifests and declared verifiers"
            if range_id == "builtin"
            else "Pinned upstream metadata; adapter health does not prove solvability"
        )
        lines.append(
            f"| `{range_id}` | {len(selected)} | {sum(card.variants for card in selected)} | {evidence} |"
        )

    lines.extend([
        "",
        "# Attribution and pinned sources",
        "",
        "| Range | Maintainer | License | Revision | Repository / status |",
        "|---|---|---|---|---|",
    ])
    for record in attribution_records():
        repository = record["repository"]
        source = f"[{repository}]({repository})"
        status = record["status"]
        note = f" — {record['note']}" if record["note"] else ""
        lines.append(
            f"| `{record['id']}` | {record['maintainer']} | {record['license']} | "
            f"`{record['revision']}` | {source} ({status}){note} |"
        )

    lines.extend([
        "",
        "# Challenge review cards",
        "",
        "The cards are grouped by range. The `offsec` catalog entry has no deployable",
        "challenges and remains a placeholder, so it contributes no card.",
        "",
    ])

    for range_id in ("builtin", "dvaa", "mcpgoat", "dvmcp", "appsecco-mcp"):
        selected = [card for card in items if card.range_id == range_id]
        lines.extend([f"# `{range_id}` — {selected[0].range_title}", ""])
        for card in selected:
            pattern = pattern_for(card)
            lines.extend([
                f"## `{card.challenge_id}` — {card.title}",
                "",
                f"**Category:** {card.category} · **Difficulty:** {card.difficulty} · "
                f"**Declared variants:** {card.variants}",
                f"**Catalog key:** `{card.key}` · **Defensive pattern:** `{card.pattern_id}`",
                "",
                "### Challenge description",
                "",
                card.description,
                "",
                "### Educational focus",
                "",
                pattern.lesson,
                "",
                f"**Trust boundary:** {pattern.boundary}",
                "",
                "### Guided defensive review",
                "",
                f"1. {pattern.questions[0]}",
                f"2. {pattern.questions[1]}",
                "",
                "### Defensive resolution",
                "",
                pattern.control,
                "",
                f"**Validation:** {pattern.validation}",
                "",
                f"**Gotcha:** {pattern.gotcha}",
                "",
                f"**Evidence status:** {card.evidence}. Offensive solution: "
                f"**{OUTSIDE_SCOPE}**.",
                "",
                f"**Provenance:** {card.provenance}",
                "",
            ])
    return "\n".join(lines).rstrip() + "\n"


def render_deck(items: list[Card]) -> str:
    blocks: list[str] = []
    total = len(items)
    for pair, card in enumerate(items, 1):
        pattern = pattern_for(card)
        variant_label = f"{card.variants} declared variant(s) · concept-level card"
        meta = [
            "<!-- kind: challenge -->",
            f"<!-- key: {card.key} -->",
            f"<!-- range: {card.range_id} -->",
            f"<!-- pair: {pair}/{total} -->",
            f"<!-- pattern: {card.pattern_id} -->",
        ]
        blocks.append("\n".join([
            *meta,
            f"# {card.title}",
            f"> {card.range_id} · {card.challenge_id} · {card.difficulty} · {variant_label}",
            f"- **DESCRIPTION:** {card.description}",
            f"- **BOUNDARY:** {pattern.boundary}",
            f"- **REVIEW:** {pattern.questions[0]} {pattern.questions[1]}",
            f"- **LEARN:** {pattern.lesson}",
        ]))
        blocks.append("\n".join([
            "<!-- kind: resolution -->",
            f"<!-- key: {card.key} -->",
            f"<!-- range: {card.range_id} -->",
            f"<!-- pair: {pair}/{total} -->",
            f"<!-- pattern: {card.pattern_id} -->",
            f"# Resolution · {card.title}",
            f"> Defensive resolution and review gotchas for {card.range_id} · {card.challenge_id}",
            f"- **CONTROL:** {pattern.control}",
            f"- **VALIDATE:** {pattern.validation}",
            f"- **GOTCHA:** {pattern.gotcha}",
            f"- **STATUS:** Offensive solution {OUTSIDE_SCOPE}. {card.evidence}.",
        ]))

    records = attribution_records()
    for appendix_index, group in enumerate((records[:3], records[3:]), 1):
        rows = [
            f"- **{record['id']}:** {record['maintainer']} · {record['license']} · "
            f"{record['revision']} · {record['repository']}"
            for record in group
        ]
        blocks.append("\n".join([
            "<!-- kind: attribution -->",
            f"<!-- key: attribution/{appendix_index} -->",
            "<!-- range: portfolio -->",
            f"<!-- pair: appendix {appendix_index}/2 -->",
            "<!-- pattern: attribution -->",
            f"# Sources and licences · {appendix_index}/2",
            "> Standalone attribution for the catalog sources represented in this deck",
            *rows,
        ]))
    return "\n\n---\n\n".join(blocks).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the checked-in Markdown differs from catalog-derived output",
    )
    args = parser.parse_args(argv)

    TRAINING.mkdir(parents=True, exist_ok=True)
    items = cards()
    expected = {
        GUIDE: render_guide(items),
        DECK: render_deck(items),
    }
    if args.check:
        drifted = [
            path
            for path, content in expected.items()
            if not path.is_file() or path.read_text() != content
        ]
        if drifted:
            for path in drifted:
                print(f"out of date: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print("learning sources match the catalog and generator")
        return 0

    for path, content in expected.items():
        path.write_text(content)
    print(f"wrote {GUIDE}")
    print(f"wrote {DECK}")
    print(f"cataloged {len(items)} concepts / {sum(card.variants for card in items)} variants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
