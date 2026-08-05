from __future__ import annotations

import json
import unittest
from pathlib import Path


class RegistryAndNeutralityTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]

    def test_all_native_skills_have_three_copies(self):
        registry = json.loads(
            (self.root / "catalog/native-skills.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(len(registry["skills"]), 32)
        for item in registry["skills"]:
            skill = item["id"]
            for path in (
                self.root / "skills" / skill / "SKILL.md",
                self.root / ".agents" / "skills" / skill / "SKILL.md",
                self.root / ".claude" / "skills" / skill / "SKILL.md",
            ):
                self.assertTrue(path.exists(), str(path))

    def test_capability_catalogues_are_comprehensive(self):
        strengths = json.loads(
            (self.root / "catalog/skill-strengths.json").read_text(
                encoding="utf-8"
            )
        )
        families = json.loads(
            (self.root / "catalog/capability-families.json").read_text(
                encoding="utf-8"
            )
        )
        resources = json.loads(
            (self.root / "catalog/capability-registry.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(len(strengths["capabilities"]), 58)
        self.assertGreaterEqual(len(families["families"]), 10)
        self.assertGreaterEqual(len(resources["resources"]), 54)

    def test_package_is_organisation_neutral(self):
        forbidden = (
            "V L " + "& CO",
            "VL" + "CO",
            "profiles/" + "vlco",
            "profile: " + "vlco",
        )
        violations = []
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            if any(
                part in {".agent", "__pycache__"}
                for part in path.parts
            ):
                continue
            if path.suffix.lower() not in {
                ".md", ".json", ".yaml", ".yml", ".py", ".txt"
            }:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for value in forbidden:
                if value in text:
                    violations.append(
                        f"{path.relative_to(self.root)}: {value}"
                    )
        self.assertEqual(violations, [])

    def test_domain_expertise_is_default(self):
        state = (self.root / "PROJECT_STATE.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("profile: domain-expertise", state)
        self.assertTrue((self.root / "DOMAIN_CONTEXT.md").exists())
        self.assertTrue(
            (self.root / "profiles/domain-expertise/PROFILE.md").exists()
        )


if __name__ == "__main__":
    unittest.main()
