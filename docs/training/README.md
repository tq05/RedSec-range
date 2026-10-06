# RedSec defensive learning materials

- `RedSec-Range-Learning-Guide.pdf` covers all 110 catalog concepts / 162
  variants through trust boundaries, guided review questions, defensive controls,
  validation ideas, gotchas, and source provenance.
- `RedSec-Range-Learning-Deck.pptx` contains exactly two slides per challenge:
  a challenge description and educational focus, followed by defensive resolution
  and review gotchas (220 slides total).
- `LEARNING-GUIDE.md` and `LEARNING-DECK.md` are the editable generated sources.
- `ARTIFACTS.sha256` records source and artifact digests. Each generated artifact
  also embeds the digest of its Markdown source, and static tests compare rendered
  keys, slide text, and ordering with that source.

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
```

The assembler does not execute or import third-party range code. Static contracts
check catalog completeness, challenge/resolution pairing, source-to-artifact hashes,
and the absence of active PDF or PowerPoint content.
