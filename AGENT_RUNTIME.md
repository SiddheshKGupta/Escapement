# Escapement Runtime

## Lifecycle

```text
SessionStart
→ Load durable state

UserPromptSubmit
→ Continue/open turn
→ Classify mode
→ Route skills
→ Write active context

Agent work
→ Execute one bounded feature
→ Capture structured checks

Stop
→ Block one premature stop

Close turn
→ Validate evidence
→ Update feature/handoff
→ Persist append-only records
```

## Local State

```text
.agent/runtime/
.agent/evidence/
.agent/evals/
.agent/runs/
```

These are local by default.

## Shared State

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
feature_list.json
SESSION_HANDOFF.md
docs/specs/
docs/decisions/
```

Shared state should be committed when it materially changes.

## Commands

```bash
python scripts/agent_runtime.py manual-start --prompt "Task"
python scripts/agent_runtime.py status
python scripts/agent_runtime.py explain --prompt "Task"
python scripts/agent_runtime.py close-turn ...
python scripts/agent_runtime.py reset-turn --reason "Reason"
python scripts/agent_runtime.py doctor
```

The Stop gate blocks at most once and never creates an unbounded loop.
