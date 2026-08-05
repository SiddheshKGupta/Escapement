---
name: quality-engineering
description: Use to define or execute unit, integration, contract, end-to-end, negative, role, accessibility, performance, migration, reconciliation or UAT verification. Do not use to claim PASS without executed evidence.
---

# Quality Engineering

Select the smallest sufficient verification stack:

```text
Static checks
→ Unit tests
→ Integration and contract tests
→ Browser or end-to-end tests
→ Security and permission tests
→ Performance and accessibility checks
→ UAT and reconciliation
```

1. Trace tests to acceptance criteria and failure modes.
2. Reproduce defects before fixing where practical.
3. Verify normal, boundary, invalid, duplicate, timeout, retry, permission and
   recovery paths.
4. Use representative data and roles.
5. Record commands, exit codes, outputs and evidence.
6. Re-run whole-system checks after parallel work is merged.
7. Treat skipped tests as explicit risk, not silent success.

A rendered screen or passing happy path is not sufficient evidence.
