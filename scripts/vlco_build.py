#!/usr/bin/env python3
"""VLCO Product Build Standard CLI.

Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "5.3.0"

CORE_INSTALL_PATHS = [
    "AGENTS.md",
    "PROJECT_STATE.yaml",
    "PROJECT_CONTEXT.md",
    "CURRENT_PHASE.md",
    "SESSION_HANDOFF.md",
    "SKILLS_INVENTORY.md",
    "SKILL_USAGE_PLAN.md",
    "AI_REPORT.md",
    "docs",
    "skills",
    "scripts",
    "schemas",
    "tests/agent-behaviour",
]


def run_python(script: str, args: list[str] | None = None) -> int:
    command = [sys.executable, str(ROOT / "scripts" / script), *(args or [])]
    return subprocess.call(command, cwd=ROOT)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def command_version(_: argparse.Namespace) -> int:
    print(VERSION)
    return 0


def command_validate(_: argparse.Namespace) -> int:
    return run_python("validate_standard.py")


def command_doctor(_: argparse.Namespace) -> int:
    checks: list[tuple[str, bool, str]] = []

    checks.append(("Python >= 3.10", sys.version_info >= (3, 10), sys.version.split()[0]))
    checks.append(("Git available", shutil.which("git") is not None, shutil.which("git") or "not found"))
    checks.append(("Repository manifest", (ROOT / "manifest.json").exists(), str(ROOT / "manifest.json")))
    checks.append(("Root AGENTS.md", (ROOT / "AGENTS.md").exists(), str(ROOT / "AGENTS.md")))
    checks.append(("Project state", (ROOT / "PROJECT_STATE.yaml").exists(), str(ROOT / "PROJECT_STATE.yaml")))
    checks.append(("Validator", (ROOT / "scripts/validate_standard.py").exists(), "scripts/validate_standard.py"))
    checks.append(("Skill audit", (ROOT / "scripts/skill_audit.py").exists(), "scripts/skill_audit.py"))

    print("VLCO BUILD DOCTOR")
    failures = 0
    for name, ok, detail in checks:
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {name}: {detail}")
        failures += 0 if ok else 1

    if failures:
        print(f"\nDoctor found {failures} blocking issue(s).")
        return 1

    print("\nRunning standard validation...")
    return command_validate(argparse.Namespace())


def copy_path(source: Path, destination: Path, overwrite: bool) -> tuple[int, int]:
    created = updated = 0
    if source.is_dir():
        for item in source.rglob("*"):
            if not item.is_file():
                continue
            relative = item.relative_to(source)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and not overwrite:
                continue
            existed = target.exists()
            shutil.copy2(item, target)
            updated += int(existed)
            created += int(not existed)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not overwrite:
            return 0, 0
        existed = destination.exists()
        shutil.copy2(source, destination)
        updated += int(existed)
        created += int(not existed)
    return created, updated


def command_init(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    created = updated = 0
    for relative in CORE_INSTALL_PATHS:
        source = ROOT / relative
        if not source.exists():
            print(f"WARN missing source: {relative}")
            continue
        destination = target / relative
        c, u = copy_path(source, destination, args.force)
        created += c
        updated += u

    install = {
        "standard": "VLCO Product Build Standard",
        "version": VERSION,
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "source": str(ROOT),
    }
    (target / ".vlco-build.json").write_text(json.dumps(install, indent=2) + "\n", encoding="utf-8")

    print(f"Installed into: {target}")
    print(f"Created: {created}")
    print(f"Updated: {updated}")
    print("Next: update PROJECT_STATE.yaml and PROJECT_CONTEXT.md")
    return 0


def command_context(args: argparse.Namespace) -> int:
    forwarded = [
        "--task", args.task,
        "--goal", args.goal,
        "--mode", args.mode,
        "--output", args.output,
    ]
    if args.scope:
        forwarded.extend(["--scope", args.scope])
    if args.acceptance:
        forwarded.extend(["--acceptance", args.acceptance])
    return run_python("build_context_pack.py", forwarded)


def command_skill_audit(args: argparse.Namespace) -> int:
    forwarded = [args.log] if args.log else []
    return run_python("skill_audit.py", forwarded)


def command_handoff(args: argparse.Namespace) -> int:
    output = Path(args.output)
    timestamp = datetime.now(timezone.utc).isoformat()
    content = f"""# Session Handoff

- Updated: {timestamp}
- Summary: {args.summary}
- Current state: {args.state or 'See PROJECT_STATE.yaml'}
- Completed: {args.completed or 'TBD'}
- Decisions: {args.decisions or 'See docs/decisions/DECISION_LOG.md'}
- Checks run: {args.checks or 'TBD'}
- Checks not run: {args.not_run or 'None recorded'}
- Blockers: {args.blockers or 'None recorded'}
- Next action: {args.next}
- Exact files: {args.files or 'TBD'}
"""
    output.write_text(content, encoding="utf-8")
    print(output)
    return 0


def command_update(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    install_file = target / ".vlco-build.json"
    if not install_file.exists():
        print("FAIL: target has no .vlco-build.json. Run init first.")
        return 1

    changed = []
    missing = []
    for relative in CORE_INSTALL_PATHS:
        source = ROOT / relative
        destination = target / relative
        if source.is_file():
            if not destination.exists():
                missing.append(relative)
            elif sha256(source) != sha256(destination):
                changed.append(relative)
        elif source.is_dir():
            for item in source.rglob("*"):
                if not item.is_file():
                    continue
                rel = item.relative_to(ROOT)
                dest = target / rel
                if not dest.exists():
                    missing.append(str(rel))
                elif sha256(item) != sha256(dest):
                    changed.append(str(rel))

    print(f"Target: {target}")
    print(f"Missing: {len(missing)}")
    print(f"Different: {len(changed)}")
    for item in missing[:50]:
        print(f"MISSING {item}")
    for item in changed[:50]:
        print(f"DIFF {item}")

    if args.apply:
        ns = argparse.Namespace(target=str(target), force=True)
        return command_init(ns)

    return 1 if missing or changed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vlco-build")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("version").set_defaults(func=command_version)
    sub.add_parser("validate").set_defaults(func=command_validate)
    sub.add_parser("doctor").set_defaults(func=command_doctor)

    init_p = sub.add_parser("init")
    init_p.add_argument("target")
    init_p.add_argument("--force", action="store_true")
    init_p.set_defaults(func=command_init)

    context_p = sub.add_parser("context")
    context_p.add_argument("--task", required=True)
    context_p.add_argument("--goal", required=True)
    context_p.add_argument("--mode", choices=["FULL", "DELTA", "EXECUTE"], required=True)
    context_p.add_argument("--scope")
    context_p.add_argument("--acceptance")
    context_p.add_argument("--output", default="CURRENT_CONTEXT.md")
    context_p.set_defaults(func=command_context)

    audit_p = sub.add_parser("skill-audit")
    audit_p.add_argument("--log", default="logs/skill-usage.jsonl")
    audit_p.set_defaults(func=command_skill_audit)

    handoff_p = sub.add_parser("handoff")
    handoff_p.add_argument("--summary", required=True)
    handoff_p.add_argument("--next", required=True)
    handoff_p.add_argument("--state")
    handoff_p.add_argument("--completed")
    handoff_p.add_argument("--decisions")
    handoff_p.add_argument("--checks")
    handoff_p.add_argument("--not-run")
    handoff_p.add_argument("--blockers")
    handoff_p.add_argument("--files")
    handoff_p.add_argument("--output", default="SESSION_HANDOFF.md")
    handoff_p.set_defaults(func=command_handoff)

    update_p = sub.add_parser("update")
    update_p.add_argument("target")
    update_p.add_argument("--apply", action="store_true")
    update_p.set_defaults(func=command_update)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
