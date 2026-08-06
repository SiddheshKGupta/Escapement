# Project Context

## Product

Escapement

## Release

`6.3.0 — Capability Strength Orchestration`

## Purpose

Help users turn rough requests into better decisions and orchestrate domain
expertise, native procedures, specialist subskills, fresh-context agents and
external tools across the delivery lifecycle.

## Core behavior

```text
Ask better questions
→ recommend defaults
→ research authoritative standards and current practice
→ compare materially different approaches
→ specify behaviour and controls
→ create bounded tasks
→ use subagents where justified
→ implement with specialised skills
→ verify independently
→ polish
→ release with evidence
```

## Architecture

```text
Kernel
→ Domain profile
→ Doctrine packs
→ Native skills
→ Capability strengths
→ Strategy adapters
→ Fresh-context agents
→ External resources
→ Evidence and handoff
```

## Design authority

`docs/standards/design-intelligence.md` is the supreme design constitution.

Design specialists operate beneath it:

- UI/UX Pro Max for research and recommendation;
- Taste for art direction;
- frontend-design for implementation;
- Impeccable for verification and polish;
- Emil Kowalski Skills for motion;
- Open Design for an optional workspace.

## Users

- developers;
- consultants and business analysts;
- product and engineering teams;
- domain experts;
- governance, legal, finance and security reviewers;
- teams using Codex or Claude Code.

## Constraints

- Python standard-library-only core;
- always-loaded kernel below 700 words;
- automatic phase context below 1,800 words;
- invoked native skill context below 1,200 words;
- project-owned state survives updates;
- authoritative evidence before trend signals;
- no automatic external installation;
- no blind deployment of catalogue agent projects;
- human approval for sensitive or irreversible actions;
- organisation-neutral public framework.

## Current inventory

```text
Doctrine packs:         11
Native skills:          34
Capability strengths:   58
Agent patterns:         21
External resources:     54
Strategy adapters:      10
Capability families:    10
Overlap groups:         12
```

## Non-goals

- requiring the user to become a prompt engineer;
- loading every capability into every phase;
- stacking complete competing harnesses;
- treating a repository listing as installation;
- replacing law, standards, policy or domain experts with model inference;
- autonomous offensive security testing;
- hidden telemetry or mandatory cloud memory.
