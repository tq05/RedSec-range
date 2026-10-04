"""Discover, parse and validate modules."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from .config import modules_dir
from .models import Module


class ModuleError(Exception):
    pass


def _module_dirs() -> list[Path]:
    root = modules_dir()
    if not root.is_dir():
        return []
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "module.yaml").is_file())


def load_module(path: Path) -> Module:
    data: dict[str, Any] = yaml.safe_load((path / "module.yaml").read_text()) or {}
    try:
        mod = Module(**data)
    except ValidationError as e:  # pragma: no cover - surfaced to user
        raise ModuleError(f"{path.name}/module.yaml invalid:\n{e}") from e
    return mod


def load_all() -> list[tuple[Path, Module]]:
    out: list[tuple[Path, Module]] = []
    for d in _module_dirs():
        out.append((d, load_module(d)))
    return out


def find(module_id: str) -> tuple[Path, Module]:
    """Resolve a module by id ('03'), slug, or 'id-slug' dirname."""
    mid = module_id.strip().lower()
    for d, m in load_all():
        if mid in {m.id, m.slug, m.dirname, m.id.lstrip("0")}:
            return d, m
    raise ModuleError(f"no module matching {module_id!r} (try `redsec list`)")


def load_check(module_dir: Path, ref: str) -> Any:
    """Load a verifier callable from a 'module:Attr' reference.

    The left side is a dotted path resolved first inside the module's ``verify``
    package, then inside ``redsec.verify.builtins``. This keeps module authoring
    self-contained: drop ``verify/checks.py`` into your module and reference
    ``checks:MyCheck``.
    """
    if ":" not in ref:
        raise ModuleError(f"bad check ref {ref!r}; expected 'module:Attr'")
    modpath, attr = ref.split(":", 1)

    # Try builtins first if explicitly namespaced.
    if modpath.startswith("builtins"):
        from .verify import builtins as b

        return getattr(b, attr)

    # Load from the module's verify/ directory.
    file_candidates = [
        module_dir / "verify" / f"{modpath}.py",
        module_dir / f"{modpath}.py",
    ]
    for fc in file_candidates:
        if fc.is_file():
            spec = importlib.util.spec_from_file_location(
                f"redsec_mod_{module_dir.name}_{modpath}", fc
            )
            assert spec and spec.loader
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)
            return getattr(mod, attr)

    # Fall back to builtins by bare name.
    from .verify import builtins as b

    if hasattr(b, attr):
        return getattr(b, attr)
    raise ModuleError(f"could not resolve check {ref!r} for module {module_dir.name}")
