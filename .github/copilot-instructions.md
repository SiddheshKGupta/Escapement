`AGENTS.md` at the repository root is the authoritative kernel -- read
and follow it, not this file. This pointer exists because some Copilot
surfaces prioritize `.github/copilot-instructions.md` specifically.

Unlike Claude Code and Codex, this host has no automatic hook wiring to
`scripts/agent_runtime.py`. Per `AGENTS.md`'s "Host Bootstrap" section,
invoke it yourself: `session-start` once per session, `prompt` after
reading each new request, `stop` before ending a turn. Treat their JSON
output as required context, not optional reading.
