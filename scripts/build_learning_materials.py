#!/usr/bin/env python3
"""Build the RedSec learning-guide PDF and PowerPoint deck."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

# Homebrew installs Pango/GLib outside the default macOS dynamic-loader path.
# WeasyPrint loads those libraries during import, so set the fallback first.
if Path("/opt/homebrew/lib").is_dir():
    os.environ.setdefault("DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib")

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
TRAINING = ROOT / "docs" / "training"
GUIDE_MD = TRAINING / "LEARNING-GUIDE.md"
DECK_MD = TRAINING / "LEARNING-DECK.md"
GUIDE_PDF = TRAINING / "RedSec-Range-Learning-Guide.pdf"
DECK_PPTX = TRAINING / "RedSec-Range-Learning-Deck.pptx"
THEME = TRAINING / "learning-theme.css"

NAVY = RGBColor(7, 24, 39)
NAVY_2 = RGBColor(13, 39, 58)
WHITE = RGBColor(246, 249, 248)
MUTED = RGBColor(164, 183, 190)
CYAN = RGBColor(0, 196, 190)
RED = RGBColor(238, 83, 105)
ORANGE = RGBColor(241, 155, 78)
PURPLE = RGBColor(151, 121, 224)
FONT = "Avenir Next"
MONO = "SFMono-Regular"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def build_pdf() -> None:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc is required to build the guide PDF")
    with tempfile.TemporaryDirectory(prefix="redsec-learning-") as temp:
        html = Path(temp) / "guide.html"
        css = Path(temp) / "learning-theme.css"
        css.write_text(THEME.read_text())
        run([
            pandoc,
            str(GUIDE_MD),
            "--from=gfm+attributes",
            "--to=html5",
            "--standalone",
            "--toc",
            "--toc-depth=2",
            "--number-sections",
            f"--css={css.name}",
            "--metadata=lang:en-GB",
            f"--output={html}",
        ])
        HTML(filename=str(html), base_url=str(html.parent)).write_pdf(str(GUIDE_PDF))


def parse_deck() -> list[dict[str, object]]:
    blocks = re.split(r"\n\s*---\s*\n", DECK_MD.read_text().strip())
    slides: list[dict[str, object]] = []
    for block in blocks:
        title_match = re.search(r"^#\s+(.+)$", block, re.M)
        if not title_match:
            continue
        takeaway_match = re.search(r"^>\s*(.+)$", block, re.M)
        bullets = [
            re.sub(r"\*\*(.+?)\*\*", r"\1", match).strip()
            for match in re.findall(r"^-\s+(.+)$", block, re.M)
        ]
        slides.append({
            "title": title_match.group(1).strip(),
            "takeaway": takeaway_match.group(1).strip() if takeaway_match else "",
            "bullets": bullets,
        })
    return slides


def set_fill(shape, color: RGBColor, transparency: int = 0) -> None:
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if transparency:
        shape.fill.transparency = transparency
    shape.line.fill.background()


def add_text(slide, text: str, x: float, y: float, w: float, h: float,
             size: float, color: RGBColor, *, bold: bool = False,
             font: str = FONT, align=PP_ALIGN.LEFT,
             valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run_ = paragraph.add_run()
    run_.text = text
    run_.font.name = font
    run_.font.size = Pt(size)
    run_.font.bold = bold
    run_.font.color.rgb = color
    return box


def add_background(slide, accent: RGBColor, index: int, total: int) -> None:
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = NAVY

    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(.14), Inches(7.5))
    set_fill(band, accent)

    # restrained technical grid
    for x in (9.25, 10.25, 11.25, 12.25):
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(x), Inches(.35), Inches(.012), Inches(6.55)
        )
        set_fill(line, RGBColor(27, 55, 72))
    for y in (1.35, 2.35, 3.35, 4.35, 5.35, 6.35):
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(8.8), Inches(y), Inches(4.1), Inches(.012)
        )
        set_fill(line, RGBColor(27, 55, 72))

    add_text(slide, "REDSEC RANGE  //  LEARNING EDITION", .55, .25, 5.8, .3,
             8.5, MUTED, bold=True)
    add_text(slide, f"{index:02d}", 11.95, .22, .65, .35, 9, accent,
             bold=True, align=PP_ALIGN.RIGHT)

    progress_bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(.55), Inches(7.17), Inches(12.1), Inches(.035)
    )
    set_fill(progress_bg, RGBColor(34, 60, 76))
    progress = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(.55), Inches(7.17),
        Inches(12.1 * index / total), Inches(.035)
    )
    set_fill(progress, accent)


def accent_for(index: int) -> RGBColor:
    if index <= 7:
        return CYAN
    if index <= 11:
        return RED
    if index <= 19:
        return RGBColor(55, 211, 176)
    if index <= 23:
        return ORANGE
    if index <= 29:
        return PURPLE
    return CYAN


def add_title_slide(prs: Presentation, slide_data: dict[str, object], total: int) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = NAVY

    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(.62), Inches(.72), Inches(.12), Inches(5.95)
    )
    set_fill(accent, CYAN)

    add_text(slide, "REDSEC RANGE", 1.08, .74, 4.2, .35, 11, CYAN, bold=True)
    add_text(slide, str(slide_data["title"]), 1.05, 1.35, 7.7, 1.3,
             42, WHITE, bold=True)
    add_text(slide, str(slide_data["takeaway"]), 1.08, 2.76, 7.5, .9,
             22, RGBColor(140, 224, 220))
    add_text(slide, "A guided learning deck", 1.08, 5.95, 4.6, .35,
             10, MUTED, bold=True)
    add_text(slide, "2026 EDITION", 1.08, 6.33, 2.0, .28, 8.5, WHITE, bold=True)

    stats = [("110", "CONCEPTS"), ("162", "VARIANTS"), ("5", "RANGES")]
    for i, (value, label) in enumerate(stats):
        y = 1.32 + i * 1.55
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(y), Inches(2.8), Inches(1.2)
        )
        set_fill(card, NAVY_2)
        card.line.color.rgb = RGBColor(39, 75, 91)
        add_text(slide, value, 9.45, y + .12, 1.1, .54, 28, CYAN, bold=True)
        add_text(slide, label, 10.55, y + .28, 1.15, .3, 9, MUTED, bold=True)

    add_text(slide, f"{total} slides • one takeaway per slide", 9.2, 6.45, 2.8, .3,
             8.5, MUTED, align=PP_ALIGN.RIGHT)


def add_content_slide(prs: Presentation, slide_data: dict[str, object], index: int,
                      total: int) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    accent = accent_for(index)
    add_background(slide, accent, index, total)

    title = str(slide_data["title"])
    title_size = 28 if len(title) < 62 else 24
    add_text(slide, title, .72, .76, 11.35, .92, title_size, WHITE, bold=True)

    takeaway = str(slide_data["takeaway"])
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(.72), Inches(1.82), Inches(10.9), Inches(.88)
    )
    set_fill(box, NAVY_2)
    box.line.color.rgb = accent
    add_text(slide, takeaway, 1.0, 2.00, 10.25, .5, 18, accent, bold=True,
             valign=MSO_ANCHOR.MIDDLE)

    bullets = list(slide_data["bullets"])
    for position, bullet in enumerate(bullets[:4]):
        y = 3.05 + position * .83
        marker = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(.78), Inches(y + .05),
            Inches(.34), Inches(.34)
        )
        set_fill(marker, accent)
        add_text(slide, str(position + 1), .78, y + .045, .34, .34, 9, NAVY,
                 bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_text(slide, bullet, 1.35, y, 9.65, .62, 16.2, WHITE)

    # visual anchor: three connected authority nodes
    nodes = [(11.45, 3.38), (12.18, 4.18), (11.28, 5.0)]
    for n, (x, y) in enumerate(nodes):
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(.42), Inches(.42)
        )
        set_fill(circle, accent if n == 1 else RGBColor(46, 78, 94))
    for x, y, w, rotation in ((11.7, 3.78, .85, 45), (11.52, 4.72, .9, -42)):
        connector = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(.025)
        )
        set_fill(connector, RGBColor(76, 105, 118))
        connector.rotation = rotation

    add_text(slide, "TRUST / DATA / AUTHORITY", 10.65, 5.65, 2.2, .32,
             7.5, MUTED, bold=True, align=PP_ALIGN.CENTER)


def build_deck() -> None:
    slides = parse_deck()
    if len(slides) < 25:
        raise SystemExit(f"deck source unexpectedly short: {len(slides)} slides")
    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    prs.core_properties.title = "RedSec Range — Learning Deck"
    prs.core_properties.subject = "AI, A2A, MCP, supply-chain, and infrastructure security labs"
    prs.core_properties.author = "RedSec Range"
    prs.core_properties.keywords = "AI security, MCP, A2A, red teaming, training"

    add_title_slide(prs, slides[0], len(slides))
    for index, slide_data in enumerate(slides[1:], start=2):
        add_content_slide(prs, slide_data, index, len(slides))
    prs.save(DECK_PPTX)


def main() -> int:
    TRAINING.mkdir(parents=True, exist_ok=True)
    build_pdf()
    build_deck()
    print(f"wrote {GUIDE_PDF}")
    print(f"wrote {DECK_PPTX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
