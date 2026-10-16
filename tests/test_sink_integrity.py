"""Oracle integrity: only posts carrying the range token count as exploit evidence."""
from __future__ import annotations

from fastapi.testclient import TestClient

from redsec.services.drop import app as drop
from redsec.verify.base import CheckContext
from redsec.verify.builtins import DropContains


class _SinkCtx(CheckContext):
    """A CheckContext that reads events from an in-process sink."""

    def __init__(self, client: TestClient) -> None:
        super().__init__(endpoints={}, drop_url="http://drop")
        self._client = client

    def drop_events(self, *, trusted_only: bool = True):
        events = self._client.get("/events").json()["events"]
        return [e for e in events if e["trusted"]] if trusted_only else events


def _sink(monkeypatch, token: str = "range-token") -> TestClient:
    monkeypatch.setattr(drop, "_TOKEN", token)
    client = TestClient(drop.app)
    client.post("/reset")
    return client


def test_direct_post_is_untrusted_and_does_not_pass(monkeypatch):
    client = _sink(monkeypatch)
    client.post("/collect/mail", json={"body": "MARKER"})
    result = DropContains(needle="MARKER").run(_SinkCtx(client))
    assert not result.passed
    assert "not from a range target" in result.message


def test_target_post_with_token_passes_and_token_is_not_stored(monkeypatch):
    client = _sink(monkeypatch)
    client.post("/collect/mail", json={"body": "MARKER"},
                headers={"X-RedSec-Drop-Token": "range-token"})
    events = client.get("/events").json()["events"]
    assert events[0]["trusted"] is True
    assert "range-token" not in str(events)
    assert DropContains(needle="MARKER").run(_SinkCtx(client)).passed


def test_wrong_or_missing_server_token_is_never_trusted(monkeypatch):
    client = _sink(monkeypatch)
    client.post("/collect", json={"body": "x"}, headers={"X-RedSec-Drop-Token": "guess"})
    unset = _sink(monkeypatch, token="")
    unset.post("/collect", json={"body": "y"}, headers={"X-RedSec-Drop-Token": ""})
    assert [e["trusted"] for e in client.get("/events").json()["events"]] == [False]
    assert [e["trusted"] for e in unset.get("/events").json()["events"]] == [False]
