# Claude Code Rules

This directory holds optional project rules loaded by Claude Code alongside `CLAUDE.md`.

The standard ships no rules of its own. `CLAUDE.md` imports `AGENTS.md`, `AGENT_RUNTIME.md`, and the runtime state files, which together carry the operating instructions.

Add a rule file here only when a project needs a constraint that is not already covered by:

| Concern | Already covered by |
|---|---|
| Operating loop, work modes, skill routing | `AGENTS.md` |
| Turn lifecycle and close-turn obligation | `AGENT_RUNTIME.md` |
| Domain standards | `docs/standards/` |
| Design and brand | `design-system` skill + `docs/standards/design-intelligence.md` |

Duplicating an existing standard here creates a second source of truth. Extend the standard instead.
