from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class UiImpliesDesignSystemTest(unittest.TestCase):
    """Found via real-world use: design-system's own triggers are all
    explicit design vocabulary ("design system", "brand", "colour",
    "typography"). enterprise-ui-review and frontend-implementation trigger
    on generic UI-building vocabulary ("frontend", "React", "page",
    "component") with no design-specific word required. A prompt like "Build
    a React frontend: upload form, results table" matched the latter two and
    never matched design-system at all -- so a real UI got implemented with
    no design decision ever surfacing, even though design-system and
    enterprise-ui-review declare each other in "paired_with" in
    catalog/native-skills.json. That field was never enforced anywhere in
    the router; this is the fix."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-ui-design-")
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

    def advance_to_specify(self, prompt: str) -> set[str]:
        start = self.run_runtime("manual-start", "--prompt", prompt, "--json")
        self.assertEqual(start.returncode, 0, start.stderr)

        skills = [item["id"] for item in self.route()["native_skills"]]
        while self.route()["current_phase"] != "SPECIFY":
            current = self.route()["current_phase"]
            advance = self.run_runtime(
                "advance-phase", "--phase", self._next_phase(current),
                "--summary", "test", "--skills-used", ",".join(skills),
                "--no-check-reason", "test",
            )
            self.assertEqual(advance.returncode, 0, advance.stderr)
            skills = [item["id"] for item in self.route()["native_skills"]]

        return {item["id"] for item in self.route()["native_skills"]}

    @staticmethod
    def _next_phase(current: str) -> str:
        order = ["DISCOVER", "RESEARCH", "BRAINSTORM", "SPECIFY"]
        return order[order.index(current) + 1]

    def test_generic_frontend_prompt_pulls_in_design_system_at_specify(self) -> None:
        """The exact real-world prompt that surfaced this gap: no design-
        specific word in it at all, only generic UI-implementation vocabulary."""
        specify_skills = self.advance_to_specify(
            "Build a React frontend for the invoice reconciliation app: "
            "upload form, rule-result table, bucketed reconciliation results"
        )
        self.assertIn("design-system", specify_skills)

    def test_non_ui_prompt_does_not_force_design_system(self) -> None:
        """The fix must not over-trigger: a prompt with no UI-implementation
        vocabulary at all should not pull in design-system either."""
        specify_skills = self.advance_to_specify(
            "Build a claims management platform: claims CRUD with a status "
            "workflow and role-based access control."
        )
        self.assertNotIn("design-system", specify_skills)


if __name__ == "__main__":
    unittest.main()
