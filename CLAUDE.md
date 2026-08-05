# Escapement Claude Code Bootstrap

@AGENTS.md
@.agent/runtime/ACTIVE_CONTEXT.md
@.agent/runtime/CONTEXT_PACK.md

The kernel and current phase pack are the only automatic imports.

Use the decision brief to ask only material questions and recommend defaults.
Follow the phase plan rather than loading every capability at once.

Open `DOMAIN_CONTEXT.md`, project state, specifications, full skills and
external references only when the current phase pack points to them.

Invoke each selected `.claude/skills/` skill. External skills, plugins and MCP
servers remain candidates until their overlap, licence, security and approval
requirements are satisfied.
