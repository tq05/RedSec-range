#!/usr/bin/env python3
"""Generate defensive learning sources from RedSec's declarative catalog.

The generator intentionally consumes only repository-owned manifests and catalog
metadata. It does not import third-party application code, copy upstream solution
text, reproduce challenge secrets, or emit operational exploit procedures.
"""
from __future__ import annotations

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
    "transport": DefensivePattern(
         "Identity and request meaning cross proxies, origins, sessions, protocol versions, or downstream services.",
         "Every layer must agree on one canonical request and bind credentials to the intended origin, audience, and session.",
         ("Which layer decides request meaning?", "Are origin, audience, version, and session identifiers bound exactly?"),
         "Canonicalise once, validate exact origins and audiences, use unpredictable sessions, and reject contradictory routing data.",
         "Exercise mismatched headers and metadata with harmless requests and assert that every layer reaches the same deny decision.",
         "A gateway and application can each appear correct while authorising different interpretations of one request.",
    ),
    "supply": DefensivePattern(
         "A model artifact, dataset, adapter, dependency, or registry record crosses the software supply-chain boundary.",
         "AI artifacts can be executable or behavior-changing inputs and need the same provenance controls as software.",
         ("What identity and digest bind the artifact?", "Where is it loaded, merged, trained, or resolved?"),
         "Pin immutable digests, verify signatures and provenance, use safe formats, scan dependencies, and load in isolation.",
         "Confirm allow-listed sources and digests with benign fixtures, then fail closed on unknown or mutable artifacts.",
         "A familiar filename, package name, or model label is not proof of origin or safe behavior.",
    ),
    "dos": DefensivePattern(
         "Attacker-controlled work crosses compute, memory, token, concurrency, or financial budget boundaries.",
         "Availability and spend are security properties that require explicit per-request and aggregate budgets.",
         ("Which resource grows with input?", "Where are tenant, tool, and global budgets enforced?"),
         "Set timeouts, size and token limits, concurrency quotas, rate limits, cancellation, and cost telemetry.",
         "Use bounded synthetic workloads to assert predictable rejection before resource use approaches operational limits.",
         "Per-request limits alone miss distributed or repeated consumption across sessions and identities.",
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


BUILTIN_PATTERN_IDS = {
    "direct-injection": "prompt",
    "indirect-injection": "prompt",
    "recon": "recon",
    "tool-abuse": "agency",
    "memory": "prompt",
    "a2a-trust": "identity",
    "a2a-message/send": "identity",
    "a2a-message-identity": "identity",
    "a2a-context": "session-context",
    "rag-source": "rag",
    "rag-retrieval": "rag",
    "rag-trust": "rag",
    "embedding-inversion": "embeddings",
    "embedding-mia": "embeddings",
    "embedding-collision": "embeddings",
    "tools": "mcp",
    "resources": "sink",
    "prompts": "prompt",
    "sampling": "mcp",
    "roots": "scope",
    "elicitation": "mcp",
    "logging": "secrets",
    "completion": "secrets",
    "tools (rug-pull)": "mcp",
    "tools (rce)": "sink",
    "streamable-http-routing": "transport",
    "tools (concealment)": "mcp",
    "supply-weights": "supply",
    "supply-data": "supply",
    "supply-adapter": "supply",
    "supply-deps": "supply",
    "infra-ssrf": "infra",
    "infra-api": "infra",
    "infra-secrets": "secrets",
    "tm-assets": "threat",
    "tm-boundaries": "threat",
    "tm-paths": "threat",
    "chain-access": "chain",
    "chain-pivot": "chain",
    "chain-exfil": "chain",
}

EXTERNAL_CATEGORY_PATTERN_IDS = {
    "data-exfiltration": "secrets",
    "prompt-injection": "prompt",
    "jailbreak": "prompt",
    "context-manipulation": "prompt",
    "mcp-exploitation": "mcp",
    "memory-injection": "prompt",
    "context-overflow": "prompt",
    "tool-registry-poisoning": "mcp",
    "tool-mitm": "transport",
    "mixed": "chain",
    "agent-to-agent": "identity",
    "MCP-specific": "mcp",
    "Prompt/Context": "prompt",
    "Injection sink": "sink",
    "AuthN/AuthZ": "identity",
    "Secrets/Exposure": "secrets",
    "Transport": "transport",
    "DoS/Cost": "dos",
    "Supply chain": "supply",
    "Attack chain": "chain",
    "Path traversal / code execution": "sink",
    "Tool output poisoning": "mcp",
    "Remote content injection": "prompt",
}

CHALLENGE_PATTERN_OVERRIDES = {
    "dvaa/L2-03": "sink",
    "dvaa/L2-05": "secrets",
    "dvaa/L3-02": "infra",
    "mcpgoat/D3": "infra",
}


def pattern_id_for(range_id: str, challenge_id: str, category: str) -> str:
    key = f"{range_id}/{challenge_id}"
    if key in CHALLENGE_PATTERN_OVERRIDES:
        return CHALLENGE_PATTERN_OVERRIDES[key]
    mapping = BUILTIN_PATTERN_IDS if range_id == "builtin" else EXTERNAL_CATEGORY_PATTERN_IDS
    try:
        return mapping[category]
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

    if len(result) != 110 or sum(card.variants for card in result) != 162:
        raise SystemExit(
            f"unexpected catalog size: {len(result)} concepts / "
            f"{sum(card.variants for card in result)} variants"
        )
    return result


def render_guide(items: list[Card]) -> str:
    lines = [
        "---",
        'title: "RedSec Range — Defensive Challenge Learning Guide"',
        'subtitle: "110 concepts · 162 variants · architecture, review, and remediation"',
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
        "# Portfolio map",
        "",
        "| Range | Concepts | Variants | Evidence meaning |",
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
                f"**Variants:** {card.variants}",
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
            f"> {card.range_id} · {card.challenge_id} · {card.difficulty} · {card.variants} variant(s)",
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
    return "\n\n---\n\n".join(blocks).rstrip() + "\n"


def main() -> int:
    TRAINING.mkdir(parents=True, exist_ok=True)
    items = cards()
    GUIDE.write_text(render_guide(items))
    DECK.write_text(render_deck(items))
    print(f"wrote {GUIDE}")
    print(f"wrote {DECK}")
    print(f"cataloged {len(items)} concepts / {sum(card.variants for card in items)} variants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
