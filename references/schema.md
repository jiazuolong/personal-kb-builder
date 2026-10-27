# Schema variants

Pick one variant during Step 2 of the workflow, then adapt the skeleton. The variants differ only in folder names, card fields, and what "evidence" usually means. Mixing is normal: use `mixed` when no single variant fits.

## Common layer (all variants)

| File | Responsibility |
|---|---|
| `README.md` | Human entry point: purpose, quick tour, how to search |
| `AI_CONTEXT.md` | Agent entry point: identity, long-term questions, answer boundaries, retrieval route |
| `profile/profile.md` | Who the user is, goals, constraints, tools, preferences |
| `timeline.md` | Dated evolution; only sourced or user-confirmed rows |
| `catalog/sources.jsonl` | Machine-readable file manifest (path, type, size, access) |
| `catalog/evidence.md` | Curated evidence: E-IDs, source, locator, kind, limitation |
| `catalog/coverage.json` | What was scanned, counts, limits, gaps |
| `maintenance/update.md` | How to add sources, when to re-review, how to run checks |
| `open-questions.md` | Known unknowns that block interpretation |

## Variant 1 — Research (`research`)

For a researcher or graduate student with papers, slide decks, notes, scripts, and data.

```text
profile/
projects/            # one card per research project (P01, P02, …)
research/            # materials, methods, literature notes
catalog/
maintenance/
```

Project card fields: question, status (unknown / active / paused), evidence table, materials studied, source locations, open questions, next step.

Evidence usually means: slides (locator = slide number), manuscripts (paragraph), code (function), data descriptions (table). Keep parameter-heavy claims attached to their parameters.

## Variant 2 — Work (`work`)

For a knowledge worker managing projects, meetings, decisions, and deliverables.

```text
profile/
projects/            # active and archived projects
areas/               # ongoing responsibilities (team, ops, hiring)
meetings/            # dated meeting notes, one file per meeting
decisions/           # decision records: context, options, decision, date
```

Project card fields: goal, stakeholders, status, decisions, links, risks, next step.
Evidence usually means: meeting notes, email exports, ticket IDs, document versions.

## Variant 3 — Learning (`learning`)

For self-directed study: courses, books, papers, exercises, flashcard material.

```text
profile/
topics/              # one card per subject
sources/             # per-book / per-course notes
questions/           # open questions and answers
```

Topic card fields: scope, key ideas, sources, exercises, open questions.
Evidence usually means: book page or chapter, lecture timestamp, paper section, exercise number.

## Variant 4 — Life archive (`life`)

For personal records: health, finance summaries, home, family, travel, hobbies.

```text
profile/
areas/               # home, health, finance, family, hobbies
records/             # dated records and receipts indexes (never raw scans)
people/              # important people and context (opt-in only)
```

Area card fields: scope, recurring events, documents index, open questions.
Evidence usually means: receipt date and amount, appointment date, document title. Keep sensitive identifiers out; reference them, do not transcribe them.

## Life/mixed

If the user wants one KB for everything, keep top-level `areas/` and `projects/` and let each card declare its domain in frontmatter:

```yaml
---
type: project | area | topic
domain: research | work | learning | life
status: active | paused | archived | unknown
---
```

Do not invent a taxonomy the user did not ask for. Start with 3–6 top-level folders; add more only when a second item needs them.

## Card conventions

- One card = one page, short enough to read in two minutes.
- Each card starts with a one-sentence question or purpose.
- Each card ends with sources and open questions, not with a summary of everything.
- Stable IDs: `P01`, `P02` for projects; `E001` for evidence; `F-<12hex>` for indexed files if needed.
- Dates: absolute (`2026-10-27`), never "last week".
