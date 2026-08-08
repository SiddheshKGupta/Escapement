# Overlap-group tag drift

Every `catalog/capability-registry.json` resource carries its own
`overlap_group` string. `catalog/overlap-groups.json` separately defines
formal groups with a `members` list and a `relation` (`SUBSTITUTE`,
`COMPLEMENTARY`, `SEQUENTIAL`, `BASELINE_PLUS_INTENSIFIER`). These are two
different systems that happen to usually agree -- and didn't, for 20 of 67
resources.

## How this was found

Building the fallback-chain mechanism (`select_external()` demoting a
displaced `SUBSTITUTE`-group member to a recorded fallback instead of
dropping it) required choosing which of the two systems was authoritative
for dedup. `graphify` is tagged `code-knowledge` but is actually governed
by `memory-and-knowledge` -- using the tag would have missed that
resource's real group membership entirely. The fallback-chain code was
built keying off `overlap-groups.json`'s `members` list, correctly, but
that meant the per-resource `overlap_group` field was left silently wrong
for every resource where it disagreed. A full audit run against
`overlap-groups.json`'s membership lists found 20, not just the one that
had already been noticed.

## Root cause: a rename, not 20 independent decisions

Every mismatch traces to the same handful of formal-group renames that
were never propagated back to the resources' own tags:

```text
session-memory         -> memory-and-knowledge
harness-methodology    -> delivery-methodology
design-director         -> design-authority
browser-automation      -> browser-verification
engineering-minimalism  -> engineering-behaviour
code-knowledge           -> memory-and-knowledge
component-source (typo) -> component-sources
```

This mattered for how the fix was applied. Doing this by matching each
resource's *tag text* against the old group names would have been wrong --
an early draft of the fix did exactly that and incorrectly retagged four
resources (`walkinglabs-learn-harness-engineering`,
`walkinglabs-harness-creator`, `gstack`, `everything-claude-code`) that
share the old vocabulary (`harness-methodology`) but were never actual
members of `delivery-methodology`. Retagging them would have falsely
claimed formal group membership and put them in scope for SUBSTITUTE
dedup against resources they have no real relationship to. Caught before
being applied by checking `delivery-methodology`'s real member list
(`escapement-core, superpowers, github-spec-kit, gsd-core, ecc,
prime-intellect-prime-agent`) and confirming those four aren't on it.

The corrected fix retags a resource only when it is an actual, listed
member of exactly one formal group whose id differs from its current tag
-- membership-verified, not text-pattern-matched. 20 resources qualified,
matching the original audit exactly.

Two of the 20 -- `nanonets-graft` and `supermemory` -- were added in the
same session that built the fallback-chain mechanism, by copying an
already-stale resource (`graphify`, `claude-mem`) as a template. The
staleness was actively propagating into new entries, not just sitting
still in old ones.

## The one genuine two-group case

`open-design` belongs to two formal groups for two different reasons:
`design-authority` (`SEQUENTIAL` -- governs which phase of the design
pipeline it activates in) and `component-sources` (`SUBSTITUTE` -- governs
whether it competes with `shadcn-ui`/`21st-dev` for the same purpose).
Its stale tag (`design-director`) matched neither. A single string field
can't represent membership in two groups at once, so the fix picks
`component-sources`: `SUBSTITUTE` is the relation that actually changes
router behaviour (dedup), while `SEQUENTIAL` only affects phase-ordering
display. `emil-kowalski-skill` has the same two-group shape (`design-
authority` plus `motion`, `COMPLEMENTARY`) but its existing tag (`motion`)
already matched one of its two memberships, so it needed no change.

## What was not changed

Membership already governed dedup behaviour correctly, via
`fix/external-candidate-overlap-dedup` and the fallback-chain work --
this fix corrects the *display/audit* field, not routing logic. No eval
case changes; the corpus doesn't assert on `overlap_group` tag values.

## Regression coverage

`overlap_group_tag_check()` in `escapement.py`, wired into `doctor`,
computes each resource's actual formal-group membership from
`overlap-groups.json` and fails if the resource's own tag disagrees.
Three tests: an unmodified copy reports no drift; a deliberately stale
tag is detected and names both the wrong tag and the correct membership;
a resource with no formal membership at all is correctly *not* flagged,
since an unaffiliated tag has nothing to be inconsistent with.

Runs unconditionally (unlike the manifest.json counts check, which is
gated to the source repository) because `catalog/` is a managed prefix
copied into every installed consumer project -- catalogue integrity
matters wherever the catalogue is installed, not just here.
