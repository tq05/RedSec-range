#!/usr/bin/env python3
"""Generate the cross-range challenge catalog from authoritative manifests."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from redsec.loader import load_all  # noqa: E402
from redsec.range_catalog import load_catalog  # noqa: E402


def clean(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def challenge_rows(definition) -> list[dict[str, object]]:
    if definition.runtime.driver == "builtin":
        rows = []
        for _, module in load_all():
            for challenge in module.challenges:
                difficulty = challenge.tier
                if not difficulty and challenge.difficulty:
                    difficulty = challenge.difficulty.value
                rows.append({
                    "id": f"{module.id}/{challenge.id}",
                    "title": challenge.title,
                    "category": module.title,
                    "difficulty": difficulty or module.difficulty.value,
                    "variants": 1,
                })
        return rows
    return [challenge.model_dump() for challenge in definition.curriculum.challenges]


def solution_label(definition) -> str:
    curriculum = definition.curriculum
    label = {
        "redsec": "RedSec reference solution",
        "upstream": "Upstream solution/guidance",
        "unknown": "No known solution",
        "unavailable": "Unavailable",
    }[curriculum.solution_status]
    if curriculum.solution_url:
        return f"[{label}]({curriculum.solution_url})"
    if curriculum.solution_path:
        path = curriculum.solution_path
        if path.startswith("docs/"):
            path = path.removeprefix("docs/")
        else:
            path = f"../{path}"
        return f"[{label}]({path})"
    return label


def render() -> str:
    catalog = load_catalog()
    available = [
        definition for definition in catalog.ranges.values()
        if definition.availability == "available"
    ]
    total_concepts = sum(len(challenge_rows(item)) for item in available)
    total_variants = sum(
        sum(int(row.get("variants", 1)) for row in challenge_rows(item))
        for item in available
    )
    lines = [
        "# Challenge catalog by range",
        "",
        "This file is generated from the built-in module manifests and",
        "[`ranges/catalog.yaml`](../ranges/catalog.yaml). Regenerate it with",
        "`python3 scripts/generate_challenge_catalog.py`.",
        "",
        f"The catalog contains **{total_concepts} challenge concepts** and ",
        f"**{total_variants} runnable variants** across five available ranges. ",
        "MCPGoat accounts for the difference: each of its concepts has easy, moderate, ",
        "and difficult scored variants. Its separate Secure level is a fixed reference, ",
        "not another flag. Appsecco calls its entries labs rather than scored challenges.",
        "",
        "`builtin` is authored and fail-before/pass-after verified by RedSec. External ",
        "entries are implemented in pinned upstream source; RedSec supplies deployment, ",
        "isolation, discovery, and smoke checks. A health check does not turn an upstream ",
        "exercise into a RedSec-verified challenge.",
        "",
        "## Range summary",
        "",
        "| Range | Ownership | Concepts | Variants | Solution provenance |",
        "|---|---|---:|---:|---|",
    ]
    for definition in available:
        rows = challenge_rows(definition)
        variants = sum(int(row.get("variants", 1)) for row in rows)
        lines.append(
            f"| `{definition.id}` | {clean(definition.maintainer)} | {len(rows)} | "
            f"{variants} | {solution_label(definition)} |"
        )
    lines.extend([
        "| `offsec` | OffSec | 0 | 0 | Placeholder only; no public deployable lab |",
        "",
        "The 85 DVAA infrastructure scanner fixtures are an additional detection corpus, ",
        "not dashboard CTF challenges, so they are not included in the challenge total.",
        "",
    ])

    for definition in available:
        rows = challenge_rows(definition)
        lines.extend([
            f"## `{definition.id}` — {definition.title}",
            "",
            definition.curriculum.note or definition.summary,
            "",
            "| ID | Challenge | Category | Difficulty | Variants | Solution |",
            "|---|---|---|---|---:|---|",
        ])
        solution = solution_label(definition)
        for row in rows:
            lines.append(
                f"| `{clean(row['id'])}` | {clean(row['title'])} | "
                f"{clean(row['category'])} | {clean(row['difficulty'])} | "
                f"{int(row.get('variants', 1))} | {solution} |"
            )
        lines.append("")

    lines.extend([
        "## Solution and verification meanings",
        "",
        "- **RedSec reference solution** means the repository contains a runnable ",
        "  `solution/solve.py` and `redsec selftest` proves fail-before/pass-after.",
        "- **Upstream solution/guidance** means the answer is maintained at the pinned ",
        "  upstream revision. DVAA embeds solutions in challenge definitions; MCPGoat ",
        "  publishes a trainer guide and attacker client; DVMCP publishes ten detailed ",
        "  guides; Appsecco publishes demonstration payloads in each lab README.",
        "- RedSec CI validates external adapters and representative protocol surfaces. ",
        "  It does not currently claim fail-before/pass-after proof for every external lab.",
        "",
    ])
    return "\n".join(line.rstrip() for line in lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the file is stale")
    args = parser.parse_args()
    destination = ROOT / "docs" / "CHALLENGE-CATALOG.md"
    generated = render()
    if args.check:
        if not destination.is_file() or destination.read_text() != generated:
            print(f"stale generated file: {destination}", file=sys.stderr)
            return 1
        return 0
    destination.write_text(generated)
    print(f"wrote {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
