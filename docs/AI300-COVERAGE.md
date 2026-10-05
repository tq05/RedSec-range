# AI-300 coverage and course-quality baseline

This document is the product-level traceability record for RedSec Range. It maps
the public OffSec **Advanced AI Red Teaming (AI-300)** syllabus to implemented,
self-verifying labs and records where this course deliberately goes deeper.

Source reviewed: [OffSec AI-300 public syllabus supplied for this audit](https://cdn.sanity.io/files/t7y0tkf4/production/024258d4bfacd78f94e3565a3657894842f68061.pdf?dl=AI-300_Syllabus.pdf)
(11 modules, retrieved 2026-10-04). The public syllabus is a high-level outline;
matching it does not make this project an OffSec course or guarantee exam coverage.
RedSec Range is independent and is not affiliated with OffSec.

## Coverage decision

All 11 public syllabus modules have a one-to-one implemented module. Every module
has a lesson, one or more live or artifact-scored challenges, a verifier, and a
reference solution exercised by the fail-before/pass-after integration suite.

| AI-300 area | RedSec evidence | Coverage |
|---|---|---|
| 1. AI red-team foundations and lifecycle | Module 01 explains the distinct attack surface, taxonomies, lifecycle, ethics and range workflow; `first-contact` demonstrates the first injection | Covered |
| 2. Reconnaissance for AI targets | Module 02 fingerprints model/provider metadata, enumerates an undocumented surface and turns verbose errors into configuration disclosure | Covered |
| 3. Attacking AI agents | Module 03 covers direct and indirect prompt injection, excessive tool agency, secret exfiltration and persistent memory poisoning | Covered |
| 4. Multi-agent systems and A2A | Module 04 covers transitive trust and a version-pinned A2A JSON-RPC model: Agent Card discovery, Messages/Parts, Tasks, `message/send`, `tasks/get`, sender impersonation and `contextId` session smuggling | Covered and extended |
| 5. RAG pipelines | Module 05 covers knowledge poisoning, retrieval ranking manipulation and trusted-looking citation spoofing | Covered |
| 6. Embeddings | Module 06 covers reference-corpus source reconstruction, membership inference and collisions using a deterministic teaching embedding | Covered; reconstruction method and mathematics are intentionally simplified |
| 7. MCP and tool surfaces | Module 07 covers the 2025 tools/resources/prompts/sampling/roots/elicitation/logging/completion surface, tool poisoning, rug-pull and RCE, plus 2026 stateless discovery and Streamable HTTP routing-policy desynchronization | Covered and extended |
| 8. AI/ML supply chain | Module 08 covers unsafe weight deserialization, poisoned datasets, backdoored adapters and dependency confusion | Covered |
| 9. Infrastructure and deployment | Module 09 covers metadata SSRF, unauthenticated model administration and secrets in model-registry metadata | Covered |
| 10. Threat modeling | Module 10 scores structured asset inventory, same-entry trust relationships and ranked multi-stage attack paths as artifacts | Covered |
| 11. Capstone engagement | Module 11 composes indirect injection, ambient authority, internal vault pivoting and crown-jewel exfiltration | Covered |

## Challenge quality contract

A challenge is course-ready only when all of the following are true:

1. Its objective names a concrete security outcome rather than a trivia answer.
2. Its target behavior demonstrates the stated failure mode.
3. Its verifier fails before exploitation and passes after the reference exploit;
   written artifacts must also meet structural requirements rather than list keywords.
4. It has a learning tier and progressive hints; impossible-tier answers are sealed.
5. Its lesson explains the concept, walkthrough boundary and defensive control.
6. It maps to the AI-300 module and uses OWASP/ATLAS mappings only where supportable.
7. Dangerous behavior is planted with canary data and documented for isolated use.

The test suite enforces the structural parts of this contract. Human review remains
necessary for conceptual fidelity; a green verifier proves reproducibility, not
that a simulation perfectly matches every production implementation.

## Protocol version policy

Protocol labs must state what they implement. A2A and MCP evolve too quickly for an
unversioned claim such as “the protocol has these exact methods” to stay accurate.

- **A2A:** Module 04 pins the teaching wire format to the v0.3 JSON-RPC binding while
  emphasizing stable concepts: Agent Cards, Messages, Parts, Tasks, context, auth,
  identity and provenance. Learners should consult the current A2A binding before a
  production assessment ([current specification](https://a2aproject.github.io/A2A/latest/specification/)).
- **MCP:** Module 07 labels its original surface matrix as MCP 2025-06-18. It also
  teaches the 2026-07-28 stateless discovery and Streamable HTTP routing model and
  calls out the deprecation of roots, sampling and logging
  ([current architecture](https://modelcontextprotocol.io/docs/learn/architecture)).

## Current scope and remaining depth

The current baseline is **11 modules, 43 challenges and 8,650 points**. The project
fully covers the public syllabus topics, but “fully covered” here means the public
objectives have practical evidence. It does not mean every possible attack variant
or private course exercise is reproduced.

The highest-value future depth remains:

- MCP OAuth/token passthrough and cross-server tool shadowing;
- A2A task ownership, push-notification SSRF and cross-tenant context isolation;
- harder guarded variants for agents, RAG, supply chain, infrastructure and the
  capstone, following `DIFFICULTY-TIERS.md`;
- stronger oracle integrity and instructor rubrics for judging analytical depth,
  tracked in `ROADMAP.md`.
