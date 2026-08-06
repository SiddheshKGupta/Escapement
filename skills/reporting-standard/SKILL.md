---
name: reporting-standard
description: Use when building dashboards, KPI tiles, management reports, or reconciliation views -- covers KPI breakdown completeness, the three-layer reporting model, and locale-correct currency/number formatting (symbol, digit grouping, unit scale) applied uniformly across every surface. Do not use for visual design decisions (colour, layout, typography) -- see design-system.
---

# Reporting and KPI Standard

Read `docs/standards/reporting-intelligence.md` before building or
reviewing any dashboard, KPI tile, management report, or reconciliation
view. It is domain expertise, not visual design -- it governs whether the
numbers are correct, traceable, and honestly formatted; `design-system`
governs what they look like.

## Before writing a single KPI tile or table column

1. Confirm the business locale (currency, digit grouping, fiscal-year
   convention) in `DOMAIN_CONTEXT.md` -- or record it as directly entailed
   by domain facts already confirmed there, rather than defaulting to
   whatever the developer's own locale happens to be.
2. Decide which layer each number belongs to (Management Summary /
   Analytical Breakdown / Record-Level Evidence) and give it the
   completeness that layer requires -- a headline tile still needs a real
   drill-down path, not just a static value.
3. Pick one formatting convention for the confirmed locale and apply it
   *everywhere* the same kind of number appears -- KPI tiles, tables, and
   exports must never disagree with each other.

## The mistake this exists to prevent

A dashboard built without reading this shows technically-correct numbers
that are still wrong for the audience: raw unformatted figures instead of
the locale's real currency convention, KPI tiles with no drill-down, totals
that do not reconcile with the table beneath them, or the same number
formatted two different ways on the same screen.
