from pathlib import Path

import pytest

from redsec import ranges
from redsec.range_catalog import load_catalog


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_contains_builtin_external_and_offsec_placeholder():
    catalog = load_catalog()

    assert set(catalog.ranges) == {
        "builtin", "offsec", "dvaa", "mcpgoat", "dvmcp", "appsecco-mcp"
    }
    assert catalog.ranges["builtin"].runtime.driver == "builtin"
    assert catalog.ranges["offsec"].availability == "placeholder"
    assert catalog.ranges["offsec"].runtime.driver == "placeholder"
    assert catalog.resolve("appsecco").id == "appsecco-mcp"
    assert catalog.resolve("mcp-goat").id == "mcpgoat"


def test_external_sources_are_immutable_and_host_ports_do_not_overlap():
    catalog = load_catalog()
    ports = []

    for definition in catalog.ranges.values():
        if definition.source:
            assert len(definition.source.revision) == 40
            assert definition.source.repository.startswith("https://github.com/")
        ports.extend(port.host for port in definition.runtime.ports)

    assert len(ports) == len(set(ports))
    assert catalog.ranges["dvmcp"].runtime.ports[-1].host == 19010


def test_enabled_profile_resolves_aliases_and_rejects_placeholder(tmp_path, monkeypatch):
    monkeypatch.setenv("REDSEC_STATE", str(tmp_path))

    enabled = ranges.set_enabled(["damn-vulnerable-ai-agent", "appsecco"], enable=True)
    assert enabled == ["builtin", "dvaa", "appsecco-mcp"]
    assert ranges.load_state()["enabled"] == enabled

    with pytest.raises(ranges.RangeLifecycleError, match="placeholder"):
        ranges.set_enabled(["offsec"], enable=True)


def test_external_up_uses_private_ports_and_an_internal_network(tmp_path, monkeypatch):
    monkeypatch.setenv("REDSEC_STATE", str(tmp_path))
    definition = load_catalog().ranges["mcpgoat"]
    calls = []

    monkeypatch.setattr(ranges, "build_external", lambda *_args, **_kwargs: ("image:test", "a" * 40))
    monkeypatch.setattr(ranges, "_wait_port", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(
        ranges, "_run",
        lambda args, **_kwargs: calls.append(args) or "",
    )

    result = ranges.up_one(definition)

    assert ["docker", "network", "create", "--internal", "redsec-ext-mcpgoat"] in calls
    run = next(command for command in calls if command[:2] == ["docker", "run"])
    assert "127.0.0.1:7332:7332" in run
    assert result["endpoints"] == {"control-panel": "http://127.0.0.1:7332/"}


def test_appsecco_adapter_packages_network_and_stdio_servers():
    definition = load_catalog().ranges["appsecco-mcp"]
    dockerfile = (ROOT / definition.runtime.dockerfile).read_text()

    assert {port.name for port in definition.runtime.ports} == {
        "indirect-injection-sse", "wikipedia-streamable"
    }
    assert definition.runtime.ports[0].path == "/mcp"
    assert len(definition.runtime.entrypoints) == 7
    assert "filesystem-workspace-actions" in definition.runtime.entrypoints
    assert "npm ci" in dockerfile
    assert "mcp==1.24.0" in dockerfile
    assert "wikipedia-mcp.py" in dockerfile


def test_external_build_explains_when_docker_is_missing(monkeypatch):
    definition = load_catalog().ranges["mcpgoat"]
    monkeypatch.setattr(ranges.shutil, "which", lambda _command: None)

    with pytest.raises(ranges.RangeLifecycleError, match="Docker is required"):
        ranges.build_external(definition)
