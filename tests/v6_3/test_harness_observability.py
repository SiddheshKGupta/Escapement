from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class HarnessObservabilityTest(unittest.TestCase):
    """turns.jsonl and logs/skill-usage.jsonl are already written on every
    turn -- but nothing read them back as a trend, so a real gap (the
    data-architecture/SKILL.md bloat that led to the skill-budget docs
    fix) had to be found by a research tangent instead of by the harness
    surfacing its own context-budget pruning. This aggregates what
    already exists into exactly that kind of trend."""

    def setUp(self):
        self.script = Path(__file__).resolve().parents[2] / "scripts" / "harness_observability.py"
        self.temp = tempfile.TemporaryDirectory(prefix="esc-observability-")
        self.root = Path(self.temp.name)
        (self.root / ".agent" / "runtime").mkdir(parents=True)
        (self.root / "logs").mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write_turns(self, records: list[dict]) -> None:
        path = self.root / ".agent" / "runtime" / "turns.jsonl"
        path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")

    def write_skill_runs(self, records: list[dict]) -> None:
        path = self.root / "logs" / "skill-usage.jsonl"
        path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")

    def run_report(self) -> dict:
        result = subprocess.run(
            [sys.executable, str(self.script), "--root", str(self.root), "--json"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_empty_logs_report_zero_closed_turns(self) -> None:
        report = self.run_report()
        self.assertEqual(report["closed_turns"], 0)
        self.assertEqual(report["skill_routed_never_used"], [])

    def test_counts_closed_turns_and_tiers(self) -> None:
        self.write_turns([
            {"turn_id": "T1", "closure": {"tier": "MATERIAL", "result": "PASS"}, "route": {"rejected": []}},
            {"turn_id": "T2", "closure": {"tier": "PROGRAM", "result": "PARTIAL"}, "route": {"rejected": []}},
        ])
        report = self.run_report()
        self.assertEqual(report["closed_turns"], 2)
        self.assertEqual(report["tier_distribution"], {"MATERIAL": 1, "PROGRAM": 1})
        self.assertEqual(report["closure_result_distribution"], {"PASS": 1, "PARTIAL": 1})

    def test_phase_replan_reasons_are_counted(self) -> None:
        self.write_turns([
            {"turn_id": "T1", "event": "phase-plan-revised", "reason": "Touches stored credentials."},
            {"turn_id": "T1", "event": "phase-plan-revised", "reason": "Touches stored credentials."},
        ])
        report = self.run_report()
        self.assertEqual(report["phase_replans"], 2)
        self.assertEqual(report["phase_replan_reasons"], {"Touches stored credentials.": 2})

    def test_skill_routed_but_never_used_is_flagged(self) -> None:
        self.write_skill_runs([
            {"turn_id": "T1", "skill": "decision-coach", "used": True},
            {"turn_id": "T1", "skill": "reference-router", "used": False},
            {"turn_id": "T2", "skill": "reference-router", "used": False},
        ])
        report = self.run_report()
        self.assertEqual(report["skill_routed_never_used"], ["reference-router"])
        self.assertNotIn("decision-coach", report["skill_routed_never_used"])

    def test_skill_used_at_least_once_is_not_flagged(self) -> None:
        self.write_skill_runs([
            {"turn_id": "T1", "skill": "decision-coach", "used": False},
            {"turn_id": "T2", "skill": "decision-coach", "used": True},
        ])
        report = self.run_report()
        self.assertEqual(report["skill_routed_never_used"], [])

    def test_rejection_reasons_from_closed_turn_routes_are_counted(self) -> None:
        self.write_turns([
            {
                "turn_id": "T1",
                "closure": {"tier": "MATERIAL", "result": "PASS"},
                "route": {"rejected": [
                    {"id": "data-architecture", "rejected_because": "invoked-skill-context-budget"},
                    {"id": "some-skill", "rejected_because": "overlap:design-direction"},
                ]},
            },
        ])
        report = self.run_report()
        self.assertEqual(report["rejection_reasons"]["invoked-skill-context-budget"], 1)
        self.assertEqual(report["rejection_reasons"]["overlap:design-direction"], 1)

    def test_malformed_json_lines_are_skipped_not_fatal(self) -> None:
        path = self.root / ".agent" / "runtime" / "turns.jsonl"
        path.write_text('{"turn_id": "T1", "closure": {"tier": "MICRO", "result": "PASS"}, "route": {"rejected": []}}\nnot json\n', encoding="utf-8")
        report = self.run_report()
        self.assertEqual(report["closed_turns"], 1)


if __name__ == "__main__":
    unittest.main()
