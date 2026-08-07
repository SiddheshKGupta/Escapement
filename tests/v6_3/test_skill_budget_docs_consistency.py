from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from capability_router import active_profile, enforce_context_budget  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DOCUMENTED_SKILL_BUDGET = 1000

DOC_CLAIMS = {
    "README.md": "Invoked native-skill context:  <= 1,000 words",
    "PROJECT_CONTEXT.md": "invoked native skill context below 1,000 words",
    "SESSION_HANDOFF.md": "Invoked skill context: tested below `1,000` words",
    "reports/VALIDATION_v6.3.md": "Invoked skill context | PASS — tested routes below 1,000 words",
}


class SkillBudgetDocsConsistencyTest(unittest.TestCase):
    """The first version of this test asserted the budget by calling
    enforce_context_budget(profile={}) -- an empty dict, which exercises the
    hardcoded fallback in capability_router.py and never loads a real
    profile. The fallback was 1,000 and the docs said 1,000, so the test
    passed; meanwhile profiles/domain-expertise/profile.json (the default
    profile, and the one every real run resolves) set 1,200. Every route
    actually enforced 1,200 while four documents promised 1,000, and the
    test that existed to prevent exactly this drift could not see it.

    Fixed by tightening the profile to the documented 1,000 rather than
    loosening the docs -- the conservative direction, and the one the
    low-token claim depends on. These tests now read the shipped profiles
    instead of a hypothetical empty one."""

    def shipped_profiles(self) -> list[tuple[str, dict]]:
        found = []
        for path in sorted((ROOT / "profiles").glob("*/profile.json")):
            found.append((path.parent.name, json.loads(path.read_text(encoding="utf-8"))))
        self.assertTrue(found, "no profiles found")
        return found

    def test_active_profile_enforces_the_documented_budget(self) -> None:
        """The check that actually matters: what a real run resolves."""
        profile_id, profile = active_profile()
        _, _, _, cost = enforce_context_budget(
            profile=profile, packs=[], skills=[], profile_id=profile_id,
            decision_brief_words=0,
        )
        self.assertEqual(
            cost["skill_budget"], DOCUMENTED_SKILL_BUDGET,
            f"active profile '{profile_id}' enforces {cost['skill_budget']}, "
            f"docs promise {DOCUMENTED_SKILL_BUDGET}",
        )

    def test_every_shipped_profile_agrees_with_the_docs(self) -> None:
        for name, profile in self.shipped_profiles():
            budget = profile.get("skill_context_budget_words")
            if budget is None:
                continue
            self.assertEqual(
                budget, DOCUMENTED_SKILL_BUDGET,
                f"profile '{name}' sets {budget}, docs promise {DOCUMENTED_SKILL_BUDGET}",
            )

    def test_code_fallback_also_agrees(self) -> None:
        _, _, _, cost = enforce_context_budget(
            profile={}, packs=[], skills=[], profile_id="test", decision_brief_words=0,
        )
        self.assertEqual(cost["skill_budget"], DOCUMENTED_SKILL_BUDGET)

    def test_documents_state_the_real_number(self) -> None:
        for relative, claim in DOC_CLAIMS.items():
            content = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(claim, content, f"{relative} no longer states the budget")
            self.assertNotIn("1,200 words", content, relative)


class ProfileConfigIsActuallyReadTest(unittest.TestCase):
    """profiles/default/profile.json declared `maximum_doctrine_packs` and
    `maximum_native_skills`, but capability_router.py only reads the
    `*_per_phase` spellings -- so selecting that profile silently fell back
    to the permissive tier defaults instead of its own stated limits.
    domain-expertise separately declared `extends: "default"`, which no code
    reads at all. Both were config that looked authoritative and did
    nothing."""

    ROUTER_SOURCE = (ROOT / "scripts" / "capability_router.py").read_text(encoding="utf-8")

    def profile_keys(self) -> set[str]:
        keys: set[str] = set()
        for path in (ROOT / "profiles").glob("*/profile.json"):
            keys |= set(json.loads(path.read_text(encoding="utf-8")))
        return keys

    def test_no_profile_declares_a_limit_key_the_router_ignores(self) -> None:
        for dead in ("maximum_doctrine_packs", "maximum_native_skills"):
            for path in (ROOT / "profiles").glob("*/profile.json"):
                profile = json.loads(path.read_text(encoding="utf-8"))
                self.assertNotIn(
                    dead, profile,
                    f"{path.parent.name} declares '{dead}', but the router only "
                    f"reads '{dead}_per_phase'",
                )

    def test_no_profile_declares_unimplemented_inheritance(self) -> None:
        self.assertNotIn("extends", self.ROUTER_SOURCE)
        for path in (ROOT / "profiles").glob("*/profile.json"):
            profile = json.loads(path.read_text(encoding="utf-8"))
            self.assertNotIn(
                "extends", profile,
                f"{path.parent.name} declares 'extends', but no code applies it",
            )

    def test_per_phase_limits_are_read_by_the_router(self) -> None:
        for key in ("maximum_doctrine_packs_per_phase", "maximum_native_skills_per_phase"):
            self.assertIn(key, self.ROUTER_SOURCE)


if __name__ == "__main__":
    unittest.main()
