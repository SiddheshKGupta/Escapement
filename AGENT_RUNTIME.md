# Escapement Runtime

```text
Prompt
→ Decision brief
→ Task tier and register
→ Current phase
→ Domain/research need
→ Phase-specific doctrine and skills
→ External strategy candidates
→ Work and evidence
→ Advance phase
→ Handoff
```

## Active files

```text
.agent/runtime/ACTIVE_CONTEXT.md
.agent/runtime/CONTEXT_PACK.md
.agent/runtime/current-turn.json
```

The context pack contains only the current phase.

## Phase transition

Complete the phase artifact, then run:

```bash
python scripts/agent_runtime.py advance-phase \
  --phase RESEARCH \
  --summary "Discovery decisions resolved" \
  --skills-used "decision-coach,project-discovery" \
  --files "PROJECT_CONTEXT.md" \
  --evidence "PROJECT_CONTEXT.md"
```

Implementation, verification and release phases require structured checks or a
truthful reason where a check is not applicable.

## Revising the phase plan

The default plan is decided once from the prompt and cannot see what
inspection during `DISCOVER` turns up. If it no longer fits:

```bash
python scripts/agent_runtime.py replan-phases \
  --add-phase VERIFY --reason "Touches stored credentials."
python scripts/agent_runtime.py replan-phases \
  --remove-phase POLISH --reason "Backend-only, no user-facing surface."
```

Only the ten cataloged phases can be added or removed. The current phase and
any phase already completed with recorded evidence cannot be removed. Every
revision requires a reason and is permanently recorded on the turn.

## Multi-module PROGRAMs

A turn's phase plan covers one piece of work. A PROGRAM with several
modules (e.g. billing, CRM core, admin portal) runs each module through
its own `DISCOVER` -> `RELEASE` cycle across many turns -- nothing else
tracks that the modules exist, or that they agree on the artifacts they
share (schema, `DESIGN.md`, `DOMAIN_CONTEXT.md`).

```bash
python scripts/program_modules.py set-program --name "CRM Platform"
python scripts/program_modules.py add-shared --path docs/specs/SCHEMA.md
python scripts/program_modules.py add-shared --path DESIGN.md
python scripts/program_modules.py add-module --id billing --name "Billing"
python scripts/program_modules.py add-module --id portal --name "Customer Portal" \
  --depends-on billing
python scripts/program_modules.py list
```

A module cannot move past `SPECIFY` (`--status plan`/`implement`/`verify`/
`polish`/`release`/`done`) until it has checked every registered shared
artifact:

```bash
python scripts/program_modules.py set-status --id billing --status plan \
  --checked-shared docs/specs/SCHEMA.md,DESIGN.md
```

A module also cannot pass that gate while a declared dependency isn't
`done`. State lives in `docs/PROGRAM_MODULES.json`, owned by the project,
not overwritten by `update`/`repair`.

## Manual start

```bash
python scripts/agent_runtime.py manual-start --prompt "User request" --json
```

## Status and closure

```bash
python scripts/agent_runtime.py status
python scripts/agent_runtime.py close-turn ...
python scripts/agent_runtime.py reset-turn --reason "Reason"
```

The Stop gate blocks at most once and cannot create an infinite loop.

## Harness observability

`close-turn` already writes to `.agent/runtime/turns.jsonl` and
`logs/skill-usage.jsonl` on every closure -- nothing reads them back as a
trend until asked:

```bash
python scripts/escapement.py observability --root .
```

Reports closed-turn counts, tier/closure-result distribution, phase-replan
frequency and reasons, skills routed but never marked used, and why
packs/skills got rejected (overlap, phase-skill-limit, context budget --
the same signal that would have flagged a bloating skill file the day it
happened). An empty report means turns aren't being closed, not that the
harness is healthy -- `close-turn` is what populates this.

## Harness ablation

Observability shows what the harness did. Ablation asks whether a
component was worth having at all:

```bash
python scripts/escapement.py ablate                  # list ablatable components
python scripts/escapement.py ablate decision-coach   # control vs ablated
```

Components are declared in `catalog/harness-components.json` with a
hypothesis, a declared context cost, and how to remove them. A run copies
the repository to a throwaway directory, removes the component's registry
entry *there*, and runs the existing corpus under `evals/` twice. Canonical
source files are never modified.

The report is a factual diff -- which cases changed result, which skills or
strengths were lost, how many context words were freed. It deliberately
computes no score or significance figure: 22 routing cases cannot support
one, and a fabricated number is worse than none.

Read the output carefully in one respect. "No measurable difference" means
the corpus does not exercise that component -- a statement about corpus
coverage, not proof the component is useless. The current corpus is
routing-only: it can see skills, strengths, packs, questions and context
words, but not retries, tool activity, turn closure or final task quality.
Measuring those needs a live-execution corpus that does not exist yet.

When that corpus is built, extend the suites under `evals/` rather than
starting a second benchmark system. Ablation compares harness
configurations on one host; host conformance compares hosts on one harness.
Both need the same tasks, or neither result is comparable.
