#!/usr/bin/env python3
"""Unified deterministic validator for the Escapement build standard."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

LINE_BUDGETS = {
    "BRD.md": 120,
    "PRD.md": 150,
    "FRD.md": 180,
    "ARCHITECTURE.md": 180,
    "SECURITY.md": 120,
    "FRONTEND_SPEC.md": 150,
    "SESSION_HANDOFF.md": 40,
}

# Required in any repository governed by the standard.
REQUIRED_ROOT = [
    "AGENTS.md",
    "AGENT_RUNTIME.md",
    "PROJECT_STATE.yaml",
    "PROJECT_CONTEXT.md",
    "CURRENT_PHASE.md",
    "SESSION_HANDOFF.md",
    "SKILLS_INVENTORY.md",
    "SKILL_USAGE_PLAN.md",
    "AI_REPORT.md",
]

# Required only in the standard's own repository. These describe the standard itself,
# so a consuming project must never be failed for lacking them.
REQUIRED_ROOT_STANDARD = [
    "README.md",
    "manifest.json",
]

NATIVE_SKILL_DIRS = [".claude/skills", ".agents/skills"]

REQUIRED_BEHAVIOURS = {
    "new-project",
    "small-bug",
    "skill-overlap",
    "skill-overuse",
    "skill-not-triggered",
    "context-rot",
    "dashboard-kpi",
    "material-architecture-change",
    "instruction-conflict",
    "production-deployment",
    "harness-improvement",
}

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def ok(self, message: str) -> None:
        self.passes.append(message)

    def emit(self) -> int:
        for message in self.passes:
            print(f"PASS {message}")
        for message in self.warnings:
            print(f"WARN {message}")
        for message in self.failures:
            print(f"FAIL {message}")
        print(
            f"\nSummary: {len(self.passes)} pass, "
            f"{len(self.warnings)} warning, {len(self.failures)} failure"
        )
        return 1 if self.failures else 0


def load_manifest(report: Report) -> dict:
    path = ROOT / "manifest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        report.fail(f"manifest.json cannot be read: {exc}")
        return {}
    if not isinstance(data.get("files"), list):
        report.fail("manifest.json must contain a files array")
    else:
        report.ok("manifest.json structure")
    return data


def is_standard_repo() -> bool:
    """False when the standard has been installed into a consuming project."""
    return not (ROOT / ".vlco-build.json").exists()


def check_required_root(report: Report) -> None:
    required = list(REQUIRED_ROOT)
    if is_standard_repo():
        required += REQUIRED_ROOT_STANDARD
    missing = [p for p in required if not (ROOT / p).exists()]
    if missing:
        report.fail(f"required root files missing: {missing}")
    else:
        report.ok("required root files")


def check_native_skills(report: Report) -> None:
    """Native skills are generated from skills/ and must not drift from it."""
    drift = []
    for source in sorted((ROOT / "skills").glob("*/SKILL.md")):
        skill = source.parent.name
        for native in NATIVE_SKILL_DIRS:
            target = ROOT / native / skill / "SKILL.md"
            if not target.exists():
                drift.append(f"missing {native}/{skill}/SKILL.md")
            elif target.read_bytes() != source.read_bytes():
                drift.append(f"stale {native}/{skill}/SKILL.md")
    if drift:
        report.fail(f"native skills out of sync (run vlco_build.py sync-skills): {drift}")
    else:
        report.ok(f"native skills synced across {len(NATIVE_SKILL_DIRS)} harness directories")


def check_versions(report: Report) -> None:
    """manifest.json, the build CLI, and the runtime must all agree on the version."""
    if not is_standard_repo():
        report.ok("version consistency check not applicable to a project install")
        return
    found: dict[str, str] = {}
    try:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        found["manifest.json"] = str(manifest.get("version", ""))
    except Exception:
        report.fail("version check could not read manifest.json")
        return
    for name in ("vlco_build.py", "agent_runtime.py"):
        text = (ROOT / "scripts" / name).read_text(encoding="utf-8")
        match = re.search(r'^VERSION\s*=\s*"([^"]+)"', text, re.MULTILINE)
        if match:
            found[name] = match.group(1)

    minors = {v.rsplit(".", 1)[0] if v.count(".") == 2 else v for v in found.values()}
    if len(minors) > 1:
        report.fail(f"version drift across sources: {found}")
    else:
        report.ok(f"version consistent across {len(found)} sources ({minors.pop()})")


def check_manifest_paths(report: Report, manifest: dict) -> None:
    files = manifest.get("files", [])
    missing = [p for p in files if not (ROOT / p).exists()]
    if missing:
        report.fail(f"manifest paths missing: {missing}")
    else:
        report.ok(f"all {len(files)} manifest paths exist")


def iter_markdown() -> Iterable[Path]:
    return ROOT.rglob("*.md")


def check_line_budgets(report: Report) -> None:
    violations = []
    for path in iter_markdown():
        limit = LINE_BUDGETS.get(path.name)
        if limit is None:
            continue
        count = len(path.read_text(encoding="utf-8").splitlines())
        if count > limit:
            violations.append(f"{path.relative_to(ROOT)}={count}>{limit}")
    if violations:
        report.fail(f"line budget violations: {violations}")
    else:
        report.ok("document line budgets")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    values = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def check_skills(report: Report) -> None:
    skills = list((ROOT / "skills").glob("*/SKILL.md"))
    names: dict[str, Path] = {}
    errors = []
    for path in skills:
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        for required in ("name", "description"):
            if not meta.get(required):
                errors.append(f"{path.relative_to(ROOT)} missing {required}")
        name = meta.get("name")
        if name:
            if name in names:
                errors.append(
                    f"duplicate skill name {name}: "
                    f"{names[name].relative_to(ROOT)} and {path.relative_to(ROOT)}"
                )
            names[name] = path
    if errors:
        report.fail(f"skill frontmatter: {errors}")
    else:
        report.ok(f"{len(skills)} skills have valid unique frontmatter")


def check_internal_links(report: Report) -> None:
    broken = []
    for path in iter_markdown():
        text = path.read_text(encoding="utf-8")
        for target in LINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if not candidate.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    if broken:
        report.fail(f"broken internal links: {broken}")
    else:
        report.ok("internal Markdown links")


def parse_simple_yaml(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith((" ", "-")):
            continue
        if ":" in raw:
            key, value = raw.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def check_project_state(report: Report) -> None:
    path = ROOT / "PROJECT_STATE.yaml"
    values = parse_simple_yaml(path)
    required = {"project_name", "phase", "work_mode", "implementation_authorized"}
    missing = sorted(required - values.keys())
    if missing:
        report.fail(f"PROJECT_STATE.yaml missing keys: {missing}")
        return
    if values["work_mode"] not in {"FULL", "DELTA", "EXECUTE"}:
        report.fail("PROJECT_STATE.yaml work_mode must be FULL, DELTA, or EXECUTE")
        return
    report.ok("PROJECT_STATE.yaml core structure")


def check_skill_log(report: Report) -> None:
    path = ROOT / "logs/skill-usage.jsonl"
    if not path.exists():
        report.fail("logs/skill-usage.jsonl missing")
        return
    required = {
        "run_id", "task_id", "skill", "version", "trigger", "phase",
        "selected_because", "alternatives_rejected", "expected_output",
        "actual_output", "checks_planned", "checks_run", "checks_not_run",
        "scores", "total_score", "result", "critical_failure",
        "retry_count", "evidence", "timestamp"
    }
    errors = []
    count = 0
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        count += 1
        try:
            record = json.loads(line)
        except Exception as exc:
            errors.append(f"line {number}: invalid JSON: {exc}")
            continue
        missing = required - record.keys()
        if missing:
            errors.append(f"line {number}: missing {sorted(missing)}")
            continue
        if not 0 <= float(record["total_score"]) <= 100:
            errors.append(f"line {number}: total_score outside 0..100")
        if record["result"] not in {"PASS", "PARTIAL", "FAIL", "NOT_NEEDED", "REDUNDANT"}:
            errors.append(f"line {number}: invalid result")
        evidence = record.get("evidence", [])
        for evidence_path in evidence:
            if evidence_path.startswith(("http://", "https://")):
                continue
            if not (ROOT / evidence_path).exists():
                errors.append(f"line {number}: missing evidence path {evidence_path}")
    if errors:
        report.fail(f"skill log errors: {errors}")
    else:
        report.ok(f"skill evidence log ({count} record(s))")


def check_context_budget(report: Report) -> None:
    candidates = [ROOT / "CURRENT_CONTEXT.md", *ROOT.glob("examples/**/CURRENT_CONTEXT.md")]
    oversized = []
    for path in candidates:
        if not path.exists():
            continue
        words = len(path.read_text(encoding="utf-8").split())
        if words > 1000:
            oversized.append(f"{path.relative_to(ROOT)}={words}")
    if oversized:
        report.fail(f"context packs above 1,000 words: {oversized}")
    else:
        report.ok("context-pack word budget")


def check_behaviour_tests(report: Report) -> None:
    directory = ROOT / "tests/agent-behaviour"
    found = {p.stem for p in directory.glob("*.yaml")}
    missing = sorted(REQUIRED_BEHAVIOURS - found)
    if missing:
        report.fail(f"machine-readable behaviour tests missing: {missing}")
    else:
        report.ok(f"{len(found)} machine-readable behaviour tests")


def check_release_placeholders(report: Report) -> None:
    state = parse_simple_yaml(ROOT / "PROJECT_STATE.yaml")
    phase = state.get("phase", "").lower()
    if phase not in {"release", "production", "closed"}:
        report.ok("release placeholder check not applicable")
        return
    violations = []
    for name in ("BRD.md", "PRD.md", "FRD.md", "ARCHITECTURE.md", "SECURITY.md"):
        path = ROOT / name
        if path.exists() and re.search(r"\bTBD\b", path.read_text(encoding="utf-8")):
            violations.append(name)
    if violations:
        report.fail(f"release documents contain TBD: {violations}")
    else:
        report.ok("release documents have no TBD placeholders")


def main() -> int:
    report = Report()
    check_required_root(report)
    if is_standard_repo():
        manifest = load_manifest(report)
        check_manifest_paths(report, manifest)
        check_versions(report)
    else:
        report.ok("manifest checks skipped (project profile)")
    check_line_budgets(report)
    check_skills(report)
    check_native_skills(report)
    check_internal_links(report)
    check_project_state(report)
    check_skill_log(report)
    check_context_budget(report)
    check_behaviour_tests(report)
    check_release_placeholders(report)
    return report.emit()


if __name__ == "__main__":
    raise SystemExit(main())
