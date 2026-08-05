#!/usr/bin/env python3
"""Machine-controlled feature list and verification state transitions."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_root() -> Path:
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()
FEATURE_FILE = ROOT / "feature_list.json"
ALLOWED = {"not_started", "active", "blocked", "passing"}


def load() -> dict[str, Any]:
    if not FEATURE_FILE.exists():
        raise SystemExit("FAIL: feature_list.json is missing.")
    value = json.loads(FEATURE_FILE.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("features"), list):
        raise SystemExit("FAIL: invalid feature_list.json.")
    return value


def save(value: dict[str, Any]) -> None:
    value["updated_at"] = utc_now()
    FEATURE_FILE.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def feature_by_id(value: dict[str, Any], feature_id: str) -> dict[str, Any]:
    for feature in value["features"]:
        if feature.get("id") == feature_id:
            return feature
    raise SystemExit(f"FAIL: unknown feature {feature_id}")


def dependency_failures(value: dict[str, Any], feature: dict[str, Any]) -> list[str]:
    failures = []
    for dependency in feature.get("dependencies", []):
        dep = feature_by_id(value, dependency)
        if dep.get("state") != "passing":
            failures.append(dependency)
    return failures


def command_list(_: argparse.Namespace) -> int:
    value = load()
    for feature in value["features"]:
        required = "required" if feature.get("required", True) else "optional"
        print(
            f"{feature.get('id')}: {feature.get('state')} | {required} | "
            f"{feature.get('behavior')}"
        )
    return 0


def command_next(_: argparse.Namespace) -> int:
    value = load()
    active = [f for f in value["features"] if f.get("state") == "active"]
    if active:
        print(active[0]["id"])
        return 0
    for feature in value["features"]:
        if feature.get("state") == "not_started" and not dependency_failures(value, feature):
            print(feature["id"])
            return 0
    blocked = [f for f in value["features"] if f.get("state") == "blocked"]
    if blocked:
        print(f"BLOCKED {blocked[0]['id']}")
        return 1
    print("COMPLETE")
    return 0


def command_activate(args: argparse.Namespace) -> int:
    value = load()
    feature = feature_by_id(value, args.feature_id)
    if feature.get("state") == "passing":
        print("Feature is already passing and cannot be reopened automatically.")
        return 1
    failures = dependency_failures(value, feature)
    if failures:
        print(f"FAIL: dependencies not passing: {', '.join(failures)}")
        return 1

    for item in value["features"]:
        if item.get("state") == "active" and item.get("id") != args.feature_id:
            print(f"FAIL: {item['id']} is already active.")
            return 1
    feature["state"] = "active"
    feature["activated_at"] = utc_now()
    feature["blocked_reason"] = None
    save(value)
    print(f"Activated {args.feature_id}")
    return 0


def command_block(args: argparse.Namespace) -> int:
    value = load()
    feature = feature_by_id(value, args.feature_id)
    if feature.get("state") == "passing":
        print("FAIL: a passing feature cannot be blocked.")
        return 1
    feature["state"] = "blocked"
    feature["blocked_reason"] = args.reason
    feature["blocked_at"] = utc_now()
    save(value)
    print(f"Blocked {args.feature_id}")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    value = load()
    feature = feature_by_id(value, args.feature_id)
    if feature.get("state") == "passing":
        print(f"{args.feature_id} already passing.")
        return 0
    if feature.get("state") not in {"active", "blocked"}:
        print("FAIL: activate the feature before verification.")
        return 1

    command = str(feature.get("verification") or "").strip()
    if not command:
        print("FAIL: feature has no verification command.")
        return 1

    runner = ROOT / "scripts" / "run_check.py"
    process = subprocess.run(
        [
            sys.executable,
            str(runner),
            "--name",
            f"feature-{args.feature_id}",
            "--scope",
            f"feature:{args.feature_id}",
            "--shell",
            command,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.stdout:
        print(process.stdout.strip())
    if process.stderr:
        print(process.stderr.strip(), file=sys.stderr)

    if process.returncode != 0:
        feature["state"] = "blocked" if args.block_on_failure else "active"
        feature["last_verification_result"] = "FAIL"
        feature["last_verified_at"] = utc_now()
        save(value)
        return process.returncode

    record_path = process.stdout.strip().splitlines()[-1]
    feature["state"] = "passing"
    feature["last_verification_result"] = "PASS"
    feature["last_verified_at"] = utc_now()
    feature.setdefault("evidence", []).append(record_path)
    save(value)
    print(f"Passed {args.feature_id}")
    return 0


def command_check(_: argparse.Namespace) -> int:
    value = load()
    failures = 0
    ids = set()
    for feature in value["features"]:
        feature_id = feature.get("id")
        if not feature_id or feature_id in ids:
            print(f"FAIL duplicate/missing feature id: {feature_id}")
            failures += 1
        ids.add(feature_id)
        if feature.get("state") not in ALLOWED:
            print(f"FAIL {feature_id}: invalid state {feature.get('state')}")
            failures += 1
        if not str(feature.get("behavior") or "").strip():
            print(f"FAIL {feature_id}: missing behavior")
            failures += 1
        if not str(feature.get("verification") or "").strip():
            print(f"FAIL {feature_id}: missing verification")
            failures += 1
    for feature in value["features"]:
        for dep in feature.get("dependencies", []):
            if dep not in ids:
                print(f"FAIL {feature.get('id')}: unknown dependency {dep}")
                failures += 1
    print(f"Failures: {failures}")
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="feature_list")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list").set_defaults(func=command_list)
    sub.add_parser("next").set_defaults(func=command_next)
    sub.add_parser("check").set_defaults(func=command_check)

    activate = sub.add_parser("activate")
    activate.add_argument("feature_id")
    activate.set_defaults(func=command_activate)

    block = sub.add_parser("block")
    block.add_argument("feature_id")
    block.add_argument("--reason", required=True)
    block.set_defaults(func=command_block)

    verify = sub.add_parser("verify")
    verify.add_argument("feature_id")
    verify.add_argument("--block-on-failure", action="store_true")
    verify.set_defaults(func=command_verify)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
