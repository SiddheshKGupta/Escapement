# VLCO Product Build Standard

**A source-available operating standard and engineering harness for disciplined AI-assisted product delivery.**

VLCO Product Build Standard helps Claude Code, Codex, Cursor, Cline, Roo Code, and other AI coding agents plan, build, test, review, and document enterprise software with stronger control and less unnecessary context.

It combines:

```text
Product thinking
+ Context engineering
+ Harness engineering
+ Skill governance
+ Enterprise standards
+ Deterministic validation
+ Human approval gates
```

> Understand enough. Decide enough. Build. Test. Prove. Update.

---

## Status

```text
Current version: 5.2
Architecture: Progressive disclosure
Primary instruction file: AGENTS.md
Governance model: Skill Evidence Loop
Context model: Selective context packs
Harness model: Deterministic-first validation
```

### Licence Status

```text
Source Available — Not Open Source
```

This repository is publicly available for reference, evaluation, learning, and attributed internal use.

Commercial redistribution, white-labelling, resale, and substantial republication require permission from V L & CO.

See:

```text
LICENSE.md
NOTICE.md
```

---

## The Problem

AI coding agents can produce prototypes quickly, but enterprise software needs more than generated code.

Common delivery failures include:

* Coding before understanding the business
* Invented workflows or business rules
* Excessive documentation before implementation
* Large instruction files consuming model context
* Multiple overlapping skills being loaded
* Generic AI-generated user interfaces
* Dashboard numbers without traceability
* Tests being claimed rather than executed
* Architecture changes without approval
* Skill usage without evidence of value
* Long agent loops without stopping conditions
* Project knowledge being lost between sessions

VLCO Product Build Standard provides a controlled delivery system for addressing these failures.

---

## Core Doctrine

```text
Judgement before answers.
Evidence before opinion.
Verification before confidence.
Structure before execution.
Implementation before commentary.
```

The standard follows these practical rules:

1. Do not code from guesses.
2. Inspect the repository before asking questions.
3. Do not ask questions already answered by project files.
4. Ask only questions that can materially affect delivery.
5. Use the smallest useful skill stack.
6. Load only the context required for the current task.
7. Run deterministic checks before model judgement.
8. Record evidence for important claims.
9. Require approval for material changes.
10. Stop documenting when the project is safe to build.

---

## Operating Model

```text
Inspect
→ Clarify
→ Decide
→ Plan
→ Build
→ Test
→ Review
→ Prove
→ Update
→ Handoff
```

Every material task should answer:

```text
What are we building?
Why does it matter?
What is already approved?
What remains unknown?
Which files are relevant?
Which skills are needed?
Which checks must run?
Which actions require approval?
What evidence proves completion?
```

---

## Work Modes

Every assignment must be classified into one operating mode.

| Mode      | Use                                                                 |
| --------- | ------------------------------------------------------------------- |
| `FULL`    | New product, application, module, architecture, or major workflow   |
| `DELTA`   | Material change to an existing product or approved design           |
| `EXECUTE` | Approved ticket, isolated bug, copy change, or small UI improvement |

### FULL

```text
Inspect
→ Discover
→ Clarify
→ Decide
→ Plan
→ Approve
→ Build
```

Use when core product, workflow, data, architecture, permissions, or security decisions must be established.

### DELTA

```text
Read existing decisions
→ Identify impact
→ Ask unresolved questions
→ Update affected documents
→ Approve material changes
→ Build
```

Use when the product already exists but a meaningful change is required.

### EXECUTE

```text
Confirm ticket
→ Inspect affected files
→ Implement
→ Test
→ Record evidence
→ Handoff
```

Use for approved and clearly bounded work.

Do not run full discovery for a minor bug or approved ticket.

---

## Progressive Disclosure

The standard avoids loading every instruction into the agent context.

The agent starts with:

```text
AGENTS.md
PROJECT_STATE.yaml
```

It then loads only the relevant standard, skill, decision, or checklist.

Examples:

| Work               | Load                                                  |
| ------------------ | ----------------------------------------------------- |
| Dashboard          | `data-reporting.md` and dashboard skill               |
| Workflow           | workflow skill and relevant process documents         |
| UI review          | `ui.md` and UI review skill                           |
| API integration    | `integrations.md` and API integration skill           |
| Security review    | `security.md`                                         |
| Performance review | `performance.md`                                      |
| Release            | release-readiness skill and pre-release checklist     |
| Skill audit        | skill-governance skill and usage log                  |
| Material task      | context engineering and harness engineering standards |

The root instruction file acts as a map, not an encyclopedia.

---

## Context Engineering

Context Engineering means giving the agent the **smallest complete context required for the current decision**.

The standard uses four actions:

```text
Write
→ Select
→ Compress
→ Isolate
```

### Write

Store durable project knowledge in repository files:

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
CURRENT_PHASE.md
DECISION_LOG.md
SESSION_HANDOFF.md
PRD.md
ARCHITECTURE.md
SECURITY.md
```

The conversation is not the permanent source of truth.

### Select

Load only:

* Current goal
* Approved scope
* Non-goals
* Exact files being changed
* Relevant decisions
* Relevant standards
* Selected skills
* Acceptance criteria
* Required checks

### Compress

At phase boundaries or after long sessions:

* Update project state
* Record decisions
* Refresh the handoff
* Remove superseded assumptions
* Replace repeated explanations with links
* Generate a fresh context pack

### Isolate

Use bounded subagents for:

* Independent research
* Security review
* Test generation
* UI critique
* Architecture review
* Repository exploration

Subagents should return concise findings and evidence paths rather than full transcripts.

---

## Context Packs

For material tasks, generate:

```text
CURRENT_CONTEXT.md
```

A context pack should contain:

```text
Task ID
Goal
Mode
Approved scope
Non-goals
Current state
Exact files
Relevant decisions
Relevant standards
Selected skills
Data and permissions
Acceptance criteria
Checks
Blockers
Approval gates
Turn and retry budget
Freshness timestamp
```

Recommended target:

```text
1,000 words or fewer
```

Context packs should be refreshed when:

* Scope changes
* Decisions change
* The task moves into a new phase
* The agent loses track of the goal
* Old logs begin crowding active context
* A session handoff occurs

---

## Harness Engineering

The engineering harness is the full environment controlling the agent:

```text
Instructions
+ Context
+ State
+ Skills
+ Tools
+ Tests
+ Approval gates
+ Feedback
```

The harness loop is:

```text
Define task
→ Assemble context
→ Route skills and tools
→ Execute one bounded step
→ Observe
→ Run deterministic checks
→ Run semantic and risk review
→ Accept, retry, escalate, or stop
→ Record evidence
→ Improve from repeated evidence
```

### Deterministic Checks First

Examples:

* Unit tests
* Integration tests
* Type checking
* Linting
* Schema validation
* Manifest validation
* File existence
* Required fields
* Markdown line limits
* Permission checks
* Reconciliation checks
* Command exit codes
* Broken link checks

Model review should not replace checks that can be performed deterministically.

### Semantic and Risk Review

Use model or human review for:

* Requirement coverage
* Business realism
* Workflow correctness
* UX quality
* Risk interpretation
* Architecture quality
* Commercial suitability
* Documentation clarity

### Human Approval Gates

Approval is required before:

* Database schema changes
* Authentication changes
* Role or permission changes
* Destructive actions
* Production deployment
* Paid service activation
* New external integrations
* Material scope changes
* Confidential data access
* Broad refactors
* Licence-sensitive code reuse
* External skill installation with broad permissions

---

## Skill Governance

Skills must be selected because they solve a defined capability need.

They should not be loaded simply because they are available.

```text
Capability need
→ Primary skill
→ Optional specialist
→ Overlapping alternatives rejected
```

### Active Skill Budget

Recommended maximum:

```text
8 active material skills
```

Reference websites and inspiration galleries do not count as active skills unless their instructions are loaded into the agent context.

### One Primary Skill per Capability

Examples:

| Capability                      | Default rule                                      |
| ------------------------------- | ------------------------------------------------- |
| UI design quality               | Taste Skill or Open Design                        |
| Agent workflow                  | Superpowers or gstack                             |
| Browser testing                 | Playwright by default                             |
| Current framework documentation | Context7                                          |
| Recent research                 | last30days                                        |
| Persistent memory               | Claude Mem only for long-running projects         |
| Repository graph                | Graphify only for complex repositories            |
| Motion quality                  | Emil Kowalski Skills only when motion is material |
| Repeated process learning       | Task Observer only when justified                 |

Overlapping skills must be rejected or explicitly justified.

---

## Skill Evidence Loop

A skill counts as used only when there is evidence.

```text
Route
→ Declare
→ Execute
→ Observe
→ Validate
→ Score
→ Decide
→ Learn
```

### Route

Identify the capability required and select one primary skill.

### Declare

Before execution, record:

```text
Skill
Trigger
Phase
Reason selected
Expected output
Validation method
Permissions
Turn budget
Retry budget
Alternatives rejected
```

### Execute

Follow the selected skill without mixing overlapping alternatives.

Save large outputs to files instead of permanently loading them into active context.

### Observe

Capture:

* Whether the skill was actually invoked
* Whether its trigger was valid
* Whether required steps were followed
* Which artifact was produced
* Which checks were planned
* Which checks were run
* Which checks were not run
* Number of retries
* Time or turns consumed
* Whether the result materially improved

### Validate

Use this order:

```text
Deterministic checks
→ Contract checks
→ Semantic and risk review
→ Human approval where material
```

### Score

Recommended skill-run scoring:

| Measure                 |  Weight |
| ----------------------- | ------: |
| Trigger accuracy        |      15 |
| Procedure adherence     |      20 |
| Output correctness      |      30 |
| Validation evidence     |      20 |
| Efficiency              |      10 |
| Clarity and reusability |       5 |
| **Total**               | **100** |

Passing rule:

```text
Total score >= 85
and
No critical correctness, security, data, or permission failure
```

### Decide

| Result           | Action                             |
| ---------------- | ---------------------------------- |
| `PASS`           | Keep skill unchanged               |
| `PARTIAL`        | Record the gap                     |
| `FAIL`           | Retry once with corrected context  |
| Repeated failure | Propose a skill revision           |
| `REDUNDANT`      | Merge or retire                    |
| `NOT_NEEDED`     | Improve routing or trigger wording |

### Learn

Do not rewrite a skill after one normal failure.

A skill change should usually require:

* Repeated failure
* Repeated missed triggers
* Repeated validation gaps
* Clear evidence of excessive cost
* Controlled comparison showing a better approach
* A critical safety or security defect

Every material skill change should be versioned and supported by a behaviour test.

---

## Skill Effectiveness

Passing a skill run does not automatically prove that the skill creates value.

Where useful, compare:

```text
Skill-assisted result
vs
Baseline result
```

Measure:

* Requirement coverage
* Defects found
* Rework required
* Test pass rate
* Review score
* Human corrections
* Turns consumed
* Time consumed
* Context consumed

Recommended report:

```text
reports/SKILL_EFFECTIVENESS.md
```

Example:

| Skill            | Relevant tasks | Assisted score | Baseline | Improvement | Added cost | Decision |
| ---------------- | -------------: | -------------: | -------: | ----------: | ---------: | -------- |
| Dashboard        |              5 |             91 |       74 |         +17 |   +2 turns | Keep     |
| UI Review        |              4 |             82 |       79 |          +3 |   +5 turns | Simplify |
| Workflow         |              3 |             93 |       70 |         +23 |   +2 turns | Keep     |
| Repository Graph |              2 |             78 |       77 |          +1 |   +8 turns | Retire   |

This prevents skill theatre and skill accumulation without measurable value.

---

## Enterprise Product Standard

The framework applies delivery controls across:

* Product requirements
* Business workflows
* Data models
* Reporting and dashboards
* Security
* Permissions
* Architecture
* Integrations
* UI and UX
* Performance
* Accessibility
* Testing
* Release management
* Documentation
* Handoff

---

## Enterprise UI Standard

The interface must not look like a generic AI-generated product.

### Avoid

* Default purple or indigo gradients
* Glow cards
* Decorative glass effects
* Sparkle icons
* Excessive rounded cards
* Large empty spaces
* Low information density
* Fake charts
* Decorative dashboards
* Random chart colours
* Non-functional buttons
* Status badges without operational meaning

### Prefer

* Neutral canvas
* Client brand colour for primary actions
* Compact spacing
* Structured navigation
* Breadcrumbs
* Filter bars
* Action toolbars
* Operational tables
* Meaningful status indicators
* Loading skeletons
* Actionable empty states
* Clear error recovery
* Keyboard support
* Accessible focus states
* Restrained animation

### Brand Model

```text
Client primary: var(--brand-color)
Client hover: var(--brand-hover)
Client soft: var(--brand-soft)

V L & CO signature: #53284F
Text foundation: #1C121B
```

Deep Plum should remain a restrained V L & CO structural signature and should not override approved client branding.

---

## Dashboard and Reporting Standard

Every important KPI must define:

```text
Meaning
Formula
Unit
Period
Source
Freshness
Filters
Breakdowns
Drill-down
Target
Owner
Access
Reconciliation
```

Where relevant, reporting should support:

```text
Financial Year
Quarter
Month
YTD
QTD
MTD
Custom period
Prior period
Target
Budget
```

No important number should appear without:

* Source
* Record count
* Refresh time
* Reconciliation logic
* Drill-down path
* Access rule

Dashboards should be operational systems, not decorative presentations.

---

## Security Standard

Applications should implement:

* Server-side permissions
* Least privilege
* Input validation
* Tenant isolation
* Record-level access
* Secure secret handling
* Material action audit logs
* Safe caching
* Data retention rules
* Backup and recovery
* AI data restrictions
* Secure failure behaviour

The agent must request approval before changing:

* Authentication
* MFA
* SSO
* Role permissions
* Row-level security
* Data residency
* Deletion rules
* Production access
* Confidential data handling

---

## Performance Standard

Performance must be measured rather than assumed.

Evaluate:

* Bundle size
* Initial load
* Interaction latency
* Image and font weight
* API latency
* Database latency
* Cache behaviour
* Search performance
* Large tables and lists
* Background processing

Use where appropriate:

* Code splitting
* Lazy loading
* Image optimisation
* Virtualisation
* Pagination
* Request cancellation
* Caching
* Compression
* Batched safe writes
* Background jobs
* Optimistic UI

Optimistic UI should not be applied blindly to:

* Financial settlements
* Material approvals
* Irreversible actions
* Security-sensitive changes
* Destructive operations

---

## Minimal Documentation

Documentation exists to support decisions and implementation.

It should not become a substitute for delivery.

| Document               | Recommended maximum |
| ---------------------- | ------------------: |
| BRD                    |           120 lines |
| PRD                    |           150 lines |
| FRD                    |           180 lines |
| Architecture           |           180 lines |
| Security               |           120 lines |
| Frontend specification |           150 lines |
| Session handoff        |            40 lines |

Prefer:

* IDs
* Tables
* Bullets
* Short process flows
* Acceptance criteria
* Decision references
* Evidence links
* Explicit `TBD` markers

Avoid:

* Repeated background
* Generic introductions
* Marketing language
* Long prose
* Duplicated requirements
* Content that does not affect implementation

### Documentation Stop Rule

Stop documenting when:

* Scope is clear
* Material decisions are recorded
* Acceptance is testable
* Architecture is safe enough
* Blocking unknowns are closed

Then build.

---

## Repository Structure

```text
VLCO-Product-Build-Standard/
│
├── AGENTS.md
├── README.md
├── manifest.json
├── CHANGELOG.md
├── LICENSE.md
├── NOTICE.md
├── CONTRIBUTING.md
│
├── PROJECT_STATE.yaml
├── PROJECT_CONTEXT.md
├── CURRENT_PHASE.md
├── SESSION_HANDOFF.md
├── SKILLS_INVENTORY.md
├── SKILL_USAGE_PLAN.md
├── AI_REPORT.md
│
├── docs/
│   ├── standards/
│   │   ├── context-engineering.md
│   │   ├── harness-engineering.md
│   │   ├── ui.md
│   │   ├── data-reporting.md
│   │   ├── security.md
│   │   ├── performance.md
│   │   ├── testing.md
│   │   └── integrations.md
│   │
│   ├── templates/
│   │   ├── BRD.template.md
│   │   ├── PRD.template.md
│   │   ├── FRD.template.md
│   │   ├── ARCHITECTURE.template.md
│   │   ├── SECURITY.template.md
│   │   ├── FRONTEND_SPEC.template.md
│   │   ├── TICKETS.template.md
│   │   ├── DISCOVERY_REPORT.template.md
│   │   ├── CONTEXT_PACK.template.md
│   │   ├── SKILL_RUN.template.md
│   │   └── SKILL_HEALTH.template.md
│   │
│   ├── decisions/
│   │   ├── ADR-000-template.md
│   │   └── DECISION_LOG.md
│   │
│   └── checklists/
│       ├── discovery-gate.md
│       ├── build-readiness.md
│       ├── context-health.md
│       ├── skill-run.md
│       └── pre-release.md
│
├── skills/
│   ├── project-discovery/
│   ├── dashboard/
│   ├── workflow/
│   ├── ui-review/
│   ├── api-integration/
│   ├── release-readiness/
│   └── skill-governance/
│
├── scripts/
│   ├── build_context_pack.py
│   ├── skill_audit.py
│   └── validate_standard.py
│
├── schemas/
│   └── skill-run.schema.json
│
├── logs/
│   └── skill-usage.jsonl
│
├── reports/
│   ├── SKILL_HEALTH.md
│   └── SKILL_EFFECTIVENESS.md
│
├── tests/
│   └── agent-behaviour/
│
├── examples/
│   └── enterprise-dashboard/
│
├── .claude/
├── .codex/
└── .github/
    ├── workflows/
    │   └── validate-standard.yml
    ├── PULL_REQUEST_TEMPLATE.md
    └── ISSUE_TEMPLATE/
```

Some roadmap files shown above may be introduced in later releases.

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/SiddheshKGupta/VLCO-Product-Build-Standard.git
cd VLCO-Product-Build-Standard
```

### 2. Add the standard to a project

Copy the required files into the target project.

Minimum recommended set:

```text
AGENTS.md
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
CURRENT_PHASE.md
SESSION_HANDOFF.md
SKILLS_INVENTORY.md
SKILL_USAGE_PLAN.md
AI_REPORT.md
docs/
skills/
scripts/
schemas/
```

### 3. Configure project state

Update:

```text
PROJECT_STATE.yaml
```

Example:

```yaml
project_name: Enterprise Workflow Platform
phase: discovery
work_mode: FULL
implementation_authorized: false
approved_ticket: null

documents:
  brd: missing
  prd: missing
  frd: missing
  architecture: missing
  security: missing
  frontend_spec: missing
  tickets: missing
  ai_report: active

blocking_decisions:
  - authentication-provider
  - tenant-model

accepted_assumptions: []
selected_skills: []
```

### 4. Configure project context

Update:

```text
PROJECT_CONTEXT.md
```

Include:

* Product
* Business problem
* Users
* Intended outcome
* Current process
* Existing systems
* Known constraints
* Current priority
* Non-goals

### 5. Start the agent

Example:

```text
Read AGENTS.md and PROJECT_STATE.yaml.

Inspect the repository before asking questions.

Classify this work as FULL, DELTA, or EXECUTE.

Load only the standards and skills relevant to the task.

Ask only questions that can materially affect scope, workflow, data,
permissions, integrations, security, architecture, UI, or acceptance.

For material work, build a context pack and declare the selected skills.

Do not begin FULL or DELTA implementation until the readiness gate is complete.
```

---

## Validation

Run the skill audit:

```bash
python scripts/skill_audit.py
```

Recommended future unified validation:

```bash
python scripts/validate_standard.py
```

The unified validator should check:

* Manifest completeness
* Required root files
* Markdown line limits
* Skill frontmatter
* Duplicate skill names
* Broken internal links
* JSONL validity
* Evidence-path existence
* Score limits
* Behaviour-test coverage
* Release placeholders
* Context-pack size

---

## GitHub Actions

The recommended CI workflow is:

```text
.github/workflows/validate-standard.yml
```

It should run on:

```text
push
pull_request
manual workflow dispatch
```

Recommended checks:

```text
Manifest
Structure
Skill schema
Skill evidence
Documentation budgets
Internal links
Behaviour tests
Context health
Licence and notice
```

This converts repository doctrine into enforceable delivery controls.

---

## Behaviour Tests

The repository includes scenarios that test whether an AI agent follows the operating model.

Examples:

* New project discovery
* Small bug execution
* Skill overlap
* Skill overuse
* Skill not triggered
* Context rot
* Harness improvement
* Dashboard KPI traceability
* Material architecture change
* Instruction conflict
* Production deployment

The agent must not:

* Start coding immediately on a new product
* Run full discovery for a minor bug
* Install every available skill
* Claim tests passed without running them
* Invent KPI totals
* Silently change architecture
* Ignore instruction conflicts
* Deploy without approval
* Rewrite skills from one anecdotal failure
* Keep stale context active

Future behaviour tests should also be machine-readable for automated agent regression testing.

---

## Definition of Done

A feature is complete only when:

* The approved requirement works
* Permissions work
* Loading, empty, error, permission, and success states work
* Tests pass
* Totals reconcile
* Accessibility is checked
* Performance is acceptable
* Security implications are reviewed
* Required evidence exists
* Documentation is updated
* No critical defect remains
* Handoff is written

---

## Roadmap

### v5.3 — Enforcement

```text
Unified validator
GitHub Actions
Enhanced skill evidence schema
Intelligent context-pack generator
Machine-readable behaviour tests
```

### v5.4 — Usability

```text
CLI installer
Doctor command
Sample enterprise project
Improved quick-start workflow
Project template separation
```

### v6.0 — Intelligence Layer

```text
Skill effectiveness comparison
Automatic skill-routing recommendations
Cross-project skill health reporting
MCP server
Central version registry
Organisational policy overlays
```

---

## Proposed CLI

```bash
vlco-build init
vlco-build validate
vlco-build context
vlco-build skill-audit
vlco-build doctor
vlco-build update
vlco-build handoff
```

---

## Reference Resources

VLCO Product Build Standard may reference external repositories, tools, skills, design resources, or research.

Examples may include:

* AppFlowy
* Plausible Analytics
* last30days
* Stop Slop
* Task Observer
* Emil Kowalski Skills
* Taste Skill
* Open Design
* Superpowers
* Claude Mem
* Graphify
* gstack
* Context7
* Playwright

Every external resource remains governed by its own licence and terms.

Reference does not mean:

* Automatic installation
* Approval for production use
* Endorsement
* Transfer of ownership
* Permission to copy code
* Permission to expose confidential information

Users must verify:

* Canonical source
* Maintenance status
* Security implications
* Required permissions
* Licence
* Compatibility
* Operational value

---

## Contributing

Improvements should be based on evidence.

Before adding a new rule:

1. Show the failure, repeated correction, or measurable need.
2. Identify the correct location.
3. Check for duplication.
4. Prefer consolidation over expansion.
5. Update the relevant behaviour test.
6. Update the changelog.

See:

```text
CONTRIBUTING.md
```

---

## Ownership

**Developed by V L & CO**

Copyright © 2026 V L & CO. All rights reserved.

This repository is source-available and is not distributed under an open-source licence.

For commercial licensing, white-labelling, organisational adoption, or implementation support, contact V L & CO.
