"""Vulnerable ports publish on loopback unless exposure is explicitly acknowledged."""
from __future__ import annotations

import pytest

from redsec import config, ranges


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    for name in ("REDSEC_BIND_HOST", "REDSEC_ALLOW_PUBLIC_BIND", "CODESPACES"):
        monkeypatch.delenv(name, raising=False)


def test_loopback_is_the_default_and_needs_no_override(monkeypatch):
    assert config.publish_spec(9030, 9030) == "127.0.0.1:9030:9030"
    monkeypatch.setenv("REDSEC_BIND_HOST", "127.0.0.2")
    assert config.publish_spec(9030, 9030) == "127.0.0.2:9030:9030"


@pytest.mark.parametrize("bind", ["all", "0.0.0.0", "192.168.1.20"])
def test_non_loopback_requires_explicit_override(monkeypatch, bind):
    monkeypatch.setenv("REDSEC_BIND_HOST", bind)
    with pytest.raises(config.PublicBindError):
        config.publish_spec(9030, 9030)
    monkeypatch.setenv("REDSEC_ALLOW_PUBLIC_BIND", "1")
    assert config.publish_spec(9030, 9030).endswith("9030:9030")


def test_codespaces_refuses_public_bind_even_with_override(monkeypatch):
    monkeypatch.setenv("CODESPACES", "true")
    monkeypatch.setenv("REDSEC_BIND_HOST", "all")
    monkeypatch.setenv("REDSEC_ALLOW_PUBLIC_BIND", "1")
    with pytest.raises(config.PublicBindError):
        config.publish_spec(9030, 9030)


def test_external_ranges_surface_a_lifecycle_error(monkeypatch):
    monkeypatch.setenv("REDSEC_BIND_HOST", "all")
    with pytest.raises(ranges.RangeLifecycleError):
        ranges._publish(9000, 9000)
