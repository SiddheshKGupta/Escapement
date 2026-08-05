# Escapement Claude Code Bootstrap

@AGENTS.md
@AGENT_RUNTIME.md
@PROJECT_STATE.yaml
@PROJECT_CONTEXT.md
@feature_list.json
@.agent/runtime/ACTIVE_CONTEXT.md
@.agent/runtime/ACTIVE_SKILLS.md
@.agent/runtime/SESSION_MEMORY.md

Treat these imports as active project memory.

For every material prompt:

1. continue the current open turn;
2. invoke each selected `.claude/skills/` skill;
3. work on one bounded feature;
4. capture checks through `scripts/run_check.py`;
5. persist state using `scripts/agent_runtime.py close-turn`;
6. do not stop with an open turn.
