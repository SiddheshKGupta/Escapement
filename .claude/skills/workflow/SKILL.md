---
name: workflow
description: Use for business processes, approvals, state machines, exception management, maker-checker controls, journeys, escalations, ownership, or SLA. Do not use for a purely visual page with no process behaviour.
---

# Workflow Design

Model:

```text
Trigger | Actors | Inputs | States | Transitions | Rules | Controls
Exceptions | Escalations | Outputs | Audit | SLA | Permissions
```

Separate current and target flows. Define allowed transitions, owner,
permissions, validation, maker-checker rules, exceptions, timeouts, reversals,
duplicates, audit events, and acceptance tests.

Never invent policy, authority, or SLA.
