# Changelog

## 5.4.1 — 2026-08-05

- Moved `validate-standard.yml` into `.github/workflows/`, where GitHub can run it. CI had never executed.
- Added the `.claude/`, `.codex/`, `.agents/`, and `.github/` trees that the manifest referenced but that were never published.
- Added `.claude/settings.json` and `.codex/hooks.json`, so the runtime protocol is enforced rather than advisory.
- Added the `design-system` skill. It was mandated by `AGENTS.md` but had never shipped.
- Added `sync-skills`; native skills are now generated from `skills/` and validated against it.
- Added `description` frontmatter to every skill, and aligned skill directory names with their frontmatter names.
- Split validation into standard and project profiles, so a consuming project is no longer failed for lacking `manifest.json` and `README.md`.
- Aligned versions across `manifest.json`, `vlco_build.py`, and `agent_runtime.py`, and added a check that keeps them aligned.
- Consolidated `manifest.v5.3.patch.json`, `manifest.v5.4.runtime.json`, and `CHANGELOG.v5.4.md` into `manifest.json` and this file.
- Promoted the long-form manual to `docs/GUIDE.md`.
- Renamed the standard to Escapement.
- `update` no longer exits non-zero merely for reporting drift; use `--check` for that.
- Removed committed bytecode and the duplicate root copy of `design-intelligence.md`.

## 5.4.0 — Runtime Enforcement

- Added per-session and per-prompt runtime injection.
- Added deterministic work-mode and skill routing.
- Added native Codex skills under `.agents/skills`.
- Added native Claude Code skills under `.claude/skills`.
- Added `CLAUDE.md` project bootstrap and imports.
- Added Codex and Claude hook configurations.
- Added one-shot Stop gate.
- Added durable active context, active skills, session memory, and turn history.
- Added provisional evidence-aware skill logging.
- Added native design-system routing and the 73-company design-intelligence standard.
- Added runtime doctor and smoke test.

## 5.3.0 — Enforcement and Usability

- Added the unified validator and GitHub Actions workflow.
- Added `doctor`, `init`, and `update` commands.
- Added intelligent context packs and enhanced skill evidence.
- Added machine-readable behaviour tests and a worked example.

## 5.2.0 — 2026-08-04

- Added context engineering, harness engineering, and evidence-based skill loop.
- Added skill logs, schema, audit scripts, health report, and behaviour tests.


## 5.1.0 — 2026-08-04

- Added public-repository governance files.
- Added explicit usage and attribution terms.
- Added contribution rules focused on instruction economy.
- Added material architecture-change behaviour test.
- Added dashboard KPI traceability behaviour test.
- Added production deployment approval behaviour test.
- Added instruction-conflict behaviour test.

## 5.0.0 — 2026-08-03

- Introduced FULL, DELTA, and EXECUTE work modes.
- Replaced the large baseline with progressive disclosure.
- Added compact BRD, PRD, FRD, architecture, security, and frontend templates.
- Added skill-overlap governance.
- Added project state, handoff, decision records, and initial agent behaviour tests.
