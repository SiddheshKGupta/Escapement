from __future__ import annotations

from copy import deepcopy
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from capability_router import route_prompt  # noqa: E402
from codex_resources import (  # noqa: E402
    FIVE_HOUR_WINDOW_MINS,
    apply_resource_policy,
    assess_resource_policy,
    load_resource_state,
    normalize_resource_snapshot,
    query_resource_state,
    write_resource_state,
)


def rate_result(used_percent: float, resets_at: int = 1_700_000_600) -> dict:
    return {
        "rateLimits": {
            "limitId": "codex",
            "primary": {
                "usedPercent": used_percent,
                "windowDurationMins": FIVE_HOUR_WINDOW_MINS,
                "resetsAt": resets_at,
            },
            "secondary": {
                "usedPercent": 20,
                "windowDurationMins": 10_080,
                "resetsAt": 1_700_600_000,
            },
            "rateLimitReachedType": None,
        }
    }


class CodexResourceStateTest(unittest.TestCase):
    def snapshot(self, used_percent: float, resets_at: int = 1_700_000_600) -> dict:
        return normalize_resource_snapshot(
            rate_result(used_percent, resets_at),
            {"summary": {"lifetimeTokens": 1234}, "dailyUsageBuckets": []},
            source="FIXTURE",
            observed_at="2023-11-14T22:13:20+00:00",
        )

    def test_five_hour_window_is_identified_without_conflating_token_activity(self):
        state = self.snapshot(82)
        self.assertEqual(len(state["five_hour_windows"]), 1)
        window = state["five_hour_windows"][0]
        self.assertEqual(window["window_duration_mins"], 300)
        self.assertEqual(window["used_percent"], 82)
        self.assertEqual(state["usage"]["summary"]["lifetimeTokens"], 1234)
        self.assertNotIn("remainingTokens", window)

    def test_policy_uses_advisory_warning_bands(self):
        expected = [
            (74, "NORMAL", "normal-execution"),
            (75, "CONSERVE", "warn-user-75-percent"),
            (89, "CONSERVE", "warn-user-75-percent"),
            (90, "CONVERGE", "warn-user-90-percent"),
            (99, "CONVERGE", "warn-user-90-percent"),
            (100, "EXHAUSTED", "warn-user-100-percent"),
            (101, "EXHAUSTED", "warn-user-100-percent"),
        ]
        for used, mode, action in expected:
            with self.subTest(used=used):
                policy = assess_resource_policy(
                    self.snapshot(used), now_epoch=1_700_000_000
                )
                self.assertEqual(policy["mode"], mode)
                self.assertEqual(policy["action"], action)
                self.assertFalse(policy["block_new_turn"])

    def test_expired_window_is_stale_and_cannot_block(self):
        policy = assess_resource_policy(
            self.snapshot(100, resets_at=1_699_999_999),
            now_epoch=1_700_000_000,
        )
        self.assertEqual(policy["mode"], "STALE")
        self.assertTrue(policy["needs_refresh"])
        self.assertFalse(policy["block_new_turn"])

    def test_non_five_hour_window_never_governs_policy(self):
        state = {
            "windows": [{
                "limit_id": "codex",
                "bucket": "secondary",
                "used_percent": 100,
                "window_duration_mins": 10_080,
                "resets_at": 1_700_600_000,
            }],
            "five_hour_windows": [],
        }
        policy = assess_resource_policy(state, now_epoch=1_700_000_000)
        self.assertEqual(policy["mode"], "UNOBSERVED")
        self.assertTrue(policy["needs_refresh"])
        self.assertFalse(policy["block_new_turn"])

    def test_malformed_five_hour_window_is_unobserved(self):
        malformed = self.snapshot(82)
        del malformed["five_hour_windows"][0]["bucket"]

        self.assertEqual(
            assess_resource_policy(malformed, now_epoch=1_700_000_000)["mode"],
            "UNOBSERVED",
        )

    def test_load_rejects_malformed_persisted_window(self):
        malformed = self.snapshot(82)
        del malformed["five_hour_windows"][0]["bucket"]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state.json"
            path.write_text(json.dumps(malformed), encoding="utf-8")

            self.assertIsNone(load_resource_state(path))

    def test_load_rejects_non_utf8_persisted_state(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state.json"
            path.write_bytes(b"\xff\xfe\x00")

            self.assertIsNone(load_resource_state(path))

    def test_warning_policy_only_attaches_resource_policy(self):
        baseline = route_prompt(
            "Build a four-module claims-management platform containing intake, "
            "assessment, approval, and reporting.",
            phase_override="DISCOVER",
        )
        for used in (75, 90, 100):
            with self.subTest(used=used):
                route = deepcopy(baseline)
                original = deepcopy(route)
                policy = assess_resource_policy(
                    self.snapshot(used), now_epoch=1_700_000_000
                )
                apply_resource_policy(route, policy)
                self.assertEqual(route.pop("resource_policy"), policy)
                self.assertEqual(route, original)

    def test_state_persistence_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "codex-resources.json"
            state = self.snapshot(82)
            write_resource_state(path, state)
            self.assertEqual(load_resource_state(path), state)

    def test_jsonl_app_server_contract_reads_limits_and_usage(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture = root / "fixture_server.py"
            fixture.write_text(
                textwrap.dedent(
                    """
                    import json
                    import sys

                    for line in sys.stdin:
                        message = json.loads(line)
                        method = message.get("method")
                        if method == "initialize":
                            print(json.dumps({"id": message["id"], "result": {"userAgent": "fixture"}}), flush=True)
                        elif method == "account/rateLimits/read":
                            result = {
                                "rateLimits": {
                                    "limitId": "codex",
                                    "primary": {"usedPercent": 81, "windowDurationMins": 300, "resetsAt": 1700000600},
                                    "secondary": None,
                                    "rateLimitReachedType": None,
                                }
                            }
                            print(json.dumps({"id": message["id"], "result": result}), flush=True)
                        elif method == "account/usage/read":
                            print(json.dumps({"method": "account/rateLimits/updated", "params": {
                                "rateLimits": {
                                    "limitId": "codex",
                                    "primary": {"usedPercent": 88, "windowDurationMins": 300, "resetsAt": 1700000600},
                                    "secondary": None,
                                    "rateLimitReachedType": None,
                                }
                            }}), flush=True)
                            print(json.dumps({"id": message["id"], "result": {"summary": {"lifetimeTokens": 99}}}), flush=True)
                    """
                ),
                encoding="utf-8",
            )
            state = query_resource_state(
                [sys.executable, str(fixture)],
                source="FIXTURE",
                timeout_seconds=5,
            )
            self.assertEqual(state["source"], "FIXTURE")
            self.assertEqual(state["five_hour_windows"][0]["used_percent"], 88)
            self.assertEqual(state["usage"]["summary"]["lifetimeTokens"], 99)

    def test_jsonl_app_server_drains_large_stderr_before_processing_requests(self):
        """Fails if App Server stderr is not drained while requests are pending."""
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "app_server.py"
            fixture.write_text(
                textwrap.dedent(
                    """
                    import json
                    import sys

                    sys.stderr.write("x" * (1024 * 1024))
                    sys.stderr.flush()
                    for line in sys.stdin:
                        message = json.loads(line)
                        method = message.get("method")
                        if method == "initialize":
                            result = {"userAgent": "fixture"}
                        elif method == "account/rateLimits/read":
                            result = {"rateLimits": {
                                "limitId": "codex",
                                "primary": {"usedPercent": 81, "windowDurationMins": 300,
                                            "resetsAt": 1700000600},
                                "secondary": None,
                            }}
                        elif method == "account/usage/read":
                            result = {"summary": {"lifetimeTokens": 99}}
                        else:
                            continue
                        print(json.dumps({"id": message["id"], "result": result}), flush=True)
                    """
                ),
                encoding="utf-8",
            )
            state = query_resource_state(
                [sys.executable, str(fixture)], source="FIXTURE", timeout_seconds=5
            )
            self.assertEqual(state["five_hour_windows"][0]["used_percent"], 81)
            self.assertEqual(state["usage"]["summary"]["lifetimeTokens"], 99)

    def test_main_cli_exposes_persisted_resource_status(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state.json"
            write_resource_state(path, self.snapshot(82, resets_at=4_102_444_800))
            process = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/escapement.py"),
                    "codex-resources",
                    "status",
                    "--state",
                    str(path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            value = json.loads(process.stdout)
            self.assertEqual(value["policy"]["mode"], "CONSERVE")


if __name__ == "__main__":
    unittest.main()
