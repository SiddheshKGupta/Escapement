# Upload Instructions

Upload this package into the repository root while preserving all paths.

## Replace

- `README.md`
- `scripts/build_context_pack.py`
- `scripts/skill_audit.py`
- `schemas/skill-run.schema.json`
- `logs/skill-usage.jsonl` only if the repository log is currently empty

## Add

- `scripts/vlco_build.py`
- `scripts/validate_standard.py`
- `.github/workflows/validate-standard.yml`
- `docs/standards/policy-levels.md`
- `reports/SKILL_EFFECTIVENESS.md`
- all `.yaml` behaviour tests
- `examples/enterprise-dashboard/`
- `manifest.v5.3.patch.json`

## Important

Do not overwrite a non-empty production `logs/skill-usage.jsonl`. Migrate existing records to the enhanced schema instead.

## Test

```bash
python scripts/vlco_build.py doctor
python scripts/vlco_build.py validate
python scripts/vlco_build.py skill-audit
```

## Suggested Commit

```text
feat: add v5.3 enforcement CLI, doctor, CI and worked example
```
