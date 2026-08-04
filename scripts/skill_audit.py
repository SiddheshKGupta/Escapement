#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "logs/skill-usage.jsonl")

required = {
    "run_id", "task_id", "skill", "version", "trigger", "phase",
    "selected_because", "alternatives_rejected", "expected_output",
    "actual_output", "checks_planned", "checks_run", "checks_not_run",
    "scores", "total_score", "result", "critical_failure",
    "retry_count", "evidence", "timestamp"
}
score_fields = {
    "trigger_accuracy": 15,
    "procedure_adherence": 20,
    "output_correctness": 30,
    "validation_evidence": 20,
    "efficiency": 10,
    "clarity": 5,
}

stats = defaultdict(lambda: {
    "runs": 0, "pass": 0, "partial": 0, "fail": 0,
    "not_needed": 0, "redundant": 0, "sum": 0.0,
    "critical_failures": 0, "retries": 0
})
errors = []

if not path.exists():
    print(json.dumps({"valid": False, "errors": [f"{path} does not exist"], "skills": {}}, indent=2))
    raise SystemExit(1)

for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip():
        continue
    try:
        record = json.loads(line)
    except Exception as exc:
        errors.append(f"line {number}: {exc}")
        continue

    missing = required - record.keys()
    if missing:
        errors.append(f"line {number}: missing {sorted(missing)}")
        continue

    scores = record["scores"]
    missing_scores = score_fields.keys() - scores.keys()
    if missing_scores:
        errors.append(f"line {number}: missing score fields {sorted(missing_scores)}")
        continue

    calculated = sum(float(scores[key]) for key in score_fields)
    if abs(calculated - float(record["total_score"])) > 0.01:
        errors.append(
            f"line {number}: total_score {record['total_score']} "
            f"does not equal component total {calculated}"
        )

    result_key = record["result"].lower()
    if result_key not in {"pass", "partial", "fail", "not_needed", "redundant"}:
        errors.append(f"line {number}: invalid result {record['result']}")
        continue

    skill = stats[record["skill"]]
    skill["runs"] += 1
    skill[result_key] += 1
    skill["sum"] += float(record["total_score"])
    skill["critical_failures"] += int(bool(record["critical_failure"]))
    skill["retries"] += int(record["retry_count"])

output = {
    "valid": not errors,
    "errors": errors,
    "skills": {
        name: {
            **{key: value for key, value in values.items() if key != "sum"},
            "average_score": round(values["sum"] / values["runs"], 1),
        }
        for name, values in stats.items()
    },
}
print(json.dumps(output, indent=2))
raise SystemExit(1 if errors else 0)
