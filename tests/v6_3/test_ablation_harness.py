from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from ablation_harness import (  # noqa: E402
    apply_ablation,
    compare,
    diff_case,
    find_component,
    load_registry,
    route_facts,
)


class RegistryTest(unittest.TestCase):
    """A stale registry is the main way this tool could silently lie: if a
    component's ablation target no longer exists, apply_ablation must fail
    loudly rather than report 'no measurable difference' from a no-op."""

    def setUp(self):
        self.registry = load_registry(ROOT)

    def test_registry_has_components(self):
        self.assertTrue(self.registry.get("components"))

    def test_component_ids_are_unique(self):
        ids = [item["id"] for item in self.registry["components"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_component_declares_required_fields(self):
        for item in self.registry["components"]:
            for field in ("id", "kind", "hypothesis", "ablation"):
                self.assertIn(field, item, item.get("id"))

    def test_every_ablation_target_actually_exists(self):
        for item in self.registry["components"]:
            spec = item["ablation"]
            path = ROOT / spec["file"]
            self.assertTrue(path.exists(), f"{item['id']}: missing {spec['file']}")
            data = json.loads(path.read_text(encoding="utf-8"))
            entries = data.get(spec["collection"])
            self.assertIsInstance(entries, list, item["id"])
            matches = [e for e in entries if e.get(spec["match_field"]) == spec["match_value"]]
            self.assertEqual(
                len(matches), 1,
                f"{item['id']}: expected exactly one entry with "
                f"{spec['match_field']}={spec['match_value']!r}",
            )

    def test_unknown_component_is_rejected(self):
        with self.assertRaises(SystemExit):
            find_component(self.registry, "no-such-component")


class ApplyAblationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="esc-ablation-test-")
        self.destination = Path(self.temp.name)
        (self.destination / "catalog").mkdir()
        self.target = self.destination / "catalog" / "things.json"
        self.target.write_text(json.dumps({
            "schema_version": "1.0",
            "things": [{"id": "keep-me"}, {"id": "remove-me"}],
        }), encoding="utf-8")
        self.component = {
            "id": "remove-me",
            "ablation": {
                "method": "remove-catalog-entry",
                "file": "catalog/things.json",
                "collection": "things",
                "match_field": "id",
                "match_value": "remove-me",
            },
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_removes_only_the_named_entry(self):
        applied = apply_ablation(self.destination, self.component)
        self.assertEqual(applied["entries_removed"], 1)
        data = json.loads(self.target.read_text(encoding="utf-8"))
        self.assertEqual([t["id"] for t in data["things"]], ["keep-me"])

    def test_preserves_other_top_level_keys(self):
        apply_ablation(self.destination, self.component)
        data = json.loads(self.target.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "1.0")

    def test_missing_match_fails_loudly(self):
        self.component["ablation"]["match_value"] = "not-present"
        with self.assertRaises(SystemExit):
            apply_ablation(self.destination, self.component)

    def test_unsupported_method_is_rejected(self):
        self.component["ablation"]["method"] = "patch-source-file"
        with self.assertRaises(SystemExit):
            apply_ablation(self.destination, self.component)

    def test_missing_target_file_fails_loudly(self):
        self.component["ablation"]["file"] = "catalog/absent.json"
        with self.assertRaises(SystemExit):
            apply_ablation(self.destination, self.component)


def record(case_id: str, result: str, skills: list[str], strengths: list[str],
           automatic: int = 1000, invoked: int = 500, questions: int = 2,
           failures: list[str] | None = None) -> dict:
    return {
        "case_id": case_id,
        "result": result,
        "failures": failures or [],
        "actual": {
            "native_skills": [{"id": s} for s in skills],
            "capability_strengths": [{"id": s} for s in strengths],
            "doctrine_packs": [],
            "external_candidates": [],
            "decision_brief": {"questions": [{}] * questions},
            "phase_plan": [{"id": "DISCOVER"}],
            "rejected": [],
            "context_cost": {"automatic_total": automatic, "invoked_skill_total": invoked},
        },
    }


class DiffTest(unittest.TestCase):
    def test_route_facts_extracts_measurable_fields(self):
        facts = route_facts(record("c", "PASS", ["a"], ["b"], questions=3))
        self.assertEqual(facts["skills"], ["a"])
        self.assertEqual(facts["strengths"], ["b"])
        self.assertEqual(facts["questions"], 3)
        self.assertEqual(facts["invoked_skill_words"], 500)

    def test_identical_routes_produce_no_delta(self):
        control = route_facts(record("c", "PASS", ["a"], ["b"]))
        ablated = route_facts(record("c", "PASS", ["a"], ["b"]))
        self.assertEqual(diff_case(control, ablated), {})

    def test_detects_lost_skill_and_context_saving(self):
        control = route_facts(record("c", "PASS", ["a", "b"], [], invoked=900))
        ablated = route_facts(record("c", "FAIL", ["a"], [], invoked=500))
        delta = diff_case(control, ablated)
        self.assertEqual(delta["skills_lost"], ["b"])
        self.assertEqual(delta["result"], "PASS -> FAIL")
        self.assertEqual(delta["invoked_skill_words"]["change"], -400)

    def test_detects_newly_added_failure(self):
        control = route_facts(record("c", "PASS", ["a"], []))
        ablated = route_facts(record("c", "FAIL", ["a"], [], failures=["missing skills ['b']"]))
        self.assertEqual(diff_case(control, ablated)["failures_added"], ["missing skills ['b']"])


class CompareTest(unittest.TestCase):
    component = {"id": "x", "kind": "native-skill", "hypothesis": "h", "cost": {}}
    applied = {"file": "catalog/x.json", "collection": "x", "entries_removed": 1}

    def test_unexercised_component_is_reported_as_such(self):
        control = [record("c1", "PASS", ["a"], [])]
        ablated = [record("c1", "PASS", ["a"], [])]
        report = compare(self.component, control, ablated, self.applied)
        self.assertFalse(report["exercised_by_corpus"])
        self.assertEqual(report["changed_cases"], [])
        self.assertEqual(report["control_passed"], report["ablated_passed"])

    def test_exercised_component_lists_changed_cases(self):
        control = [record("c1", "PASS", ["a", "b"], []), record("c2", "PASS", ["a"], [])]
        ablated = [record("c1", "FAIL", ["a"], []), record("c2", "PASS", ["a"], [])]
        report = compare(self.component, control, ablated, self.applied)
        self.assertTrue(report["exercised_by_corpus"])
        self.assertEqual(report["cases_with_result_change"], ["c1"])
        self.assertEqual(report["control_passed"], 2)
        self.assertEqual(report["ablated_passed"], 1)

    def test_report_always_carries_its_limitations(self):
        report = compare(self.component, [record("c1", "PASS", ["a"], [])],
                         [record("c1", "PASS", ["a"], [])], self.applied)
        self.assertTrue(report["limitations"])
        self.assertTrue(any("No score" in item for item in report["limitations"]))

    def test_no_score_field_is_produced(self):
        """The corpus is 22 routing cases. Any composite score would imply a
        rigour this evidence does not have. Checks the report's data keys --
        the limitations prose legitimately mentions these words."""
        report = compare(self.component, [record("c1", "PASS", ["a"], [])],
                         [record("c1", "FAIL", [], [])], self.applied)
        keys = set(report) | {
            key for case in report["changed_cases"] for key in case["delta"]
        }
        for banned in ("score", "significance", "improvement", "p_value", "rating"):
            self.assertFalse(
                [key for key in keys if banned in key.lower()],
                f"report exposes a {banned}-like field: {sorted(keys)}",
            )


class CanonicalSafetyTest(unittest.TestCase):
    """The whole design rests on canonical files never being edited. If a run
    ever dirties the working tree, the tool is unsafe regardless of output."""

    def test_listing_components_does_not_modify_the_repository(self):
        before = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=False,
        ).stdout
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "ablation_harness.py"), "list"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        after = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=False,
        ).stdout
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
