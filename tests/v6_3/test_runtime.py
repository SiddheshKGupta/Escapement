from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="escapement-v63-")
        self.target = Path(self.temp.name) / "project"
        install = subprocess.run(
            [
                sys.executable,
                str(self.source / "scripts/escapement.py"),
                "init",
                str(self.target),
            ],
            cwd=self.source,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)
        self.runtime = self.target / "scripts/agent_runtime.py"

    def tearDown(self):
        self.temp.cleanup()

    def run_runtime(self, *args):
        return subprocess.run(
            [sys.executable, str(self.runtime), *args],
            cwd=self.target,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_program_can_advance_and_reload_phase_strengths(self):
        start = self.run_runtime(
            "manual-start",
            "--prompt",
            "Build a new AI agent platform using current industry standards.",
            "--json",
        )
        self.assertEqual(start.returncode, 0, start.stderr)
        payload = json.loads(start.stdout)
        self.assertEqual(payload["current_phase"], "DISCOVER")
        self.assertTrue(payload["material_questions"])

        advance = self.run_runtime(
            "advance-phase",
            "--phase",
            "RESEARCH",
            "--summary",
            "Discovery defaults accepted",
            "--skills-used",
            ",".join(payload["native_skills"]),
            "--no-check-reason",
            "Discovery phase",
        )
        self.assertEqual(advance.returncode, 0, advance.stderr)

        status = self.run_runtime("status")
        route = json.loads(status.stdout)["turn"]["route"]
        self.assertEqual(route["current_phase"], "RESEARCH")
        self.assertIn(
            "domain-research",
            {item["id"] for item in route["native_skills"]},
        )
        self.assertIn("capability_readiness", route)

    def test_context_pack_is_phase_bounded(self):
        start = self.run_runtime(
            "manual-start",
            "--prompt",
            "Design a management dashboard with charts and responsive behaviour.",
            "--json",
        )
        self.assertEqual(start.returncode, 0, start.stderr)
        pack = (
            self.target / ".agent/runtime/CONTEXT_PACK.md"
        ).read_text(encoding="utf-8")
        self.assertLessEqual(len(pack.split()), 1800)
        self.assertIn("## Skill and Readiness Audit", pack)
        self.assertIn("design-intelligence:constitution", pack)

    def test_info_creates_no_open_turn(self):
        result = self.run_runtime(
            "manual-start",
            "--prompt",
            "What is the current project name?",
            "--json",
        )
        payload = json.loads(result.stdout)
        self.assertIsNone(payload["turn_id"])
        self.assertEqual(payload["tier"], "INFO")
        self.assertFalse(
            (self.target / ".agent/runtime/current-turn.json").exists()
        )


if __name__ == "__main__":
    unittest.main()
