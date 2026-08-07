# External Candidates Review -- 2026-08

Seven externally-referenced repositories were reviewed for addition to
Escapement's governed capability registry: Prime Agent, Understand Anything,
Evolver, Agency Agents, Prompt Master, Matt Pocock's Grilling/Grill Me, and
Cloudflare OS. This records why each was classified the way it was, why
most were not directly installed, the authority and overlap decisions made,
licence considerations, and future adapter opportunities.

Licences were verified via each repository's own README/LICENSE/package.json
metadata as surfaced 2026-08-07; a maintainer should re-verify the LICENSE
file text directly before any actual code is copied, not just this note.

## Classification

| Candidate | Kind | Status | Why |
|---|---|---|---|
| Understand Anything | code-knowledge-plugin | `optional` | Strongest immediate candidate -- MIT, on-demand, read-only knowledge-graph generation, already cross-tool aware (works with Claude Code, Codex, Cursor, Copilot, Gemini CLI). |
| Grilling / Grill Me | decision-interview-skill | `optional` | Real, tested addition -- adapted (not copied) into `skills/decision-coach/SKILL.md` as an explicit intensifier. |
| Prompt Master | prompt-export-skill | `optional-reference` | Genuinely useful, but strictly sequenced after Escapement's own specification stage; registry entry only. |
| Agency Agents | agent-role-catalogue | `reference-only` | Large persona library; useful as a discovery catalogue, wrong shape to install wholesale. |
| Prime Agent | external-agent-runtime | `conditional` | A second complete runtime; registry entry plus adapter-boundary notes, no integration. |
| Evolver | agent-evolution-meta-observer | `conditional` | GPL-3.0 today with an announced move to source-available; review-mode-only, no automatic mutation. |
| Cloudflare OS | agent-workspace-and-security-architecture | `reference-only` | Genuinely instructive architecture (Gatekeeper capability mediation), but its runtime depends on Cloudflare Workers -- not something Escapement's file-based core should absorb. |

## Why most were not directly installed

Escapement's own doctrine (`AGENTS.md`, Approval Gates and Precedence
sections) requires that new dependencies, external skills, and plugins be
approved individually and not silently override the kernel, lifecycle,
approval gates, evidence model, or closure rules. Five of the seven
candidates are complete systems that own their own state, execution, or
authority model (Prime Agent's runtime, Evolver's self-evolution loop,
Agency Agents' full persona roster, Cloudflare OS's workspace platform,
Prompt Master's export pipeline). Installing any of them wholesale would
create a second authority for something Escapement already owns --
exactly the failure mode `docs/OVERLAP_ANALYSIS.md` exists to prevent.
Cataloguing them as governed candidates preserves the option to use them
narrowly, later, with an explicit approval and a defined authority
boundary, without pretending review is the same thing as installation.

## Authority and overlap decisions

- **`decision-interview`** (new group): `decision-coach` stays canonical;
  `mattpocock-grilling` is a `BASELINE_PLUS_INTENSIFIER`, matching the
  existing `karpathy-guidelines`/`ponytail` pattern for an
  externally-inspired but natively-owned behaviour. It activates only on
  explicit stress-test language (verified by
  `tests/v6_3/test_external_candidates.py::RoutingTest`), never implicitly.
- **`prompt-shaping`** (new group): `product-specification` stays
  canonical; `nidhinjs-prompt-master` is `SEQUENTIAL` -- it can only run
  after a specification is approved, never in place of discovery.
- **`skill-learning`**: `evomap-evolver` joins `task-observer` as a second
  `META_OBSERVER`. Both may propose; only `skill-governance` may promote,
  retire, or apply a change. Evolver's own "propose, don't mutate" design
  (per its README) matches this relation cleanly.
- **`memory-and-knowledge`**: `egonex-understand-anything` joins `graphify`
  as a `SUBSTITUTE` for code-relationship mapping. This mirrors graphify's
  existing precedent exactly (its registry `overlap_group` field says
  `code-knowledge`, but the matrix group it actually lives in is
  `memory-and-knowledge` -- a pre-existing, tolerated convention this
  review followed rather than diverged from).
- **`delivery-methodology`**: `prime-intellect-prime-agent` joins
  `escapement-core`/`superpowers`/`github-spec-kit`/`gsd-core`/`ecc`. It is
  the most complete external runtime of the group -- worth a real matrix
  entry rather than only a descriptive tag, because it is exactly the kind
  of system that could plausibly try to own lifecycle phase and closure if
  installed carelessly.
- **Agency Agents and Cloudflare OS**: deliberately given a descriptive
  `overlap_group` tag with **no** dedicated matrix group, matching the
  existing precedent for `500-ai-agents-projects`. A matrix group exists to
  arbitrate a genuine conflict; nothing in Escapement currently competes
  with either of these for the same job.

## Grilling: why it got deeper treatment than the rest

Grilling is the only candidate of the seven that was actually implemented
rather than only catalogued, because it is the only one that is small,
MIT-licensed, has no runtime/network/credential footprint, and extends a
skill Escapement already owns (`decision-coach`) rather than competing with
one. The design-tree/question-frontier method was rewritten in original
wording as the "Grilling Intensifier" section of
`skills/decision-coach/SKILL.md`, attributed with the source URL, and
bounded by decision-coach's existing rules (repository-first inspection,
five-question cap, recommended default and consequence, wait for
confirmation before implementing). It was not copied verbatim, and it did
not become a new `skills/` folder -- Escapement's existing convention for
an externally-inspired but natively-owned behaviour is a doctrine/overlap
addition (see `karpathy-guidelines`/`ponytail`), not a new skill directory.
See `THIRD_PARTY_NOTICES.md` for the full adaptation record.

Understand Anything received the second-deepest treatment (a dedicated
overlap-group membership and a full routing test suite) because it is the
only other candidate the task explicitly named as the strongest immediate
integration candidate, and because its use case -- codebase understanding
-- is one Escapement already has a real gap in (no native skill currently
produces an architecture map or dependency graph beyond ordinary file
inspection).

## Licence considerations

| Candidate | Licence | Note |
|---|---|---|
| Prime Agent | MIT | Verified from repository and coverage. |
| Understand Anything | MIT | Verified from `package.json`. |
| Evolver | GPL-3.0-or-later (current release) | Publisher has announced future releases move to source-available; not retroactive. Do not copy GPL code into Escapement's source-available core without a deliberate legal/architectural decision. |
| Agency Agents | MIT | Verified from repository. |
| Prompt Master | MIT | Verified via community catalogue listing. |
| Matt Pocock Grilling / Grill Me | MIT | Verified from `mattpocock/skills` repository LICENSE. |
| Cloudflare OS | Apache-2.0 | Verified; runtime depends on Cloudflare Workers, so "open source" here does not mean "portable." |

## Future adapter opportunities

- **Prime Agent adapter**: Escapement would own specification, governance,
  approvals, evidence requirements, and closure; Prime Agent would act as
  the approved execution host for a single bounded task, with an explicit
  input contract, output contract, working directory, allowed commands,
  time/token limits, evidence return format, failure/cancellation
  behaviour, and an explicit statement of which system owns memory and
  which owns final closure. Not built in this review -- no demonstrated
  need yet for a second runtime.
- **Understand Anything adapter**: an optional `escapement.py` command
  could shell out to a locally-installed Understand Anything CLI during
  `ORIENT`/`DISCOVER` on large repositories, with the generated graph
  treated as supporting evidence, not a replacement for `PROJECT_STATE.yaml`.
  Not built in this review -- kept to a registry entry plus overlap
  membership, since no local installation exists to integrate against yet.
- **Evolver adapter**: a review-mode-only command that reads
  `scripts/harness_observability.py`'s own output and hands it to Evolver's
  proposal step, with every proposal routed back through
  `skill-governance` before anything changes. Not built in this review.

## What this PR does not do

It does not install all seven repositories as running dependencies, add a
second lifecycle owner, enable automatic self-evolution, introduce
Cloudflare Workers dependencies, bulk-install agent personas, or change
Escapement's core authority model.
