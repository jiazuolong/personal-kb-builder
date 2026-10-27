# AI context — Demo Learning KB

This file is the entry point for AI assistants. It is part of a **synthetic demo**.

## Who this KB belongs to

- Name / handle: Demo Learner (fictional)
- Field or role: Self-directed learner
- Current stage: demo only
- Source of these facts: `profile/profile.md` (built from user answers on 2026-10-27)

## Long-term questions

1. What have I read, and what does each source actually claim?
2. Which claims are from a source, and which did I confirm myself?
3. What is still unclear about spaced repetition?

## Map of the KB

| Topic | First read |
|---|---|
| Topics / methods | `topics/` |
| Timeline | `timeline.md` |
| Sources and evidence | `catalog/evidence.md` |
| Coverage and gaps | `catalog/coverage.json` |
| Open questions | `open-questions.md` |

## What the evidence can support

- E001: one reading note reports an argument and two small classroom studies. It is `document-reported`, not verified.
- E002: a course outline lists modules and an assessment, but not the grading rubric. It is `document-reported` with a `partial` limitation.

Nothing here is `user-confirmed` except the existence of this demo.

## Must-keep distinctions

1. A source statement is not an independently verified fact.
2. Plans are not results; drafts are not publications.
3. A course outline does not prove the course was taken or passed.
4. Current status is unknown unless the user or a dated source says otherwise.

## Retrieval route

1. Read this file.
2. Open the relevant topic card.
3. Search `catalog/evidence.md` for the relevant E-IDs; follow their sources.
4. Read the source in place (read-only). Do not copy it into the KB.
5. Cite E-ID + locator + source path.

## Storage and boundaries

- Raw data roots: `examples/demo-data`
- Raw data is read-only and never copied into this KB.
- Do not execute scripts or notebooks from the sources.
- When in doubt, say the current status is unknown and point to `open-questions.md`.
