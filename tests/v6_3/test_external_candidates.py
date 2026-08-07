from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from capability_router import route_prompt  # noqa: E402

NEW_IDS = [
    "prime-intellect-prime-agent",
    "egonex-understand-anything",
    "evomap-evolver",
    "agency-agents",
    "nidhinjs-prompt-master",
    "mattpocock-grilling",
    "cloudflare-os",
]


def load_registry() -> dict:
    return json.loads((ROOT / "catalog" / "capability-registry.json").read_text(encoding="utf-8"))


def load_matrix() -> dict:
    return json.loads((ROOT / "catalog" / "overlap-matrix.json").read_text(encoding="utf-8"))


class RegistrySchemaTest(unittest.TestCase):
    """Seven new external candidates reviewed 2026-08-07: an agent runtime
    (Prime Agent), a code-knowledge plugin (Understand Anything), a
    self-evolution meta-observer (Evolver), a persona catalogue (Agency
    Agents), a prompt-export skill (Prompt Master), a decision-interview
    skill (Matt Pocock's Grilling), and an architecture reference
    (Cloudflare OS). None are installed as running dependencies -- being
    catalogued is not being installed (see docs/REFERENCE_CATALOG.md)."""

    def setUp(self):
        self.registry = load_registry()
        self.resources = {item["id"]: item for item in self.registry["resources"]}

    def test_all_seven_candidates_present(self):
        for candidate_id in NEW_IDS:
            self.assertIn(candidate_id, self.resources)

    def test_resource_ids_are_unique(self):
        ids = [item["id"] for item in self.registry["resources"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_new_candidates_have_valid_source_urls(self):
        for candidate_id in NEW_IDS:
            source = self.resources[candidate_id]["source"]
            parsed = urlparse(source)
            self.assertIn(parsed.scheme, {"http", "https"}, candidate_id)
            self.assertTrue(parsed.netloc, candidate_id)

    def test_new_candidates_have_license_status(self):
        for candidate_id in NEW_IDS:
            item = self.resources[candidate_id]
            self.assertTrue(item.get("license"))
            self.assertTrue(item.get("license_status"))

    def test_no_candidate_marked_installed(self):
        installed_like = {"installed"}
        for candidate_id in NEW_IDS:
            self.assertNotIn(self.resources[candidate_id]["status"], installed_like)

    def test_none_of_the_seven_are_native_skills(self):
        native = json.loads((ROOT / "catalog" / "native-skills.json").read_text(encoding="utf-8"))
        native_ids = {item["id"] for item in native.get("skills", native.get("native_skills", []))}
        for candidate_id in NEW_IDS:
            self.assertNotIn(candidate_id, native_ids)


class OverlapGroupReferenceTest(unittest.TestCase):
    def setUp(self):
        self.matrix = load_matrix()
        self.groups = {g["id"]: g for g in self.matrix["groups"]}

    def test_decision_interview_group_exists_and_is_canonical_decision_coach(self):
        group = self.groups["decision-interview"]
        self.assertEqual(group["canonical"], "decision-coach")
        self.assertIn("mattpocock-grilling", group["members"])

    def test_prompt_shaping_group_is_sequential_after_specification(self):
        group = self.groups["prompt-shaping"]
        self.assertEqual(group["relation"], "SEQUENTIAL")
        self.assertEqual(group["canonical"], "product-specification")
        self.assertIn("nidhinjs-prompt-master", group["members"])

    def test_evolver_joins_skill_learning_as_meta_observer(self):
        group = self.groups["skill-learning"]
        self.assertEqual(group["relation"], "META_OBSERVER")
        self.assertIn("evomap-evolver", group["members"])
        self.assertIn("task-observer", group["members"])

    def test_understand_anything_joins_memory_and_knowledge_as_substitute(self):
        group = self.groups["memory-and-knowledge"]
        self.assertEqual(group["relation"], "SUBSTITUTE")
        self.assertIn("egonex-understand-anything", group["members"])

    def test_prime_agent_joins_delivery_methodology(self):
        group = self.groups["delivery-methodology"]
        self.assertIn("prime-intellect-prime-agent", group["members"])
        self.assertEqual(group["canonical"], "escapement-core")

    def test_agency_agents_and_cloudflare_os_have_no_dedicated_matrix_group(self):
        """Reference-only catalogues without a genuine conflict to arbitrate
        (matching the existing precedent for 500-ai-agents-projects, which
        has a descriptive overlap_group tag but no matrix group either)."""
        registry = load_registry()
        resources = {item["id"]: item for item in registry["resources"]}
        for candidate_id in ("agency-agents", "cloudflare-os"):
            group_tag = resources[candidate_id]["overlap_group"]
            self.assertNotIn(group_tag, self.groups)


class RoutingTest(unittest.TestCase):
    def candidates(self, prompt: str, phase: str) -> set[str]:
        route = route_prompt(prompt, phase_override=phase)
        return {item["id"] for item in route["external_candidates"]}

    def test_understand_anything_routes_for_codebase_understanding(self):
        for prompt in [
            "Help me understand this large unfamiliar codebase",
            "Create an architecture map of this repository",
            "Extract the business-domain flows from this repository",
        ]:
            self.assertIn("egonex-understand-anything", self.candidates(prompt, "DISCOVER"))

    def test_understand_anything_does_not_route_for_trivial_edits(self):
        for prompt in ["Fix this typo", "Rename one variable", "Explain this five-line function"]:
            self.assertNotIn("egonex-understand-anything", self.candidates(prompt, "IMPLEMENT"))

    def test_grilling_routes_only_for_explicit_stress_test_language(self):
        for prompt in [
            "Grill me on this architecture",
            "Stress-test my plan",
            "Challenge every assumption in this design",
        ]:
            self.assertIn("mattpocock-grilling", self.candidates(prompt, "DISCOVER"))

    def test_grilling_does_not_route_implicitly_for_feature_requests(self):
        for prompt in ["Build a claims platform", "Add a login page", "Design my database"]:
            self.assertNotIn("mattpocock-grilling", self.candidates(prompt, "DISCOVER"))

    def test_prompt_master_routes_for_cross_tool_export(self):
        for prompt in [
            "Convert this approved specification into a Cursor prompt",
            "Write a prompt for Midjourney using this approved creative brief",
            "Export this Escapement brief for Claude Code",
        ]:
            self.assertIn("nidhinjs-prompt-master", self.candidates(prompt, "SPECIFY"))

    def test_prompt_master_does_not_replace_normal_discovery(self):
        for prompt in ["Build a claims platform", "Design my database", "Fix this API"]:
            self.assertNotIn("nidhinjs-prompt-master", self.candidates(prompt, "SPECIFY"))

    def test_agency_agents_routes_only_for_role_discovery(self):
        for prompt in [
            "Find a specialist agent role",
            "Suggest a fresh-context reviewer",
            "Find a domain persona for this review",
        ]:
            self.assertIn("agency-agents", self.candidates(prompt, "PLAN"))

    def test_evolver_routes_only_with_usable_history_framing(self):
        for prompt in [
            "Analyse the harness logs for recurring failures",
            "Suggest an auditable improvement to our agent workflow",
            "Review repeated routing failures",
        ]:
            self.assertIn("evomap-evolver", self.candidates(prompt, "VERIFY"))

    def test_evolver_inactive_with_no_history_framing(self):
        self.assertNotIn("evomap-evolver", self.candidates("Build a claims platform", "VERIFY"))

    def test_prime_agent_routes_as_external_runtime_not_a_skill(self):
        for prompt in [
            "Run a long-lived background coding agent",
            "Use a persistent REPL with recursive subagents",
            "I need detachable agent sessions and JSON RPC",
        ]:
            ids = self.candidates(prompt, "PLAN")
            self.assertIn("prime-intellect-prime-agent", ids)
        registry = load_registry()
        resource = next(r for r in registry["resources"] if r["id"] == "prime-intellect-prime-agent")
        self.assertEqual(resource["kind"], "external-agent-runtime")

    def test_cloudflare_os_routes_only_as_architecture_reference(self):
        for prompt in [
            "Design a secure enterprise agent workspace",
            "How should agents receive narrow access to company systems?",
            "Design sandboxed AI-generated internal apps",
            "Create an approval layer for agent side effects",
        ]:
            self.assertIn("cloudflare-os", self.candidates(prompt, "RESEARCH"))
        registry = load_registry()
        resource = next(r for r in registry["resources"] if r["id"] == "cloudflare-os")
        self.assertEqual(resource["status"], "reference-only")


class DecisionGrillingSkillTest(unittest.TestCase):
    """The real, tested implementation lives in decision-coach's SKILL.md
    as an original intensifier section -- not a copy of the external
    skill's text, and not a separate skills/ folder (capability strengths
    like karpathy-guidelines/ponytail already establish that pattern for
    externally-inspired behaviour that isn't its own native procedure)."""

    def setUp(self):
        self.content = (ROOT / "skills" / "decision-coach" / "SKILL.md").read_text(encoding="utf-8")

    def test_grilling_intensifier_section_exists(self):
        self.assertIn("## Grilling Intensifier", self.content)

    def test_attributes_the_source(self):
        section = self.content.split("## Grilling Intensifier")[1]
        self.assertIn("mattpocock/skills", section)
        self.assertIn("MIT", section)

    def test_preserves_five_question_cap(self):
        section = self.content.split("## Grilling Intensifier")[1]
        self.assertIn("five material questions", section)

    def test_references_overlap_group(self):
        section = self.content.split("## Grilling Intensifier")[1]
        self.assertIn("decision-interview", section)


if __name__ == "__main__":
    unittest.main()
