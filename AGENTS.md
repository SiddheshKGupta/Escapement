---
owner: V L & CO
version: "5.0"
mode: caveman
purpose: "Build correct enterprise software with minimum reading and minimum paperwork."
---

# AGENTS.md

## 1. Prime Rule

**Understand enough. Decide enough. Build. Test. Update docs.**

Do not write long essays.
Do not ask what repo already answers.
Do not install every skill.
Do not code from guesses.

## 2. Work Mode

Pick one:

| Mode | Use |
|---|---|
| FULL | New app, module, architecture, major workflow |
| DELTA | Material change to existing product |
| EXECUTE | Approved ticket, bug, small UI change |

### FULL

Ask essential questions. Create short plan docs. Get approval. Build.

### DELTA

Read existing docs. Ask only what changed or is unclear. Update affected docs. Build.

### EXECUTE

Confirm ticket, files, tests, acceptance. Build. No full discovery.

## 3. First Actions

1. Read `PROJECT_STATE.yaml`.
2. Read nearest `AGENTS.md`.
3. Read only linked docs needed for current task.
4. Inspect repo before asking questions.
5. State:
   - what is known
   - what is unknown
   - what blocks work
   - proposed mode
6. Ask questions in small rounds.
7. Do not repeat answered questions.

## 4. Ask Before Build

Ask only questions that can change:

- Scope
- workflow
- data
- KPI
- permission
- integration
- security
- architecture
- brand/UI
- acceptance

For every question:

```text
Question:
Why it matters:
Recommended answer:
Other options:
Decision:
```

Stop asking when build can safely start.

## 5. Mandatory Approval Gate

For FULL or DELTA work, show:

```text
READY CHECK
- Scope:
- Non-goals:
- Users:
- Workflow:
- Data/KPIs:
- Permissions:
- Integrations:
- UI direction:
- Security:
- Scale:
- Skill stack:
- Open risks:
- Ready to build: YES/NO
```

Build only after approval or explicit instruction to proceed with listed assumptions.

## 6. Always / Ask / Never

### Always

- Preserve approved behaviour.
- Use server-side permissions.
- Validate inputs.
- Handle loading, empty, error, permission, success.
- Test changed behaviour.
- Update affected docs.
- Tell truth about checks not run.
- Every KPI: definition, period, source, breakdown, drill-down.
- Dashboards: FY, quarter, month where relevant.
- Use client brand for primary actions.
- Use Deep Plum `#53284F` only as restrained V L & CO signature.

### Ask First

- New dependency
- schema migration
- auth/RBAC change
- destructive action
- production deploy
- paid service
- new integration
- broad refactor
- licence-sensitive code reuse
- external skill installation

### Never

- Invent business rules.
- Claim tests passed without running them.
- expose secrets.
- disable controls to make code work.
- copy reference repo code without licence review.
- use fake KPI totals.
- use generic AI UI.
- install overlapping skills without reason.

## 7. Enterprise UI Rule

Avoid:

- purple/indigo gradients
- glow cards
- sparkle icons
- huge padding
- low data density
- rounded-3xl everywhere
- fake charts
- decorative dashboards

Use:

- neutral canvas
- client primary colour
- compact tables
- sidebar + header + breadcrumbs
- filter bar + toolbar
- status dots/pills
- skeletons
- actionable empty states
- keyboard support
- clear focus
- restrained motion

Read `docs/standards/ui.md` only for UI work.

## 8. Dashboard Rule

Every important number must show:

```text
Definition | Formula | Unit | Period | Source | Freshness | Filters | Breakdown | Drill-down
```

Default time views where relevant:

```text
FY | Quarter | Month | YTD | QTD | MTD | Custom | Prior period | Target
```

Read `docs/standards/data-reporting.md` for dashboard/MIS work.

## 9. Skill Rule

Use the **smallest useful stack**.

Default maximum: 8 active material skills.

For each capability:

```text
Need → Primary skill → Optional helper → Redundant skills rejected
```

Do not count reference websites as missing skills.

Read `SKILLS_INVENTORY.md` and `SKILL_USAGE_PLAN.md`.

## 10. Required Small Docs

Create only what the task needs.

| File | Max size |
|---|---:|
| BRD.md | 120 lines |
| PRD.md | 150 lines |
| FRD.md | 180 lines |
| ARCHITECTURE.md | 180 lines |
| SECURITY.md | 120 lines |
| FRONTEND_SPEC.md | 150 lines |
| TICKETS.md | 1 table, atomic tickets |
| AI_REPORT.md | append-only short log |
| SESSION_HANDOFF.md | 40 lines |

Use templates in `docs/templates/`.

## 11. Documentation Stop Rule

Stop documenting when:

- Scope is clear.
- Material decisions are recorded.
- Acceptance is testable.
- Architecture is safe enough.
- Blocking unknowns are closed.

Then build.

No repeated background.
No marketing prose.
No generic explanations.
Use IDs, bullets, tables, links.

## 12. Delivery Loop

```text
Inspect → Clarify → Decide → Plan → Build → Test → Review → Update docs → Handoff
```

Implement one approved ticket at a time.

## 13. Done Means

- Requirement works.
- permissions work.
- edge states work.
- tests pass.
- totals reconcile.
- performance acceptable.
- accessibility checked.
- docs updated.
- no critical defect.
- handoff written.

## 14. Read When Relevant

| Work | Read |
|---|---|
| Discovery | `skills/project-discovery/SKILL.md` |
| Dashboard | `skills/dashboard/SKILL.md` |
| Workflow | `skills/workflow/SKILL.md` |
| UI | `skills/ui-review/SKILL.md` |
| API | `skills/api-integration/SKILL.md` |
| Release | `skills/release-readiness/SKILL.md` |
| Security | `docs/standards/security.md` |
| Performance | `docs/standards/performance.md` |
| Testing | `docs/standards/testing.md` |

## 15. Instruction Order

1. Safety/platform rules
2. Current user instruction
3. Approved decisions
4. Nearest folder `AGENTS.md`
5. Root `AGENTS.md`
6. Project docs
7. Loaded skill
8. Reference material

On conflict: stop, show conflict, recommend resolution.
