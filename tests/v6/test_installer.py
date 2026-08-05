from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class InstallerSafetyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = Path(__file__).resolve().parents[2]
        self.cli = self.source / "scripts" / "escapement.py"
        self.temp = tempfile.TemporaryDirectory(prefix="escapement-installer-")
        self.target = Path(self.temp.name) / "product"
        process = subprocess.run(
            [sys.executable, str(self.cli), "init", str(self.target)],
            cwd=self.source,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_project_owned_state_is_preserved(self) -> None:
        state = self.target / "PROJECT_STATE.yaml"
        context = self.target / "PROJECT_CONTEXT.md"
        state.write_text(
            "project_name: Real Product\nphase: implementation\n"
            "work_mode: DELTA\nimplementation_authorized: true\n",
            encoding="utf-8",
        )
        context.write_text("# Project Context\n\nReal client context.\n", encoding="utf-8")

        process = subprocess.run(
            [sys.executable, str(self.cli), "update", str(self.target), "--apply"],
            cwd=self.source,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("Real Product", state.read_text(encoding="utf-8"))
        self.assertIn("Real client context", context.read_text(encoding="utf-8"))

    def test_modified_managed_file_is_not_overwritten_without_force(self) -> None:
        agents = self.target / "AGENTS.md"
        original = agents.read_text(encoding="utf-8")
        agents.write_text(original + "\nLOCAL PROJECT RULE\n", encoding="utf-8")

        process = subprocess.run(
            [sys.executable, str(self.cli), "update", str(self.target), "--apply"],
            cwd=self.source,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("LOCAL PROJECT RULE", agents.read_text(encoding="utf-8"))

    def test_install_record_tracks_managed_files(self) -> None:
        record = json.loads(
            (self.target / ".escapement-install.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["version"], "6.0.0")
        self.assertIn("AGENTS.md", record["managed_files"])
        self.assertIn("PROJECT_STATE.yaml", record["project_owned_files"])


if __name__ == "__main__":
    unittest.main()
