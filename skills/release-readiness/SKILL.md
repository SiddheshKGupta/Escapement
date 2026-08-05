---
name: release-readiness
description: Use for release, production deployment, go-live, rollout, launch, UAT, handover, or release approval. Do not use during ordinary local implementation.
---

# Release Readiness

Required gates:

- acceptance complete;
- feature list has no required non-passing items;
- structured checks pass;
- security and permissions reviewed;
- migration and rollback defined;
- monitoring ready;
- reconciliation complete;
- performance and accessibility acceptable;
- known risks accepted;
- human approval recorded.

Output `GO / NO-GO`, evidence, risks, owner, rollback, monitoring, and approval.
Never deploy silently.
