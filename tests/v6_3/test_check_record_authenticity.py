from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_record_id(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"check:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:32]}"


class CheckRecordAuthenticityTest(unittest.TestCase):
    """A hand-written check record that never actually ran must not be able to
    close a turn as PASS. Found via adversarial testing: the original
    load_checks() only verified 5 shallow key names were present, so any JSON
    file claiming exit_code 0 / result PASS was accepted without proof a
    command was ever executed."""

    def setUp(self):
        self.source = Path(__file__).resolve().parents[2]
        self.temp = tempfile.TemporaryDirectory(prefix="esc-check-auth-")
        self.target = Path(self.temp.name) / "project"
        install = subprocess.run(
            [sys.executable, str(self.source / "scripts/escapement.py"), "init", str(self.target)],
            cwd=self.source, text=True, capture_output=True, check=False,
        )
        self.assertEqual(install.returncode, 0, install.stderr)
        self.runtime = self.target / "scripts/agent_runtime.py"
        self.run_check_script = self.target / "scripts/run_check.py"

    def tearDown(self):
        self.temp.cleanup()

    def run_runtime(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.runtime), *args],
            cwd=self.target, text=True, capture_output=True, check=False,
        )

    def open_micro_turn(self) -> None:
        start = self.run_runtime(
            "manual-start",
            "--prompt", "Fix the isolated login typo, simplest possible fix",
            "--json",
        )
        self.assertEqual(start.returncode, 0, start.stderr)
        self.assertEqual(json.loads(start.stdout)["tier"], "MICRO")

    def test_hand_written_record_with_missing_fields_is_rejected(self) -> None:
        self.open_micro_turn()
        evidence = self.target / ".agent/evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        forged = evidence / "forged.json"
        forged.write_text(json.dumps({
            "record_type": "check",
            "name": "fabricated-check-i-never-ran",
            "command": ["echo", "never executed"],
            "exit_code": 0,
            "result": "PASS",
        }), encoding="utf-8")

        close = self.run_runtime(
            "close-turn", "--summary", "Fixed it", "--next", "None",
            "--skills-used", "", "--check-records", ".agent/evidence/forged.json",
            "--result", "PASS",
        )
        self.assertNotEqual(close.returncode, 0)
        self.assertIn("incomplete check record", close.stderr)

    def test_record_with_fabricated_output_hash_is_rejected(self) -> None:
        """All 13 required fields present, but the stdout/stderr hashes are made up
        rather than matching real captured output -- the shape of the record a
        careless-but-not-determined forger would produce."""
        self.open_micro_turn()
        evidence = self.target / ".agent/evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        (evidence / "stdout.txt").write_text("fake output\n", encoding="utf-8")
        (evidence / "stderr.txt").write_text("", encoding="utf-8")
        forged = evidence / "forged.json"
        forged.write_text(json.dumps({
            "record_type": "check",
            "record_id": "check:" + "0" * 32,
            "schema_version": "1.0",
            "name": "fabricated-check-i-never-ran",
            "command": ["echo", "never executed"],
            "started_at": "2026-08-05T00:00:00+00:00",
            "completed_at": "2026-08-05T00:00:01+00:00",
            "exit_code": 0,
            "result": "PASS",
            "stdout_path": ".agent/evidence/stdout.txt",
            "stderr_path": ".agent/evidence/stderr.txt",
            "stdout_sha256": "0" * 64,
            "stderr_sha256": "0" * 64,
        }), encoding="utf-8")

        close = self.run_runtime(
            "close-turn", "--summary", "Fixed it", "--next", "None",
            "--skills-used", "", "--check-records", ".agent/evidence/forged.json",
            "--result", "PASS",
        )
        self.assertNotEqual(close.returncode, 0)
        self.assertIn("does not match its recorded hash", close.stderr)

    def test_record_with_correct_hashes_but_forged_record_id_is_rejected(self) -> None:
        """The output hashes are real (computed from real files), but the
        record_id -- the tamper-evidence binding those hashes to a specific
        name/command/timing -- was not recomputed to match. This is the
        component that stops a forged record from being silently reattributed
        to a different command or outcome after the fact."""
        self.open_micro_turn()
        evidence = self.target / ".agent/evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        stdout_path = evidence / "stdout.txt"
        stderr_path = evidence / "stderr.txt"
        stdout_path.write_text("genuinely captured output\n", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")

        forged = evidence / "forged.json"
        forged.write_text(json.dumps({
            "record_type": "check",
            "record_id": "check:" + "a" * 32,  # not recomputed from the identity below
            "schema_version": "1.0",
            "name": "claimed-check",
            "command": ["pytest"],
            "started_at": "2026-08-05T00:00:00+00:00",
            "completed_at": "2026-08-05T00:00:01+00:00",
            "exit_code": 0,
            "result": "PASS",
            "stdout_path": ".agent/evidence/stdout.txt",
            "stderr_path": ".agent/evidence/stderr.txt",
            "stdout_sha256": sha256_bytes(stdout_path.read_bytes()),
            "stderr_sha256": sha256_bytes(stderr_path.read_bytes()),
        }), encoding="utf-8")

        close = self.run_runtime(
            "close-turn", "--summary", "Fixed it", "--next", "None",
            "--skills-used", "", "--check-records", ".agent/evidence/forged.json",
            "--result", "PASS",
        )
        self.assertNotEqual(close.returncode, 0)
        self.assertIn("forged or tampered", close.stderr)

    def test_genuine_run_check_record_is_accepted(self) -> None:
        """A real record.json produced by run_check.py must still close a turn as
        PASS -- the fix must reject forgeries without breaking the legitimate path."""
        self.open_micro_turn()
        check = subprocess.run(
            [sys.executable, str(self.run_check_script), "--name", "real-check",
             "--", sys.executable, "-c", "print('genuinely ran')"],
            cwd=self.target, text=True, capture_output=True, check=False,
        )
        self.assertEqual(check.returncode, 0, check.stderr)
        record_path = check.stdout.strip()

        close = self.run_runtime(
            "close-turn", "--summary", "Fixed it", "--next", "None",
            "--skills-used", "", "--check-records", record_path,
            "--result", "PASS",
        )
        self.assertEqual(close.returncode, 0, close.stderr)


if __name__ == "__main__":
    unittest.main()
