"""Module-05 custom check: confirm attacker content is cited as a trusted source."""
from __future__ import annotations

from redsec.verify.base import Check, CheckContext, CheckResult


class CitationSpoofed(Check):
    """Active oracle: ask the victim question and confirm the assistant cites the
    attacker's spoofed authoritative source and surfaces the attacker's content.

    Fail-before safe: before the attacker ingests the doc, it isn't retrieved, so
    neither the source nor the needle appears.
    """

    id = "citation-spoofed"
    description = "attacker content is cited under a trusted-looking source"

    def run(self, ctx: CheckContext) -> CheckResult:
        q = self.params["question"]
        src = self.params["source_contains"].lower()
        needle = self.params["needle"].lower()
        with ctx.client() as c:
            r = c.post(ctx.base("rag") + "/chat", json={"message": q, "top_k": 2})
        data = r.json()
        sources = data.get("used_sources", [])
        cited = any(src in s.get("source", "").lower() for s in sources)
        surfaced = needle in str(data).lower()
        if cited and surfaced:
            return CheckResult.ok("attacker source cited and content surfaced",
                                  sources=[s["source"] for s in sources])
        return CheckResult.fail(
            f"not yet (cited={cited}, surfaced={surfaced})",
            sources=[s.get("source") for s in sources])
