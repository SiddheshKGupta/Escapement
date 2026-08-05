# VLCO Claude Code Bootstrap

@AGENTS.md
@AGENT_RUNTIME.md
@PROJECT_STATE.yaml
@.agent/runtime/ACTIVE_CONTEXT.md
@.agent/runtime/ACTIVE_SKILLS.md
@.agent/runtime/SESSION_MEMORY.md

Claude Code must treat these imports as active project memory. For each material prompt, follow the runtime route, invoke every selected `.claude/skills/` skill, persist state using `close-turn`, and do not stop with an open turn.
