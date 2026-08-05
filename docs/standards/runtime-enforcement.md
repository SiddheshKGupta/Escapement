# Runtime Enforcement

Markdown standards are passive. Runtime enforcement turns them into controls.

```text
SessionStart → inject durable memory
UserPromptSubmit → classify mode and route native skills
Agent work → invoke selected skills
Stop → block once if turn is open
close-turn → persist handoff and evidence
```

| Control | Mechanism |
|---|---|
| Project instructions | `AGENTS.md`, `CLAUDE.md` |
| Session memory | `SessionStart` hook |
| Prompt routing | `UserPromptSubmit` hook |
| Codex skills | `.agents/skills/` |
| Claude skills | `.claude/skills/` |
| Completion gate | `Stop` hook |
| Durable state | `.agent/runtime/*.md` |
| Evidence | runtime and skill JSONL logs |
| Commit validation | GitHub Actions, separate from interactive runtime |

The Stop hook blocks once only; it must not create an unbounded autonomous loop.
