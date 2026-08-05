<div align="center">

# VLCO Product Build Standard

### A runtime-enforced operating system for building serious software with AI coding agents.

Give Codex and Claude Code durable project memory, automatic skill routing, approval gates, design standards, deterministic checks, and reliable handoffs.

[![Version](https://img.shields.io/badge/version-5.4-53284F?style=flat-square)](https://github.com/SiddheshKGupta/VLCO-Product-Build-Standard)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Codex](https://img.shields.io/badge/Codex-ready-111111?style=flat-square)](https://developers.openai.com/codex/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-ready-D97757?style=flat-square)](https://docs.anthropic.com/en/docs/claude-code/)
[![Licence](https://img.shields.io/badge/licence-source--available-6B7280?style=flat-square)](LICENSE.md)

**Understand enough. Decide enough. Build. Test. Prove. Persist.**

</div>

---

## Why this exists

AI coding agents are excellent at generating code.

They are less reliable at remembering long-running project decisions, selecting the right specialist instructions, respecting approval gates, proving that work was tested, and leaving a usable handoff for the next session.

VLCO Product Build Standard adds the missing operating layer.

```text
Project instructions
+ Durable state
+ Native skills
+ Runtime hooks
+ Approval gates
+ Deterministic checks
+ Evidence
+ Handoff
```

It is designed for:

- enterprise applications;
- dashboards and MIS;
- business workflows;
- APIs and integrations;
- governance and approval systems;
- design systems;
- testing and release readiness.

---

## What you get

| Capability | What it does |
|---|---|
| Durable project memory | Saves the current task, decisions, evidence, and next action in repository files |
| Automatic skill routing | Selects the smallest useful skill stack from the user prompt |
| Work modes | Routes work through `FULL`, `DELTA`, or `EXECUTE` |
| Native Codex skills | Uses project skills from `.agents/skills/` |
| Native Claude Code skills | Uses project skills from `.claude/skills/` |
| Runtime hooks | Injects context at session start and prompt submission |
| Completion gate | Prevents one premature stop when material work is still open |
| Design intelligence | Provides a high-level synthesis of 73 company design systems |
| Approval gates | Pauses before schema, auth, permissions, destructive, paid, integration, or production changes |
| Deterministic validation | Encourages tests, lint, type checks, schemas, reconciliation, and permission checks before subjective review |
| Skill evidence | Records selected skills, checks, files, results, and evidence |
| Session handoff | Persists what was completed and what should happen next |

---

## The most important rule

The standard must live inside the **same repository as the product being built**.

### Correct

```text
my-product/
├── AGENTS.md
├── CLAUDE.md
├── PROJECT_STATE.yaml
├── PROJECT_CONTEXT.md
├── .agent/
├── .agents/
├── .claude/
├── docs/
├── scripts/
└── src/
```

### Incorrect

```text
VLCO-Product-Build-Standard/
    standard files

my-product/
    product code
```

A separate standards repository does not automatically control an agent working in another repository.

---

# Quick start

## Create a new project

```bash
git clone https://github.com/SiddheshKGupta/VLCO-Product-Build-Standard.git my-new-product
cd my-new-product
```

Disconnect the project from the original repository:

```bash
git remote remove origin
```

Connect your own repository:

```bash
git remote add origin YOUR_NEW_REPOSITORY_URL
git branch -M main
git push -u origin main
```

---

## Add it to an existing project

Copy the following into the root of the existing repository:

```text
AGENTS.md
CLAUDE.md
AGENT_RUNTIME.md
PROJECT_STATE.yaml
PROJECT_CONTEXT.md

.agent/
.agents/
.claude/

docs/
scripts/
schemas/
tests/
```

Do not overwrite non-empty evidence logs:

```text
logs/skill-usage.jsonl
.agent/runtime/turns.jsonl
```

---

## Configure the project

Edit `PROJECT_STATE.yaml`:

```yaml
project_name: Subvention Management Platform
phase: discovery
work_mode: FULL
implementation_authorized: false
approved_ticket: null

blocking_decisions: []
accepted_assumptions: []
selected_skills: []

runtime:
  version: "5.4"
  enabled: true
  last_closed_turn: null
```

Then add the basic product context to `PROJECT_CONTEXT.md`:

```markdown
# Project Context

## Product

Subvention Management Platform

## Business Problem

The current process is managed through spreadsheets and email.

## Users

- Operations
- Finance
- Management
- OEM coordination team

## Intended Outcome

Create a controlled workflow from scheme creation to claim settlement,
accounting, reporting, and closure.

## Known Constraints

- Every transaction requires an audit trail.
- Management needs claim ageing and recovery visibility.
- New external integrations require approval.

## Non-goals

- Replacing the entire lease management system.
```

Write only what is currently known. The framework will help complete the rest.

---

## Verify the installation

```bash
python scripts/agent_runtime.py doctor
```

Alternative:

```bash
python3 scripts/agent_runtime.py doctor
```

Windows:

```powershell
py -3 scripts/agent_runtime.py doctor
```

Expected:

```text
Failures: 0
```

---

# Use with Codex

Open the product repository in Codex from the repository root.

Codex uses:

```text
AGENTS.md
.agents/skills/
.codex/hooks.json
```

## Trust the project hooks

Inside Codex:

```text
/hooks
```

Review and trust:

```text
<project>/.codex/hooks.json
```

Changed hooks may require approval again.

## Check project skills

Inside Codex:

```text
/skills
```

Expected skills:

```text
project-discovery
dashboard
workflow
design-system
enterprise-ui-review
api-integration
release-readiness
skill-governance
```

You can invoke one explicitly:

```text
$dashboard Review the KPI contracts for this dashboard.
```

---

# Use with Claude Code

Install Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
```

Check the installation:

```bash
claude doctor
```

Start it from the repository root:

```bash
claude
```

Claude Code uses:

```text
CLAUDE.md
.claude/skills/
.claude/settings.json
```

Review and approve the project settings when prompted.

Check loaded project memory:

```text
/memory
```

---

# First prompt

Use this before asking the agent to build anything:

```text
Read AGENTS.md, PROJECT_STATE.yaml, PROJECT_CONTEXT.md,
.agent/runtime/ACTIVE_CONTEXT.md,
.agent/runtime/ACTIVE_SKILLS.md and
.agent/runtime/SESSION_MEMORY.md.

Do not build anything yet.

Tell me:

1. the current project;
2. the current phase;
3. the recommended work mode;
4. the available skills;
5. the important missing decisions;
6. whether the runtime appears active.
```

A healthy first response should orient the project instead of immediately writing code.

---

# How it works

```text
Session starts
    ↓
Load project state and previous handoff
    ↓
User sends a prompt
    ↓
Classify FULL / DELTA / EXECUTE
    ↓
Select the smallest useful skill stack
    ↓
Inject active context and selected skills
    ↓
Execute one bounded step
    ↓
Run deterministic checks
    ↓
Persist evidence and handoff
    ↓
Close the runtime turn
```

---

## Work modes

### `FULL`

Use for:

- a new application;
- a new product;
- a new module;
- a new architecture;
- a major workflow.

```text
Understand
→ Ask essential questions
→ Record decisions
→ READY CHECK
→ Approval
→ Build
```

### `DELTA`

Use for a meaningful change to something that already exists.

Examples:

- redesigning the application;
- adding a workflow;
- adding an integration;
- changing permissions;
- changing architecture.

```text
Read current state
→ Identify impact
→ Approve material changes
→ Build
```

### `EXECUTE`

Use for a small, approved, bounded task.

Examples:

- fix a bug;
- update copy;
- repair one component;
- implement an approved ticket.

```text
Confirm task
→ Change files
→ Test
→ Persist evidence
```

---

## Native skills

| Skill | Trigger |
|---|---|
| `project-discovery` | New or unclear products, modules, architecture, or major change |
| `dashboard` | KPIs, MIS, metrics, analytics, charts, drill-down, reconciliation |
| `workflow` | Processes, approvals, states, exceptions, maker-checker, escalation |
| `design-system` | Brand, colour, typography, layout, motion, responsive behaviour, `DESIGN.md` |
| `enterprise-ui-review` | UI structure, hierarchy, density, states, accessibility |
| `api-integration` | APIs, webhooks, OAuth, connectors, external systems |
| `release-readiness` | Production, rollout, rollback, monitoring, go-live |
| `skill-governance` | Skill selection, evidence, checks, results, and improvement |

Native paths:

```text
.agents/skills/   # Codex
.claude/skills/   # Claude Code
```

The older `skills/` directory is compatibility documentation and should not be treated as the native runtime location.

---

# Example prompts

## New product

```text
I want to build a Subvention Management Platform.

First understand the users, workflows, data, approvals,
reporting, permissions, integrations, security and design direction.

Do not begin implementation until the READY CHECK is approved.
```

Expected route:

```text
Mode: FULL

Skills:
- project-discovery
- workflow
- skill-governance
```

---

## Dashboard

```text
Build a management dashboard for subvention claims.

Show claim value, approved amount, collected amount,
outstanding amount, ageing, recovery rate, source records,
freshness, filters, reconciliation and drill-down.

Use the client brand and avoid generic AI styling.
```

Expected route:

```text
Skills:
- dashboard
- design-system
- enterprise-ui-review
- skill-governance
```

---

## Workflow

```text
Design the workflow from OEM scheme creation through transaction eligibility,
claim generation, approval, OEM submission, rejection handling,
invoice, collection, accounting, MIS and closure.

Include actors, states, permissions, controls, exceptions,
escalations, audit events and SLA.
```

Expected route:

```text
Skills:
- workflow
- skill-governance
```

---

## UI redesign

```text
Redesign this application as a credible enterprise platform.

Use the client brand, improve density and hierarchy,
create or update DESIGN.md, cover all operating states,
add keyboard focus and remove generic AI gradients and glow cards.
```

Expected route:

```text
Skills:
- design-system
- enterprise-ui-review
- skill-governance
```

---

## API integration

```text
Integrate the application with the lease management system.

Before coding, define authentication, permissions, request and response contracts,
validation, idempotency, retries, timeouts, error handling,
audit events, monitoring and fallback behaviour.
```

Expected route:

```text
Skills:
- api-integration
- skill-governance
```

---

# Persistent memory

For each material prompt, the runtime updates:

```text
.agent/runtime/ACTIVE_CONTEXT.md
.agent/runtime/ACTIVE_SKILLS.md
```

These files contain:

- the current goal;
- the selected work mode;
- selected skills;
- required reads;
- approval gates;
- turn obligations.

At the end of work, it updates:

```text
.agent/runtime/SESSION_MEMORY.md
SESSION_HANDOFF.md
.agent/runtime/turns.jsonl
logs/skill-usage.jsonl
```

This allows the next session to recover the current state from the repository instead of relying only on chat history.

---

# Close every material turn

Before completing material work, the agent should run:

```bash
python scripts/agent_runtime.py close-turn \
  --summary "What was completed" \
  --next "Exact next action" \
  --files "path/a,path/b" \
  --checks "test one;test two" \
  --evidence "path/a,path/b"
```

Example:

```bash
python scripts/agent_runtime.py close-turn \
  --summary "KPI catalogue and dashboard specification completed" \
  --next "Implement the approved dashboard shell" \
  --files "DESIGN.md,docs/KPI_CATALOGUE.md" \
  --checks "KPI review;design review" \
  --evidence "DESIGN.md,docs/KPI_CATALOGUE.md"
```

This is the mechanism that preserves memory between turns.

---

# Manual mode

Some chat environments do not execute local repository hooks.

Start the runtime manually:

```bash
python scripts/agent_runtime.py manual-start \
  --prompt "Build the Subvention Management dashboard"
```

Then tell the agent:

```text
Read:

- AGENTS.md
- .agent/runtime/ACTIVE_CONTEXT.md
- .agent/runtime/ACTIVE_SKILLS.md

Follow all selected skills and close the runtime turn before finishing.
```

---

# Design system

For any UI or design work, create or update:

```text
DESIGN.md
```

Start with:

```text
docs/templates/DESIGN.template.md
```

Use:

```text
docs/standards/design-intelligence.md
```

The product design system should define:

- product and users;
- client brand priority;
- visual direction;
- primary design archetype;
- adopted references;
- rejected references;
- colour tokens;
- typography;
- spacing;
- layout;
- navigation;
- buttons;
- forms;
- tables;
- cards;
- charts;
- status states;
- motion;
- responsiveness;
- accessibility.

Client branding always takes precedence over external design references.

---

# Approval gates

The agent must pause before:

- database schema changes;
- authentication changes;
- role or permission changes;
- destructive actions;
- production deployments;
- paid services;
- new external integrations;
- confidential-data access;
- material scope changes;
- broad refactors;
- licence-sensitive reuse.

The framework makes these decisions explicit. It does not remove human control.

---

# Commands

## Runtime

```bash
python scripts/agent_runtime.py doctor
python scripts/agent_runtime.py status
python scripts/agent_runtime.py manual-start --prompt "Your task"
python scripts/agent_runtime.py close-turn --summary "Done" --next "Next action"
python scripts/agent_runtime.py reset-turn --reason "Reason"
```

## Validation

```bash
python scripts/vlco_build.py validate
python scripts/vlco_build.py skill-audit
```

## Runtime smoke test

```bash
python -m unittest tests.runtime.test_agent_runtime
```

Expected:

```text
OK
```

---

# Project structure

```text
.
├── AGENTS.md
├── CLAUDE.md
├── AGENT_RUNTIME.md
├── PROJECT_STATE.yaml
├── PROJECT_CONTEXT.md
├── CURRENT_CONTEXT.md
├── CURRENT_PHASE.md
├── DESIGN.md
├── SESSION_HANDOFF.md
│
├── .agent/
│   └── runtime/
│       ├── ACTIVE_CONTEXT.md
│       ├── ACTIVE_SKILLS.md
│       ├── SESSION_MEMORY.md
│       └── turns.jsonl
│
├── .agents/
│   └── skills/
│
├── .claude/
│   ├── settings.json
│   └── skills/
│
├── .codex/
│   └── hooks.json
│
├── docs/
│   ├── standards/
│   ├── templates/
│   ├── decisions/
│   └── checklists/
│
├── logs/
│   └── skill-usage.jsonl
│
├── scripts/
│   ├── agent_runtime.py
│   ├── validate_standard.py
│   └── vlco_build.py
│
├── schemas/
└── tests/
```

---

# Troubleshooting

## The agent forgets after one turn

Check:

```text
.agent/runtime/SESSION_MEMORY.md
SESSION_HANDOFF.md
```

Then run:

```bash
python scripts/agent_runtime.py status
```

Common causes:

- the standard is outside the product repository;
- the agent was started from the wrong folder;
- hooks were not approved;
- the previous turn was not closed;
- the agent was not restarted after hook or skill changes;
- an ordinary web chat is being used instead of a repository coding runtime.

---

## Skills are not being used

Confirm:

```text
.agents/skills/
.claude/skills/
```

Test routing:

```bash
python scripts/agent_runtime.py manual-start \
  --prompt "Redesign the management dashboard and define KPI drill-down"
```

Expected:

```text
dashboard
design-system
enterprise-ui-review
skill-governance
```

Inspect:

```text
.agent/runtime/ACTIVE_SKILLS.md
```

---

## The agent starts coding too quickly

Use:

```text
Treat this as FULL or DELTA mode.

Do not implement until the READY CHECK is complete and approved.
```

---

## The agent asks too many questions

Use:

```text
Use the smallest sufficient discovery round.

Recommend a default answer for every question.

Stop asking when implementation can safely begin.
```

For a bounded task:

```text
Treat this as EXECUTE mode.

The task and acceptance criteria are approved.

Do not run full discovery.
```

---

## The UI still looks generic

Use:

```text
Use the design-system and enterprise-ui-review skills.

Create or update DESIGN.md before implementation.

State:
- the primary design archetype;
- adopted patterns;
- rejected patterns;
- colour tokens;
- typography;
- layout;
- component states;
- responsive rules;
- motion rules.
```

---

## The Stop hook interrupts the agent

Close the active turn:

```bash
python scripts/agent_runtime.py close-turn \
  --summary "Completed work" \
  --next "Next action"
```

Reset a stale turn:

```bash
python scripts/agent_runtime.py reset-turn \
  --reason "Previous session ended unexpectedly"
```

---

# What this repository does not do

It does not:

- automatically control another repository;
- make an ordinary GitHub page execute local hooks;
- guarantee correct software because the files exist;
- replace business judgement;
- replace human approval;
- permit protected brand or code copying;
- remove the need to inspect tests and evidence.

The framework works when it is installed inside the actual product repository and used through a supported coding-agent runtime.

---

# Roadmap

- [x] Progressive-disclosure project standard
- [x] Runtime state and session memory
- [x] Native Codex skills
- [x] Native Claude Code skills
- [x] Prompt-based skill routing
- [x] Completion gate
- [x] Skill evidence
- [x] Design intelligence
- [x] Runtime doctor and smoke test
- [ ] Packaged CLI installer
- [ ] Automatic skill effectiveness reports
- [ ] Organisation-level policy overlays
- [ ] MCP server
- [ ] Cross-project health reporting

---

# Contributing

This repository is currently maintained as a controlled source-available standard.

Before proposing a change:

1. identify the observed failure or missing behaviour;
2. provide evidence;
3. show the affected rule, skill, test, or runtime component;
4. add or update a behaviour test;
5. avoid expanding the standard without a clear operational benefit.

Open an issue before making a large structural change.

---

# Licence

```text
Source Available — Not Open Source
```

The repository is available for reference, evaluation, learning, and attributed internal use.

Commercial redistribution, resale, white-labelling, and substantial republication require permission from V L & CO.

See:

- [LICENSE.md](../LICENSE.md)
- [NOTICE.md](../NOTICE.md)

---

<div align="center">

## Built by V L & CO

**Judgement before answers. Evidence before opinion. Verification before confidence.**

Copyright © 2026 V L & CO. All rights reserved.

</div>
