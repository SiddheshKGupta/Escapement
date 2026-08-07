from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class GeminiBootstrapTest(unittest.TestCase):
    """Gemini CLI's default context filename is GEMINI.md, not AGENTS.md --
    a fresh Gemini CLI session reads nothing here at all unless a user has
    manually reconfigured context.fileName in their own settings.json.
    Verified 2026-08-07 against Gemini CLI's own docs (google-gemini/gemini-cli).
    Antigravity needs no equivalent file: it reads AGENTS.md at the repo
    root natively (see docs/decisions/EXTERNAL_CANDIDATES_2026_08.md)."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-gemini-")
        self.target = Path(self.temp.name) / "project"
        install = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "init", str(self.target)],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)

    def tearDown(self):
        self.temp.cleanup()

    def test_init_creates_gemini_pointer(self):
        path = self.target / "GEMINI.md"
        self.assertTrue(path.exists())
        content = path.read_text(encoding="utf-8")
        self.assertIn("AGENTS.md", content)
        self.assertIn("Host Bootstrap", content)

    def test_doctor_checks_for_gemini_md(self):
        result = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "doctor", "--root", str(self.target)],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertIn("[PASS] GEMINI.md", result.stdout)

    def test_agents_md_bootstrap_names_gemini_and_antigravity(self):
        content = (self.target / "AGENTS.md").read_text(encoding="utf-8")
        bootstrap_section = content.split("## Host Bootstrap")[1].split("##")[0]
        self.assertIn("Gemini CLI", bootstrap_section)
        self.assertIn("Antigravity", bootstrap_section)


if __name__ == "__main__":
    unittest.main()
