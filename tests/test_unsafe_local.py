"""Bare local mode refuses RCE/SSRF modules unless the learner opts in."""
from __future__ import annotations

from typer.testing import CliRunner

from redsec import cli
from redsec.loader import load_all


def test_only_isolation_modules_are_gated():
    gated = {m.id for _, m in load_all() if m.local_isolation_required}
    assert gated == {"07", "08", "09"}


def test_up_refuses_without_unsafe_local(monkeypatch, tmp_path):
    monkeypatch.setenv("REDSEC_STATE", str(tmp_path))
    started = []
    monkeypatch.setattr(cli, "start_range", lambda *a, **k: started.append(a))
    result = CliRunner().invoke(cli.app, ["up", "08"])
    assert result.exit_code == 2 and not started
    assert "--unsafe-local" in result.output and "range up 08" in result.output


def test_unsafe_local_flag_allows_the_start(monkeypatch, tmp_path):
    monkeypatch.setenv("REDSEC_STATE", str(tmp_path))

    class _Range:
        endpoints = {"registry": "http://127.0.0.1:9080"}
        drop_url = None
        pids: list[int] = []

    monkeypatch.setattr(cli, "start_range", lambda *a, **k: _Range())
    result = CliRunner().invoke(cli.app, ["up", "08", "--unsafe-local"])
    assert result.exit_code == 0, result.output
