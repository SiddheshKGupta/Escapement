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
from capability_router import route_prompt  # noqa: E402

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
    phase_override = case.get("phase_override")
    route = route_prompt(prompt, phase_override=phase_override)
    expected = case.get("expected", {})
    failures: list[str] = []

    if route["material"] != bool(expected.get("material")):
        failures.append(
            f"material expected {expected.get('material')} got {route['material']}"
        )

    for key in ("tier", "mode", "register", "profile", "current_phase"):
        value = expected.get(key)
        if value and route.get(key) != value:
            failures.append(f"{key} expected {value} got {route.get(key)}")

    actual_skills = {item["id"] for item in route.get("native_skills", [])}
    required_skills = set(expected.get("skills", []))
    missing = sorted(required_skills - actual_skills)
    if missing:
        failures.append(f"missing skills {missing}")

    forbidden = sorted(set(expected.get("forbidden_skills", [])) & actual_skills)
    if forbidden:
        failures.append(f"forbidden skills selected {forbidden}")

    maximum_skills = expected.get("maximum_skills")
    if maximum_skills is not None and len(actual_skills) > int(maximum_skills):
        failures.append(
            f"skill budget expected <= {maximum_skills} got {len(actual_skills)}"
        )

    actual_packs = {item["id"] for item in route.get("doctrine_packs", [])}
    required_packs = set(expected.get("packs", []))
    missing_packs = sorted(required_packs - actual_packs)
    if missing_packs:
        failures.append(f"missing packs {missing_packs}")

    forbidden_packs = sorted(set(expected.get("forbidden_packs", [])) & actual_packs)
    if forbidden_packs:
        failures.append(f"forbidden packs selected {forbidden_packs}")

    maximum_packs = expected.get("maximum_packs")
    if maximum_packs is not None and len(actual_packs) > int(maximum_packs):
        failures.append(
            f"pack budget expected <= {maximum_packs} got {len(actual_packs)}"
        )

    maximum_context = expected.get("maximum_context_words")
    actual_context = int(route.get("context_cost", {}).get("total", 0))
    if maximum_context is not None and actual_context > int(maximum_context):
        failures.append(
            f"context expected <= {maximum_context} got {actual_context}"
        )

    required_external = set(expected.get("external_candidates", []))
    actual_external = {
        item["id"] for item in route.get("external_candidates", [])
    }
    missing_external = sorted(required_external - actual_external)
    if missing_external:
        failures.append(f"missing external candidates {missing_external}")

    forbidden_external = sorted(
        set(expected.get("forbidden_external_candidates", [])) & actual_external
    )
    if forbidden_external:
        failures.append(f"forbidden external candidates selected {forbidden_external}")

    # A licence gate is only worth having if it is asserted. Maps a candidate
    # id to its expected adoption gate; null asserts the absence of one.
    actual_adoption = {
        item["id"]: item.get("adoption")
        for item in route.get("external_candidates", [])
    }
    for candidate, expected_gate in expected.get("external_adoption", {}).items():
        if candidate not in actual_adoption:
            failures.append(f"adoption gate uncheckable, {candidate} not routed")
        elif actual_adoption[candidate] != expected_gate:
            failures.append(
                f"{candidate} adoption gate is {actual_adoption[candidate]!r}, "
                f"expected {expected_gate!r}"
            )

    # A displaced SUBSTITUTE member should be demoted to a fallback on the
    # winner, not dropped. Maps a winning candidate to the fallbacks it must
    # carry, so the chain is asserted rather than assumed.
    actual_fallbacks = {
        item["id"]: [f["id"] for f in item.get("fallbacks", [])]
        for item in route.get("external_candidates", [])
    }
    for winner, expected_chain in expected.get("external_fallbacks", {}).items():
        if winner not in actual_fallbacks:
            failures.append(f"fallback chain uncheckable, {winner} not routed")
        elif actual_fallbacks[winner] != list(expected_chain):
            failures.append(
                f"{winner} fallbacks are {actual_fallbacks[winner]}, "
                f"expected {list(expected_chain)}"
            )

    actual_strengths = {
        item["id"] for item in route.get("capability_strengths", [])
    }
    required_strengths = set(expected.get("strengths", []))
    missing_strengths = sorted(required_strengths - actual_strengths)
    if missing_strengths:
        failures.append(f"missing capability strengths {missing_strengths}")

    forbidden_strengths = sorted(
        set(expected.get("forbidden_strengths", [])) & actual_strengths
    )
    if forbidden_strengths:
        failures.append(
            f"forbidden capability strengths selected {forbidden_strengths}"
        )

    maximum_strengths = expected.get("maximum_strengths")
    if maximum_strengths is not None and len(actual_strengths) > int(maximum_strengths):
        failures.append(
            f"strength budget expected <= {maximum_strengths} "
            f"got {len(actual_strengths)}"
        )

    context_cost = route.get("context_cost", {})
    maximum_skill_context = expected.get("maximum_skill_context_words")
    actual_skill_context = int(context_cost.get("invoked_skill_total", 0))
    if (
        maximum_skill_context is not None
        and actual_skill_context > int(maximum_skill_context)
    ):
        failures.append(
            f"skill context expected <= {maximum_skill_context} "
            f"got {actual_skill_context}"
        )

    expected_design_authority = expected.get("design_authority")
    actual_design_authority = (
        "design-intelligence:constitution" in actual_strengths
    )
    if (
        expected_design_authority is not None
        and actual_design_authority != bool(expected_design_authority)
    ):
        failures.append(
            f"design authority expected {expected_design_authority} "
            f"got {actual_design_authority}"
        )

    required_research_sources = set(expected.get("research_sources", []))
    actual_research_sources = set(
        route.get("research_plan", {}).get("sources", [])
    )
    missing_research_sources = sorted(
        required_research_sources - actual_research_sources
    )
    if missing_research_sources:
        failures.append(
            f"missing research sources {missing_research_sources}"
        )

    # decision_brief.questions was previously unchecked entirely -- there was
    # no way to assert "the ambiguity in this prompt actually gets asked
    # about", which is exactly what an ambiguity-trap case needs to verify.
    actual_questions = {
        item["id"] for item in route.get("decision_brief", {}).get("questions", [])
    }
    required_questions = set(expected.get("questions_include", []))
    missing_questions = sorted(required_questions - actual_questions)
    if missing_questions:
        failures.append(f"missing material questions {missing_questions}")

    forbidden_questions = sorted(
        set(expected.get("questions_exclude", [])) & actual_questions
    )
    if forbidden_questions:
        failures.append(f"unexpected material questions asked {forbidden_questions}")

    identity = {
        "suite": suite_name,
        "suite_path": suite_path,
        "case_id": case.get("id"),
        "phase_override": case.get("phase_override"),
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
        "schema_version": "3.0",
        "eval_id": eval_id,
        "suite": suite_name,
        "suite_path": suite_path,
        "case_id": case.get("id"),
        "description": case.get("description"),
        "claim": case.get("claim"),
        "category": case.get("category"),
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
