#!/usr/bin/env python3
"""Assemble the complete learner guide from RedSec and pinned upstream solutions.

This script is for maintainers. External source paths must point at checkouts of the
exact revisions recorded in ranges/catalog.yaml. The generated Markdown is committed
so learners do not need those checkouts to build the PDF.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
import re
import subprocess
from pathlib import Path

from redsec.range_catalog import load_catalog

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "docs" / "training" / "LEARNING-GUIDE.md"


def without_title(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def section(text: str, start_pattern: str, end_pattern: str) -> str:
    start = re.search(start_pattern, text, re.M | re.I)
    if not start:
        return ""
    end = re.search(end_pattern, text[start.end():], re.M | re.I)
    stop = start.end() + end.start() if end else len(text)
    return text[start.end():stop].strip()


def dvaa_challenges(source: Path) -> list[dict]:
    script = f"""
const {{ CHALLENGES }} = await import('file://{source.as_posix()}');
const keep = Object.values(CHALLENGES).map(
  ({{id,name,category,difficulty,objectives,hints,solution,defendHow}}) =>
  ({{id,name,category,difficulty,objectives,hints,solution,defendHow}}));
console.log(JSON.stringify(keep));
"""
    output = subprocess.check_output(
        ["node", "--input-type=module", "-e", script], text=True
    )
    return json.loads(output)


def verify_upstream_revisions(upstreams: Path) -> dict[str, str]:
    """Reject solution text from a checkout other than the catalog's pinned commit."""
    catalog = load_catalog()
    checkout_names = {
        "dvaa": "dvaa",
        "mcpgoat": "mcpgoat",
        "dvmcp": "dvmcp",
        "appsecco-mcp": "appsecco",
    }
    revisions: dict[str, str] = {}
    for range_id, checkout_name in checkout_names.items():
        expected = catalog.ranges[range_id].source.revision
        actual = subprocess.check_output(
            ["git", "-C", str(upstreams / checkout_name), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        if actual != expected:
            raise SystemExit(
                f"{range_id} checkout is {actual}; expected pinned revision {expected}"
            )
        dirty = subprocess.check_output(
            [
                "git", "-C", str(upstreams / checkout_name), "status",
                "--porcelain", "--untracked-files=no",
            ],
            text=True,
        ).strip()
        if dirty:
            raise SystemExit(f"{range_id} checkout has modified tracked files")
        revisions[range_id] = expected
    return revisions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--upstreams",
        type=Path,
        default=Path("/private/tmp/redsec-upstreams-20261005"),
        help="directory containing dvaa, mcpgoat, dvmcp, and appsecco checkouts",
    )
    args = parser.parse_args()
    upstreams = args.upstreams.resolve()

    required = ["dvaa", "mcpgoat", "dvmcp", "appsecco"]
    missing = [name for name in required if not (upstreams / name).is_dir()]
    if missing:
        parser.error(f"missing pinned upstream checkouts: {', '.join(missing)}")
    revisions = verify_upstream_revisions(upstreams)

    catalog = (ROOT / "docs" / "CHALLENGE-CATALOG.md").read_text()
    catalog = catalog.replace("(../ranges/catalog.yaml)", "(../../ranges/catalog.yaml)")
    catalog = catalog.replace("(SOLUTIONS.md)", "(../SOLUTIONS.md)")
    builtins = (ROOT / "docs" / "SOLUTIONS.md").read_text()
    builtins = builtins.replace("(WORKSHEET.md)", "(../WORKSHEET.md)")
    sealed_a2a = (ROOT / "modules/04-multi-agent-a2a/solution/SEALED.md").read_text()
    sealed_mcp = (ROOT / "modules/07-mcp-tool-surfaces/solution/SEALED.md").read_text()

    lines = [
        "---",
        'title: "RedSec Range — Complete Challenge Learning Guide"',
        'subtitle: "110 concepts · 162 runnable variants · built-in and external ranges"',
        'author: "RedSec Range"',
        f'date: "{date.today().isoformat()}"',
        "---",
        "",
        "# How to use this guide {.unnumbered}",
        "",
        "> **Scope.** This is a defensive training workbook for deliberately vulnerable,",
        "> isolated lab targets. Use only the RedSec Range or systems you are authorised",
        "> to test. Never expose a challenge service publicly.",
        "",
        "The guide separates three evidence levels:",
        "",
        "1. **RedSec verified** — 43 built-in challenges have runnable reference exploits",
        "   and fail-before/pass-after verification.",
        "2. **Upstream solved** — DVAA, MCPGoat, and DVMCP publish their own solutions;",
        "   RedSec pins and deploys those implementations.",
        "3. **Upstream demonstrated** — Appsecco publishes demonstration procedures, but",
        "   does not provide one unified scored solution suite.",
        "",
        "## The repeatable learning loop",
        "",
        "1. **Observe** the tools, resources, prompts, routes, identities, and trust edges.",
        "2. **Hypothesise** where data crosses from untrusted content into authority.",
        "3. **Exploit** one narrow assumption in the isolated lab.",
        "4. **Verify** the flag, oracle event, or scored artifact.",
        "5. **Explain** the root cause and write the smallest effective defense.",
        "6. **Reset and repeat** at the next difficulty level.",
        "",
        "## Start the range",
        "",
        "```bash",
        "# Codespaces is the default hosted path",
        "range status",
        "redsec lesson 01",
        "range solve 01",
        "",
        "# Enable all pinned external integrations",
        "redsec ranges enable dvaa mcpgoat dvmcp appsecco-mcp",
        "redsec ranges up",
        "redsec ranges status",
        "redsec ranges challenges",
        "```",
        "",
        "# Course map and answer provenance",
        "",
        without_title(catalog),
        "",
        "# Part I — RedSec built-in course: exact walkthroughs",
        "",
        "Every entry in this part is backed by `solution/solve.py`. Run the manual steps",
        "first, then compare with `range solve MODULE CHALLENGE`.",
        "",
        without_title(builtins),
        "",
        "# Built-in impossible tier — spoiler appendix",
        "",
        "> Read this section only after attempting the sealed challenges. These answers",
        "> are included because this edition is the complete instructor guide.",
        "",
        without_title(sealed_a2a),
        "",
        without_title(sealed_mcp),
        "",
        "# Part II — DVAA: 22 embedded upstream solutions",
        "",
        f"Source revision: `{revisions['dvaa']}`. Each entry below",
        "preserves the upstream objective, solution path, and primary defense.",
        "",
    ]

    for item in dvaa_challenges(upstreams / "dvaa/src/challenges/index.js"):
        lines.extend([
            f"## {item['id']} — {item['name']}",
            "",
            f"**Category:** `{item['category']}` · **Difficulty:** `{item['difficulty']}`",
            "",
            "**Goal**",
            "",
            *[f"- {value}" for value in item.get("objectives", [])],
            "",
            "**Step-by-step solution**",
            "",
            str(item.get("solution", "")).strip(),
            "",
            "**If you get stuck**",
            "",
            *[f"- {value}" for value in item.get("hints", [])],
            "",
            "**Defense lesson**",
            "",
            str(item.get("defendHow", "")).strip(),
            "",
        ])

    mcpgoat = (upstreams / "mcpgoat/docs/SOLUTIONS.md").read_text()
    lines.extend([
        "# Part III — MCPGoat: 26 concepts across 78 scored variants",
        "",
        f"Source revision: `{revisions['mcpgoat']}`. Work each",
        "concept at Easy, Moderate, and Difficult, reconnecting after every level change.",
        "The Secure level is the fixed reference implementation.",
        "",
        without_title(mcpgoat),
        "",
        "# Part IV — Damn Vulnerable MCP Server: 10 guided challenges",
        "",
        f"Source revision: `{revisions['dvmcp']}`. The following",
        "walkthroughs are the upstream solution guides, grouped by RedSec challenge ID.",
        "",
    ])

    for number in range(1, 11):
        path = upstreams / f"dvmcp/solutions/challenge{number}_solution.md"
        lines.extend([
            f"## DVMCP {number:02d}",
            "",
            without_title(path.read_text()),
            "",
        ])

    appsecco_dirs = {
        "filesystem-workspace-actions": "vulnerable-mcp-server-filesystem-workspace-actions",
        "indirect-prompt-injection": "vulnerable-mcp-server-indirect-prompt-injection",
        "indirect-prompt-injection-remote": "vulnerable-mcp-server-indirect-prompt-injection-remote-mcp",
        "malicious-code-exec": "vulnerable-mcp-server-malicious-code-exec",
        "malicious-tools": "vulnerable-mcp-server-malicious-tools",
        "namespace-typosquatting": "vulnerable-mcp-server-namespace-typosquatting",
        "outdated-packages": "vulnerable-mcp-server-outdated-pacakges",
        "secrets-pii": "vulnerable-mcp-server-secrets-pii",
        "wikipedia-streamable": "vulnerable-mcp-server-wikipedia-http-streamable",
    }
    lines.extend([
        "# Part V — Appsecco: nine demonstration labs",
        "",
        f"Source revision: `{revisions['appsecco-mcp']}`. These are",
        "demonstrations rather than a unified flag suite. Record the observed unsafe",
        "behavior, then repeat after applying the defense described in the lab.",
        "",
    ])
    for challenge_id, dirname in appsecco_dirs.items():
        readme = (upstreams / "appsecco" / dirname / "README.md").read_text()
        title = re.search(r"^#\s+(.+)$", readme, re.M).group(1)
        vulnerable = section(readme, r"^## How it is vulnerable\s*$", r"^## Requirements\s*$")
        examples = section(readme, r"^## Example usage[^\n]*$", r"^## Notes\s*$")
        lines.extend([
            f"## {challenge_id} — {title}",
            "",
            "**What to observe**",
            "",
            vulnerable,
            "",
            "**Demonstration procedure**",
            "",
            examples or "Follow the lab README and inspect the exposed tools and returned content.",
            "",
        ])

    lines.extend([
        "# Instructor close-out checklist",
        "",
        "- Can the learner state the trust boundary before showing the payload?",
        "- Can they distinguish model behavior from host/application authority?",
        "- Did they capture evidence through a verifier, flag, or observable side effect?",
        "- Can they propose a defense at the correct layer: input, protocol, authorization,",
        "  sandbox, egress, dependency, or monitoring?",
        "- Can they explain why the same exploit class reappears across agents, A2A, RAG,",
        "  MCP, model artifacts, and infrastructure?",
        "",
        "The durable challenge inventory is `docs/CHALLENGE-CATALOG.md`. Upstream",
        "solutions remain authoritative for external ranges and should be refreshed when",
        "their pinned revisions change.",
        "",
    ])

    DEST.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines)
    DEST.write_text("\n".join(line.rstrip() for line in content.splitlines()) + "\n")
    print(f"wrote {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
