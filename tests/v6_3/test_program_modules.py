from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ProgramModulesTest(unittest.TestCase):
    """A PROGRAM-tier build with several modules (billing, CRM core, admin
    portal) runs each module through its own DISCOVER->RELEASE cycle across
    many turns -- but a single turn's phase plan has no concept of "module",
    so nothing durable tracked that the modules exist or that they agreed
    on shared artifacts (schema, DESIGN.md, DOMAIN_CONTEXT.md) before
    diverging. program_modules.py is that missing registry, and its one
    enforced rule -- a module cannot leave SPECIFY until it has checked
    every registered shared artifact -- is what this test proves."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-modules-")
        self.target = Path(self.temp.name) / "project"
        install = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "init", str(self.target)],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)
        self.script = self.target / "scripts/program_modules.py"

    def tearDown(self):
        self.temp.cleanup()

    def run_modules(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            cwd=self.target, text=True, capture_output=True, check=False,
        )

    def registry(self) -> dict:
        return json.loads((self.target / "docs" / "PROGRAM_MODULES.json").read_text(encoding="utf-8"))

    def test_register_program_shared_artifacts_and_modules(self) -> None:
        self.assertEqual(self.run_modules("set-program", "--name", "CRM Platform").returncode, 0)
        self.assertEqual(self.run_modules("add-shared", "--path", "DESIGN.md").returncode, 0)
        self.assertEqual(self.run_modules("add-module", "--id", "billing", "--name", "Billing").returncode, 0)

        value = self.registry()
        self.assertEqual(value["program"], "CRM Platform")
        self.assertEqual(value["shared_artifacts"], ["DESIGN.md"])
        self.assertEqual(value["modules"][0]["id"], "billing")
        self.assertEqual(value["modules"][0]["status"], "not_started")

    def test_module_cannot_leave_specify_with_unchecked_shared_artifact(self) -> None:
        self.run_modules("add-shared", "--path", "DESIGN.md")
        self.run_modules("add-shared", "--path", "docs/specs/SCHEMA.md")
        self.run_modules("add-module", "--id", "billing", "--name", "Billing")

        result = self.run_modules("set-status", "--id", "billing", "--status", "plan")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must check shared artifacts", result.stderr)
        self.assertEqual(self.registry()["modules"][0]["status"], "not_started")

    def test_module_can_leave_specify_once_all_shared_artifacts_checked(self) -> None:
        self.run_modules("add-shared", "--path", "DESIGN.md")
        self.run_modules("add-shared", "--path", "docs/specs/SCHEMA.md")
        self.run_modules("add-module", "--id", "billing", "--name", "Billing")

        result = self.run_modules(
            "set-status", "--id", "billing", "--status", "plan",
            "--checked-shared", "DESIGN.md,docs/specs/SCHEMA.md",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.registry()["modules"][0]["status"], "plan")

    def test_module_cannot_leave_specify_while_dependency_not_done(self) -> None:
        self.run_modules("add-module", "--id", "billing", "--name", "Billing")
        self.run_modules("add-module", "--id", "portal", "--name", "Portal", "--depends-on", "billing")

        result = self.run_modules("set-status", "--id", "portal", "--status", "plan")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("billing is not done", result.stderr)

    def test_reset_requires_confirm(self) -> None:
        self.run_modules("set-program", "--name", "CRM Platform")
        result = self.run_modules("reset")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--confirm", result.stderr)
        self.assertEqual(self.registry()["program"], "CRM Platform")

    def test_reset_confirmed_clears_registry(self) -> None:
        self.run_modules("set-program", "--name", "CRM Platform")
        self.run_modules("add-module", "--id", "billing", "--name", "Billing")

        result = self.run_modules("reset", "--confirm")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.target / "docs" / "PROGRAM_MODULES.json").exists())

        listing = self.run_modules("list")
        self.assertIn("(unset)", listing.stdout)

    def test_unregistered_shared_artifact_is_rejected(self) -> None:
        self.run_modules("add-module", "--id", "billing", "--name", "Billing")
        result = self.run_modules(
            "set-status", "--id", "billing", "--status", "plan",
            "--checked-shared", "not-a-registered-artifact.md",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a registered shared artifact", result.stderr)


if __name__ == "__main__":
    unittest.main()
