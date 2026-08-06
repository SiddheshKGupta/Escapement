# Capability Strength Map

Escapement separates a **native procedure** from a **specialist strength**.

```text
Native skill
→ reliable built-in fallback

Capability strength
→ a narrow behaviour from a skill, methodology, plugin, tool or reference
```

This prevents a 30-skill plugin from becoming one vague catalogue entry and
allows Escapement to use only the subskill that is strongest for the current
phase.

## Counts

```text
Native skills:          34
Capability strengths:   58
Capability families:    10
Strategy adapters:      10
```

## Routing rule

```text
Current phase
→ Required outcome
→ Native fallback
→ Specialist strength
→ Overlap resolution
→ Installation/readiness state
→ Evidence
```

The active phase normally receives no more than eight specialist strengths,
and external parents remain candidates until approved.

## `agent-blueprint-discovery`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `500-ai-agents:blueprint-discovery` | `500-ai-agents-projects` | RESEARCH, BRAINSTORM, PLAN | `discovery-only` | Discover linked agent implementations and industry use cases for deeper validation. |
## `agent-orchestration`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `superpowers:dispatching-parallel-agents` | `superpowers` | IMPLEMENT | `conditional` | Parallelise independent tasks with explicit contracts. |
| `superpowers:subagent-driven-development` | `superpowers` | IMPLEMENT | `conditional` | Use fresh sequential contexts with specification and quality review. |
## `browser-automation`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `stagehand:self-healing` | `stagehand` | IMPLEMENT, VERIFY | `production-browser-automation` | Hybrid natural-language and code browser automation with reusable cached actions. |
## `browser-verification`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `agent-browser:agent-snapshots` | `agent-browser` | VERIFY | `conditional` | Agent-readable browser snapshots and concise CLI interaction. |
| `cypress:project-tests` | `cypress` | IMPLEMENT, VERIFY | `project-existing` | Use when Cypress is already the project's browser test framework. |
| `playwright-mcp:exploratory` | `playwright-mcp` | VERIFY | `conditional-high-context` | Persistent accessibility-tree browser interaction for exploratory agent loops. |
| `playwright:project-tests` | `playwright` | IMPLEMENT, VERIFY | `project-existing-or-approved` | Deterministic cross-browser end-to-end testing. |
| `puppeteer-mcp:legacy` | `puppeteer-mcp` | VERIFY | `discouraged-legacy` | Legacy MCP browser automation only when already required. |
## `code-knowledge`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `graphify:code-knowledge-graph` | `graphify` | ORIENT, PLAN | `large-complex-repository` | Map codebase structures and dependencies when ordinary file inspection is insufficient. |
## `code-review`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `superpowers:requesting-code-review` | `superpowers` | VERIFY | `conditional` | Request an independent specification and quality review. |
## `component-selection`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `emil:pick-ui-library` | `emil-kowalski-skill` | SPECIFY, PLAN | `conditional` | Choose maintained UI libraries rather than hand-rolling mature components. |
## `delivery-methodology`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `superpowers:brainstorming` | `superpowers` | BRAINSTORM | `preferred-when-installed` | Explore design through structured questions and incremental approval. |
| `superpowers:writing-plans` | `superpowers` | PLAN | `preferred-when-installed` | Create detailed implementation plans with exact files and verification. |
## `delivery-quality`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `taste:full-output-enforcement` | `taste-skill` | IMPLEMENT | `conditional` | Prevent half-finished or placeholder frontend output. |
## `design-art-direction`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `taste:design-taste-frontend` | `taste-skill` | BRAINSTORM, IMPLEMENT | `choose-one-art-director` | Infer design language and tune variance, motion and density for greenfield interfaces. |
| `taste:gpt-taste` | `taste-skill` | BRAINSTORM, IMPLEMENT | `choose-one-art-director` | Stricter Codex/GPT anti-slop frontend direction. |
| `taste:high-end-visual-design` | `taste-skill` | BRAINSTORM | `explicit-direction` | Calm premium visual direction with softer contrast and whitespace. |
| `taste:industrial-brutalist-ui` | `taste-skill` | BRAINSTORM | `explicit-direction` | Experimental mechanical visual language. |
| `taste:minimalist-ui` | `taste-skill` | BRAINSTORM | `explicit-direction` | Restrained editorial/product design with crisp structure. |
## `design-authority`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `design-intelligence:constitution` | `design-intelligence-constitution` | RESEARCH, BRAINSTORM, SPECIFY, IMPLEMENT, VERIFY, POLISH | `mandatory-for-design` | Governing design authority for product direction, hierarchy, archetypes, tokens, components, states, accessibility and anti-generic-AI rules. |
## `design-image-pipeline`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `taste:image-to-code` | `taste-skill` | BRAINSTORM, IMPLEMENT | `conditional` | Generate or analyse visual references before implementation. |
## `design-polish`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `impeccable:polish` | `impeccable` | POLISH | `preferred-when-installed` | Final visual and interaction refinement before release. |
## `design-redesign`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `taste:redesign-existing-projects` | `taste-skill` | RESEARCH, IMPLEMENT | `conditional` | Audit and surgically upgrade an existing interface without rewriting functionality. |
## `design-reference`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `emil:apple-design` | `emil-kowalski-skill` | RESEARCH, BRAINSTORM | `reference-only` | Apply Apple interface and fluid-motion principles when the product direction warrants them. |
## `design-research`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `ui-ux-pro-max:chart-and-data-viz` | `ui-ux-pro-max` | RESEARCH, SPECIFY | `dashboard-or-data-viz` | Recommend chart types and data-visualisation patterns appropriate to the product and decision. |
| `ui-ux-pro-max:design-system-generator` | `ui-ux-pro-max` | RESEARCH, BRAINSTORM, SPECIFY | `conditional` | Generate product-type-aware design-system recommendations from a searchable design corpus. |
| `ui-ux-pro-max:style-search` | `ui-ux-pro-max` | RESEARCH | `conditional` | Search styles, palettes, fonts, UX guidance, charts and stack-specific rules. |
## `design-verification`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `impeccable:audit` | `impeccable` | VERIFY | `preferred-when-installed` | Detect design anti-patterns deterministically and through critique. |
| `impeccable:critique` | `impeccable` | VERIFY | `conditional` | Review UX and visual decisions against a high craft bar. |
| `impeccable:harden` | `impeccable` | VERIFY | `conditional` | Add edge cases, error handling, text overflow, i18n and resilience. |
## `design-workspace`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `open-design:workspace` | `open-design` | RESEARCH, BRAINSTORM, ARTIFACT | `explicit-workspace-decision` | Local-first design workspace, prototypes, assets, migrations and export workflows. |
## `engineering-behaviour`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `karpathy:goal-driven-execution` | `karpathy-guidelines` | PLAN, IMPLEMENT, VERIFY | `baseline` | Convert vague tasks into verifiable goals and feedback loops. |
| `karpathy:simplicity-first` | `karpathy-guidelines` | PLAN, IMPLEMENT, VERIFY | `baseline` | Prevent speculative abstractions and unnecessary flexibility. |
| `karpathy:surgical-changes` | `karpathy-guidelines` | IMPLEMENT, VERIFY | `baseline` | Keep diffs directly traceable to the approved task. |
| `karpathy:think-before-coding` | `karpathy-guidelines` | DISCOVER, PLAN, IMPLEMENT | `baseline` | Surface assumptions, ambiguity and trade-offs before changing code. |
## `engineering-execution`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `superpowers:executing-plans` | `superpowers` | IMPLEMENT | `conditional` | Execute an approved plan with human checkpoints. |
| `superpowers:test-driven-development` | `superpowers` | IMPLEMENT | `preferred-when-applicable` | Write failing tests first and implement to a precise goal. |
## `engineering-minimalism`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `ponytail:full` | `ponytail` | IMPLEMENT | `conditional` | Strong standard-library-first and minimum-code pressure. |
| `ponytail:lite` | `ponytail` | PLAN, IMPLEMENT | `conditional` | Light YAGNI and native-platform preference. |
| `ponytail:ultra` | `ponytail` | IMPLEMENT | `explicit-only` | Extreme simplification when code bloat is the primary defect. |
## `frontend-implementation`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `frontend-design:implementation` | `frontend-design` | IMPLEMENT | `conditional` | Implement distinctive production-grade interfaces from an approved design specification. |
## `frontend-performance`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `impeccable:optimize` | `impeccable` | VERIFY | `conditional` | Improve frontend performance without changing approved design intent. |
## `memory`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `claude-mem:session-memory` | `claude-mem` | ALL | `explicit-memory-decision` | Persistent semantic session memory for long-running projects. |
## `motion-design`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `emil:animation-vocabulary` | `emil-kowalski-skill` | SPECIFY | `motion-present` | Describe motion precisely enough for reliable implementation. |
| `emil:emil-design-eng` | `emil-kowalski-skill` | IMPLEMENT, POLISH | `motion-justified` | Purposeful motion, component craft, perceived speed and design engineering details. |
| `emil:find-animation-opportunities` | `emil-kowalski-skill` | BRAINSTORM, POLISH | `conditional` | Identify where motion adds comprehension and where it should be deleted. |
## `motion-review`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `emil:improve-animations` | `emil-kowalski-skill` | VERIFY, POLISH | `motion-present` | Audit animation code and produce prioritised fix plans. |
| `emil:review-animations` | `emil-kowalski-skill` | VERIFY | `motion-present` | Strict animation review with explicit block/approve criteria. |
## `platform-research`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `agent-reach:platform-research` | `agent-reach` | RESEARCH | `approved-network` | Reach platform-specific sources, social evidence and transcripts. |
## `release`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `superpowers:finishing-a-development-branch` | `superpowers` | RELEASE | `conditional` | Finish branch, checks and integration cleanly. |
## `responsive-design`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `impeccable:adapt` | `impeccable` | VERIFY | `conditional` | Adapt interface behaviour across device classes. |
## `skill-learning`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `task-observer:observe` | `task-observer` | ALL | `opt-in-observer` | Log repeated capability gaps and propose candidate skills. |
## `technical-research`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `context7:library-docs` | `context7` | RESEARCH, IMPLEMENT | `technical-docs-needed` | Fetch current library and framework documentation. |
## `trend-research`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `last30days:recent-discourse` | `last30days` | RESEARCH | `current-trends-needed` | Find recent practitioner and community signals. |
## `ux-writing`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `impeccable:clarify` | `impeccable` | VERIFY, POLISH | `conditional` | Improve unclear product microcopy. |
## `verification`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `superpowers:verification-before-completion` | `superpowers` | VERIFY, RELEASE | `preferred-when-installed` | Require actual verification evidence before completion claims. |
## `writing-quality`

| Capability strength | Parent | Phases | Activation | Core strength |
|---|---|---|---|---|
| `stop-slop:final-lint` | `stop-slop` | VERIFY, POLISH | `conditional` | Remove generic AI phrasing and repetitive prose after substantive content is correct. |


# Source of Truth

Machine-readable registry:

```text
catalog/skill-strengths.json
```

Phase orchestration:

```text
catalog/phase-capabilities.json
catalog/strategy-adapters.json
```
