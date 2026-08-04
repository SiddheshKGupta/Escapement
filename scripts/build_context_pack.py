#!/usr/bin/env python3
"""Build a compact task context pack from repository state."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()


def read(path: str, max_chars: int = 6000) -> str:
    p = ROOT / path
    if not p.exists():
        return "Not available."
    text = p.read_text(encoding="utf-8").strip()
    return text[:max_chars] if text else "Empty."


def extract_list(text: str, heading: str) -> str:
    lines = text.splitlines()
    capture = False
    found = []
    for line in lines:
        if line.strip().lower() == heading.lower():
            capture = True
            continue
        if capture and line.startswith("#"):
            break
        if capture and line.strip():
            found.append(line)
    return "\n".join(found[:20]) or "Not specified."


def trim_words(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]) + "\n\n[Context compressed to word budget.]"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--mode", choices=["FULL", "DELTA", "EXECUTE"], required=True)
    parser.add_argument("--scope")
    parser.add_argument("--acceptance")
    parser.add_argument("--output", default="CURRENT_CONTEXT.md")
    args = parser.parse_args()

    state = read("PROJECT_STATE.yaml", 3000)
    context = read("PROJECT_CONTEXT.md", 3500)
    phase = read("CURRENT_PHASE.md", 2500)
    decisions = read("docs/decisions/DECISION_LOG.md", 2500)
    skills = read("SKILL_USAGE_PLAN.md", 2500)

    content = f"""# Current Context

- Task ID: {args.task}
- Goal: {args.goal}
- Mode: {args.mode}
- Generated: {datetime.now(timezone.utc).isoformat()}
- Freshness: Rebuild after scope, decision, phase, or selected-skill change.

## Approved Scope

{args.scope or "Derive from approved ticket and project documents. Confirm before material implementation."}

## Non-goals

{extract_list(context, "## Non-goals")}

## Acceptance

{args.acceptance or "Use the approved ticket acceptance criteria. Mark unresolved criteria before implementation."}

## Current Project State

```yaml
{state}
```

## Product Context

{context}

## Current Phase

{phase}

## Relevant Decisions

{decisions}

## Selected Skills and Usage

{skills}

## Exact Files

List only files required for this task before editing.

## Relevant Standards

Load only standards triggered by the task.

## Data and Permissions

Confirm sources, sensitivity, access rules, and approval gates.

## Required Checks

- Deterministic checks first.
- Contract and acceptance checks.
- Semantic and risk review.
- Human approval where material.

## Blockers and Assumptions

Record unresolved blockers and explicitly accepted assumptions.

## Budget

- Active context target: <= 1,000 words.
- Use one primary skill per capability.
- Retry once after correcting context; then escalate.
"""

    output = ROOT / args.output
    output.write_text(trim_words(content, 1000), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
