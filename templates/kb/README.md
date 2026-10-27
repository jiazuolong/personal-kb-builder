# {{KB_NAME}}

A personal knowledge base built with [personal-kb-builder](https://github.com/jiazuolong/personal-kb-builder).
Created on {{DATE}} · variant: {{VARIANT}} · raw data roots: {{DATA_ROOTS}}

This KB stores structure, summaries, provenance, and indexes. **Raw data stays where it is.**

## Start here

| Entry | What it contains |
|---|---|
| [profile/profile.md](profile/profile.md) | Who you are, goals, constraints, tools |
| [projects/](projects/) | One card per project or area |
| [topics/](topics/) | Subject and method notes |
| [timeline.md](timeline.md) | Dated evolution |
| [catalog/evidence.md](catalog/evidence.md) | Curated evidence with sources and limits |
| [catalog/coverage.json](catalog/coverage.json) | What was scanned and what was not |
| [open-questions.md](open-questions.md) | Known unknowns |
| [maintenance/update.md](maintenance/update.md) | How to add and review sources |

## How to use it

- Keep one card per project/topic; short enough to read in two minutes.
- Every claim points to a source, or is marked as user-confirmed.
- When adding material: record the source, read the relevant part, write the summary, note the limitation, run the check.
- Current status unknown? Write `TBD / 待确认`, never a guess.

## Maintenance

```bash
python <skill>/scripts/scan.py --root <your-data-folder> --out catalog
python <skill>/scripts/check.py --kb .
```

## Boundaries

- Raw documents, images, datasets, and scripts are not stored here.
- Nothing in this KB is a substitute for the original source.
- The KB records what a source says; it does not independently verify it.
