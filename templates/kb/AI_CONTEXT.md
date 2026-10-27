# AI context — {{KB_NAME}}

This file is the entry point for AI assistants. Read it first, then follow the retrieval route below. Answer boundaries are part of the instruction, not decoration.

## Who this KB belongs to

- Name / handle: TBD
- Field or role: TBD
- Current stage: TBD
- Source of these facts: `profile/profile.md` (built from user answers on {{DATE}})

## Long-term questions

<!-- Replace with 1–3 questions the KB exists to answer. Keep them stable; they drive the schema. -->

1. TBD
2. TBD
3. TBD

## Map of the KB

| Topic | First read |
|---|---|
| Projects | `projects/` |
| Topics / methods | `topics/` |
| Timeline | `timeline.md` |
| Sources and evidence | `catalog/evidence.md` |
| Coverage and gaps | `catalog/coverage.json` |
| Open questions | `open-questions.md` |

## What the evidence can support

<!-- After seeding, summarize here which layers exist: user-confirmed, documents, plans, code structure, second-hand. Keep it short. -->

- TBD

## Must-keep distinctions

1. A source statement is not an independently verified fact.
2. Code existing is not code running.
3. Plans are not results; drafts are not publications.
4. Model output, measurement, and experiment are separate evidence layers.
5. Current status is unknown unless the user or a dated source says otherwise.

## Retrieval route

1. Read this file.
2. Open the relevant project or topic card.
3. Search `catalog/evidence.md` for the relevant E-IDs; follow their sources.
4. Read the source in place (read-only). Do not copy it into the KB.
5. Cite E-ID + locator + source path.

## Storage and boundaries

- Raw data roots: `{{DATA_ROOTS}}`
- Raw data is read-only and never copied into this KB.
- Do not execute scripts or notebooks from the sources.
- When in doubt, say the current status is unknown and point to `open-questions.md`.
