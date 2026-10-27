---
name: personal-kb-builder
description: Turn a user's own files into a traceable Markdown personal knowledge base. Use when someone wants to build a personal database, second brain, research wiki, or organized archive from documents, notes, papers, or code, with sources and provenance. 个人知识库、个人数据库、整理个人资料、把资料变成可追溯的 Markdown 库时使用。
whenToUse: The user wants a durable, source-linked Markdown knowledge base from their own data folders, not a one-off summary or a single answer. Works for research, work, study, and life archives.
---

# Personal KB Builder

Build a personal knowledge base (KB) from data the user already has. The raw data stays where it is; the KB stores structure, summaries, provenance, and a small index. The result is readable by humans and by future AI sessions.

## What you produce

A directory (the KB) containing:

- `README.md` — human entry point: what this KB is, how to use it
- `AI_CONTEXT.md` — agent entry point: identity, goals, answer boundaries, retrieval route
- `profile/` — who the user is and what they are trying to do (from the interview)
- `projects/` or `areas/` — one card per project or area of responsibility
- `topics/` or `research/` — domain, material, or method notes
- `timeline.md` — dated evolution, only from sources or user statements
- `catalog/` — `sources.jsonl` (file manifest), `evidence.md` (curated evidence), `coverage.json` (coverage and gaps)
- `maintenance/` — update rules and checks
- optional: `AGENTS.md` (agent operating rules), `tools/` (index scripts)

## Boundaries (non-negotiable)

1. Raw data is read-only and stays in place. Never copy, move, unzip, or import source files into the KB, a temp directory, or the agent workspace.
2. Never execute scripts, notebooks, or binaries found in the source data.
3. Ask before scanning. Do not scan an entire disk, home directory, cloud mount, or network share without explicit confirmation.
4. Exclude secrets and sensitive records: passwords, tokens, keys, ID scans, financial and medical records. Only include them if the user explicitly selects a sanitized subset.
5. Never fabricate content. Every claim in the KB must point to a source path + locator, or be marked as user-confirmed.
6. Keep raw volume out of context. Inspect samples, file metadata, and indexes; summarize instead of pasting file contents.

## Workflow

### Step 0 — Intake (interview)

Ask no more than 3 questions at a time:

1. Goal: research, work projects, learning, life archive, or mixed?
2. Where is the data: local folder(s), external or cloud-synced folder, or a few files to upload?
3. What must be excluded: private directories, file types, people, topics?

Then ask at most 3 more: approximate size and type mix, existing tools (Obsidian, Zotero, Notion export, bookmarks), output language.

Use the environment's structured question tool when available (`ask_user_question` in DSH). Put the recommended option first and mark it `(Recommended)`. Never ask for passwords or tokens. For paths, give examples and let the user type the real path.

### Step 1 — Inventory (read-only)

Sample one or two directories first, then produce a manifest:

- file counts and bytes by extension and year
- inaccessible or huge subtrees
- duplicate names (do not diff contents yet)

Write `catalog/sources.jsonl` and `catalog/coverage.json` with `scripts/scan.py` or an equivalent read-only pass. Report gaps explicitly; never claim completeness.

### Step 2 — Propose the schema

Pick a variant from `references/schema.md` (research, work, learning, life/mixed) based on the interview. Show the proposed folder tree and 2–3 sample cards. Ask the user to confirm or adjust: use as-is / simplify / change variant.

### Step 3 — Generate the skeleton

Copy `templates/kb/` or run `scripts/init_kb.py`. Fill only what the interview answered. Leave unknown fields as `TBD / 待确认`. Every card starts as a stub with source pointers, not invented prose.

### Step 4 — Seed the end-to-end loop

Pick 3–5 representative items (one document, one project, one note set). For each: source path → locator → summary → evidence kind → limitation. Add them to `catalog/evidence.md` and link them from the relevant card. Then run `scripts/check.py`.

### Step 5 — Verify and hand off

Run the checks, show `coverage.json` gaps, and give the user a short maintenance guide (`maintenance/update.md`): how to add a source, when to re-review, what "current" means.

## Evidence rules

Each curated item in `catalog/evidence.md` carries:

- `id`: `E001`, `E002`, … (stable, unique)
- `source`: absolute path, or archive path + member
- `locator`: page / paragraph / function / table / timestamp
- `kind`: user-confirmed | document-reported | plan | code-structure | second-hand | path-only
- `limitation`: unverified, single run, specific parameters, stale, image-only, etc.
- optional: `reviewed_at`, `reviewed_sha256`

Rules: a document's statement is not an independently verified fact; code existing is not code working; plans are not results; path presence is not content. See `references/evidence.md`.

## Reference map

- `references/schema.md` — framework variants and file responsibilities
- `references/interview.md` — full question bank and question-tool patterns
- `references/evidence.md` — provenance model, ID scheme, limits
- `references/platforms.md` — install paths for DSH and other SKILL.md agents
- `scripts/init_kb.py`, `scripts/scan.py`, `scripts/check.py`
- `templates/kb/` — copyable skeleton

## Definition of done

- [ ] Interview answers recorded in `profile/`
- [ ] `catalog/sources.jsonl` and `catalog/coverage.json` exist and state gaps
- [ ] Every project/topic card has at least one source, or is marked as a stub
- [ ] 3–5 evidence entries with locator and limitation
- [ ] `scripts/check.py` passes
- [ ] Raw data unchanged; no source file copied into the KB
