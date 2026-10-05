# RedSec learning materials

- `RedSec-Range-Learning-Guide.pdf` is the complete instructor workbook. It covers
  all 110 catalog concepts / 162 runnable variants and includes the two sealed
  built-in answers.
- `RedSec-Range-Learning-Deck.pptx` is the presentation version: one teaching point
  per slide, designed for a guided workshop rather than as an answer dump.
- `LEARNING-GUIDE.md` and `LEARNING-DECK.md` are the editable sources.

Rebuild both artifacts from the repository root:

```bash
python -m pip install -e '.[training]'
# macOS: brew install pandoc pango
# Linux: install pandoc plus the Pango/GLib runtime packages.
python scripts/build_learning_materials.py
```

Maintainers can refresh the guide after changing an external pinned revision by
checking out the four upstream repositories at the revisions in
`ranges/catalog.yaml`, then running:

```bash
python scripts/assemble_learning_guide.py --upstreams /path/to/checkouts
python scripts/build_learning_materials.py
```

The built-in walkthroughs are RedSec-authored and verifier-backed. External answer
material is attributed to its upstream project and pinned revision in the guide.
