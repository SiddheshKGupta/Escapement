from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class PhaseReplanningTest(unittest.TestCase):
    """phase_plan() decides which phases apply using keyword patterns matched
    against the prompt, computed once at turn start -- it has no way to see what
    DISCOVER's own repository inspection actually turns up. Nothing could revise
    it, and no skill was assigned to reason about phase fit at all: ORIENT, whose
    job description is exactly this, has zero native skills in
    catalog/phase-capabilities.json and is never actually the active phase of any
    real turn (initial_phase() never returns it). lifecycle-planning fills that
    gap at DISCOVER, the real first active phase, backed by replan-phases."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-replan-")
        self.target = Path(self.temp.name) / "project"
        install = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "init", str(self.target)],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)
        self.runtime = self.target / "scripts/agent_runtime.py"

    def tearDown(self):
        self.temp.cleanup()

    def run_runtime(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.runtime), *args],
            cwd=self.target, text=True, capture_output=True, check=False,
        )

    def route(self) -> dict:
        status = self.run_runtime("status")
        self.assertEqual(status.returncode, 0, status.stderr)
        return json.loads(status.stdout)["turn"]["route"]

    def open_material_turn(self, prompt: str) -> None:
        start = self.run_runtime("manual-start", "--prompt", prompt, "--json")
        self.assertEqual(start.returncode, 0, start.stderr)
        self.assertEqual(json.loads(start.stdout)["tier"], "MATERIAL")

    def test_lifecycle_planning_is_routed_at_discover_by_default(self) -> None:
        self.open_material_turn("Add a user login endpoint that stores credentials in the database.")
        skills = {item["id"] for item in self.route()["native_skills"]}
        self.assertIn("lifecycle-planning", skills)

    def test_add_phase_not_in_default_plan(self) -> None:
        self.open_material_turn("Add a user login endpoint that stores credentials in the database.")
        before = [item["id"] for item in self.route()["phase_plan"]]
        self.assertNotIn("POLISH", before)

        result = self.run_runtime(
            "replan-phases", "--add-phase", "POLISH",
            "--reason", "User-facing form needs a polish pass.",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("POLISH", [item["id"] for item in self.route()["phase_plan"]])

    def test_added_phase_survives_advance_phase_recompute(self) -> None:
        """The regression this whole mechanism exists to prevent: route_prompt()
        rebuilds phase_plan from scratch on every advance-phase call, so a naive
        mutation would silently vanish on the very next transition."""
        self.open_material_turn("Add a user login endpoint that stores credentials in the database.")
        self.run_runtime("replan-phases", "--add-phase", "POLISH", "--reason", "Needs polish.")

        skills = ",".join(item["id"] for item in self.route()["native_skills"])
        advance = self.run_runtime(
            "advance-phase", "--phase", "RESEARCH",
            "--summary", "Discovery complete", "--skills-used", skills,
            "--no-check-reason", "Discovery phase",
        )
        self.assertEqual(advance.returncode, 0, advance.stderr)
        self.assertIn("POLISH", [item["id"] for item in self.route()["phase_plan"]])

    def test_cannot_remove_current_phase(self) -> None:
        self.open_material_turn("Add a user login endpoint that stores credentials in the database.")
        current = self.route()["current_phase"]
        result = self.run_runtime("replan-phases", "--remove-phase", current, "--reason", "test")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot remove the current phase", result.stderr)

    def test_cannot_remove_a_completed_phase(self) -> None:
        self.open_material_turn("Add a user login endpoint that stores credentials in the database.")
        skills = ",".join(item["id"] for item in self.route()["native_skills"])
        self.run_runtime(
            "advance-phase", "--phase", "RESEARCH",
            "--summary", "Discovery complete", "--skills-used", skills,
            "--no-check-reason", "Discovery phase",
        )
        result = self.run_runtime("replan-phases", "--remove-phase", "DISCOVER", "--reason", "test")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already completed with recorded evidence", result.stderr)

    def test_cannot_add_a_phase_already_present(self) -> None:
        self.open_material_turn("Add a user login endpoint that stores credentials in the database.")
        already_present = self.route()["phase_plan"][0]["id"]
        result = self.run_runtime("replan-phases", "--add-phase", already_present, "--reason", "test")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already in the phase plan", result.stderr)

    def test_revision_is_recorded_with_its_reason(self) -> None:
        self.open_material_turn("Add a user login endpoint that stores credentials in the database.")
        self.run_runtime(
            "replan-phases", "--add-phase", "POLISH",
            "--reason", "User-facing form needs a polish pass.",
        )
        status = json.loads(self.run_runtime("status").stdout)["turn"]
        overrides = status["phase_plan_overrides"]
        self.assertEqual(len(overrides), 1)
        self.assertEqual(overrides[0]["action"], "add")
        self.assertEqual(overrides[0]["phase"], "POLISH")
        self.assertIn("polish pass", overrides[0]["reason"])


if __name__ == "__main__":
    unittest.main()
