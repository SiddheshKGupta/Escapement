# Escapement Runtime

```text
Prompt
→ Decision brief
→ Task tier and register
→ Current phase
→ Domain/research need
→ Phase-specific doctrine and skills
→ External strategy candidates
→ Work and evidence
→ Advance phase
→ Handoff
```

## Active files

```text
.agent/runtime/ACTIVE_CONTEXT.md
.agent/runtime/CONTEXT_PACK.md
.agent/runtime/current-turn.json
```

The context pack contains only the current phase.

## Phase transition

Complete the phase artifact, then run:

```bash
python scripts/agent_runtime.py advance-phase \
  --phase RESEARCH \
  --summary "Discovery decisions resolved" \
  --skills-used "decision-coach,project-discovery" \
  --files "PROJECT_CONTEXT.md" \
  --evidence "PROJECT_CONTEXT.md"
```

Implementation, verification and release phases require structured checks or a
truthful reason where a check is not applicable.

## Manual start

```bash
python scripts/agent_runtime.py manual-start --prompt "User request" --json
```

## Status and closure

```bash
python scripts/agent_runtime.py status
python scripts/agent_runtime.py close-turn ...
python scripts/agent_runtime.py reset-turn --reason "Reason"
```

The Stop gate blocks at most once and cannot create an infinite loop.
