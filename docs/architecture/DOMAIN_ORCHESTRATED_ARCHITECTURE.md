> Superseded by `CAPABILITY_STRENGTH_ARCHITECTURE.md` in v6.3. Retained for release history.

# Domain-Orchestrated Architecture

## Objective

Help users ask better questions, make better decisions and deliver stronger
systems without forcing every skill, agent, methodology and reference into one
context window.

## Architecture

```text
Kernel
→ Decision brief
→ Domain evidence
→ Phase plan
→ Phase-specific doctrine and skills
→ Optional external strategy adapter
→ Fresh-context agents
→ Deterministic verification
→ Durable handoff
```

## Why phase orchestration

Capabilities have different strengths.

- Superpowers brainstorming is strongest before design approval.
- Writing-plans is strongest after an approach is approved.
- TDD and subagent-driven development belong during implementation.
- Browser, code-review and security tools belong during verification.
- Agent Reach and Last30Days belong in targeted research.
- 500+ AI Agent Projects is useful for blueprint discovery, not blind deployment.

The runtime therefore uses more capabilities across the lifecycle while keeping
the active phase context below the configured budget.

## Decision assistance

For MATERIAL and PROGRAM work, Escapement:

1. identifies the actual decision;
2. inspects project evidence;
3. asks no more than five high-impact questions;
4. recommends defaults;
5. explains the consequence of other choices;
6. produces an improved execution prompt;
7. suggests standards and trend research where it can change the decision.

## Research

Authoritative evidence comes first.

```text
Project evidence
→ regulator, law or standards body
→ official documentation
→ primary disclosures
→ institutional research
→ industry research
→ practitioner and community signals
```

Agent Reach and Last30Days extend coverage. They do not replace authoritative
sources.

## Parallel agents

Parallel execution is permitted only when tasks are independent and the plan
defines:

- separate inputs and outputs;
- non-conflicting files or state;
- an integration owner;
- merge order;
- whole-system verification.

## Agent blueprints

The agent catalogue is a discovery source.

Every linked implementation must be checked for licence, maintenance, runnable
code, tests, dependencies, data handling, secrets, deployment and evaluation
before reuse.

## Context economy

```text
Kernel:              <= 700 words
Active phase pack:   <= 1,800 words
Doctrine per phase:  <= 3 normally
Skills per phase:    <= 4 normally
```

The lifecycle may use many capabilities. The current phase remains focused.
