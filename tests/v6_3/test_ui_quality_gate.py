from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class UiQualityGateTest(unittest.TestCase):
    """frontend-implementation/SKILL.md already instructed covering loading/
    error states, motion, and responsiveness -- correct, existing doctrine
    that was still skipped in real use, because nothing forced actually
    reading it before considering UI work done. ui_quality_gate.py checks
    for concrete, detectable signals in the source instead of trusting
    that the routed skill was read -- same idea as security_gate.py not
    relying on an agent remembering to be careful."""

    def setUp(self):
        self.script = Path(__file__).resolve().parents[2] / "scripts" / "ui_quality_gate.py"
        self.temp = tempfile.TemporaryDirectory(prefix="esc-ui-gate-")
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_gate(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.script), str(self.root), *args],
            text=True, capture_output=True, check=False,
        )

    def test_warns_on_all_signals_for_bare_component(self) -> None:
        (self.root / "App.jsx").write_text("export default function App() { return <div>hi</div> }")
        (self.root / "App.css").write_text(".foo { color: red; }")

        result = self.run_gate("--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        statuses = {f["check"]: f["status"] for f in report["findings"]}
        self.assertEqual(statuses["responsive-breakpoints"], "WARN")
        self.assertEqual(statuses["motion-transitions"], "WARN")
        self.assertEqual(statuses["reduced-motion-respect"], "WARN")
        self.assertEqual(statuses["focus-visible"], "WARN")
        self.assertEqual(statuses["loading-state-handling"], "WARN")
        self.assertEqual(statuses["error-state-handling"], "WARN")
        self.assertEqual(report["warnings"], 6)

    def test_passes_all_signals_when_present(self) -> None:
        (self.root / "App.css").write_text(
            "@media (max-width: 768px) { .a { color: red; } }\n"
            ".b { transition: color 140ms ease-out; }\n"
            "@media (prefers-reduced-motion: reduce) { * { transition: none; } }\n"
            "button:focus-visible { outline: 2px solid blue; }\n"
        )
        (self.root / "Page.jsx").write_text(
            "function Page() {\n"
            "  try {\n"
            "    doThing()\n"
            "  } catch {\n"
            "    setError('failed')\n"
            "  }\n"
            "  return <p>Loading...</p>\n"
            "}\n"
        )

        result = self.run_gate("--json")
        report = json.loads(result.stdout)
        self.assertEqual(report["warnings"], 0)

    def test_fail_on_warn_exits_nonzero(self) -> None:
        (self.root / "App.jsx").write_text("export default function App() { return null }")
        result = self.run_gate("--fail-on-warn")
        self.assertNotEqual(result.returncode, 0)

    def test_missing_root_fails(self) -> None:
        result = subprocess.run(
            [sys.executable, str(self.script), str(self.root / "does-not-exist")],
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
