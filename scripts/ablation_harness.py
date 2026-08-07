#!/usr/bin/env python3
"""Ablation harness v0: does a harness component change anything measurable?

Escapement keeps adding components -- skills, strengths, doctrine, kernel
prose -- and each one costs context on every turn that loads it. Nothing
could answer whether a given component earns that cost. This runs the
existing evaluation corpus twice, once with a component present (control)
and once with it removed (ablated), and reports the deterministic
differences.

How ablation is applied: the repository is copied to a throwaway directory
and the component's registry entry is removed *there*. Canonical source
files are never modified, so an interrupted run cannot corrupt the repo.

Honest limitations, v0:

- This reuses the routing corpus under `evals/`, which exercises routing
  decisions only. It can show which skills, strengths, packs, questions and
  context words change. It cannot show retries, tool activity, turn closure
  or final task quality -- those need a live-execution corpus that does not
  exist yet. That same corpus is what the Host Conformance Lab will need,
  and it should be one shared corpus, not two.
- "No measurable difference" means this corpus does not exercise the
  component. That is a statement about corpus coverage, not proof the
  component is useless.
- No score, index or significance figure is computed. 22 routing cases
  cannot support one, and a fabricated number would be worse than none.
  The output is a factual diff for a human to judge.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

IGNORED = shutil.ignore_patterns(
    ".git", ".agent", "__pycache__", "*.pyc", "node_modules", ".venv", "backups",
)


def find_root() -> Path:
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists() and (candidate / "catalog").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()


def load_registry(root: Path = ROOT) -> dict[str, Any]:
    path = root / "catalog" / "harness-components.json"
    if not path.exists():
        raise SystemExit(f"FAIL: missing component registry: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def find_component(registry: dict[str, Any], component_id: str) -> dict[str, Any]:
    for item in registry.get("components", []):
        if item.get("id") == component_id:
            return item
    known = ", ".join(sorted(i["id"] for i in registry.get("components", [])))
    raise SystemExit(f"FAIL: unknown component '{component_id}'. Known: {known}")


def materialize(destination: Path) -> None:
    shutil.copytree(ROOT, destination, ignore=IGNORED)


def apply_ablation(destination: Path, component: dict[str, Any]) -> dict[str, Any]:
    """Remove the component from the throwaway copy only."""
    spec = component["ablation"]
    method = spec.get("method")
    if method != "remove-catalog-entry":
        raise SystemExit(f"FAIL: unsupported ablation method '{method}'")

    path = destination / spec["file"]
    if not path.exists():
        raise SystemExit(f"FAIL: ablation target missing: {spec['file']}")

    data = json.loads(path.read_text(encoding="utf-8"))
    collection = spec["collection"]
    items = data.get(collection)
    if not isinstance(items, list):
        raise SystemExit(f"FAIL: '{collection}' is not a list in {spec['file']}")

    field, value = spec["match_field"], spec["match_value"]
    kept = [item for item in items if item.get(field) != value]
    removed = len(items) - len(kept)
    if removed == 0:
        raise SystemExit(
            f"FAIL: nothing to ablate -- no entry with {field}={value!r} "
            f"in {spec['file']}. The registry is stale."
        )

    data[collection] = kept
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"file": spec["file"], "collection": collection, "entries_removed": removed}


def run_evals(root: Path) -> list[dict[str, Any]]:
    process = subprocess.run(
        [sys.executable, str(root / "scripts" / "eval_harness.py"), "run"],
        cwd=root, text=True, capture_output=True, check=False,
    )
    # eval_harness exits 1 when cases fail, which is expected under ablation.
    if process.returncode not in (0, 1):
        raise SystemExit(f"FAIL: eval harness error ({process.returncode}):\n{process.stderr}")

    results = root / ".agent" / "evals" / "results.ndjson"
    if not results.exists():
        raise SystemExit(f"FAIL: no eval results produced in {root}")

    records = []
    for line in results.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def route_facts(record: dict[str, Any]) -> dict[str, Any]:
    route = record.get("actual", {})
    cost = route.get("context_cost", {})
    return {
        "result": record.get("result"),
        "failures": record.get("failures", []),
        "skills": sorted(i["id"] for i in route.get("native_skills", [])),
        "strengths": sorted(i["id"] for i in route.get("capability_strengths", [])),
        "packs": sorted(i["id"] for i in route.get("doctrine_packs", [])),
        "external_candidates": sorted(i["id"] for i in route.get("external_candidates", [])),
        "questions": len(route.get("decision_brief", {}).get("questions", [])),
        "phases": [p.get("id") for p in route.get("phase_plan", [])],
        "rejected": len(route.get("rejected", [])),
        "automatic_context_words": int(cost.get("automatic_total", 0)),
        "invoked_skill_words": int(cost.get("invoked_skill_total", 0)),
    }


def diff_case(control: dict[str, Any], ablated: dict[str, Any]) -> dict[str, Any]:
    delta: dict[str, Any] = {}

    if control["result"] != ablated["result"]:
        delta["result"] = f"{control['result']} -> {ablated['result']}"

    new_failures = [f for f in ablated["failures"] if f not in control["failures"]]
    if new_failures:
        delta["failures_added"] = new_failures

    for field in ("skills", "strengths", "packs", "external_candidates"):
        lost = sorted(set(control[field]) - set(ablated[field]))
        gained = sorted(set(ablated[field]) - set(control[field]))
        if lost:
            delta[f"{field}_lost"] = lost
        if gained:
            delta[f"{field}_gained"] = gained

    for field in ("questions", "rejected", "automatic_context_words", "invoked_skill_words"):
        if control[field] != ablated[field]:
            delta[field] = {
                "control": control[field],
                "ablated": ablated[field],
                "change": ablated[field] - control[field],
            }

    if control["phases"] != ablated["phases"]:
        delta["phase_plan"] = {"control": control["phases"], "ablated": ablated["phases"]}

    return delta


def compare(
    component: dict[str, Any],
    control_records: list[dict[str, Any]],
    ablated_records: list[dict[str, Any]],
    ablation_applied: dict[str, Any],
) -> dict[str, Any]:
    control = {r["case_id"]: route_facts(r) for r in control_records}
    ablated = {r["case_id"]: route_facts(r) for r in ablated_records}

    shared = [case for case in control if case in ablated]
    cases = []
    for case_id in shared:
        delta = diff_case(control[case_id], ablated[case_id])
        if delta:
            cases.append({"case_id": case_id, "delta": delta})

    result_changed = [
        c["case_id"] for c in cases if "result" in c["delta"]
    ]
    control_passed = sum(1 for f in control.values() if f["result"] == "PASS")
    ablated_passed = sum(1 for f in ablated.values() if f["result"] == "PASS")

    return {
        "schema_version": "1.0",
        "component": component["id"],
        "kind": component.get("kind"),
        "hypothesis": component.get("hypothesis"),
        "declared_cost": component.get("cost", {}),
        "ablation_applied": ablation_applied,
        "corpus_cases": len(shared),
        "control_passed": control_passed,
        "ablated_passed": ablated_passed,
        "cases_with_result_change": result_changed,
        "cases_with_any_route_change": [c["case_id"] for c in cases],
        "changed_cases": cases,
        "exercised_by_corpus": bool(cases),
        "limitations": [
            "Routing corpus only: no retries, tool activity, turn closure or task quality.",
            "No score or significance is computed; this is a factual diff.",
            "No change means the corpus does not exercise this component, "
            "not that the component is useless.",
        ],
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        "HARNESS ABLATION",
        f"Component: {report['component']} ({report['kind']})",
        f"Hypothesis: {report['hypothesis']}",
        "",
        f"Ablation: removed {report['ablation_applied']['entries_removed']} entry from "
        f"{report['ablation_applied']['file']} (throwaway copy)",
        "",
        f"Corpus cases:  {report['corpus_cases']}",
        f"Passed control: {report['control_passed']}",
        f"Passed ablated: {report['ablated_passed']}",
        "",
    ]

    if not report["exercised_by_corpus"]:
        lines += [
            "NOT EXERCISED BY THIS CORPUS.",
            "",
            "Removing this component changed no routing decision in any case.",
            "That means this corpus cannot measure it -- it is not evidence",
            "that the component is unnecessary. Extend the shared corpus under",
            "evals/ with a case that depends on it, then re-run.",
        ]
        return "\n".join(lines)

    lines.append(f"Cases with a changed result: {len(report['cases_with_result_change'])}")
    lines.append(f"Cases with any route change: {len(report['cases_with_any_route_change'])}")
    lines += ["", "Changed cases:", ""]

    for case in report["changed_cases"]:
        lines.append(f"  {case['case_id']}")
        for key, value in case["delta"].items():
            lines.append(f"    {key}: {json.dumps(value, ensure_ascii=False)}")
        lines.append("")

    lines += ["Limitations:"] + [f"  - {item}" for item in report["limitations"]]
    return "\n".join(lines)


def command_list(_: argparse.Namespace) -> int:
    registry = load_registry()
    for item in registry.get("components", []):
        cost = item.get("cost", {}).get("context_words", "?")
        print(f"{item['id']}: {item.get('kind')} | context_words={cost} | {item.get('hypothesis')}")
    return 0


def command_run(args: argparse.Namespace) -> int:
    component = find_component(load_registry(), args.component)
    workspace = Path(tempfile.mkdtemp(prefix="esc-ablation-"))
    try:
        control_root = workspace / "control"
        ablated_root = workspace / "ablated"
        materialize(control_root)
        materialize(ablated_root)
        applied = apply_ablation(ablated_root, component)

        report = compare(
            component,
            run_evals(control_root),
            run_evals(ablated_root),
            applied,
        )
    finally:
        if args.keep:
            print(f"Workspace kept: {workspace}", file=sys.stderr)
        else:
            shutil.rmtree(workspace, ignore_errors=True)

    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else render_text(report))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="ablation_harness")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list").set_defaults(func=command_list)

    run = sub.add_parser("run")
    run.add_argument("component")
    run.add_argument("--json", action="store_true")
    run.add_argument("--keep", action="store_true", help="keep the throwaway workspace")
    run.set_defaults(func=command_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
