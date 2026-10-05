"""Contract checks for the generated instructor guide and workshop deck."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

from redsec.loader import load_all
from redsec.range_catalog import load_catalog


ROOT = Path(__file__).resolve().parents[1]
TRAINING = ROOT / "docs" / "training"


def test_learning_guide_catalogs_every_challenge_and_solution_source():
    guide = (TRAINING / "LEARNING-GUIDE.md").read_text()

    builtin = [
        f"{module.id}/{challenge.id}"
        for _, module in load_all()
        for challenge in module.challenges
    ]
    assert len(builtin) == 43
    for challenge_id in builtin:
        assert f"| `{challenge_id}` |" in guide

    catalog = load_catalog()
    expected = {"dvaa": 22, "mcpgoat": 26, "dvmcp": 10, "appsecco-mcp": 9}
    for range_id, count in expected.items():
        curriculum = catalog.ranges[range_id].curriculum
        assert len(curriculum.challenges) == count
        assert f"## `{range_id}`" in guide
        for challenge in curriculum.challenges:
            assert f"| `{challenge.id}` |" in guide

    assert "# Built-in impossible tier — spoiler appendix" in guide
    assert "# Part II — DVAA: 22 embedded upstream solutions" in guide
    assert "# Part III — MCPGoat: 26 concepts across 78 scored variants" in guide
    assert "# Part IV — Damn Vulnerable MCP Server: 10 guided challenges" in guide
    assert "# Part V — Appsecco: nine demonstration labs" in guide


def test_published_learning_artifacts_are_complete_and_openable():
    pdf = TRAINING / "RedSec-Range-Learning-Guide.pdf"
    pdf_bytes = pdf.read_bytes()
    assert pdf_bytes.startswith(b"%PDF-")
    assert pdf_bytes.rstrip().endswith(b"%%EOF")
    assert len(pdf_bytes) > 300_000

    deck_source = (TRAINING / "LEARNING-DECK.md").read_text().strip()
    source_slides = re.split(r"\n\s*---\s*\n", deck_source)
    assert len(source_slides) == 34
    assert all(re.search(r"^#\s+.+$", slide, re.MULTILINE) for slide in source_slides)
    assert all(re.search(r"^>\s+.+$", slide, re.MULTILINE) for slide in source_slides)
    assert all(len(re.findall(r"^-\s+.+$", slide, re.MULTILINE)) <= 4 for slide in source_slides)

    pptx = TRAINING / "RedSec-Range-Learning-Deck.pptx"
    with zipfile.ZipFile(pptx) as archive:
        assert archive.testzip() is None
        slide_parts = [
            name for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        ]
        assert len(slide_parts) == 34
