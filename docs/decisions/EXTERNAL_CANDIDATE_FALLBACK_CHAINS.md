# External candidate fallback chains

When two external resources compete for the same SUBSTITUTE overlap group,
the displaced one is demoted to a fallback on the winner, not dropped.

## Why

`feat/registry-graft-observability` (later `fix/external-candidate-overlap-dedup`)
made `select_external()` collapse SUBSTITUTE groups to a single winner, the
same way `select_skills()` already did. That fixed the immediate bug -- two
competing memory tools no longer surface at once -- but copying the skills
behaviour exactly would have copied its limitation too: the loser simply
disappears.

That is a bigger problem for external resources than for native skills.
Native skills are part of the repository; if one is unavailable that is a
bug. External resources are, by definition, not installed until someone
adopts them -- "choose one code-knowledge system" with no recorded second
choice means that if the winner cannot be installed, is blocked by its
licence gate, or simply does not work for the project, there is nothing to
fall back to. The agent would have to re-derive the alternative from
scratch, or the user would have to know the catalogue well enough to look
for one.

## What changed

`select_external()` now attaches a `fallbacks` list to the winning
candidate:

```json
{
  "id": "egonex-understand-anything",
  "fallbacks": [
    {"id": "helixdb", "name": "HelixDB", "reason": "overlap:memory-and-knowledge"}
  ]
}
```

Rendered in the context pack as:

```text
- `egonex-understand-anything` — Understand Anything — on-demand-read-only-analysis — ...
  - fallback if unavailable: `helixdb` — HelixDB
```

`select_skills()` got the equivalent treatment for consistency, with one
caveat recorded in the code rather than hidden: every one of the 35 native
skills currently declares a *unique* `overlap_group`, so the rejection
branch that would populate a skill's `fallbacks` is presently unreachable.
Left in rather than removed, because it costs nothing to keep and stops
being dead code the moment two skills are ever placed in the same group --
which is a real possibility now that the registry has grown past 60
external resources plus 35 skills sharing groups by convention rather than
by enforced uniqueness.

Capability strengths were checked and found to have **no overlap groups at
all** (58 of 58 untagged) -- there is currently no collision to resolve
there, so nothing was added.

## Regression case

`overlap-external-03-displaced-member-becomes-fallback` asserts the full
shape: the winner is selected, both the loser and any third competing
resource stay out of the primary list, and the loser appears by id inside
the winner's `fallbacks`.

## Batch of five new registry resources

Added together with this change, each checked for licence and
over-triggering before being catalogued:

| id | licence | gate | notes |
|---|---|---|---|
| `supermemory` | MIT | none | joins `memory-and-knowledge` (now 8 members) |
| `sanyuan-skills` | MIT | none | joins `code-review`; last published 2026-05-11, confirm still maintained before relying on it |
| `mattpocock-skills` | MIT | none | the suite, as a source to read/adapt from; `mattpocock-grilling` remains the separate entry for the one skill already catalogued out of it |
| `floci` | MIT | none | sole member of a new `local-runtime-emulation` group, which has no declared `relation` yet -- same open item as `harness-methodology` |
| `awesome-claude-skills` | none found (GitHub licence endpoint returns 404) | **approval-required** | 72k stars did not make it licensed; catalogued as `reference-only`/`discovery-only` rather than excluded, per the two-tier gating policy this builds on |

Three regression cases cover the batch: the unlicensed entry routes with
its gate, a permissive addition routes with none, and none of the five
fire on an ordinary unrelated bug fix.

## Not done here

`floci`'s `local-runtime-emulation` group and `harness-methodology`
(`github-spec-kit` / `gsd-core`, noted in the overlap-dedup fix) both lack
a declared `relation`. Assigning one is a design decision about how those
resources should compete or complement each other, not a mechanical
consequence of adding a fifth resource -- left as an open item rather than
guessed at here.
