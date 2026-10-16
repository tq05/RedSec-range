"""Core verification types.

Three verification patterns are supported, which between them cover every module:

* **flag**   -- the exploit reveals a canary string the learner submits.
* **oracle** -- the verifier observes a *side effect* of the exploit (a secret
                landing in the exfil sink, a privileged action logged, a tampered
                record) and decides success itself. No submission required.
* **artifact** -- the learner supplies a produced artifact (an extracted system
                prompt, an inverted embedding) and the verifier scores it.

A check is any object with a ``run(ctx) -> CheckResult``. Subclass
:class:`Check` for module-specific logic; simple flag checks use the builtin.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class CheckResult:
    passed: bool
    message: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, message: str = "", **evidence: Any) -> "CheckResult":
        return cls(True, message or "verified", evidence)

    @classmethod
    def fail(cls, message: str, **evidence: Any) -> "CheckResult":
        return cls(False, message, evidence)


@dataclass
class CheckContext:
    """Everything a check needs, independent of where targets are deployed."""

    endpoints: dict[str, str]  # target name -> base URL (local or k8s-resolved)
    drop_url: str | None = None  # the shared exfil sink, if deployed
    submitted_flag: str | None = None
    artifact: str | None = None  # learner-supplied artifact (artifact checks)
    params: dict[str, Any] = field(default_factory=dict)
    timeout: float = 15.0

    def base(self, target: str) -> str:
        if target not in self.endpoints:
            raise KeyError(
                f"target {target!r} not resolved; have {list(self.endpoints)}"
            )
        return self.endpoints[target].rstrip("/")

    def client(self) -> httpx.Client:
        return httpx.Client(timeout=self.timeout, follow_redirects=True)

    # -- sink helpers ----------------------------------------------------------
    def drop_events(self, *, trusted_only: bool = True) -> list[dict[str, Any]]:
        """Sink events; by default only those a range target sent with the token."""
        if not self.drop_url:
            return []
        with self.client() as c:
            r = c.get(f"{self.drop_url.rstrip('/')}/events")
            r.raise_for_status()
            events = r.json().get("events", [])
        if trusted_only:
            events = [ev for ev in events if ev.get("trusted") is True]
        return events

    def drop_contains(self, needle: str) -> bool:
        needle = needle.lower()
        for ev in self.drop_events():
            if needle in str(ev).lower():
                return True
        return False

    def drop_forged(self, needle: str) -> bool:
        """True if ``needle`` reached the sink only in untrusted (direct) posts."""
        needle = needle.lower()
        return any(needle in str(ev).lower()
                   for ev in self.drop_events(trusted_only=False)
                   if ev.get("trusted") is not True)


class Check:
    """Base class for module-defined checks."""

    id: str = "check"
    description: str = ""

    def __init__(self, **params: Any) -> None:
        self.params = params

    def run(self, ctx: CheckContext) -> CheckResult:  # pragma: no cover - abstract
        raise NotImplementedError


# -- flag utilities ------------------------------------------------------------
FLAG_RE = re.compile(r"REDSEC\{[^}]+\}")


def norm_flag(s: str | None) -> str:
    return (s or "").strip()


def flag_matches(submitted: str | None, expected: str | None = None,
                 expected_sha256: str | None = None) -> bool:
    sub = norm_flag(submitted)
    if not sub:
        return False
    if expected is not None and sub == norm_flag(expected):
        return True
    if expected_sha256 is not None:
        return hashlib.sha256(sub.encode()).hexdigest() == expected_sha256.lower()
    return False


def extract_flag(text: str) -> str | None:
    m = FLAG_RE.search(text or "")
    return m.group(0) if m else None
