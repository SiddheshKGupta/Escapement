from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class RuntimeSmokeTest(unittest.TestCase):
    def test_router_stop_and_close(self) -> None:
        root = Path(__file__).resolve().parents[2]
        script = root / "scripts" / "agent_runtime.py"

        start = subprocess.run(
            [
                sys.executable, str(script), "manual-start",
                "--prompt", "Redesign the management dashboard and define KPI drill-down",
            ],
            cwd=root, text=True, capture_output=True, check=False,
        )
        self.assertEqual(start.returncode, 0, start.stderr)

        turn_file = root / ".agent" / "runtime" / "current-turn.json"
        turn = json.loads(turn_file.read_text(encoding="utf-8"))
        self.assertEqual(turn["mode"], "DELTA")
        self.assertEqual(
            turn["skills"],
            ["dashboard", "design-system", "enterprise-ui-review", "skill-governance"],
        )

        stop = subprocess.run(
            [sys.executable, str(script), "stop"],
            cwd=root,
            input=json.dumps({"stop_hook_active": False}),
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(json.loads(stop.stdout)["decision"], "block")

        close = subprocess.run(
            [
                sys.executable, str(script), "close-turn",
                "--summary", "Runtime smoke test completed",
                "--next", "None",
                "--files", ".agent/runtime/ACTIVE_CONTEXT.md",
                "--checks", "runtime smoke test",
                "--evidence", ".agent/runtime/ACTIVE_CONTEXT.md",
            ],
            cwd=root, text=True, capture_output=True, check=False,
        )
        self.assertEqual(close.returncode, 0, close.stderr)

        after = subprocess.run(
            [sys.executable, str(script), "stop"],
            cwd=root,
            input=json.dumps({"stop_hook_active": False}),
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(after.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
