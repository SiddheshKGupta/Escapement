# Agent Runtime

The repository standard becomes effective only when executed on every material turn.

```text
SessionStart → durable memory
UserPromptSubmit → mode + skill routing
Agent work → native skill invocation
Stop → one-shot gate
close-turn → state + evidence + handoff
```

## Runtime Files

| File | Role |
|---|---|
| `.agent/runtime/ACTIVE_CONTEXT.md` | Current goal, mode, state, obligations |
| `.agent/runtime/ACTIVE_SKILLS.md` | Selected skills and native invocations |
| `.agent/runtime/SESSION_MEMORY.md` | Durable compact handoff |
| `.agent/runtime/current-turn.json` | Local open-turn control state |
| `.agent/runtime/turns.jsonl` | Append-only turn history |
| `logs/skill-usage.jsonl` | Provisional evidence records |

## Commands

```bash
python scripts/agent_runtime.py doctor
python scripts/agent_runtime.py manual-start --prompt "Build a dashboard"
python scripts/agent_runtime.py status
python scripts/agent_runtime.py close-turn --summary "Done" --next "Next" --files "a,b" --checks "test;lint" --evidence "a,b"
python scripts/agent_runtime.py reset-turn --reason "Stale session"
```

The Stop hook blocks at most once. It never creates an unbounded loop.

A normal web chat with GitHub read access does not execute repository hooks. Use Codex/Claude Code in the repo, or invoke `manual-start`.
