import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-X", "utf8", str(SCRIPTS / name), *args]
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"no YAML frontmatter in {path}")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        if key and value:
            fields[key.strip()] = value.strip()
    return fields


class SkillPackageTest(unittest.TestCase):
    def test_frontmatter(self) -> None:
        fields = read_frontmatter(ROOT / "SKILL.md")
        self.assertIn("name", fields)
        self.assertRegex(fields["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertTrue(fields.get("description", "").strip())

    def test_skill_body_is_compact(self) -> None:
        body = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(body), 8000, "SKILL.md should stay small; move detail into references/")

    def test_reference_files_exist(self) -> None:
        for name in ("schema.md", "interview.md", "evidence.md", "platforms.md"):
            self.assertTrue((ROOT / "references" / name).is_file(), name)

    def test_demo_kb_passes_check(self) -> None:
        result = run_script("check.py", "--kb", str(ROOT / "examples" / "demo-kb"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class InitTest(unittest.TestCase):
    def test_init_and_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "kb"
            result = run_script(
                "init_kb.py",
                "--target",
                str(target),
                "--name",
                "Unit Test KB",
                "--variant",
                "research",
                "--lang",
                "zh",
                "--data-roots",
                "D:/demo",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "AI_CONTEXT.md").is_file())
            self.assertTrue((target / "profile" / "profile.md").is_file())
            for document in target.rglob("*.md"):
                text = document.read_text(encoding="utf-8")
                self.assertNotIn("{{", text, f"unreplaced placeholder in {document}")
            self.assertIn("Unit Test KB", (target / "README.md").read_text(encoding="utf-8"))

    def test_init_refuses_non_empty_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            (target / "existing.txt").write_text("x", encoding="utf-8")
            result = run_script("init_kb.py", "--target", str(target))
            self.assertEqual(result.returncode, 2)


class ScanTest(unittest.TestCase):
    def test_scan_writes_manifest_and_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            data = Path(temp) / "data"
            (data / "notes").mkdir(parents=True)
            (data / "notes" / "a.md").write_text("alpha", encoding="utf-8")
            (data / "b.txt").write_text("beta", encoding="utf-8")
            (data / ".hidden").write_text("x", encoding="utf-8")
            out = Path(temp) / "catalog"
            result = run_script("scan.py", "--root", str(data), "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            lines = (out / "sources.jsonl").read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertTrue(all('"access": "local_file"' in line for line in lines))
            coverage = (out / "coverage.json").read_text(encoding="utf-8")
            self.assertIn('"file_count": 2', coverage)


class CheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.kb = Path(self.temp.name) / "demo-kb"
        shutil.copytree(ROOT / "examples" / "demo-kb", self.kb)
        shutil.copytree(ROOT / "examples" / "demo-data", Path(self.temp.name) / "demo-data")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_demo_with_sources(self) -> None:
        result = run_script("check.py", "--kb", str(self.kb), "--check-sources")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_broken_link_is_reported(self) -> None:
        readme = self.kb / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\n[missing](nope.md)\n", encoding="utf-8")
        result = run_script("check.py", "--kb", str(self.kb))
        self.assertEqual(result.returncode, 1)
        self.assertIn("broken link", result.stdout)

    def test_missing_evidence_field_is_reported(self) -> None:
        evidence = self.kb / "catalog" / "evidence.md"
        evidence.write_text(
            evidence.read_text(encoding="utf-8").replace("- kind: document-reported\n", ""),
            encoding="utf-8",
        )
        result = run_script("check.py", "--kb", str(self.kb))
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing fields", result.stdout)

    def test_unknown_evidence_kind_is_reported(self) -> None:
        evidence = self.kb / "catalog" / "evidence.md"
        evidence.write_text(
            evidence.read_text(encoding="utf-8").replace("kind: document-reported", "kind: guess"),
            encoding="utf-8",
        )
        result = run_script("check.py", "--kb", str(self.kb))
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown kind", result.stdout)

    def test_missing_source_is_reported(self) -> None:
        evidence = self.kb / "catalog" / "evidence.md"
        evidence.write_text(
            evidence.read_text(encoding="utf-8").replace(
                "../demo-data/notes/course-outline.md", "../demo-data/notes/missing.md"
            ),
            encoding="utf-8",
        )
        result = run_script("check.py", "--kb", str(self.kb), "--check-sources")
        self.assertEqual(result.returncode, 1)
        self.assertIn("source does not exist", result.stdout)


if __name__ == "__main__":
    unittest.main()
