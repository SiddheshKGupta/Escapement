#!/usr/bin/env python3
"""Escapement v6 runtime.

Standard-library only.

Provides:
- session context injection;
- explainable materiality, mode, and native-skill routing;
- open-turn continuity protection;
- one-shot Stop gate;
- structured evidence validation;
- durable handoff and content-addressed NDJSON records.
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
from typing import Any, Iterable

VERSION = "6.3.0"

SKILLS: dict[str, dict[str, Any]] = {
    "project-discovery": {
        "patterns": [
            r"\bnew\b.{0,60}\b(app|application|product|platform|module|system)\b",
            r"\bfrom scratch\b",
            r"\barchitecture\b",
            r"\bunclear requirements?\b",
            r"\bdiscover(y)?\b",
            r"\bprototype\b",
            r"\bspecification\b",
        ],
        "reads": [
            "PROJECT_CONTEXT.md",
            "PROJECT_STATE.yaml",
            "docs/specs/CONSTITUTION.md",
            "docs/checklists/discovery-gate.md",
        ],
        "purpose": "Clarify scope, decisions, risks, specification, and readiness.",
    },
    "dashboard": {
        "patterns": [
            r"\bdashboard\b",
            r"\bkpi(s)?\b",
            r"\bmis\b",
            r"\breport(ing)?\b",
            r"\bmetric(s)?\b",
            r"\banalytics\b",
            r"\bchart(s)?\b",
            r"\breconciliation\b",
        ],
        "reads": [
            "docs/standards/data-reporting.md",
            "docs/checklists/build-readiness.md",
        ],
        "purpose": "Define traceable metrics, periods, sources, drill-down, and reconciliation.",
    },
    "workflow": {
        "patterns": [
            r"\bworkflow\b",
            r"\bprocess\b",
            r"\bapproval\b",
            r"\bstate machine\b",
            r"\bjourney\b",
            r"\bescalation\b",
            r"\bmaker[- ]checker\b",
            r"\bexception\b",
            r"\bsla\b",
        ],
        "reads": [
            "PROJECT_CONTEXT.md",
            "docs/decisions/DECISION_LOG.md",
        ],
        "purpose": "Model states, actors, transitions, controls, exceptions, and SLA.",
    },
    "design-system": {
        "patterns": [
            r"\bdesign\b",
            r"\bbrand\b",
            r"\bcolour\b",
            r"\bcolor\b",
            r"\btypograph(y|ic)\b",
            r"\bfont(s)?\b",
            r"\blayout\b",
            r"\banimation\b",
            r"\bmotion\b",
            r"\bdesign system\b",
            r"\bDESIGN\.md\b",
            r"\bvisual\b",
            r"\bpalette\b",
            r"\btheme\b",
            r"\bredesign\b",
        ],
        "reads": [
            "docs/standards/design-intelligence.md",
            "docs/standards/ui.md",
            "DESIGN.md",
        ],
        "purpose": "Create an original design system with client-brand precedence.",
    },
    "enterprise-ui-review": {
        "patterns": [
            r"\bui\b",
            r"\bux\b",
            r"\binterface\b",
            r"\bfrontend\b",
            r"\bpage\b",
            r"\bscreen\b",
            r"\bcomponent\b",
            r"\bresponsive\b",
            r"\baccessib(le|ility)\b",
            r"\bgeneric ai\b",
            r"\blooks? (bad|poor|unappealing)\b",
            r"\bredesign\b",
        ],
        "reads": [
            "docs/standards/ui.md",
            "docs/standards/design-intelligence.md",
            "DESIGN.md",
        ],
        "purpose": "Review hierarchy, density, states, accessibility, and brand.",
    },
    "api-integration": {
        "patterns": [
            r"\bapi\b",
            r"\bintegration\b",
            r"\bwebhook\b",
            r"\bendpoint\b",
            r"\bconnector\b",
            r"\boauth\b",
            r"\bthird[- ]party\b",
            r"\bmcp\b",
        ],
        "reads": [
            "docs/standards/integrations.md",
            "docs/standards/security.md",
        ],
        "purpose": "Define contracts, authentication, retries, idempotency, errors, and audit.",
    },
    "release-readiness": {
        "patterns": [
            r"\bdeploy(ment)?\b",
            r"\brelease\b",
            r"\bproduction\b",
            r"\bgo[- ]live\b",
            r"\blaunch\b",
            r"\brollout\b",
            r"\bhandover\b",
            r"\buat\b",
        ],
        "reads": [
            "docs/checklists/pre-release.md",
            "docs/standards/security.md",
            "docs/standards/performance.md",
            "docs/standards/testing.md",
        ],
        "purpose": "Prove readiness, rollback, monitoring, UAT, and approval.",
    },
    "security-review": {
        "patterns": [
            r"\bsecurity\b",
            r"\bauth(entication|orization)?\b",
            r"\brbac\b",
            r"\bpermission(s)?\b",
            r"\bsecret(s)?\b",
            r"\bvulnerabilit(y|ies)\b",
            r"\bpenetration test\b",
            r"\bpentest\b",
            r"\bpayment\b",
            r"\bconfidential\b",
            r"\bpii\b",
            r"\bprivacy\b",
            r"\bmcp\b",
            r"\bhook(s)?\b",
        ],
        "reads": [
            "SECURITY.md",
            "docs/standards/security.md",
            "docs/standards/privacy-observability.md",
        ],
        "purpose": "Review secrets, permissions, hooks, MCP, privacy, and attack surface.",
    },    "reference-router": {
        "patterns": [
            r"\bfind (a )?skill\b",
            r"\binstall (a )?(skill|plugin|tool|mcp)\b",
            r"\bexternal (skill|plugin|tool|repository|repo|service)\b",
            r"\bopen[- ]source\b",
            r"\bgithub repo(sitory)?\b",
            r"\bplugin\b",
            r"\bskill marketplace\b",
            r"\buse .* as[- ]is\b",
            r"\binspiration\b",
            r"\breference catalogue\b",
        ],
        "reads": [
            "catalog/external-resources.json",
            "docs/REFERENCE_CATALOG.md",
            "SECURITY.md",
            "THIRD_PARTY_NOTICES.md",
        ],
        "purpose": "Select and govern external skills, plugins, repositories, CLIs, MCP servers, and services.",
    },
}

MATERIAL_PATTERNS = [
    r"\bbuild\b",
    r"\bcreate\b",
    r"\bmake\b",
    r"\bimplement\b",
    r"\badd\b",
    r"\bchange\b",
    r"\bupdate\b",
    r"\bfix\b",
    r"\bdebug\b",
    r"\brefactor\b",
    r"\breview\b",
    r"\bdesign\b",
    r"\btest\b",
    r"\bdeploy\b",
    r"\bintegrate\b",
    r"\banaly[sz]e\b",
    r"\baudit\b",
    r"\bplan\b",
    r"\bdraft\b",
    r"\bmigrate\b",
    r"\bspecify\b",
]

FULL_PATTERNS = [
    r"\bnew\b.{0,60}\b(app|application|product|platform|module|system)\b",
    r"\bfrom scratch\b",
    r"\bmajor architecture\b",
]

EXECUTE_PATTERNS = [
    r"\bbug\b",
    r"\bfix\b",
    r"\bapproved ticket\b",
    r"\bcopy change\b",
    r"\bsmall change\b",
    r"\bisolated\b",
    r"\btypo\b",
]

MODE_PRIORITY = {"NONE": 0, "EXECUTE": 1, "DELTA": 2, "FULL": 3}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_record_id(prefix: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"{prefix}:{sha256_bytes(canonical.encode('utf-8'))[:32]}"


def find_root() -> Path:
    starts: list[Path] = []
    for name in ("ESCAPEMENT_PROJECT_DIR", "CLAUDE_PROJECT_DIR"):
        value = os.getenv(name)
        if value:
            starts.append(Path(value))
    starts.extend([Path.cwd(), Path(__file__).resolve().parent])
    for start in starts:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists() and (candidate / "PROJECT_STATE.yaml").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()
RUNTIME = ROOT / ".agent" / "runtime"
TURN_FILE = RUNTIME / "current-turn.json"
ACTIVE_CONTEXT = RUNTIME / "ACTIVE_CONTEXT.md"
ACTIVE_SKILLS = RUNTIME / "ACTIVE_SKILLS.md"
SESSION_MEMORY = RUNTIME / "SESSION_MEMORY.md"
TURNS_LOG = RUNTIME / "turns.jsonl"
SKILL_LOG = ROOT / "logs" / "skill-usage.jsonl"
RUNS_ROOT = ROOT / ".agent" / "runs"


def ensure_runtime() -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    RUNS_ROOT.mkdir(parents=True, exist_ok=True)
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


def read_hook_input() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def read_simple_yaml(relative: str) -> dict[str, str]:
    path = ROOT / relative
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith((" ", "-")):
            continue
        if ":" in raw:
            key, value = raw.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def any_match(patterns: Iterable[str], text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def classify_material(prompt: str) -> bool:
    return any_match(MATERIAL_PATTERNS, prompt) or any(
        any_match(definition["patterns"], prompt)
        for definition in SKILLS.values()
    )


def classify_mode(prompt: str) -> str:
    if any_match(FULL_PATTERNS, prompt):
        return "FULL"
    if any_match(EXECUTE_PATTERNS, prompt):
        return "EXECUTE"
    state_mode = read_simple_yaml("PROJECT_STATE.yaml").get("work_mode", "")
    if state_mode in {"FULL", "DELTA", "EXECUTE"} and not re.search(
        r"\b(change|update|redesign|replace|integrate|material|migrate)\b",
        prompt,
        re.IGNORECASE,
    ):
        return state_mode
    return "DELTA"


def route_prompt(prompt: str) -> dict[str, Any]:
    material = classify_material(prompt)
    mode = classify_mode(prompt) if material else "NONE"
    reasons: dict[str, list[str]] = {}
    selected: list[str] = []

    if material:
        for name, definition in SKILLS.items():
            matched = [
                pattern
                for pattern in definition["patterns"]
                if re.search(pattern, prompt, re.IGNORECASE)
            ]
            if matched:
                selected.append(name)
                reasons[name] = matched

        if "design-system" in selected and any_match(
            [
                r"\bui\b",
                r"\bpage\b",
                r"\bscreen\b",
                r"\bcomponent\b",
                r"\bfrontend\b",
                r"\bbuild\b",
                r"\bredesign\b",
            ],
            prompt,
        ):
            if "enterprise-ui-review" not in selected:
                selected.append("enterprise-ui-review")
                reasons["enterprise-ui-review"] = ["paired-with-design-system"]

        if mode == "FULL" and "project-discovery" not in selected:
            selected.insert(0, "project-discovery")
            reasons["project-discovery"] = ["FULL-mode-default"]

        selected.append("skill-governance")
        reasons["skill-governance"] = ["material-turn-evidence"]

    ordered: list[str] = []
    for name in selected:
        if name not in ordered:
            ordered.append(name)

    truncated: list[str] = []
    if len(ordered) > 4:
        keep = [name for name in ordered if name != "skill-governance"][:3]
        truncated = [name for name in ordered if name not in keep and name != "skill-governance"]
        ordered = keep + ["skill-governance"]

    reads = [
        "AGENTS.md",
        "AGENT_RUNTIME.md",
        "PROJECT_STATE.yaml",
        "feature_list.json",
        ".agent/runtime/SESSION_MEMORY.md",
    ]
    for skill in ordered:
        if skill == "skill-governance":
            reads.extend([
                "docs/standards/harness-engineering.md",
                "docs/standards/context-engineering.md",
            ])
        else:
            reads.extend(SKILLS.get(skill, {}).get("reads", []))

    return {
        "material": material,
        "mode": mode,
        "skills": ordered,
        "reasons": reasons,
        "truncated_skills": truncated,
        "required_reads": list(dict.fromkeys(reads)),
    }


def emit_hook_context(event: str, context: str, system_message: str | None = None) -> None:
    payload: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": context,
        }
    }
    if system_message:
        payload["systemMessage"] = system_message
    print(json.dumps(payload))


def load_turn() -> dict[str, Any] | None:
    if not TURN_FILE.exists():
        return None
    try:
        value = json.loads(TURN_FILE.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def save_turn(turn: dict[str, Any]) -> None:
    turn["updated_at"] = utc_now()
    TURN_FILE.write_text(
        json.dumps(turn, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_active_files(turn: dict[str, Any]) -> None:
    state = read_simple_yaml("PROJECT_STATE.yaml")
    skills = turn.get("skills", [])
    required_reads = turn.get("required_reads", [])
    history = turn.get("prompt_history", [])
    latest = history[-1]["prompt"] if history else ""

    ACTIVE_CONTEXT.write_text(
        f"""# Active Context

- Escapement version: {VERSION}
- Turn ID: {turn['turn_id']}
- Started: {turn['started_at']}
- Status: {turn['status']}
- Material: {str(turn['material']).lower()}
- Mode: {turn['mode']}
- Current request: {latest}
- Prompt count: {len(history)}
- Project: {state.get('project_name', 'TBD')}
- Phase: {state.get('phase', 'TBD')}
- Implementation authorised: {state.get('implementation_authorized', 'false')}
- Approved ticket: {state.get('approved_ticket', 'null')}

## Mandatory Reads

{chr(10).join(f'- `{path}`' for path in required_reads)}

## Selected Skills

{chr(10).join(f'- `{skill}`' for skill in skills) if skills else '- None'}

## Turn Contract

1. Continue this open turn; do not replace it silently.
2. Read `ACTIVE_SKILLS.md`.
3. Invoke every selected native skill.
4. Execute one bounded feature or task.
5. Capture checks through `scripts/run_check.py`.
6. Update shared state where material.
7. Close the turn with structured evidence before the final response.

## Approval Gates

Pause before schema, authentication, RBAC, destructive, production,
paid-service, confidential-data, new-integration, or material-scope changes.
""",
        encoding="utf-8",
    )

    lines = [
        "# Active Skills",
        "",
        f"- Turn ID: {turn['turn_id']}",
        f"- Mode: {turn['mode']}",
        "",
    ]
    if not skills:
        lines.append("No native skill selected.")
    for skill in skills:
        purpose = (
            "Record selection, outputs, checks, evidence, and closure truthfully."
            if skill == "skill-governance"
            else SKILLS.get(skill, {}).get("purpose", "")
        )
        reason = ", ".join(turn.get("route_reasons", {}).get(skill, [])) or "runtime selection"
        lines.extend([
            f"## {skill}",
            "",
            f"- Purpose: {purpose}",
            f"- Selected because: {reason}",
            f"- Codex: `${skill}`",
            f"- Claude Code: `/{skill}`",
            f"- Codex file: `.agents/skills/{skill}/SKILL.md`",
            f"- Claude Code file: `.claude/skills/{skill}/SKILL.md`",
            "",
        ])
    ACTIVE_SKILLS.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def create_turn(prompt: str, hook_data: dict[str, Any] | None = None) -> dict[str, Any]:
    route = route_prompt(prompt)
    started = utc_now()
    turn = {
        "runtime_version": VERSION,
        "turn_id": f"TURN-{uuid.uuid4().hex[:12]}",
        "session_id": (hook_data or {}).get("session_id")
        or os.getenv("CODEX_SESSION_ID")
        or "unknown",
        "started_at": started,
        "updated_at": started,
        "material": route["material"],
        "mode": route["mode"],
        "skills": route["skills"],
        "route_reasons": route["reasons"],
        "required_reads": route["required_reads"],
        "truncated_skills": route["truncated_skills"],
        "status": "open" if route["material"] else "informational",
        "close_required": route["material"],
        "stop_blocks": 0,
        "prompt_history": [{
            "timestamp": started,
            "prompt": prompt.strip(),
            "sha256": sha256_bytes(prompt.encode("utf-8")),
            "material": route["material"],
            "mode": route["mode"],
        }],
        "closure": None,
    }
    save_turn(turn)
    write_active_files(turn)
    return turn


def continue_turn(turn: dict[str, Any], prompt: str) -> dict[str, Any]:
    route = route_prompt(prompt)
    turn.setdefault("prompt_history", []).append({
        "timestamp": utc_now(),
        "prompt": prompt.strip(),
        "sha256": sha256_bytes(prompt.encode("utf-8")),
        "material": route["material"],
        "mode": route["mode"],
    })
    turn["material"] = bool(turn.get("material")) or bool(route["material"])
    if MODE_PRIORITY.get(route["mode"], 0) > MODE_PRIORITY.get(turn.get("mode", "NONE"), 0):
        turn["mode"] = route["mode"]

    skills = list(turn.get("skills", []))
    for skill in route["skills"]:
        if skill not in skills:
            skills.append(skill)
    if len(skills) > 4:
        non_governance = [name for name in skills if name != "skill-governance"][:3]
        skills = non_governance + (
            ["skill-governance"] if "skill-governance" in skills else []
        )
    turn["skills"] = skills

    reasons = turn.setdefault("route_reasons", {})
    for skill, matched in route["reasons"].items():
        current = reasons.setdefault(skill, [])
        for item in matched:
            if item not in current:
                current.append(item)

    turn["required_reads"] = list(dict.fromkeys(
        turn.get("required_reads", []) + route["required_reads"]
    ))
    turn["continuation_count"] = int(turn.get("continuation_count", 0)) + 1
    save_turn(turn)
    write_active_files(turn)
    return turn


def start_or_continue(
    prompt: str,
    hook_data: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], bool]:
    ensure_runtime()
    current = load_turn()
    if current and current.get("status") == "open" and current.get("close_required"):
        return continue_turn(current, prompt), True
    return create_turn(prompt, hook_data), False


def split_values(value: str | None, separator: str = ",") -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(separator) if part.strip()]


def existing_paths(values: list[str]) -> tuple[list[str], list[str]]:
    present: list[str] = []
    missing: list[str] = []
    for value in values:
        if value.startswith(("http://", "https://")):
            present.append(value)
        elif (ROOT / value).exists():
            present.append(value)
        else:
            missing.append(value)
    return present, missing


def load_check_records(
    paths: list[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    required = {
        "record_type",
        "record_id",
        "schema_version",
        "name",
        "command",
        "started_at",
        "completed_at",
        "exit_code",
        "result",
        "stdout_path",
        "stderr_path",
    }
    root_resolved = ROOT.resolve()

    for value in paths:
        path = (ROOT / value).resolve()
        try:
            path.relative_to(root_resolved)
        except ValueError:
            errors.append(f"check record outside repository: {value}")
            continue
        if not path.exists():
            errors.append(f"check record missing: {value}")
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid check record {value}: {exc}")
            continue

        missing = required - set(record)
        if missing:
            errors.append(f"check record {value} missing {sorted(missing)}")
            continue
        if record.get("record_type") != "check":
            errors.append(f"check record {value} has wrong record_type")
            continue

        expected_id = stable_record_id(
            "check",
            {
                "name": record["name"],
                "command": record["command"],
                "started_at": record["started_at"],
                "completed_at": record["completed_at"],
                "exit_code": record["exit_code"],
                "stdout_sha256": record.get("stdout_sha256"),
                "stderr_sha256": record.get("stderr_sha256"),
            },
        )
        if record.get("record_id") != expected_id:
            errors.append(f"check record {value} content hash mismatch")
            continue
        records.append(record)

    return records, errors


def compute_scores(
    *,
    selected_skills: list[str],
    used_skills: list[str],
    files_present: bool,
    check_records: list[dict[str, Any]],
    critical_failure: bool,
) -> dict[str, int]:
    all_checks_pass = bool(check_records) and all(
        int(record["exit_code"]) == 0 and record.get("result") == "PASS"
        for record in check_records
    )
    skills_covered = set(selected_skills).issubset(set(used_skills))
    return {
        "trigger_accuracy": 15,
        "procedure_adherence": 20 if skills_covered else 8,
        "output_correctness": 30 if files_present and not critical_failure else 8,
        "validation_evidence": 20 if all_checks_pass else (8 if check_records else 0),
        "efficiency": 10,
        "clarity": 5,
    }


def command_session_start(_: argparse.Namespace) -> int:
    ensure_runtime()
    state = read_simple_yaml("PROJECT_STATE.yaml")
    emit_hook_context(
        "SessionStart",
        "Escapement runtime active. Read AGENTS.md, PROJECT_STATE.yaml, "
        "feature_list.json, ACTIVE_CONTEXT.md, ACTIVE_SKILLS.md, and "
        "SESSION_MEMORY.md before material work. "
        f"Project={state.get('project_name', 'TBD')}; "
        f"phase={state.get('phase', 'TBD')}; "
        f"mode={state.get('work_mode', 'TBD')}.",
        "Escapement runtime bootstrap loaded",
    )
    return 0


def command_prompt(_: argparse.Namespace) -> int:
    data = read_hook_input()
    prompt = str(
        data.get("prompt")
        or data.get("user_prompt")
        or data.get("message")
        or ""
    )
    if not prompt:
        return 0

    turn, continued = start_or_continue(prompt, data)
    if not turn["material"]:
        emit_hook_context(
            "UserPromptSubmit",
            "Informational prompt: no material runtime turn is required.",
        )
        return 0

    invocations = ", ".join(
        f"{skill} (Codex `${skill}` / Claude `/{skill}`)"
        for skill in turn["skills"]
    )
    action = "continued" if continued else "opened"
    emit_hook_context(
        "UserPromptSubmit",
        f"Escapement {action} material turn {turn['turn_id']}. "
        f"Mode={turn['mode']}. Selected skills: {invocations}. "
        "Read ACTIVE_CONTEXT.md and ACTIVE_SKILLS.md, invoke all selected skills, "
        "work on one bounded feature, capture checks with run_check.py, and close "
        "the turn with structured evidence before the final response.",
        f"Escapement route: {turn['mode']} | {', '.join(turn['skills'])}",
    )
    return 0


def command_manual_start(args: argparse.Namespace) -> int:
    turn, continued = start_or_continue(args.prompt, {})
    payload = {
        "turn_id": turn["turn_id"],
        "continued": continued,
        "material": turn["material"],
        "mode": turn["mode"],
        "skills": turn["skills"],
        "required_reads": turn["required_reads"],
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Turn: {turn['turn_id']}")
        print(f"Continued: {continued}")
        print(f"Material: {turn['material']}")
        print(f"Mode: {turn['mode']}")
        print(f"Skills: {', '.join(turn['skills']) or 'None'}")
    return 0


def command_explain(args: argparse.Namespace) -> int:
    route = route_prompt(args.prompt)
    if args.json:
        print(json.dumps(route, indent=2))
        return 0

    print(f"Material: {route['material']}")
    print(f"Mode: {route['mode']}")
    print("Skills:")
    for skill in route["skills"]:
        reasons = ", ".join(route["reasons"].get(skill, []))
        print(f"  - {skill}: {reasons}")
    if route["truncated_skills"]:
        print(f"Budget-rejected: {', '.join(route['truncated_skills'])}")
    print("Required reads:")
    for path in route["required_reads"]:
        print(f"  - {path}")
    return 0


def command_stop(_: argparse.Namespace) -> int:
    data = read_hook_input()
    turn = load_turn()
    if not turn or turn.get("status") != "open" or not turn.get("close_required"):
        return 0

    if bool(data.get("stop_hook_active")) or int(turn.get("stop_blocks", 0)) >= 1:
        turn["runtime_warning"] = (
            "Agent stopped with an open turn after the one allowed continuation."
        )
        save_turn(turn)
        append_jsonl(
            TURNS_LOG,
            {
                "turn_id": turn["turn_id"],
                "timestamp": utc_now(),
                "event": "stop-allowed-open-turn",
            },
        )
        return 0

    turn["stop_blocks"] = int(turn.get("stop_blocks", 0)) + 1
    save_turn(turn)
    reason = (
        f"Escapement turn {turn['turn_id']} remains open. "
        "Invoke unused selected skills, update shared state, capture structured "
        "checks with scripts/run_check.py, then run close-turn with "
        "--skills-used, --check-records, files, and evidence."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


def command_close(args: argparse.Namespace) -> int:
    ensure_runtime()
    turn = load_turn()
    if not turn:
        print("FAIL: no runtime turn exists.", file=sys.stderr)
        return 1
    if turn.get("status") == "closed":
        print("Turn already closed.")
        return 0

    files_requested = split_values(args.files)
    evidence_requested = split_values(args.evidence)
    used_skills = split_values(args.skills_used)
    check_paths = split_values(args.check_records)

    files_present, missing_files = existing_paths(files_requested)
    evidence_present, missing_evidence = existing_paths(evidence_requested)
    check_records, check_errors = load_check_records(check_paths)

    selected_skills = list(turn.get("skills", []))
    skills_covered = set(selected_skills).issubset(set(used_skills))
    checks_pass = bool(check_records) and all(
        int(record["exit_code"]) == 0 and record.get("result") == "PASS"
        for record in check_records
    )

    errors: list[str] = []
    if args.result == "PASS":
        if args.critical_failure:
            errors.append("critical_failure cannot be PASS")
        if missing_files:
            errors.append(f"missing output files: {missing_files}")
        if missing_evidence:
            errors.append(f"missing evidence paths: {missing_evidence}")
        errors.extend(check_errors)
        if not check_records:
            errors.append("PASS requires at least one structured check record")
        if not checks_pass:
            errors.append("PASS requires every structured check to pass")
        if not skills_covered:
            errors.append(
                "PASS requires every selected skill to be declared used: "
                f"{selected_skills}"
            )

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    result = "FAIL" if args.critical_failure else args.result
    scores = compute_scores(
        selected_skills=selected_skills,
        used_skills=used_skills,
        files_present=not missing_files,
        check_records=check_records,
        critical_failure=args.critical_failure,
    )
    total_score = sum(scores.values())
    if result == "PASS" and total_score < 85:
        result = "PARTIAL"

    closure = {
        "closed_at": utc_now(),
        "summary": args.summary,
        "next_action": args.next,
        "files": files_present,
        "missing_files": missing_files,
        "skills_used": used_skills,
        "check_records": check_paths,
        "evidence": evidence_present,
        "missing_evidence": missing_evidence,
        "result": result,
        "critical_failure": args.critical_failure,
        "blockers": args.blockers or "None recorded",
        "scores": scores,
        "total_score": total_score,
    }

    turn["status"] = "closed"
    turn["close_required"] = False
    turn["closure"] = closure
    save_turn(turn)
    append_jsonl(TURNS_LOG, turn)

    memory = f"""# Session Memory

- Last completed turn: {turn['turn_id']}
- Closed: {closure['closed_at']}
- Mode: {turn['mode']}
- Skills selected: {', '.join(selected_skills) or 'None'}
- Skills used: {', '.join(used_skills) or 'None'}
- Summary: {closure['summary']}
- Files: {', '.join(files_present) or 'None recorded'}
- Check records: {', '.join(check_paths) or 'None recorded'}
- Evidence: {', '.join(evidence_present) or 'None recorded'}
- Result: {result}
- Blockers: {closure['blockers']}
- Next action: {closure['next_action']}
"""
    SESSION_MEMORY.write_text(memory, encoding="utf-8")
    (ROOT / "SESSION_HANDOFF.md").write_text(
        memory.replace("# Session Memory", "# Session Handoff"),
        encoding="utf-8",
    )

    run_dir = RUNS_ROOT / turn["turn_id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "turn.json").write_text(
        json.dumps(turn, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for skill in selected_skills:
        base_record = {
            "record_type": "skill-run",
            "schema_version": "2.0",
            "task_id": turn["turn_id"],
            "skill": skill,
            "version": VERSION,
            "trigger": turn.get("prompt_history", [{}])[-1].get("prompt", "")[:500],
            "selected_because": turn.get("route_reasons", {}).get(skill, []),
            "actual_output": files_present,
            "check_records": check_paths,
            "evidence": evidence_present,
            "scores": scores,
            "total_score": total_score,
            "result": result,
            "critical_failure": args.critical_failure,
            "retry_count": int(turn.get("stop_blocks", 0)),
            "turns_used": len(turn.get("prompt_history", [])),
            "timestamp": closure["closed_at"],
        }
        base_record["record_id"] = stable_record_id("skill", base_record)
        append_jsonl(SKILL_LOG, base_record)

    write_active_files(turn)
    print(f"Closed {turn['turn_id']} with result {result}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    ensure_runtime()
    payload = {
        "runtime_version": VERSION,
        "root": str(ROOT),
        "turn": load_turn(),
    }
    print(json.dumps(payload, indent=2))
    return 0


def command_reset(args: argparse.Namespace) -> int:
    ensure_runtime()
    turn = load_turn() or {}
    append_jsonl(
        TURNS_LOG,
        {
            "turn_id": turn.get("turn_id", "unknown"),
            "timestamp": utc_now(),
            "event": "reset-turn",
            "reason": args.reason,
        },
    )
    TURN_FILE.unlink(missing_ok=True)
    ACTIVE_CONTEXT.write_text(
        "# Active Context\n\nNo active material turn. Previous turn was reset.\n",
        encoding="utf-8",
    )
    ACTIVE_SKILLS.write_text(
        "# Active Skills\n\nNo active skills.\n",
        encoding="utf-8",
    )
    print("Runtime turn reset.")
    return 0


def command_doctor(_: argparse.Namespace) -> int:
    ensure_runtime()
    required = [
        "AGENTS.md",
        "AGENT_RUNTIME.md",
        "PROJECT_STATE.yaml",
        "feature_list.json",
        "CLAUDE.md",
        ".codex/hooks.json",
        ".claude/settings.json",
        "scripts/agent_runtime.py",
        "scripts/run_check.py",
        "scripts/feature_list.py",
    ]
    failures = 0
    print("ESCAPEMENT RUNTIME DOCTOR")
    for relative in required:
        ok = (ROOT / relative).exists()
        print(f"[{'PASS' if ok else 'FAIL'}] {relative}")
        failures += int(not ok)

    for skill in [*SKILLS.keys(), "skill-governance"]:
        codex = ROOT / ".agents" / "skills" / skill / "SKILL.md"
        claude = ROOT / ".claude" / "skills" / skill / "SKILL.md"
        canonical = ROOT / "skills" / skill / "SKILL.md"
        ok = codex.exists() and claude.exists() and canonical.exists()
        print(f"[{'PASS' if ok else 'FAIL'}] native skill {skill}")
        failures += int(not ok)

    print(f"\nFailures: {failures}")
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent_runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("session-start").set_defaults(func=command_session_start)
    sub.add_parser("prompt").set_defaults(func=command_prompt)
    sub.add_parser("stop").set_defaults(func=command_stop)
    sub.add_parser("status").set_defaults(func=command_status)
    sub.add_parser("doctor").set_defaults(func=command_doctor)

    manual = sub.add_parser("manual-start")
    manual.add_argument("--prompt", required=True)
    manual.add_argument("--json", action="store_true")
    manual.set_defaults(func=command_manual_start)

    explain = sub.add_parser("explain")
    explain.add_argument("--prompt", required=True)
    explain.add_argument("--json", action="store_true")
    explain.set_defaults(func=command_explain)

    close = sub.add_parser("close-turn")
    close.add_argument("--summary", required=True)
    close.add_argument("--next", required=True)
    close.add_argument("--files", default="")
    close.add_argument("--skills-used", default="")
    close.add_argument("--check-records", default="")
    close.add_argument("--evidence", default="")
    close.add_argument("--blockers", default="")
    close.add_argument(
        "--result",
        choices=["PASS", "PARTIAL", "FAIL", "NOT_NEEDED", "REDUNDANT"],
        default="PASS",
    )
    close.add_argument("--critical-failure", action="store_true")
    close.set_defaults(func=command_close)

    reset = sub.add_parser("reset-turn")
    reset.add_argument("--reason", required=True)
    reset.set_defaults(func=command_reset)

    return parser


def main() -> int:
    ensure_runtime()
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
