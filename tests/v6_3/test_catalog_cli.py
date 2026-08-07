from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ESCAPEMENT = ROOT / "scripts" / "escapement.py"


class CatalogCliTest(unittest.TestCase):
    """load_external_catalog() read the deprecated catalog/external-resources.json
    (47 entries, marked "deprecated": true in its own JSON) instead of
    catalog/capability-registry.json (54 entries, the file the README's own
    "external resources" table and count claims are generated from). It also read
    a "use_mode" field that doesn't exist on any resource -- the real field is
    "use_modes" -- so every listed usage mode was silently blank."""

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ESCAPEMENT), *args],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )

    def test_catalog_list_count_matches_capability_registry(self) -> None:
        registry = json.loads((ROOT / "catalog/capability-registry.json").read_text(encoding="utf-8"))
        expected = len(registry["resources"])

        result = self.run_cli("catalog", "list", "--catalog", "resources")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(len(lines), expected)

    def test_usage_modes_are_not_blank(self) -> None:
        result = self.run_cli("catalog", "list", "--catalog", "resources")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertTrue(lines)
        for line in lines:
            usage_modes = line.rsplit("|", 1)[-1].strip()
            self.assertNotEqual(usage_modes, "", f"blank usage modes: {line}")

    def test_search_finds_ui_ux_pro_max(self) -> None:
        result = self.run_cli("catalog", "search", "ui ux pro", "--catalog", "resources")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ui-ux-pro-max", result.stdout)

    def test_search_finds_karpathy(self) -> None:
        result = self.run_cli("catalog", "search", "karpathy", "--catalog", "resources")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Matches: 1", result.stdout)


class SkillsCatalogTest(unittest.TestCase):
    """catalog list only ever covered --catalog resources/patterns -- the 35
    native skills, arguably the first thing a new user wants to browse, had
    no CLI at all. native-skills.json itself carries no human description
    (just routing data: triggers/phases/overlap_group), so list/search read
    the one-line `description:` from each skill's own SKILL.md frontmatter."""

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ESCAPEMENT), *args],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )

    def test_catalog_list_count_matches_native_skills(self) -> None:
        skills = json.loads((ROOT / "catalog/native-skills.json").read_text(encoding="utf-8"))
        expected = len(skills["skills"])

        result = self.run_cli("catalog", "list", "--catalog", "skills")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(len(lines), expected)

    def test_list_shows_real_description_not_blank(self) -> None:
        result = self.run_cli("catalog", "list", "--catalog", "skills")
        self.assertEqual(result.returncode, 0, result.stderr)
        line = next(l for l in result.stdout.splitlines() if l.startswith("decision-coach:"))
        self.assertIn("MATERIAL or PROGRAM", line)

    def test_search_finds_decision_coach_by_description_text(self) -> None:
        result = self.run_cli("catalog", "search", "decision-coach", "--catalog", "skills")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"id": "decision-coach"', result.stdout)


if __name__ == "__main__":
    unittest.main()
