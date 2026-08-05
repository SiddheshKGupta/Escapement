# Capability Strength Architecture

## Objective

Use more capabilities to their full strength without forcing more context into
one agent turn.

## Core distinction

```text
Native skill
→ built-in executable fallback

Capability strength
→ narrow specialised behaviour from a skill, methodology, plugin or tool

Strategy adapter
→ maps an external system's subskills to lifecycle phases

Overlap matrix
→ decides authority, substitution, pairing and sequence
```

A repository may contain thirty skills while one phase loads only three native
procedures and five specialist strengths.

## Lifecycle

```text
ORIENT
→ DISCOVER
→ RESEARCH
→ BRAINSTORM
→ SPECIFY
→ PLAN
→ IMPLEMENT
→ VERIFY
→ POLISH
→ RELEASE
```

The phase is an isolation boundary.

When the phase advances:

1. completed outputs and evidence are persisted;
2. previous doctrine and specialists are unloaded;
3. the next phase's native skills and strengths are selected;
4. the context budget is recalculated;
5. external candidates remain inactive until approved.

## Decision support

Before substantive planning, the runtime:

- identifies the actual decision;
- inspects repository state;
- identifies material unknowns;
- asks at most five questions;
- recommends a default;
- explains the consequence of choosing differently;
- generates an improved execution prompt;
- creates a research and lifecycle plan.

## Domain research

```text
Project evidence
→ law, regulator or standards body
→ official documentation
→ primary disclosures
→ institutional research
→ reputable industry research
→ community and practitioner signals
```

Agent Reach and Last30Days are supporting channels. Context7 is specialised for
current technical documentation. The 500+ agent catalogue is a blueprint
discovery source.

## Design

`docs/standards/design-intelligence.md` is the supreme design constitution.

```text
RESEARCH   → UI/UX Pro Max
BRAINSTORM → Taste or another selected art director
SPECIFY    → Design system + UI/UX Pro Max
IMPLEMENT  → frontend-design + conditional Emil motion
VERIFY     → Impeccable + browser evidence + conditional Emil review
POLISH     → Impeccable + Stop Slop + conditional motion improvement
```

The constitution remains active across every design phase.

## Engineering behaviour

```text
Karpathy Guidelines
→ baseline:
   think first
   simplify
   change surgically
   define verifiable goals

Ponytail
→ implementation intensifier:
   YAGNI
   native platform first
   standard library first
   minimum code
```

Ponytail is not a second permanent doctrine.

## Context budgets

```text
Kernel:                       <= 700 words
Automatic phase context:      <= 1,800 words
Invoked native skill context: <= 1,200 words
Native skills:                <= 5 normal / 6 programme
Capability strengths:         <= 8 per active phase
```

Automatic and invoked context are measured separately because skill bodies are
loaded only when invoked.

## Readiness

Every route contains:

```text
Detected native skills
Active native skills
Active specialist strengths
External install or load candidates
Overlap decisions
Lifecycle use
```

The readiness audit prevents a catalogue entry from being mistaken for an
installed capability.

## Parallel execution

Parallel work requires:

- independent tasks;
- non-conflicting state;
- explicit input and output contracts;
- named integration owner;
- merge order;
- deterministic whole-system verification.

Subagent-driven development is preferred where tasks are sequential but benefit
from clean contexts.

## Evidence

`PASS` requires executed checks and existing evidence.

The runtime cannot mark a critical failure as passing. Verification and release
phases require structured checks or a truthful documented exception.
