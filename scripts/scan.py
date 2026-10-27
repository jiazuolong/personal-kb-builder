#!/usr/bin/env python3
"""Read-only inventory of personal data roots.

Writes a file manifest (sources.jsonl) and a coverage report (coverage.json).
Never opens file contents, never copies files, never follows symlinks by default.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_RECORD_KEYS = ("id", "path", "root", "ext", "size_bytes", "access")
DEFAULT_EXCLUDES = (
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    ".cache",
    "$RECYCLE.BIN",
    "System Volume Information",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory data roots and write catalog/sources.jsonl + coverage.json.",
    )
    parser.add_argument("--root", action="append", required=True, help="Data root to scan (repeatable).")
    parser.add_argument("--out", default="catalog", help="Catalog directory to write into (default: catalog).")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Extra exclude pattern; matches a path part, basename, or relative path (repeatable).",
    )
    parser.add_argument("--include-hidden", action="store_true", help="Include dot files and dot directories.")
    parser.add_argument("--follow-symlinks", action="store_true", help="Follow directory symlinks (off by default).")
    parser.add_argument("--ext", default="", help="Comma-separated extension filter, e.g. '.md,.pdf'.")
    parser.add_argument("--max-files", type=int, default=50000, help="Stop after this many indexed files.")
    return parser


def is_excluded(relative_posix: str, name: str, patterns: tuple[str, ...]) -> bool:
    for pattern in patterns:
        if not pattern:
            continue
        if fnmatch.fnmatchcase(name, pattern) or fnmatch.fnmatchcase(relative_posix, pattern):
            return True
        if "*" not in pattern and "?" not in pattern and pattern in relative_posix.split("/"):
            return True
    return False


def file_id(path: str) -> str:
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]
    return f"F-{digest}"


def year_of(timestamp: float) -> str:
    try:
        return str(datetime.fromtimestamp(timestamp, timezone.utc).year)
    except (OSError, OverflowError, ValueError):
        return "unknown"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.max_files < 1:
        print("error: --max-files must be positive", file=sys.stderr)
        return 2

    extensions = {item.strip().lower() for item in args.ext.split(",") if item.strip()}
    patterns = tuple(DEFAULT_EXCLUDES) + tuple(args.exclude)
    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    roots_report: list[dict[str, object]] = []
    skipped: list[dict[str, str]] = []
    inaccessible: list[str] = []
    by_extension: dict[str, int] = {}
    by_year: dict[str, int] = {}
    seen: set[str] = set()
    truncated = False

    for root_arg in args.root:
        root = Path(root_arg).expanduser().resolve()
        root_record: dict[str, object] = {
            "path": str(root),
            "exists": root.is_dir(),
            "file_count": 0,
            "total_bytes": 0,
        }
        if not root.is_dir():
            roots_report.append(root_record)
            skipped.append({"path": str(root), "reason": "root-missing"})
            continue
        if not args.include_hidden and root.name.startswith("."):
            skipped.append({"path": str(root), "reason": "hidden-root"})

        for current, dirnames, filenames in os.walk(root, followlinks=args.follow_symlinks):
            if truncated:
                break
            current_path = Path(current)
            kept_dirs = []
            for dirname in sorted(dirnames):
                candidate = current_path / dirname
                relative = candidate.relative_to(root).as_posix()
                if not args.include_hidden and dirname.startswith("."):
                    skipped.append({"path": relative, "reason": "hidden-dir"})
                    continue
                if candidate.is_symlink() and not args.follow_symlinks:
                    skipped.append({"path": relative, "reason": "symlink-dir"})
                    continue
                if is_excluded(relative, dirname, patterns):
                    skipped.append({"path": relative, "reason": "excluded-dir"})
                    continue
                kept_dirs.append(dirname)
            dirnames[:] = kept_dirs

            for filename in sorted(filenames):
                if truncated:
                    break
                candidate = current_path / filename
                try:
                    stat = candidate.stat()
                except OSError:
                    inaccessible.append(str(candidate))
                    continue
                relative = candidate.relative_to(root).as_posix()
                if not args.include_hidden and filename.startswith("."):
                    skipped.append({"path": relative, "reason": "hidden-file"})
                    continue
                if candidate.is_symlink() and not args.follow_symlinks:
                    skipped.append({"path": relative, "reason": "symlink-file"})
                    continue
                if is_excluded(relative, filename, patterns):
                    skipped.append({"path": relative, "reason": "excluded-file"})
                    continue
                suffix = candidate.suffix.lower()
                if extensions and suffix not in extensions:
                    continue

                path_str = str(candidate)
                if path_str in seen:
                    continue
                seen.add(path_str)
                if len(records) >= args.max_files:
                    truncated = True
                    break
                records.append(
                    {
                        "id": file_id(path_str),
                        "path": path_str,
                        "root": str(root),
                        "relative_path": relative,
                        "ext": suffix,
                        "size_bytes": stat.st_size,
                        "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                        "access": "local_file",
                    }
                )
                by_extension[suffix or "(none)"] = by_extension.get(suffix or "(none)", 0) + 1
                year = year_of(stat.st_mtime)
                by_year[year] = by_year.get(year, 0) + 1
                root_record["file_count"] = int(root_record["file_count"]) + 1
                root_record["total_bytes"] = int(root_record["total_bytes"]) + stat.st_size

        roots_report.append(root_record)
        if truncated:
            break

    records.sort(key=lambda item: str(item["path"]))
    manifest_path = out_dir / "sources.jsonl"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    total_bytes = sum(int(record["size_bytes"]) for record in records)
    coverage = {
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "roots": roots_report,
        "file_count": len(records),
        "total_bytes": total_bytes,
        "by_extension": dict(sorted(by_extension.items())),
        "by_year": dict(sorted(by_year.items())),
        "truncated": truncated,
        "skipped": skipped[:500],
        "skipped_count": len(skipped),
        "inaccessible_count": len(inaccessible),
        "inaccessible": inaccessible[:100],
        "limits": [
            "Read-only inventory: file paths and metadata only, contents were not read.",
            "File counts are not knowledge counts; the manifest is not evidence.",
            "Skipped and inaccessible entries are reported, not guessed.",
            "File modification time is not the time of any underlying work.",
        ],
    }
    write_json(out_dir / "coverage.json", coverage)

    print(
        json.dumps(
            {
                "roots": [str(Path(root).expanduser().resolve()) for root in args.root],
                "files_indexed": len(records),
                "total_bytes": total_bytes,
                "truncated": truncated,
                "skipped": len(skipped),
                "inaccessible": len(inaccessible),
                "manifest": str(manifest_path),
                "coverage": str(out_dir / "coverage.json"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
