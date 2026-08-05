from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from capability_router import route_prompt  # noqa: E402


class DomainCapabilityTest(unittest.TestCase):
    def skills(self, prompt, phase):
        route = route_prompt(prompt, phase_override=phase)
        return {item["id"] for item in route["native_skills"]}, route

    def test_ai_agent_lifecycle(self):
        prompt = (
            "Build a new AI agent platform and research existing agent "
            "blueprints and current industry trends."
        )
        research, route = self.skills(prompt, "RESEARCH")
        specify, _ = self.skills(prompt, "SPECIFY")
        implement, _ = self.skills(prompt, "IMPLEMENT")
        verify, _ = self.skills(prompt, "VERIFY")

        self.assertIn("agent-blueprint-discovery", research)
        self.assertIn("domain-research", research)
        self.assertIn("ai-agent-engineering", specify)
        self.assertIn("product-specification", specify)
        self.assertIn("ai-agent-engineering", implement)
        self.assertIn("quality-engineering", verify)
        self.assertIn("500-ai-agents", route["research_plan"]["sources"])
        self.assertIn("agent-reach", route["research_plan"]["sources"])

    def test_legal_and_controls_pair(self):
        skills, _ = self.skills(
            "Review this vendor contract and map compliance obligations "
            "into workflow controls.",
            "SPECIFY",
        )
        self.assertTrue({
            "legal-compliance-analysis",
            "governance-risk-controls",
            "workflow",
            "product-specification",
        }.issubset(skills))

    def test_investment_analysis_is_distinct(self):
        skills, route = self.skills(
            "Analyse this investment portfolio holding, unit economics, "
            "valuation and XIRR.",
            "RESEARCH",
        )
        self.assertEqual(route["register"], "CONSULTING")
        self.assertIn("investment-analysis", skills)
        self.assertIn("finance-reporting", skills)
        self.assertIn("domain-research", skills)

    def test_data_pipeline_and_dashboard_pair(self):
        skills, route = self.skills(
            "Build an ETL pipeline and dashboard for transaction reconciliation.",
            "IMPLEMENT",
        )
        self.assertIn("data-engineering", skills)
        self.assertIn("frontend-implementation", skills)
        self.assertIn(
            "design-intelligence:constitution",
            {item["id"] for item in route["capability_strengths"]},
        )

    def test_generic_build_has_spec_implementation_and_quality_fallbacks(self):
        prompt = (
            "Build a new internal approval module with role-based access "
            "and audit history."
        )
        spec, _ = self.skills(prompt, "SPECIFY")
        implementation, _ = self.skills(prompt, "IMPLEMENT")
        verification, _ = self.skills(prompt, "VERIFY")
        self.assertIn("product-specification", spec)
        self.assertIn("software-implementation", implementation)
        self.assertIn("quality-engineering", verification)


if __name__ == "__main__":
    unittest.main()
