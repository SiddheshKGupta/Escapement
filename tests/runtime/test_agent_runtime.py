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
SCRIPT = REPO / "scripts" / "agent_runtime.py"


class RuntimeSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        """Run against a throwaway root.

        agent_runtime writes SESSION_HANDOFF.md and logs/skill-usage.jsonl into whichever
        root it resolves. Pointing it at the repository would dirty tracked files on every
        test run, so give it a temporary one via CLAUDE_PROJECT_DIR.
        """
        self.root = Path(tempfile.mkdtemp(prefix="escapement-test-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        for name in ("AGENTS.md", "PROJECT_STATE.yaml"):
            shutil.copy2(REPO / name, self.root / name)

        self.env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)}

    def run_runtime(self, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=self.root, env=self.env, input=stdin,
            text=True, capture_output=True, check=False,
        )

    def test_router_stop_and_close(self) -> None:
        start = self.run_runtime(
            "manual-start",
            "--prompt", "Redesign the management dashboard and define KPI drill-down",
        )
        self.assertEqual(start.returncode, 0, start.stderr)

        turn = json.loads((self.root / ".agent" / "runtime" / "current-turn.json").read_text(encoding="utf-8"))
        self.assertEqual(turn["mode"], "DELTA")
        self.assertEqual(
            turn["skills"],
            ["dashboard", "design-system", "enterprise-ui-review", "skill-governance"],
        )

        stop = self.run_runtime("stop", stdin=json.dumps({"stop_hook_active": False}))
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(json.loads(stop.stdout)["decision"], "block")

        close = self.run_runtime(
            "close-turn",
            "--summary", "Runtime smoke test completed",
            "--next", "None",
            "--files", ".agent/runtime/ACTIVE_CONTEXT.md",
            "--checks", "runtime smoke test",
            "--evidence", ".agent/runtime/ACTIVE_CONTEXT.md",
        )
        self.assertEqual(close.returncode, 0, close.stderr)

        after = self.run_runtime("stop", stdin=json.dumps({"stop_hook_active": False}))
        self.assertEqual(after.stdout.strip(), "")

    def test_repository_is_not_modified(self) -> None:
        """The suite must never write into the repository it is testing."""
        handoff = (REPO / "SESSION_HANDOFF.md").read_bytes()
        log = (REPO / "logs" / "skill-usage.jsonl").read_bytes()

        self.run_runtime("manual-start", "--prompt", "Build a dashboard")
        self.run_runtime(
            "close-turn",
            "--summary", "isolation check", "--next", "None",
            "--files", "a", "--checks", "isolation", "--evidence", "a",
        )

        self.assertEqual((REPO / "SESSION_HANDOFF.md").read_bytes(), handoff)
        self.assertEqual((REPO / "logs" / "skill-usage.jsonl").read_bytes(), log)


if __name__ == "__main__":
    unittest.main()
