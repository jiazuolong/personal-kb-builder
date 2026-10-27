#!/usr/bin/env python3
"""Validate a personal knowledge base built with personal-kb-builder.

Checks: required files, evidence format, unique E-IDs, Markdown links, JSON
catalog files, and optionally that evidence sources still exist.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = (
    "README.md",
    "AI_CONTEXT.md",
    "profile/profile.md",
    "catalog/evidence.md",
    "catalog/sources.jsonl",
    "catalog/coverage.json",
    "maintenance/update.md",
)
OPTIONAL_FILES = ("timeline.md", "open-questions.md", "AGENTS.md")

EVIDENCE_FIELDS = ("source", "locator", "kind", "limitation")
EVIDENCE_OPTIONAL_FIELDS = ("reviewed_at", "reviewed_sha256")
KINDS = {
    "user-confirmed",
    "document-reported",
    "plan",
    "code-structure",
    "second-hand",
    "path-only",
}
SOURCE_MANIFEST_KEYS = ("id", "path", "root", "ext", "size_bytes", "access")
SKIP_SOURCE_MARKERS = ("{{", "<", "TBD", "待确认", "—")

SECTION_RE = re.compile(r"^##\s+(E\d{3})\s*$", re.MULTILINE)
FIELD_RE = re.compile(
    r"^[-*]\s+(source|locator|kind|limitation|reviewed_at|reviewed_sha256)\s*:\s*(.+?)\s*$",
    re.IGNORECASE,
)
E_REF_RE = re.compile(r"\bE\d{3}\b")
LINK_RE = re.compile(r"\]\((.+?)\)")
FENCE_RE = re.compile(r"^[ \t]{0,3}```.*?^[ \t]{0,3}```[^\n]*$", re.MULTILINE | re.DOTALL)


def strip_code_fences(text: str) -> str:
    """Ignore links and E-IDs inside fenced code blocks (they are examples, not references)."""
    return FENCE_RE.sub("", text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a personal knowledge base.")
    parser.add_argument("--kb", default=".", help="KB root (default: current directory).")
    parser.add_argument("--check-sources", action="store_true", help="Verify that evidence sources exist.")
    parser.add_argument("--check-hashes", action="store_true", help="Verify reviewed_sha256 when present.")
    return parser


def parse_evidence(text: str, errors: list[str]) -> dict[str, dict[str, str]]:
    matches = list(SECTION_RE.finditer(text))
    records: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        evidence_id = match.group(1)
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : body_end]
        if evidence_id in records:
            errors.append(f"catalog/evidence.md: duplicate ID {evidence_id}")
            continue
        fields: dict[str, str] = {}
        for line in body.splitlines():
            field_match = FIELD_RE.match(line.strip())
            if field_match:
                fields[field_match.group(1).lower()] = field_match.group(2).strip()
        missing = [name for name in EVIDENCE_FIELDS if not fields.get(name)]
        if missing:
            errors.append(f"catalog/evidence.md: {evidence_id} missing fields: {', '.join(missing)}")
        if fields.get("kind") and fields["kind"] not in KINDS:
            errors.append(
                f"catalog/evidence.md: {evidence_id} has unknown kind '{fields['kind']}' "
                f"(allowed: {', '.join(sorted(KINDS))})"
            )
        records[evidence_id] = fields
    return records


def check_links(kb: Path, errors: list[str]) -> None:
    for document in sorted(kb.rglob("*.md")):
        if ".git" in document.parts:
            continue
        text = strip_code_fences(document.read_text(encoding="utf-8"))
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").strip()
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
                continue
            if "{{" in target or target.startswith(("C:", "c:", "/", "\\\\")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (document.parent / path_part).resolve()
            if not resolved.exists():
                errors.append(f"{document.relative_to(kb).as_posix()}: broken link '{target}'")


def check_manifest(kb: Path, errors: list[str], warnings: list[str]) -> int:
    manifest = kb / "catalog" / "sources.jsonl"
    count = 0
    for line_number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"catalog/sources.jsonl:{line_number}: invalid JSON ({error})")
            continue
        if not isinstance(record, dict):
            errors.append(f"catalog/sources.jsonl:{line_number}: expected an object")
            continue
        missing = [key for key in SOURCE_MANIFEST_KEYS if key not in record]
        if missing:
            errors.append(f"catalog/sources.jsonl:{line_number}: missing keys: {', '.join(missing)}")
        count += 1
    if count == 0:
        warnings.append("catalog/sources.jsonl is empty; run scripts/scan.py")
    return count


def check_coverage(kb: Path, errors: list[str]) -> None:
    path = kb / "catalog" / "coverage.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        errors.append(f"catalog/coverage.json: invalid JSON ({error})")
        return
    if not isinstance(data, dict):
        errors.append("catalog/coverage.json: expected an object")
        return
    for key in ("roots", "file_count", "limits"):
        if key not in data:
            errors.append(f"catalog/coverage.json: missing key '{key}'")
    if not data.get("built_at_utc"):
        errors.append("catalog/coverage.json: built_at_utc is null; run scripts/scan.py")


def clean_source(value: str) -> str:
    return value.strip().strip("`").strip()


def check_sources(
    kb: Path,
    records: dict[str, dict[str, str]],
    errors: list[str],
    check_hashes: bool,
) -> None:
    for evidence_id, fields in records.items():
        source = clean_source(fields.get("source", ""))
        if not source or any(marker in source for marker in SKIP_SOURCE_MARKERS):
            continue
        path = Path(source).expanduser()
        if not path.is_absolute():
            path = (kb / path).resolve()
        if not path.exists():
            errors.append(f"{evidence_id}: source does not exist: {source}")
            continue
        expected = clean_source(fields.get("reviewed_sha256", ""))
        if check_hashes and expected and path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != expected:
                errors.append(f"{evidence_id}: source changed since review: {source}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    kb = Path(args.kb).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not kb.is_dir():
        print(f"error: KB directory not found: {kb}", file=sys.stderr)
        return 2

    for relative in REQUIRED_FILES:
        if not (kb / relative).is_file():
            errors.append(f"missing required file: {relative}")
    for relative in OPTIONAL_FILES:
        if not (kb / relative).is_file():
            warnings.append(f"missing optional file: {relative}")

    evidence_path = kb / "catalog" / "evidence.md"
    records: dict[str, dict[str, str]] = {}
    if evidence_path.is_file():
        records = parse_evidence(evidence_path.read_text(encoding="utf-8"), errors)
        if not records:
            errors.append("catalog/evidence.md: no E### sections found; add 3-5 evidence records")

    referenced: set[str] = set()
    for document in sorted(kb.rglob("*.md")):
        if ".git" in document.parts:
            continue
        referenced.update(E_REF_RE.findall(strip_code_fences(document.read_text(encoding="utf-8"))))
    for evidence_id in sorted(referenced - set(records)):
        errors.append(f"evidence ID referenced but not defined: {evidence_id}")

    check_links(kb, errors)
    manifest_count = check_manifest(kb, errors, warnings)
    if (kb / "catalog" / "coverage.json").is_file():
        check_coverage(kb, errors)

    if args.check_sources or args.check_hashes:
        check_sources(kb, records, errors, args.check_hashes)

    summary = {
        "ok": not errors,
        "kb": str(kb),
        "evidence_records": len(records),
        "manifest_records": manifest_count,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
