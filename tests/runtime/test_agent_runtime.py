from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RUNTIME_SCRIPT = REPO / "scripts" / "agent_runtime.py"
CHECK_SCRIPT = REPO / "scripts" / "run_check.py"

PROMPT = "Redesign the management dashboard and define KPI drill-down"
EXPECTED_SKILLS = ["dashboard", "design-system", "enterprise-ui-review", "skill-governance"]


class RuntimeSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        """Run against a throwaway root.

        agent_runtime and run_check both resolve their root from AGENTS.md plus cwd,
        so pointing them at the repository directly would write SESSION_HANDOFF.md,
        logs, and .agent/evidence into tracked files on every test run.
        """
        self.root = Path(tempfile.mkdtemp(prefix="escapement-test-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        for name in ("AGENTS.md", "PROJECT_STATE.yaml"):
            shutil.copy2(REPO / name, self.root / name)

        self.env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)}

    def run_runtime(self, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(RUNTIME_SCRIPT), *args],
            cwd=self.root, env=self.env, input=stdin,
            text=True, capture_output=True, check=False,
        )

    def run_check(self, name: str, *command: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CHECK_SCRIPT), "--name", name, "--", *command],
            cwd=self.root, env=self.env,
            text=True, capture_output=True, check=False,
        )

    def test_router_stop_and_close(self) -> None:
        start = self.run_runtime("manual-start", "--prompt", PROMPT)
        self.assertEqual(start.returncode, 0, start.stderr)

        turn = json.loads((self.root / ".agent" / "runtime" / "current-turn.json").read_text(encoding="utf-8"))
        self.assertEqual(turn["mode"], "DELTA")
        self.assertEqual(turn["skills"], EXPECTED_SKILLS)

        stop = self.run_runtime("stop", stdin=json.dumps({"stop_hook_active": False}))
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(json.loads(stop.stdout)["decision"], "block")

        # close-turn --result PASS (the default) requires a real structured check
        # record and every routed skill declared used. Passing free text, as the
        # v5 CLI allowed, no longer satisfies the contract.
        check = self.run_check("runtime-smoke-check", sys.executable, "-c", "print('ok')")
        self.assertEqual(check.returncode, 0, check.stderr)
        record_path = check.stdout.strip()
        self.assertTrue((self.root / record_path).exists(), record_path)

        close = self.run_runtime(
            "close-turn",
            "--summary", "Runtime smoke test completed",
            "--next", "None",
            "--files", ".agent/runtime/ACTIVE_CONTEXT.md",
            "--skills-used", ",".join(EXPECTED_SKILLS),
            "--check-records", record_path,
            "--evidence", ".agent/runtime/ACTIVE_CONTEXT.md",
        )
        self.assertEqual(close.returncode, 0, close.stderr)

        after = self.run_runtime("stop", stdin=json.dumps({"stop_hook_active": False}))
        self.assertEqual(after.stdout.strip(), "")

    def test_repository_is_not_modified(self) -> None:
        """The suite must never write into the repository it is testing."""
        handoff = (REPO / "SESSION_HANDOFF.md").read_bytes()
        log_path = REPO / "logs" / "skill-usage.jsonl"
        log = log_path.read_bytes() if log_path.exists() else b""

        self.run_runtime("manual-start", "--prompt", "Build a dashboard")
        check = self.run_check("isolation-check", sys.executable, "-c", "print('ok')")
        self.run_runtime(
            "close-turn",
            "--summary", "isolation check", "--next", "None",
            "--skills-used", "dashboard,skill-governance",
            "--check-records", check.stdout.strip(),
        )

        self.assertEqual((REPO / "SESSION_HANDOFF.md").read_bytes(), handoff)
        self.assertEqual(log_path.read_bytes() if log_path.exists() else b"", log)


if __name__ == "__main__":
    unittest.main()
