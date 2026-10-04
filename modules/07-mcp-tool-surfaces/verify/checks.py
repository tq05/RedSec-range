"""Module-07 custom checks.

Demonstrates the module-authoring pattern: drop a ``Check`` subclass in
``verify/`` and reference it from ``module.yaml`` as ``checks:HostExfil``.

``HostExfil`` is an *oracle*: it confirms that an exploit's side effect reached
the shared sink, keyed by a per-vector marker the server/host prepends. It is
"fail-before safe" -- before the exploit runs the sink is empty, so selftest can
assert fail -> pass.
"""
from __future__ import annotations

from redsec.verify.base import Check, CheckContext, CheckResult


class HostExfil(Check):
    """Success iff the exfil sink saw an event containing ``needle``."""

    id = "host-exfil"
    description = "host-side exploit reached the exfiltration sink"

    def run(self, ctx: CheckContext) -> CheckResult:
        needle = self.params.get("needle", "")
        if not needle:
            return CheckResult.fail("misconfigured: no needle")
        matches = [e for e in ctx.drop_events()
                   if needle.lower() in str(e).lower()]
        if matches:
            return CheckResult.ok(
                f"sink captured {needle!r} ({len(matches)} event(s))",
                sample=matches[-1].get("body", "")[:200])
        return CheckResult.fail(
            f"sink has not captured {needle!r}", events=len(ctx.drop_events()))
