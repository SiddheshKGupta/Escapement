# Copilot Instructions

This repository is governed by the Escapement build standard.

Read these before any material change:

```text
AGENTS.md                          operating instructions
PROJECT_STATE.yaml                 durable project facts
.agent/runtime/ACTIVE_CONTEXT.md   current turn goal, mode, obligations
```

## Rules

1. Pick a work mode: `FULL`, `DELTA`, or `EXECUTE`. `FULL` and `DELTA` need a readiness gate before implementation.
2. Do not code from guesses. Inspect the repository before asking questions.
3. Run deterministic checks before offering judgement. Report checks that were not run as not run.
4. Ask before dependencies, schema changes, auth or permissions, destructive actions, production deployment, paid services, new integrations, and broad refactors.
5. Never invent business rules or KPIs, expose secrets, disable controls to force a pass, or claim tests you did not run.

Copilot does not execute the runtime hooks. When working here, open and close the turn manually:

```bash
python scripts/agent_runtime.py manual-start --prompt "<the request>"
python scripts/agent_runtime.py close-turn --summary "..." --next "..." --files "..." --checks "..." --evidence "..."
```
