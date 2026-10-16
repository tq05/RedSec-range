"""`redsec verify` exits 0 only when every verified challenge passes."""
from __future__ import annotations

from typer.testing import CliRunner

from redsec import state
from redsec.cli import app
from redsec.loader import find


def test_verify_sweep_requires_every_challenge(monkeypatch, tmp_path):
    # Module 10 has no running targets, so its artifact checks run offline.
    monkeypatch.setenv("REDSEC_STATE", str(tmp_path))
    _, module = find("10")
    first, *rest = module.challenges
    runner = CliRunner()

    state.mark_solved(module.id, first.id, first.points)
    partial = runner.invoke(app, ["verify", "10"])
    assert partial.exit_code == 1
    assert f"1/{len(module.challenges)} solved" in partial.output

    for c in rest:
        state.mark_solved(module.id, c.id, c.points)
    assert runner.invoke(app, ["verify", "10"]).exit_code == 0
    assert runner.invoke(app, ["verify", "10", first.id]).exit_code == 0
