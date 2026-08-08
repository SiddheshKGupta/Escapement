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

    def test_long_prompt_is_not_duplicated_beyond_context_budget(self):
        prompt = (
            "Build an API integration with deterministic verification. "
            + "Preserve this detailed constraint. " * 200
        )
        start = self.run_runtime("manual-start", "--prompt", prompt, "--json")
        self.assertEqual(start.returncode, 0, start.stderr)
        payload = json.loads(start.stdout)
        pack = (
            self.target / ".agent/runtime/CONTEXT_PACK.md"
        ).read_text(encoding="utf-8")
        pack_words = len(pack.split())
        self.assertLessEqual(pack_words, payload["context_cost"]["budget"])
        self.assertEqual(
            payload["context_cost"]["generated_pack_words"],
            pack_words,
        )

    def test_fresh_turn_hydrates_durable_handoff_and_program_state(self):
        (self.target / "SESSION_HANDOFF.md").write_text(
            "# Session Handoff\n\n- Program: Claims Management Platform\n"
            "- Current module: Intake\n- Next action: validate intake schema\n",
            encoding="utf-8",
        )
        modules = self.target / "docs/PROGRAM_MODULES.json"
        modules.parent.mkdir(parents=True, exist_ok=True)
        modules.write_text(
            json.dumps({
                "program": "Claims Management Platform",
                "modules": [{"id": "intake", "status": "IMPLEMENT"}],
            }),
            encoding="utf-8",
        )

        start = self.run_runtime(
            "manual-start",
            "--prompt",
            "Continue the project from the repository's authoritative state.",
            "--json",
        )
        self.assertEqual(start.returncode, 0, start.stderr)
        pack = (
            self.target / ".agent/runtime/CONTEXT_PACK.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Claims Management Platform", pack)
        self.assertIn("Intake", pack)
        self.assertIn("validate intake schema", pack)

    def test_exhausted_five_hour_window_warns_but_allows_new_material_turn(self):
        resource_path = self.target / ".agent/runtime/codex-resources.json"
        resource_path.parent.mkdir(parents=True, exist_ok=True)
        resource_path.write_text(
            json.dumps({
                "schema_version": "1.0",
                "source": "FIXTURE",
                "observed_at": "2023-11-14T22:13:20+00:00",
                "windows": [{
                    "limit_id": "codex",
                    "bucket": "primary",
                    "used_percent": 100,
                    "window_duration_mins": 300,
                    "resets_at": 4_102_444_800,
                }],
                "five_hour_windows": [{
                    "limit_id": "codex",
                    "bucket": "primary",
                    "used_percent": 100,
                    "window_duration_mins": 300,
                    "resets_at": 4_102_444_800,
                }],
                "rate_limits": {},
                "usage": {},
            }),
            encoding="utf-8",
        )
        start = self.run_runtime(
            "manual-start",
            "--prompt",
            "Add authentication to this application.",
            "--json",
        )
        self.assertEqual(start.returncode, 0, start.stderr)
        payload = json.loads(start.stdout)
        self.assertEqual(payload["resource_policy"]["mode"], "EXHAUSTED")
        self.assertEqual(payload["resource_policy"]["action"], "warn-user-100-percent")
        self.assertFalse(payload["resource_policy"]["block_new_turn"])
        self.assertTrue((self.target / ".agent/runtime/current-turn.json").exists())

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
