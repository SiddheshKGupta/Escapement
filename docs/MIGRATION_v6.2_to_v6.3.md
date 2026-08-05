# Migration from v6.2 to v6.3

## Changes

- `design-intelligence.md` becomes the design constitution.
- Capability strengths are added beneath native skills.
- Overlap groups gain relation types and phase rules.
- Native skill count expands to 32.
- Automatic and invoked context budgets are separated.
- Trigger matching uses complete terms.
- A `POLISH` phase is added.
- Capability readiness audits become available.

## Upgrade

Preview:

```bash
python scripts/escapement.py update /path/to/project
```

Apply safe managed changes:

```bash
python scripts/escapement.py update /path/to/project --apply
```

Project-owned state remains preserved.

Validate:

```bash
python scripts/agent_runtime.py doctor
python scripts/escapement.py doctor --root /path/to/project
python scripts/eval_harness.py run
python -m unittest discover -s tests -p "test_*.py"
```

Generate a readiness audit for the first material task:

```bash
python scripts/escapement.py capability-audit "<task>" --markdown
```

External capabilities are not automatically installed during migration.
