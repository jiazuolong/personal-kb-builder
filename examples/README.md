# Demo: a synthetic learning KB

This folder shows what a finished `personal-kb-builder` result looks like. Everything here is **synthetic** — no real person, no real course, no personal data.

- `demo-kb/` — a small knowledge base built with the templates
- `demo-data/` — two fake source notes that the demo KB points at

Try it:

```bash
python scripts/check.py --kb examples/demo-kb
python scripts/check.py --kb examples/demo-kb --check-sources
python scripts/scan.py --root examples/demo-data --out /tmp/demo-catalog
```

`demo-kb/catalog/sources.jsonl` is intentionally empty: the manifest is generated per machine by `scan.py`, and committing absolute paths would be neither portable nor useful.

What to notice in the demo:

- `catalog/evidence.md` records what each source supports, with a locator and a limitation.
- `topics/reading-notes.md` links back to the E-IDs instead of repeating the source.
- `AI_CONTEXT.md` states what the evidence can and cannot support.
- Nothing from `demo-data/` is copied into `demo-kb/`; the cards point at the source.
