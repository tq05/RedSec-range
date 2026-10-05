from pathlib import Path
import json

import pytest
from typer.testing import CliRunner

from redsec import ranges
from redsec.cli import app
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


def test_every_external_challenge_is_cataloged_with_solution_provenance():
    catalog = load_catalog()
    expected = {"dvaa": 22, "mcpgoat": 26, "dvmcp": 10, "appsecco-mcp": 9}

    for range_id, count in expected.items():
        curriculum = catalog.ranges[range_id].curriculum
        assert len(curriculum.challenges) == count
        assert curriculum.solution_status == "upstream"
        assert curriculum.solution_url
        assert len({challenge.id for challenge in curriculum.challenges}) == count

    mcpgoat = catalog.ranges["mcpgoat"].curriculum.challenges
    assert sum(challenge.variants for challenge in mcpgoat) == 78


def test_challenge_catalog_cli_lists_all_ranges_as_json():
    result = CliRunner().invoke(app, ["ranges", "challenges", "--json"])

    assert result.exit_code == 0, result.output
    rows = json.loads(result.stdout)
    assert len(rows) == 110
    assert {row["range"] for row in rows} == {
        "builtin", "dvaa", "mcpgoat", "dvmcp", "appsecco-mcp"
    }
    assert any(
        row["range"] == "dvaa" and row["id"] == "L4-02"
        for row in rows
    )


def test_status_marks_local_update_beyond_catalog_as_curriculum_drift(tmp_path, monkeypatch):
    monkeypatch.setenv("REDSEC_STATE", str(tmp_path))
    state = ranges.load_state()
    state["revisions"]["mcpgoat"] = "f" * 40
    ranges.save_state(state)

    row = next(item for item in ranges.status_rows() if item["id"] == "mcpgoat")
    assert row["catalog_revision"] == load_catalog().ranges["mcpgoat"].source.revision
    assert row["revision"] == "f" * 40
    assert row["curriculum_current"] is False


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
    monkeypatch.setattr(ranges, "_proxy_image", lambda: "gateway:test")
    monkeypatch.setattr(ranges, "_wait_port", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(
        ranges, "_run",
        lambda args, **_kwargs: calls.append(args) or "",
    )

    result = ranges.up_one(definition)

    assert ["docker", "network", "create", "--internal", "redsec-ext-mcpgoat"] in calls
    assert ["docker", "network", "create", "redsec-ext-mcpgoat-access"] in calls
    runs = [command for command in calls if command[:2] == ["docker", "run"]]
    target, gateway = runs
    assert "127.0.0.1:7332:7332" not in target
    assert "127.0.0.1:7332:7332" in gateway
    assert "TARGET_HOST=redsec-ext-mcpgoat" in gateway
    assert [
        "docker", "network", "connect", "redsec-ext-mcpgoat",
        "redsec-ext-mcpgoat-gateway",
    ] in calls
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


def test_external_ci_enumerates_challenges_and_runs_native_regression():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text()

    assert "/api/challenges" in workflow
    assert "len(x) == 22" in workflow
    assert "seq 19001 19010" in workflow
    assert "npm run ci" in workflow
    assert "REDSEC_STATE: ${{ github.workspace }}/.redsec" in workflow
    assert 'node-version: "22"' in workflow
    assert "Initialize every Appsecco stdio MCP server" in workflow
    assert "protocolVersion" in workflow
    assert "generate_challenge_catalog.py --check" in workflow


def test_external_build_explains_when_docker_is_missing(monkeypatch):
    definition = load_catalog().ranges["mcpgoat"]
    monkeypatch.setattr(ranges.shutil, "which", lambda _command: None)

    with pytest.raises(ranges.RangeLifecycleError, match="Docker is required"):
        ranges.build_external(definition)
