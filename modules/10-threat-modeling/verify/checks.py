"""Module-10 custom check: score a submitted threat model (artifact) for coverage.

Demonstrates the *artifact* verification pattern: the learner submits a document
(markdown/JSON) and the verifier checks it covers the required elements, rather
than looking for a flag or a side effect.
"""
from __future__ import annotations

import re

from redsec.verify.base import Check, CheckContext, CheckResult


_WORD_RE = re.compile(r"\b[\w'-]+\b")
_ENTRY_RE = re.compile(r"^\s*(?P<marker>[-*+]|\d+[.)])\s+(?P<body>.+)$")


def _entries(text: str) -> list[tuple[str, str]]:
    """Return Markdown list entries, joining wrapped continuation lines."""
    entries: list[tuple[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = _ENTRY_RE.match(raw_line)
        if match:
            entries.append((match.group("marker"), match.group("body").strip()))
        elif entries:
            marker, body = entries[-1]
            entries[-1] = (marker, f"{body} {line}")
    return entries


class ArtifactCovers(Check):
    """Score both topical coverage and basic threat-model structure.

    Term matching is case-insensitive substring matching. Structural parameters
    make a comma-separated keyword dump insufficient: entries must be Markdown
    bullets/numbered items, relations must co-occur within an entry, and attack
    chains use ``->`` between steps.
    """

    id = "artifact-covers"
    description = "threat-model artifact covers the required elements"

    def run(self, ctx: CheckContext) -> CheckResult:
        text = (ctx.artifact or "").lower()
        if not text:
            return CheckResult.fail("no artifact submitted "
                                    "(use `redsec verify 10 <chal> --artifact-file FILE`)")
        all_of = [t.lower() for t in self.params.get("all_of", [])]
        missing = [t for t in all_of if t not in text]
        any_of = [t.lower() for t in self.params.get("any_of", [])]
        min_matches = self.params.get("min_matches", len(any_of))
        any_hits = [t for t in any_of if t in text]
        entries = _entries(text)
        numbered_entries = [entry for marker, entry in entries if marker[0].isdigit()]
        word_count = len(_WORD_RE.findall(text))

        min_words = int(self.params.get("min_words", 0))
        min_entries = int(self.params.get("min_entries", 0))
        min_numbered = int(self.params.get("min_numbered_entries", 0))

        relations = [
            [str(term).lower() for term in relation]
            for relation in self.params.get("required_relations", [])
        ]
        missing_relations = [
            relation for relation in relations
            if not any(all(term in entry.lower() for term in relation)
                       for _, entry in entries)
        ]

        min_chains = int(self.params.get("min_chains", 0))
        min_chain_steps = int(self.params.get("min_chain_steps", 2))
        chains = [
            entry for _, entry in entries
            if entry.count("->") + 1 >= min_chain_steps
        ]

        structural_errors: list[str] = []
        if word_count < min_words:
            structural_errors.append(f"words {word_count}/{min_words}")
        if len(entries) < min_entries:
            structural_errors.append(f"list entries {len(entries)}/{min_entries}")
        if len(numbered_entries) < min_numbered:
            structural_errors.append(
                f"numbered entries {len(numbered_entries)}/{min_numbered}"
            )
        if missing_relations:
            structural_errors.append(f"missing same-entry relations {missing_relations}")
        if len(chains) < min_chains:
            structural_errors.append(f"multi-step chains {len(chains)}/{min_chains}")

        ok = (not missing and (not any_of or len(any_hits) >= min_matches)
              and not structural_errors)
        if ok:
            return CheckResult.ok(
                "artifact covers the required elements with sufficient structure",
                matched_any=any_hits,
                words=word_count,
                entries=len(entries),
                chains=len(chains),
            )
        return CheckResult.fail(
            f"missing required: {missing}; any_of hits {len(any_hits)}/{min_matches}; "
            f"structure: {structural_errors}",
            missing=missing,
            structural_errors=structural_errors,
        )
