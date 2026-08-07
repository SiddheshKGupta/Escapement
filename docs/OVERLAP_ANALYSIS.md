# Overlap Analysis

Escapement preserves capabilities without pretending that every capability
should be active simultaneously.

## Relation types

| Relation | Meaning |
|---|---|
| `BASELINE_PLUS_INTENSIFIER` | A universal baseline remains active; a narrower capability increases pressure in one phase |
| `SUBSTITUTE` | Select one capability for the same job |
| `COMPLEMENTARY` | Capabilities solve distinct parts and may pair |
| `SEQUENTIAL` | Capabilities overlap broadly but are strongest in different phases |
| `REFERENCE_ONLY` | Use for evidence or inspiration, not execution authority |
| `META_OBSERVER` | Observe and propose; do not own execution |

## Core decision

Overlap is not resolved by:

```text
delete everything
or
load everything
```

It is resolved through:

```text
authority
+ phase
+ outcome
+ evidence type
+ existing project stack
+ token cost
+ security
```

## `engineering-behaviour`

- Relation: `BASELINE_PLUS_INTENSIFIER`
- Canonical capability: `karpathy-guidelines`
- Rule: Karpathy Guidelines remain the baseline for thinking, surgical changes and verifiable goals. Ponytail may intensify implementation minimalism when overengineering risk is high.

### Members

- `karpathy-guidelines`
- `ponytail`

### Phase use

- `ALL_ENGINEERING_PHASES`: `karpathy-guidelines`
- `IMPLEMENT`: `ponytail`
## `design-authority`

- Relation: `SEQUENTIAL`
- Canonical capability: `design-intelligence-constitution`
- Rule: The constitution is supreme. Use UI/UX Pro Max for research/specification, one art director for brainstorming, frontend-design for implementation, Impeccable for audit/polish and Emil for motion.

### Members

- `design-intelligence-constitution`
- `ui-ux-pro-max`
- `taste-skill`
- `impeccable`
- `emil-kowalski-skill`
- `open-design`
- `frontend-design`

### Allowed pairings

- `design-intelligence-constitution` + `ui-ux-pro-max`
- `design-intelligence-constitution` + `taste-skill`
- `design-intelligence-constitution` + `impeccable`
- `design-intelligence-constitution` + `emil-kowalski-skill`
- `frontend-design` + `emil-kowalski-skill`
- `impeccable` + `emil-review-animations`

### Forbidden in the same phase

- `taste-skill` + `open-design` + `impeccable`
- `taste-skill` + `ui-ux-pro-max` + `open-design`
## `writing-quality`

- Relation: `BASELINE_PLUS_INTENSIFIER`
- Canonical capability: `writing-quality`
- Rule: Native writing-quality owns content clarity and business usefulness. Stop Slop is a final anti-AI-pattern lint pass.

### Members

- `writing-quality`
- `stop-slop`
## `skill-learning`

- Relation: `META_OBSERVER`
- Canonical capability: `skill-governance`
- Rule: Task Observer and Evolver may log repeated gaps or propose an improvement from runtime history. Skill governance owns evaluation, promotion, overlap and retirement. Neither may rewrite skills, AGENTS.md or project state automatically.

### Members

- `skill-governance`
- `task-observer`
- `evomap-evolver`
## `delivery-methodology`

- Relation: `SEQUENTIAL`
- Canonical capability: `escapement-core`
- Rule: Escapement owns runtime, state and evidence. Use component-level adapters from external methodologies at their strongest phases; do not install competing complete lifecycle hooks together. Prime Agent is a separate long-running runtime, not a methodology adapter: do not let it and Escapement co-own lifecycle phase, task state, memory, permissions or closure -- a future adapter must define the authority boundary.

### Members

- `escapement-core`
- `superpowers`
- `github-spec-kit`
- `gsd-core`
- `ecc`
- `prime-intellect-prime-agent`
## `memory-and-knowledge`

- Relation: `SUBSTITUTE`
- Canonical capability: `escapement-file-state`
- Rule: File state is default. Claude Mem, AppFlowy or HelixDB may become the primary external memory substrate only after a demonstrated need. Graphify or Understand Anything may complement file state for code relationships -- choose one code-knowledge/graph system per repository and prefer ordinary repository inspection for small projects.

### Members

- `escapement-file-state`
- `claude-mem`
- `appflowy`
- `helixdb`
- `graphify`
- `egonex-understand-anything`
## `decision-interview`

- Relation: `BASELINE_PLUS_INTENSIFIER`
- Canonical capability: `decision-coach`
- Rule: decision-coach remains the default for every MATERIAL or PROGRAM request. Grilling activates only after an explicit request to stress-test, grill, or challenge a plan or design, and still obeys decision-coach's rules: inspect the repository first, ask no more than five material questions per round, give a recommended default and consequence, and wait for confirmation before implementing.

### Members

- `decision-coach`
- `mattpocock-grilling`
## `prompt-shaping`

- Relation: `SEQUENTIAL`
- Canonical capability: `product-specification`
- Rule: Escapement owns discovery, decisions, specification and acceptance criteria. Prompt Master activates only after a specification is approved, to format or adapt the approved result for a named target tool -- it does not replace normal discovery for an ordinary build/design/fix request.

### Members

- `product-specification`
- `decision-coach`
- `nidhinjs-prompt-master`
## `research-freshness`

- Relation: `COMPLEMENTARY`
- Canonical capability: `primary-web`
- Rule: Choose by evidence type: authoritative public facts, technical documentation, grounded research, recent discourse or platform-specific reach. Maximum two supporting channels per research question.

### Members

- `primary-web`
- `context7`
- `perplexity`
- `last30days`
- `agent-reach`
## `browser-verification`

- Relation: `SUBSTITUTE`
- Canonical capability: `project-existing-browser-framework`
- Rule: Use the project's existing browser test framework first. Select one primary driver per run; do not duplicate browser automation stacks.

### Members

- `playwright`
- `agent-browser`
- `stagehand`
- `puppeteer-mcp`
- `cypress`
## `code-review`

- Relation: `SUBSTITUTE`
- Canonical capability: `engineering-review`
- Rule: Choose one primary review workflow. Add a second independent reviewer only for material/high-risk changes with a stated reason.

### Members

- `engineering-review`
- `superpowers-requesting-code-review`
- `claude-code-review`
- `gstack-review`
## `component-sources`

- Relation: `SUBSTITUTE`
- Canonical capability: `project-component-system`
- Rule: Use the existing project component system first. External component sources require stack, licence, accessibility and visual-consistency review.

### Members

- `project-component-system`
- `shadcn-ui`
- `21st-dev`
- `open-design`


## External candidates without a dedicated group

Agency Agents and Cloudflare OS are catalogued as `reference-only` with a
descriptive `overlap_group` tag on their registry entry, but neither has a
dedicated group here -- matching the existing precedent for
`500-ai-agents-projects`, which also has a descriptive tag with no matrix
group. A matrix group exists to arbitrate a genuine conflict between
capabilities competing for the same job; a reference-only catalogue that
nothing else in Escapement currently competes with does not need one.

## Recommended use, seven candidates reviewed 2026-08-07

| Candidate | Recommended Escapement use |
|---|---|
| Understand Anything | On-demand code-knowledge integration candidate |
| Grilling / Grill Me | Explicit decision-interview mode, implemented in `skills/decision-coach/SKILL.md` |
| Prompt Master | Post-specification prompt-export adapter |
| Agency Agents | Specialist-role discovery catalogue |
| Prime Agent | Separate runtime or future execution adapter |
| Evolver | Review-only meta-observer |
| Cloudflare OS | Security and workspace architecture reference |

See `docs/decisions/EXTERNAL_CANDIDATES_2026_08.md` for the full review.

# Enforcement

Machine-readable detailed matrix:

```text
catalog/overlap-matrix.json
```

Compact runtime groups:

```text
catalog/overlap-groups.json
```

Tests:

```text
tests/v6_3/test_overlap.py
tests/v6_3/test_design_authority.py
tests/v6_3/test_browser_and_research.py
```
