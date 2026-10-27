# Changelog

## 0.1.0 — 2026-10-27

Initial release.

- `SKILL.md`: 6-step workflow (intake → inventory → schema → skeleton → seed → verify) with evidence rules and boundaries.
- `references/`: schema variants (research, work, learning, life/mixed), interview protocol and question bank, evidence model, platform installation.
- `templates/kb/`: copyable Markdown skeleton with profile, project/topic cards, timeline, open questions, catalog, maintenance.
- `scripts/init_kb.py`: scaffold a KB from templates.
- `scripts/scan.py`: read-only inventory → `catalog/sources.jsonl` and `coverage.json`.
- `scripts/check.py`: validate required files, evidence IDs and fields, Markdown links, JSON catalog, optional source existence and hashes.
- `examples/demo-kb`: synthetic demo with two evidence records.
- Unit tests and GitHub Actions validation.
