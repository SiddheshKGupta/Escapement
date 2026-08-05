from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from capability_router import route_prompt  # noqa: E402


class OverlapTest(unittest.TestCase):
    def strengths(self, route):
        return {item["id"] for item in route["capability_strengths"]}

    def test_karpathy_is_baseline_and_ponytail_is_intensifier(self):
        route = route_prompt(
            "Implement this isolated API fix using the simplest solution "
            "and avoid overengineering."
        )
        strengths = self.strengths(route)
        self.assertIn("karpathy:surgical-changes", strengths)
        self.assertIn("karpathy:goal-driven-execution", strengths)
        self.assertIn("ponytail:full", strengths)
        self.assertNotIn("ponytail:ultra", strengths)

        matrix = json.loads(
            (ROOT / "catalog/overlap-matrix.json").read_text(
                encoding="utf-8"
            )
        )
        group = next(
            item for item in matrix["groups"]
            if item["id"] == "engineering-behaviour"
        )
        self.assertEqual(group["canonical"], "karpathy-guidelines")
        self.assertEqual(group["relation"], "BASELINE_PLUS_INTENSIFIER")

    def test_trigger_matching_never_uses_accidental_substrings(self):
        route = route_prompt(
            "Analyse this investment portfolio holding and valuation.",
            phase_override="PLAN",
        )
        skills = {item["id"] for item in route["native_skills"]}
        self.assertNotIn("quality-engineering", skills)

    def test_design_art_directors_do_not_collide(self):
        brainstorm = self.strengths(
            route_prompt(
                "Design a premium responsive product interface.",
                phase_override="BRAINSTORM",
            )
        )
        verify = self.strengths(
            route_prompt(
                "Design a premium responsive product interface.",
                phase_override="VERIFY",
            )
        )
        self.assertIn("taste:design-taste-frontend", brainstorm)
        self.assertNotIn("impeccable:audit", brainstorm)
        self.assertIn("impeccable:audit", verify)
        self.assertNotIn("taste:design-taste-frontend", verify)

    def test_external_methodologies_are_phase_components(self):
        adapters = json.loads(
            (ROOT / "catalog/strategy-adapters.json").read_text(
                encoding="utf-8"
            )
        )
        superpowers = next(
            item for item in adapters["adapters"]
            if item["id"] == "superpowers-sdlc"
        )
        self.assertIn(
            "superpowers:brainstorming",
            superpowers["phase_mapping"]["BRAINSTORM"],
        )
        self.assertIn(
            "superpowers:test-driven-development",
            superpowers["phase_mapping"]["IMPLEMENT"],
        )
        self.assertIn(
            "superpowers:verification-before-completion",
            superpowers["phase_mapping"]["VERIFY"],
        )


if __name__ == "__main__":
    unittest.main()
