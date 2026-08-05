#!/usr/bin/env python3
"""Executable and resumable Escapement router evaluation harness."""

from __future__ import annotations

import argparse
import hashlib
import json
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
sys.path.insert(0, str(ROOT / "scripts"))
from agent_runtime import route_prompt  # noqa: E402

RESULTS = ROOT / ".agent" / "evals" / "results.ndjson"


def stable_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"eval:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:32]}"


def load_suites() -> list[dict[str, Any]]:
    suites: list[dict[str, Any]] = []
    for path in sorted((ROOT / "evals").rglob("evals.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("evals"), list):
            raise SystemExit(f"FAIL: invalid eval suite {path}")
        data["_path"] = str(path.relative_to(ROOT)).replace("\\", "/")
        suites.append(data)
    if not suites:
        raise SystemExit("FAIL: no eval suites found.")
    return suites


def read_completed() -> set[str]:
    completed: set[str] = set()
    if not RESULTS.exists():
        return completed
    for raw in RESULTS.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if record.get("result") == "PASS":
            completed.add(str(record.get("eval_id")))
    return completed


def evaluate(case: dict[str, Any], suite_name: str, suite_path: str) -> dict[str, Any]:
    prompt = str(case.get("prompt") or "")
    route = route_prompt(prompt)
    expected = case.get("expected", {})
    failures: list[str] = []

    if route["material"] != bool(expected.get("material")):
        failures.append(
            f"material expected {expected.get('material')} got {route['material']}"
        )

    expected_mode = expected.get("mode")
    if expected_mode and route["mode"] != expected_mode:
        failures.append(f"mode expected {expected_mode} got {route['mode']}")

    required_skills = set(expected.get("skills", []))
    actual_skills = set(route["skills"])
    missing = sorted(required_skills - actual_skills)
    if missing:
        failures.append(f"missing skills {missing}")

    forbidden = sorted(set(expected.get("forbidden_skills", [])) & actual_skills)
    if forbidden:
        failures.append(f"forbidden skills selected {forbidden}")

    maximum_skills = expected.get("maximum_skills")
    if maximum_skills is not None and len(route["skills"]) > int(maximum_skills):
        failures.append(
            f"skill budget expected <= {maximum_skills} got {len(route['skills'])}"
        )

    expected_reads = set(expected.get("required_reads", []))
    missing_reads = sorted(expected_reads - set(route["required_reads"]))
    if missing_reads:
        failures.append(f"missing required reads {missing_reads}")

    identity = {
        "suite": suite_name,
        "suite_path": suite_path,
        "case_id": case.get("id"),
        "prompt": prompt,
        "expected": expected,
    }
    eval_id = stable_id(identity)
    return {
        "record_type": "eval",
        "record_id": stable_id({
            **identity,
            "route": route,
            "failures": failures,
        }),
        "schema_version": "1.0",
        "eval_id": eval_id,
        "suite": suite_name,
        "suite_path": suite_path,
        "case_id": case.get("id"),
        "description": case.get("description"),
        "prompt": prompt,
        "expected": expected,
        "actual": route,
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
        "timestamp": utc_now(),
    }


def command_list(_: argparse.Namespace) -> int:
    for suite in load_suites():
        print(f"{suite.get('name')}: {len(suite['evals'])} cases | {suite['_path']}")
    return 0


def command_run(args: argparse.Namespace) -> int:
    suites = load_suites()
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    completed = read_completed() if args.resume else set()
    total = 0
    passed = 0
    failed = 0
    skipped = 0

    with RESULTS.open("a", encoding="utf-8") as handle:
        for suite in suites:
            suite_name = str(suite.get("name") or Path(suite["_path"]).parent.name)
            if args.suite and suite_name != args.suite:
                continue
            for case in suite["evals"]:
                record = evaluate(case, suite_name, suite["_path"])
                if record["eval_id"] in completed:
                    skipped += 1
                    continue
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                handle.flush()
                total += 1
                if record["result"] == "PASS":
                    passed += 1
                    print(f"PASS {suite_name}/{case.get('id')}")
                else:
                    failed += 1
                    print(
                        f"FAIL {suite_name}/{case.get('id')}: "
                        + "; ".join(record["failures"])
                    )
                if args.fail_fast and record["result"] == "FAIL":
                    break
            if args.fail_fast and failed:
                break

    summary = {
        "run_at": utc_now(),
        "executed": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "results": str(RESULTS.relative_to(ROOT)).replace("\\", "/"),
    }
    summary_path = RESULTS.parent / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 1 if failed else 0


def command_clean(_: argparse.Namespace) -> int:
    RESULTS.unlink(missing_ok=True)
    (RESULTS.parent / "summary.json").unlink(missing_ok=True)
    print("Evaluation results cleared.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eval_harness")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list").set_defaults(func=command_list)

    run = sub.add_parser("run")
    run.add_argument("--suite")
    run.add_argument("--resume", action="store_true")
    run.add_argument("--fail-fast", action="store_true")
    run.set_defaults(func=command_run)

    sub.add_parser("clean").set_defaults(func=command_clean)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
