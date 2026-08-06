---
name: lifecycle-planning
description: Use during DISCOVER, immediately after inspecting the repository, to check whether the deterministic phase plan actually fits the task. Revise it with replan-phases when it does not. Do not use to invent phases outside the fixed ten-phase catalog.
---

# Lifecycle Planning

The phase plan you were handed is a default, not a judgement. It was built
by matching keywords in the prompt against a fixed pattern set, before
anyone looked at the repository. It has no memory of what DISCOVER's own
inspection turns up.

1. Read the current `phase_plan` and the reason each phase is present.
2. Inspect the repository for constraints the prompt's wording did not name
   -- an existing security posture, a compliance obligation, a data model
   the request would touch without saying so.
3. Ask: does a phase in the plan not apply here? Does the task need a phase
   that is missing -- most commonly `VERIFY`'s security-review weight, when
   the request touches credentials, permissions, or external input without
   using the word "security"?
4. If the plan is wrong, revise it before continuing:

```bash
python scripts/agent_runtime.py replan-phases --add-phase VERIFY --reason "Touches stored credentials; the prompt never said 'security' so the default router weight for this phase under-served it."
python scripts/agent_runtime.py replan-phases --remove-phase POLISH --reason "Backend-only change, no user-facing surface to polish."
```

5. State the revision and its reason in the phase's `--summary` when you
   advance, so the record explains itself without needing the raw override
   log.

## Boundaries

- Only the ten cataloged phases exist (`ORIENT`, `DISCOVER`, `RESEARCH`,
  `BRAINSTORM`, `SPECIFY`, `PLAN`, `IMPLEMENT`, `VERIFY`, `POLISH`,
  `RELEASE`). This is revision of sequence, not invention of new phases.
- Cannot remove the current phase or a phase already completed with
  recorded evidence -- a revision is forward-looking, not retroactive.
- Every revision requires a reason and is permanently recorded
  (`phase_plan_overrides` on the turn, `turns.jsonl` as
  `phase-plan-revised`). Do not use this to quietly drop required work.

## Coordinate with parallel and sub-agent dispatch

A phase you add or keep may still be a poor fit for the default skill
routing if it is large enough to warrant a fresh-context sub-agent. Decide
phase fit and sub-agent fit together, not as two separate passes: if a phase
requires independent, non-conflicting work, apply the same criteria as
`AGENTS.md`'s "Agents and Parallel Work" section (independent tasks,
separate files, explicit input/output contracts, a named integration owner,
deterministic verification after merge) before dispatching, rather than
defaulting to a single sequential agent because the phase plan happens to
list it that way.
