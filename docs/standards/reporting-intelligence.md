# Reporting and KPI Standard

**Status: domain expertise, subordinate to [Design Intelligence](design-intelligence.md) for anything visual.**

This standard governs how numbers are structured, broken down, and formatted
in dashboards, KPI tiles, tables, and exports. Design Intelligence governs
what they look like (colour, layout, density); this standard governs whether
they are correct, traceable, and honestly labelled. Both apply together to
any reporting surface.

## 1. Every number needs a breakdown

A KPI is incomplete unless a user can get to:

1. Definition
2. Unit
3. Calculation formula
4. Source system
5. Data freshness
6. Applied filters
7. Comparative period
8. Record-level breakup
9. Owner or responsible function
10. Exception status

Do not show a consolidated number without a usable route to its components.
A KPI card without meaning and drill-down is decoration, not information --
this is the same rule the design-system skill's KPI-card requirement points
back to.

## 2. Absolute numbers first, percentages second

For owner/management-facing views, lead with counts, values, ageing, pending
work, value at risk, and exceptions. Use percentages as supporting analysis,
not the headline. State what needs action now before showing derived ratios.

## 3. Three-layer reporting model

```text
Layer 1 -- Management Summary: headline numbers, trend, risk/exception
           indicator, period comparison, target comparison, decision cue.
Layer 2 -- Analytical Breakdown: dimension-wise breakup, trend,
           contribution, ageing, status distribution, variance drivers.
Layer 3 -- Record-Level Evidence: underlying records, transaction detail,
           source references, activity history, approval trail, export.
```

Each KPI tile should be a real entry point into Layer 2/3 for that metric --
clicking it should filter or drill into the records behind the number, not
just sit there as a static tile.

## 4. Mandatory time views

Where the domain has a natural reporting period, support current-period vs.
previous-period and current vs. target/budget, applied consistently across
KPI tiles, charts, tables, drill-downs, and exports. The active period must
always be visible. Use the domain's actual fiscal-year convention (confirmed
in `DOMAIN_CONTEXT.md`), not a silently assumed calendar year.

## 5. Reconciliation

Dashboard totals, table totals, and exported totals must reconcile with each
other and with the record-level data underneath. A report is not complete
merely because it renders -- state control totals, record counts, and last
refresh timestamp somewhere a reviewer can check them.

## 6. Locale-correct numeric and currency formatting

Currency symbol, digit grouping, and unit-scale convention must match the
business locale confirmed in `DOMAIN_CONTEXT.md` -- not the developer's
default locale, and not left as raw unformatted numbers. This must be
applied *uniformly* across every surface showing the same figures: KPI
tiles, tables, and exports must never disagree on formatting for the same
kind of number.

Concretely, for an India/INR domain:

- Prefix amounts with `₹`.
- Group digits in the Indian convention (last three digits, then pairs):
  `₹1,20,000.00`, not `₹120,000.00`.
- Abbreviate large *aggregate* figures using Lakh (`10^5`) and Crore
  (`10^7`) -- e.g. a KPI tile showing `₹45.00 L` rather than
  `₹45,00,000.00`.
- Keep *record-level* rows exact and unabbreviated -- reconciliation
  precision matters more than scannability at that layer (see §5).

The same principle generalises to any other confirmed locale: match its real
convention (grouping, symbol placement, decimal separator, unit-scale
language), and confirm the locale in `DOMAIN_CONTEXT.md` rather than
inferring it silently -- unless, as with an already-confirmed GST/India
domain, the locale is directly entailed by facts already confirmed, in
which case record it as entailed rather than asking again.

## 7. Charts

Every chart states: the business question it answers, metric, unit, period,
source, freshness, filter state, aggregation logic, and comparison basis.
Prefer a table over a chart when exact values matter more than shape.
