from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RuntimeEvidenceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = Path(__file__).resolve().parents[2]
        self.cli = self.source / "scripts" / "escapement.py"
        self.temp = tempfile.TemporaryDirectory(prefix="escapement-runtime-")
        self.target = Path(self.temp.name) / "product"
        install = subprocess.run(
            [sys.executable, str(self.cli), "init", str(self.target)],
            cwd=self.source,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)
        self.runtime = self.target / "scripts" / "agent_runtime.py"
        self.checker = self.target / "scripts" / "run_check.py"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_runtime(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.runtime), *args],
            cwd=self.target,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_later_prompt_continues_open_turn(self) -> None:
        first = self.run_runtime(
            "manual-start",
            "--prompt",
            "Redesign the management dashboard and define KPI drill-down",
            "--json",
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        first_payload = json.loads(first.stdout)

        second = self.run_runtime(
            "manual-start",
            "--prompt",
            "Also make the screen accessible",
            "--json",
        )
        self.assertEqual(second.returncode, 0, second.stderr)
        second_payload = json.loads(second.stdout)

        self.assertEqual(first_payload["turn_id"], second_payload["turn_id"])
        self.assertTrue(second_payload["continued"])

        turn = json.loads(
            (self.target / ".agent/runtime/current-turn.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(len(turn["prompt_history"]), 2)

    def test_pass_requires_structured_check_and_skill_coverage(self) -> None:
        start = self.run_runtime(
            "manual-start",
            "--prompt",
            "Redesign the management dashboard and define KPI drill-down",
            "--json",
        )
        payload = json.loads(start.stdout)
        skills = ",".join(payload["skills"])

        check = subprocess.run(
            [
                sys.executable,
                str(self.checker),
                "--name",
                "runtime-smoke",
                "--",
                sys.executable,
                "-c",
                "print('ok')",
            ],
            cwd=self.target,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(check.returncode, 0, check.stderr)
        record = check.stdout.strip().splitlines()[-1]

        output = self.target / "evidence.txt"
        output.write_text("verified\n", encoding="utf-8")

        close = self.run_runtime(
            "close-turn",
            "--summary",
            "Runtime test complete",
            "--next",
            "None",
            "--skills-used",
            skills,
            "--files",
            "evidence.txt",
            "--check-records",
            record,
            "--evidence",
            "evidence.txt",
        )
        self.assertEqual(close.returncode, 0, close.stderr)
        self.assertIn("PASS", close.stdout)

    def test_critical_failure_cannot_pass(self) -> None:
        start = self.run_runtime(
            "manual-start",
            "--prompt",
            "Review security permissions",
            "--json",
        )
        payload = json.loads(start.stdout)
        skills = ",".join(payload["skills"])

        check = subprocess.run(
            [
                sys.executable,
                str(self.checker),
                "--name",
                "security-smoke",
                "--",
                sys.executable,
                "-c",
                "print('ok')",
            ],
            cwd=self.target,
            text=True,
            capture_output=True,
            check=False,
        )
        record = check.stdout.strip().splitlines()[-1]
        output = self.target / "security.txt"
        output.write_text("critical issue\n", encoding="utf-8")

        close = self.run_runtime(
            "close-turn",
            "--summary",
            "Critical issue found",
            "--next",
            "Fix it",
            "--skills-used",
            skills,
            "--files",
            "security.txt",
            "--check-records",
            record,
            "--evidence",
            "security.txt",
            "--critical-failure",
        )
        self.assertNotEqual(close.returncode, 0)
        self.assertIn("critical_failure cannot be PASS", close.stderr)


if __name__ == "__main__":
    unittest.main()
