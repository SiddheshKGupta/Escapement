from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class LicenseStatusTaxonomyTest(unittest.TestCase):
    """capability-registry.json's license_status field sprawled to 18
    distinct values across 67 resources, several spelling the same
    evidence state differently (verified, verified-from-readme, verified-
    in-prior-review and others all meant "someone actually read a real
    source and confirmed the licence"). Consolidated to 7 values
    describing evidence state only; doctor now rejects any value outside
    that closed set so it can't silently sprawl back."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-license-status-")
        self.copy = Path(self.temp.name) / "repo"
        shutil.copytree(
            self.source, self.copy,
            ignore=shutil.ignore_patterns(".git", ".agent", "__pycache__", "*.pyc", "backups"),
        )
        self.escapement = self.copy / "scripts" / "escapement.py"
        self.registry_path = self.copy / "catalog" / "capability-registry.json"

    def tearDown(self):
        self.temp.cleanup()

    def run_doctor(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.escapement), "doctor", "--root", str(self.copy)],
            cwd=self.copy, text=True, capture_output=True, check=False,
        )

    def test_unmodified_copy_reports_all_recognised(self) -> None:
        result = self.run_doctor()
        self.assertIn("[PASS] license_status values are all recognised", result.stdout)

    def test_unrecognised_value_is_detected(self) -> None:
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        resource = registry["resources"][0]
        resource["license_status"] = "verified-from-readme"
        self.registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        result = self.run_doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("license_status values outside the recognised set", result.stdout)
        self.assertIn(f"{resource['id']}: license_status 'verified-from-readme'", result.stdout)

    def test_all_seven_consolidated_values_are_individually_accepted(self) -> None:
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        values = [
            "verified", "must-verify", "verified-unlicensed", "not-open-source",
            "not-code-resource", "source-required", "special-terms",
        ]
        for resource, value in zip(registry["resources"], values):
            resource["license_status"] = value
        self.registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        result = self.run_doctor()
        self.assertIn("[PASS] license_status values are all recognised", result.stdout)


if __name__ == "__main__":
    unittest.main()
