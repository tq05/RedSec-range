"""Instantiate and run the checks declared on a challenge."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..models import Challenge, VerifyStep
from .base import Check, CheckContext, CheckResult


@dataclass
class StepOutcome:
    step: VerifyStep
    result: CheckResult


@dataclass
class ChallengeOutcome:
    challenge: Challenge
    outcomes: list[StepOutcome]

    @property
    def passed(self) -> bool:
        return bool(self.outcomes) and all(o.result.passed for o in self.outcomes)


def _instantiate(module_dir: Path, step: VerifyStep) -> Check:
    from ..loader import load_check
    from .builtins import FlagCheck

    if step.check:
        obj = load_check(module_dir, step.check)
        # Allow either a Check subclass or a bare callable returning a Check.
        if isinstance(obj, type) and issubclass(obj, Check):
            return obj(**step.params)
        if callable(obj):
            inst = obj(**step.params)  # type: ignore[call-arg]
            if isinstance(inst, Check):
                return inst
        raise TypeError(f"check {step.check!r} is not a Check")
    # Default: a flag check using the step's expected flag.
    params = dict(step.params)
    if step.flag:
        params.setdefault("flag", step.flag)
    return FlagCheck(**params)


def run_challenge(
    module_dir: Path, challenge: Challenge, ctx: CheckContext
) -> ChallengeOutcome:
    outcomes: list[StepOutcome] = []
    for step in challenge.verify:
        try:
            check = _instantiate(module_dir, step)
            result = check.run(ctx)
        except Exception as e:  # a failing check must never crash the runner
            result = CheckResult.fail(f"check error: {e}")
        outcomes.append(StepOutcome(step=step, result=result))
    return ChallengeOutcome(challenge=challenge, outcomes=outcomes)
