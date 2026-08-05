from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from capability_router import route_prompt  # noqa: E402


class BrowserAndResearchTest(unittest.TestCase):
    def test_browser_frameworks_are_not_loaded_together(self):
        route = route_prompt(
            "Verify this responsive frontend in Playwright with accessibility "
            "and end-to-end tests.",
            phase_override="VERIFY",
        )
        strengths = {
            item["id"] for item in route["capability_strengths"]
        }
        self.assertIn("playwright:project-tests", strengths)
        self.assertNotIn("cypress:project-tests", strengths)
        self.assertNotIn("stagehand:self-healing", strengths)

    def test_recent_research_uses_supporting_channels(self):
        route = route_prompt(
            "Research the latest industry standards and current Reddit and "
            "YouTube trends from the last 30 days.",
            phase_override="RESEARCH",
        )
        sources = set(route["research_plan"]["sources"])
        self.assertIn("primary-web", sources)
        self.assertIn("last30days", sources)
        self.assertIn("agent-reach", sources)
        self.assertTrue(route["research_plan"]["authoritative_first"])

    def test_500_agents_remains_discovery_only(self):
        route = route_prompt(
            "Find an AI agent blueprint from the 500 agents catalogue.",
            phase_override="RESEARCH",
        )
        strengths = {
            item["id"] for item in route["capability_strengths"]
        }
        self.assertIn("500-ai-agents:blueprint-discovery", strengths)
        self.assertNotIn(
            "500-ai-agents:blueprint-discovery",
            {item["id"] for item in route["native_skills"]},
        )


if __name__ == "__main__":
    unittest.main()
