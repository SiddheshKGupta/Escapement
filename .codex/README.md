# Codex Configuration

| File | Role |
|---|---|
| `hooks.json` | Session, prompt, and stop hooks that drive `scripts/agent_runtime.py` |
| `../.agents/skills/<skill>/SKILL.md` | Native Codex skills, invoked as `$skill-name` |

Native skills are generated from `skills/` and must stay identical to it. After editing a skill, run:

```bash
python scripts/vlco_build.py sync-skills
```

`python scripts/vlco_build.py validate` fails if the native copies have drifted from `skills/`.

Codex does not read `.claude/settings.json`. Both harnesses run the same three runtime commands, so behaviour is identical across them.
