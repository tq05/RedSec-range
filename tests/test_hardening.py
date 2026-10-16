"""Framework hardening: sink limits, chart containment, and container flags."""
from __future__ import annotations

import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

from redsec import ranges
from redsec.range_catalog import load_catalog
from redsec.services.drop import app as drop


def _load_validator():
    path = Path(__file__).resolve().parents[1] / "scripts" / "validate_manifests.py"
    spec = importlib.util.spec_from_file_location("validate_manifests", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_drop_caps_stored_body_size():
    client = TestClient(drop.app)
    client.post("/reset")
    client.post("/collect", content=b"S3CRET")
    client.post("/collect", content=b"x" * (drop._MAX_BODY + 10))
    events = client.get("/events").json()["events"]
    assert events[0]["body"] == "S3CRET" and events[0]["truncated"] is False
    assert len(events[1]["body"]) == drop._MAX_BODY and events[1]["truncated"] is True


def test_rendered_pods_have_no_token_and_dns_is_scoped():
    v = _load_validator()
    objs = v.render({
        "range": {"module": "00", "slug": "demo", "namespace": "redsec-demo"},
        "image": {"registry": "r", "tag": "t"},
        "drop": {"enabled": True, "name": "drop", "port": 9099, "image": "r/drop:t"},
        "targets": [{"name": "rce", "port": 9070, "image": "r/rce:t",
                     "privileged": True, "egress": False}],
    })
    assert v.structural_checks(objs) == []
    policy = next(o for o in objs if o["metadata"]["name"] == "allow-intra-and-dns")
    policy["spec"]["egress"][1]["to"] = []
    assert any("open to all peers" in e for e in v.structural_checks(objs))


def test_external_containers_run_hardened(monkeypatch):
    calls: list[list[str]] = []
    monkeypatch.setattr(ranges, "build_external", lambda *a, **k: ("img", "rev"))
    monkeypatch.setattr(ranges, "_proxy_image", lambda: "gateway")
    monkeypatch.setattr(ranges, "_wait_port", lambda *a, **k: True)
    monkeypatch.setattr(ranges, "save_state", lambda data: None)
    monkeypatch.setattr(ranges, "_run", lambda args, **k: calls.append(args) or "")
    ranges.up_one(load_catalog().ranges["dvmcp"])
    runs = [c for c in calls if c[:2] == ["docker", "run"]]
    target = next(c for c in runs if "img" in c)
    gateway = next(c for c in runs if "gateway" in c)
    assert "no-new-privileges" in target and "--pids-limit" in target
    assert {"--cap-drop", "ALL", "no-new-privileges", "--read-only"} <= set(gateway)
