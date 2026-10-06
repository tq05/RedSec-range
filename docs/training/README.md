# RedSec defensive learning materials

- `RedSec-Range-Learning-Guide.pdf` contains 110 concept-level cards representing
  162 declared variants, with trust boundaries, guided review questions, defensive
  controls, validation ideas, gotchas, and source provenance.
- `RedSec-Range-Learning-Deck.pptx` contains exactly two slides per catalog concept:
  a challenge description and educational focus, followed by defensive resolution
  and review gotchas, plus two attribution slides (222 slides total).
- `LEARNING-GUIDE.md` and `LEARNING-DECK.md` are the editable generated sources.
- `ARTIFACTS.sha256` records generator, source, theme, and artifact digests. Each
  generated artifact also embeds a digest of its relevant build inputs, and static
  tests compare rendered keys, slide text, and ordering with the Markdown source.

This edition intentionally omits challenge secrets, operational payloads, sealed
answers, and step-by-step exploitation procedures. Runtime exploitability is
**not verified—outside the current scope**. Existing RedSec and upstream evidence
is linked as provenance rather than copied into the artifacts.

Regenerate the sources from repository-owned manifests and catalog metadata, then
build both artifacts:

```bash
python -m pip install -e '.[training]'
# macOS: brew install pandoc pango
# Linux: install pandoc plus the Pango/GLib runtime packages.
python scripts/assemble_learning_materials.py
python scripts/build_learning_materials.py
python scripts/assemble_learning_materials.py --check
```

The assembler does not execute or import third-party range code. Static contracts
check regeneration consistency, catalog completeness, challenge/resolution pairing,
build-input fingerprints, and artifact structure. PDF actions are limited to the
pinned HTTPS provenance links printed in the guide; the PowerPoint has no external
relationships or executable content.
