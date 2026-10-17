"""Reusable checks available to every module via `builtins:Name`."""
from __future__ import annotations

from .base import Check, CheckContext, CheckResult, flag_matches


class FlagCheck(Check):
    """Compare the learner's submitted flag to an expected value.

    Params: ``flag`` (plaintext) and/or ``flag_sha256``.
    """

    id = "flag"
    description = "submitted flag matches expected value"

    def run(self, ctx: CheckContext) -> CheckResult:
        if flag_matches(
            ctx.submitted_flag,
            expected=self.params.get("flag"),
            expected_sha256=self.params.get("flag_sha256"),
        ):
            return CheckResult.ok("flag accepted")
        return CheckResult.fail("flag incorrect or missing")


class DropContains(Check):
    """Oracle: success iff the exfil sink received ``needle``.

    Params: ``needle`` (string that must appear in a sink event).
    """

    id = "drop-contains"
    description = "exfiltration sink received the target value"

    def run(self, ctx: CheckContext) -> CheckResult:
        needle = self.params.get("needle", "")
        if not needle:
            return CheckResult.fail("misconfigured check: no 'needle'")
        if ctx.drop_contains(needle):
            return CheckResult.ok(
                "sink received the exfiltrated value", needle=needle
            )
        if ctx.drop_forged(needle):
            return CheckResult.fail(
                "the value reached the sink, but not from a range target; make the "
                "target send it", needle=needle,
            )
        return CheckResult.fail(
            "sink has not received the value yet", needle=needle,
            events=len(ctx.drop_events()),
        )


class HttpContains(Check):
    """Oracle: GET ``path`` on ``target`` and assert ``needle`` is present."""

    id = "http-contains"
    description = "endpoint response contains the expected marker"

    def run(self, ctx: CheckContext) -> CheckResult:
        target = self.params["target"]
        path = self.params.get("path", "/")
        needle = self.params.get("needle", "")
        with ctx.client() as c:
            r = c.get(ctx.base(target) + path)
        if needle.lower() in r.text.lower():
            return CheckResult.ok("marker present", status=r.status_code)
        return CheckResult.fail("marker absent", status=r.status_code)


BUILTINS: dict[str, type[Check]] = {
    "FlagCheck": FlagCheck,
    "DropContains": DropContains,
    "HttpContains": HttpContains,
}
