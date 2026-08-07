`AGENTS.md` at the repository root is the authoritative kernel -- read
and follow it, not this file. This pointer exists because Gemini CLI's
default context filename is `GEMINI.md`; without it, a fresh Gemini CLI
session reads nothing here at all unless a user has manually reconfigured
`context.fileName` in their own `settings.json` to include `AGENTS.md`.

Unlike Claude Code and Codex, this host has no automatic hook wiring to
`scripts/agent_runtime.py`. Per `AGENTS.md`'s "Host Bootstrap" section,
invoke it yourself: `session-start` once per session, `prompt` after
reading each new request, `stop` before ending a turn. Treat their JSON
output as required context, not optional reading.
