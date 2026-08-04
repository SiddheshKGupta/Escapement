# VLCO Product Build Standard

**A source-available product engineering standard and executable harness for disciplined AI-assisted software delivery.**

VLCO Product Build Standard helps Claude Code, Codex, Cursor, Cline, Roo Code, and other coding agents understand enough, decide enough, build, test, prove, and hand off enterprise software without unnecessary context or paperwork.

```text
Product thinking
+ Context engineering
+ Harness engineering
+ Skill governance
+ Deterministic validation
+ Human approval gates
```

> Understand enough. Decide enough. Build. Test. Prove. Update.

## Status

| Item | Value |
|---|---|
| Version | 5.3 |
| Architecture | Progressive disclosure |
| Root instruction | `AGENTS.md` |
| Context model | Selective context packs |
| Harness model | Deterministic-first validation |
| Skill model | Evidence-based selection and evaluation |
| Licence | Source Available — Not Open Source |

See `LICENSE.md` and `NOTICE.md`.

## Why This Exists

AI coding agents can generate working prototypes quickly, but enterprise delivery also needs:

- clear requirements and workflows;
- controlled assumptions and decisions;
- data and KPI traceability;
- permissions and security;
- enterprise UI quality;
- measurable testing;
- approval gates;
- reliable handoff;
- evidence that skills and tools actually helped.

This repository turns those needs into a small operating system and executable validation harness.

## Operating Loop

```text
Inspect
→ Clarify
→ Decide
→ Plan
→ Build
→ Test
→ Review
→ Prove
→ Update
→ Handoff
```

## Work Modes

| Mode | Use |
|---|---|
| `FULL` | New product, module, architecture, or major workflow |
| `DELTA` | Material change to an existing product |
| `EXECUTE` | Approved ticket, bug, or small UI change |

`FULL` and `DELTA` work require a readiness check before implementation. `EXECUTE` work should not be slowed down by full discovery.

## Quick Start

Clone:

```bash
git clone https://github.com/SiddheshKGupta/VLCO-Product-Build-Standard.git
cd VLCO-Product-Build-Standard
```

Run the environment doctor:

```bash
python scripts/vlco_build.py doctor
```

Validate the repository:

```bash
python scripts/vlco_build.py validate
```

Create a context pack:

```bash
python scripts/vlco_build.py context \
  --task T-014 \
  --goal "Build management dashboard" \
  --mode DELTA
```

Audit skill usage:

```bash
python scripts/vlco_build.py skill-audit
```

Create a handoff:

```bash
python scripts/vlco_build.py handoff \
  --summary "Dashboard KPI contracts completed" \
  --next "Implement approved dashboard ticket"
```

Install the standard into another project:

```bash
python scripts/vlco_build.py init ../my-project
```

## CLI Commands

| Command | Purpose |
|---|---|
| `init` | Install the standard into a project |
| `doctor` | Diagnose environment and repository readiness |
| `validate` | Run all deterministic standard checks |
| `context` | Build a task-specific context pack |
| `skill-audit` | Validate and summarise skill evidence |
| `handoff` | Generate a compact session handoff |
| `update` | Compare installed files with this standard |
| `version` | Show the installed standard version |

## Progressive Disclosure

Agents start with:

```text
AGENTS.md
PROJECT_STATE.yaml
```

They then load only the relevant standard, skill, decision, or checklist.

| Task | Load |
|---|---|
| Dashboard | `docs/standards/data-reporting.md` + dashboard skill |
| UI | `docs/standards/ui.md` + UI review skill |
| Integration | `docs/standards/integrations.md` + API skill |
| Security | `docs/standards/security.md` |
| Material task | Context and harness engineering standards |
| Skill review | Skill governance skill and evidence log |
| Release | Release-readiness skill and pre-release checklist |

The root file is a routing layer, not an encyclopedia.

## Context Engineering

Context Engineering supplies the smallest complete context required for the current decision.

```text
Write durable facts
→ Select relevant material
→ Compress completed work
→ Isolate bounded investigations
```

Material tasks use `CURRENT_CONTEXT.md`, generated from current project state, phase, decisions, selected skills, and requested goal.

Recommended context-pack target:

```text
<= 1,000 words
```

## Harness Engineering

The harness consists of:

```text
Instructions
+ Context
+ State
+ Skills
+ Tools
+ Tests
+ Approval gates
+ Feedback
```

The harness runs deterministic checks before semantic or model review.

Human approval is required for material changes such as schema migrations, authentication, permissions, destructive actions, production deployment, paid services, confidential data access, and new integrations.

## Skill Evidence Loop

A skill counts as used only when evidence exists.

```text
Route
→ Declare
→ Execute
→ Observe
→ Validate
→ Score
→ Decide
→ Learn
```

Each skill run records:

- trigger and selection reason;
- rejected alternatives;
- expected and actual outputs;
- checks planned, run, and skipped;
- component scores;
- retries, duration, and impact;
- evidence paths;
- critical failures.

Passing rule:

```text
Total >= 85
AND no critical correctness, security, data, or permission failure
```

## Validation

The unified validator checks:

- `manifest.json` completeness;
- required root files;
- Markdown line budgets;
- skill frontmatter;
- duplicate skill names;
- broken internal links;
- project-state structure;
- skill JSONL schema;
- evidence-path existence;
- score consistency;
- context-pack word budget;
- release placeholders;
- behaviour-test coverage.

Run:

```bash
python scripts/validate_standard.py
```

or:

```bash
python scripts/vlco_build.py validate
```

GitHub Actions runs the same checks on pushes and pull requests.

## Repository Structure

```text
AGENTS.md
README.md
manifest.json
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
CURRENT_PHASE.md
SESSION_HANDOFF.md
SKILLS_INVENTORY.md
SKILL_USAGE_PLAN.md
AI_REPORT.md

docs/
  standards/
  templates/
  decisions/
  checklists/

skills/
scripts/
schemas/
logs/
reports/
tests/
examples/
.github/workflows/
```

## Worked Example

See:

```text
examples/enterprise-dashboard/
```

It demonstrates:

```text
Request
→ Mode selection
→ Context pack
→ Skill routing
→ KPI contract
→ Evidence record
→ Validation
→ Handoff
```

## Documentation Limits

| Document | Maximum |
|---|---:|
| BRD | 120 lines |
| PRD | 150 lines |
| FRD | 180 lines |
| Architecture | 180 lines |
| Security | 120 lines |
| Frontend specification | 150 lines |
| Session handoff | 40 lines |
| Context pack | 1,000 words |

Stop documenting when scope is clear, material decisions are recorded, acceptance is testable, architecture is safe enough, and blockers are closed.

## Definition of Done

A feature is complete only when:

- approved requirements work;
- permissions and edge states work;
- tests pass;
- totals reconcile;
- accessibility and performance are reviewed;
- required evidence exists;
- documents are updated;
- no critical defect remains;
- a handoff is written.

## Roadmap

### v5.4

- packaged executable and optional PyPI release;
- richer project presets;
- controlled skill-assisted versus baseline experiments;
- automatic skill-effectiveness reports.

### v6.0

- MCP server;
- organisation-level policy overlays;
- cross-project health reporting;
- central standard version registry.

## Ownership

Developed by **V L & CO**.

This repository is source-available and is not distributed under an open-source licence. Commercial redistribution, white-labelling, or substantial republication requires permission.
