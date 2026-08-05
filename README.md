# Escapement

**A build standard your coding agent actually executes.**

Escapement is a runtime harness that makes AI coding agents work like disciplined engineers — routing the right skills, holding durable state across sessions, running deterministic checks before claiming success, and refusing to end a turn without evidence.

It runs in Claude Code, Codex, Cursor, Cline, and Roo Code. It is standard library Python only. There is nothing to install.

> Understand enough. Decide enough. Build. Test. Prove. Persist.

---

## Agents: read this first

If you are an AI agent working in a repository that has Escapement installed, read these three files before anything else, in this order:

```text
AGENTS.md                          # your operating instructions
PROJECT_STATE.yaml                 # durable project facts
.agent/runtime/ACTIVE_CONTEXT.md   # this turn's goal, mode, and obligations
```

Everything else loads on demand. Do not read the whole repository.

---

## What this is, and what it is not

**It is** an enforcement layer. Hooks fire on every session start, every prompt, and every attempted stop. The router picks a minimal skill stack from the prompt. The turn does not close until you record what you changed, which checks you ran, and where the evidence lives.

**It is not** a prompt library, a set of style guidelines, or documentation you hope the model reads. Guidelines get skipped under context pressure. Hooks do not.

The distinction matters because the failure mode of AI-assisted delivery is not bad code — it is confident code with no durable record of what was decided, what was verified, and what was merely asserted.

It does not govern another repository automatically, make an ordinary web chat execute local hooks, guarantee correct software because the files exist, replace business judgement or human approval, permit copying protected brand assets, or remove your need to read the tests and the evidence. It works when it is installed inside the actual product repository and driven by a supported coding-agent runtime.

---

## Why

Agents produce working prototypes fast. Enterprise delivery also needs traceable KPIs, server-side permissions, tested edge states, recorded decisions, approval gates before destructive work, and a handoff the next session can actually use.

Without a harness, each of those depends on the model remembering to care. Escapement makes them structural: the checks run before the model's own judgement, and the turn cannot close while they are outstanding.

---

## Install

Install into an existing project:

```bash
python scripts/vlco_build.py init /path/to/your-project
```

This copies the instruction set, standards, templates, skills, scripts, schemas, hook configuration, native skills, and behaviour tests. It writes `.vlco-build.json` to record the source and version.

The hooks ship pre-configured, so normally you only need to approve them in your harness. This is the step that makes the standard enforced rather than aspirational.

**Claude Code** — `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [{ "type": "command", "command": "python scripts/agent_runtime.py session-start" }] }
    ],
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "python scripts/agent_runtime.py prompt" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "python scripts/agent_runtime.py stop" }] }
    ]
  }
}
```

**Codex** — `.codex/hooks.json` uses the same three events.

Verify every layer:

```bash
python scripts/vlco_build.py doctor
```

That runs the environment checks, the unified validator, and the runtime doctor in sequence. All three must reach zero failures.

### Without hooks

Web chat and GitHub-read integrations do not execute repository hooks. Open the turn manually:

```bash
python scripts/agent_runtime.py manual-start --prompt "Build the management dashboard"
```

The close-turn requirement is unchanged.

---

## How a turn works

```text
SessionStart      →  load durable memory
UserPromptSubmit  →  classify mode, route skills, write ACTIVE_CONTEXT
agent work        →  invoke native skills, one bounded step
deterministic     →  checks run before model judgement
Stop              →  one-shot gate; blocks a premature stop exactly once
close-turn        →  persist state, evidence, and handoff
```

The Stop gate blocks at most once and then permits the stop. It cannot loop.

Closing a turn:

```bash
python scripts/agent_runtime.py close-turn \
  --summary "KPI contracts implemented for the dashboard" \
  --next "Wire the approvals table to the permissions service" \
  --files "src/kpi.ts,src/dashboard.tsx" \
  --checks "unit tests;totals reconcile;permission matrix" \
  --evidence "reports/kpi-run.json"
```

Durable state between turns:

```text
.agent/runtime/ACTIVE_CONTEXT.md   goal, mode, obligations
.agent/runtime/ACTIVE_SKILLS.md    selected skills and how to invoke them
.agent/runtime/SESSION_MEMORY.md   compact carry-over
SESSION_HANDOFF.md                 the human-readable handoff
logs/skill-usage.jsonl             evidence records
```

---

## Work modes

| Mode | Use | Gate |
|---|---|---|
| `FULL` | New product, module, architecture, or major workflow | Readiness check before implementation |
| `DELTA` | Material change to an existing product | Approval on the material change |
| `EXECUTE` | Approved ticket, isolated bug, copy or bounded UI change | Confirm ticket, files, acceptance, checks |

`EXECUTE` deliberately skips discovery. Slowing down a one-line fix with a readiness gate is how standards get abandoned.

---

## Skills

Eight native skills. The router selects at most four per turn.

| Skill | Owns |
|---|---|
| `project-discovery` | New product, module, architecture, unclear material change |
| `design-system` | Brand, colour, typography, layout, motion, responsive, `DESIGN.md` |
| `enterprise-ui-review` | New UI, redesign, generic-AI-look detection, usability |
| `dashboard` | Dashboards, MIS, KPI definition, analytics, management reporting |
| `workflow` | Operational process, approval, exception handling, SLA, governance |
| `api-integration` | External APIs, webhooks, file exchange, connectors |
| `release-readiness` | UAT, deploy, production, handover |
| `skill-governance` | Selecting, scoring, improving, and retiring skills |

Native skills load from `.claude/skills/<skill>/SKILL.md` and `.agents/skills/<skill>/SKILL.md`. Both are generated from `skills/`, which is the single source of truth. After editing a skill:

```bash
python scripts/vlco_build.py sync-skills
```

Validation fails if the native copies drift from `skills/`.

A skill counts as used only when evidence exists. Each run records its trigger, the alternatives rejected, expected versus actual output, checks planned and skipped, scores, and evidence paths. Passing requires a total at or above 85 with no critical correctness, security, data, or permission failure.

---

## Example prompts and expected routing

**New product** — `FULL` mode; routes to `project-discovery`, `workflow`, `skill-governance`:

```text
I want to build a Subvention Management Platform.

First understand the users, workflows, data, approvals, reporting,
permissions, integrations, security and design direction.

Do not begin implementation until the READY CHECK is approved.
```

**Dashboard** — routes to `dashboard`, `design-system`, `enterprise-ui-review`, `skill-governance`:

```text
Build a management dashboard for subvention claims.

Show claim value, approved amount, collected amount, outstanding amount,
ageing, recovery rate, source records, freshness, filters, reconciliation
and drill-down.

Use the client brand and avoid generic AI styling.
```

**Workflow** — routes to `workflow`, `skill-governance`:

```text
Design the workflow from OEM scheme creation through transaction eligibility,
claim generation, approval, OEM submission, rejection handling, invoice,
collection, accounting, MIS and closure.

Include actors, states, permissions, controls, exceptions, escalations,
audit events and SLA.
```

**UI redesign** — routes to `design-system`, `enterprise-ui-review`, `skill-governance`:

```text
Redesign this application as a credible enterprise platform.

Use the client brand, improve density and hierarchy, create or update
DESIGN.md, cover all operating states, add keyboard focus and remove
generic AI gradients and glow cards.
```

**API integration** — routes to `api-integration`, `skill-governance`:

```text
Integrate the application with the lease management system.

Before coding, define authentication, permissions, request and response
contracts, validation, idempotency, retries, timeouts, error handling,
audit events, monitoring and fallback behaviour.
```

---

## Commands

**Build CLI** — `python scripts/vlco_build.py <command>`

| Command | Purpose |
|---|---|
| `init <target>` | Install into a project (`--force` to overwrite) |
| `update <target>` | Compare an install against this standard (`--apply` to sync, `--check` to fail on drift) |
| `sync-skills` | Regenerate native skills from `skills/` |
| `doctor` | Environment, validation, and runtime readiness |
| `validate` | All deterministic standard checks |
| `context` | Build a task-scoped context pack |
| `skill-audit` | Validate and summarise skill evidence |
| `handoff` | Generate a compact session handoff |
| `version` | Installed standard version |

**Runtime CLI** — `python scripts/agent_runtime.py <command>`

| Command | Purpose |
|---|---|
| `session-start` | Load durable memory (SessionStart hook) |
| `prompt` | Classify mode and route skills (UserPromptSubmit hook) |
| `stop` | One-shot gate on premature stop (Stop hook) |
| `manual-start` | Open a turn without hooks |
| `close-turn` | Persist state, evidence, handoff |
| `status` | Inspect the open turn |
| `reset-turn` | Clear a stale turn |
| `doctor` | Runtime wiring and native skill presence |

Building a context pack:

```bash
python scripts/vlco_build.py context \
  --task T-014 \
  --goal "Build the management dashboard" \
  --mode DELTA
```

---

## Progressive disclosure

`AGENTS.md` is a routing layer, not an encyclopaedia. Agents start with the instruction file and project state, then load only what the task needs.

| Task | Loads |
|---|---|
| Dashboard | `docs/standards/data-reporting.md` + `dashboard` |
| UI or design | `docs/standards/ui.md`, `docs/standards/design-intelligence.md` + `design-system` |
| Integration | `docs/standards/integrations.md` + `api-integration` |
| Security | `docs/standards/security.md` |
| Material change | `docs/standards/context-engineering.md`, `harness-engineering.md` |
| Release | `release-readiness` + `docs/checklists/pre-release.md` |

---

## What gets validated

```bash
python scripts/vlco_build.py validate
```

Manifest completeness, required root files, version consistency across the manifest and both scripts, Markdown line budgets, skill frontmatter, duplicate skill names, native skill sync, broken internal links, project-state structure, skill JSONL schema, evidence-path existence, score consistency, context-pack word budget, release placeholders, and coverage of all eleven behaviour tests.

Validation runs in two profiles. In this repository it checks the standard's own inventory. In a project the standard was installed into — detected via `.vlco-build.json` — it skips `manifest.json` and `README.md`, which describe the standard itself and which no consuming project should be failed for lacking.

CI runs the validator, the runtime tests, and a fresh-install check on every push and pull request via `.github/workflows/validate-standard.yml`.

---

## Budgets

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

---

## Definition of done

Approved requirements work. Permissions and edge states work. Tests pass. Totals reconcile. Accessibility and performance are reviewed. Required evidence exists. Documents are updated. No critical defect remains. A handoff is written.

Checks that were not run are reported as not run. Never as passing.

---

## Layout

```text
AGENTS.md              # agent instructions (the routing layer)
AGENT_RUNTIME.md       # turn lifecycle and runtime files
CLAUDE.md              # Claude Code bootstrap imports
PROJECT_STATE.yaml     # durable project facts
manifest.json          # file inventory, validated

.claude/               # Claude Code hooks and native skills
.agents/               # Codex native skills
.codex/                # Codex hooks
.agent/runtime/        # per-turn state (generated, gitignored)

docs/
  standards/           # domain standards, loaded on demand
  templates/           # BRD, PRD, FRD, architecture, security, frontend, design
  checklists/          # readiness, discovery, context health, pre-release
  decisions/           # ADR template and decision log
skills/                # source of truth for all skills
scripts/               # build CLI, runtime, validator, context packer
schemas/               # JSON schemas for state and evidence
tests/                 # behaviour tests and runtime unit tests
examples/              # worked end-to-end example
```

`examples/enterprise-dashboard/` walks a real request through mode selection, context pack, skill routing, KPI contracts, evidence records, validation, and handoff.

---

## Troubleshooting

**The agent forgets after one turn.** Run `python scripts/agent_runtime.py status` and read `.agent/runtime/SESSION_MEMORY.md`. Usual causes: the standard sits outside the product repository, the agent was started from the wrong folder, hooks were never approved, the previous turn was never closed, the agent was not restarted after a hook or skill change, or you are in a web chat rather than a repository runtime.

**Skills are not being used.** Confirm `.claude/skills/` and `.agents/skills/` exist, then test the router:

```bash
python scripts/agent_runtime.py manual-start --prompt "Redesign the management dashboard and define KPI drill-down"
```

Expect `dashboard`, `design-system`, `enterprise-ui-review`, `skill-governance`. Inspect `.agent/runtime/ACTIVE_SKILLS.md` for what was actually selected.

**The agent starts coding too quickly.** Tell it: *Treat this as FULL or DELTA mode. Do not implement until the READY CHECK is complete and approved.*

**The agent asks too many questions.** Tell it: *Use the smallest sufficient discovery round. Recommend a default answer for every question. Stop asking when implementation can safely begin.* For a bounded task, state that the mode is `EXECUTE` and the acceptance criteria are already approved.

**The UI still looks generic.** Require `design-system` and `enterprise-ui-review`, and require `DESIGN.md` before implementation, stating the archetype, adopted and rejected patterns, colour tokens, typography, layout, component states, responsive rules, and motion rules.

**The Stop hook interrupts the agent.** The turn is still open. Close it with `close-turn`, or clear a stale one:

```bash
python scripts/agent_runtime.py reset-turn --reason "Previous session ended unexpectedly"
```

**An install has drifted.** `python scripts/vlco_build.py update <target>` reports the difference; `--apply` syncs it.

---

## Roadmap

- [x] Progressive-disclosure project standard
- [x] Runtime state and session memory
- [x] Native Codex and Claude Code skills
- [x] Prompt-based skill routing
- [x] Completion gate and skill evidence
- [x] Design intelligence
- [x] Runtime doctor and smoke test
- [ ] Packaged CLI installer
- [ ] Automatic skill-effectiveness reports
- [ ] Organisation-level policy overlays
- [ ] MCP server
- [ ] Cross-project health reporting

---

## Ownership

Developed by **V L & CO**. Formerly the VLCO Product Build Standard.

Source-available, not open source. Commercial redistribution, white-labelling, or substantial republication requires permission. See [LICENSE.md](LICENSE.md) and [NOTICE.md](NOTICE.md).
