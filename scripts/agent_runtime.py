#!/usr/bin/env python3
"""VLCO v5.4 runtime enforcement.

Standard-library only:
- session context injection
- per-prompt deterministic skill routing
- one-shot Stop gate
- durable turn closure
- provisional evidence logging
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "5.4.1"

SKILLS: dict[str, dict[str, Any]] = {
    "project-discovery": {
        "patterns": [
            r"\bnew (app|application|product|platform|module|system)\b",
            r"\bfrom scratch\b", r"\barchitecture\b",
            r"\bunclear requirements?\b", r"\bdiscover(y)?\b", r"\bprototype\b",
        ],
        "reads": ["PROJECT_CONTEXT.md", "PROJECT_STATE.yaml", "docs/checklists/discovery-gate.md"],
        "purpose": "Clarify scope, decisions, risks, and readiness.",
    },
    "dashboard": {
        "patterns": [
            r"\bdashboard\b", r"\bkpi(s)?\b", r"\bmis\b", r"\breport(ing)?\b",
            r"\bmetric(s)?\b", r"\banalytics\b", r"\bchart(s)?\b", r"\breconciliation\b",
        ],
        "reads": ["docs/standards/data-reporting.md", "docs/checklists/build-readiness.md"],
        "purpose": "Define traceable metrics, periods, sources, drill-down, and reconciliation.",
    },
    "workflow": {
        "patterns": [
            r"\bworkflow\b", r"\bprocess\b", r"\bapproval\b", r"\bstate machine\b",
            r"\bjourney\b", r"\bescalation\b", r"\bmaker[- ]checker\b", r"\bexception\b",
        ],
        "reads": ["PROJECT_CONTEXT.md", "docs/decisions/DECISION_LOG.md"],
        "purpose": "Model states, actors, transitions, controls, and exceptions.",
    },
    "design-system": {
        "patterns": [
            r"\bdesign\b", r"\bbrand\b", r"\bcolour\b", r"\bcolor\b",
            r"\btypograph(y|ic)\b", r"\bfont(s)?\b", r"\blayout\b",
            r"\banimation\b", r"\bmotion\b", r"\bdesign system\b",
            r"\bDESIGN\.md\b", r"\bvisual\b", r"\bpalette\b", r"\btheme\b", r"\bredesign\b",
        ],
        "reads": ["docs/standards/design-intelligence.md", "docs/standards/ui.md", "DESIGN.md"],
        "purpose": "Create an original design system with client-brand precedence.",
    },
    "enterprise-ui-review": {
        "patterns": [
            r"\bui\b", r"\bux\b", r"\binterface\b", r"\bfrontend\b",
            r"\bpage\b", r"\bscreen\b", r"\bcomponent\b",
            r"\bresponsive\b", r"\baccessib(le|ility)\b",
            r"\bgeneric ai\b", r"\blooks? (bad|poor|unappealing)\b", r"\bredesign\b",
        ],
        "reads": ["docs/standards/ui.md", "docs/standards/design-intelligence.md", "DESIGN.md"],
        "purpose": "Review structure, density, hierarchy, states, accessibility, and brand.",
    },
    "api-integration": {
        "patterns": [
            r"\bapi\b", r"\bintegration\b", r"\bwebhook\b", r"\bendpoint\b",
            r"\bconnector\b", r"\boauth\b", r"\bthird[- ]party\b",
        ],
        "reads": ["docs/standards/integrations.md", "docs/standards/security.md"],
        "purpose": "Define contracts, auth, retries, idempotency, errors, and audit.",
    },
    "release-readiness": {
        "patterns": [
            r"\bdeploy(ment)?\b", r"\brelease\b", r"\bproduction\b",
            r"\bgo[- ]live\b", r"\blaunch\b", r"\brollout\b",
        ],
        "reads": [
            "docs/checklists/pre-release.md", "docs/standards/security.md",
            "docs/standards/performance.md", "docs/standards/testing.md",
        ],
        "purpose": "Prove readiness, rollback, monitoring, and approval.",
    },
}

MATERIAL = [
    r"\bbuild\b", r"\bcreate\b", r"\bmake\b", r"\bimplement\b", r"\badd\b",
    r"\bchange\b", r"\bupdate\b", r"\bfix\b", r"\bdebug\b", r"\brefactor\b",
    r"\breview\b", r"\bdesign\b", r"\btest\b", r"\bdeploy\b", r"\bintegrate\b",
    r"\banaly[sz]e\b", r"\baudit\b", r"\bplan\b", r"\bdraft\b",
]
FULL = [
    r"\bnew (app|application|product|platform|module|system)\b",
    r"\bfrom scratch\b", r"\bmajor architecture\b",
]
EXECUTE = [
    r"\bbug\b", r"\bfix\b", r"\bapproved ticket\b",
    r"\bcopy change\b", r"\bsmall change\b", r"\bisolated\b",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_root() -> Path:
    starts: list[Path] = []
    if os.getenv("CLAUDE_PROJECT_DIR"):
        starts.append(Path(os.environ["CLAUDE_PROJECT_DIR"]))
    starts.extend([Path.cwd(), Path(__file__).resolve().parent])
    for start in starts:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists() and (candidate / "PROJECT_STATE.yaml").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()
RUNTIME = ROOT / ".agent" / "runtime"
TURN = RUNTIME / "current-turn.json"
ACTIVE_CONTEXT = RUNTIME / "ACTIVE_CONTEXT.md"
ACTIVE_SKILLS = RUNTIME / "ACTIVE_SKILLS.md"
SESSION_MEMORY = RUNTIME / "SESSION_MEMORY.md"
TURNS_LOG = RUNTIME / "turns.jsonl"
SKILL_LOG = ROOT / "logs" / "skill-usage.jsonl"


def ensure() -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    SKILL_LOG.parent.mkdir(parents=True, exist_ok=True)
    seeds = {
        ACTIVE_CONTEXT: "# Active Context\n\nNo active material turn.\n",
        ACTIVE_SKILLS: "# Active Skills\n\nNo active skills.\n",
        SESSION_MEMORY: "# Session Memory\n\nNo completed turn.\n",
        TURNS_LOG: "",
        SKILL_LOG: "",
    }
    for path, content in seeds.items():
        if not path.exists():
            path.write_text(content, encoding="utf-8")


def hook_input() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def simple_yaml(relative: str) -> dict[str, str]:
    path = ROOT / relative
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith((" ", "-")):
            continue
        if ":" in raw:
            key, value = raw.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def matches(patterns: list[str], text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def material(prompt: str) -> bool:
    return matches(MATERIAL, prompt) or any(matches(v["patterns"], prompt) for v in SKILLS.values())


def mode(prompt: str) -> str:
    if matches(FULL, prompt):
        return "FULL"
    if matches(EXECUTE, prompt):
        return "EXECUTE"
    current = simple_yaml("PROJECT_STATE.yaml").get("work_mode", "")
    if current in {"FULL", "DELTA", "EXECUTE"} and not re.search(
        r"\b(change|update|redesign|replace|integrate|material)\b", prompt, re.IGNORECASE
    ):
        return current
    return "DELTA"


def route(prompt: str) -> list[str]:
    selected = [name for name, definition in SKILLS.items() if matches(definition["patterns"], prompt)]

    if "design-system" in selected and matches(
        [r"\bui\b", r"\bpage\b", r"\bscreen\b", r"\bcomponent\b", r"\bfrontend\b", r"\bbuild\b"],
        prompt,
    ) and "enterprise-ui-review" not in selected:
        selected.append("enterprise-ui-review")

    if mode(prompt) == "FULL" and "project-discovery" not in selected:
        selected.insert(0, "project-discovery")

    if material(prompt):
        selected.append("skill-governance")

    ordered: list[str] = []
    for item in selected:
        if item not in ordered:
            ordered.append(item)

    if len(ordered) > 4:
        ordered = [x for x in ordered if x != "skill-governance"][:3] + ["skill-governance"]
    return ordered


def reads_for(selected: list[str]) -> list[str]:
    reads = ["AGENTS.md", "AGENT_RUNTIME.md", "PROJECT_STATE.yaml", ".agent/runtime/SESSION_MEMORY.md"]
    for skill in selected:
        if skill == "skill-governance":
            reads.extend(["docs/standards/harness-engineering.md", "docs/standards/context-engineering.md"])
        else:
            reads.extend(SKILLS.get(skill, {}).get("reads", []))
    return list(dict.fromkeys(reads))


def emit_context(event: str, context: str, message: str | None = None) -> None:
    payload: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": context,
        }
    }
    if message:
        payload["systemMessage"] = message
    print(json.dumps(payload))


def save_turn(value: dict[str, Any]) -> None:
    TURN.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def load_turn() -> dict[str, Any] | None:
    if not TURN.exists():
        return None
    try:
        value = json.loads(TURN.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def write_active(value: dict[str, Any]) -> None:
    state = simple_yaml("PROJECT_STATE.yaml")
    selected = value.get("skills", [])
    required = value.get("required_reads", [])

    ACTIVE_CONTEXT.write_text(
        f"""# Active Context

- Runtime: {VERSION}
- Turn ID: {value['turn_id']}
- Started: {value['started_at']}
- Status: {value['status']}
- Material: {str(value['material']).lower()}
- Mode: {value['mode']}
- User goal: {value['prompt']}
- Project: {state.get('project_name', 'TBD')}
- Phase: {state.get('phase', 'TBD')}
- Implementation authorised: {state.get('implementation_authorized', 'TBD')}
- Approved ticket: {state.get('approved_ticket', 'TBD')}

## Mandatory Reads

{chr(10).join(f'- `{path}`' for path in required)}

## Selected Skills

{chr(10).join(f'- `{skill}`' for skill in selected) if selected else '- None'}

## Turn Contract

1. Read this file and `ACTIVE_SKILLS.md`.
2. Invoke every selected native skill.
3. Perform one bounded step.
4. Run deterministic checks first.
5. Update durable state.
6. Close the turn before the final response.

## Approval Gates

Pause before schema, authentication, RBAC, destructive, production, paid-service,
confidential-data, new-integration, or material-scope changes.
""",
        encoding="utf-8",
    )

    lines = ["# Active Skills", "", f"- Turn ID: {value['turn_id']}", f"- Mode: {value['mode']}", ""]
    if not selected:
        lines.append("No native skill selected.")
    for skill in selected:
        purpose = (
            "Record selection, outputs, checks, evidence, and closure truthfully."
            if skill == "skill-governance"
            else SKILLS.get(skill, {}).get("purpose", "")
        )
        lines.extend([
            f"## {skill}", "",
            f"- Purpose: {purpose}",
            f"- Codex: `${skill}`",
            f"- Claude Code: `/{skill}`",
            f"- Codex file: `.agents/skills/{skill}/SKILL.md`",
            f"- Claude file: `.claude/skills/{skill}/SKILL.md`",
            "",
        ])
    ACTIVE_SKILLS.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def start(prompt: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    ensure()
    is_material = material(prompt)
    selected = route(prompt) if is_material else []
    value = {
        "runtime_version": VERSION,
        "turn_id": f"TURN-{uuid.uuid4().hex[:12]}",
        "session_id": (data or {}).get("session_id") or os.getenv("CODEX_SESSION_ID") or "unknown",
        "started_at": now(),
        "updated_at": now(),
        "prompt": prompt.strip(),
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "material": is_material,
        "mode": mode(prompt) if is_material else "NONE",
        "skills": selected,
        "required_reads": reads_for(selected),
        "status": "open" if is_material else "informational",
        "close_required": is_material,
        "stop_blocks": 0,
        "closure": None,
    }
    save_turn(value)
    write_active(value)
    return value


def append(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False) + "\n")


def split(value: str | None, separator: str = ",") -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(separator) if part.strip()]


def valid_evidence(items: list[str]) -> list[str]:
    return [x for x in items if x.startswith(("http://", "https://")) or (ROOT / x).exists()]


def scores(has_evidence: bool, has_checks: bool) -> dict[str, int]:
    return {
        "trigger_accuracy": 15,
        "procedure_adherence": 18,
        "output_correctness": 25 if has_evidence else 8,
        "validation_evidence": 18 if has_checks and has_evidence else (10 if has_checks else 0),
        "efficiency": 8,
        "clarity": 5,
    }


def cmd_session(_: argparse.Namespace) -> int:
    ensure()
    state = simple_yaml("PROJECT_STATE.yaml")
    emit_context(
        "SessionStart",
        "VLCO runtime active. Read AGENTS.md, AGENT_RUNTIME.md, ACTIVE_CONTEXT.md, "
        "ACTIVE_SKILLS.md, and SESSION_MEMORY.md before material work. "
        f"Project={state.get('project_name', 'TBD')}; phase={state.get('phase', 'TBD')}; "
        f"mode={state.get('work_mode', 'TBD')}.",
        "VLCO runtime bootstrap loaded",
    )
    return 0


def cmd_prompt(_: argparse.Namespace) -> int:
    data = hook_input()
    prompt = str(data.get("prompt") or data.get("user_prompt") or data.get("message") or "")
    if not prompt:
        return 0
    value = start(prompt, data)
    if not value["material"]:
        emit_context("UserPromptSubmit", "Informational prompt: no material runtime turn required.")
        return 0
    selected = ", ".join(f"{x} (Codex `${x}` / Claude `/{x}`)" for x in value["skills"])
    emit_context(
        "UserPromptSubmit",
        f"VLCO MATERIAL TURN {value['turn_id']}. Mode={value['mode']}. "
        f"Selected skills: {selected}. Read ACTIVE_CONTEXT.md and ACTIVE_SKILLS.md, "
        "invoke all selected skills, execute one bounded step, run checks, and call "
        "`python scripts/agent_runtime.py close-turn ...` before the final response. "
        "The Stop hook blocks one premature stop.",
        f"VLCO route: {value['mode']} | {', '.join(value['skills'])}",
    )
    return 0


def cmd_manual(args: argparse.Namespace) -> int:
    value = start(args.prompt, {})
    print(f"Turn: {value['turn_id']}")
    print(f"Material: {value['material']}")
    print(f"Mode: {value['mode']}")
    print(f"Skills: {', '.join(value['skills']) or 'None'}")
    return 0


def cmd_stop(_: argparse.Namespace) -> int:
    data = hook_input()
    value = load_turn()
    if not value or not value.get("close_required") or value.get("status") != "open":
        return 0

    if bool(data.get("stop_hook_active")) or int(value.get("stop_blocks", 0)) >= 1:
        value["runtime_warning"] = "Stopped with an open turn after the one allowed continuation."
        value["updated_at"] = now()
        save_turn(value)
        append(TURNS_LOG, {"turn_id": value["turn_id"], "timestamp": now(), "event": "stop-allowed-open-turn"})
        return 0

    value["stop_blocks"] = int(value.get("stop_blocks", 0)) + 1
    value["updated_at"] = now()
    save_turn(value)
    reason = (
        f"VLCO runtime turn {value['turn_id']} remains open. Read ACTIVE_CONTEXT.md and "
        "ACTIVE_SKILLS.md, invoke any unused selected skills, update durable state, run "
        "deterministic checks, then execute `python scripts/agent_runtime.py close-turn "
        "--summary \"...\" --next \"...\" --files \"...\" --checks \"...\" "
        "--evidence \"...\"` before responding."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


def cmd_close(args: argparse.Namespace) -> int:
    ensure()
    value = load_turn()
    if not value:
        print("FAIL: no runtime turn exists.", file=sys.stderr)
        return 1
    if value.get("status") == "closed":
        print("Turn already closed.")
        return 0

    files = split(args.files)
    checks = split(args.checks, ";")
    not_run = split(args.not_run, ";")
    evidence = valid_evidence(split(args.evidence))

    closure = {
        "closed_at": now(),
        "summary": args.summary,
        "next_action": args.next,
        "files": files,
        "checks_run": checks,
        "checks_not_run": not_run,
        "evidence": evidence,
        "result": args.result,
        "blockers": args.blockers or "None recorded",
    }
    value.update(status="closed", close_required=False, updated_at=now(), closure=closure)
    save_turn(value)
    append(TURNS_LOG, value)

    memory = f"""# Session Memory

- Last completed turn: {value['turn_id']}
- Closed: {closure['closed_at']}
- Mode: {value['mode']}
- Skills: {', '.join(value['skills']) or 'None'}
- Summary: {closure['summary']}
- Files: {', '.join(files) or 'None recorded'}
- Checks run: {'; '.join(checks) or 'None recorded'}
- Checks not run: {'; '.join(not_run) or 'None'}
- Evidence: {', '.join(evidence) or 'None recorded'}
- Blockers: {closure['blockers']}
- Next action: {closure['next_action']}
"""
    SESSION_MEMORY.write_text(memory, encoding="utf-8")
    (ROOT / "SESSION_HANDOFF.md").write_text(memory.replace("# Session Memory", "# Session Handoff"), encoding="utf-8")

    for skill in value.get("skills", []):
        component_scores = scores(bool(evidence), bool(checks))
        total = sum(component_scores.values())
        result = args.result
        if result == "PASS" and (not evidence or not checks or total < 85):
            result = "PARTIAL"
        append(SKILL_LOG, {
            "run_id": f"SR-{uuid.uuid4().hex[:12]}",
            "task_id": value["turn_id"],
            "skill": skill,
            "version": VERSION,
            "trigger": value["prompt"][:500],
            "phase": simple_yaml("PROJECT_STATE.yaml").get("phase", "unknown"),
            "selected_because": "Selected deterministically by the VLCO runtime router.",
            "alternatives_rejected": [],
            "expected_output": "Task-appropriate artifact and evidence defined by the native skill.",
            "actual_output": files,
            "checks_planned": checks + not_run,
            "checks_run": checks,
            "checks_not_run": not_run,
            "scores": component_scores,
            "total_score": total,
            "result": result,
            "critical_failure": args.critical_failure,
            "retry_count": int(value.get("stop_blocks", 0)),
            "duration_seconds": 0,
            "turns_used": 1 + int(value.get("stop_blocks", 0)),
            "impact": args.impact or "Runtime-selected skill used for the material turn.",
            "reviewer": "runtime-provisional",
            "evidence": evidence,
            "timestamp": closure["closed_at"],
        })

    write_active(value)
    print(f"Closed {value['turn_id']}")
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    ensure()
    print(json.dumps({"runtime_version": VERSION, "root": str(ROOT), "turn": load_turn()}, indent=2))
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    ensure()
    value = load_turn() or {}
    append(TURNS_LOG, {
        "turn_id": value.get("turn_id", "unknown"),
        "timestamp": now(),
        "event": "reset-turn",
        "reason": args.reason,
    })
    TURN.unlink(missing_ok=True)
    ACTIVE_CONTEXT.write_text("# Active Context\n\nNo active material turn. Previous turn was reset.\n", encoding="utf-8")
    ACTIVE_SKILLS.write_text("# Active Skills\n\nNo active skills.\n", encoding="utf-8")
    print("Runtime turn reset.")
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    ensure()
    required = [
        "AGENTS.md", "AGENT_RUNTIME.md", "PROJECT_STATE.yaml", "CLAUDE.md",
        ".codex/hooks.json", ".claude/settings.json",
        "docs/standards/design-intelligence.md", "scripts/agent_runtime.py",
    ]
    failures = 0
    print("VLCO RUNTIME DOCTOR")
    for relative in required:
        ok = (ROOT / relative).exists()
        print(f"[{'PASS' if ok else 'FAIL'}] {relative}")
        failures += int(not ok)

    # Derived from skills/ so the doctor cannot drift from the shipped skill set.
    native = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
    if not native:
        print("[FAIL] skills/ contains no SKILL.md files")
        failures += 1
    for skill in native:
        ok = (
            (ROOT / ".agents" / "skills" / skill / "SKILL.md").exists()
            and (ROOT / ".claude" / "skills" / skill / "SKILL.md").exists()
        )
        print(f"[{'PASS' if ok else 'FAIL'}] native skill {skill}")
        failures += int(not ok)

    state = simple_yaml("PROJECT_STATE.yaml")
    if state.get("project_name") in {"", "TBD", None}:
        print("[WARN] PROJECT_STATE.yaml is still a template.")
    else:
        print(f"[PASS] project state: {state.get('project_name')}")
    print(f"\nFailures: {failures}")
    return 1 if failures else 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="agent_runtime")
    sub = root.add_subparsers(dest="command", required=True)

    sub.add_parser("session-start").set_defaults(func=cmd_session)
    sub.add_parser("prompt").set_defaults(func=cmd_prompt)
    sub.add_parser("stop").set_defaults(func=cmd_stop)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("doctor").set_defaults(func=cmd_doctor)

    manual = sub.add_parser("manual-start")
    manual.add_argument("--prompt", required=True)
    manual.set_defaults(func=cmd_manual)

    close = sub.add_parser("close-turn")
    close.add_argument("--summary", required=True)
    close.add_argument("--next", required=True)
    close.add_argument("--files", default="")
    close.add_argument("--checks", default="")
    close.add_argument("--not-run", default="")
    close.add_argument("--evidence", default="")
    close.add_argument("--blockers", default="")
    close.add_argument("--impact", default="")
    close.add_argument("--result", choices=["PASS", "PARTIAL", "FAIL", "NOT_NEEDED", "REDUNDANT"], default="PASS")
    close.add_argument("--critical-failure", action="store_true")
    close.set_defaults(func=cmd_close)

    reset = sub.add_parser("reset-turn")
    reset.add_argument("--reason", required=True)
    reset.set_defaults(func=cmd_reset)
    return root


def main() -> int:
    ensure()
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
