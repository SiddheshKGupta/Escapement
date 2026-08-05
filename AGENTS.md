---
owner: V L & CO
version: "5.4"
mode: runtime-enforced
purpose: "Build correct enterprise software with durable state, explicit skill routing, and evidence."
---

# VLCO Agent Instructions

## 0. Mandatory Runtime Protocol

For every material user prompt:

1. Read `.agent/runtime/ACTIVE_CONTEXT.md`.
2. Read `.agent/runtime/ACTIVE_SKILLS.md`.
3. Read `PROJECT_STATE.yaml`.
4. Invoke every selected native skill before material work:
   - Codex: `$skill-name`
   - Claude Code: `/skill-name`
5. Work on one bounded step.
6. Run deterministic checks before model judgement.
7. Before the final response, close the turn:

```bash
python scripts/agent_runtime.py close-turn \
  --summary "What was completed" \
  --next "Exact next action" \
  --files "path/a,path/b" \
  --checks "check one;check two" \
  --evidence "path/a,path/b"
```

Do not provide the final response while the runtime turn is open.

The `Stop` hook blocks one premature stop and directs the agent to close the turn. It then allows stopping to prevent an infinite loop.

### Runtime fallback

When hooks are unavailable:

```bash
python scripts/agent_runtime.py manual-start --prompt "User request"
```

Then follow the same close-turn command.

## 1. Prime Rule

**Understand enough. Decide enough. Build. Test. Prove. Persist.**

Do not code from guesses, treat chat as the source of truth, claim unrun checks, load every skill, mix overlapping skills without reason, or finish material work without durable state.

## 2. Work Modes

| Mode | Use |
|---|---|
| `FULL` | New application, product, module, architecture, or major workflow |
| `DELTA` | Material change to an existing product |
| `EXECUTE` | Approved ticket, isolated bug, copy change, or bounded UI improvement |

`FULL`: Inspect → discover → decide → readiness gate → approve → build.  
`DELTA`: Read state/decisions → identify impact → approve material change → build.  
`EXECUTE`: Confirm ticket/files/acceptance/checks → implement → prove → close turn.

## 3. First Actions

1. Inspect repository state before asking questions.
2. Determine known, unknown, blocker, mode, selected skills, and checks.
3. Ask only questions that can change scope, workflow, data/KPI, permissions, integrations, security, architecture, brand/UI, or acceptance.
4. Do not repeat answered questions.

## 4. Readiness Gate

For `FULL` or `DELTA`:

```text
READY CHECK
Scope:
Non-goals:
Users:
Workflow:
Data/KPIs:
Permissions:
Integrations:
UI direction:
Security:
Scale:
Selected skills:
Open risks:
Ready to build: YES/NO
```

Proceed only after approval or explicit instruction to proceed with listed assumptions.

## 5. Skill Rule

The runtime router selects the smallest useful stack:

```text
Capability → Primary skill → Reason → Artifact → Validation → Overlap rejected
```

Maximum active material skills: 4 by default.

Native skill directories:

```text
Codex: .agents/skills/<skill>/SKILL.md
Claude Code: .claude/skills/<skill>/SKILL.md
```

The compatibility `skills/` folder is documentation only and must not be assumed to auto-load.

## 6. Design Rule

For design, frontend, UI, brand, colour, typography, layout, animation, or responsive work:

1. Invoke `design-system`.
2. Invoke `enterprise-ui-review` for implementation/review.
3. Read `docs/standards/design-intelligence.md`.
4. Create/update product `DESIGN.md`.
5. State adopted and rejected reference patterns.
6. Client brand overrides external references.

Do not copy protected logos, fonts, images, or trade dress.

## 7. Enterprise Product Rules

Always preserve approved behaviour, use server-side permissions, validate inputs, cover loading/empty/error/permission/success, test changed behaviour, report checks not run, and make KPIs traceable.

Ask before dependencies, schema, auth/RBAC, destructive actions, production, paid services, integrations, broad refactors, licence-sensitive reuse, or confidential data.

Never invent business rules/KPIs, expose secrets, disable controls to force success, use generic AI UI, silently change architecture, or claim unrun tests.

## 8. Durable Context

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
CURRENT_PHASE.md
CURRENT_CONTEXT.md
.agent/runtime/ACTIVE_CONTEXT.md
.agent/runtime/ACTIVE_SKILLS.md
.agent/runtime/SESSION_MEMORY.md
SESSION_HANDOFF.md
docs/decisions/DECISION_LOG.md
```

Use `Write → Select → Compress → Isolate`.

## 9. Evidence

Run deterministic checks first: tests, types, lint, schemas, files, manifest, reconciliation, permissions, and exit codes. Then perform semantic, business, UX, risk, and human review.

## 10. Delivery Loop

```text
Bootstrap → Route → Declare → Execute → Observe → Validate → Decide → Persist → Close turn → Handoff
```

## 11. Done Means

Requirements work; permissions and edge states work; checks are truthful; totals reconcile; accessibility/performance are considered; evidence exists; state is updated; the runtime turn is closed; next action is explicit.

## 12. Read When Relevant

| Work | Read |
|---|---|
| Runtime | `AGENT_RUNTIME.md` |
| Discovery | native `project-discovery` |
| Dashboard/MIS | native `dashboard` + `data-reporting.md` |
| Workflow | native `workflow` |
| UI | native `enterprise-ui-review` + `ui.md` |
| Design/brand/motion | native `design-system` + `design-intelligence.md` |
| API | native `api-integration` |
| Release | native `release-readiness` |
| Skill evidence | native `skill-governance` |
| Context | `context-engineering.md` |
| Harness | `harness-engineering.md` |

## 13. Instruction Precedence

Safety/platform → current user → approved decisions → nearest `AGENTS.md` → root `AGENTS.md` → runtime/project state → loaded skill → references.

On conflict: stop, state it, recommend resolution.
