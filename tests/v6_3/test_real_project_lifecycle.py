from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RealProjectLifecycleTest(unittest.TestCase):
    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-real-project-")
        self.target = Path(self.temp.name) / "product"
        result = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "init", str(self.target)],
            cwd=self.source,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.runtime = self.target / "scripts/agent_runtime.py"

    def tearDown(self):
        self.temp.cleanup()

    def runtime_call(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.runtime), *args],
            cwd=self.target,
            text=True,
            capture_output=True,
            check=False,
        )

    def route(self) -> dict:
        status = self.runtime_call("status")
        self.assertEqual(status.returncode, 0, status.stderr)
        return json.loads(status.stdout)["turn"]["route"]

    def advance(self, phase: str, summary: str, artifact: str) -> None:
        path = self.target / artifact
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {phase}\n\n{summary}\n", encoding="utf-8")
        skills = ",".join(item["id"] for item in self.route()["native_skills"])
        result = self.runtime_call(
            "advance-phase",
            "--phase", phase,
            "--summary", summary,
            "--skills-used", skills,
            "--files", artifact,
            "--evidence", artifact,
            "--no-check-reason", "Lifecycle orchestration regression fixture",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_fresh_project_runs_complete_phase_lifecycle(self):
        self.assertTrue((self.target / "docs/plans").is_dir())
        self.assertFalse((self.target / "tests/v6_3").exists())

        prompt = (
            "Build a domain-aware enterprise claims management platform with "
            "workflows, dashboards, audit history, APIs, RBAC, responsive UI, "
            "purposeful motion and an AI document-triage assistant. Research "
            "current standards and agent blueprints, avoid overengineering, "
            "and use parallel agents only where safe."
        )
        start = self.runtime_call("manual-start", "--prompt", prompt, "--json")
        self.assertEqual(start.returncode, 0, start.stderr)
        payload = json.loads(start.stdout)
        self.assertEqual(payload["tier"], "PROGRAM")
        self.assertEqual(payload["current_phase"], "DISCOVER")
        self.assertEqual(
            payload["phase_plan"],
            [
                "ORIENT", "DISCOVER", "RESEARCH", "BRAINSTORM", "SPECIFY",
                "PLAN", "IMPLEMENT", "VERIFY", "POLISH", "RELEASE",
            ],
        )

        self.advance("RESEARCH", "Discovery completed", "PROJECT_CONTEXT.md")
        self.advance("BRAINSTORM", "Domain evidence recorded", "DOMAIN_CONTEXT.md")
        self.advance("SPECIFY", "Solution selected", "docs/decisions/DECISION_LOG.md")
        self.advance("PLAN", "Specification completed", "docs/specs/product.md")
        self.advance("IMPLEMENT", "Implementation plan completed", "docs/plans/plan.md")
        self.advance("VERIFY", "Bounded implementation completed", "src/module.py")
        self.advance("POLISH", "Verification completed", "reports/verification.md")
        self.advance("RELEASE", "Applicable polish completed", "reports/polish.md")

        release = self.route()
        self.assertEqual(release["current_phase"], "RELEASE")
        release_artifact = self.target / "reports/release.md"
        release_artifact.write_text("# Release\n\nPartial smoke release.\n", encoding="utf-8")
        skills = ",".join(item["id"] for item in release["native_skills"])
        close = self.runtime_call(
            "close-turn",
            "--summary", "Full lifecycle smoke test completed",
            "--next", "Implement remaining modules",
            "--files", "reports/release.md",
            "--skills-used", skills,
            "--evidence", "reports/release.md",
            "--result", "PARTIAL",
        )
        self.assertEqual(close.returncode, 0, close.stderr)

        status = json.loads(self.runtime_call("status").stdout)["turn"]
        self.assertEqual(status["status"], "closed")
        self.assertEqual(status["closure"]["result"], "PARTIAL")
        self.assertEqual(
            [item["phase"] for item in status["phase_history"]],
            ["DISCOVER", "RESEARCH", "BRAINSTORM", "SPECIFY", "PLAN", "IMPLEMENT", "VERIFY", "POLISH"],
        )


if __name__ == "__main__":
    unittest.main()
