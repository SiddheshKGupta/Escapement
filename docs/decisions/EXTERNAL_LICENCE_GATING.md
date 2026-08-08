# External licence adoption gating

Licence-encumbered resources stay in the catalogue and stay routable. What
changes is that adopting one now requires an explicit decision rather than
an assumption.

## The gap

The rule already existed, in three places:

```text
AGENTS.md                 "Ask before ... licence-sensitive reuse"
capability_router.py:756  "Candidates remain inactive until overlap,
                           licence, security and approval review."
agent_runtime.py:178      "install or load external candidates only
                           after approval"
```

What did not exist was any way to tell *which* resources those sentences
were about. Every candidate rendered identically, so a verified-MIT tool
and a viral-AGPL application looked the same at the point of decision. A
generic warning attached to all 62 resources is a warning about none of
them.

A survey of the registry found 23 of 62 resources carrying licence risk,
and 19 of those declared `use_modes` including `integrate`, `install` or
`adapt` — adoptable, with nothing marking the risk:

- `perplexity-cli` recorded *"No licence file observed during review"* and
  was still `catalogued` and adoptable. No licence file means all rights
  reserved, not permissive.
- `appflowy`, `plausible-analytics`, `claude-mem` and `evomap-evolver` are
  AGPL or GPL, adoptable, with copyleft obligations noted only in prose.
- Nine more (`ponytail`, `last30days`, `frontend-design`, `21st-dev`,
  `gstack`, `task-observer`, and others) were `must-verify` — the licence
  was simply unknown — and adoptable.

## Two tiers, split by cause

A known-restrictive licence and an unverified licence are different
problems with different remedies, so they are not collapsed into one flag.

```text
approval-required      licence is KNOWN and restrictive
                       remedy: the user decides
                       copyleft, source-available, commercial, unlicensed
                       11 resources

verify-licence-first   licence is UNKNOWN
                       remedy: verification, not permission
                       must-verify, verify-current-release, mixed
                       12 resources

(absent)               verified permissive licence, freely adoptable
                       39 resources
```

Reference use is never gated. Reading a repository to learn from its
architecture is exactly what the catalogue is for, and that was the
explicit intent behind keeping these entries rather than removing them.
The gate applies to adoption: integrating, installing, vendoring, or
otherwise making the resource part of the project.

`use_modes` are deliberately left untouched. They describe *how* a
resource could be adopted, which stays useful information; the `adoption`
field governs *whether* that may happen without asking.

## Where it surfaces

`select_external()` carries `adoption` and `license` into every candidate,
and the context pack renders the gate inline:

```text
- `plausible-analytics` — Plausible Analytics — on-demand —
  https://github.com/plausible/analytics — **ASK BEFORE ADOPTING** (AGPL-3.0-or-later)
- `nanonets-graft` — Graft — on-demand — https://github.com/nanonets/graft
```

The second line is the point of the design. If everything is flagged, the
flag stops being read, so the 39 verified-permissive resources render
exactly as before.

## Regression cases

- `licence-01-copyleft-requires-approval` — AGPL resources route *and*
  carry `approval-required`. Fails without the gating data.
- `licence-02-unknown-licence-verify-first` — `last30days` carries
  `verify-licence-first` while verified-permissive siblings routed in the
  same turn carry no gate. Fails without the gating data.
- `licence-03-verified-permissive-ungated` — negative control asserting a
  verified MIT resource acquires no gate. Passes either way today; it
  exists so that a future over-broad rule that gates everything fails
  loudly instead of quietly turning the signal into noise.

`external_adoption` was added to `eval_harness.py` for this, mapping a
candidate id to its expected gate, with `null` asserting absence.

## Not done here

The kernel already instructs asking before licence-sensitive reuse, so no
kernel words were spent restating it — the data now makes that instruction
actionable, which was the missing half.

Enforcement is advisory: the gate is surfaced to the agent, not mechanically
blocked in `escapement.py install`. That script already has an
`approval_required` / `--approved` mechanism for component manifests, and
wiring registry adoption into it is a reasonable follow-up, but it is a
different change from making the risk visible.

The 18 distinct `license_status` values and 10 `status` values across 62
resources are more taxonomy than this catalogue needs, and several encode
the same idea in different words. Consolidating that vocabulary is a real
cleanup, deliberately not bundled into this change.
