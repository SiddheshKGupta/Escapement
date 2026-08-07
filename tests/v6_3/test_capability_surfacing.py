from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text)


class CapabilitySurfacingDoctrineTest(unittest.TestCase):
    """A first-time user has no way to know Escapement has 35 native skills
    and 61 governed external candidates unless they already know to run
    `catalog list`. decision-coach asked material questions about the
    decision but never mentioned a matched, not-yet-installed capability --
    the audit existed (capability-audit) but was framed as a pre-implement
    checklist, not part of the same conversation where the user could
    actually say yes or no to using one. This is a doctrine (prose) change,
    so it's tested the same way other doctrine changes in this repo are:
    asserting the required content and framing actually landed."""

    def setUp(self):
        self.kernel = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.decision_coach = (ROOT / "skills" / "decision-coach" / "SKILL.md").read_text(encoding="utf-8")

    def test_kernel_moves_audit_into_the_question_round(self):
        section = self.kernel.split("## Help the User Think Better")[1].split("##")[0]
        self.assertIn("during this round, not only before implementing", section)
        self.assertIn("optional lever", section)

    def test_kernel_requires_offering_not_auto_running_research(self):
        section = normalize(self.kernel.split("## Help the User Think Better")[1].split("##")[0])
        self.assertIn("offer -- never auto-run -- research", section)

    def test_decision_coach_has_surface_relevant_capabilities_section(self):
        self.assertIn("## Surface Relevant Capabilities", self.decision_coach)

    def test_decision_coach_surfacing_references_capability_audit(self):
        section = self.decision_coach.split("## Surface Relevant Capabilities")[1].split("##")[0]
        self.assertIn("capability-audit", section)
        self.assertIn("recommended yes/use-it or", section)

    def test_decision_coach_surfacing_is_an_approval_gate(self):
        section = normalize(self.decision_coach.split("## Surface Relevant Capabilities")[1].split("##")[0])
        self.assertIn("Approval Gates", section)
        self.assertIn("never an installed default", section)

    def test_decision_coach_offers_research_beyond_the_catalogue(self):
        section = normalize(self.decision_coach.split("## Surface Relevant Capabilities")[1].split("##")[0])
        self.assertIn("do not silently perform", section)
        self.assertIn("reference-router", section)

    def test_decision_coach_surfacing_scoped_away_from_micro(self):
        section = self.decision_coach.split("## Surface Relevant Capabilities")[1].split("##")[0]
        self.assertIn("Skip this section for MICRO work", section)

    def test_fanned_out_skill_copies_stay_in_sync(self):
        for host in (".agents", ".claude"):
            copy = (ROOT / host / "skills" / "decision-coach" / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(copy, self.decision_coach, f"{host} copy drifted from canonical skills/")

    def test_kernel_still_within_budget(self):
        from capability_router import word_count
        self.assertLessEqual(word_count(ROOT / "AGENTS.md"), 1000)


if __name__ == "__main__":
    unittest.main()
