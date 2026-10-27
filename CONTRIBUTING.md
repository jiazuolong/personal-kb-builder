# Contributing

Thanks for helping improve personal-kb-builder.

## Scope

This project is about **procedure and provenance**, not about storing personal data. In scope:

- the skill workflow (`SKILL.md`, `references/`)
- schema variants and templates
- validation and inventory scripts (standard library only)
- synthetic examples and tests

Out of scope: cloud sync services, databases, embeddings/vector search, anything that requires copying the user's raw data.

## Development

```bash
python -m unittest discover -s tests -v
python scripts/check.py --kb examples/demo-kb --check-sources
```

Python 3.9+ with no third-party packages. Keep scripts cross-platform.

## Adding a schema variant

1. Add a section to `references/schema.md` with the folder tree, card fields, and what evidence usually means.
2. If it needs different template files, add them under `templates/kb/`.
3. Update `examples/demo-kb` only if the common skeleton changes.
4. Run the tests and the demo check.

## Editing the skill

- `SKILL.md` must stay compact (the test enforces < 8000 characters). Move detail into `references/`.
- Frontmatter: `name` is kebab-case, `description` is required and should carry the routing triggers in both Chinese and English.
- Do not add agent-specific fields that break other `SKILL.md` loaders.

## Data hygiene (required)

- Never commit personal data, real absolute paths, tokens, or source contents.
- Examples must be synthetic and clearly labeled.
- Test fixtures must be generated in temporary directories.

## Pull requests

- One concern per PR.
- Include the test output for the scripts you changed.
- Update `CHANGELOG.md` for user-visible changes.
