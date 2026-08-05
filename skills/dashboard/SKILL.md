---
name: dashboard
description: Use for dashboards, KPIs, MIS, metrics, management reporting, analytics, charts, drill-down, ageing, or reconciliation. Do not use for decorative data visualisation without an operational decision.
---

# Dashboard and KPI Contract

For every material metric define:

```text
Meaning | Formula | Unit | Period | Source | Freshness | Filters
Breakdown | Drill-down | Target/comparison | Owner | Access | Reconciliation
```

Procedure:

1. Identify the decision supported.
2. Confirm source records and time logic.
3. Define KPI contracts before visualisation.
4. Select the simplest chart or table.
5. Add loading, empty, partial, stale, error, and permission states.
6. Provide record-level drill-down.
7. Reconcile totals.
8. Verify filters and periods.

Critical failures: invented totals, missing source, missing reconciliation,
misleading periods, or colour-only meaning.
