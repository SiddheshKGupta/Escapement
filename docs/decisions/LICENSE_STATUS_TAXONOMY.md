# License-status taxonomy consolidation

`catalog/capability-registry.json`'s `license_status` field had grown to
18 distinct values across 67 resources. Consolidated to 7, each with a
genuinely distinct meaning, verified individually rather than merged by
string similarity.

## Why this happened

`license_status` conflates three different axes that should be separate:

1. **Evidence state** — do we actually know the licence, or not?
2. **Action** — what should happen before this resource is adopted?
3. **Resource lifecycle** — is the repository still maintained?

Axis 2 already has its own field (`adoption`, added in the licence-
adoption-gating change: `approval-required` / `verify-licence-first` /
absent). Axis 3 is now covered dynamically by `scripts/registry_audit.py`
rather than needing to be hand-encoded. `license_status` should only ever
have described axis 1, but new entries kept inventing a new spelling for
"we checked and confirmed" instead of reusing `verified` — `verified-
from-readme`, `verified-in-prior-review`, `verified-from-project-docs`,
`verified-from-skill-docs` were all the same fact (someone read a real
source and confirmed the licence), differing only in *where* it was
read, which the `notes`/`do_not` fields already record.

## Method: inspected individually, not pattern-matched

Every rare value was read in full context (`license`, `do_not`, `notes`,
`adoption`, `status`) before deciding whether to fold it, following a
mistake caught earlier in this same session: an early draft of the
overlap-group tag fix matched resources by *tag text* against old group
names and would have wrongly claimed formal group membership for four
resources that never actually had it. The same risk applies here — two
values sounding similar (`verify-current-release` vs `must-verify`) do
not necessarily mean the same evidence state, and one pair that sounds
opposite (`unverified-restrict-copying`) turned out to mean the opposite
of what its name suggests.

## The 7 consolidated values

```text
verified              (49)  a real source was read and the licence confirmed
must-verify            (10)  not yet checked; check before adopting
verified-unlicensed     (2)  checked -- confirmed NO licence file exists
not-open-source          (2)  a commercial service/product; no OSS licence applies
not-code-resource        (2)  content/design reference, not a code dependency
source-required          (1)  exact source repository not yet identified
special-terms            (1)  verified, but a bespoke non-OSS commercial model
```

## Renames worth explaining

- `unverified-restrict-copying` → **`verified-unlicensed`**. The old name
  reads as "we haven't verified this," when the true state is the
  opposite: we verified that no licence file exists, which is itself a
  confirmed, actionable fact (all rights reserved by default), not an
  open question. Applies to `perplexity-cli` and `awesome-claude-skills`
  — the latter's GitHub licence API endpoint returns 404 despite 72k
  stars, exactly the case the licence-adoption-gating change was built
  to catch.
- `not-open-source-service` → merged into **`not-open-source`**. Same
  real category (a commercial offering with no applicable OSS licence)
  under two names.
- `archived-security-review-required` (`puppeteer-mcp`) → **`verified`**.
  The licence itself was confirmed; "archived" is a resource-lifecycle
  fact already carried by `status: discouraged-legacy`, and is now
  independently, dynamically checkable via `registry_audit.py` instead
  of needing a hand-typed static field that would drift the moment
  GitHub's archived flag changes and nobody remembers to update it.
- `verify-current-release`, `verified-review-required-per-release`,
  `mixed-verify-selected-component`, `verified-with-obligations` →
  **`verified`**. Each carries a real nuance (rolling releases, a
  sub-component that may differ, copyleft obligations), but the
  nuance already lives in `do_not`, and the actionable "don't just
  assume, check before adopting" signal already lives in `adoption:
  verify-licence-first` (or `approval-required` for the copyleft case).
  Re-encoding the same nuance a second time in `license_status` was
  redundant, not additive.

## Regression coverage

`LICENSE_STATUS_VALUES` (the closed set of 7) and `license_status_check()`
added to `escapement.py`, wired into `doctor`. Three tests: an
unmodified copy reports all-recognised; a value outside the set (using
one of the retired spellings, `verified-from-readme`) is detected and
named; and all 7 consolidated values are individually accepted, proving
the check isn't just permissive by accident.

## Not done here

`status` (10 distinct values: `catalogued`, `optional`, `conditional`,
`reference-only`, `preferred-when-existing`, `discouraged-legacy`, and
others) was surveyed alongside `license_status` but not consolidated —
unlike `license_status`, each `status` value carries a genuinely distinct
operational meaning rather than being a repeated synonym, so there is no
equivalent sprawl to fix there.
