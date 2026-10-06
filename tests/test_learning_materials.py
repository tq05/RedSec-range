"""Static contracts for the defensive guide and paired workshop deck."""
from __future__ import annotations

import hashlib
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from pypdf import PdfReader

from redsec.loader import load_all
from redsec.range_catalog import load_catalog


ROOT = Path(__file__).resolve().parents[1]
TRAINING = ROOT / "docs" / "training"
OUTSIDE_SCOPE = "not verified—outside the current scope"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def expected_keys() -> list[str]:
    keys = [
        f"builtin/{module.id}/{challenge.id}"
        for _, module in load_all()
        for challenge in module.challenges
    ]
    catalog = load_catalog()
    for range_id in ("dvaa", "mcpgoat", "dvmcp", "appsecco-mcp"):
        keys.extend(
            f"{range_id}/{challenge.id}"
            for challenge in catalog.ranges[range_id].curriculum.challenges
        )
    return keys


def source_slides() -> list[str]:
    source = (TRAINING / "LEARNING-DECK.md").read_text().strip()
    return re.split(r"\n\s*---\s*\n", source)


def comment(block: str, name: str) -> str:
    match = re.search(rf"<!-- {re.escape(name)}: (.+) -->", block)
    assert match
    return match.group(1)


def expected_slide_text(block: str) -> list[str]:
    title = re.search(r"^#\s+(.+)$", block, re.MULTILINE)
    takeaway = re.search(r"^>\s+(.+)$", block, re.MULTILINE)
    assert title and takeaway
    values = [title.group(1), takeaway.group(1)]
    for bullet in re.findall(r"^-\s+(.+)$", block, re.MULTILINE):
        labelled = re.fullmatch(r"\*\*([^*]+?):\*\*\s*(.+)", bullet)
        assert labelled
        values.extend(labelled.groups())
    return values


def test_learning_sources_cover_every_catalog_concept_without_runbook_content():
    guide = (TRAINING / "LEARNING-GUIDE.md").read_text()
    deck = (TRAINING / "LEARNING-DECK.md").read_text()
    keys = expected_keys()

    assert len(keys) == 110
    for key in keys:
        _range_id, challenge_id = key.split("/", 1)
        assert f"## `{challenge_id}`" in guide
        assert deck.count(f"<!-- key: {key} -->") == 2

    assert guide.count(OUTSIDE_SCOPE) >= 110
    assert deck.count(OUTSIDE_SCOPE) == 110

    expected_patterns = {
        "builtin/04/session-smuggling": "session-context",
        "builtin/05/knowledge-poisoning": "rag",
        "builtin/06/embedding-inversion": "embeddings",
        "builtin/07/resource-traversal": "sink",
        "builtin/07/command-injection": "sink",
        "builtin/09/metadata-ssrf": "infra",
        "dvaa/L2-03": "sink",
        "dvaa/L3-02": "infra",
        "mcpgoat/D1": "sink",
        "mcpgoat/D2": "sink",
        "mcpgoat/D3": "infra",
    }
    patterns = {
        comment(block, "key"): comment(block, "pattern")
        for block in source_slides()[::2]
    }
    for key, pattern_id in expected_patterns.items():
        assert patterns[key] == pattern_id

    prohibited = (
        "REDSEC{",
        "Step-by-step solution",
        "SEALED.md",
        "curl -s",
        '"method":"tools/call"',
        "reverse shell",
        "../../../../etc/passwd",
    )
    combined = guide + deck
    for value in prohibited:
        assert value not in combined


def test_deck_is_exactly_two_ordered_slides_per_challenge():
    slides = source_slides()

    assert len(slides) == 220
    for pair_index in range(0, len(slides), 2):
        challenge, resolution = slides[pair_index:pair_index + 2]
        challenge_key = comment(challenge, "key")
        resolution_key = comment(resolution, "key")
        assert "<!-- kind: challenge -->" in challenge
        assert "<!-- kind: resolution -->" in resolution
        assert challenge_key == resolution_key
        assert comment(challenge, "pattern") == comment(resolution, "pattern")
        assert len(re.findall(r"^-\s+.+$", challenge, re.MULTILINE)) == 4
        assert len(re.findall(r"^-\s+.+$", resolution, re.MULTILINE)) == 4


def test_published_artifacts_match_sources_and_have_no_active_content():
    manifest_entries = {}
    for line in (TRAINING / "ARTIFACTS.sha256").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        digest, relative = line.split("  ", 1)
        manifest_entries[relative] = digest

    expected_paths = {
        "docs/training/LEARNING-GUIDE.md",
        "docs/training/LEARNING-DECK.md",
        "docs/training/learning-theme.css",
        "docs/training/RedSec-Range-Learning-Guide.pdf",
        "docs/training/RedSec-Range-Learning-Deck.pptx",
    }
    assert set(manifest_entries) == expected_paths
    for relative, expected_digest in manifest_entries.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected_digest

    pdf = TRAINING / "RedSec-Range-Learning-Guide.pdf"
    pdf_bytes = pdf.read_bytes()
    assert pdf_bytes.startswith(b"%PDF-")
    assert pdf_bytes.rstrip().endswith(b"%%EOF")
    for active_marker in (b"/JavaScript", b"/EmbeddedFile", b"/Launch", b"/OpenAction"):
        assert active_marker not in pdf_bytes

    reader = PdfReader(pdf)
    assert not reader.is_encrypted
    guide_digest = hashlib.sha256((TRAINING / "LEARNING-GUIDE.md").read_bytes()).hexdigest()
    assert f"source-sha256:{guide_digest}" in (reader.metadata.get("/Keywords") or "")
    catalog = reader.trailer["/Root"]
    assert "/OpenAction" not in catalog
    assert "/AA" not in catalog
    names = catalog.get("/Names")
    if names:
        names = names.get_object()
        assert "/JavaScript" not in names
        assert "/EmbeddedFiles" not in names
    for page in reader.pages:
        assert "/AA" not in page

    pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    compact_pdf_text = re.sub(r"\s+", "", pdf_text)
    positions = []
    for key in expected_keys():
        position = compact_pdf_text.find(key)
        assert position >= 0, f"catalog key missing from PDF: {key}"
        positions.append(position)
    assert positions == sorted(positions)

    pptx = TRAINING / "RedSec-Range-Learning-Deck.pptx"
    with zipfile.ZipFile(pptx) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        slide_parts = sorted([
            name for name in names
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        ], key=lambda name: int(re.search(r"\d+", Path(name).stem).group()))
        assert len(slide_parts) == 220
        assert not any(
            marker in name.lower()
            for name in names
            for marker in ("vbaproject", "embeddings/", "oleobject", "externallink")
        )
        for name in (item for item in names if item.endswith(".rels")):
            root = ElementTree.fromstring(archive.read(name))
            assert all(rel.attrib.get("TargetMode") != "External" for rel in root)

        deck_digest = hashlib.sha256((TRAINING / "LEARNING-DECK.md").read_bytes()).hexdigest()
        core_properties = archive.read("docProps/core.xml").decode()
        assert f"source-sha256:{deck_digest}" in core_properties

        blocks = source_slides()
        for part, block in zip(slide_parts, blocks, strict=True):
            root = ElementTree.fromstring(archive.read(part))
            rendered = [
                node.text or ""
                for node in root.findall(f".//{{{DRAWING_NS}}}t")
            ]
            for expected in expected_slide_text(block):
                assert expected in rendered, f"missing rendered text in {part}: {expected}"
