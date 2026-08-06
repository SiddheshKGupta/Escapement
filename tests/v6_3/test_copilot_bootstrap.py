from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CopilotBootstrapTest(unittest.TestCase):
    """GitHub Copilot already reads AGENTS.md natively (GitHub Changelog,
    2025-08-28) -- so a Copilot host isn't missing a file to read. What it's
    missing is the automatic hook wiring Claude Code (.claude/settings.json)
    and Codex (.codex/hooks.json) have, which actually invoke
    agent_runtime.py. Without that, a host reads the kernel as static prose
    and never activates routing, phase-gating, or evidence at all -- exactly
    why results were bad on a host with no hook support. Fixed with an
    explicit "Host Bootstrap" section telling any such host to invoke the
    runtime itself, plus a .github/copilot-instructions.md pointer since
    some Copilot surfaces (VS Code) prioritize that file specifically."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-copilot-")
        self.target = Path(self.temp.name) / "project"
        install = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "init", str(self.target)],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)

    def tearDown(self):
        self.temp.cleanup()

    def test_init_creates_copilot_instructions_pointer(self):
        path = self.target / ".github" / "copilot-instructions.md"
        self.assertTrue(path.exists())
        content = path.read_text(encoding="utf-8")
        self.assertIn("AGENTS.md", content)
        self.assertIn("Host Bootstrap", content)

    def test_doctor_checks_for_copilot_instructions(self):
        result = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "doctor", "--root", str(self.target)],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertIn("[PASS] .github/copilot-instructions.md", result.stdout)

    def test_agents_md_has_host_bootstrap_section(self):
        content = (self.target / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## Host Bootstrap", content)
        self.assertIn("session-start", content)
        self.assertIn("stop", content)

    def test_agents_md_bootstrap_names_hosts_without_hook_wiring(self):
        content = (self.target / "AGENTS.md").read_text(encoding="utf-8")
        bootstrap_section = content.split("## Host Bootstrap")[1].split("##")[0]
        self.assertIn("Copilot", bootstrap_section)


if __name__ == "__main__":
    unittest.main()
