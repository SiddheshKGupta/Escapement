from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DoctorDriftDetectionTest(unittest.TestCase):
    """Found via real-world adversarial testing: a project installed via
    escapement.py init had a since-fixed security_gate.py bug silently persist,
    because doctor's install-record check only ever printed the recorded version
    string as PASS -- it never compared the installed copy's managed-file content
    against the source clone's current content. The install record already stores
    the source path used at install time; doctor just never used it."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-drift-")
        self.target = Path(self.temp.name) / "project"
        install = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "init", str(self.target)],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)
        self.escapement = self.target / "scripts/escapement.py"

    def tearDown(self):
        self.temp.cleanup()

    def run_doctor(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.escapement), "doctor"],
            cwd=self.target, text=True, capture_output=True, check=False,
        )

    def test_fresh_install_reports_no_drift(self) -> None:
        result = self.run_doctor()
        self.assertIn("[PASS] managed files match the source install", result.stdout)

    def test_stale_managed_file_is_detected(self) -> None:
        drifted = self.target / "scripts" / "run_check.py"
        original = drifted.read_text(encoding="utf-8")
        drifted.write_text(original.replace("check:", "old-format-check:"), encoding="utf-8")

        result = self.run_doctor()
        self.assertIn("managed file(s) differ from the source install", result.stdout)
        self.assertIn("scripts/run_check.py", result.stdout)
        self.assertIn("escapement.py update", result.stdout)

    def test_update_apply_resolves_the_warning(self) -> None:
        drifted = self.target / "scripts" / "run_check.py"
        original = drifted.read_text(encoding="utf-8")
        drifted.write_text(original.replace("check:", "old-format-check:"), encoding="utf-8")
        self.assertIn("differ from the source install", self.run_doctor().stdout)

        update = subprocess.run(
            [sys.executable, str(self.escapement), "update", str(self.target),
             "--apply", "--force-managed"],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertEqual(update.returncode, 0, update.stderr)
        self.assertIn("[PASS] managed files match the source install", self.run_doctor().stdout)


if __name__ == "__main__":
    unittest.main()
