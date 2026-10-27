# Platforms and installation

The KB is plain Markdown and plain files. The Skill bundle follows the common `SKILL.md` convention, so any agent that loads skill bundles can use it. DSH is the reference implementation.

## DSH

Skill roots are scanned one level deep. Install by placing the whole directory under one of:

```text
<project>/.dsh/skills/personal-kb-builder/
<project>/.agents/skills/personal-kb-builder/
~/.dsh/skills/personal-kb-builder/          (user-wide)
~/.agents/skills/personal-kb-builder/       (user-wide)
```

`SKILL.md` must be at the root of that directory. Invoke it:

- model: the agent calls the `skill` tool with `name: personal-kb-builder`
- user: type `/personal-kb-builder` in the composer

If you edit `SKILL.md`, open a new session or switch presets so the catalog refreshes.

## Other SKILL.md agents

Place the same directory in the agent's skills directory (for example `.claude/skills/personal-kb-builder/` for Claude Code). The bundle is deliberately generic:

- frontmatter uses only `name`, `description`, `whenToUse`
- the only agent-specific reference is the question tool: `ask_user_question` in DSH; use the equivalent structured question tool elsewhere, or ask the same questions in prose
- scripts are Python 3.9+ standard library only; no network, no install

## Python scripts

Run them directly; no virtualenv is required:

```bash
python scripts/init_kb.py --target ~/my-kb --name "My KB" --variant research --lang zh
python scripts/scan.py --root ~/Documents --out ~/my-kb/catalog --exclude "**/.git/**"
python scripts/check.py --kb ~/my-kb
```

On Windows use `py` or `python` from any PowerShell/cmd window.

## Manual use without an agent

The workflow is explicit enough to follow by hand:

1. Read `references/schema.md`, choose a variant.
2. Copy `templates/kb/` to a new folder.
3. Replace `{{KB_NAME}}`, `{{DATE}}`, `{{DATA_ROOTS}}`.
4. Run `scripts/scan.py` to build the manifest.
5. Fill `catalog/evidence.md` for 3–5 items, then run `scripts/check.py`.

## Updating

- Keep the KB as its own git repository if the user wants history.
- Do not store raw data in the KB repository; store paths and summaries.
- Re-run `scripts/scan.py` after adding files; re-run `scripts/check.py` after editing evidence.
