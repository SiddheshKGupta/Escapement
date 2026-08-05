from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class ReadinessAuditTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]

    def test_audit_maps_active_missing_and_overlap(self):
        process = subprocess.run(
            [
                sys.executable,
                str(self.root / "scripts/capability_audit.py"),
                "Design a premium dashboard with responsive charts and animation.",
            ],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        audit = json.loads(process.stdout)
        self.assertIn(
            "design-intelligence:constitution",
            audit["active_capability_strengths"],
        )
        self.assertEqual(
            audit["design_authority"],
            "docs/standards/design-intelligence.md",
        )
        self.assertTrue(audit["phase_plan"])
        self.assertTrue(audit["overlap_decisions"])

    def test_markdown_audit_is_human_readable(self):
        process = subprocess.run(
            [
                sys.executable,
                str(self.root / "scripts/escapement.py"),
                "capability-audit",
                "Build a new AI agent platform.",
                "--markdown",
            ],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("# Skill and Capability Readiness Audit", process.stdout)
        self.assertIn("## Phase Plan", process.stdout)
        self.assertIn("## External Install or Load Candidates", process.stdout)


if __name__ == "__main__":
    unittest.main()
