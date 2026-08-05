from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class FeatureListTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = Path(__file__).resolve().parents[2]
        self.cli = self.source / "scripts" / "escapement.py"
        self.temp = tempfile.TemporaryDirectory(prefix="escapement-feature-")
        self.target = Path(self.temp.name) / "product"
        install = subprocess.run(
            [sys.executable, str(self.cli), "init", str(self.target)],
            cwd=self.source,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)
        self.feature_cli = self.target / "scripts" / "feature_list.py"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_only_verify_moves_feature_to_passing(self) -> None:
        feature_file = self.target / "feature_list.json"
        feature_file.write_text(
            json.dumps({
                "schema_version": "1.0",
                "project": "Test",
                "features": [{
                    "id": "F-001",
                    "behavior": "A deterministic smoke feature passes.",
                    "verification": f"{sys.executable} -c \"print('ok')\"",
                    "state": "not_started",
                    "dependencies": [],
                    "evidence": []
                }]
            }, indent=2) + "\n",
            encoding="utf-8",
        )

        activate = subprocess.run(
            [sys.executable, str(self.feature_cli), "activate", "F-001"],
            cwd=self.target,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(activate.returncode, 0, activate.stderr)

        verify = subprocess.run(
            [sys.executable, str(self.feature_cli), "verify", "F-001"],
            cwd=self.target,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(verify.returncode, 0, verify.stderr)

        feature = json.loads(feature_file.read_text(encoding="utf-8"))["features"][0]
        self.assertEqual(feature["state"], "passing")
        self.assertTrue(feature["evidence"])


if __name__ == "__main__":
    unittest.main()
