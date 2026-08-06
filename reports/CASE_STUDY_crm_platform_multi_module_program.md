# Case Study: A Four-Module CRM PROGRAM, and What Building It Actually Fixed

Recorded: 2026-08-06

## Setup

A `PROGRAM`-tier request against `CRM Platform`: lead onboarding, GST
document compliance gating, invoice reconciliation, and inventory rental
lifecycle -- four independently-owned backend services plus one frontend,
registered as a real multi-module `PROGRAM` via `program_modules.py`
(shipped one turn earlier in this same session, and immediately put to
work rather than left theoretical).

Real `DISCOVER` questions were asked and answered for every new module
before any code was written -- 12 material decisions total (capture
channel, qualification model, conversion shape, duplicate handling;
document set, storage shape, validation rigor, gating; asset shape,
lifecycle states, billing scope, due-date handling), each with a stated
recommended default and the alternative that was turned down, all
recorded in `DOMAIN_CONTEXT.md`. `reconciliation` was reused directly
from the `invoice-recon-mini` case study's verified code rather than
rebuilt -- 29/29 ported tests passed with zero modification.

## The registry catching a real bug live

Attempting to advance `document-compliance` past `SPECIFY` failed with
`FAIL: dependency lead-onboarding is not done` -- correct behaviour. The
underlying cause was sloppy bookkeeping: `lead-onboarding` was
functionally complete (17/17 tests) but its registry status had never
been advanced past `implement`. Not a theoretical benefit of building the
registry -- an actual save, in the very first module transition after it
shipped.

A second registry finding: `DOMAIN_CONTEXT.md` already said
`inventory-rental` needs compliance clearance the same way
`reconciliation` does, but `docs/PROGRAM_MODULES.json` only listed
`lead-onboarding` as its dependency -- the registry and the confirmed
business rule had quietly drifted apart before a line of that module's
code was written. Fixed before starting the module, not after.

## Reuse exposed a real integration gap, not a bug in the reused code

Wiring `reconciliation` to `document-compliance`'s compliance gate
required a `customer_id` on every invoice -- and the ported schema had
none at all, because `invoice-recon-mini` was standalone (vendor invoices
only, no CRM customer concept). This wasn't a defect in the original
module; it's the gap between "verified in isolation" and "verified in
the context it's now reused in." Shipping the reuse without checking that
fit would have produced a reconciliation pipeline that could never
actually enforce the gate it was built to enforce. Fixed: added
`customer_id INTEGER NOT NULL`, updated the upload endpoint and all
affected tests, then built `compliance_gate.py` -- an HTTP check against
`document-compliance`'s `/compliance-status` endpoint that **fails
closed** (an unreachable compliance service means not compliant, never
"assume it's fine"), injectable so tests aren't network-dependent. The
same module reused into `inventory-rental` with zero changes.

## A leftover dev server that looked like a working one

Starting all four backend services for real (not the test client) to
verify the frontend, port 5000 returned invoice data that looked like
real reconciliation output -- but it was `invoice-recon-mini`'s own dev
server from hours earlier in the same session, never stopped, still
holding the same default port this module's `app.py` also defaults to.
The new server had silently failed to bind; curl was routed to whichever
process actually held the port. This is the dangerous failure mode
specifically because the response was well-formed and plausible, not an
obvious error. Fixed operationally: killed every stray process (8 total,
several Flask-reloader parent/child pairs), wiped the four `.db` files,
restarted deliberately, and verified each response was genuinely empty
before trusting any of it.

## The UI/UX gap: correct doctrine, never actually applied

`frontend-implementation/SKILL.md` already instructed covering loading/
empty/error states, motion, focus, and responsiveness -- correct,
already-routed doctrine, not a missing mechanism. It was still skipped
building the real frontend, because implementation happened by writing
code directly rather than by operating through the phase-routed
skill-loading mechanism for `IMPLEMENT`/`POLISH`. Applying
`enterprise-ui-review`'s 13-point checklist for real, after the fact,
found: zero motion anywhere, no loading states outside the dashboard, no
error states at all, zero responsive breakpoints, and no data-freshness
indicator despite `reporting-standard`'s own rule requiring one -- all
fixed. The durable fix went into Escapement itself:
`scripts/ui_quality_gate.py`, a deterministic scanner (same shape as
`security_gate.py`, same honest heuristic limitation) for these exact
signals, so the next build doesn't depend on an agent remembering to
apply doctrine that was already correct and already routed.

## No input validation, and a bug the tests couldn't have caught

A real lead-capture form had no validation at all: `name` accepted bare
digits, `contact_phone` accepted any string, `contact_email` didn't even
require an `@`. `data-architecture/SKILL.md` covered database/schema/API
decisions in depth but said nothing about basic field-shape validation --
fixed in Escapement itself with a new baseline-validation section
(name/phone/email/money/date defaults, overridden only by a stated
`DOMAIN_CONTEXT.md` rule), then applied here: server-side regex
validation, a country-code selector instead of one freeform phone field,
17 new tests.

Verifying it live in the browser then surfaced a bug the unit tests could
not have caught: the HTML `pattern` attribute
`[A-Za-z][A-Za-z\s'-]{1,99}` threw `Invalid character in character
class` at submit time -- the browser's pattern-regex compiler is
stricter about an unescaped trailing hyphen in a character class than
Python's `re` is. Every submission was silently failing with a JS
exception, not a clean validation message. Caught only by checking
`checkValidity()` directly rather than trusting a single console-log
read, which turned out to return stale buffered entries that would have
looked like the bug was still present if trusted at face value.

## What this demonstrates that the prior case studies didn't

The reconciliation case study showed the framework's own doctrine being
violated by the agent operating it -- caught by the user, fixed as
structural changes. This one shows the next stage of the same discipline
compounding: a registry built one session catching a real bug in its
first real use; a reused module's hidden context-dependency surfacing
only when actually wired into something new; and a UI-quality gap fixed
not by writing more prose doctrine (there was already good doctrine) but
by building the deterministic check that doesn't depend on an agent
reading it. Four modules, 108 backend tests, one frontend, and nine
distinct findings -- most of them caught by actually running the thing
end to end in a browser, not by code review alone.
