"""Static contracts for the defensive guide and paired workshop deck."""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
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


def expected_provenance_urls() -> set[str]:
    catalog = load_catalog()
    urls = set()
    for definition in catalog.ranges.values():
        urls.add(
            definition.source.repository.removesuffix(".git")
            if definition.source
            else definition.homepage
        )
        if definition.curriculum.solution_url:
            urls.add(definition.curriculum.solution_url)
    return urls


def input_fingerprint(*paths: Path) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


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
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "assemble_learning_materials.py"), "--check"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

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

    catalog = load_catalog()
    for range_id, definition in catalog.ranges.items():
        assert f"| `{range_id}` | {definition.maintainer} | {definition.license} |" in guide

    expected_patterns = {
        "builtin/04/session-smuggling": "session-context",
        "builtin/05/knowledge-poisoning": "rag",
        "builtin/06/embedding-inversion": "embeddings",
        "builtin/07/resource-traversal": "path",
        "builtin/07/command-injection": "command",
        "builtin/09/metadata-ssrf": "infra",
        "dvaa/L2-03": "path",
        "dvaa/L2-08": "tool-registration",
        "dvaa/L3-02": "infra",
        "dvaa/L3-06": "tool-dataflow",
        "dvaa/L3-07": "tool-shadowing",
        "mcpgoat/D1": "command",
        "mcpgoat/D2": "path",
        "mcpgoat/D3": "infra",
        "mcpgoat/D4": "sql",
        "mcpgoat/D5": "nosql",
        "mcpgoat/D6": "template",
        "mcpgoat/D7": "xml",
        "mcpgoat/D8": "deserialization",
    }
    patterns = {
        comment(block, "key"): comment(block, "pattern")
        for block in source_slides()
        if comment(block, "kind") == "challenge"
    }
    for key, pattern_id in expected_patterns.items():
        assert patterns[key] == pattern_id
    assert set(patterns) == set(keys)

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

    assert len(slides) == 222
    for pair_index in range(0, 220, 2):
        challenge, resolution = slides[pair_index:pair_index + 2]
        challenge_key = comment(challenge, "key")
        resolution_key = comment(resolution, "key")
        assert "<!-- kind: challenge -->" in challenge
        assert "<!-- kind: resolution -->" in resolution
        assert challenge_key == resolution_key
        assert comment(challenge, "pattern") == comment(resolution, "pattern")
        assert len(re.findall(r"^-\s+.+$", challenge, re.MULTILINE)) == 4
        assert len(re.findall(r"^-\s+.+$", resolution, re.MULTILINE)) == 4
    for appendix_index, appendix in enumerate(slides[220:], 1):
        assert "<!-- kind: attribution -->" in appendix
        assert comment(appendix, "key") == f"attribution/{appendix_index}"
        assert len(re.findall(r"^-\s+.+$", appendix, re.MULTILINE)) == 3


def test_published_artifacts_match_sources_and_allow_only_expected_links():
    manifest_entries = {}
    for line in (TRAINING / "ARTIFACTS.sha256").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        digest, relative = line.split("  ", 1)
        manifest_entries[relative] = digest

    expected_paths = {
        "scripts/assemble_learning_materials.py",
        "scripts/build_learning_materials.py",
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
    guide_digest = input_fingerprint(
        TRAINING / "LEARNING-GUIDE.md",
        TRAINING / "learning-theme.css",
        ROOT / "scripts" / "build_learning_materials.py",
    )
    assert f"input-sha256:{guide_digest}" in (reader.metadata.get("/Keywords") or "")
    catalog = reader.trailer["/Root"]
    assert "/OpenAction" not in catalog
    assert "/AA" not in catalog
    names = catalog.get("/Names")
    if names:
        names = names.get_object()
        assert "/JavaScript" not in names
        assert "/EmbeddedFiles" not in names
    allowed_uris = expected_provenance_urls()
    observed_uris: set[str] = set()
    for page in reader.pages:
        assert "/AA" not in page
        for annotation_ref in page.get("/Annots") or []:
            annotation = annotation_ref.get_object()
            assert "/AA" not in annotation
            action = annotation.get("/A")
            if not action:
                continue
            action = action.get_object()
            assert action.get("/S") == "/URI"
            uri = str(action.get("/URI", ""))
            assert uri.startswith("https://")
            assert uri in allowed_uris
            observed_uris.add(uri)
    assert observed_uris == allowed_uris

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
        assert len(slide_parts) == 222
        assert all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist())
        assert not any(
            marker in name.lower()
            for name in names
            for marker in ("vbaproject", "embeddings/", "oleobject", "externallink")
        )
        for name in (item for item in names if item.endswith(".rels")):
            root = ElementTree.fromstring(archive.read(name))
            assert all(rel.attrib.get("TargetMode") != "External" for rel in root)

        deck_digest = input_fingerprint(
            TRAINING / "LEARNING-DECK.md",
            ROOT / "scripts" / "build_learning_materials.py",
        )
        core_properties = archive.read("docProps/core.xml").decode()
        assert f"input-sha256:{deck_digest}" in core_properties
        presentation_xml = b"".join(archive.read(name) for name in names if name.endswith(".xml"))
        assert b"Avenir Next" not in presentation_xml
        assert b"Arial" in presentation_xml

        blocks = source_slides()
        for part, block in zip(slide_parts, blocks, strict=True):
            root = ElementTree.fromstring(archive.read(part))
            rendered = [
                node.text or ""
                for node in root.findall(f".//{{{DRAWING_NS}}}t")
            ]
            for expected in expected_slide_text(block):
                assert expected in rendered, f"missing rendered text in {part}: {expected}"
