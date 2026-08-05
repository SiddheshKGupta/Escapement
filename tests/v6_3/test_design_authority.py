from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from capability_router import build_context_pack, route_prompt  # noqa: E402


PROMPT = (
    "Design a premium enterprise management dashboard with charts, "
    "responsive behaviour and subtle animations."
)


class DesignAuthorityTest(unittest.TestCase):
    def ids(self, route, key):
        return [item["id"] for item in route[key]]

    def test_design_intelligence_is_constitution(self):
        path = ROOT / "docs/standards/design-intelligence.md"
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Design Intelligence Constitution"))
        self.assertIn("SUPREME DESIGN AUTHORITY", text)

    def test_constitution_is_active_across_design_lifecycle(self):
        for phase in (
            "DISCOVER", "RESEARCH", "BRAINSTORM", "SPECIFY",
            "PLAN", "IMPLEMENT", "VERIFY", "POLISH", "RELEASE",
        ):
            route = route_prompt(PROMPT, phase_override=phase)
            self.assertIn(
                "design-intelligence:constitution",
                self.ids(route, "capability_strengths"),
                phase,
            )

    def test_specialists_have_distinct_phases(self):
        research = route_prompt(PROMPT, phase_override="RESEARCH")
        brainstorm = route_prompt(PROMPT, phase_override="BRAINSTORM")
        verify = route_prompt(PROMPT, phase_override="VERIFY")
        polish = route_prompt(PROMPT, phase_override="POLISH")

        self.assertIn(
            "ui-ux-pro-max:style-search",
            self.ids(research, "capability_strengths"),
        )
        self.assertIn(
            "taste:design-taste-frontend",
            self.ids(brainstorm, "capability_strengths"),
        )
        self.assertNotIn(
            "impeccable:audit",
            self.ids(brainstorm, "capability_strengths"),
        )
        self.assertIn(
            "impeccable:audit",
            self.ids(verify, "capability_strengths"),
        )
        self.assertNotIn(
            "taste:design-taste-frontend",
            self.ids(verify, "capability_strengths"),
        )
        self.assertIn(
            "impeccable:polish",
            self.ids(polish, "capability_strengths"),
        )

    def test_emil_is_conditional_on_motion(self):
        with_motion = route_prompt(PROMPT, phase_override="IMPLEMENT")
        without_motion = route_prompt(
            "Implement the approved responsive enterprise dashboard.",
            phase_override="IMPLEMENT",
        )
        self.assertIn(
            "emil:emil-design-eng",
            self.ids(with_motion, "capability_strengths"),
        )
        self.assertNotIn(
            "emil:emil-design-eng",
            self.ids(without_motion, "capability_strengths"),
        )

    def test_context_pack_stays_under_budget(self):
        for phase in (
            "DISCOVER", "RESEARCH", "BRAINSTORM", "SPECIFY",
            "PLAN", "IMPLEMENT", "VERIFY", "POLISH", "RELEASE",
        ):
            route = route_prompt(PROMPT, phase_override=phase)
            pack = build_context_pack(PROMPT, route)
            self.assertLessEqual(len(pack.split()), 1800, phase)
            self.assertLessEqual(
                route["context_cost"]["automatic_total"],
                route["context_cost"]["automatic_budget"],
                phase,
            )


if __name__ == "__main__":
    unittest.main()
