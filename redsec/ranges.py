"""Lifecycle controller for the built-in course and external range adapters."""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

from .config import (
    CONTAINER_HARDENING, EXTERNAL_CONTAINER_HARDENING, PublicBindError, publish_spec,
    repo_root, state_dir,
)
from .range_catalog import RangeCatalog, RangeDefinition, load_catalog


class RangeLifecycleError(RuntimeError):
    pass


def _require_docker() -> None:
    if shutil.which("docker") is None:
        raise RangeLifecycleError(
            "Docker is required to run external ranges; use a Codespace, Fly Machine, "
            "or local Docker host"
        )


def _run(
    args: list[str], *, cwd: Path | None = None, check: bool = True,
    stream: bool = False,
) -> str:
    result = subprocess.run(
        args, cwd=cwd, capture_output=not stream, text=True
    )
    if check and result.returncode:
        detail = "" if stream else (result.stderr.strip() or result.stdout.strip())
        raise RangeLifecycleError(f"{' '.join(args)}\n{detail}")
    return "" if stream else result.stdout.strip()


def _state_path() -> Path:
    return state_dir() / "ranges.json"


def load_state() -> dict:
    path = _state_path()
    if path.is_file():
        data = json.loads(path.read_text())
    else:
        data = {}
    data.setdefault("enabled", ["builtin"])
    data.setdefault("running", {})
    data.setdefault("revisions", {})
    return data


def save_state(data: dict) -> None:
    _state_path().write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def resolve_many(values: Iterable[str], catalog: RangeCatalog | None = None) -> list[RangeDefinition]:
    catalog = catalog or load_catalog()
    resolved: list[RangeDefinition] = []
    seen: set[str] = set()
    for value in values:
        try:
            definition = catalog.resolve(value)
        except KeyError as exc:
            raise RangeLifecycleError(f"unknown range {value!r}; run `redsec ranges list`") from exc
        if definition.id not in seen:
            resolved.append(definition)
            seen.add(definition.id)
    return resolved


def available(catalog: RangeCatalog | None = None) -> list[RangeDefinition]:
    catalog = catalog or load_catalog()
    return [item for item in catalog.ranges.values() if item.availability == "available"]


def set_enabled(values: Iterable[str], *, enable: bool) -> list[str]:
    catalog = load_catalog()
    definitions = resolve_many(values, catalog)
    unavailable = [item.id for item in definitions if item.availability != "available"]
    if unavailable:
        raise RangeLifecycleError(
            f"range(s) {', '.join(unavailable)} are placeholders and cannot be enabled"
        )
    state = load_state()
    selected = set(state["enabled"])
    for definition in definitions:
        (selected.add if enable else selected.discard)(definition.id)
    state["enabled"] = [key for key in catalog.ranges if key in selected]
    save_state(state)
    return state["enabled"]


def selected_ranges(values: Iterable[str] | None = None, *, select_all: bool = False) -> list[RangeDefinition]:
    catalog = load_catalog()
    if select_all:
        return available(catalog)
    explicit = list(values or [])
    if explicit:
        return resolve_many(explicit, catalog)
    state = load_state()
    return resolve_many(state["enabled"], catalog)


def _source_dir(definition: RangeDefinition) -> Path:
    return state_dir() / "external-ranges" / definition.id / "source"


def _ensure_source(definition: RangeDefinition) -> tuple[Path, str]:
    assert definition.source
    source = _source_dir(definition)
    git_dir = source / ".git"
    if not git_dir.is_dir():
        source.mkdir(parents=True, exist_ok=True)
        _run(["git", "init", "-q"], cwd=source)
        _run(["git", "remote", "add", "origin", definition.source.repository], cwd=source)
        _run(["git", "fetch", "--depth", "1", "origin", definition.source.revision], cwd=source)
        _run(["git", "checkout", "--detach", "FETCH_HEAD"], cwd=source)
    revision = _run(["git", "rev-parse", "HEAD"], cwd=source)
    dockerignore = source / ".dockerignore"
    if not dockerignore.exists():
        dockerignore.write_text(".git\nnode_modules\n**/__pycache__\n")
    return source, revision


def _image_name(definition: RangeDefinition, revision: str) -> str:
    return f"redsec/external-{definition.id}:{revision[:12]}"


def _dockerfile(definition: RangeDefinition, source: Path) -> Path:
    assert definition.runtime.dockerfile
    if definition.runtime.driver == "adapter":
        return repo_root() / definition.runtime.dockerfile
    return source / definition.runtime.dockerfile


def build_external(definition: RangeDefinition, *, rebuild: bool = False) -> tuple[str, str]:
    _require_docker()
    source, revision = _ensure_source(definition)
    image = _image_name(definition, revision)
    present = subprocess.run(
        ["docker", "image", "inspect", image], capture_output=True, text=True
    ).returncode == 0
    if rebuild or not present:
        _run([
            "docker", "build", "--pull", "-f", str(_dockerfile(definition, source)),
            "-t", image, str(source),
        ], stream=True)
    state = load_state()
    state["revisions"][definition.id] = revision
    save_state(state)
    return image, revision


def _publish(host: int, container: int) -> str:
    try:
        return publish_spec(host, container)
    except PublicBindError as exc:
        raise RangeLifecycleError(str(exc)) from exc


def _container_name(definition: RangeDefinition) -> str:
    return f"redsec-ext-{definition.id}"


def _network_name(definition: RangeDefinition) -> str:
    return f"redsec-ext-{definition.id}"


def _proxy_name(definition: RangeDefinition) -> str:
    return f"redsec-ext-{definition.id}-gateway"


def _access_network_name(definition: RangeDefinition) -> str:
    return f"redsec-ext-{definition.id}-access"


def _proxy_image() -> str:
    image = "redsec/range-tcp-gateway:local"
    present = subprocess.run(
        ["docker", "image", "inspect", image], capture_output=True, text=True
    ).returncode == 0
    if not present:
        _run([
            "docker", "build", "--pull",
            "-f", str(repo_root() / "ranges" / "adapters" / "tcp-proxy.Dockerfile"),
            "-t", image, str(repo_root()),
        ], stream=True)
    return image


def _wait_port(port: int, timeout: float = 60) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def _builtin_up() -> None:
    command = ["bash", str(repo_root() / "scripts" / "sandbox-up.sh")]
    modules = os.environ.get("REDSEC_MODULES", "").split()
    _run([*command, *modules], stream=True)


def _builtin_down() -> None:
    _run([sys.executable, str(repo_root() / "scripts" / "range_ctl.py"), "down-all"])


def up_one(
    definition: RangeDefinition, *, allow_egress: bool = False, rebuild: bool = False
) -> dict:
    if definition.availability != "available":
        raise RangeLifecycleError(f"{definition.id} is a placeholder and has no deployment adapter")
    if definition.runtime.driver == "builtin":
        _builtin_up()
        return {"id": definition.id, "driver": "builtin", "status": "running"}

    image, revision = build_external(definition, rebuild=rebuild)
    container = _container_name(definition)
    network = _network_name(definition)
    proxy = _proxy_name(definition)
    access_network = _access_network_name(definition)
    _run(["docker", "rm", "-f", container], check=False)
    _run(["docker", "rm", "-f", proxy], check=False)
    _run(["docker", "network", "rm", network], check=False)
    _run(["docker", "network", "rm", access_network], check=False)
    network_args = ["docker", "network", "create"]
    if not allow_egress:
        network_args.append("--internal")
    _run([*network_args, network])

    args = [
        "docker", "run", "-d", "--restart", "unless-stopped", "--name", container,
        "--network", network, *EXTERNAL_CONTAINER_HARDENING,
    ]
    if allow_egress:
        for port in definition.runtime.ports:
            args += ["-p", _publish(port.host, port.container)]
    for name, value in definition.runtime.environment.items():
        args += ["-e", f"{name}={value}"]
    args.append(image)
    args.extend(definition.runtime.command)

    try:
        _run(args)
        if not allow_egress:
            gateway_image = _proxy_image()
            _run(["docker", "network", "create", access_network])
            gateway_args = [
                "docker", "run", "-d", "--restart", "unless-stopped",
                "--read-only", *CONTAINER_HARDENING,
                "--name", proxy, "--network", access_network,
                "-e", f"TARGET_HOST={container}",
                "-e", "TARGET_PORTS=" + ",".join(
                    str(port.container) for port in definition.runtime.ports
                ),
            ]
            for port in definition.runtime.ports:
                gateway_args += ["-p", _publish(port.host, port.container)]
            gateway_args.append(gateway_image)
            _run(gateway_args)
            _run(["docker", "network", "connect", network, proxy])
        health_name = definition.runtime.health_port
        health = next(
            (port for port in definition.runtime.ports if port.name == health_name), None
        )
        if health and not _wait_port(health.host):
            logs = _run(["docker", "logs", "--tail", "80", container], check=False)
            raise RangeLifecycleError(
                f"{definition.id} did not open port {health.host}\n{logs}"
            )
    except Exception:
        _run(["docker", "rm", "-f", container], check=False)
        _run(["docker", "rm", "-f", proxy], check=False)
        _run(["docker", "network", "rm", network], check=False)
        _run(["docker", "network", "rm", access_network], check=False)
        raise

    entry = {
        "id": definition.id,
        "driver": definition.runtime.driver,
        "container": container,
        "network": network,
        "gateway": proxy if not allow_egress else None,
        "access_network": access_network if not allow_egress else None,
        "revision": revision,
        "egress": allow_egress,
        "endpoints": {
            port.name: f"http://127.0.0.1:{port.host}{port.path}"
            for port in definition.runtime.ports
        },
    }
    state = load_state()
    state["running"][definition.id] = entry
    save_state(state)
    return {**entry, "status": "running"}


def up_many(
    definitions: Iterable[RangeDefinition], *, allow_egress: bool = False,
    rebuild: bool = False,
) -> list[dict]:
    return [
        up_one(item, allow_egress=allow_egress, rebuild=rebuild)
        for item in definitions
    ]


def down_one(definition: RangeDefinition) -> None:
    if definition.runtime.driver == "builtin":
        _builtin_down()
    elif definition.runtime.driver in {"dockerfile", "adapter"}:
        _run(["docker", "rm", "-f", _container_name(definition)], check=False)
        _run(["docker", "rm", "-f", _proxy_name(definition)], check=False)
        _run(["docker", "network", "rm", _network_name(definition)], check=False)
        _run(["docker", "network", "rm", _access_network_name(definition)], check=False)
    state = load_state()
    state["running"].pop(definition.id, None)
    save_state(state)


def down_many(definitions: Iterable[RangeDefinition]) -> None:
    for definition in definitions:
        down_one(definition)


def _container_status(name: str) -> str:
    try:
        return _run(
            ["docker", "inspect", "-f", "{{.State.Status}}", name], check=False
        ) or "down"
    except FileNotFoundError:
        return "down"


def status_rows(catalog: RangeCatalog | None = None) -> list[dict]:
    catalog = catalog or load_catalog()
    state = load_state()
    rows: list[dict] = []
    builtin_state = state_dir() / "range.json"
    for definition in catalog.ranges.values():
        enabled = definition.id in state["enabled"]
        entry = state["running"].get(definition.id, {})
        if definition.runtime.driver == "builtin":
            endpoints: dict[str, str] = {}
            status = "down"
            if builtin_state.is_file():
                try:
                    modules = json.loads(builtin_state.read_text())
                    statuses = []
                    for module_id, module in modules.items():
                        for name, url in module.get("endpoints", {}).items():
                            endpoints[f"{module_id}/{name}"] = url
                        for container in module.get("names", {}).values():
                            statuses.append(_container_status(container))
                    if statuses and all(value == "running" for value in statuses):
                        status = "running"
                    elif statuses:
                        status = "degraded"
                except (OSError, ValueError, TypeError):
                    status = "degraded"
        elif definition.runtime.driver in {"dockerfile", "adapter"}:
            status = _container_status(_container_name(definition))
            endpoints = entry.get("endpoints", {})
        else:
            status = "placeholder"
            endpoints = {}
        revision = entry.get("revision") or state["revisions"].get(definition.id)
        catalog_revision = definition.source.revision if definition.source else None
        rows.append({
            "id": definition.id,
            "title": definition.title,
            "maintainer": definition.maintainer,
            "availability": definition.availability,
            "enabled": enabled,
            "status": status,
            "revision": revision,
            "catalog_revision": catalog_revision,
            "curriculum_current": not revision or not catalog_revision or revision == catalog_revision,
            "endpoints": endpoints,
        })
    return rows


def update_one(definition: RangeDefinition) -> tuple[str, str, bool]:
    if not definition.source:
        raise RangeLifecycleError(f"{definition.id} is managed with RedSec and has no external source")
    source, old = _ensure_source(definition)
    _run(["git", "fetch", "--depth", "1", "origin", definition.source.branch], cwd=source)
    _run(["git", "checkout", "--detach", "FETCH_HEAD"], cwd=source)
    new = _run(["git", "rev-parse", "HEAD"], cwd=source)
    running = _container_status(_container_name(definition)) == "running"
    build_external(definition, rebuild=True)
    if running:
        state = load_state()
        allow_egress = bool(state["running"].get(definition.id, {}).get("egress"))
        up_one(definition, allow_egress=allow_egress, rebuild=False)
    return old, new, running


def container_exec(definition: RangeDefinition, command: list[str], *, interactive: bool = False) -> int:
    if definition.runtime.driver not in {"dockerfile", "adapter"}:
        raise RangeLifecycleError("exec is available for external container ranges")
    _require_docker()
    args = ["docker", "exec"]
    if interactive:
        args += ["-it"]
    else:
        args += ["-i"]
    args += [_container_name(definition), *command]
    return subprocess.run(args).returncode
