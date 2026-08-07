<div align="center">

# Escapement

### A governed, low-token harness for context-aware AI-assisted delivery.

Escapement helps turn rough requests into clearer decisions, structures context
across delivery phases, supports capability routing and verification, and
preserves project decisions and handoffs across sessions.

[![Version](https://img.shields.io/badge/version-6.3.0-53284F?style=flat-square)](VERSION)
[![CI](https://github.com/SiddheshKGupta/escapement/actions/workflows/validate-standard.yml/badge.svg)](https://github.com/SiddheshKGupta/escapement/actions/workflows/validate-standard.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.12%20%7C%203.13-3776AB?style=flat-square&logo=python&logoColor=white)](.github/workflows/validate-standard.yml)
[![Kernel](https://img.shields.io/badge/kernel-795%20%2F%201000-2F855A?style=flat-square)](AGENTS.md)
[![Native skills](https://img.shields.io/badge/native%20skills-35-2F855A?style=flat-square)](catalog/native-skills.json)
[![Unit tests](https://img.shields.io/badge/unit%20tests-143%20passing-2F855A?style=flat-square)](manifest.json)
[![Case studies](https://img.shields.io/badge/published%20case%20studies-4-2F855A?style=flat-square)](#proof-from-real-use)
[![Licence](https://img.shields.io/badge/licence-source--available-6B7280?style=flat-square)](LICENSE.md)

**Escapement does not upgrade the model. It upgrades how the model works.**

[Why Escapement?](#why-escapement) ·
[Quick start](#quick-start) ·
[How it works](#how-it-works) ·
[Proof](#proof-from-real-use) ·
[Architecture](#architecture) ·
[Validation](#current-validation) ·
[Contributing](#contributing)

</div>

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

AI agents can produce code quickly. Reliable delivery also requires clear
decisions, bounded scope, domain context, explicit permissions, real evidence,
and a handoff that the next session can trust.

---

## Why it exists

Escapement was shaped through repeated work on B2B SaaS, enterprise systems,
governance workflows, reporting products, and AI-assisted builds.

The recurring problem was not only code generation. It was delivery discipline.

| Common failure | Escapement response |
|---|---|
| Important decisions disappear between sessions | Persist decisions, evidence, phase history, and the next action in the repository |
| Agents skip material questions or answer them themselves | Ask no more than five high-impact questions and wait for real answers when a user is present |
| Familiar technologies become silent defaults | Compare materially different options and record the chosen trade-off |
| Business rules and controls arrive after implementation | Route domain, governance, security, data, design, and reporting expertise before or during specification |
| Every skill is loaded into every prompt | Keep the kernel small and load only phase-relevant context |
| Parallel agents produce individually correct but incompatible work | Require independence, explicit contracts, an integration owner, and whole-system verification |
| A generated feature is described as complete without proof | Require structured check records and truthful closure |
| A project grows across several modules and loses shared consistency | Track modules, dependencies, and shared artifacts through a durable PROGRAM registry |
| Installed framework files drift from their source | Detect exact managed-file drift and provide a safe remediation path |

Escapement began with B2B SaaS and enterprise delivery, but it is not limited to
those categories. It can support any repository-based project where an AI agent
must make decisions, use specialist expertise, work across multiple stages,
verify outcomes, and preserve context.

Typical uses include:

- SaaS products and internal platforms
- APIs, backend services, and frontend applications
- data engineering, analytics, and reporting
- workflow automation and AI-agent systems
- governance, finance, legal, security, and compliance work
- consulting deliverables, specifications, SOPs, and structured artifacts
- research-heavy or domain-specific projects

---

## What Escapement is

Escapement is a repository-native operating layer for AI-assisted delivery.

It provides:

- a compact always-loaded delivery kernel;
- task classification for information, micro changes, material work, and programs;
- phase-specific routing of doctrine, native skills, capability strengths, and tools;
- real-user question gates and recommended defaults;
- adaptive lifecycle planning after repository inspection;
- connected database, schema, and API decisioning;
- explicit approval gates for sensitive changes;
- durable project memory and multi-session handoff;
- managed installation, update, repair, and drift detection;
- deterministic checks and content-addressed evidence;
- honest `PASS`, `PARTIAL`, and failure semantics;
- packaging and hooks for Claude Code and Codex.

Escapement is not:

- a replacement for the underlying model;
- a prompt library that loads everything at once;
- permission to deploy, change production data, expose credentials, or run
  security tests;
- a substitute for laws, standards, policy, or qualified domain experts;
- a claim that every catalogued external tool is installed;
- a guarantee that locally produced evidence is equivalent to independently
  controlled CI evidence.

---

## Proof from real use

Escapement is repeatedly exercised through real repository builds, adversarial
scenarios, regression tests, and end-to-end delivery flows.

Four detailed case studies are published:

1. [Vanilla vs. Governed Implementation](reports/CASE_STUDY_vanilla_vs_governed.md)
2. [Full PROGRAM-Tier Claims Platform Build](reports/CASE_STUDY_claims_platform_program_build.md)
3. [Invoice Reconciliation PROGRAM Build](reports/CASE_STUDY_invoice_reconciliation_program_build.md)
4. [Four-Module CRM PROGRAM Build](reports/CASE_STUDY_crm_platform_multi_module_program.md)

Together, they document failures caught in implementation, integration, security
evidence, design routing, capability visibility, reporting, and release
readiness. They also show the framework refusing to describe incomplete work as
production-ready.

Beyond the published reports, Escapement is being used across additional
completed and ongoing projects. Findings from those projects continue to be
converted into framework changes, regression tests, standards, and case studies.

“Battle-tested” here means repeatedly used and challenged against real work. It
does not mean a statistical benchmark or a claim of broad production adoption.

---

## Quick start

### 1. Clone Escapement

```bash
git clone https://github.com/SiddheshKGupta/escapement.git
cd escapement
```

### 2. Install it into a project

```bash
python scripts/escapement.py init /path/to/your-project
```

Windows:

```powershell
py -3 scripts/escapement.py init C:\path\to\your-project
```

The installer copies framework-managed files and creates project-owned seed
files without treating them as disposable framework content.

### 3. Configure the project

Edit:

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
DOMAIN_CONTEXT.md
```

A safe initial state is:

```yaml
project_name: My Product
profile: domain-expertise
phase: discovery
work_mode: FULL
implementation_authorized: false
approved_ticket: null
```

### 4. Verify the installation

From the installed project:

```bash
python scripts/escapement.py doctor --root .
```

### 5. Discover what's available

A first-time user does not automatically know what Escapement can already
do. Browse before you ask for anything:

```bash
python scripts/escapement.py catalog list --catalog skills      # 35 native skills
python scripts/escapement.py catalog list --catalog resources   # 61 governed external candidates
python scripts/escapement.py catalog list --catalog patterns    # agent patterns
python scripts/escapement.py catalog search "browser test"      # search any of the above
```

Being catalogued is not being installed or active by default -- see
[docs/REFERENCE_CATALOG.md](docs/REFERENCE_CATALOG.md). You do not need to
browse manually every time: `decision-coach` also surfaces matched,
not-yet-installed capabilities as part of its own question round for
MATERIAL/PROGRAM work (see [How it works](#how-it-works)).

### 6. Start a governed turn

```bash
python scripts/agent_runtime.py manual-start \
  --prompt "Build a controlled claims workflow" \
  --json
```

For an explanation without starting a turn:

```bash
python scripts/escapement.py explain \
  "Build a controlled claims workflow"
```

For a capability-readiness report:

```bash
python scripts/escapement.py capability-audit \
  "Build a controlled claims workflow" \
  --markdown
```

---

## Host integration

Escapement includes repository packaging for Claude Code and Codex.

### Claude Code

`.claude/settings.json` connects the runtime to:

- session start;
- user prompt submission;
- stop.

### Codex

`.codex/hooks.json` provides the same lifecycle hooks through shell and
PowerShell wrappers.

### Other agents (GitHub Copilot, Cursor, Gemini, manual sessions)

GitHub Copilot already reads `AGENTS.md` natively, and
`.github/copilot-instructions.md` points to it for surfaces that
prioritize that file specifically (VS Code). What these hosts lack is
Claude Code/Codex's automatic hook wiring to `agent_runtime.py` -- without
it, a host reads the kernel as static prose and never activates routing,
phase-gating, or evidence. `AGENTS.md`'s "Host Bootstrap" section makes
this explicit: any host without hook support must invoke `session-start`,
`prompt`, and `stop` itself, and treat their JSON output as required
context, not optional reading.

---

## How it works

### Task tiers

| Tier | Intended use | Runtime expectation |
|---|---|---|
| `INFO` | Explanation, navigation, or status | No material turn required |
| `MICRO` | Small, bounded change | Compact context and at most one native skill per phase |
| `MATERIAL` | Feature or meaningful change | Questions, phase routing, explicit evidence, and durable closure |
| `PROGRAM` | Product, module, or transformation | Full lifecycle, broader capability routing, and multi-turn governance |

### Lifecycle

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
| `ORIENT` | Read the repository, state, constraints, and active work |
| `DISCOVER` | Identify the real decision, inspect before asking, and resolve material questions |
| `RESEARCH` | Gather authoritative domain, regulatory, product, and technical evidence |
| `BRAINSTORM` | Compare materially different approaches |
| `SPECIFY` | Define behaviour, controls, architecture, data, reporting, design, and acceptance criteria |
| `PLAN` | Create bounded tasks, dependencies, ownership, and verification steps |
| `IMPLEMENT` | Build through approved, phase-routed skills |
| `VERIFY` | Test behaviour, integration seams, security, accessibility, and evidence |
| `POLISH` | Improve usability, language, responsiveness, and motion where relevant |
| `RELEASE` | Apply readiness gates and issue a truthful verdict and handoff |

Advance explicitly:

```bash
python scripts/agent_runtime.py advance-phase \
  --phase RESEARCH \
  --summary "Discovery decisions resolved" \
  --skills-used "decision-coach,project-discovery" \
  --files "PROJECT_CONTEXT.md" \
  --evidence "PROJECT_CONTEXT.md"
```

### Adaptive phase planning

The initial phase plan is a default created before full repository inspection.
After `DISCOVER`, it can be revised:

```bash
python scripts/agent_runtime.py replan-phases \
  --add-phase VERIFY \
  --reason "Stored credentials require explicit security verification."

python scripts/agent_runtime.py replan-phases \
  --remove-phase POLISH \
  --reason "Backend-only change with no user-facing surface."
```

A revision:

- can use only the ten catalogued phases;
- cannot remove the current phase;
- cannot remove a phase already completed with evidence;
- requires a reason;
- is persisted in the turn record and `turns.jsonl`.

---

## Better decisions before better code

For `MATERIAL` and `PROGRAM` work, the runtime requires:

```text
Actual decision
Known facts and assumptions
Maximum five material questions
Recommended default for each question
Consequence of choosing differently
Improved execution brief
Domain-research plan
Phase plan
Skill and capability readiness audit
```

When a user is present, the agent must wait for real answers to material
questions. Recommended defaults make the decision easier to review. They are not
permission to silently proceed.

Defaults may be used automatically only for a genuinely unattended run.

The capability-readiness audit must be shown before implementation so users can
see:

- active native skills;
- active specialist strengths;
- detected repository capabilities;
- external candidates and their readiness;
- overlap decisions;
- lifecycle usage;
- licence and activation status.

---

## Data architecture as one decision

Database choice, schema, and API shape are treated as one connected decision.

The `data-architecture` skill requires the agent to:

1. inspect `PROJECT_CONTEXT.md` and `DOMAIN_CONTEXT.md`;
2. assess data shape, consistency, query patterns, write volume, concurrency,
   and operational reality;
3. compare at least two materially different options;
4. present the recommendation and wait for approval;
5. design the schema for the chosen technology’s actual model;
6. design the API against that schema;
7. record the selected option and rejected alternatives durably.

This prevents a database, schema, and API from being designed independently and
then forcing one another to be rebuilt.

Common fields have a sane baseline shape even when nothing project-specific
overrides it -- name, phone, email, money, and date each have a stated
default (letters-only names, country-code-qualified phone numbers, real
email shape, non-negative amounts, real calendar dates), enforced
server-side. Absence of a stated domain rule is not permission to accept
anything.

---

## Multi-module PROGRAMs

A single turn governs one bounded piece of work. A large program may span many
modules and many turns.

`scripts/program_modules.py` provides a durable registry for:

- modules;
- dependencies;
- current module status;
- shared artifacts such as `DESIGN.md`, schema definitions, and
  `DOMAIN_CONTEXT.md`;
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

A module cannot move beyond `SPECIFY` until every registered shared artifact has
been checked. It also cannot advance while a declared dependency remains
incomplete.

The registry lives in `docs/PROGRAM_MODULES.json` and is project-owned.

---

## Architecture

```mermaid
flowchart LR
    A[Rough request] --> B[Decision brief]
    B --> C[Material questions]
    C --> D[Authoritative evidence]
    D --> E[Alternative approaches]
    E --> F[Approved specification]
    F --> G[Phase plan]
    G --> H[Implementation]
    H --> I[Independent verification]
    I --> J[Release verdict]
    J --> K[Durable handoff]
```

### Operating layers

| Layer | Purpose | Loading model |
|---|---|---|
| Kernel | Universal delivery doctrine, safety, approvals, and phase rules | Always loaded |
| Profile | Project and domain decision conventions | One selected profile |
| Doctrine packs | Compact judgement for the current problem | Phase-routed |
| Native skills | Executable procedures available without an external dependency | Phase-routed |
| Capability strengths | Specialist subskills used where they are strongest | Phase-routed |
| Strategy adapters | Bounded methods from compatible delivery approaches | Selected, not stacked blindly |
| Fresh-context agents | Isolated work for justified subproblems | Planned and contract-bound |
| External resources | Tools, plugins, MCP servers, services, and repositories | Candidates until reviewed and approved |
| Evidence and handoff | Checks, decisions, turn history, and next actions | Persisted in the repository |

### Current inventory

```text
Version:                 6.3.0
Repository files:        265
Kernel:                  795 / 1000 words
Profiles:                  2
Doctrine packs:           11
Native skills:            35
Capability strengths:     58
Agent patterns:           21
External resources:       61
Strategy adapters:        10
Capability families:      10
Overlap groups:           14
Published case studies:    4
```

### Low-token contract

```text
Always-loaded kernel:          <= 1000 words
Current kernel:                 795 words
Automatic phase context:       <= 1,800 words
Invoked native-skill context:  <= 1,000 words
Normal doctrine packs:         <= 3 per phase
Native skills for MICRO:       <= 1 per phase
Native skills for MATERIAL:    <= 5 per phase
Native skills for PROGRAM:     <= 6 per phase
```

Escapement uses more capabilities across the lifecycle, not more context inside
one prompt.

---

## Capability orchestration

Escapement does not resolve overlap by loading every capability or deleting
useful alternatives.

It records explicit relationships:

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
Karpathy Guidelines
→ baseline engineering behaviour

Ponytail
→ optional implementation intensifier
```

```text
Design Intelligence
→ authority

UI/UX Pro Max
→ research and recommendation

Taste Skill
→ art direction

frontend-design
→ implementation

Impeccable
→ verification and polish

Emil Kowalski
→ motion specialisation
```

See:

- [Capability Strength Map](docs/CAPABILITY_STRENGTH_MAP.md)
- [Overlap Analysis](docs/OVERLAP_ANALYSIS.md)
- [Overlap Matrix](catalog/overlap-matrix.json)
- [Capability Registry](catalog/capability-registry.json)
- [Reference Catalogue](docs/REFERENCE_CATALOG.md)

A registry entry is not treated as an installation.

---

## Native skills

The canonical source for each skill is:

```text
skills/<skill>/SKILL.md
```

The installer maintains native mirrors for supported hosts:

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

Synchronise the native mirrors:

```bash
python scripts/escapement.py sync-skills
```

Check without modifying:

```bash
python scripts/escapement.py sync-skills --check
```

---

## Domain, design, and reporting authority

Escapement separates domain correctness from visual execution.

### Domain context

Every installed project receives `DOMAIN_CONTEXT.md`, which can record:

- industry and geography;
- users and stakeholders;
- business model and operating reality;
- laws, regulations, and standards;
- current market and technical practice;
- comparable systems;
- terminology;
- approved evidence;
- confidence and research date.

Evidence priority is:

```text
Project evidence
→ law, regulator, or standards body
→ official documentation
→ primary disclosures
→ institutional research
→ reputable industry research
→ practitioner and community signals
```

### Design authority

[`docs/standards/design-intelligence.md`](docs/standards/design-intelligence.md)
is the supreme design constitution.

A generic frontend request must still surface design direction before
implementation. Specialists may research, propose, implement, verify, or polish.
They may not silently override approved product requirements, accessibility
obligations, `DESIGN.md`, or the constitution.

### Reporting authority

[`docs/standards/reporting-intelligence.md`](docs/standards/reporting-intelligence.md)
governs whether dashboards, KPI tiles, tables, and exports are correct,
traceable, and honestly formatted.

It requires:

- a definition, formula, source, freshness, filters, comparison, breakdown,
  owner, and exception status for each KPI;
- management summary, analytical breakdown, and record-level evidence;
- absolute numbers before percentages for management views;
- visible reporting periods and relevant comparisons;
- reconciliation between dashboards, tables, exports, and source records;
- locale-correct currency, digit grouping, and unit scale.

Design Intelligence governs appearance. Reporting Intelligence governs the
meaning and integrity of the numbers.

---

## Parallel and fresh-context agents

Parallel execution requires:

- genuinely independent tasks;
- separate files or non-conflicting state;
- explicit input and output contracts;
- bounded context;
- a named integration owner;
- a defined merge order;
- whole-system verification after integration.

Use fresh-context agents for sequential work that benefits from isolation.

The availability of actual parallel dispatch depends on the host. The planning,
contract, ownership, and verification rules remain applicable even when work is
performed sequentially.

---

## Evidence and truthful closure

Escapement treats evidence as part of the runtime contract.

Run a deterministic check:

```bash
python scripts/run_check.py \
  --name "unit-tests" \
  --scope tests \
  -- \
  python -m unittest discover -s tests -p "test_*.py"
```

The resulting record includes:

```text
Check name
Command
Working directory
Scope
Start and completion time
Duration
Exit code
Result
Standard-output path and hash
Standard-error path and hash
Content-derived record identity
```

Before accepting a record, the runtime verifies that:

- required fields are present;
- referenced output files exist;
- output hashes match;
- the record identity can be recomputed;
- the check actually passed.

Closure rules:

- a critical failed check cannot become a `PASS`;
- `MATERIAL` and `PROGRAM` work require structured evidence;
- missing production evidence requires `PARTIAL` or failure;
- the handoff must state what was built, checked, deferred, and approved.

Local content-addressed evidence raises the cost of accidental or casual
fabrication. It is not a substitute for independently controlled CI or a
sandbox when stronger assurance is required.

Every closed turn already writes to `.agent/runtime/turns.jsonl` and
`logs/skill-usage.jsonl` -- nothing read them back as a trend until asked:

```bash
python scripts/escapement.py observability --root <target>
```

Reports closure-result distribution, phase-replan frequency, skills routed
but never used, and why packs/skills got rejected (overlap, phase limit,
context budget). An empty report means turns aren't being closed, not
that the harness is healthy.

Observability shows what the harness did. Ablation asks whether a component
earned its place:

```bash
python scripts/escapement.py ablate                  # list ablatable components
python scripts/escapement.py ablate decision-coach   # control vs ablated
```

A run copies the repository to a throwaway directory, removes the
component's registry entry there, and runs the corpus under `evals/` twice.
Canonical files are never modified. The output is a factual diff -- cases
changed, skills or strengths lost, context words freed -- and deliberately
no score: 22 routing cases cannot support one.

"No measurable difference" means the corpus does not exercise that
component, not that the component is useless. Today's corpus is
routing-only; retries, tool activity and task quality need a live-execution
corpus that does not exist yet.

---

## Security and approval gates

Sensitive actions require explicit approval, including:

- adding dependencies;
- using credentials or confidential data;
- changing schemas or role-based access control;
- installing external skills, plugins, or MCP servers;
- running security tests;
- performing destructive operations;
- deploying to production;
- reusing licence-sensitive external material.

The security gate scans for high-risk patterns, including compound secret
assignments such as:

```text
admin_password
db_secret
stripe_api_key
```

Run it directly:

```bash
python scripts/escapement.py security --fail-on high
```

See [SECURITY.md](SECURITY.md).

---

## Durable project memory

The repository, not chat, is the system of record.

An installed project maintains:

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

These files preserve:

- approved decisions and rejected alternatives;
- task tier and lifecycle phase;
- phase-plan revisions;
- domain context and evidence;
- implementation status;
- executed checks;
- open risks and deferred work;
- the exact next action for a future session.

---

## Safe installation and updates

Escapement distinguishes three classes of files.

| Class | Behaviour |
|---|---|
| Framework-managed | Installed and updated by Escapement |
| Project-owned seed files | Created when missing, then preserved as project state |
| Generated local runtime files | Created during work and excluded from framework replacement |

Preview an update:

```bash
python scripts/escapement.py update /path/to/your-project
```

Apply safe managed-file updates:

```bash
python scripts/escapement.py update /path/to/your-project --apply
```

Conflicts are reported rather than silently overwritten. Managed files selected
for replacement are backed up first.

Repair missing managed files:

```bash
python scripts/escapement.py repair /path/to/your-project
```

Detect drift:

```bash
python scripts/escapement.py doctor --root /path/to/your-project
```

---

## Commands

### Framework

```text
python scripts/escapement.py version
python scripts/escapement.py init <target>
python scripts/escapement.py update <target>
python scripts/escapement.py repair <target>
python scripts/escapement.py doctor --root <target>
python scripts/escapement.py explain "<prompt>"
python scripts/escapement.py capability-audit "<prompt>" --markdown
python scripts/escapement.py sync-skills
python scripts/escapement.py eval
python scripts/escapement.py security --fail-on high
python scripts/escapement.py observability --root <target>
python scripts/escapement.py ablate <component>
python scripts/escapement.py view
python scripts/escapement.py component list
python scripts/escapement.py catalog search "<query>"
```

### Runtime

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

### Program registry

```text
python scripts/program_modules.py set-program --name "<name>"
python scripts/program_modules.py add-shared --path <path>
python scripts/program_modules.py add-module --id <id> --name "<name>"
python scripts/program_modules.py set-status --id <id> --status <status>
python scripts/program_modules.py list
```

### UI quality

```text
python scripts/ui_quality_gate.py <frontend-src-dir>
python scripts/ui_quality_gate.py <frontend-src-dir> --fail-on-warn
```

Scans for responsive breakpoints, motion transitions,
`prefers-reduced-motion`, `:focus-visible`, and loading/error-state
handling -- concrete signals, not a substitute for looking at the
interface.

---

## Current validation

The current status is recorded in [`manifest.json`](manifest.json), exercised by
the [Validate Escapement workflow](.github/workflows/validate-standard.yml), and
summarised in [`SESSION_HANDOFF.md`](SESSION_HANDOFF.md).

```text
Routing evaluations:       22 / 22 PASS
Unit tests:                 143 / 143 PASS
Runtime doctor:              0 failures
Repository doctor:           0 failures, 0 warnings
Security gate:               0 findings
Fresh-install self-test:    PASS
Python CI matrix:           3.10, 3.12, 3.13
Native skills:              35
Published case studies:      4
```

Run the same checks locally:

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

## Honest boundaries

Escapement currently has several host or infrastructure boundaries:

- execution of external capabilities depends on the host;
- live network research depends on available tools and permissions;
- real parallel-agent dispatch depends on the host;
- production deployment still requires real infrastructure and human approval;
- local evidence is not equivalent to independently controlled execution;
- strict per-skill evidence mapping remains a future hardening opportunity;
- one catalogued legacy capability, `skill-ui`, still has an unresolved exact
  source.

These boundaries are stated rather than hidden behind a completion claim.

---

## Project structure

```text
.
├── AGENTS.md
├── AGENT_RUNTIME.md
├── CLAUDE.md
├── PROJECT_STATE.yaml
├── PROJECT_CONTEXT.md
├── DOMAIN_CONTEXT.md
├── SESSION_HANDOFF.md
├── manifest.json
│
├── .claude/
├── .codex/
├── .agents/
├── .escapement/
├── .github/workflows/
│
├── skills/
├── profiles/
├── docs/
│   ├── architecture/
│   ├── doctrine/
│   ├── standards/
│   ├── templates/
│   ├── specs/
│   └── decisions/
│
├── catalog/
├── schemas/
├── scripts/
├── tests/
├── evals/
├── reports/
├── extensions/
├── presets/
└── bundles/
```

---

## Contributing

Contributions should strengthen the smallest correct layer rather than expand
the always-loaded core without evidence.

Before proposing a change:

1. show a repeated failure or measurable need;
2. identify the smallest correct layer;
3. add or update an executable test or evaluation;
4. preserve project-owned state and safe update boundaries;
5. update relevant documentation and release notes;
6. run the self-test and security gate.

```bash
python scripts/escapement.py self-test
python scripts/escapement.py security --fail-on high
```

Useful contribution areas include:

- new regression cases from real projects;
- integrations and host adapters;
- routing evaluations;
- domain and reporting skills;
- security and evidence hardening;
- additional case studies;
- documentation and installation improvements.

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Licence

Escapement is source-available for evaluation, learning, non-commercial
experimentation, and attributed internal use.

Commercial redistribution, resale, white-labelling, hosted resale, and
substantial republication require written permission.

Third-party capabilities retain their own licences. A registry entry does not
grant permission to copy or deploy the referenced project.

See:

- [LICENSE.md](LICENSE.md)
- [NOTICE.md](NOTICE.md)
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- [Reference Catalogue](docs/REFERENCE_CATALOG.md)

---

<div align="center">

**Ask better questions. Route the right expertise. Verify the result. Preserve the truth.**

</div>
