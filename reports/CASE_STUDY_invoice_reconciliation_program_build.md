# Case Study: A GST-Shaped Reconciliation Build, and Four Framework Bugs It Surfaced After the Fact

Recorded: 2026-08-06

## Setup

A `PROGRAM`-tier request against `InvoiceRecon Mini`: a GST-shaped invoice
reconciliation console -- CSV ingestion of invoices and a vendor master,
CGST/IGST billing-type and TDS (HSN/SAC) compliance rules, e-way-bill
threshold checks, two-tier reconciliation matching, and a React dashboard.
Inspired by a fuller CRM process-flow specification the user supplied, but
scoped deliberately smaller by explicit decision, not by omission.

Real `DISCOVER` questions were asked and answered before any code was
written -- scope, rule fidelity, backend/frontend stack, database, single
vs. multi-stakeholder, success definition, approval gate -- each with a
stated recommended default and the consequence of choosing differently,
not silently assumed.

## The integration bug: `reconcile_all()` silently overwriting rule failures

`db.py` (schema/connection layer) was built first, sequentially --
everything else depends on its shape. `rules.py` (GST/TDS/e-way-bill
compliance) and `reconciliation.py` (two-tier vendor matching) were then
genuinely independent against that shared interface and dispatched as
parallel subagents. Each module's own tests passed in isolation.

The integration owner then traced the actual pipeline order the spec
required -- rules first, reconciliation second -- and found that calling
`reconciliation.py`'s `reconcile_all()` directly after a rules pass would
silently overwrite any `INVOICE_ERROR` status with `MATCHED` or
`VENDOR_FILE_ERROR`, since it unconditionally reprocessed every row
regardless of current status. Neither subagent's own test suite exercised
this specific ordering, because neither had visibility into how the other
module's output would be consumed. Fixed by adding `run_full_pipeline()`,
which applies rules first, excludes rule-failing invoices from
reconciliation entirely, and only then reconciles the rest -- the same
class of cross-module seam bug the claims-platform case study found, in a
different pair of modules.

## What the framework did *not* catch on the first pass -- and what that produced

The backend was built correctly and verified. The frontend was where the
process broke down, in four distinct, compounding ways -- each one found
by the user, not by the framework, and each one turned into a durable fix
in this repository rather than a one-off correction:

**1. No design decision was ever asked.** `design-system`'s own triggers
are explicit design vocabulary ("design system", "brand", "colour").
"Build a React frontend: upload form, results table" matched only
`enterprise-ui-review`/`frontend-implementation`'s generic UI-building
triggers, so a full visual design shipped with zero decision surfaced --
directly contradicting the "ask, don't self-answer" rule this same repo
had shipped one turn earlier. Fixed in
[PR #17](https://github.com/SiddheshKGupta/escapement/pull/17): `design-system`
is now forced into the routed set whenever a UI-implementation skill
matches and `design-system` itself hasn't.

**2. No research, no domain-KPI expertise, no theme choice.** Even after
#17 was live, the actual redesign happened without applying it live in the
same session -- no research into how comparable AP/reconciliation
dashboards are structured, no domain-appropriate KPI selection, no
light/dark decision. Corrected in-session by actually running the newly
fixed procedure: real research (AP/reconciliation dashboard conventions,
GST-tool patterns), a real `AskUserQuestion` covering archetype, KPI
selection, and theme default -- then building only what was decided.

**3. The framework's own capability-readiness report was never shown.**
`scripts/capability_audit.py` already computed exactly which skills were
active and which external resources were candidates -- it was just never
run or surfaced to the user, because nothing in `AGENTS.md` said to. Fixed
in [PR #18](https://github.com/SiddheshKGupta/escapement/pull/18): showing
it is now a required step before implementing, for every `MATERIAL`/`PROGRAM`
request.

**4. Raw, locale-blind numbers.** The rebuilt dashboard still showed plain
unformatted figures for a domain that is unambiguously India/INR -- no
rupee symbol, no Indian digit grouping, no Lakh/Crore convention, caught
directly by the user. Fixed in
[PR #20](https://github.com/SiddheshKGupta/escapement/pull/20): a new
`reporting-standard` skill, synthesizing (and genericizing, with no
company branding retained) a KPI/reporting doctrine the user had
separately developed, plus a new explicit rule that currency and
number-format conventions must match the confirmed business locale and be
applied uniformly across every surface.

## The fifth finding: a question, not a bug

Asked directly whether a fixed 700-word kernel budget bottlenecks a
genuinely large multi-module build, the honest answer was no -- the
budget bounds per-turn context, not total system complexity, and the repo
is the durable record across turns. But answering that question required
checking, and the check found a real gap: nothing in the runtime had any
concept of a *module* spanning many turns within one `PROGRAM`, so nothing
would have caught two modules quietly disagreeing on a shared schema or
design system. Fixed in
[PR #19](https://github.com/SiddheshKGupta/escapement/pull/19):
`program_modules.py`, a durable per-project registry that blocks a module
from leaving `SPECIFY` until it has checked every artifact it shares with
the others.

## What this demonstrates that the prior case studies didn't

The claims-platform study showed the framework catching a real bug
*within* one build, using its existing mechanisms as designed. This one
shows the opposite and more useful failure mode: the framework's own
doctrine being violated by the agent operating it, caught by the user
each time, and turned into a structural fix rather than an apology --
four separate times, on one build, in one session. A framework that only
works when the agent remembers to use it correctly is not yet done; each
of these fixes moved one more piece of "remembering correctly" out of the
agent's discretion and into something the router or the kernel enforces
on its own.
