from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from capability_audit import audit  # noqa: E402
from capability_router import route_prompt  # noqa: E402


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

    def test_phase_plan_matches_direct_prompt_routing(self):
        prompt = (
            "Build an API capability that imports transaction records from CSV, "
            "validates records, persists them safely, identifies unmatched "
            "transactions, and produces a reconciliation summary."
        )
        value = audit(prompt)
        for phase in value["phase_plan"]:
            direct = route_prompt(prompt, phase_override=phase["phase"])
            self.assertEqual(
                phase["native_skills"],
                [item["id"] for item in direct["native_skills"]],
                phase["phase"],
            )
            self.assertEqual(
                [item["id"] for item in phase["capability_strengths"]],
                [item["id"] for item in direct["capability_strengths"]],
                phase["phase"],
            )


if __name__ == "__main__":
    unittest.main()
