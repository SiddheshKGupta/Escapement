from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from capability_router import enforce_context_budget  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


class SkillBudgetDocsConsistencyTest(unittest.TestCase):
    """Found while researching "context rot" (skill files growing too large
    without ever being pruned): README.md and PROJECT_CONTEXT.md both
    claimed the invoked-native-skill-context ceiling was 1,200 words, but
    no profile overrides capability_router.py's actual default of 1,000 --
    the real enforcement was stricter than the documented promise. Fixed
    by correcting the docs to the real number rather than loosening the
    code, since loosening would be the wrong direction for the exact
    failure mode that surfaced this. This test locks the actual default in
    place and cross-checks it against the documented claim, so the two
    can't silently drift apart again."""

    def test_actual_default_skill_budget_is_1000(self) -> None:
        _, _, _, cost = enforce_context_budget(
            profile={}, packs=[], skills=[], profile_id="test", decision_brief_words=0,
        )
        self.assertEqual(cost["skill_budget"], 1000)

    def test_readme_states_the_real_default(self) -> None:
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Invoked native-skill context:  <= 1,000 words", content)
        self.assertNotIn("1,200 words", content)

    def test_project_context_states_the_real_default(self) -> None:
        content = (ROOT / "PROJECT_CONTEXT.md").read_text(encoding="utf-8")
        self.assertIn("invoked native skill context below 1,000 words", content)


if __name__ == "__main__":
    unittest.main()
