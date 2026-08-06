#!/usr/bin/env python3
"""Aggregates turns.jsonl and logs/skill-usage.jsonl into harness-health
trends.

Every turn already writes phase-advanced/phase-plan-revised/closure events
to .agent/runtime/turns.jsonl, and every closed turn writes one skill-usage
record per routed skill to logs/skill-usage.jsonl -- but nothing reads them
back as a trend. Same idea as security_gate.py/ui_quality_gate.py: a small
deterministic report over data that already exists, not a new logging
system.

Honest limitation: this only sees turns that were actually closed via
close-turn. A build done by writing code directly without ever closing a
runtime turn -- which is exactly the informal-operation pattern several
real findings this session traced back to -- leaves nothing here to
aggregate. An empty report is not proof the harness is healthy; it may
just mean turns aren't being closed.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def aggregate(root: Path) -> dict[str, Any]:
    turns = read_jsonl(root / ".agent" / "runtime" / "turns.jsonl")
    skill_runs = read_jsonl(root / "logs" / "skill-usage.jsonl")

    closed_turns = [t for t in turns if "closure" in t]
    replans = [t for t in turns if t.get("event") == "phase-plan-revised"]

    tier_counts = Counter(
        t["closure"]["tier"] for t in closed_turns if "tier" in t.get("closure", {})
    )
    result_counts = Counter(
        t["closure"]["result"] for t in closed_turns if "result" in t.get("closure", {})
    )
    replan_reasons = Counter(r.get("reason", "unspecified") for r in replans)

    selected_counts: Counter[str] = Counter()
    used_counts: Counter[str] = Counter()
    for run in skill_runs:
        skill = run.get("skill")
        if not skill:
            continue
        selected_counts[skill] += 1
        if run.get("used"):
            used_counts[skill] += 1

    routed_never_used = sorted(
        skill for skill in selected_counts if used_counts.get(skill, 0) == 0
    )

    rejection_reasons: Counter[str] = Counter()
    for turn in closed_turns:
        for item in turn.get("route", {}).get("rejected", []):
            reason = item.get("rejected_because")
            if reason:
                rejection_reasons[reason] += 1

    return {
        "schema_version": "1.0",
        "root": str(root),
        "turns_logged": len({t.get("turn_id") for t in turns if t.get("turn_id")}),
        "closed_turns": len(closed_turns),
        "tier_distribution": dict(tier_counts.most_common()),
        "closure_result_distribution": dict(result_counts.most_common()),
        "phase_replans": len(replans),
        "phase_replan_reasons": dict(replan_reasons.most_common()),
        "skill_selected_counts": dict(selected_counts.most_common()),
        "skill_routed_never_used": routed_never_used,
        "rejection_reasons": dict(rejection_reasons.most_common()),
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        "HARNESS OBSERVABILITY",
        f"Root: {report['root']}",
        "",
        f"Turns logged: {report['turns_logged']}",
        f"Closed turns: {report['closed_turns']}",
        "",
        "Tier distribution:",
    ]
    for tier, count in report["tier_distribution"].items():
        lines.append(f"  {tier}: {count}")

    lines += ["", "Closure result distribution:"]
    for result, count in report["closure_result_distribution"].items():
        lines.append(f"  {result}: {count}")

    lines += ["", f"Phase replans: {report['phase_replans']}"]
    for reason, count in report["phase_replan_reasons"].items():
        lines.append(f"  ({count}x) {reason}")

    lines += ["", "Skills routed but never marked used:"]
    if report["skill_routed_never_used"]:
        lines += [f"  {skill}" for skill in report["skill_routed_never_used"]]
    else:
        lines.append("  None")

    lines += ["", "Rejection reasons (overlap, budget, phase-skill-limit):"]
    if report["rejection_reasons"]:
        for reason, count in report["rejection_reasons"].items():
            lines.append(f"  {reason}: {count}")
    else:
        lines.append("  None")

    if report["closed_turns"] == 0:
        lines += [
            "",
            "No closed turns found -- either this is a fresh install, or work",
            "happened without ever running close-turn. An empty report here is",
            "not evidence of a healthy harness.",
        ]

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(prog="harness_observability")
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = aggregate(root)
    print(json.dumps(report, indent=2) if args.json else render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
