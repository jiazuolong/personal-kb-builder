# Evidence and provenance

A personal KB is only as useful as its ability to answer "where does this come from, and how sure are we?". Keep this model small and consistent.

## Evidence record

Store curated evidence in `catalog/evidence.md`, one section per item:

```markdown
## E001

**Short title**

One- to three-sentence summary. No invented numbers.

- source: `C:/Users/me/Documents/notes/2026-09-reading.md`
- locator: paragraph 12 / slide 8 / function `parse()` / table `results`
- kind: document-reported
- limitation: single run; parameters from one machine; image not OCR'd
- reviewed_at: 2026-10-27
```

Required fields: `source`, `locator`, `kind`, `limitation`. Optional: `reviewed_at`, `reviewed_sha256`.

`scripts/check.py` verifies that every `E###` mentioned anywhere in the KB has a matching section and that the four required fields are present.

## Evidence kinds

| kind | Meaning | May be written as |
|---|---|---|
| `user-confirmed` | The user said it in conversation | "You confirmed that …" |
| `document-reported` | A file states it (slide, paper, report) | "The 2025-03 report states …" |
| `plan` | A plan or proposal, not done work | "The plan proposes …" |
| `code-structure` | Code exists with this structure | "The repository contains a parser for …" |
| `second-hand` | A summary, old AI draft, or someone else's account | "An older summary claims …" |
| `path-only` | Only a path or filename is known | "A file named X exists at …" |

Rules:

- `document-reported` is not independently verified. Say "the document reports", not "it is true".
- `code-structure` is not execution. Say "code exists", not "it works".
- `plan` is not a result.
- `path-only` is not content. Do not summarize a file you have not opened.
- A model prediction, a DFT run, and an experiment are different evidence layers; never merge them into one claim.

## Limitations taxonomy

Use one or more:

- `unverified` — not checked against the source
- `single-run` — one calculation, one experiment, one observation
- `parameters:<names>` — only valid for specific parameters/settings
- `stale` — source changed after the summary was written
- `image-only` — content exists only in images or scans
- `partial` — only part of the source was read
- `second-hand` — not the primary source

## Review and change detection

- `reviewed_at` is the date a human or agent last read the source.
- `reviewed_sha256` is optional; when present, `scripts/check.py --check-hashes` marks stale records.
- File modification time is not research time and not review time. Do not infer dates from it.
- When a source changes, update the summary; never keep two contradictory "current" statements.

## "Current status" rules

- Unknown current status stays unknown. Write `TBD / 待确认`, not a guess.
- User statements override older summaries. Record the date of the user statement.
- Do not promote a plan to "done" because a later file exists.
- Do not claim "complete", "verified", "published", or "converged" unless the source supports exactly that.

## Coverage

`catalog/coverage.json` records what was scanned and what was not: roots, counts, skipped subtrees, inaccessible files, and explicit limits. A file count is not a knowledge count: 10,000 indexed files may produce 20 evidence records.

## Index vs evidence

- `catalog/sources.jsonl` is an automatic, cheap manifest of files. It proves nothing about content.
- `catalog/evidence.md` is curated and expensive. It carries claims with locators and limits.
- Never let the manifest masquerade as evidence.
