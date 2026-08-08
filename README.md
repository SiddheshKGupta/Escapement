<div align="center">

# Escapement

### A governed, low-token harness for context-aware AI-assisted delivery.

Escapement adds an executable delivery layer around coding agents: decision gates,
phase-scoped context, capability routing, durable project state, structured
verification, truthful closure, and measurement of the harness itself.

[![Version](https://img.shields.io/badge/version-6.3.0-53284F?style=flat-square)](VERSION)
[![CI](https://github.com/SiddheshKGupta/Escapement/actions/workflows/validate-standard.yml/badge.svg)](https://github.com/SiddheshKGupta/Escapement/actions/workflows/validate-standard.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.12%20%7C%203.13-3776AB?style=flat-square&logo=python&logoColor=white)](.github/workflows/validate-standard.yml)
[![Kernel](https://img.shields.io/badge/kernel-795%20%2F%201000-2F855A?style=flat-square)](AGENTS.md)
[![Native skills](https://img.shields.io/badge/native%20skills-35-2F855A?style=flat-square)](catalog/native-skills.json)
[![Unit tests](https://img.shields.io/badge/unit%20tests-165%20passing-2F855A?style=flat-square)](manifest.json)
[![Routing evals](https://img.shields.io/badge/routing%20evals-72%20%2F%2072-2F855A?style=flat-square)](evals/)
[![Case studies](https://img.shields.io/badge/case%20studies-4-2F855A?style=flat-square)](#evidence-from-real-use)
[![Licence](https://img.shields.io/badge/licence-source--available-6B7280?style=flat-square)](LICENSE.md)

**Escapement does not upgrade the model. It upgrades how the model works.**

[60-second overview](#escapement-in-60-seconds) ·
[Quick start](#quick-start) ·
[How it works](#how-it-works) ·
[Capabilities](#capability-orchestration) ·
[Evidence](#evidence-from-real-use) ·
[Validation](#current-validation) ·
[v2 roadmap](#v20-roadmap)

</div>

---

## Escapement in 60 seconds

A capable model can still make poor delivery decisions: assume instead of ask,
load too much context, forget prior decisions, skip a specialist capability,
declare work complete without evidence, or lose consistency across a long
multi-module build.

Escapement is a repository-native harness designed to reduce those failure modes.

It is **more than an instruction file**. The repository includes an executable
runtime, capability router, context budgets, lifecycle state, approval gates,
evidence records, observability, ablation testing, managed installation, and
host packaging.

### What changes when Escapement is active

| Agent behavior without a delivery harness | Escapement mechanism |
|---|---|
| One growing context accumulates across the task | Fresh, bounded context is composed for the active phase |
| Material choices are silently assumed | `MATERIAL` and `PROGRAM` work surfaces high-impact decisions and waits for the user |
| The same instructions are carried through every stage | Skills, doctrine, strengths, agents, and external candidates are routed by phase |
| A capability exists but the user never discovers it | Capability audit and catalogue search surface relevant native and optional capabilities |
| Chat history becomes project memory | Decisions, evidence, phase history, and the next action persist in the repository |
| "Looks done" becomes "done" | Closure is tied to executed checks and explicit `PASS`, `PARTIAL`, or failure semantics |
| Large builds drift across modules | A PROGRAM registry tracks dependencies, shared artifacts, and module state |
| External tools become ambient authority | External resources remain governed candidates until reviewed and approved |
| Harness rules grow without proof they help | Observability and ablation expose routing behavior and test selected components against the evaluation corpus |

### What is actually inside

```text
User request
    ↓
Task classification
    ↓
Decision + question gate
    ↓
Capability readiness
    ↓
Adaptive phase plan
    ↓
Bounded context composition
    ├── compact kernel
    ├── project + domain context
    ├── doctrine packs
    ├── native skills
    ├── specialist strengths
    └── approved external candidates
    ↓
Implementation
    ↓
Executed verification
    ↓
Truthful closure
    ↓
Durable handoff
```

Current inventory:

```text
Version:                   6.3.0
Repository files:          269
Kernel:                    795 / 1000 words
Profiles:                    2
Doctrine packs:             11
Native skills:              35
Capability strengths:       58
Agent patterns:             21
Governed external resources: 61
Strategy adapters:          10
Capability families:        10
Overlap groups:             14
Published case studies:      4
Unit tests:                 165
Routing evaluations:        72
```

Escapement deliberately uses **more capabilities across the lifecycle, not more
context inside one prompt**.

---

## Why “Escapement”?

A mechanical escapement converts stored energy into controlled, measurable movement.

Escapement applies the same principle to AI coding agents:

```text
Unbounded generation
        ↓
Specify → Route → Execute → Verify → Persist
        ↓
Controlled delivery
```

AI agents can generate code quickly. Reliable delivery also requires decisions
to be explicit, context to remain usable, specialist capabilities to appear at
the right time, sensitive actions to remain bounded, verification to be
executed, and the next session to inherit trustworthy state.

---

## What Escapement is

Escapement is a **repository-native operating layer for AI-assisted delivery**.

It provides:

- an always-loaded kernel with an enforced word budget;
- runtime classification into `INFO`, `MICRO`, `MATERIAL`, and `PROGRAM`;
- a ten-phase lifecycle with adaptive replanning;
- real-user question gates for material decisions;
- phase-specific capability routing;
- 35 native executable skill procedures;
- 58 specialist capability strengths;
- governed external capability discovery with overlap and licence controls;
- domain, design, reporting, engineering, data, governance, finance, legal,
  security, AI-agent, automation, and artifact-production procedures;
- durable project memory and multi-session handoff;
- multi-module PROGRAM dependency governance;
- structured, content-addressed check evidence;
- `PASS`, `PARTIAL`, and failure closure semantics;
- deterministic security and UI-quality gates;
- harness observability;
- harness ablation against a shared evaluation corpus;
- managed install, update, repair, backup, and drift detection;
- automatic runtime hook packaging for Claude Code and Codex;
- bootstrap guidance for other repository-aware hosts.

Escapement is **not**:

- a replacement for the underlying model;
- a guarantee of correct software;
- a giant prompt that loads every capability at once;
- an autonomous permission to deploy, modify production data, expose
  credentials, install dependencies, or run security tests;
- a claim that every catalogued external resource is installed;
- a substitute for law, regulation, policy, standards, or qualified domain
  experts;
- a claim that local evidence is equivalent to independently controlled CI;
- an MCP server today;
- the provider-agnostic execution control plane described in the v2 roadmap.

---

# Evidence from real use

Escapement has been repeatedly exercised through real repository builds,
adversarial scenarios, regression tests, and end-to-end delivery flows.

Four detailed case studies are published:

1. [Vanilla vs. Governed Implementation](reports/CASE_STUDY_vanilla_vs_governed.md)
2. [Full PROGRAM-Tier Claims Platform Build](reports/CASE_STUDY_claims_platform_program_build.md)
3. [Invoice Reconciliation PROGRAM Build](reports/CASE_STUDY_invoice_reconciliation_program_build.md)
4. [Four-Module CRM PROGRAM Build](reports/CASE_STUDY_crm_platform_multi_module_program.md)

Those builds did more than confirm happy paths. They surfaced problems that
became framework changes and regression tests, including:

- sequencing drift between PROGRAM modules;
- a declared business dependency missing from the module registry;
- a verified standalone module that failed when integrated into a broader
  compliance workflow;
- a stale development server that returned plausible but wrong runtime data;
- UI doctrine that existed but was skipped in practice, leading to a
  deterministic UI-quality gate;
- missing baseline field validation;
- a browser-only validation failure that unit tests did not expose;
- context-budget regressions caused by adding too much kernel or skill prose;
- host bootstrap behavior that could leave the runtime inactive even when an
  agent had read the instructions.

The operating pattern is:

```text
Real build
    ↓
Observed failure or gap
    ↓
Identify the smallest correct harness layer
    ↓
Implement the mechanism
    ↓
Add regression evidence
```

"Battle-tested" in this repository means repeatedly used and challenged against
real work. It does **not** mean a statistical benchmark or broad production
adoption.

Current real-use evidence is strongest on Claude Code. Codex has automatic
runtime-hook packaging in the repository, but equivalent cross-host conformance
and quota-aware execution validation remain future work.

---

## The harness measures itself

Escapement does not treat more doctrine as automatically better.

### Observability

Every formally closed turn can contribute to harness-health trends:

```bash
python scripts/escapement.py observability --root <target>
```

The report can surface:

- turn and closure-result distribution;
- task-tier distribution;
- phase-replan frequency and reasons;
- skills selected but never marked used;
- rejection causes such as overlap, phase limits, and context budget.

An empty observability report is **not** treated as proof of a healthy harness.
It may mean work happened without formal `close-turn` records.

### Ablation Harness v0

Escapement can also ask a harder question:

> Does this harness component change anything this corpus can measure?

```bash
python scripts/escapement.py ablate
python scripts/escapement.py ablate design-intelligence-constitution
python scripts/escapement.py ablate decision-coach
```

An ablation run:

1. copies the repository to a throwaway workspace;
2. removes one declared component from that copy only;
3. runs the same evaluation corpus as a control;
4. runs it again with the component removed;
5. reports factual differences.

Canonical source files are not modified.

One current example is clearly exercised by the routing corpus:
removing `design-intelligence:constitution` changed the routing result from
22/22 passing cases to 13/22.

The counter-example is equally important. A routing-only corpus cannot determine
whether `decision-coach` actually prevents bad human decisions during live
delivery. A null result is therefore reported as **not exercised by this
corpus**, not as evidence that the component is useless.

Escapement deliberately does not invent a composite "harness score" or
statistical significance from 22 routing cases.

The current ablation corpus measures routing behavior. It does not yet measure
live retries, tool activity, turn closure, or final task quality.

---

# Quick start

## 1. Clone

```bash
git clone https://github.com/SiddheshKGupta/Escapement.git
cd Escapement
```

## 2. Install into a project

```bash
python scripts/escapement.py init /path/to/your-project
```

Windows:

```powershell
py -3 scripts/escapement.py init C:\path\to\your-project
```

Escapement copies framework-managed files while creating project-owned state
that is not treated as disposable framework content.

## 3. Configure the project

Start with:

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
DOMAIN_CONTEXT.md
```

Example:

```yaml
project_name: My Product
profile: domain-expertise
phase: discovery
work_mode: FULL
implementation_authorized: false
approved_ticket: null
```

## 4. Verify the installation

From the installed project:

```bash
python scripts/escapement.py doctor --root .
```

## 5. See what Escapement can already do

```bash
python scripts/escapement.py catalog list --catalog skills
python scripts/escapement.py catalog list --catalog resources
python scripts/escapement.py catalog list --catalog patterns
python scripts/escapement.py catalog search "browser test"
```

The current catalogue exposes:

```text
35 native skills
21 agent patterns
61 governed external resources
```

A catalogue entry is **not** an installation. External capabilities retain
their own activation, approval, overlap, and licence boundaries.

For `MATERIAL` and `PROGRAM` work, `decision-coach` also surfaces relevant
not-yet-installed candidates during the question round and recommends whether
to use or skip them.

## 6. Start a governed turn

```bash
python scripts/agent_runtime.py manual-start \
  --prompt "Build a controlled claims workflow" \
  --json
```

Explain routing without starting a turn:

```bash
python scripts/escapement.py explain \
  "Build a controlled claims workflow"
```

Inspect capability readiness:

```bash
python scripts/escapement.py capability-audit \
  "Build a controlled claims workflow" \
  --markdown
```

---

# How it works

## Task tiers

| Tier | Intended use | Runtime expectation |
|---|---|---|
| `INFO` | Explanation, navigation, or status | No material runtime turn required |
| `MICRO` | Small bounded change | Compact context and at most one native skill per phase |
| `MATERIAL` | Feature or meaningful change | Decisions, phase routing, evidence, and durable closure |
| `PROGRAM` | Product, module, or transformation | Full lifecycle, broader orchestration, and multi-turn governance |

The tier changes the amount of ceremony and context. A typo should not be
treated like a platform build.

## Lifecycle

```text
ORIENT
→ DISCOVER
→ RESEARCH
→ BRAINSTORM
→ SPECIFY
→ PLAN
→ IMPLEMENT
→ VERIFY
→ POLISH
→ RELEASE
```

| Phase | Primary responsibility |
|---|---|
| `ORIENT` | Read the repository, current state, constraints, and active work |
| `DISCOVER` | Identify the real decision, inspect first, and resolve material unknowns |
| `RESEARCH` | Gather authoritative domain, regulatory, product, and technical evidence |
| `BRAINSTORM` | Compare materially different approaches |
| `SPECIFY` | Define behavior, controls, architecture, data, reporting, design, and acceptance criteria |
| `PLAN` | Create bounded tasks, dependencies, ownership, and verification |
| `IMPLEMENT` | Build through approved, phase-relevant capabilities |
| `VERIFY` | Test behavior, seams, security, accessibility, and evidence |
| `POLISH` | Improve usability, language, responsiveness, and motion where relevant |
| `RELEASE` | Apply readiness gates and issue a truthful verdict and handoff |

### Adaptive phase planning

The initial lifecycle is a starting plan, not a rigid ceremony.

After repository inspection, a turn can revise future phases:

```bash
python scripts/agent_runtime.py replan-phases \
  --add-phase VERIFY \
  --reason "Stored credentials require explicit security verification."
```

or:

```bash
python scripts/agent_runtime.py replan-phases \
  --remove-phase POLISH \
  --reason "Backend-only change with no user-facing surface."
```

A replan:

- can use only the catalogued lifecycle phases;
- cannot remove the current phase;
- cannot erase a phase already completed with evidence;
- requires a reason;
- is persisted in the turn history.

---

## Better decisions before better code

For `MATERIAL` and `PROGRAM` work, the runtime expects a decision brief that
contains:

```text
Actual decision
Known facts and assumptions
Maximum five material questions
Recommended default for each question
Consequence of choosing differently
Improved execution brief
Domain-research plan
Phase plan
Capability-readiness audit
```

When a user is present, the agent is expected to wait for real answers to
material questions rather than silently using defaults.

Defaults exist to reduce user effort and support genuinely unattended work.
They are not permission to self-answer an interactive decision.

An explicit request such as "grill me", "stress-test this plan", or "challenge
every assumption" activates a deeper decision-tree pass inside
`decision-coach`. It does not silently activate on an ordinary feature request.

---

# Bounded context engineering

Escapement's low-token design is not based only on having a short `AGENTS.md`.

The runtime separates:

```text
Always loaded
└── compact kernel

Project-relevant
├── project state
├── project context
└── domain context

Phase-relevant
├── doctrine packs
├── native skills
├── capability strengths
├── fresh-context agents
└── approved external candidates

Persisted afterward
├── decisions
├── phase history
├── artifacts
├── evidence
└── next action
```

Current enforced budgets:

```text
Always-loaded kernel:          <= 1,000 words
Current kernel:                   795 words
Automatic phase context:       <= 1,800 words
Invoked native-skill context:  <= 1,000 words
Doctrine packs:                <= 3 per phase
Native skills for MICRO:       <= 1 per phase
Native skills for MATERIAL:    <= 5 per phase
Native skills for PROGRAM:     <= 6 per phase
```

The budgets are active constraints, not decorative documentation.

Recent changes demonstrated this directly: adding capability-surfacing prose
initially pushed the kernel and `decision-coach` far enough to break unrelated
routing evaluations. The change was trimmed to fit instead of raising the
budgets.

---

# Capability orchestration

Escapement separates **what exists** from **what should be active now**.

### Operating layers

| Layer | Purpose | Loading model |
|---|---|---|
| Kernel | Universal delivery doctrine, safety, approvals, and phase rules | Always loaded |
| Profile | Project and domain decision conventions | One selected profile |
| Doctrine packs | Compact judgement for the current problem | Phase-routed |
| Native skills | Executable procedures available without an external dependency | Phase-routed |
| Capability strengths | Specialist subskills used where strongest | Phase-routed |
| Strategy adapters | Bounded methods from compatible delivery approaches | Selected, not blindly stacked |
| Fresh-context agents | Isolated work for justified subproblems | Contract-bound |
| External resources | Tools, plugins, MCP servers, services, and repositories | Candidates until reviewed and approved |
| Evidence and handoff | Checks, decisions, history, and next action | Persisted |

### Overlap is explicit

Escapement does not resolve overlap by loading everything or deleting every
alternative.

Relationships include:

```text
BASELINE_PLUS_INTENSIFIER
SUBSTITUTE
COMPLEMENTARY
SEQUENTIAL
REFERENCE_ONLY
META_OBSERVER
```

Examples:

```text
decision-coach
→ canonical material-decision procedure

Grilling
→ explicit intensifier only when requested
```

```text
product-specification
→ owns the approved specification

Prompt Master
→ optional sequential export after specification
```

```text
skill-governance
→ owns evaluation and promotion

Task Observer / Evolver
→ may observe or propose, not mutate the harness automatically
```

See:

- [Capability Strength Map](docs/CAPABILITY_STRENGTH_MAP.md)
- [Overlap Analysis](docs/OVERLAP_ANALYSIS.md)
- [Overlap Matrix](catalog/overlap-matrix.json)
- [Capability Registry](catalog/capability-registry.json)
- [Reference Catalogue](docs/REFERENCE_CATALOG.md)

---

## Native skills

The canonical skill source is:

```text
skills/<skill>/SKILL.md
```

Native mirrors are maintained for supported host layouts:

```text
.agents/skills/<skill>/SKILL.md
.claude/skills/<skill>/SKILL.md
```

<details>
<summary><strong>View all 35 native skills</strong></summary>

### Decision, discovery, research, and planning

- [`decision-coach`](skills/decision-coach/SKILL.md)
- [`project-discovery`](skills/project-discovery/SKILL.md)
- [`lifecycle-planning`](skills/lifecycle-planning/SKILL.md)
- [`domain-research`](skills/domain-research/SKILL.md)
- [`solution-brainstorming`](skills/solution-brainstorming/SKILL.md)
- [`product-specification`](skills/product-specification/SKILL.md)
- [`delivery-planning`](skills/delivery-planning/SKILL.md)
- [`reference-router`](skills/reference-router/SKILL.md)

### Consulting, governance, finance, and domain work

- [`consulting-analysis`](skills/consulting-analysis/SKILL.md)
- [`governance-risk-controls`](skills/governance-risk-controls/SKILL.md)
- [`finance-reporting`](skills/finance-reporting/SKILL.md)
- [`dashboard`](skills/dashboard/SKILL.md)
- [`reporting-standard`](skills/reporting-standard/SKILL.md)
- [`workflow`](skills/workflow/SKILL.md)
- [`data-analysis`](skills/data-analysis/SKILL.md)
- [`legal-compliance-analysis`](skills/legal-compliance-analysis/SKILL.md)
- [`investment-analysis`](skills/investment-analysis/SKILL.md)

### Engineering, data, AI, and automation

- [`engineering-review`](skills/engineering-review/SKILL.md)
- [`data-architecture`](skills/data-architecture/SKILL.md)
- [`data-engineering`](skills/data-engineering/SKILL.md)
- [`api-integration`](skills/api-integration/SKILL.md)
- [`software-implementation`](skills/software-implementation/SKILL.md)
- [`frontend-implementation`](skills/frontend-implementation/SKILL.md)
- [`ai-agent-engineering`](skills/ai-agent-engineering/SKILL.md)
- [`automation-engineering`](skills/automation-engineering/SKILL.md)
- [`agent-orchestration`](skills/agent-orchestration/SKILL.md)
- [`agent-blueprint-discovery`](skills/agent-blueprint-discovery/SKILL.md)

### Design, quality, security, and artifacts

- [`design-system`](skills/design-system/SKILL.md)
- [`enterprise-ui-review`](skills/enterprise-ui-review/SKILL.md)
- [`quality-engineering`](skills/quality-engineering/SKILL.md)
- [`security-review`](skills/security-review/SKILL.md)
- [`release-readiness`](skills/release-readiness/SKILL.md)
- [`artifact-production`](skills/artifact-production/SKILL.md)
- [`writing-quality`](skills/writing-quality/SKILL.md)
- [`skill-governance`](skills/skill-governance/SKILL.md)

</details>

Synchronize host mirrors:

```bash
python scripts/escapement.py sync-skills
```

Check without modifying:

```bash
python scripts/escapement.py sync-skills --check
```

---

## Governed external capabilities

Escapement currently preserves 61 external skills, tools, plugins, MCP servers,
repositories, services, and reference systems as governed candidates.

Being catalogued means:

```text
reviewed enough to classify
        ≠
installed
        ≠
active
        ≠
authorized
```

Each candidate can carry:

- source and publisher;
- licence and licence-review status;
- activation status;
- trigger cues;
- permitted use modes;
- overlap group;
- `use_when`;
- `do_not`;
- notes and authority boundaries.

Recent examples include:

| Candidate | Escapement treatment |
|---|---|
| Understand Anything | On-demand code-knowledge candidate for large unfamiliar repositories |
| Grilling / Grill Me | Explicit decision-interview intensifier adapted into `decision-coach` |
| Prompt Master | Optional post-specification prompt-export reference |
| Agency Agents | Specialist-role discovery catalogue |
| Prime Agent | Separate external runtime candidate with explicit authority boundary |
| Evolver | Review-only meta-observer candidate |
| Cloudflare OS | Security and agent-workspace architecture reference |

See [External Candidates Review, 2026-08](docs/decisions/EXTERNAL_CANDIDATES_2026_08.md).

---

# Domain, design, reporting, and data authority

Escapement does not treat all specialist work as generic software engineering.

## Domain evidence

`DOMAIN_CONTEXT.md` can record:

- industry and geography;
- business model;
- users and stakeholders;
- operational reality;
- laws, regulation, and standards;
- terminology;
- market and technical practice;
- approved evidence;
- confidence and research date.

Evidence priority:

```text
Project evidence
→ law, regulator, or standards body
→ official documentation
→ primary disclosures
→ institutional research
→ reputable industry research
→ practitioner and community signals
```

Community popularity is not treated as authoritative evidence.

## Design authority

[`docs/standards/design-intelligence.md`](docs/standards/design-intelligence.md)
is the governing design constitution.

Specialists can research, recommend, implement, verify, or polish beneath that
authority. They do not silently override approved requirements,
accessibility obligations, or project design decisions.

## Reporting authority

[`docs/standards/reporting-intelligence.md`](docs/standards/reporting-intelligence.md)
governs the meaning and traceability of dashboards, KPIs, tables, and exports.

It expects reporting logic such as:

- definition;
- formula;
- source;
- freshness;
- filter context;
- comparison;
- breakdown;
- owner;
- exception status;
- reconciliation to underlying records.

Design Intelligence governs presentation. Reporting Intelligence governs the
integrity of the numbers.

## Data architecture as one decision

Database choice, schema, and API shape are treated as a connected decision.

The `data-architecture` procedure expects the agent to:

1. inspect project and domain context;
2. assess data shape, consistency, query patterns, write volume, concurrency,
   and operational reality;
3. compare materially different options;
4. wait for approval on the selected architecture;
5. design the schema for the chosen model;
6. design the API against that schema;
7. persist selected and rejected alternatives.

Baseline field-shape rules exist unless the domain overrides them:

```text
Name           letters, spaces, hyphens, apostrophes
Phone          target-country digit rules + explicit country code
Email          standard local@domain shape
Money/quantity non-negative unless the domain genuinely permits otherwise
Date           real calendar date
```

Server-side validation remains the control. Client-side validation is a UX
layer.

---

# Multi-module PROGRAMs

A single turn should govern one bounded slice. A PROGRAM may span many modules
and many turns.

`scripts/program_modules.py` maintains project-owned state for:

- modules;
- dependencies;
- current module status;
- shared artifacts;
- cross-module consistency checks.

Example:

```bash
python scripts/program_modules.py set-program --name "CRM Platform"
python scripts/program_modules.py add-shared --path DESIGN.md
python scripts/program_modules.py add-module \
  --id billing \
  --name "Billing"
python scripts/program_modules.py add-module \
  --id portal \
  --name "Customer Portal" \
  --depends-on billing
python scripts/program_modules.py set-status \
  --id billing \
  --status plan \
  --checked-shared DESIGN.md
python scripts/program_modules.py list
```

A module cannot move beyond `SPECIFY` until registered shared artifacts have
been checked. It cannot advance through a declared incomplete dependency.

The registry lives in:

```text
docs/PROGRAM_MODULES.json
```

---

# Evidence and truthful closure

Escapement treats executed evidence as part of the runtime contract.

Run a deterministic check:

```bash
python scripts/run_check.py \
  --name "unit-tests" \
  --scope tests \
  -- \
  python -m unittest discover -s tests -p "test_*.py"
```

A check record can contain:

```text
Check name
Command
Working directory
Scope
Start time
Completion time
Duration
Exit code
Result
stdout path + hash
stderr path + hash
Content-derived record identity
```

Before accepting evidence, the runtime verifies:

- required fields;
- referenced output files;
- output hashes;
- record identity;
- successful check result.

Closure rules include:

- a critical failed check cannot become `PASS`;
- `MATERIAL` and `PROGRAM` work require structured evidence;
- missing required production evidence must remain `PARTIAL` or failed;
- the handoff states what was built, checked, deferred, and approved.

Content-addressed local evidence makes accidental or casual fabrication harder.
It is not a substitute for independently controlled CI, external attestations,
or a security sandbox.

---

# Deterministic quality gates

Escapement increasingly converts recurring failures into mechanical checks
instead of adding more prose.

## Security gate

```bash
python scripts/escapement.py security --fail-on high
```

The scanner checks high-risk patterns including private keys and supported
provider-secret formats. Sensitive actions still require approval.

## UI-quality gate

```bash
python scripts/ui_quality_gate.py <frontend-src-dir>
python scripts/ui_quality_gate.py <frontend-src-dir> --fail-on-warn
```

It checks for detectable signals such as:

- responsive breakpoints;
- motion transitions;
- reduced-motion handling;
- `:focus-visible`;
- loading-state handling;
- error-state handling.

This is a heuristic. A clean report is not proof of good UX.

---

# Security and approval gates

Explicit approval is expected before actions such as:

- adding dependencies;
- installing external skills, plugins, or MCP servers;
- using credentials or confidential data;
- changing schemas or role-based access control;
- destructive actions;
- production deployment;
- security testing;
- licence-sensitive reuse.

Authority precedence is defined by the kernel rather than left implicit.

See [SECURITY.md](SECURITY.md).

---

# Durable project memory

The repository, not the chat transcript, is the durable source of project state.

An installed project can maintain:

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
DOMAIN_CONTEXT.md
SESSION_HANDOFF.md
feature_list.json
docs/decisions/DECISION_LOG.md
.agent/runtime/ACTIVE_CONTEXT.md
.agent/runtime/CONTEXT_PACK.md
.agent/runtime/SESSION_MEMORY.md
.agent/runtime/current-turn.json
.agent/runtime/turns.jsonl
```

These files can preserve:

- approved decisions;
- rejected alternatives;
- task tier and lifecycle phase;
- phase-plan revisions;
- domain context and evidence;
- implementation status;
- executed checks;
- open risks;
- deferred work;
- exact next action.

---

# Parallel and fresh-context work

Fresh-context agents are used where isolation is justified.

Parallel work requires:

- genuinely independent tasks;
- separate files or non-conflicting state;
- explicit input and output contracts;
- bounded context;
- a named integration owner;
- merge order;
- whole-system verification after integration.

Actual parallel dispatch remains host-dependent.

---

# Host integration

Escapement separates **having instructions available** from **actually activating
the runtime**.

| Host | Current repository integration | Evidence boundary |
|---|---|---|
| Claude Code | `.claude/settings.json`, native skill mirror, Claude plugin manifest | Strongest current real-use evidence |
| Codex | `.codex/hooks.json`, `.agents/skills`, Codex plugin manifest | Automatic runtime packaging exists; equivalent cross-host conformance is not yet established |
| Gemini CLI | `GEMINI.md` points to the authoritative kernel | Runtime bootstrap remains manual |
| GitHub Copilot | `.github/copilot-instructions.md` points to the kernel where applicable | Runtime bootstrap remains host-dependent/manual |
| Cursor / Antigravity / other repository-aware agents | Kernel can be followed where supported | Runtime activation depends on host capability |

### Claude Code

`.claude/settings.json` wires the Escapement runtime into:

- session start;
- user prompt submission;
- stop.

The repository also includes:

```text
.claude-plugin/plugin.json
```

as Claude plugin packaging metadata.

### Codex

`.codex/hooks.json` provides runtime hook packaging through shell and PowerShell
wrappers.

The repository also includes:

```text
.codex-plugin/plugin.json
```

with skills and hook metadata.

These manifests are packaging surfaces. Their presence is not a claim of
marketplace publication or full host conformance.

### Other hosts

A host that only reads `AGENTS.md` sees the doctrine but may not automatically
run `agent_runtime.py`.

For hosts without automatic wiring, the kernel requires the equivalent of:

```text
session-start
prompt
stop
```

and treats the runtime output as required context.

---

# Safe installation, updates, and drift detection

Escapement distinguishes:

| File class | Behavior |
|---|---|
| Framework-managed | Installed and updated by Escapement |
| Project-owned seed | Created when missing, then preserved as project state |
| Generated runtime | Created during work and not treated as disposable framework content |

Preview an update:

```bash
python scripts/escapement.py update /path/to/your-project
```

Apply safe managed-file changes:

```bash
python scripts/escapement.py update /path/to/your-project --apply
```

Conflicts are reported instead of silently overwritten. Managed replacements
are backed up first.

Repair missing framework-managed files:

```bash
python scripts/escapement.py repair /path/to/your-project
```

Detect drift:

```bash
python scripts/escapement.py doctor --root /path/to/your-project
```

---

# Commands

## Framework

```text
python scripts/escapement.py version
python scripts/escapement.py init <target>
python scripts/escapement.py update <target>
python scripts/escapement.py repair <target>
python scripts/escapement.py doctor --root <target>
python scripts/escapement.py explain "<prompt>"
python scripts/escapement.py capability-audit "<prompt>" --markdown
python scripts/escapement.py catalog list --catalog skills
python scripts/escapement.py catalog list --catalog resources
python scripts/escapement.py catalog list --catalog patterns
python scripts/escapement.py catalog search "<query>"
python scripts/escapement.py sync-skills
python scripts/escapement.py eval
python scripts/escapement.py security --fail-on high
python scripts/escapement.py observability --root <target>
python scripts/escapement.py ablate <component>
python scripts/escapement.py view
python scripts/escapement.py component list
```

## Runtime

```text
python scripts/agent_runtime.py session-start
python scripts/agent_runtime.py manual-start --prompt "<task>" --json
python scripts/agent_runtime.py status
python scripts/agent_runtime.py advance-phase --phase <PHASE> ...
python scripts/agent_runtime.py replan-phases --add-phase <PHASE> --reason "<reason>"
python scripts/agent_runtime.py replan-phases --remove-phase <PHASE> --reason "<reason>"
python scripts/agent_runtime.py close-turn ...
python scripts/agent_runtime.py reset-turn --reason "<reason>"
```

## PROGRAM registry

```text
python scripts/program_modules.py set-program --name "<name>"
python scripts/program_modules.py add-shared --path <path>
python scripts/program_modules.py add-module --id <id> --name "<name>"
python scripts/program_modules.py set-status --id <id> --status <status>
python scripts/program_modules.py list
```

---

# Current validation

Current repository status is recorded in [`manifest.json`](manifest.json) and
exercised through the standard CI workflow.

```text
Validated:                   2026-08-07
Routing evaluations:         72 / 72 PASS
Unit tests:                  165 / 165 PASS
Runtime doctor:               0 failures
Repository doctor:            0 failures, 0 warnings
Security gate:                0 findings
Self-test:                    PASS
Fresh-install lifecycle:      PASS
Python CI matrix:             3.10, 3.12, 3.13
Latest main validation run:   SUCCESS
Kernel:                       795 / 1000 words
Native skills:                35
Capability strengths:         58
Governed external resources:  61
Published case studies:        4
```

Run the main checks locally:

```bash
python -m py_compile scripts/*.py
python scripts/agent_runtime.py doctor
python scripts/escapement.py doctor --root .
python scripts/eval_harness.py run
python -m unittest discover -s tests -p "test_*.py"
python scripts/security_gate.py --fail-on high
python scripts/escapement.py self-test
```

---

# Honest boundaries

Current boundaries include:

- external capability execution depends on host support;
- live network research depends on available tools and permissions;
- real parallel-agent dispatch depends on the host;
- local evidence is not equivalent to independently controlled execution;
- the current ablation corpus measures routing, not final task quality;
- cross-host conformance is not yet established at the same level as current
  Claude Code real-use evidence;
- quota-aware model routing and execution-budget enforcement are not current
  v6.3 capabilities;
- MCP exposure is future scope;
- strict per-skill evidence mapping remains a future hardening opportunity;
- one legacy catalogued capability, `skill-ui`, still has an unresolved exact
  source.

These are boundaries, not hidden completion claims.

---

# v2.0 roadmap

[`ESCAPEMENT_V2_FUTURE_SCOPE.md`](ESCAPEMENT_V2_FUTURE_SCOPE.md) is a future
roadmap, not a description of the current product.

The proposed direction is to evolve the repository-native harness toward a
**provider-agnostic execution control plane for AI-assisted software delivery**.

Major future work includes:

```text
Stable Escapement Core API
        ↓
Host / Provider / Gateway / Local Runtime adapters
        ↓
Execution Governor
        ↓
Model + budget + quota policy
        ↓
Local MCP interface
        ↓
Host Conformance Lab
        ↓
Context + Tool Trust Firewall
        ↓
Context health, worktree isolation, tracing, and optional team surfaces
```

The roadmap explicitly distinguishes:

```text
HostAdapter
ProviderAdapter
GatewayAdapter
LocalRuntimeAdapter
```

and plans for environments such as:

- Claude Code, Codex, Gemini CLI;
- Cursor, Kiro, GitHub Copilot, Kimi Code/CLI, OpenCode, Cline, Windsurf,
  Antigravity, and Aider;
- Anthropic, OpenAI, Google, Moonshot/Kimi, and other model providers;
- OpenRouter, LiteLLM, and enterprise gateways;
- Ollama, LM Studio, vLLM, and other local inference runtimes.

v2 is deliberately **not** defined as "turn Escapement into an MCP server".
MCP is intended to be one portable interface into a stable core.

No v2 roadmap item should be described as integrated until it is implemented
and tested.

---

# Project structure

```text
.
├── AGENTS.md
├── AGENT_RUNTIME.md
├── CLAUDE.md
├── GEMINI.md
├── PROJECT_STATE.yaml
├── PROJECT_CONTEXT.md
├── DOMAIN_CONTEXT.md
├── SESSION_HANDOFF.md
├── manifest.json
├── ESCAPEMENT_V2_FUTURE_SCOPE.md
│
├── .claude/
├── .claude-plugin/
├── .codex/
├── .codex-plugin/
├── .agents/
├── .escapement/
├── .github/
│
├── skills/
├── profiles/
├── catalog/
│   └── harness-components.json
├── docs/
│   ├── architecture/
│   ├── doctrine/
│   ├── standards/
│   ├── templates/
│   ├── specs/
│   └── decisions/
├── schemas/
├── scripts/
│   ├── agent_runtime.py
│   ├── escapement.py
│   ├── eval_harness.py
│   ├── ablation_harness.py
│   ├── harness_observability.py
│   ├── security_gate.py
│   └── ui_quality_gate.py
├── tests/
├── evals/
├── reports/
├── extensions/
├── presets/
└── bundles/
```

---

# Contributing

Contributions should strengthen the smallest correct layer instead of expanding
the always-loaded kernel by default.

Before proposing a change:

1. identify the observed failure or missing capability;
2. decide whether deterministic tooling can solve it before adding doctrine;
3. place the change at the narrowest correct layer;
4. preserve context budgets;
5. add or extend evaluation evidence;
6. update generated/catalogued state where required;
7. run the validation suite;
8. keep current capability claims separate from future scope.

For harness components, prefer a measurable hypothesis where practical:

```text
What failure should this component prevent?
What context or complexity does it cost?
Which evaluation can exercise it?
What would happen if it were removed?
```

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

# Licence

Escapement is **source-available**, not OSI open source.

The source is publicly available for evaluation, learning, non-commercial
experimentation, and attributed internal use.

Commercial redistribution, resale, white-labelling, hosted resale, and
substantial republication require written permission from the copyright owner.

Third-party skills, plugins, tools, and references retain their own licences.

See:

- [LICENSE.md](LICENSE.md)
- [NOTICE.md](NOTICE.md)
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- [Reference Catalogue](docs/REFERENCE_CATALOG.md)

---

<div align="center">

**Understand enough. Improve the decision. Build. Test. Prove. Persist.**

</div>
