#!/usr/bin/env python3
"""Scaffold a personal knowledge base from the bundled templates.

Read-only with respect to the user's data: this script only writes inside the
target directory.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

# Files copied from templates/kb; sources.example.jsonl is not copied as-is.
SKIP_NAMES = {"sources.example.jsonl"}
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yml", ".yaml", ".txt"}

PLACEHOLDERS = ("{{KB_NAME}}", "{{DATE}}", "{{VARIANT}}", "{{LANGUAGE}}", "{{DATA_ROOTS}}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a personal knowledge base skeleton (Markdown + catalog).",
    )
    parser.add_argument("--target", required=True, help="Directory to create (must be empty or new).")
    parser.add_argument("--name", default="My Knowledge Base", help="Human-readable KB name.")
    parser.add_argument(
        "--variant",
        default="mixed",
        choices=["research", "work", "learning", "life", "mixed"],
        help="Schema variant; see references/schema.md.",
    )
    parser.add_argument("--lang", default="zh", choices=["zh", "en"], help="KB output language.")
    parser.add_argument(
        "--data-roots",
        default="TBD",
        help="Comma-separated raw data roots, e.g. '/Users/me/Documents,/Volumes/Archive'.",
    )
    parser.add_argument("--date", default=date.today().isoformat(), help="Creation date (YYYY-MM-DD).")
    parser.add_argument("--force", action="store_true", help="Write into a non-empty target directory.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    template = Path(__file__).resolve().parents[1] / "templates" / "kb"
    if not template.is_dir():
        print(f"error: templates not found at {template}", file=sys.stderr)
        return 2

    target = Path(args.target).expanduser().resolve()
    if target.exists() and any(target.iterdir()) and not args.force:
        print(f"error: target is not empty: {target} (use --force to merge)", file=sys.stderr)
        return 2

    language = {"zh": "中文", "en": "English"}[args.lang]
    values = {
        "{{KB_NAME}}": args.name,
        "{{DATE}}": args.date,
        "{{VARIANT}}": args.variant,
        "{{LANGUAGE}}": language,
        "{{DATA_ROOTS}}": args.data_roots,
    }

    created = 0
    for source in sorted(template.rglob("*")):
        if source.is_dir():
            continue
        if source.name == ".gitkeep" or source.name in SKIP_NAMES:
            continue
        relative = source.relative_to(template)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() in TEXT_SUFFIXES:
            text = source.read_text(encoding="utf-8")
            for key, value in values.items():
                text = text.replace(key, value)
            with destination.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
        else:
            shutil.copyfile(source, destination)
        created += 1

    # The manifest starts empty; scanning fills it later.
    (target / "catalog").mkdir(parents=True, exist_ok=True)
    manifest = target / "catalog" / "sources.jsonl"
    if not manifest.exists():
        manifest.write_text("", encoding="utf-8")

    print(f"Created KB at {target}")
    print(f"  variant: {args.variant} | language: {language} | files: {created}")
    print("Next steps:")
    print(f"  1. Fill profile/profile.md from the intake interview.")
    print(f"  2. Run: python scripts/scan.py --root <data-root> --out \"{target / 'catalog'}\"")
    print(f"  3. Add 3-5 evidence records to catalog/evidence.md, then run: python scripts/check.py --kb \"{target}\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
