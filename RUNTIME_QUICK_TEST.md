# Runtime Quick Test

## 1. Doctor

```bash
python scripts/agent_runtime.py doctor
```

Expected: zero failures.

## 2. Manual route

```bash
python scripts/agent_runtime.py manual-start \
  --prompt "Redesign the management dashboard and define KPI drill-down"
```

Expected skills:

```text
dashboard
design-system
enterprise-ui-review
skill-governance
```

## 3. Inspect

```bash
python scripts/agent_runtime.py status
```

## 4. Close

```bash
python scripts/agent_runtime.py close-turn \
  --summary "Runtime test completed" \
  --next "Start a real agent session" \
  --files ".agent/runtime/ACTIVE_CONTEXT.md" \
  --checks "runtime route inspected" \
  --evidence ".agent/runtime/ACTIVE_CONTEXT.md"
```
