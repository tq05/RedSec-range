"""Assessor harnesses reach only lab targets and never the exfiltration sink."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_agent_solver_cannot_reach_the_sink():
    solver = _load_script("agent_solver")
    entry = {"endpoints": {"assistant": "http://127.0.0.1:9030",
                           "drop": "http://127.0.0.1:9099"},
             "drop_url": "http://127.0.0.1:9099"}
    allow = solver.allowed_hosts(entry)
    assert allow == {"127.0.0.1:9030"}
    out = solver.run_tool("http_request", {"method": "POST",
                                           "url": "http://127.0.0.1:9099/collect"},
                          allow, {})
    assert out.startswith("BLOCKED")


def test_grok_http_request_is_loopback_only_by_default():
    grok = _load_script("grok_cli")
    assert grok._host_allowed("http://127.0.0.1:9030/chat")
    assert grok._host_allowed("http://localhost:9000/")
    assert grok._host_allowed("http://[::1]:9000/")
    assert not grok._host_allowed("http://169.254.169.254/latest/meta-data/")
    assert not grok._host_allowed("https://example.com/")
    assert grok._host_allowed("https://example.com/", allow_hosts=["example.com"])
    blocked = grok.run_tool("http_request", {"url": "https://example.com/"}, ".")
    assert blocked.startswith("BLOCKED")
