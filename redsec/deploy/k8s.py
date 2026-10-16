"""Render and deploy a module to Kubernetes via the bundled Helm chart.

The chart (``deploy/helm/redsec-module``) takes a values file that this module
derives mechanically from ``module.yaml`` -- so module authors never hand-write
Kubernetes manifests. ``redsec render`` emits YAML for review/GitOps; ``redsec
deploy`` installs it; both refuse gracefully if helm/kubectl are absent.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml

from ..config import DROP_NAME, DROP_PORT, NS_PREFIX, new_drop_token, repo_root
from ..models import Module


def chart_dir() -> Path:
    return repo_root() / "deploy" / "helm" / "redsec-module"


def namespace_for(module: Module, instance: str | None = None) -> str:
    base = f"{NS_PREFIX}-{module.id}"
    return f"{base}-{instance}" if instance else base


def module_to_values(module: Module, registry: str, tag: str,
                     instance: str | None = None) -> dict[str, Any]:
    targets = []
    drop_enabled = False
    for t in module.targets:
        if t.uses_builtin == "drop":
            drop_enabled = True
            continue
        image = t.image or f"{registry}/m{module.id}-{t.name}:{tag}"
        targets.append({
            "name": t.name,
            "port": t.port,
            "image": image,
            "privileged": t.privileged,
            "egress": t.network.egress,
            "allowTargets": t.network.allow_targets,
            "env": t.env,
        })
    return {
        "range": {
            "module": module.id,
            "slug": module.slug,
            "namespace": namespace_for(module, instance),
        },
        "image": {"registry": registry, "tag": tag},
        "drop": {"enabled": drop_enabled, "name": DROP_NAME, "port": DROP_PORT,
                 "image": f"{registry}/drop:{tag}", "token": new_drop_token()},
        "targets": targets,
    }


def _require(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        raise RuntimeError(
            f"{tool!r} not found on PATH. Install it to use Kubernetes deployment "
            f"(local development via `redsec dev` needs neither helm nor kubectl)."
        )
    return path


def render(module: Module, registry: str, tag: str,
           instance: str | None = None) -> str:
    helm = _require("helm")
    values = module_to_values(module, registry, tag, instance)
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        yaml.safe_dump(values, f)
        values_path = f.name
    release = f"{NS_PREFIX}-{module.id}" + (f"-{instance}" if instance else "")
    try:
        out = subprocess.run(
            [helm, "template", release, str(chart_dir()),
             "-f", values_path, "--namespace", values["range"]["namespace"]],
            capture_output=True, text=True,
        )
    finally:
        Path(values_path).unlink(missing_ok=True)
    if out.returncode != 0:
        raise RuntimeError(f"helm template failed:\n{out.stderr}")
    return out.stdout


def deploy(module: Module, registry: str, tag: str,
           instance: str | None = None) -> str:
    helm = _require("helm")
    _require("kubectl")
    values = module_to_values(module, registry, tag, instance)
    ns = values["range"]["namespace"]
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        yaml.safe_dump(values, f)
        values_path = f.name
    release = f"{NS_PREFIX}-{module.id}" + (f"-{instance}" if instance else "")
    try:
        out = subprocess.run(
            [helm, "upgrade", "--install", release, str(chart_dir()),
             "-f", values_path, "--namespace", ns, "--create-namespace", "--wait"],
            capture_output=True, text=True,
        )
    finally:
        Path(values_path).unlink(missing_ok=True)
    if out.returncode != 0:
        raise RuntimeError(f"helm install failed:\n{out.stderr}")
    return f"deployed release {release} to namespace {ns}\n{out.stdout}"


def destroy(module: Module, instance: str | None = None) -> str:
    helm = _require("helm")
    release = f"{NS_PREFIX}-{module.id}" + (f"-{instance}" if instance else "")
    ns = namespace_for(module, instance)
    subprocess.run([helm, "uninstall", release, "--namespace", ns],
                   capture_output=True, text=True)
    return f"uninstalled {release} (namespace {ns} left in place)"
