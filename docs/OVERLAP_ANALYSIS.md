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
- Rule: Task Observer may log repeated gaps. Skill governance owns evaluation, promotion, overlap and retirement. Task Observer must not rewrite skills automatically.

### Members

- `skill-governance`
- `task-observer`
## `delivery-methodology`

- Relation: `SEQUENTIAL`
- Canonical capability: `escapement-core`
- Rule: Escapement owns runtime, state and evidence. Use component-level adapters from external methodologies at their strongest phases; do not install competing complete lifecycle hooks together.

### Members

- `escapement-core`
- `superpowers`
- `github-spec-kit`
- `gsd-core`
- `ecc`
## `memory-and-knowledge`

- Relation: `SUBSTITUTE`
- Canonical capability: `escapement-file-state`
- Rule: File state is default. Claude Mem, AppFlowy or HelixDB may become the primary external memory substrate only after a demonstrated need. Graphify may complement file state for code relationships.

### Members

- `escapement-file-state`
- `claude-mem`
- `appflowy`
- `helixdb`
- `graphify`
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
