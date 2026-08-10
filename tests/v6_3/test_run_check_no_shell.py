"""run_check.py used to accept `--shell "<string>"` and hand it to subprocess
with shell=True. Its only caller passed the `verification` command out of
feature_list.json -- a file the agent writes -- so a model-authored string
reached a shell, guarded by nothing but the word "trusted" in the argparse
help text. The effect surface audit found it; these tests keep it gone."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN_CHECK = ROOT / "scripts" / "run_check.py"
FEATURE_LIST = ROOT / "scripts" / "feature_list.py"


def run_check(*argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUN_CHECK), *argv],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )


class NoShellExecutionTest(unittest.TestCase):
    def test_shell_flag_no_longer_exists(self) -> None:
        result = run_check("--name", "x", "--shell", "echo hello")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unrecognized arguments: --shell", result.stderr)

    def test_no_source_file_passes_shell_true(self) -> None:
        for script in (RUN_CHECK, FEATURE_LIST):
            source = script.read_text(encoding="utf-8")
            for line in source.splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue  # the explanatory comments name it deliberately
                self.assertNotIn("shell=True", stripped, f"{script.name}: {stripped}")

    def test_argv_command_runs_and_records_evidence(self) -> None:
        result = run_check("--name", "argv-ok", "--", sys.executable, "-c", "print(1)")
        self.assertEqual(result.returncode, 0)
        record = json.loads((ROOT / result.stdout.strip()).read_text(encoding="utf-8"))
        self.assertEqual(record["result"], "PASS")

    def test_metacharacters_are_arguments_not_operators(self) -> None:
        """The whole point: `;` reaches the program as a literal argument
        instead of terminating a command and starting another one."""
        marker = "pwned-marker"
        result = run_check(
            "--name", "meta", "--",
            sys.executable, "-c", "import sys; print(sys.argv[1:])",
            f"; echo {marker}",
        )
        record = json.loads((ROOT / result.stdout.strip()).read_text(encoding="utf-8"))
        stdout = (ROOT / record["stdout_path"]).read_text(encoding="utf-8")
        self.assertIn(marker, stdout)          # present, as a quoted argument
        self.assertIn("; echo", stdout)        # still one string, not executed

    def test_missing_binary_records_a_failure_instead_of_raising(self) -> None:
        """Without a shell nothing converts "command not found" into an exit
        status. A check that could not run must still leave evidence."""
        result = run_check("--name", "missing", "--", "definitely-not-a-real-binary")
        self.assertEqual(result.returncode, 127)
        record = json.loads((ROOT / result.stdout.strip()).read_text(encoding="utf-8"))
        self.assertEqual(record["result"], "FAIL")
        self.assertEqual(record["exit_code"], 127)


class FeatureListRejectsShellSyntaxTest(unittest.TestCase):
    def test_metacharacter_commands_are_rejected(self) -> None:
        source = FEATURE_LIST.read_text(encoding="utf-8")
        self.assertIn("SHELL_METACHARACTERS", source)
        self.assertIn("shlex.split", source)
        self.assertNotIn('"--shell"', source)

    def test_rejected_characters_cover_the_operators_that_matter(self) -> None:
        namespace: dict[str, object] = {}
        for line in FEATURE_LIST.read_text(encoding="utf-8").splitlines():
            if line.startswith("SHELL_METACHARACTERS"):
                exec(line, namespace)  # noqa: S102 - reading our own constant
                break
        rejected = set(namespace["SHELL_METACHARACTERS"])  # type: ignore[arg-type]
        for character in (";", "|", "&", "$", "`", ">", "<", "\n", "\r"):
            self.assertIn(character, rejected)


if __name__ == "__main__":
    unittest.main()
