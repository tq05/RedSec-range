"""Local progress tracking (solved challenges, score)."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .config import state_dir


def _file() -> Path:
    return state_dir() / "progress.json"


def load() -> dict[str, Any]:
    f = _file()
    if f.is_file():
        try:
            return json.loads(f.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def _save(data: dict[str, Any]) -> None:
    _file().write_text(json.dumps(data, indent=2, sort_keys=True))


def mark_solved(module_id: str, challenge_id: str, points: int) -> None:
    data = load()
    mod = data.setdefault(module_id, {})
    if challenge_id not in mod:
        mod[challenge_id] = {"solved": True, "ts": time.time(), "points": points}
        _save(data)


def is_solved(module_id: str, challenge_id: str) -> bool:
    return bool(load().get(module_id, {}).get(challenge_id, {}).get("solved"))


def reset_module(module_id: str) -> None:
    data = load()
    data.pop(module_id, None)
    _save(data)


def total_points() -> int:
    return sum(
        c.get("points", 0)
        for mod in load().values()
        for c in mod.values()
    )
