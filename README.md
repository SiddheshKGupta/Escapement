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

This copies the instruction set, standards, templates, skills, scripts, schemas, and behaviour tests. It writes `.vlco-build.json` to record the source and version.

Then wire the runtime — this is the step that makes the standard enforced rather than aspirational.

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

**Codex** — `.codex/hooks.json` follows the same three events.

Verify both layers:

```bash
python scripts/vlco_build.py doctor
python scripts/agent_runtime.py doctor
```

Both must reach zero failures. The runtime doctor checks that hook config exists and that all eight native skills are present under `.claude/skills/` and `.agents/skills/`.

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

Native skills load from `.claude/skills/<skill>/SKILL.md` and `.agents/skills/<skill>/SKILL.md`. The `skills/` directory is documentation only and does not auto-load.

A skill counts as used only when evidence exists. Each run records its trigger, the alternatives rejected, expected versus actual output, checks planned and skipped, scores, and evidence paths. Passing requires a total at or above 85 with no critical correctness, security, data, or permission failure.

---

## Commands

**Build CLI** — `python scripts/vlco_build.py <command>`

| Command | Purpose |
|---|---|
| `init <target>` | Install into a project (`--force` to overwrite) |
| `update <target>` | Compare an install against this standard (`--apply` to sync) |
| `doctor` | Environment and repository readiness |
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

Manifest completeness, required root files, Markdown line budgets, skill frontmatter, duplicate skill names, broken internal links, project-state structure, skill JSONL schema, evidence-path existence, score consistency, context-pack word budget, release placeholders, and coverage of all eleven behaviour tests.

CI runs the same checks on every push and pull request via `.github/workflows/validate-standard.yml`.

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
.agent/runtime/        # per-turn state (generated)

docs/
  standards/           # domain standards, loaded on demand
  templates/           # BRD, PRD, FRD, architecture, security, frontend
  checklists/          # readiness, discovery, context health, pre-release
  decisions/           # ADR template and decision log
skills/                # documentation copies of the native skills
scripts/               # build CLI, runtime, validator, context packer
schemas/               # JSON schemas for state and evidence
tests/                 # behaviour tests and runtime unit tests
examples/              # worked end-to-end example
```

---

## Worked example

`examples/enterprise-dashboard/` walks a real request through mode selection, context pack, skill routing, KPI contracts, evidence records, validation, and handoff.

---

## Troubleshooting

**The agent ignores the standard.** Run `python scripts/agent_runtime.py doctor`. If hook config is missing, nothing is enforced and the standard is only advisory.

**`doctor` reports missing native skills.** The `skills/` directory does not auto-load. Skills must exist under `.claude/skills/` and `.agents/skills/`.

**An install has drifted.** `python scripts/vlco_build.py update <target>` reports the difference; `--apply` syncs it.

**A turn is stuck open.** `python scripts/agent_runtime.py reset-turn --reason "Stale session"`.

---

## Ownership

Developed by **V L & CO**.

Source-available, not open source. Commercial redistribution, white-labelling, or substantial republication requires permission. See `LICENSE.md` and `NOTICE.md`.
