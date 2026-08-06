<div align="center">

# Escapement

### Capability-strength orchestration for AI-assisted product delivery.

Escapement turns rough requests into stronger decisions, researches relevant
domain standards and current practice, then activates native skills, specialist
capabilities, agents and external tools at the phase where each is strongest.

[![Version](https://img.shields.io/badge/version-6.3.0-53284F?style=flat-square)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Kernel](https://img.shields.io/badge/kernel-698%20words-2F855A?style=flat-square)](AGENTS.md)
[![Evals](https://img.shields.io/badge/routing%20evals-22%2F22-2F855A?style=flat-square)](reports/VALIDATION_v6.3.md)
[![Tests](https://img.shields.io/badge/unit%20tests-61%2F61-2F855A?style=flat-square)](reports/VALIDATION_v6.3.md)
[![Security](https://img.shields.io/badge/security-0%20findings-2F855A?style=flat-square)](reports/VALIDATION_v6.3.md)

**Ask better questions. Use each capability at its strongest phase. Build. Test. Prove. Persist.**

[Quick start](#quick-start) ·
[Architecture](#architecture) ·
[Design authority](#design-authority) ·
[Overlap](#overlap-is-a-first-class-system) ·
[Capability audit](#skill-and-capability-readiness-audit) ·
[Full registry](#external-capability-registry)

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

Agents can generate code quickly. Reliable delivery also requires a shared definition of done, durable decisions, limited scope, explicit permissions, runtime evidence, and a handoff the next session can trust.

### Why the framework exists

AI agents usually fail in one of two directions:

```text
Too little structure
→ forgotten context, invented behaviour and inconsistent execution

Too much structure
→ the agent spends its context managing the framework instead of delivering
```

Escapement keeps the always-loaded kernel small and moves depth into
phase-specific layers:

```text
Decision coaching
→ Domain research
→ Structured brainstorming
→ Product and technical specification
→ Delivery planning
→ Focused implementation
→ Independent verification
→ Polish
→ Release
```

The project can use many capabilities across its lifecycle without loading them
all into one prompt.

---

# What Escapement is

Escapement is a repository-native control system for AI-assisted delivery.

It provides:

- decision coaching before implementation;
- domain-aware research and evidence routing;
- phase-specific native skills and specialist capabilities;
- durable project state and session handoffs;
- explicit approval gates for sensitive actions;
- deterministic checks and truthful completion semantics.

Escapement is **not**:

- a bundle that silently installs every listed plugin or skill;
- a replacement for laws, standards, policy or qualified domain experts;
- an autonomous permission to deploy, change production data or run security tests;
- a guarantee that locally generated evidence is equivalent to isolated CI evidence.

---

# Architecture

```mermaid
flowchart LR
    A[Rough request] --> B[Decision brief]
    B --> C[Material questions + defaults]
    C --> D[Domain standards + current evidence]
    D --> E[Alternative solutions]
    E --> F[Specification]
    F --> G[Plan + agent assignments]
    G --> H[Implementation]
    H --> I[Independent verification]
    I --> J[Polish]
    J --> K[Release + handoff]
```

## Six operating layers

| Layer | Purpose | Loaded |
|---|---|---|
| Kernel | Universal doctrine, safety, questions, phase rules | Always |
| Profile | Domain and project decision conventions | One |
| Doctrine packs | Compact judgement for the current problem | Phase-routed |
| Native skills | Executable fallback procedures | Phase-routed |
| Capability strengths | Specialised subskills used where strongest | Phase-routed |
| External resources | Plugins, MCPs, tools, repositories and services | Candidate until approved |

## Current inventory

```text
Kernel words:          698
Profiles:                2
Doctrine packs:         11
Native skills:          35
Capability strengths:   58
Agent patterns:         21
External resources:     54
Strategy adapters:      10
Capability families:    10
Overlap groups:         12
```

---

# Better decisions before better code

For every `MATERIAL` or `PROGRAM` request, the runtime creates:

```text
Actual decision
Known facts and assumptions
Maximum five material questions
Recommended default for each question
Consequence of choosing differently
Improved execution prompt
Domain-research plan
Phase plan
Skill and capability readiness audit
```

The user does not need to become a prompt engineer.

The agent inspects and researches before asking for information that can be
discovered safely.

---

# Lifecycle

| Phase | Strongest capability examples |
|---|---|
| `ORIENT` | Repository state, Karpathy think-before-coding |
| `DISCOVER` | Decision Coach, Project Discovery |
| `RESEARCH` | Domain Research, Context7, Agent Reach, Last30Days, UI/UX Pro Max |
| `BRAINSTORM` | Superpowers Brainstorming, Taste Skill, solution alternatives |
| `SPECIFY` | Product Specification, domain skills, UI/UX Pro Max design-system recommendations |
| `PLAN` | Delivery Planning, Superpowers Writing Plans, Karpathy simplicity, Ponytail Lite |
| `IMPLEMENT` | Specialised native skills, TDD, subagent development, surgical changes |
| `VERIFY` | Quality Engineering, code review, Impeccable, browser and security evidence |
| `POLISH` | Impeccable Polish, Emil motion review, Stop Slop final lint |
| `RELEASE` | Release Readiness, verification-before-completion, branch finishing |

Advance phases explicitly:

```bash
python scripts/agent_runtime.py advance-phase \
  --phase RESEARCH \
  --summary "Discovery decisions resolved" \
  --skills-used "decision-coach,project-discovery" \
  --files "PROJECT_CONTEXT.md" \
  --evidence "PROJECT_CONTEXT.md"
```

Each transition unloads the previous phase context before loading the next.

## Revising the phase plan

`phase_plan` is a default, decided once at turn start by matching keywords
in the prompt -- it has no way to see what `DISCOVER`'s own repository
inspection actually turns up. `lifecycle-planning`, routed alongside
`decision-coach` and `project-discovery` at every `DISCOVER` phase, checks
whether the default plan still fits once real inspection has happened, and
revises it when it does not:

```bash
python scripts/agent_runtime.py replan-phases \
  --add-phase VERIFY \
  --reason "Touches stored credentials; the prompt never said 'security'."
python scripts/agent_runtime.py replan-phases \
  --remove-phase POLISH \
  --reason "Backend-only change, no user-facing surface."
```

Only the ten cataloged phases can be added or removed -- this revises
sequence, not invents new phases. A phase already completed with recorded
evidence, or the current phase, cannot be removed. Every revision requires a
reason and is permanently recorded on the turn and in `turns.jsonl`.

---

# Low-token contract

```text
Always-loaded kernel:          <= 700 words
Actual kernel:                 698 words
Automatic phase context:       <= 1,800 words
Invoked native skill context:  <= 1,200 words
Normal doctrine packs:         <= 3 per phase
Native skills — MICRO:         <= 1 per phase
Native skills — MATERIAL:      <= 5 per phase
Native skills — PROGRAM:       <= 6 per phase
Specialist strengths:          selected by phase and overlap
```

Escapement counts automatic context and invoked skill context separately.

A selected skill is referenced in the context pack and loaded by the native
agent only when invoked.

---

# Evidence and security integrity

Escapement treats completion evidence as part of the runtime contract.

Structured check records bind together:

```text
Check name
Command
Timing
Exit code
Standard-output hash
Standard-error hash
Record identity
```

The runtime rejects malformed or edited records whose output hashes or record
identity do not match their evidence files.

The security gate also checks common compound secret assignments such as:

```text
admin_password
db_secret
stripe_api_key
```

For high-assurance releases, run checks in isolated CI or a sandboxed runner.
A local verifier and a local agent sharing the same filesystem cannot provide
the same assurance as independently controlled execution infrastructure.

---

# Design authority

[`docs/standards/design-intelligence.md`](docs/standards/design-intelligence.md)
is the **supreme design constitution**.

```text
Approved product requirements and accessibility obligations
→ Product DESIGN.md and brand configuration
→ Design Intelligence Constitution
→ Phase-specific design specialists
→ External references and component sources
```

Specialists have distinct responsibilities:

| Specialist | Strongest role |
|---|---|
| UI/UX Pro Max | Searchable design research, product patterns, palettes, typography, charts and stack guidance |
| Taste Skill | Greenfield art direction, anti-slop variance, density and motion dials |
| Impeccable | Deterministic audit, critique, hardening and final polish |
| Emil Kowalski Skills | Motion decisions, animation implementation and strict motion review |
| Open Design | Optional local design workspace, prototypes, assets and export ecosystem |
| frontend-design | Production frontend implementation from an approved design |
| Mobbin / Refero / Recent | Bounded pattern research |
| Penpot | Collaborative design-system and design-to-code workflow |

No specialist may silently override `DESIGN.md` or the design constitution.

See [Design Stack](catalog/design-stack.json).

---

# Overlap is a first-class system

Escapement does not solve overlap by deleting capabilities or loading all of
them.

It records the relationship:

```text
BASELINE_PLUS_INTENSIFIER
SUBSTITUTE
COMPLEMENTARY
SEQUENTIAL
REFERENCE_ONLY
META_OBSERVER
```

## Example: Karpathy and Ponytail

```text
Karpathy Guidelines
→ baseline engineering behaviour
→ assumptions, simplicity, surgical changes, verifiable goals

Ponytail
→ optional implementation intensifier
→ stronger YAGNI, native-platform and minimum-code pressure
```

Ponytail does not become a second permanent engineering doctrine.

## Example: design systems

```text
Design Intelligence
→ authority

UI/UX Pro Max
→ research and recommendation

Taste Skill
→ brainstorming and art direction

frontend-design
→ implementation

Impeccable
→ verification and polish

Emil Kowalski
→ motion specialisation
```

See:

- [Overlap Analysis](docs/OVERLAP_ANALYSIS.md)
- [Machine-readable Matrix](catalog/overlap-matrix.json)
- [Compact Operational Groups](catalog/overlap-groups.json)

---

# Domain expertise

Each installed project contains:

```text
DOMAIN_CONTEXT.md
```

It records:

- industry and geography;
- users and stakeholders;
- business model and operating reality;
- laws, regulations and standards;
- current market and technology practice;
- comparable systems;
- domain terminology;
- approved evidence;
- confidence and research date.

Evidence order:

```text
Project evidence
→ law, regulator or standards body
→ official documentation
→ primary disclosures
→ institutional research
→ reputable industry research
→ practitioner and community signals
```

Agent Reach and Last30Days extend research coverage. They do not replace
authoritative evidence.

---

# Native skills

Canonical source:

```text
skills/<skill>/SKILL.md
```

Native agent copies:

```text
.agents/skills/<skill>/SKILL.md
.claude/skills/<skill>/SKILL.md
```

| Skill | Phases | Registers |
|---|---|---|
| [`project-discovery`](skills/project-discovery/SKILL.md) | DISCOVER, SPECIFY | CONSULTING, ENGINEERING, DUAL |
| [`consulting-analysis`](skills/consulting-analysis/SKILL.md) | DISCOVER, RESEARCH, BRAINSTORM, SPECIFY, VERIFY | CONSULTING, DUAL |
| [`governance-risk-controls`](skills/governance-risk-controls/SKILL.md) | DISCOVER, SPECIFY, VERIFY | CONSULTING, DUAL |
| [`finance-reporting`](skills/finance-reporting/SKILL.md) | RESEARCH, SPECIFY, IMPLEMENT, VERIFY | CONSULTING, DUAL |
| [`dashboard`](skills/dashboard/SKILL.md) | SPECIFY, IMPLEMENT, VERIFY | CONSULTING, DUAL |
| [`workflow`](skills/workflow/SKILL.md) | DISCOVER, SPECIFY, IMPLEMENT, VERIFY | CONSULTING, DUAL |
| [`engineering-review`](skills/engineering-review/SKILL.md) | BRAINSTORM, SPECIFY, PLAN, IMPLEMENT, VERIFY | ENGINEERING, DUAL |
| [`design-system`](skills/design-system/SKILL.md) | BRAINSTORM, SPECIFY | ENGINEERING, DUAL, ARTIFACT |
| [`enterprise-ui-review`](skills/enterprise-ui-review/SKILL.md) | IMPLEMENT, VERIFY, POLISH | ENGINEERING, DUAL |
| [`api-integration`](skills/api-integration/SKILL.md) | SPECIFY, PLAN, IMPLEMENT, VERIFY | ENGINEERING, DUAL |
| [`artifact-production`](skills/artifact-production/SKILL.md) | SPECIFY, IMPLEMENT, VERIFY, POLISH, RELEASE | ARTIFACT, CONSULTING |
| [`writing-quality`](skills/writing-quality/SKILL.md) | IMPLEMENT, VERIFY, POLISH | ARTIFACT, CONSULTING |
| [`security-review`](skills/security-review/SKILL.md) | RESEARCH, SPECIFY, PLAN, VERIFY, RELEASE | ENGINEERING, DUAL |
| [`release-readiness`](skills/release-readiness/SKILL.md) | RELEASE | ENGINEERING, DUAL |
| [`reference-router`](skills/reference-router/SKILL.md) | DISCOVER, RESEARCH, BRAINSTORM, PLAN | CONSULTING, ENGINEERING, DUAL, ARTIFACT |
| [`skill-governance`](skills/skill-governance/SKILL.md) | DISCOVER, RESEARCH, PLAN, VERIFY | ENGINEERING, DUAL |
| [`decision-coach`](skills/decision-coach/SKILL.md) | DISCOVER | CONSULTING, ENGINEERING, DUAL, ARTIFACT |
| [`lifecycle-planning`](skills/lifecycle-planning/SKILL.md) | DISCOVER | CONSULTING, ENGINEERING, DUAL, ARTIFACT |
| [`domain-research`](skills/domain-research/SKILL.md) | RESEARCH | CONSULTING, ENGINEERING, DUAL, ARTIFACT |
| [`solution-brainstorming`](skills/solution-brainstorming/SKILL.md) | BRAINSTORM | CONSULTING, ENGINEERING, DUAL, ARTIFACT |
| [`delivery-planning`](skills/delivery-planning/SKILL.md) | PLAN | CONSULTING, ENGINEERING, DUAL, ARTIFACT |
| [`agent-orchestration`](skills/agent-orchestration/SKILL.md) | PLAN, IMPLEMENT | CONSULTING, ENGINEERING, DUAL, ARTIFACT |
| [`agent-blueprint-discovery`](skills/agent-blueprint-discovery/SKILL.md) | RESEARCH, BRAINSTORM, PLAN | CONSULTING, ENGINEERING, DUAL |
| [`product-specification`](skills/product-specification/SKILL.md) | SPECIFY | CONSULTING, ENGINEERING, DUAL, ARTIFACT |
| [`data-architecture`](skills/data-architecture/SKILL.md) | SPECIFY | ENGINEERING, DUAL |
| [`data-engineering`](skills/data-engineering/SKILL.md) | SPECIFY, PLAN, IMPLEMENT, VERIFY | ENGINEERING, DUAL, CONSULTING |
| [`frontend-implementation`](skills/frontend-implementation/SKILL.md) | IMPLEMENT | ENGINEERING, DUAL |
| [`quality-engineering`](skills/quality-engineering/SKILL.md) | PLAN, IMPLEMENT, VERIFY, RELEASE | ENGINEERING, DUAL, ARTIFACT |
| [`ai-agent-engineering`](skills/ai-agent-engineering/SKILL.md) | SPECIFY, PLAN, IMPLEMENT, VERIFY | ENGINEERING, DUAL, CONSULTING |
| [`automation-engineering`](skills/automation-engineering/SKILL.md) | SPECIFY, PLAN, IMPLEMENT, VERIFY | ENGINEERING, DUAL, CONSULTING |
| [`data-analysis`](skills/data-analysis/SKILL.md) | RESEARCH, SPECIFY, IMPLEMENT, VERIFY | CONSULTING, ENGINEERING, DUAL |
| [`legal-compliance-analysis`](skills/legal-compliance-analysis/SKILL.md) | RESEARCH, SPECIFY, VERIFY | CONSULTING, DUAL, ARTIFACT |
| [`investment-analysis`](skills/investment-analysis/SKILL.md) | RESEARCH, BRAINSTORM, SPECIFY, VERIFY | CONSULTING, DUAL, ARTIFACT |
| [`software-implementation`](skills/software-implementation/SKILL.md) | IMPLEMENT | ENGINEERING, DUAL |

Synchronise:

```bash
python scripts/escapement.py sync-skills
```

---

# Skill and capability readiness audit

Run:

```bash
python scripts/escapement.py capability-audit \
  "Design a management dashboard with responsive charts and motion" \
  --markdown
```

The audit reports:

```text
Active native skills
Active specialist strengths
Detected repository skills
External install or load candidates
Lifecycle usage plan
Overlap decisions
Design authority
Licence and activation status
```

A catalogue entry is not treated as installed.

---

# Strategy adapters

| Adapter | Name | Phases |
|---|---|---|
| `superpowers-sdlc` | Superpowers SDLC Adapter | BRAINSTORM, PLAN, IMPLEMENT, PARALLEL_IMPLEMENT, VERIFY, FINISH |
| `github-spec-kit` | GitHub Spec Kit Adapter | DISCOVER, SPECIFY, PLAN, CONVERGE |
| `gsd-core` | GSD Phase Execution Adapter | DISCOVER, PLAN, IMPLEMENT, VERIFY, FINISH |
| `agent-reach` | Agent Reach Research Adapter | RESEARCH |
| `last30days` | Last30Days Trends Adapter | RESEARCH |
| `500-ai-agents` | 500+ AI Agent Blueprint Adapter | RESEARCH, BRAINSTORM, PLAN |
| `agent-browser` | Agent Browser Verification Adapter | VERIFY |
| `engineering-behaviour` | Karpathy + Ponytail Engineering Adapter | DISCOVER, PLAN, IMPLEMENT, VERIFY |
| `design-strength-orchestration` | Design Intelligence Specialist Adapter | RESEARCH, BRAINSTORM, SPECIFY, IMPLEMENT, VERIFY, POLISH |
| `browser-verification` | Browser Verification Adapter | IMPLEMENT, VERIFY |

Superpowers is used component-by-component:

```text
BRAINSTORM → brainstorming
PLAN       → writing-plans
IMPLEMENT  → TDD, subagent-driven-development or executing-plans
PARALLEL   → dispatching-parallel-agents
VERIFY     → requesting-code-review + verification-before-completion
RELEASE    → finishing-a-development-branch
```

The runtime remains Escapement. External lifecycle hooks are not stacked
blindly.

---

# Capability families

Fine-grained intents from the original standards are preserved under canonical
families:

| Family | Native fallbacks | Phases |
|---|---|---|
| `business-consulting` | decision-coach, consulting-analysis, project-discovery | DISCOVER, RESEARCH, BRAINSTORM, SPECIFY |
| `governance-risk-controls` | governance-risk-controls, workflow, security-review | DISCOVER, SPECIFY, VERIFY |
| `finance-and-private-capital` | finance-reporting, consulting-analysis, dashboard | RESEARCH, SPECIFY, IMPLEMENT, VERIFY |
| `product-management` | project-discovery, solution-brainstorming, delivery-planning | DISCOVER, BRAINSTORM, SPECIFY, PLAN, RELEASE |
| `data-engineering-and-analytics` | finance-reporting, dashboard, engineering-review, api-integration | SPECIFY, PLAN, IMPLEMENT, VERIFY |
| `engineering` | engineering-review, api-integration, security-review, release-readiness | BRAINSTORM, SPECIFY, PLAN, IMPLEMENT, VERIFY, RELEASE |
| `ai-and-automation` | agent-blueprint-discovery, agent-orchestration, api-integration, security-review | RESEARCH, BRAINSTORM, SPECIFY, PLAN, IMPLEMENT, VERIFY |
| `design-and-experience` | design-system, enterprise-ui-review, writing-quality | RESEARCH, BRAINSTORM, SPECIFY, IMPLEMENT, VERIFY, POLISH |
| `documentation-and-artifacts` | artifact-production, writing-quality | DISCOVER, SPECIFY, PLAN, VERIFY, RELEASE |
| `connectors-and-platforms` | api-integration, reference-router, security-review | RESEARCH, SPECIFY, PLAN, IMPLEMENT, VERIFY, RELEASE |

The detailed intent catalogue includes business analysis, governance, finance,
private capital, product management, data engineering, analytics, software
engineering, AI and automation, design, documentation, artifacts and
connectors.

See [Capability Strength Map](docs/CAPABILITY_STRENGTH_MAP.md).

---

# Parallel and subagent execution

Parallel execution requires:

- genuinely independent tasks;
- separate files or non-conflicting state;
- explicit input and output contracts;
- bounded context;
- a named integration owner;
- merge order;
- whole-system verification after merge.

Use subagent-driven development for sequential tasks that benefit from fresh
contexts.

Use parallel agents only after the plan proves independence.

---

# Agent blueprint discovery

The 500+ AI Agent Projects repository is a discovery catalogue, not one
deployable runtime.

For every linked blueprint, Escapement checks:

```text
Exact repository
Licence
Maintenance
Runnable code
Framework and model dependencies
Tests and examples
Secrets and permissions
Data handling
Deployment model
Evaluation quality
```

Cloning, adapting or deploying still requires approval.

---

# Quick start

## Install

```bash
git clone https://github.com/SiddheshKGupta/escapement.git
cd escapement

python scripts/escapement.py init /path/to/your-product
```

Windows:

```powershell
py -3 scripts/escapement.py init C:\path\to\your-product
```

## Configure

Edit:

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
DOMAIN_CONTEXT.md
```

Safe starting state:

```yaml
project_name: My Product
profile: domain-expertise
phase: discovery
work_mode: FULL
implementation_authorized: false
approved_ticket: null
```

## Verify

```bash
python scripts/escapement.py doctor --root /path/to/your-product
```

## Start

```bash
python scripts/agent_runtime.py manual-start \
  --prompt "Build a controlled claims workflow" \
  --json
```

---

# Commands

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
python scripts/escapement.py security
python scripts/escapement.py view
python scripts/escapement.py component list
python scripts/escapement.py catalog search "<query>"
```

Runtime:

```text
python scripts/agent_runtime.py manual-start --prompt "<task>" --json
python scripts/agent_runtime.py advance-phase --phase <PHASE> ...
python scripts/agent_runtime.py status
python scripts/agent_runtime.py close-turn ...
python scripts/agent_runtime.py reset-turn --reason "<reason>"
```

---

# External capability registry

Escapement preserves external skills, plugins, tools, repositories, MCP
servers, services and references without claiming they are installed.

<details>
<summary><strong>View all 54 external resources</strong></summary>

| ID | Resource | Kind | Status | Overlap group |
|---|---|---|---|---|
| `voltagent-awesome-design-md` | [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | reference-repository | `catalogued` | `design-reference` |
| `perplexity-org` | [Perplexity AI GitHub organisation](https://github.com/perplexityai) | organisation-index | `catalogued` | `research-freshness` |
| `perplexity-api-platform-developers` | [api-platform-developers](https://github.com/perplexityai/api-platform-developers) | skills-and-plugin-repository | `catalogued` | `research-freshness` |
| `perplexity-cli` | [pplx CLI](https://github.com/perplexityai/perplexity-cli) | external-cli | `catalogued` | `research-freshness` |
| `perplexity-search-evals` | [search_evals](https://github.com/perplexityai/search_evals) | evaluation-framework | `catalogued` | `evaluation` |
| `perplexity-bumblebee` | [Bumblebee](https://github.com/perplexityai/bumblebee) | security-inventory-tool | `catalogued` | `security-testing` |
| `perplexity-modelcontextprotocol` | [Perplexity MCP server](https://github.com/perplexityai/modelcontextprotocol) | mcp-repository | `catalogued` | `research-freshness` |
| `perplexity-codescythe` | [Codescythe](https://github.com/perplexityai/codescythe) | code-analysis-tool | `catalogued` | `code-review` |
| `appflowy` | [AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) | product-repository | `catalogued` | `session-memory` |
| `plausible-analytics` | [Plausible Analytics](https://github.com/plausible/analytics) | product-repository | `catalogued` | `observability` |
| `github-spec-kit` | [Spec Kit](https://github.com/github/spec-kit) | specification-framework | `catalogued` | `harness-methodology` |
| `500-ai-agents-projects` | [500+ AI Agent Projects & Use Cases](https://github.com/ashishpatel26/500-AI-Agents-Projects) | agent-pattern-catalogue | `catalogued` | `agent-pattern-catalogue` |
| `walkinglabs-learn-harness-engineering` | [Learn Harness Engineering](https://walkinglabs.github.io/learn-harness-engineering/en/) | course-and-reference-repository | `catalogued` | `harness-methodology` |
| `walkinglabs-harness-creator` | [harness-creator skill](https://github.com/walkinglabs/learn-harness-engineering/tree/main/skills/harness-creator) | agent-skill | `catalogued` | `harness-methodology` |
| `penpot` | [Penpot](https://github.com/penpot/penpot) | design-platform | `catalogued` | `design-reference` |
| `helixdb` | [HelixDB](https://github.com/HelixDB/helix-db) | database-and-cli | `catalogued` | `session-memory` |
| `agent-reach` | [Agent Reach](https://github.com/Panniantong/agent-reach) | capability-installer | `catalogued` | `research-freshness` |
| `agent-browser` | [agent-browser](https://github.com/vercel-labs/agent-browser) | browser-automation-cli | `catalogued` | `browser-automation` |
| `gsd-core` | [GSD Core](https://github.com/gsd-build/get-shit-done) | context-and-phase-framework | `catalogued` | `harness-methodology` |
| `anthropic-mcp-builder` | [mcp-builder skill](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | agent-skill | `catalogued` | `mcp-building` |
| `vercel-find-skills` | [find-skills skill](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md) | agent-skill | `catalogued` | `external-discovery` |
| `ecc` | [ECC](https://github.com/affaan-m/ECC) | agent-harness-ecosystem | `catalogued` | `harness-methodology` |
| `strix` | [Strix](https://github.com/usestrix/strix) | security-testing-tool | `catalogued` | `security-testing` |
| `stop-slop` | [Stop Slop](https://github.com/hardikpandya/stop-slop) | agent-skill | `optional` | `writing-quality` |
| `task-observer` | [Task Observer](https://github.com/rebelytics/one-skill-to-rule-them-all) | meta-skill | `conditional` | `skill-learning` |
| `taste-skill` | [Taste Skill](https://github.com/Leonxlnx/taste-skill) | agent-skill-suite | `optional` | `design-director` |
| `open-design` | [Open Design](https://github.com/nexu-io/open-design) | design-platform-and-skill-suite | `optional` | `design-director` |
| `emil-kowalski-skill` | [Emil Kowalski Design Skills](https://github.com/emilkowalski/skills) | agent-skill-suite | `optional` | `motion` |
| `impeccable` | [Impeccable](https://github.com/pbakaus/impeccable) | agent-skill-and-cli | `optional` | `design-director` |
| `superpowers` | [Superpowers](https://github.com/obra/superpowers) | agent-methodology-plugin | `optional` | `harness-methodology` |
| `claude-mem` | [Claude Mem](https://github.com/thedotmack/claude-mem) | memory-plugin | `conditional` | `session-memory` |
| `graphify` | [Graphify](https://github.com/Graphify-Labs/graphify) | code-knowledge-skill-and-cli | `conditional` | `code-knowledge` |
| `gstack` | [gstack](https://github.com/garrytan/gstack) | agent-role-skill-suite | `optional` | `harness-methodology` |
| `everything-claude-code` | [Everything Claude Code / ECC](https://github.com/affaan-m/everything-claude-code) | harness-ecosystem | `optional` | `harness-methodology` |
| `context7` | [Context7](https://github.com/upstash/context7) | documentation-mcp | `optional` | `research-freshness` |
| `last30days` | [Last30Days](https://github.com/mvanhorn/last30days-skill) | research-skill | `optional` | `research-freshness` |
| `skill-ui` | Skill UI *(source unresolved)* | legacy-capability-reference | `preserved-unresolved` | `external-discovery` |
| `claude-code-review` | [Claude Code Review](https://code.claude.com/docs/en/code-review) | managed-code-review-service | `optional` | `code-review` |
| `ponytail` | [Ponytail](https://github.com/DietrichGebert/ponytail) | minimal-code-skill-and-plugin | `optional` | `engineering-minimalism` |
| `mobbin` | [Mobbin](https://mobbin.com) | commercial-design-reference | `reference-only` | `design-reference` |
| `refero` | [Refero](https://refero.design) | design-reference | `reference-only` | `design-reference` |
| `recent-designs` | [Recent](https://recent.design) | design-reference | `reference-only` | `design-reference` |
| `21st-dev` | [21st.dev](https://21st.dev) | component-reference-and-service | `optional` | `component-source` |
| `shadcn-ui` | [shadcn/ui](https://github.com/shadcn-ui/ui) | component-system | `optional` | `component-source` |
| `gsap` | [GSAP](https://github.com/greensock/GSAP) | motion-library | `optional` | `motion` |
| `headroom-js` | [Headroom.js](https://github.com/WickyNilliams/headroom.js) | interaction-library | `optional` | `motion` |
| `playwright` | [Playwright](https://github.com/microsoft/playwright) | browser-testing-framework | `preferred-when-existing` | `browser-automation` |
| `karpathy-guidelines` | [Andrej Karpathy Coding Guidelines](https://github.com/forrestchang/andrej-karpathy-skills) | behavioural-skill | `preferred-policy` | `engineering-behaviour` |
| `ui-ux-pro-max` | [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | design-intelligence-skill-and-cli | `optional-preferred-design-research` | `design-authority` |
| `frontend-design` | [Anthropic Frontend Design](https://github.com/openclaw/skills/tree/main/skills/qrucio/anthropic-frontend-design) | frontend-implementation-skill | `optional` | `design-authority` |
| `playwright-mcp` | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | browser-automation-mcp | `optional` | `browser-verification` |
| `stagehand` | [Stagehand](https://github.com/browserbase/stagehand) | ai-browser-automation-framework | `optional` | `browser-verification` |
| `cypress` | [Cypress](https://github.com/cypress-io/cypress) | browser-testing-framework | `preferred-when-existing` | `browser-verification` |
| `puppeteer-mcp` | [Puppeteer MCP Server](https://github.com/modelcontextprotocol/servers-archived) | legacy-browser-mcp | `discouraged-legacy` | `browser-verification` |

</details>

Before activation:

```text
Capability gap
→ Search registry
→ Check native fallback
→ Check strongest phase
→ Resolve overlap
→ Verify source and licence
→ Inspect hooks, network, permissions and credentials
→ Request approval
→ Pin version or commit
→ Record attribution
→ Validate
```

See [Reference Catalogue](docs/REFERENCE_CATALOG.md).

---

# Validation

The current repository has been validated through routing evaluations, unit
tests, runtime and repository doctors, security checks, native-skill
synchronisation, and a fresh-install lifecycle test.

```text
Routing evaluations:      22 / 22 PASS
Unit tests:               61 / 61 PASS
Runtime doctor:            0 failures
Repository doctor:         0 failures, 0 warnings
Security gate:             0 findings
Native skill sync:        35 / 35 PASS
Fresh-install self-test:  PASS
```

Run locally:

```bash
python scripts/eval_harness.py run
python -m unittest discover -s tests -p "test_*.py"
python scripts/agent_runtime.py doctor
python scripts/escapement.py self-test
python scripts/security_gate.py --fail-on high
```

These checks prove the framework's own code is healthy. For what the
governed lifecycle catches on an actual feature that a fast, ungoverned
implementation does not, see
[Case Study: Vanilla vs. Governed Implementation](reports/CASE_STUDY_vanilla_vs_governed.md).
For what it catches on a full `PROGRAM`-tier build with genuine parallel
subagent work, see
[Case Study: A Full PROGRAM-Tier Build](reports/CASE_STUDY_claims_platform_program_build.md).

---

# Project structure

```text
.
├── AGENTS.md
├── CLAUDE.md
├── PROJECT_STATE.yaml
├── PROJECT_CONTEXT.md
├── DOMAIN_CONTEXT.md
├── SESSION_HANDOFF.md
│
├── profiles/
├── docs/
│   ├── doctrine/
│   ├── standards/
│   │   └── design-intelligence.md
│   ├── architecture/
│   ├── specs/
│   └── decisions/
│
├── skills/
├── .agents/skills/
├── .claude/skills/
│
├── catalog/
│   ├── native-skills.json
│   ├── doctrine-packs.json
│   ├── skill-strengths.json
│   ├── capability-families.json
│   ├── design-stack.json
│   ├── strategy-adapters.json
│   ├── phase-capabilities.json
│   ├── capability-registry.json
│   ├── overlap-matrix.json
│   └── overlap-groups.json
│
├── scripts/
│   ├── capability_router.py
│   ├── capability_audit.py
│   ├── agent_runtime.py
│   ├── escapement.py
│   ├── run_check.py
│   └── eval_harness.py
└── tests/
```

---

# Licence

Escapement is source-available.

External capabilities retain their own licences. A registry entry does not
install a project or grant permission to copy it.

See:

- [LICENSE.md](LICENSE.md)
- [NOTICE.md](NOTICE.md)
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

---

<div align="center">

**Low automatic context. Deep capability. Explicit overlap. Verified delivery.**

</div>
