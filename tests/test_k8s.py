"""Offline validation of the Kubernetes manifests the chart produces."""
from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_validator():
    path = Path(__file__).resolve().parents[1] / "scripts" / "validate_manifests.py"
    spec = importlib.util.spec_from_file_location("validate_manifests", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_manifests_valid_against_k8s_schema():
    v = _load_validator()
    assert v.main() == 0, "rendered manifests failed offline schema/structural validation"
