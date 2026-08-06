from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DataArchitectureRoutingTest(unittest.TestCase):
    """Found via real-world use: no skill in the catalog covered choosing a
    database technology and designing the schema/API around that choice from
    the start. api-integration covers external contracts; data-engineering
    covers ETL/analytics pipelines over an existing store; software-
    implementation is generic. A project needing its first persistence layer
    had nothing routing it to a considered database choice."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-data-arch-")
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

    def test_data_architecture_is_routed_at_specify_for_a_database_prompt(self) -> None:
        start = self.run_runtime(
            "manual-start", "--prompt",
            "Build a new inventory tracking system with a database to store products and transactions.",
            "--json",
        )
        self.assertEqual(start.returncode, 0, start.stderr)

        skills = [item["id"] for item in self.route()["native_skills"]]
        advance = self.run_runtime(
            "advance-phase", "--phase", "SPECIFY",
            "--summary", "Discovery complete", "--skills-used", ",".join(skills),
            "--no-check-reason", "Discovery phase",
        )
        self.assertEqual(advance.returncode, 0, advance.stderr)

        specify_skills = {item["id"] for item in self.route()["native_skills"]}
        self.assertIn("data-architecture", specify_skills)
        self.assertIn("product-specification", specify_skills)


if __name__ == "__main__":
    unittest.main()
