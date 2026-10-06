"""Defensive-only contracts for the catalog-wide Codex threat-model workflow."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "redsec_codex_threat_models",
    ROOT / "scripts" / "codex_threat_models.py",
)
assert SPEC and SPEC.loader
THREAT_MODELS = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = THREAT_MODELS
SPEC.loader.exec_module(THREAT_MODELS)

AbusePath = THREAT_MODELS.AbusePath
Evidence = THREAT_MODELS.Evidence
ThreatBatch = THREAT_MODELS.ThreatBatch
ThreatModel = THREAT_MODELS.ThreatModel
batches = THREAT_MODELS.batches
build_inventory = THREAT_MODELS.build_inventory
generate = THREAT_MODELS.generate
render = THREAT_MODELS.render
validate_batch = THREAT_MODELS.validate_batch
AVAILABLE_RANGES = THREAT_MODELS.AVAILABLE_RANGES
BLOCKED_OUTPUT = THREAT_MODELS.BLOCKED_OUTPUT


def synthetic_model(record: dict) -> ThreatModel:
    return ThreatModel(
        key=record["key"],
        title=record["title"],
        system_context="A bounded training service processes untrusted requests.",
        primary_risk="Untrusted input may cross an authority boundary without an enforced policy.",
        risk_rating="high",
        control_families=["identity-access", "logging-detection"],
        assets=["Authorised service state", "Audit evidence"],
        trust_boundaries=["Untrusted caller to service", "Service to protected resource"],
        threat_actors=["An unauthorised or compromised caller"],
        abuse_preconditions=["The service accepts a request before enforcing the intended policy"],
        abuse_paths=[
            AbusePath(
                scenario="A caller supplies untrusted data that reaches a protected operation.",
                impact="The operation may disclose data or perform an unauthorised effect.",
            )
        ],
        secure_before_abuse=[
            "Authenticate the caller at the service boundary.",
            "Authorise the requested object and effect server-side.",
            "Constrain the service identity to least privilege.",
        ],
        detection_and_response=[
            "Record denied decisions with stable actor and object identifiers.",
            "Alert on repeated policy failures and investigate the affected identity.",
        ],
        safe_validation=[
            "Use synthetic identities to confirm cross-user requests fail closed.",
            "Use inert malformed inputs to confirm parsing errors do not broaden access.",
        ],
        security_outcome="Unauthorised requests are rejected before protected state is accessed.",
        residual_risk=["Compromised authorised identities still require behavioral monitoring."],
        evidence=[
            Evidence(
                path=record["evidence_paths"][0],
                reason="Defines the catalog identity or deployment boundary for this concept.",
            )
        ],
        confidence="medium",
        limitations=["No target or exploit was executed during this design review."],
    )


def write_synthetic_results(results_dir: Path, inventory: list[dict], batch_size: int = 8) -> None:
    for batch in batches(inventory, batch_size):
        data = ThreatBatch(
            range_id=batch["range_id"],
            batch_id=batch["batch_id"],
            threat_models=[synthetic_model(record) for record in batch["challenges"]],
        )
        wrapper = {
            "schema_version": 1,
            "batch_id": batch["batch_id"],
            "source_revision": "a" * 40,
            "model": "gpt-6-sol",
            "reasoning_effort": "high",
            "response_id": "synthetic",
            "generated_at": "2026-10-06T00:00:00+00:00",
            "data": data.model_dump(),
        }
        (results_dir / f"{batch['batch_id']}.json").write_text(json.dumps(wrapper))


def test_inventory_and_dry_run_exclude_secrets_solutions_and_execution(tmp_path):
    inventory = build_inventory()

    assert len(inventory) == 110
    assert sum(record["variants"] for record in inventory) == 162
    assert {record["range_id"] for record in inventory} == {
        "builtin", "dvaa", "mcpgoat", "dvmcp", "appsecco-mcp"
    }
    serialized = json.dumps(inventory)
    assert "REDSEC{" not in serialized
    assert '"hints"' not in serialized
    assert '"flag":' not in serialized
    assert "solution/solve.py" not in serialized

    requests = tmp_path / "requests"
    result = generate(
        argparse.Namespace(
            results_dir=tmp_path / "unused",
            model="gpt-6-sol",
            reasoning_effort="high",
            batch_size=8,
            source_revision="a" * 40,
            overwrite=False,
            dry_run=True,
            request_dir=requests,
        )
    )
    assert result == 0
    previews = sorted(requests.glob("*.request.json"))
    assert len(previews) == 17
    preview_text = "".join(path.read_text() for path in previews)
    assert "OPENAI_API_KEY" not in preview_text
    assert "REDSEC{" not in preview_text
    assert '"store": false' in preview_text
    assert '"type": "json_schema"' in preview_text


def test_validator_rejects_operational_payload_content():
    record = build_inventory()[0]
    model = synthetic_model(record)
    model.safe_validation[0] = "Run curl -s against the target."
    parsed = ThreatBatch(
        range_id=record["range_id"],
        batch_id="builtin-01",
        threat_models=[model],
    )
    expected = {
        "range_id": record["range_id"],
        "batch_id": "builtin-01",
        "challenges": [record],
    }

    with pytest.raises(ValueError, match="prohibited operational content"):
        validate_batch(parsed, expected, {record["key"]: set(record["evidence_paths"])})


def test_renderer_requires_full_catalog_and_builds_portfolio(tmp_path):
    inventory = build_inventory()
    results = tmp_path / "results"
    results.mkdir()
    write_synthetic_results(results, inventory)
    output = tmp_path / "threat-models"

    assert render(argparse.Namespace(results_dir=results, output_dir=output)) == 0

    overview = (output / "OVERVIEW.md").read_text()
    assert "110 challenge concepts" in overview
    assert "162 declared variants" in overview
    assert "[control-gap matrix](CONTROL-GAP-MATRIX.md)" in overview
    assert overview.count("| `builtin`") == 43 + 1
    assert "Secure before abuse" in (output / "generated" / "builtin.md").read_text()
    assert sum(
        path.read_text().count('<a id="')
        for path in (output / "generated").glob("*.md")
    ) == 110
    manifest = json.loads((output / "generated" / "MANIFEST.json").read_text())
    assert manifest["concepts"] == 110
    assert manifest["declared_variants"] == 162
    assert len(manifest["files"]) == 11

    one_batch = next(results.glob("*.json"))
    one_batch.unlink()
    with pytest.raises(ValueError, match="missing or unexpected batches"):
        render(argparse.Namespace(results_dir=results, output_dir=output))


def test_workflow_keeps_model_generation_read_only_and_publish_separate():
    path = ROOT / ".github" / "workflows" / "codex-threat-models.yml"
    text = path.read_text()
    workflow = yaml.load(text, Loader=yaml.BaseLoader)

    assert set(workflow["on"]) == {"workflow_dispatch"}
    generate_job = workflow["jobs"]["generate"]
    publish_job = workflow["jobs"]["publish"]
    assert generate_job["if"] == "${{ github.ref == 'refs/heads/main' }}"
    assert generate_job["permissions"] == {"contents": "read"}
    assert publish_job["permissions"] == {"contents": "write", "pull-requests": "write"}
    assert "persist-credentials: false" in text
    assert "OPENAI_API_KEY" in yaml.safe_dump(generate_job)
    assert "OPENAI_API_KEY" not in yaml.safe_dump(publish_job)
    assert "gh pr create" in text
    assert "@codex security review" in text
    for job in workflow["jobs"].values():
        for step in job.get("steps", []):
            if "run" in step:
                subprocess.run(
                    ["bash", "-n"],
                    input=step["run"],
                    text=True,
                    capture_output=True,
                    check=True,
                )


def test_committed_portfolio_matches_catalog_and_integrity_manifest():
    root = ROOT / "docs" / "threat-models"
    generated = root / "generated"
    manifest = json.loads((generated / "MANIFEST.json").read_text())
    inventory = build_inventory()
    expected = {record["key"]: record for record in inventory}
    seen: dict[str, ThreatModel] = {}

    for range_id in AVAILABLE_RANGES:
        document = json.loads((generated / "data" / f"{range_id}.json").read_text())
        assert document["range_id"] == range_id
        assert document["source_revision"] == manifest["source_revision"]
        assert document["model"] == manifest["model"]
        for raw in document["threat_models"]:
            model = ThreatModel.model_validate(raw)
            assert model.key not in seen
            assert model.key in expected
            assert model.title == expected[model.key]["title"]
            seen[model.key] = model

    assert list(seen) == [record["key"] for record in inventory]
    assert manifest["concepts"] == len(seen) == 110
    assert manifest["declared_variants"] == sum(record["variants"] for record in inventory) == 162

    for relative, expected_hash in manifest["files"].items():
        content = (root / relative).read_bytes()
        assert hashlib.sha256(content).hexdigest() == expected_hash

    published = (root / "OVERVIEW.md").read_text() + "".join(
        (generated / f"{range_id}.md").read_text() for range_id in AVAILABLE_RANGES
    )
    assert published.count('<a id="') == 110
    assert "not verified—outside the current scope" in published
    for pattern in BLOCKED_OUTPUT:
        assert not pattern.search(published), pattern.pattern

    matrix = (root / "CONTROL-GAP-MATRIX.md").read_text()
    assert "| Component | Threat | Who can exploit it | Controls in place | Controls missing |" in matrix
    assert matrix.count("\n| ") >= 20
    assert "not verified—outside the current scope" in matrix
