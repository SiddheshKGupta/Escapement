---
name: agent-orchestration
description: Use when a plan contains independent research, implementation or review tasks that benefit from fresh-context subagents or parallel execution. Do not parallelise tasks that modify the same state without a merge protocol.
---

# Agent Orchestration

## Eligibility

Parallel execution requires:

- at least two independent tasks;
- explicit input and output contracts;
- separate files or non-conflicting state;
- bounded context for each agent;
- named integration owner;
- deterministic verification.

## Procedure

1. Choose the smallest number of agents.
2. Give each agent only the context needed for its task.
3. Require an artifact, evidence and unresolved issues.
4. Use two-stage review for implementation:
   - specification compliance;
   - engineering quality.
5. Merge sequentially through the integration owner.
6. Re-run whole-system verification after merge.

Prefer installed Superpowers subagent-driven-development or
dispatching-parallel-agents when compatible.
