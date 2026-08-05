---
owner: V L & CO
product: Escapement
version: "6.0.0"
mode: runtime-enforced
purpose: "Deliver enterprise software through executable specifications, bounded work, structured evidence, and durable state."
---

# Escapement Agent Instructions

## Prime Rule

**Understand enough. Decide enough. Build. Test. Prove. Persist.**

The repository is the system of record. Chat is not.

## Mandatory Runtime Protocol

For every material prompt:

1. Read `.agent/runtime/ACTIVE_CONTEXT.md`.
2. Read `.agent/runtime/ACTIVE_SKILLS.md`.
3. Read `PROJECT_STATE.yaml`.
4. Read `feature_list.json`.
5. Continue an existing open turn rather than replacing it.
6. Invoke every selected native skill.
7. Work on one bounded feature or task.
8. Capture deterministic checks with `scripts/run_check.py`.
9. Do not mark a feature `passing` directly.
10. Close the turn with structured evidence before the final response.

Manual fallback:

```bash
python scripts/agent_runtime.py manual-start --prompt "User request"
```

## Specification Flow

For material new work:

```text
Constitution
→ Specification
→ Plan
→ Tasks
→ Feature list
→ Implementation
→ Verification
→ Convergence
```

Do not implement `FULL` work without:

- an approved readiness gate;
- a specification;
- a plan;
- actionable tasks;
- at least one feature with a verification command.

## Work Modes

| Mode | Use |
|---|---|
| `FULL` | New application, product, module, architecture, or major workflow |
| `DELTA` | Material change to an existing product |
| `EXECUTE` | Approved ticket, isolated bug, or bounded change |

`FULL`: Inspect → discover → specify → plan → approve → build.  
`DELTA`: Read state → assess impact → update artifacts → approve → build.  
`EXECUTE`: Confirm ticket/files/acceptance/checks → implement → prove.

## Feature List Rules

- File: `feature_list.json`
- One feature is active by default.
- Every feature requires behaviour, verification, state, and evidence.
- Allowed states: `not_started`, `active`, `blocked`, `passing`.
- Only `scripts/feature_list.py verify <id>` may move a feature to `passing`.
- A failed verification keeps the feature active or blocked.
- Feature scope should be completable in one focused session.
- Project completion requires zero non-passing required features.

## Readiness Gate

For `FULL` and material `DELTA` work:

```text
READY CHECK
Scope:
Non-goals:
Users:
Behaviour:
Workflow:
Data/KPIs:
Permissions:
Integrations:
UI direction:
Security:
Scale:
Specification:
Plan:
Tasks:
Active feature:
Selected skills:
Required checks:
Open risks:
Ready to build: YES/NO
```

Proceed only after approval or explicit instruction to proceed with listed
assumptions.

## Skill Rule

Use the smallest useful skill stack.

```text
Capability
→ Primary skill
→ Why selected
→ Required artifact
→ Verification
→ Overlap rejected
```

Maximum active material skills: 4 unless an explicit reason is recorded.

Canonical skills:

```text
skills/<skill>/SKILL.md
```

Native generated copies:

```text
.agents/skills/<skill>/SKILL.md
.claude/skills/<skill>/SKILL.md
```


## External Capability Rule

Before recommending, installing, copying, or invoking an external skill, plugin,
repository, CLI, MCP server, service, or agent framework:

1. Read `catalog/external-resources.json`.
2. Match the task to the resource's `triggers` and `use_when`.
3. Verify the current licence at the exact tag or commit.
4. Prefer external integration over copying source.
5. Check maintenance, overlap, hooks, permissions, network access, credentials,
   destructive behaviour, and data handling.
6. Request approval for installation, dependencies, MCP registration, network
   access, credentials, licence-sensitive reuse, or security testing.
7. Pin the version or commit.
8. Update `THIRD_PARTY_NOTICES.md` and the decision log.
9. Capture installation and validation evidence.

A public GitHub repository is not automatically open source. When a catalogue
entry says `must-verify` or `unverified-restrict-copying`, use it only as a
reference or external integration until the licence is confirmed.

Invoke `reference-router` when the user asks to find, compare, install, or use
an external capability, or when the current native skill stack cannot safely
complete the task.

## Evidence Rule

Deterministic checks come first.

Required structured evidence includes:

```text
Command
Start time
Completion time
Exit code
Stdout path and hash
Stderr path and hash
Scope
Result
```

A material turn cannot close as `PASS` when:

- a critical failure exists;
- required output files are missing;
- required evidence is missing;
- selected skills are not declared used;
- no structured check record exists;
- any required check fails.

Model-entered check labels are declarations, not proof.

## Security Rule

Before approving or committing sensitive work:

- scan for secrets;
- inspect project hooks;
- inspect MCP servers;
- validate inputs and permissions;
- preserve least privilege;
- avoid remote `curl | shell` installation inside project hooks;
- sandbox authorised external security tools;
- never test a system without permission.

Invoke `security-review` for authentication, permissions, secrets, hooks, MCP,
payments, confidential data, deployment, or external integrations.

## Design Rule

For UI, brand, layout, typography, colour, motion, or responsive work:

1. invoke `design-system`;
2. invoke `enterprise-ui-review` for implementation or review;
3. read `docs/standards/design-intelligence.md`;
4. create or update product `DESIGN.md`;
5. state adopted and rejected patterns;
6. client brand overrides external references.

## Approval Gates

Ask before:

- new dependency;
- schema migration;
- authentication or RBAC change;
- destructive action;
- production deployment;
- paid service;
- external integration;
- confidential-data access;
- broad refactor;
- licence-sensitive reuse;
- security testing outside an authorised local or sandbox environment.

## Observability Rule

Escapement records both:

- runtime observability: commands, outputs, errors, state transitions;
- process observability: specification, sprint contract, rubric, decisions.

Do not rely on unstructured narrative logs for acceptance.

## Session Closure

Every session must leave:

- a clean or explicitly blocked feature state;
- updated shared artifacts;
- structured check records;
- `SESSION_HANDOFF.md`;
- exact next action;
- no ambiguous “mostly done” status.

## Instruction Precedence

1. Safety and platform rules
2. Current user instruction
3. Approved constitution/specification/decisions
4. Nearest folder `AGENTS.md`
5. Root `AGENTS.md`
6. Runtime and project state
7. Loaded native skill
8. Reference material

On conflict: stop, describe the conflict, and recommend a resolution.
