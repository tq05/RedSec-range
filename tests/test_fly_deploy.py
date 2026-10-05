"""Contract tests for the private Fly.io deployment path."""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLY = ROOT / "deploy" / "fly"


def test_port_publication_is_private_by_default(monkeypatch, tmp_path):
    monkeypatch.setenv("REDSEC_STATE", str(tmp_path))
    spec = importlib.util.spec_from_file_location(
        "range_ctl", ROOT / "scripts" / "range_ctl.py"
    )
    assert spec and spec.loader
    range_ctl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(range_ctl)

    monkeypatch.delenv("REDSEC_BIND_HOST", raising=False)
    assert range_ctl.publish_arg(9070, 9070) == "127.0.0.1:9070:9070"

    monkeypatch.setenv("REDSEC_BIND_HOST", "all")
    assert range_ctl.publish_arg(9070, 9070) == "9070:9070"


def test_fly_config_has_no_public_service_and_stops_on_ttl():
    config = tomllib.loads((FLY / "fly.toml").read_text())
    assert "services" not in config
    assert "http_service" not in config
    assert config["env"]["REDSEC_BIND_HOST"] == "all"
    assert config["env"]["REDSEC_RANGES"] == "builtin"
    assert config["vm"][0]["persist_rootfs"] == "restart"
    assert config["vm"][0]["size"] == "shared-cpu-2x"
    assert config["vm"][0]["memory"] == "4gb"
    assert config["restart"][0]["policy"] == "never"
    assert config["build"]["dockerfile"] == "Dockerfile"


def test_fly_shell_entrypoints_parse_and_help_without_credentials():
    scripts = sorted(FLY.glob("*.sh")) + [ROOT / "scripts" / "sandbox-up.sh"]
    subprocess.run(["bash", "-n", *map(str, scripts)], check=True)
    for name in ("up.sh", "down.sh"):
        result = subprocess.run(
            ["bash", str(FLY / name), "--help"],
            check=True,
            capture_output=True,
            text=True,
        )
        assert "Usage:" in result.stdout


def test_docker_context_excludes_local_credentials_and_state():
    ignored = set((ROOT / ".dockerignore").read_text().splitlines())
    assert {".env", ".env.*", ".redsec", ".aws", ".fly", "*.key"} <= ignored


def test_repository_root_has_no_public_fly_launch_configuration():
    assert not (ROOT / "fly.toml").exists()
    assert not (ROOT / "Dockerfile").exists()


def test_up_script_creates_unique_app_and_persists_harness_state(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    calls = tmp_path / "calls"
    fly = fake_bin / "fly"
    fly.write_text(
        """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$FAKE_FLY_CALLS"
if [ "$1" = status ]; then exit 1; fi
exit 0
"""
    )
    fly.chmod(0o755)
    state = tmp_path / "fly.json"
    env = {
        **os.environ,
        "PATH": f"{fake_bin}:{os.environ['PATH']}",
        "FAKE_FLY_CALLS": str(calls),
        "REDSEC_FLY_STATE": str(state),
    }

    result = subprocess.run(
        [
            str(FLY / "up.sh"), "--region", "lhr", "--modules", "01",
            "--ranges", "builtin mcpgoat", "--json",
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    output = json.loads(result.stdout)
    saved = json.loads(state.read_text())
    assert output["ready"] is True
    assert output["app"].startswith("redsec-range-")
    assert saved["app"] == output["app"]
    commands = calls.read_text()
    assert f"apps create {output['app']} --yes" in commands
    assert f"deploy {ROOT} --app {output['app']}" in commands
    assert "--env REDSEC_RANGES=builtin mcpgoat" in commands
    assert f"ssh console --quiet --app {output['app']}" in commands


def test_failed_first_deploy_destroys_new_app_and_clears_state(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    calls = tmp_path / "calls"
    fly = fake_bin / "fly"
    fly.write_text(
        """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$FAKE_FLY_CALLS"
if [ "$1" = status ] || [ "$1" = deploy ]; then exit 1; fi
exit 0
"""
    )
    fly.chmod(0o755)
    state = tmp_path / "fly.json"
    env = {
        **os.environ,
        "PATH": f"{fake_bin}:{os.environ['PATH']}",
        "FAKE_FLY_CALLS": str(calls),
        "REDSEC_FLY_STATE": str(state),
    }

    result = subprocess.run(
        [str(FLY / "up.sh"), "--modules", "01", "--json"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "deployment failed; removing newly-created app" in result.stderr
    assert "apps destroy redsec-range-" in calls.read_text()
    assert not state.exists()
