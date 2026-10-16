"""Regression tests for the framework review: env scoping, backend shape, models."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from redsec.deploy import local
from redsec.mockllm import Message
from redsec.mockllm import backends
from redsec.models import Target

ROOT = Path(__file__).resolve().parents[1]


def _load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_local_targets_do_not_inherit_shell_credentials(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_fake")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "fake")
    monkeypatch.setenv("REDSEC_LLM_BACKEND", "mock")
    monkeypatch.setenv("LC_ALL", "C.UTF-8")
    env = local._target_env()
    assert "GITHUB_TOKEN" not in env and "AWS_SECRET_ACCESS_KEY" not in env
    assert env["REDSEC_LLM_BACKEND"] == "mock" and env["LC_ALL"] == "C.UTF-8"
    assert "PATH" in env


def test_real_backend_sends_tool_output_as_labelled_content(monkeypatch):
    sent: dict = {}

    class _Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": "ok"}}]}

    def fake_post(url, json, headers, timeout):
        sent.update(json)
        return _Resp()

    import httpx

    monkeypatch.setattr(httpx, "post", fake_post)
    backends.OpenAICompatBackend().complete([
        Message("system", "be helpful"),
        Message("document", "untrusted page"),
        Message("tool", "file contents", name="read_file"),
    ])
    roles = [m["role"] for m in sent["messages"]]
    assert roles == ["system", "user", "user"]
    assert sent["messages"][2]["content"].startswith("[tool result: read_file]")
    assert "tool_call_id" not in json.dumps(sent)


def test_privileged_target_cannot_have_egress():
    Target(name="rce", privileged=True)
    with pytest.raises(ValidationError):
        Target(name="rce", privileged=True, network={"egress": True})
    with pytest.raises(ValidationError):
        Target(name="")


def test_agent_shell_env_strips_credentials(monkeypatch):
    grok = _load_script("grok_cli")
    monkeypatch.setenv("XAI_API_KEY", "xai-fake")
    monkeypatch.setenv("GH_TOKEN", "fake")
    monkeypatch.setenv("REDSEC_MODULES", "01")
    env = grok._shell_env()
    assert "XAI_API_KEY" not in env and "GH_TOKEN" not in env
    assert env["REDSEC_MODULES"] == "01"


def test_agent_confirm_mode_declines_without_yes(monkeypatch):
    grok = _load_script("grok_cli")
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    out = grok.run_tool("exec_shell", {"command": "echo hi"}, ".", confirm=True)
    assert out == "operator declined to run this command"
