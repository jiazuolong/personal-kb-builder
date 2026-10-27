# personal-kb-builder

[![validate](https://github.com/jiazuolong/personal-kb-builder/actions/workflows/validate.yml/badge.svg)](https://github.com/jiazuolong/personal-kb-builder/actions/workflows/validate.yml)

[中文说明](README.zh-CN.md) · [Demo](examples/demo-kb) · [SKILL.md](SKILL.md)

A portable agent **Skill** that turns your own files into a traceable, Markdown-based personal knowledge base.

> Raw data stays where it is. The KB stores structure, summaries, provenance, and indexes — not copies of your files.

## Why

Personal data piles up in folders: papers, notes, slides, code, exports, bookmarks. Chat assistants can summarize one file, but they forget the structure, the sources, and the uncertainty. A personal KB fixes that, if it is built with discipline:

- **one card per project/topic**, short enough to read;
- **every claim has a source and a locator**;
- **evidence kinds are distinguished** (a plan is not a result, code is not execution);
- **gaps are recorded**, not smoothed over;
- **raw data is never copied or executed**.

This skill encodes that discipline as a repeatable workflow: an interview, a read-only inventory, a schema proposal, a skeleton, a seeded end-to-end loop, and checks.

## How it works

```text
Intake (ask_user_question)
   -> Inventory (read-only scan)
   -> Schema proposal (research / work / learning / life / mixed)
   -> Skeleton (templates, no invented content)
   -> Seed 3-5 items end to end (source -> evidence -> card -> check)
   -> Handoff (maintenance guide, coverage gaps)
```

The AI asks at most 3 questions per round and at most 8 in total. It never scans before the user confirms the scope, never copies source files, and never executes scripts from the data.

## Quick start

### With an agent (DSH, or any agent that loads `SKILL.md` bundles)

```bash
# DSH: one of these roots
cp -r personal-kb-builder ~/.dsh/skills/
# or: <project>/.dsh/skills/  or  <project>/.agents/skills/
```

Then ask the agent to build your personal knowledge base, or invoke it directly:

- DSH: `/personal-kb-builder`
- model-facing: the `skill` tool with `name: personal-kb-builder`

See [references/platforms.md](references/platforms.md) for details and for other agents.

### With the CLI (no agent required)

```bash
python scripts/init_kb.py --target ~/my-kb --name "My KB" --variant research --lang zh \
  --data-roots "/Users/me/Documents,/Volumes/Archive"
python scripts/scan.py --root "/Users/me/Documents" --out ~/my-kb/catalog
python scripts/check.py --kb ~/my-kb
```

Python 3.9+ standard library only. No network, no install, no database.

## What you get

```text
my-kb/
  README.md            # human entry point
  AI_CONTEXT.md        # agent entry point: goals, boundaries, retrieval route
  AGENTS.md            # optional agent rules
  profile/profile.md   # from the interview
  projects/            # one card per project
  topics/              # subject / method notes
  timeline.md
  open-questions.md
  catalog/
    evidence.md        # E-IDs: source, locator, kind, limitation
    sources.jsonl      # read-only file manifest
    coverage.json      # what was scanned, what was not
  maintenance/update.md
```

## Evidence model

| Field | Meaning |
|---|---|
| `source` | Absolute path, or archive path + member |
| `locator` | Page / paragraph / slide / function / table |
| `kind` | `user-confirmed` · `document-reported` · `plan` · `code-structure` · `second-hand` · `path-only` |
| `limitation` | `unverified` · `single-run` · `parameters:…` · `stale` · `image-only` · `partial` · `second-hand` |

The distinction is the point: a report saying "we did X" is not an audit of X; a file existing is not a file working; a plan is not a result.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/init_kb.py` | Scaffold a KB from `templates/kb/` |
| `scripts/scan.py` | Read-only inventory → `sources.jsonl` + `coverage.json` |
| `scripts/check.py` | Validate required files, E-IDs, fields, links, JSON, optionally sources |

Run the checks after every editing session:

```bash
python scripts/check.py --kb ~/my-kb --check-sources
```

## Repository layout

```text
SKILL.md              # the skill procedure
references/           # read on demand: schema variants, interview, evidence, platforms
templates/kb/         # copyable skeleton
scripts/              # init / scan / check (stdlib)
examples/             # synthetic demo KB + demo data
tests/                # unit tests
```

## Design principles

1. **Raw data is read-only.** No copying, moving, unzipping, or executing.
2. **Minimal end-to-end first.** Skeleton → 3–5 seeded items → checks; add depth later.
3. **Provenance over prose.** A claim without a locator is a guess.
4. **Ask, don't assume.** Structured questions with recommended options; 8 questions max.
5. **Gaps are first-class.** `open-questions.md` and `coverage.json` are features, not failures.
6. **Portable by default.** Plain Markdown, plain files, standard-library scripts.

## Development

```bash
python -m unittest discover -s tests -v
python scripts/check.py --kb examples/demo-kb --check-sources
```

The demo is synthetic. Do not commit personal data, real paths, or source contents to this repository.

## License

MIT — see [LICENSE](LICENSE).
