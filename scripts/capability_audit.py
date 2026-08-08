#!/usr/bin/env python3
"""Generate a phase-aware skill and capability readiness audit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from capability_router import find_root, installed_skill_names, route_prompt  # noqa: E402

ROOT = find_root()


def load_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def audit(prompt: str) -> dict[str, Any]:
    route = route_prompt(prompt)
    installed = installed_skill_names()
    registry = load_json("catalog/capability-registry.json")
    resources = {item["id"]: item for item in registry["resources"]}
    strengths = load_json("catalog/skill-strengths.json")["capabilities"]
    strength_index = {item["id"]: item for item in strengths}
    overlap = load_json("catalog/overlap-matrix.json")["groups"]

    phase_plan = []
    required_external: list[str] = []
    for phase in route["phase_plan"]:
        phase_route = route_prompt(prompt, phase_override=phase["id"])
        phase_strengths = []
        for selected in phase_route.get("capability_strengths", []):
            strength_id = selected["id"]
            item = strength_index.get(strength_id, {"id": strength_id})
            parent = item.get("parent")
            status = "internal"
            if parent and parent != "design-intelligence-constitution":
                candidates = {
                    parent,
                    strength_id.split(":", 1)[-1],
                    strength_id.replace(":", "-"),
                }
                status = "installed" if installed.intersection(candidates) else "catalogued"
                if status == "catalogued" and parent not in required_external:
                    required_external.append(parent)
            phase_strengths.append({
                "id": strength_id,
                "parent": parent,
                "status": status,
                "strength": item.get("strength"),
            })
        phase_plan.append({
            "phase": phase["id"],
            "purpose": phase["purpose"],
            "native_skills": [
                item["id"] for item in phase_route.get("native_skills", [])
            ],
            "capability_strengths": phase_strengths,
            "external_candidates": [
                item["id"] for item in phase_route.get("external_candidates", [])
            ],
        })

    overlap_relevant = []
    selected_parents = {
        item.get("parent")
        for phase in phase_plan
        for item in phase["capability_strengths"]
        if item.get("parent")
    }
    for group in overlap:
        members = set(group["members"])
        if members.intersection(selected_parents):
            overlap_relevant.append({
                "id": group["id"],
                "canonical": group["canonical"],
                "relation": group["relation"],
                "rule": group["rule"],
                "selected_members": sorted(members.intersection(selected_parents)),
            })

    external_details = []
    for resource_id in required_external:
        resource = resources.get(resource_id)
        if resource:
            external_details.append({
                "id": resource_id,
                "name": resource.get("name"),
                "source": resource.get("source"),
                "status": resource.get("status"),
                "activation": resource.get("activation"),
                "license": resource.get("license"),
                "license_status": resource.get("license_status"),
            })
        else:
            external_details.append({
                "id": resource_id,
                "name": resource_id,
                "status": "strategy-or-subskill",
                "activation": "resolve-through-parent-adapter",
            })

    return {
        "schema_version": "1.0",
        "prompt": prompt,
        "tier": route["tier"],
        "register": route["register"],
        "current_phase": route["current_phase"],
        "detected_skill_folders": sorted(installed),
        "active_native_skills": [
            item["id"] for item in route["native_skills"]
        ],
        "active_capability_strengths": [
            item["id"] for item in route["capability_strengths"]
        ],
        "phase_plan": phase_plan,
        "external_install_or_load_candidates": external_details,
        "overlap_decisions": overlap_relevant,
        "design_authority": (
            "docs/standards/design-intelligence.md"
            if any(
                item["id"] == "design-intelligence:constitution"
                for item in route["capability_strengths"]
            )
            else None
        ),
        "rule": (
            "A catalogued capability is not active until source, licence, "
            "security, overlap, installation and approval are resolved."
        ),
    }


def render_markdown(value: dict[str, Any]) -> str:
    lines = [
        "# Skill and Capability Readiness Audit",
        "",
        f"- Tier: `{value['tier']}`",
        f"- Register: `{value['register']}`",
        f"- Current phase: `{value['current_phase']}`",
        f"- Design authority: `{value['design_authority'] or 'not required'}`",
        "",
        "## Active",
        "",
        "- Native skills: "
        + (", ".join(value["active_native_skills"]) or "none"),
        "- Capability strengths: "
        + (", ".join(value["active_capability_strengths"]) or "none"),
        "",
        "## Phase Plan",
        "",
    ]
    for phase in value["phase_plan"]:
        lines.append(f"### {phase['phase']}")
        lines.append(f"- Purpose: {phase['purpose']}")
        lines.append(
            "- Native skills: "
            + (", ".join(phase["native_skills"]) or "task-routed")
        )
        for item in phase["capability_strengths"]:
            lines.append(
                f"- `{item['id']}` — `{item['status']}` — "
                f"{item.get('strength') or 'strength defined by adapter'}"
            )
        if phase["external_candidates"]:
            lines.append(
                "- External candidates: "
                + ", ".join(phase["external_candidates"])
            )
        lines.append("")

    lines.extend(["## External Install or Load Candidates", ""])
    if not value["external_install_or_load_candidates"]:
        lines.append("None.")
    for item in value["external_install_or_load_candidates"]:
        lines.append(
            f"- `{item['id']}` — {item.get('name')} — "
            f"{item.get('activation')} — {item.get('source') or 'see strategy adapter'}"
        )

    lines.extend(["", "## Overlap Decisions", ""])
    if not value["overlap_decisions"]:
        lines.append("No material overlap group selected.")
    for item in value["overlap_decisions"]:
        lines.append(
            f"- `{item['id']}` — {item['relation']} — {item['rule']}"
        )

    lines.extend(["", "## Rule", "", value["rule"]])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(prog="capability_audit")
    parser.add_argument("prompt")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    value = audit(args.prompt)
    output = render_markdown(value) if args.markdown else json.dumps(
        value, indent=2, ensure_ascii=False
    ) + "\n"
    if args.output:
        path = Path(args.output)
        if not path.is_absolute():
            path = ROOT / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(path)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
