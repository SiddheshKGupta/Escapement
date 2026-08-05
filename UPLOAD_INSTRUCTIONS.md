# v5.4 Runtime Enforcement Upload

Upload into the repository root while preserving all paths.

## Replace

- `AGENTS.md`
- `PROJECT_STATE.yaml`

## Add

- `CLAUDE.md`
- `AGENT_RUNTIME.md`
- `.codex/hooks.json`
- `.claude/settings.json`
- `.github/copilot-instructions.md`
- `.agent/runtime/`
- `.agents/skills/`
- `.claude/skills/`
- `scripts/agent_runtime.py`
- `docs/standards/runtime-enforcement.md`
- `docs/standards/design-intelligence.md`
- `docs/templates/DESIGN.template.md`
- `tests/runtime/`
- `PROJECT_STATE.v5.4.template.yaml`

## Protect real logs

The package contains empty seed files:

```text
logs/skill-usage.jsonl
.agent/runtime/turns.jsonl
```

Do not overwrite non-empty production logs. Migrate or retain them.

## Verify

```bash
python scripts/agent_runtime.py doctor
python -m unittest tests.runtime.test_agent_runtime
```

## Activate Codex

1. Open the repository in Codex.
2. Review and trust `.codex/hooks.json`.
3. Confirm project hooks are active.
4. Start a new session.
5. Native skills are under `.agents/skills/`.

## Activate Claude Code

1. Open the repository root in Claude Code.
2. Approve `.claude/settings.json` project hooks.
3. Start a new session.
4. Native skills are under `.claude/skills/`.
5. `CLAUDE.md` imports runtime memory automatically.

## Test prompt

```text
Redesign the management dashboard using the client brand, define KPI drill-down,
and remove the generic AI look.
```

Expected route:

```text
Mode: DELTA
Skills:
- dashboard
- design-system
- enterprise-ui-review
- skill-governance
```

The agent should be prevented from finishing once until it runs `close-turn`.

## Important distinction

GitHub Actions validate pushes and pull requests. They do not inject memory into an interactive agent.

Normal ChatGPT GitHub access also does not execute local project hooks. Use Codex/Claude Code in the repository or invoke:

```bash
python scripts/agent_runtime.py manual-start --prompt "<request>"
```
