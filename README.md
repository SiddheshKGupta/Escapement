# VLCO BuildOS

**Enterprise operating system for disciplined AI-assisted product planning, engineering, governance, testing, and delivery.**

VLCO BuildOS provides a compact, structured operating framework for Claude Code, Codex, Cursor, Roo Code, Cline, and other AI coding agents.

It is designed to solve a common problem in AI-assisted development:

> Agents either start coding before understanding the product, or spend too much time generating long documentation instead of building.

VLCO BuildOS creates a practical middle path:

```text
Understand enough
→ Decide enough
→ Plan clearly
→ Build
→ Test
→ Review
→ Update documentation
```

---

## Why VLCO BuildOS

AI coding agents can generate working prototypes quickly, but enterprise software requires more than working screens.

Projects also need:

* Clear business requirements
* Defined workflows and controls
* Reliable data structures
* Role-based permissions
* Scalable architecture
* API integration discipline
* Enterprise UI and UX
* Performance and accessibility
* Testing and release controls
* Audit-ready documentation
* Human approval at material decision points

VLCO BuildOS introduces these disciplines without forcing the agent to read or write large documents during every task.

---

## Core Principles

```text
Judgement before answers.
Evidence before opinion.
Verification before confidence.
Structure before execution.
Implementation before commentary.
```

The operating model follows five practical rules:

1. Do not code from assumptions.
2. Do not ask questions already answered by the repository.
3. Do not create documentation longer than necessary.
4. Do not install overlapping skills without a clear purpose.
5. Stop documenting once the project is safe to build.

---

## Work Modes

The agent must classify every assignment into one of three modes.

| Mode      | Use                                                                      |
| --------- | ------------------------------------------------------------------------ |
| `FULL`    | New application, module, architecture, major workflow, or major redesign |
| `DELTA`   | Material change to an existing product                                   |
| `EXECUTE` | Approved ticket, isolated bug, copy change, or small UI improvement      |

### FULL Mode

Used when the business model, workflows, data, architecture, or security model must be established.

```text
Inspect
→ Discover
→ Clarify
→ Decide
→ Plan
→ Approve
→ Build
```

### DELTA Mode

Used when the product already exists but a material change is required.

```text
Read existing decisions
→ Identify the change
→ Ask only unresolved questions
→ Update affected documents
→ Build
```

### EXECUTE Mode

Used for approved and well-defined work.

```text
Confirm ticket
→ Inspect affected code
→ Implement
→ Test
→ Handoff
```

The agent must not perform full discovery for a minor bug or approved ticket.

---

## Progressive Disclosure

VLCO BuildOS avoids loading every standard into the model context.

The agent starts with the compact root file:

```text
AGENTS.md
```

It then loads only the files relevant to the current task.

Examples:

| Task            | Files loaded                                  |
| --------------- | --------------------------------------------- |
| Dashboard       | `data-reporting.md` and dashboard skill       |
| UI redesign     | `ui.md` and UI review skill                   |
| API integration | `integrations.md` and API integration skill   |
| Security review | `security.md`                                 |
| Release         | release-readiness skill and release checklist |

This reduces token usage and prevents irrelevant instructions from distracting the agent.

---

## Repository Structure

```text
vlco-build-os/
│
├── AGENTS.md
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
│   │   └── DISCOVERY_REPORT.template.md
│   │
│   ├── decisions/
│   │   ├── ADR-000-template.md
│   │   └── DECISION_LOG.md
│   │
│   └── checklists/
│       ├── discovery-gate.md
│       ├── build-readiness.md
│       └── pre-release.md
│
├── skills/
│   ├── project-discovery/
│   ├── dashboard/
│   ├── workflow/
│   ├── ui-review/
│   ├── api-integration/
│   └── release-readiness/
│
├── tests/
│   └── agent-behaviour/
│
├── .claude/
├── .codex/
└── .github/
```

---

## Quick Start

### 1. Add VLCO BuildOS to a project

Copy the following into the target repository:

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
```

### 2. Update the project state

Edit:

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

selected_skills: []
```

### 3. Complete the project context

Edit:

```text
PROJECT_CONTEXT.md
```

Add:

* Product
* business problem
* users
* intended outcome
* current process
* existing systems
* known constraints
* current priority
* non-goals

### 4. Start the coding agent

Example instruction:

```text
Read AGENTS.md and PROJECT_STATE.yaml.

Inspect the repository before asking questions.

Classify this work as FULL, DELTA, or EXECUTE.

Ask only questions that could materially affect the scope, workflow,
data, permissions, integrations, security, UI, architecture, or
acceptance criteria.

Do not begin development until the required readiness gate is complete.
```

---

## Minimal Documentation

VLCO BuildOS treats documentation as a decision and execution tool, not as an essay.

| Document               | Recommended maximum |
| ---------------------- | ------------------: |
| BRD                    |           120 lines |
| PRD                    |           150 lines |
| FRD                    |           180 lines |
| Architecture           |           180 lines |
| Security               |           120 lines |
| Frontend specification |           150 lines |
| Session handoff        |            40 lines |

Documents should use:

* Bullets
* Tables
* IDs
* Short process flows
* Acceptance criteria
* Decision references
* `TBD` markers

Documents should avoid:

* Repeated background
* Generic introductions
* Marketing language
* Long prose explanations
* Content that does not affect implementation

### Documentation Stop Rule

The agent must stop writing documentation when:

* Scope is clear
* Material decisions are recorded
* Acceptance is testable
* Architecture is safe enough
* Blocking unknowns are closed

The agent must then begin implementation.

---

## Skill Governance

VLCO BuildOS uses the smallest effective skill stack.

```text
Capability need
→ Select one primary skill
→ Add a specialist only when necessary
→ Reject overlapping alternatives
```

### Default Skill Budget

A normal working session should use no more than:

```text
8 active material skills
```

Reference websites and design galleries do not count as active skills unless their full instructions are loaded.

### Example Selection Rules

| Capability              | Rule                                              |
| ----------------------- | ------------------------------------------------- |
| UI taste                | Taste Skill or Open Design                        |
| Agent workflow          | Superpowers or gstack                             |
| Browser testing         | Playwright by default                             |
| Technical documentation | Context7                                          |
| Recent research         | last30days                                        |
| Persistent memory       | Claude Mem only for long projects                 |
| Codebase graph          | Graphify only for complex repositories            |
| Motion design           | Emil Kowalski Skills only when motion is material |
| Session learning        | Task Observer only for long-running work          |

The agent must document selected and rejected skills in:

```text
SKILLS_INVENTORY.md
SKILL_USAGE_PLAN.md
```

---

## Enterprise UI Standard

The application must not look like a generic AI-generated interface.

### Avoid

* Default purple or indigo gradients
* Glow effects
* Glassmorphism without purpose
* Sparkle icons
* Excessive rounded cards
* Large empty spaces
* Low information density
* Fake dashboards
* Random chart colours
* Non-functional buttons
* Decorative status badges

### Prefer

* Neutral canvas
* Client brand colour for primary actions
* Compact spacing
* Clear typography
* Structured navigation
* Breadcrumbs
* Filter bars
* Action toolbars
* Operational tables
* Functional status indicators
* Loading skeletons
* Actionable empty states
* Friendly error recovery
* Keyboard navigation
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

Deep Plum should remain a restrained builder signature and should not override the approved product or client branding.

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
```

Where relevant, dashboards should support:

```text
Financial Year
Quarter
Month
YTD
QTD
MTD
Custom period
Prior period
Target or budget
```

Every number must be traceable to the underlying records.

No total should appear without:

* Source
* record count
* refresh time
* reconciliation logic
* drill-down path

---

## Security Standard

Applications must implement:

* Server-side permissions
* Least privilege
* Input validation
* Tenant isolation
* Record-level access
* Secure secrets
* Material action audit logs
* Safe caching
* Data retention rules
* Backup and recovery
* AI data restrictions

The agent must ask before changing:

* Authentication
* MFA
* SSO
* role permissions
* row-level security
* data residency
* deletion rules
* production access

---

## Performance Standard

The agent must measure performance rather than claim it.

Where appropriate, target:

```text
Lighthouse Performance: 90+
```

Evaluate:

* Bundle size
* page loading
* interaction latency
* image and font weight
* API latency
* database latency
* cache behaviour
* large lists
* search performance

Use where appropriate:

* Code splitting
* Lazy loading
* Image optimisation
* Virtualisation
* Pagination
* Request cancellation
* Caching
* Batched safe writes
* Compression
* Background processing
* Optimistic UI

Optimistic UI must not be used blindly for financial settlement, material approvals, irreversible actions, or security-sensitive changes.

---

## Agent Behaviour Gates

The repository includes behaviour scenarios for testing whether an agent follows the operating model.

Examples:

* New project discovery
* Small bug execution
* Skill overlap handling
* Material architecture change
* Dashboard KPI request
* Production deployment

The agent must not:

* Start coding immediately on a new project
* Perform full discovery for a minor bug
* Install every listed skill
* Claim access it does not have
* Claim tests passed without running them
* Silently introduce business rules
* Rewrite architecture outside the approved scope

---

## Project Files

### `PROJECT_STATE.yaml`

Machine-readable current state.

### `PROJECT_CONTEXT.md`

Short product orientation.

### `CURRENT_PHASE.md`

Current goal, ticket, blockers, and next action.

### `SESSION_HANDOFF.md`

Continuity between agent sessions.

### `SKILLS_INVENTORY.md`

Skills available, installed, blocked, or optional.

### `SKILL_USAGE_PLAN.md`

How and when each selected skill will be used.

### `AI_REPORT.md`

Short audit log of:

* AI tools
* skills
* prompts
* errors
* bugs
* corrections
* validation
* lessons

---

## Delivery Loop

```text
Inspect
→ Clarify
→ Decide
→ Plan
→ Build
→ Test
→ Review
→ Update documents
→ Handoff
```

A feature is complete only when:

* Requirement works
* Permissions work
* Loading, empty, error, permission, and success states work
* Tests pass
* Totals reconcile
* Accessibility is checked
* Performance is acceptable
* Documentation is updated
* No critical defect remains
* Handoff is written

---

## Future Roadmap

Possible future additions:

* CLI installer
* Project generator
* Automated document validation
* Skill availability scanner
* Agent readiness checker
* GitHub Actions enforcement
* MCP server
* Central template registry
* Project portfolio dashboard
* Shared organisational standards
* Automated session handoff
* Release readiness reports

Suggested future commands:

```bash
vlco-build init
vlco-build audit
vlco-build validate
vlco-build update
vlco-build handoff
vlco-build doctor
```

---

## Reference Repositories

VLCO BuildOS may reference external open-source repositories for patterns, research, or optional capabilities.

Examples include:

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

Every external repository remains governed by its own licence.

Reference does not mean automatic installation, approval, endorsement, or permission to copy code.

---

## Ownership

**Developed by V L & CO**

Copyright © 2026 V L & CO. All rights reserved.

This repository is proprietary unless a different licence is expressly provided.

See:

```text
LICENSE.md
NOTICE.md
```

---

## Status

```text
Version: 5.0.0
Status: Initial operational release
Architecture: Progressive disclosure
Primary instruction file: AGENTS.md
```
