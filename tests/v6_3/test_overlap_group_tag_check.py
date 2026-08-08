from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class OverlapGroupTagCheckTest(unittest.TestCase):
    """Each capability-registry.json resource carries its own overlap_group
    string, separate from the membership list that actually governs router
    dedup behaviour in overlap-groups.json. The two silently disagreed for
    20 resources on this repo -- a prior group rename/consolidation
    (session-memory -> memory-and-knowledge, harness-methodology ->
    delivery-methodology, and others) never propagated back to each
    resource's own tag field, and two resources added in the same session
    that introduced this check inherited the staleness by copying an
    already-stale resource as a template. doctor now computes each
    resource's actual formal group membership and fails if its own tag
    disagrees."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-overlap-tag-")
        self.copy = Path(self.temp.name) / "repo"
        shutil.copytree(
            self.source, self.copy,
            ignore=shutil.ignore_patterns(".git", ".agent", "__pycache__", "*.pyc", "backups"),
        )
        self.escapement = self.copy / "scripts" / "escapement.py"
        self.registry_path = self.copy / "catalog" / "capability-registry.json"

    def tearDown(self):
        self.temp.cleanup()

    def run_doctor(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.escapement), "doctor", "--root", str(self.copy)],
            cwd=self.copy, text=True, capture_output=True, check=False,
        )

    def test_unmodified_copy_reports_no_drift(self) -> None:
        result = self.run_doctor()
        self.assertIn("[PASS] overlap_group tags match formal group membership", result.stdout)

    def test_stale_tag_is_detected(self) -> None:
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        resource = next(r for r in registry["resources"] if r["id"] == "ponytail")
        resource["overlap_group"] = "deliberately-wrong"
        self.registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        result = self.run_doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("overlap_group tags drifted from formal group membership", result.stdout)
        self.assertIn("ponytail: overlap_group tag 'deliberately-wrong'", result.stdout)
        self.assertIn("engineering-behaviour", result.stdout)

    def test_resource_with_no_formal_membership_is_not_flagged(self) -> None:
        # A resource that isn't a member of any formal group has nothing
        # to be inconsistent with -- its tag is purely informational and
        # must not be reported as drifted just because it exists.
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        groups = json.loads((self.copy / "catalog" / "overlap-groups.json").read_text(encoding="utf-8"))
        all_members = {m for g in groups["groups"] for m in g["members"]}
        unaffiliated = next(r for r in registry["resources"] if r["id"] not in all_members)
        unaffiliated["overlap_group"] = "anything-at-all-unaffiliated"
        self.registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        result = self.run_doctor()
        self.assertIn("[PASS] overlap_group tags match formal group membership", result.stdout)


if __name__ == "__main__":
    unittest.main()
