#!/usr/bin/env python3
"""Escapement v6.3 capability-strength runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from capability_router import build_context_pack, find_root, route_prompt  # noqa: E402
from run_check import sha256_file, stable_record_id  # noqa: E402

VERSION = "6.3.0"
ROOT = find_root()
RUNTIME = ROOT / ".agent" / "runtime"
TURN = RUNTIME / "current-turn.json"
ACTIVE_CONTEXT = RUNTIME / "ACTIVE_CONTEXT.md"
CONTEXT_PACK = RUNTIME / "CONTEXT_PACK.md"
SESSION_MEMORY = RUNTIME / "SESSION_MEMORY.md"
TURNS_LOG = RUNTIME / "turns.jsonl"
SKILL_LOG = ROOT / "logs" / "skill-usage.jsonl"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure() -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    SKILL_LOG.parent.mkdir(parents=True, exist_ok=True)
    seeds = {
        ACTIVE_CONTEXT: "# Active Context\n\nNo active material turn.\n",
        CONTEXT_PACK: "# Active Context Pack\n\nNo active material turn.\n",
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


def emit(event: str, context: str, message: str | None = None) -> None:
    payload: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": context,
        }
    }
    if message:
        payload["systemMessage"] = message
    print(json.dumps(payload))


def load_turn() -> dict[str, Any] | None:
    if not TURN.exists():
        return None
    try:
        value = json.loads(TURN.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def save_turn(value: dict[str, Any]) -> None:
    value["updated_at"] = now()
    TURN.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


VALID_PHASE_IDS = [
    "ORIENT", "DISCOVER", "RESEARCH", "BRAINSTORM",
    "SPECIFY", "PLAN", "IMPLEMENT", "VERIFY", "POLISH", "RELEASE",
]


def load_phase_catalog() -> dict[str, dict[str, Any]]:
    path = ROOT / "catalog" / "phase-capabilities.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data["phases"]}


def build_phase_entry(phase_id: str) -> dict[str, Any]:
    definition = load_phase_catalog()[phase_id]
    return {
        "id": phase_id,
        "purpose": definition["purpose"],
        "native_skills": definition.get("native_skills", []),
        "doctrine_packs": definition.get("doctrine_packs", []),
        "external_candidates": [],
        "outputs": definition.get("outputs", []),
        "capability_strengths": definition.get("capability_strengths", []),
    }


def apply_phase_overrides(route: dict[str, Any], overrides: list[dict[str, Any]]) -> None:
    """Reapply durable phase-plan revisions after route_prompt recomputes phase_plan.

    route_prompt() always rebuilds phase_plan deterministically from the prompt and
    tier alone -- it has no memory of prior turns. Without this, a phase added or
    removed via replan-phases would silently revert on the very next advance-phase
    call or continued prompt, since both recompute the whole route from scratch.
    """
    plan = list(route.get("phase_plan", []))
    ids = [item["id"] for item in plan]
    for override in overrides:
        if override["action"] == "add" and override["phase"] not in ids:
            plan.append(build_phase_entry(override["phase"]))
            ids.append(override["phase"])
        elif override["action"] == "remove" and override["phase"] in ids:
            plan = [item for item in plan if item["id"] != override["phase"]]
            ids.remove(override["phase"])
    route["phase_plan"] = plan


def write_context(turn: dict[str, Any]) -> None:
    latest_prompt = turn["prompt_history"][-1]["prompt"]
    route = turn["route"]
    skills = [item["id"] for item in route["native_skills"]]
    packs = [item["id"] for item in route["doctrine_packs"]]
    strengths = [item["id"] for item in route.get("capability_strengths", [])]
    overrides = turn.get("phase_plan_overrides", [])
    revisions = "\n".join(
        f"- {item['action']} `{item['phase']}`: {item['reason']}" for item in overrides
    ) or "None"

    ACTIVE_CONTEXT.write_text(
        f"""# Active Context

- Turn: `{turn['turn_id']}`
- Tier: `{route['tier']}`
- Mode: `{route['mode']}`
- Register: `{route['register']}`
- Profile: `{route['profile']}`
- Current phase: `{route['current_phase']}`
- Status: `{turn['status']}`
- Request: {latest_prompt}
- Doctrine: {', '.join(packs) or 'kernel only'}
- Skills: {', '.join(skills) or 'none'}
- Capability strengths: {', '.join(strengths) or 'none'}
- Context estimate: {route['context_cost']['total']} / {route['context_cost']['budget']} words
- Phase plan revisions: {len(overrides)}
{revisions}

## Work Contract

- Stay within the declared tier.
- Read `CONTEXT_PACK.md`.
- Invoke each selected native skill.
- Apply the current phase's capability strengths; install or load external candidates only after approval.
- Do not activate external candidates without overlap, licence, security, and approval review.
- Keep development primary; create only tier-required process artefacts.
- Close the turn truthfully.
""",
        encoding="utf-8",
    )
    CONTEXT_PACK.write_text(build_context_pack(latest_prompt, route), encoding="utf-8")


def combine_prompts(turn: dict[str, Any], prompt: str) -> str:
    prompts = [item["prompt"] for item in turn.get("prompt_history", [])]
    prompts.append(prompt)
    return "\n".join(prompts)


def start_or_continue(prompt: str, data: dict[str, Any] | None = None) -> tuple[dict[str, Any], bool]:
    ensure()
    current = load_turn()
    if current and current.get("status") == "open":
        current.setdefault("prompt_history", []).append({
            "timestamp": now(),
            "prompt": prompt.strip(),
            "sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        })
        current_phase = current.get("route", {}).get("current_phase")
        current["route"] = route_prompt(
            combine_prompts(
                {**current, "prompt_history": current["prompt_history"][:-1]},
                prompt,
            ),
            phase_override=current_phase,
        )
        apply_phase_overrides(current["route"], current.get("phase_plan_overrides", []))
        current["continuation_count"] = int(current.get("continuation_count", 0)) + 1
        save_turn(current)
        write_context(current)
        return current, True

    route = route_prompt(prompt)
    if route["tier"] == "INFO":
        value = {
            "runtime_version": VERSION,
            "turn_id": None,
            "status": "informational",
            "route": route,
            "prompt_history": [{"timestamp": now(), "prompt": prompt.strip()}],
        }
        ACTIVE_CONTEXT.write_text("# Active Context\n\nInformational request; no runtime turn.\n", encoding="utf-8")
        CONTEXT_PACK.write_text(build_context_pack(prompt, route), encoding="utf-8")
        return value, False

    value = {
        "runtime_version": VERSION,
        "turn_id": f"TURN-{uuid.uuid4().hex[:12]}",
        "session_id": (data or {}).get("session_id") or os.getenv("CODEX_SESSION_ID") or "unknown",
        "started_at": now(),
        "updated_at": now(),
        "status": "open",
        "stop_blocks": 0,
        "prompt_history": [{
            "timestamp": now(),
            "prompt": prompt.strip(),
            "sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        }],
        "route": route,
        "closure": None,
    }
    save_turn(value)
    write_context(value)
    return value, False


def split(value: str | None, separator: str = ",") -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(separator) if part.strip()]


def existing(values: list[str]) -> tuple[list[str], list[str]]:
    present, missing = [], []
    for value in values:
        if value.startswith(("http://", "https://")) or (ROOT / value).exists():
            present.append(value)
        else:
            missing.append(value)
    return present, missing


CHECK_RECORD_REQUIRED_FIELDS = {
    "record_type", "record_id", "schema_version", "name", "command",
    "started_at", "completed_at", "exit_code", "result",
    "stdout_path", "stderr_path", "stdout_sha256", "stderr_sha256",
}


def load_checks(paths: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    """Load and authenticate structured check records.

    A record is accepted only if its stdout/stderr output exists on disk with
    hashes matching the record, and its record_id equals the content hash
    run_check.py would compute -- so a hand-written record claiming a PASS
    that never actually ran is rejected. See schemas/check-record.schema.json.
    """
    records, errors = [], []
    for relative in paths:
        path = (ROOT / relative).resolve()
        try:
            path.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"outside repository: {relative}")
            continue
        if not path.exists():
            errors.append(f"missing check record: {relative}")
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid check record {relative}: {exc}")
            continue
        missing = CHECK_RECORD_REQUIRED_FIELDS - set(record)
        if missing:
            errors.append(f"incomplete check record {relative}: missing {sorted(missing)}")
            continue
        if record.get("record_type") != "check":
            errors.append(f"wrong record type: {relative}")
            continue

        stdout_path = (ROOT / record["stdout_path"]).resolve()
        stderr_path = (ROOT / record["stderr_path"]).resolve()
        try:
            stdout_path.relative_to(ROOT.resolve())
            stderr_path.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"check record output paths outside repository: {relative}")
            continue
        if not stdout_path.exists() or not stderr_path.exists():
            errors.append(f"check record output missing on disk: {relative}")
            continue

        actual_stdout_sha256 = sha256_file(stdout_path)
        actual_stderr_sha256 = sha256_file(stderr_path)
        if (
            record["stdout_sha256"] != actual_stdout_sha256
            or record["stderr_sha256"] != actual_stderr_sha256
        ):
            errors.append(f"check record output does not match its recorded hash: {relative}")
            continue

        identity = {
            "name": record["name"],
            "command": record["command"],
            "started_at": record["started_at"],
            "completed_at": record["completed_at"],
            "exit_code": record["exit_code"],
            "stdout_sha256": actual_stdout_sha256,
            "stderr_sha256": actual_stderr_sha256,
        }
        if record["record_id"] != stable_record_id(identity):
            errors.append(f"check record does not match its own content -- forged or tampered: {relative}")
            continue

        records.append(record)
    return records, errors


def command_session(_: argparse.Namespace) -> int:
    ensure()
    emit(
        "SessionStart",
        "Escapement v6.3 is active. Read AGENTS.md, ACTIVE_CONTEXT.md, and "
        "CONTEXT_PACK.md. Load deeper state only when the context pack points to it.",
        "Escapement low-token kernel loaded",
    )
    return 0


def command_prompt(_: argparse.Namespace) -> int:
    data = hook_input()
    prompt = str(data.get("prompt") or data.get("user_prompt") or data.get("message") or "")
    if not prompt:
        return 0
    turn, continued = start_or_continue(prompt, data)
    route = turn["route"]
    if route["tier"] == "INFO":
        emit("UserPromptSubmit", "Informational request: no material runtime turn.")
        return 0

    skills = ", ".join(item["id"] for item in route["native_skills"]) or "none"
    packs = ", ".join(item["id"] for item in route["doctrine_packs"]) or "kernel only"
    action = "continued" if continued else "opened"
    emit(
        "UserPromptSubmit",
        f"Escapement {action} {route['tier']} turn {turn['turn_id']}. "
        f"Register={route['register']}; phase={route['current_phase']}; doctrine={packs}; skills={skills}; "
        f"context={route['context_cost']['total']}/{route['context_cost']['budget']} words. "
        "Read CONTEXT_PACK.md, invoke selected skills, and stay within tier.",
        f"Escapement: {route['tier']} | {route['register']} | {skills}",
    )
    return 0


def command_manual(args: argparse.Namespace) -> int:
    turn, continued = start_or_continue(args.prompt, {})
    route = turn["route"]
    payload = {
        "turn_id": turn.get("turn_id"),
        "continued": continued,
        "tier": route["tier"],
        "mode": route["mode"],
        "register": route["register"],
        "profile": route["profile"],
        "current_phase": route["current_phase"],
        "material_questions": route["decision_brief"]["questions"],
        "improved_prompt": route["decision_brief"]["improved_prompt"],
        "phase_plan": [item["id"] for item in route["phase_plan"]],
        "research_plan": route["research_plan"],
        "parallel_assessment": route["parallel_assessment"],
        "doctrine_packs": [item["id"] for item in route["doctrine_packs"]],
        "native_skills": [item["id"] for item in route["native_skills"]],
        "capability_strengths": [item["id"] for item in route.get("capability_strengths", [])],
        "capability_readiness": route.get("capability_readiness", {}),
        "external_candidates": [item["id"] for item in route["external_candidates"]],
        "context_cost": route["context_cost"],
    }
    print(json.dumps(payload, indent=2) if args.json else "\n".join(
        f"{key}: {value}" for key, value in payload.items()
    ))
    return 0


def command_explain(args: argparse.Namespace) -> int:
    route = route_prompt(args.prompt)
    print(json.dumps(route, indent=2))
    return 0



def command_advance(args: argparse.Namespace) -> int:
    """Persist the current phase and load the next phase-specific context."""
    ensure()
    turn = load_turn()
    if not turn or turn.get("status") != "open":
        print("FAIL: no open runtime turn.", file=sys.stderr)
        return 1

    route = turn["route"]
    current_phase = route["current_phase"]
    valid_phases = [item["id"] for item in route.get("phase_plan", [])]
    if args.phase not in valid_phases:
        print(
            f"FAIL: {args.phase} is not in the active phase plan: {valid_phases}",
            file=sys.stderr,
        )
        return 1
    if args.phase == current_phase:
        print(f"Already in phase {current_phase}.")
        return 0

    selected_skills = [item["id"] for item in route.get("native_skills", [])]
    used_skills = split(args.skills_used)
    files, missing_files = existing(split(args.files))
    evidence, missing_evidence = existing(split(args.evidence))
    check_paths = split(args.check_records)
    check_records, check_errors = load_checks(check_paths)

    errors = []
    if not set(selected_skills).issubset(set(used_skills)):
        errors.append(f"selected skills not declared used: {selected_skills}")
    if missing_files:
        errors.append(f"missing phase files: {missing_files}")
    if missing_evidence:
        errors.append(f"missing phase evidence: {missing_evidence}")
    if current_phase in {"IMPLEMENT", "VERIFY", "POLISH", "RELEASE"}:
        errors.extend(check_errors)
        if not check_records and not args.no_check_reason:
            errors.append(
                f"{current_phase} phase requires structured checks or --no-check-reason"
            )
        if check_records and not all(
            int(record.get("exit_code", 1)) == 0
            and record.get("result") == "PASS"
            for record in check_records
        ):
            errors.append("one or more phase checks failed")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    phase_record = {
        "phase": current_phase,
        "completed_at": now(),
        "summary": args.summary,
        "skills_selected": selected_skills,
        "skills_used": used_skills,
        "files": files,
        "check_records": check_paths,
        "no_check_reason": args.no_check_reason,
        "evidence": evidence,
        "next_phase": args.phase,
    }
    turn.setdefault("phase_history", []).append(phase_record)

    combined = "\n".join(
        item["prompt"] for item in turn.get("prompt_history", [])
    )
    turn["route"] = route_prompt(combined, phase_override=args.phase)
    apply_phase_overrides(turn["route"], turn.get("phase_plan_overrides", []))
    turn["stop_blocks"] = 0
    save_turn(turn)
    write_context(turn)
    append_jsonl(
        TURNS_LOG,
        {
            "turn_id": turn["turn_id"],
            "event": "phase-advanced",
            **phase_record,
        },
    )
    print(f"Advanced {turn['turn_id']} from {current_phase} to {args.phase}")
    return 0


def command_replan(args: argparse.Namespace) -> int:
    """Add or remove a phase from the current turn's plan.

    phase_plan() in capability_router.py decides which of the ten phases apply
    using keyword patterns matched against the prompt, computed once at turn
    start. It cannot see what DISCOVER's own inspection actually turns up. This
    command is the lever for when that inspection reveals the default plan is
    wrong -- e.g. a security-sensitive constraint surfaces that never triggered
    VERIFY's security-review routing because the prompt never said "security".
    """
    ensure()
    turn = load_turn()
    if not turn or turn.get("status") != "open":
        print("FAIL: no open runtime turn.", file=sys.stderr)
        return 1

    action = "add" if args.add_phase else "remove"
    phase = args.add_phase or args.remove_phase
    reason = args.reason.strip()
    if not reason:
        print("FAIL: --reason is required.", file=sys.stderr)
        return 1

    route = turn["route"]
    plan_ids = [item["id"] for item in route.get("phase_plan", [])]
    completed_phases = {item["phase"] for item in turn.get("phase_history", [])}
    current_phase = route["current_phase"]

    if action == "add" and phase in plan_ids:
        print(f"FAIL: {phase} is already in the phase plan.", file=sys.stderr)
        return 1
    if action == "remove":
        if phase not in plan_ids:
            print(f"FAIL: {phase} is not in the phase plan.", file=sys.stderr)
            return 1
        if phase == current_phase:
            print(f"FAIL: cannot remove the current phase ({phase}).", file=sys.stderr)
            return 1
        if phase in completed_phases:
            print(
                f"FAIL: cannot remove {phase} -- already completed with recorded evidence.",
                file=sys.stderr,
            )
            return 1

    override = {"action": action, "phase": phase, "reason": reason, "recorded_at": now()}
    turn.setdefault("phase_plan_overrides", []).append(override)
    apply_phase_overrides(route, turn["phase_plan_overrides"])
    save_turn(turn)
    write_context(turn)
    append_jsonl(TURNS_LOG, {"turn_id": turn["turn_id"], "event": "phase-plan-revised", **override})

    verb = "Added" if action == "add" else "Removed"
    preposition = "to" if action == "add" else "from"
    print(f"{verb} {phase} {preposition} the phase plan: {reason}")
    return 0


def command_stop(_: argparse.Namespace) -> int:
    data = hook_input()
    turn = load_turn()
    if not turn or turn.get("status") != "open":
        return 0
    if bool(data.get("stop_hook_active")) or int(turn.get("stop_blocks", 0)) >= 1:
        turn["runtime_warning"] = "Stopped with an open turn after one allowed continuation."
        save_turn(turn)
        return 0
    turn["stop_blocks"] = int(turn.get("stop_blocks", 0)) + 1
    save_turn(turn)
    route = turn["route"]
    print(json.dumps({
        "decision": "block",
        "reason": (
            f"Escapement {route['tier']} turn remains open. "
            "Complete the current phase, then use advance-phase or close-turn. "
            "Do not create additional process artefacts beyond the declared phase."
        ),
    }))
    return 0


def command_close(args: argparse.Namespace) -> int:
    ensure()
    turn = load_turn()
    if not turn or turn.get("status") != "open":
        print("FAIL: no open runtime turn.", file=sys.stderr)
        return 1

    route = turn["route"]
    tier = route["tier"]
    selected_skills = [item["id"] for item in route["native_skills"]]
    used_skills = split(args.skills_used)
    files, missing_files = existing(split(args.files))
    evidence, missing_evidence = existing(split(args.evidence))
    check_paths = split(args.check_records)
    check_records, check_errors = load_checks(check_paths)
    checks_pass = all(
        int(record.get("exit_code", 1)) == 0 and record.get("result") == "PASS"
        for record in check_records
    ) if check_records else False

    errors = []
    if args.result == "PASS":
        if args.critical_failure:
            errors.append("critical failure cannot be PASS")
        if missing_files:
            errors.append(f"missing files: {missing_files}")
        if missing_evidence:
            errors.append(f"missing evidence: {missing_evidence}")
        if not set(selected_skills).issubset(set(used_skills)):
            errors.append(f"selected skills not declared used: {selected_skills}")
        if tier in {"MATERIAL", "PROGRAM"}:
            errors.extend(check_errors)
            if not check_records:
                errors.append(f"{tier} PASS requires structured checks")
            elif not checks_pass:
                errors.append("required checks did not pass")
        elif tier == "MICRO":
            if check_paths:
                errors.extend(check_errors)
            if not check_records and not args.no_check_reason:
                errors.append("MICRO closure requires a check or --no-check-reason")
            elif check_records and not checks_pass:
                errors.append("required checks did not pass")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    result = "FAIL" if args.critical_failure else args.result
    closure = {
        "closed_at": now(),
        "tier": tier,
        "summary": args.summary,
        "next_action": args.next,
        "files": files,
        "skills_used": used_skills,
        "check_records": check_paths,
        "no_check_reason": args.no_check_reason,
        "evidence": evidence,
        "result": result,
        "critical_failure": args.critical_failure,
        "blockers": args.blockers or "None",
    }
    turn["status"] = "closed"
    turn["closure"] = closure
    save_turn(turn)
    append_jsonl(TURNS_LOG, turn)

    memory = f"""# Session Memory

- Turn: {turn['turn_id']}
- Tier: {tier}
- Result: {result}
- Phases completed: {", ".join(item["phase"] for item in turn.get("phase_history", [])) or "None"}
- Final phase: {route["current_phase"]}
- Summary: {args.summary}
- Files: {', '.join(files) or 'None'}
- Checks: {', '.join(check_paths) or args.no_check_reason or 'None'}
- Evidence: {', '.join(evidence) or 'None'}
- Blockers: {closure['blockers']}
- Next action: {args.next}
"""
    SESSION_MEMORY.write_text(memory, encoding="utf-8")
    (ROOT / "SESSION_HANDOFF.md").write_text(
        memory.replace("# Session Memory", "# Session Handoff"),
        encoding="utf-8",
    )

    for skill in selected_skills:
        append_jsonl(SKILL_LOG, {
            "record_type": "skill-run",
            "schema_version": "3.0",
            "turn_id": turn["turn_id"],
            "tier": tier,
            "skill": skill,
            "used": skill in used_skills,
            "result": result,
            "checks": check_paths,
            "evidence": evidence,
            "timestamp": closure["closed_at"],
        })

    write_context(turn)
    print(f"Closed {turn['turn_id']} as {result}")
    return 0


def command_status(_: argparse.Namespace) -> int:
    ensure()
    print(json.dumps({
        "version": VERSION,
        "root": str(ROOT),
        "turn": load_turn(),
    }, indent=2))
    return 0


def command_reset(args: argparse.Namespace) -> int:
    ensure()
    current = load_turn()
    if current:
        append_jsonl(TURNS_LOG, {
            "turn_id": current.get("turn_id"),
            "event": "reset",
            "reason": args.reason,
            "timestamp": now(),
        })
    TURN.unlink(missing_ok=True)
    ACTIVE_CONTEXT.write_text("# Active Context\n\nNo active material turn.\n", encoding="utf-8")
    CONTEXT_PACK.write_text("# Active Context Pack\n\nNo active material turn.\n", encoding="utf-8")
    print("Runtime turn reset.")
    return 0


def command_doctor(_: argparse.Namespace) -> int:
    ensure()
    required = [
        "AGENTS.md",
        "CLAUDE.md",
        "catalog/doctrine-packs.json",
        "catalog/native-skills.json",
        "catalog/overlap-groups.json",
        "catalog/capability-registry.json",
        "catalog/strategy-adapters.json",
        "catalog/phase-capabilities.json",
        "catalog/research-policy.json",
        "catalog/skill-strengths.json",
        "catalog/design-stack.json",
        "catalog/capability-families.json",
        "catalog/overlap-matrix.json",
        "DOMAIN_CONTEXT.md",
        "scripts/capability_router.py",
        "scripts/agent_runtime.py",
    ]
    failures = 0
    print("ESCAPEMENT 6.3 RUNTIME DOCTOR")
    for relative in required:
        ok = (ROOT / relative).exists()
        print(f"[{'PASS' if ok else 'FAIL'}] {relative}")
        failures += int(not ok)

    kernel_words = len((ROOT / "AGENTS.md").read_text(encoding="utf-8").split())
    kernel_ok = kernel_words <= 1000
    print(f"[{'PASS' if kernel_ok else 'FAIL'}] kernel words: {kernel_words}/1000")
    failures += int(not kernel_ok)

    skills = json.loads((ROOT / "catalog/native-skills.json").read_text(encoding="utf-8"))["skills"]
    for item in skills:
        skill_id = item["id"]
        canonical = ROOT / "skills" / skill_id / "SKILL.md"
        codex = ROOT / ".agents" / "skills" / skill_id / "SKILL.md"
        claude = ROOT / ".claude" / "skills" / skill_id / "SKILL.md"
        ok = canonical.exists() and codex.exists() and claude.exists()
        print(f"[{'PASS' if ok else 'FAIL'}] skill {skill_id}")
        failures += int(not ok)

    print(f"\nFailures: {failures}")
    return 1 if failures else 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="agent_runtime")
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("session-start").set_defaults(func=command_session)
    sub.add_parser("prompt").set_defaults(func=command_prompt)
    sub.add_parser("stop").set_defaults(func=command_stop)
    sub.add_parser("status").set_defaults(func=command_status)
    sub.add_parser("doctor").set_defaults(func=command_doctor)

    manual = sub.add_parser("manual-start")
    manual.add_argument("--prompt", required=True)
    manual.add_argument("--json", action="store_true")
    manual.set_defaults(func=command_manual)

    explain = sub.add_parser("explain")
    explain.add_argument("--prompt", required=True)
    explain.set_defaults(func=command_explain)

    advance = sub.add_parser("advance-phase")
    advance.add_argument("--phase", required=True, choices=VALID_PHASE_IDS)
    advance.add_argument("--summary", required=True)
    advance.add_argument("--skills-used", default="")
    advance.add_argument("--files", default="")
    advance.add_argument("--check-records", default="")
    advance.add_argument("--no-check-reason", default="")
    advance.add_argument("--evidence", default="")
    advance.set_defaults(func=command_advance)

    replan = sub.add_parser("replan-phases")
    replan_target = replan.add_mutually_exclusive_group(required=True)
    replan_target.add_argument("--add-phase", choices=VALID_PHASE_IDS)
    replan_target.add_argument("--remove-phase", choices=VALID_PHASE_IDS)
    replan.add_argument("--reason", required=True)
    replan.set_defaults(func=command_replan)

    close = sub.add_parser("close-turn")
    close.add_argument("--summary", required=True)
    close.add_argument("--next", required=True)
    close.add_argument("--files", default="")
    close.add_argument("--skills-used", default="")
    close.add_argument("--check-records", default="")
    close.add_argument("--no-check-reason", default="")
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
    return root


def main() -> int:
    ensure()
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
