from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ManifestCountCheckTest(unittest.TestCase):
    """manifest.json is a hand-maintained snapshot that no script previously
    read, so nothing ever verified its declared counts matched the actual
    catalogue/eval/test files. It drifted twice in one real session: a
    routing-evaluation count missed by a shell heredoc encoding mismatch,
    and a files count that fell behind after two documents landed without a
    second manual increment -- confirmed live via `git ls-files` returning
    272 while manifest.json still said 270. doctor now computes each count
    from the actual files and fails if manifest.json or README.md disagree."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-manifest-count-")
        self.copy = Path(self.temp.name) / "repo"
        shutil.copytree(
            self.source, self.copy,
            ignore=shutil.ignore_patterns(".git", ".agent", "__pycache__", "*.pyc", "backups"),
        )
        self.escapement = self.copy / "scripts" / "escapement.py"
        self.manifest_path = self.copy / "manifest.json"

    def tearDown(self):
        self.temp.cleanup()

    def run_doctor(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.escapement), "doctor", "--root", str(self.copy)],
            cwd=self.copy, text=True, capture_output=True, check=False,
        )

    def test_unmodified_copy_reports_no_drift(self) -> None:
        result = self.run_doctor()
        self.assertIn("[PASS] manifest.json counts match actual repository state", result.stdout)

    def test_stale_native_skill_count_is_detected(self) -> None:
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        manifest["counts"]["native_skills"] += 3
        self.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        result = self.run_doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("manifest.json counts drifted", result.stdout)
        self.assertIn("counts.native_skills=", result.stdout)

    def test_stale_routing_evaluation_fraction_is_detected(self) -> None:
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        manifest["validation"]["routing_evaluations"] = "PASS — 1/1"
        self.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        result = self.run_doctor()
        self.assertIn("validation.routing_evaluations claims 1", result.stdout)

    def test_readme_inventory_drift_is_detected_independently_of_manifest(self) -> None:
        # Uses "Native skills:", not "Repository files:" -- the latter is
        # only checked when the fixture has a real .git directory to run
        # `git ls-files` against, and this throwaway copy deliberately
        # excludes .git (same ignore list ablation_harness.py uses).
        readme_path = self.copy / "README.md"
        readme = readme_path.read_text(encoding="utf-8")
        match = re.search(r"Native skills:\s+(\d+)", readme)
        self.assertIsNotNone(match, "README.md's Native skills line moved or changed format")
        wrong_count = int(match.group(1)) + 1
        readme = readme[:match.start(1)] + str(wrong_count) + readme[match.end(1):]
        readme_path.write_text(readme, encoding="utf-8")

        result = self.run_doctor()
        self.assertIn(f"README.md Native skills inventory says {wrong_count}", result.stdout)

    def test_missing_manifest_skips_the_check_without_failing(self) -> None:
        self.manifest_path.unlink()
        result = self.run_doctor()
        self.assertNotIn("manifest.json counts", result.stdout)


if __name__ == "__main__":
    unittest.main()
