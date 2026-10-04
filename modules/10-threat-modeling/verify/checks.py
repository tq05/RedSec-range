"""Module-10 custom check: score a submitted threat model (artifact) for coverage.

Demonstrates the *artifact* verification pattern: the learner submits a document
(markdown/JSON) and the verifier checks it covers the required elements, rather
than looking for a flag or a side effect.
"""
from __future__ import annotations

from redsec.verify.base import Check, CheckContext, CheckResult


class ArtifactCovers(Check):
    """Pass if the submitted artifact mentions all required terms (and, optionally,
    at least ``min_matches`` of an ``any_of`` set).

    Params: ``all_of`` (list[str]), ``any_of`` (list[str]), ``min_matches`` (int).
    Matching is case-insensitive substring.
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
        ok = not missing and (not any_of or len(any_hits) >= min_matches)
        if ok:
            return CheckResult.ok("artifact covers the required elements",
                                  matched_any=any_hits)
        return CheckResult.fail(
            f"missing required: {missing}; any_of hits {len(any_hits)}/{min_matches}",
            missing=missing)
