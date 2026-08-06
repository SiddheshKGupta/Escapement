from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReportingStandardRoutingTest(unittest.TestCase):
    """Found via real-world use: a dashboard was built with raw unformatted
    numbers -- no currency symbol, no locale-correct digit grouping, no
    Lakh/Crore convention for an India/INR domain -- because nothing in the
    catalog covered KPI/reporting correctness as a distinct concern from
    design-system's visual guidance. design-system governs what a KPI card
    looks like; nothing governed whether its number was formatted for the
    confirmed business locale, or whether it had the breakdown a real KPI
    needs. reporting-standard fills that gap."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-reporting-")
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

    def specify_skills_for(self, prompt: str) -> set[str]:
        start = self.run_runtime("manual-start", "--prompt", prompt, "--json")
        self.assertEqual(start.returncode, 0, start.stderr)

        skills = [item["id"] for item in self.route()["native_skills"]]
        advance = self.run_runtime(
            "advance-phase", "--phase", "SPECIFY",
            "--summary", "Discovery complete", "--skills-used", ",".join(skills),
            "--no-check-reason", "Discovery phase",
        )
        self.assertEqual(advance.returncode, 0, advance.stderr)
        return {item["id"] for item in self.route()["native_skills"]}

    def test_reporting_standard_is_routed_for_a_dashboard_kpi_prompt(self) -> None:
        specify_skills = self.specify_skills_for(
            "Build a management dashboard with KPI tiles showing reconciliation totals."
        )
        self.assertIn("reporting-standard", specify_skills)

    def test_reporting_standard_is_routed_for_a_currency_formatting_prompt(self) -> None:
        specify_skills = self.specify_skills_for(
            "Build a new finance dashboard where rupee amounts use proper lakh and crore formatting."
        )
        self.assertIn("reporting-standard", specify_skills)

    def test_reporting_standard_does_not_over_trigger_on_unrelated_prompt(self) -> None:
        specify_skills = self.specify_skills_for(
            "Build a new user profile settings page with theme preferences."
        )
        self.assertNotIn("reporting-standard", specify_skills)


if __name__ == "__main__":
    unittest.main()
