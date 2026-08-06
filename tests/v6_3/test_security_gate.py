from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from security_gate import SECRET_PATTERNS, is_candidate  # noqa: E402

GENERIC_SECRET_PATTERN = next(p for name, _, p in SECRET_PATTERNS if name == "generic-secret-assignment")
ANTHROPIC_KEY_PATTERN = next(p for name, _, p in SECRET_PATTERNS if name == "anthropic-key")
OPENAI_KEY_PATTERN = next(p for name, _, p in SECRET_PATTERNS if name == "openai-key")


class GenericSecretPatternTest(unittest.TestCase):
    """Found via adversarial testing: the original pattern wrapped its keywords in
    \\b...\\b, so admin_password = "..." was silently missed -- an underscore is a
    word character, so there is no boundary between "admin_" and "password". Bare
    password = "..." matched; the far more common prefixed/compound convention did
    not."""

    # Fixture values use "fake" so they don't themselves trip security_gate.py's own
    # repository scan (it excludes lines containing fake/example/placeholder/redacted).
    def test_prefixed_identifiers_are_detected(self) -> None:
        cases = [
            'admin_password = "fake-Adm1nSecretValue2026"',
            'db_secret = "fake-Adm1nSecretValue2026"',
            'stripe_api_key = "fake-whatever12345"',
            'user_token: "fake-abcdefghijklmnop"',
            'DB_SECRET_KEY="fake-abcdefghijklmnop"',
        ]
        for line in cases:
            with self.subTest(line=line):
                self.assertIsNotNone(GENERIC_SECRET_PATTERN.search(line), f"missed: {line}")

    def test_bare_keywords_are_still_detected(self) -> None:
        for line in ['password = "fake-Adm1nSecretValue2026"', 'api_key = "fake-not-a-real-key-value"']:
            with self.subTest(line=line):
                self.assertIsNotNone(GENERIC_SECRET_PATTERN.search(line))

    def test_non_assignments_are_not_flagged(self) -> None:
        cases = [
            'password = "short"',
            'is_password_valid = check(x)',
            'passwordless_login = True',
        ]
        for line in cases:
            with self.subTest(line=line):
                self.assertIsNone(GENERIC_SECRET_PATTERN.search(line), f"false positive: {line}")


class AnthropicKeyLabelTest(unittest.TestCase):
    """Found while researching harness/context-engineering repos for
    suggestions: a framework built primarily for Claude Code had no
    dedicated pattern for Anthropic's own API key format. The generic
    openai-key pattern (bare \\bsk-...\\b) already matched sk-ant-... keys --
    the secret WAS caught, just mislabeled as an OpenAI key, which would
    misdirect whoever reviews the report about which credential to
    rotate."""

    def test_anthropic_key_is_labelled_correctly(self) -> None:
        line = 'ANTHROPIC_API_KEY="sk-ant-api03-fakeabcdefghijklmnopqrstuvwxyz1234567890"'
        self.assertIsNotNone(ANTHROPIC_KEY_PATTERN.search(line))

    def test_anthropic_key_no_longer_matches_openai_pattern(self) -> None:
        line = 'ANTHROPIC_API_KEY="sk-ant-api03-fakeabcdefghijklmnopqrstuvwxyz1234567890"'
        self.assertIsNone(OPENAI_KEY_PATTERN.search(line))

    def test_real_openai_key_still_matches_openai_pattern(self) -> None:
        line = 'OPENAI_API_KEY="sk-proj-fakeabcdefghijklmnopqrstuvwxyz1234567890"'
        self.assertIsNotNone(OPENAI_KEY_PATTERN.search(line))
        self.assertIsNone(ANTHROPIC_KEY_PATTERN.search(line))


class BackupExclusionTest(unittest.TestCase):
    """Found via real-world use: update/repair --force-managed back up the
    previous file under .escapement/backups/<timestamp>/ before overwriting.
    security_gate.py contains its own detection regexes as literal string
    content, so a backup copy of security_gate.py always matched its own
    powershell-download-exec pattern -- a deterministic false positive on
    every backup of this file, in every project that has ever run update or
    repair."""

    def test_backup_paths_are_excluded_from_scanning(self) -> None:
        path = Path(".escapement/backups/20260806T055347Z/scripts/security_gate.py")
        self.assertFalse(is_candidate(path))

    def test_ordinary_paths_are_still_scanned(self) -> None:
        path = Path("src/auth.py")
        self.assertTrue(is_candidate(path))


if __name__ == "__main__":
    unittest.main()
