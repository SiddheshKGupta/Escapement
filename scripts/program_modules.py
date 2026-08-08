#!/usr/bin/env python3
"""Multi-module PROGRAM registry.

A single runtime turn (agent_runtime.py) tracks the phase cycle for one
piece of work. A PROGRAM-tier build with several modules (e.g. billing,
CRM core, admin portal) runs each module through its own DISCOVER->RELEASE
cycle across many turns -- nothing durable tracked that a module exists,
what phase it is at, or whether it was checked against the artifacts other
modules also depend on (shared schema, DESIGN.md, DOMAIN_CONTEXT.md).

This file is that missing durable registry. The one rule it enforces: a
module cannot be marked past SPECIFY until every registered shared artifact
has been checked for consistency with that module's spec -- cross-module
drift is exactly the class of gap this exists to prevent.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PAST_SPECIFY = {"plan", "implement", "verify", "polish", "release", "done"}
ALLOWED_STATUS = {
    "not_started", "discover", "research", "brainstorm", "specify",
    *PAST_SPECIFY, "blocked",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_root() -> Path:
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()
REGISTRY_FILE = ROOT / "docs" / "PROGRAM_MODULES.json"


def load() -> dict[str, Any]:
    if not REGISTRY_FILE.exists():
        return {
            "schema_version": "1.0",
            "program": None,
            "shared_artifacts": [],
            "modules": [],
            "updated_at": utc_now(),
        }
    return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))


def save(value: dict[str, Any]) -> None:
    value["updated_at"] = utc_now()
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def module_by_id(value: dict[str, Any], module_id: str) -> dict[str, Any]:
    for module in value["modules"]:
        if module.get("id") == module_id:
            return module
    raise SystemExit(f"FAIL: unknown module {module_id}")


def command_set_program(args: argparse.Namespace) -> int:
    value = load()
    value["program"] = args.name
    save(value)
    print(f"Program set: {args.name}")
    return 0


def command_add_shared(args: argparse.Namespace) -> int:
    value = load()
    if args.path not in value["shared_artifacts"]:
        value["shared_artifacts"].append(args.path)
    save(value)
    print(f"Shared artifact registered: {args.path}")
    return 0


def command_add_module(args: argparse.Namespace) -> int:
    value = load()
    if any(m["id"] == args.id for m in value["modules"]):
        raise SystemExit(f"FAIL: module {args.id} already registered")
    depends_on = [d for d in (args.depends_on or "").split(",") if d]
    value["modules"].append({
        "id": args.id,
        "name": args.name,
        "status": "not_started",
        "depends_on": depends_on,
        "shared_artifacts_checked": [],
        "created_at": utc_now(),
    })
    save(value)
    print(f"Module registered: {args.id}")
    return 0


def command_reset(args: argparse.Namespace) -> int:
    if not REGISTRY_FILE.exists():
        print("Program registry already absent.")
        return 0
    if not args.confirm:
        raise SystemExit(
            "FAIL: reset would discard the current program registry. Re-run with --confirm."
        )
    REGISTRY_FILE.unlink()
    print(f"Program registry cleared: {REGISTRY_FILE}")
    return 0


def command_list(_: argparse.Namespace) -> int:
    value = load()
    print(f"Program: {value.get('program') or '(unset)'}")
    print(f"Shared artifacts: {', '.join(value['shared_artifacts']) or '(none)'}")
    for module in value["modules"]:
        checked = module.get("shared_artifacts_checked", [])
        print(
            f"  {module['id']}: {module['status']} | depends_on="
            f"{','.join(module.get('depends_on', [])) or 'none'} | "
            f"shared_checked={','.join(checked) or 'none'}"
        )
    return 0


def command_set_status(args: argparse.Namespace) -> int:
    value = load()
    module = module_by_id(value, args.id)

    just_checked = [c for c in (args.checked_shared or "").split(",") if c]
    for artifact in just_checked:
        if artifact not in value["shared_artifacts"]:
            raise SystemExit(f"FAIL: {artifact} is not a registered shared artifact")
        if artifact not in module["shared_artifacts_checked"]:
            module["shared_artifacts_checked"].append(artifact)

    if args.status not in ALLOWED_STATUS:
        raise SystemExit(f"FAIL: unknown status {args.status}")

    if args.status in PAST_SPECIFY:
        missing = set(value["shared_artifacts"]) - set(module["shared_artifacts_checked"])
        if missing:
            raise SystemExit(
                "FAIL: module must check shared artifacts before leaving SPECIFY: "
                + ", ".join(sorted(missing))
            )

    for dependency in module.get("depends_on", []):
        dep = module_by_id(value, dependency)
        if args.status in PAST_SPECIFY and dep["status"] != "done":
            raise SystemExit(f"FAIL: dependency {dependency} is not done")

    module["status"] = args.status
    save(value)
    print(f"{args.id}: {args.status}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="program_modules")
    sub = parser.add_subparsers(dest="command", required=True)

    set_program = sub.add_parser("set-program")
    set_program.add_argument("--name", required=True)
    set_program.set_defaults(func=command_set_program)

    add_shared = sub.add_parser("add-shared")
    add_shared.add_argument("--path", required=True)
    add_shared.set_defaults(func=command_add_shared)

    add_module = sub.add_parser("add-module")
    add_module.add_argument("--id", required=True)
    add_module.add_argument("--name", required=True)
    add_module.add_argument("--depends-on", default="")
    add_module.set_defaults(func=command_add_module)

    sub.add_parser("list").set_defaults(func=command_list)

    reset = sub.add_parser("reset")
    reset.add_argument("--confirm", action="store_true")
    reset.set_defaults(func=command_reset)

    set_status = sub.add_parser("set-status")
    set_status.add_argument("--id", required=True)
    set_status.add_argument("--status", required=True)
    set_status.add_argument("--checked-shared", default="")
    set_status.set_defaults(func=command_set_status)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
