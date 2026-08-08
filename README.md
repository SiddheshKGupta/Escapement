<div align="center">

# Escapement

### A governed, low-token execution harness for context-aware AI-assisted delivery.

Escapement surrounds AI coding agents with decision gates, bounded phase context,
capability orchestration, durable repository state, executable verification,
truthful closure, host-aware resource governance, and measurement of the harness itself.

[![Version](https://img.shields.io/badge/version-6.3.0-53284F?style=flat-square)](VERSION)
[![CI](https://github.com/SiddheshKGupta/Escapement/actions/workflows/validate-standard.yml/badge.svg)](https://github.com/SiddheshKGupta/Escapement/actions/workflows/validate-standard.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.12%20%7C%203.13-3776AB?style=flat-square&logo=python&logoColor=white)](.github/workflows/validate-standard.yml)
[![Kernel](https://img.shields.io/badge/kernel-795%20%2F%201000-2F855A?style=flat-square)](AGENTS.md)
[![Native skills](https://img.shields.io/badge/native%20skills-35-2F855A?style=flat-square)](catalog/native-skills.json)
[![Unit tests](https://img.shields.io/badge/unit%20tests-189%20passing-2F855A?style=flat-square)](manifest.json)
[![Routing evals](https://img.shields.io/badge/routing%20evals-122%20%2F%20122-2F855A?style=flat-square)](evals/)
[![Case studies](https://img.shields.io/badge/case%20studies-4-2F855A?style=flat-square)](#evidence-from-real-use)
[![Licence](https://img.shields.io/badge/licence-source--available-6B7280?style=flat-square)](LICENSE.md)

**Escapement does not upgrade the model. It upgrades how the model works.**

[60-second overview](#escapement-in-60-seconds) ·
[Quick start](#quick-start) ·
[How it works](#how-it-works) ·
[Capabilities](#capability-orchestration) ·
[Host evidence](#evidence-across-hosts) ·
[Evidence](#evidence-from-real-use) ·
[Validation](#current-validation)

</div>

---

# Escapement in 60 seconds

Capable AI agents can still make poor delivery decisions.

They can:

- assume instead of ask;
- load too much context;
- forget prior decisions;
- miss a specialist capability;
- stack overlapping tools;
- continue from stale project state;
- use external resources without a clear authority or licence boundary;
- declare work complete without executed evidence;
- lose consistency across long or multi-module builds.

Escapement is a repository-native execution harness designed to reduce those failure modes.

It is **more than an instruction file**.

The repository contains an executable runtime, capability router, bounded context
engine, lifecycle state, approval gates, project memory, evidence records,
PROGRAM dependency governance, observability, ablation testing, host bootstrap
logic, installation/update tooling, and deterministic validation of the harness itself.

## What changes when Escapement is active

| Without a governed delivery harness | Escapement mechanism |
|---|---|
| One growing context accumulates across the task | Fresh, bounded context is composed for the active phase |
| Material choices are silently assumed | High-impact questions are surfaced before implementation |
| Every instruction remains active all the time | Skills, doctrine, strengths and external candidates are routed by phase |
| Useful capabilities remain undiscovered | Capability audit and catalogue search surface relevant native and optional capabilities |
| Overlapping capabilities are stacked blindly | Overlap rules select a primary capability and retain governed fallbacks where useful |
| External tools become ambient authority | External candidates remain bounded by licence, overlap, security, installation and approval rules |
| Chat history becomes project memory | Decisions, phase history, evidence and next actions persist in the repository |
| Large builds drift between modules | PROGRAM state tracks modules, dependencies and shared artifacts |
| "Looks done" becomes "done" | Closure depends on executed checks and explicit `PASS`, `PARTIAL`, or failure semantics |
| Harness rules accumulate without proof | Observability, benchmarks and ablation test measurable behavior |
| Host output is treated as truth | Host findings are checked against the repository before Escapement changes itself |

## What is actually inside

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
    └── governed external candidates
    ↓
Execution
    ↓
Verification
    ↓
Evidence
    ↓
Truthful closure
    ↓
Durable handoff
```

## Current validated baseline

```text
Version:                   6.3.0
Repository files:          282
Kernel:                    795 / 1000 words
Profiles:                    2
Doctrine packs:             11
Native skills:              35
Capability strengths:       58
Agent patterns:             21
Governed external resources: 67
Strategy adapters:          10
Capability families:        10
Overlap groups:             14
Published case studies:      4
Unit tests:                 189
Routing evaluations:        122
Version:                      6.3.0
Repository files:             280
Kernel:                       795 / 1000 words
Profiles:                       2
Doctrine packs:                11
Native skills:                 35
Capability strengths:          58
Agent patterns:                21
Governed external resources:   67
Strategy adapters:             10
Capability families:           10
Overlap groups:                14
Published case studies:         4
Unit tests:                   186 / 186 PASS
Routing evaluations:          122 / 122 PASS
```

Escapement deliberately uses **more capabilities across the lifecycle, not more
context inside one prompt**.

---

# Why "Escapement"?

A mechanical escapement converts stored energy into controlled, measurable movement.

Escapement applies the same principle to AI-assisted delivery:

```text
Unbounded generation
        ↓
Specify → Route → Execute → Verify → Persist
        ↓
Controlled delivery
```

AI agents can generate quickly.

Reliable delivery also requires the system to know:

- what decision is actually being made;
- what information matters now;
- which capabilities should participate;
- what the agent is authorized to do;
- which external resources are adoptable;
- what must be verified;
- what evidence exists;
- what the next session should inherit.

---

# What Escapement is

Escapement is a **repository-native execution harness for AI-assisted delivery**.

It provides:

- a compact always-loaded kernel with an enforced word budget;
- runtime classification into `INFO`, `MICRO`, `MATERIAL`, and `PROGRAM`;
- a ten-phase delivery lifecycle with adaptive replanning;
- material-decision and clarification gates;
- phase-specific capability routing;
- 35 native executable skills;
- 58 specialist capability strengths;
- governed external capability discovery;
- capability overlap and fallback handling;
- licence-aware adoption controls;
- durable project and domain context;
- multi-session handoff;
- multi-module PROGRAM dependency governance;
- structured, content-addressed check evidence;
- explicit `PASS`, `PARTIAL`, and failure closure semantics;
- deterministic security and UI-quality gates;
- harness observability;
- deterministic benchmark suites;
- component ablation against a shared corpus;
- source-repository drift detection;
- safe install, update, repair and backup behavior;
- automatic runtime hook packaging for Claude Code and Codex;
- Gemini CLI bootstrap through `GEMINI.md`;
- native `AGENTS.md` bootstrap for Google Antigravity;
- host-agnostic bootstrap guidance for other repository-aware agents;
- Codex App Server resource reads and five-hour-window execution governance.

Escapement is **not**:

- a replacement for the underlying model;
- another coding agent;
- a guarantee of correct software;
- a giant prompt that loads every capability at once;
- an autonomous permission to deploy or modify production systems;
- a claim that every catalogued external resource is installed or approved;
- a substitute for regulation, standards, policy or qualified domain expertise;
- a claim that local evidence is equivalent to independently controlled CI;
- a universal provider abstraction;
- an MCP server today;
- a statistically proven claim that governed execution always beats vanilla execution;
- the adaptive research architecture described by Quantum Escapement.

---

# How it works

## 1. Task tiers

Escapement changes its level of ceremony according to the task.

| Tier | Intended use | Runtime expectation |
|---|---|---|
| `INFO` | Explanation, navigation or status | No material runtime turn |
| `MICRO` | Small bounded change | Compact context and minimal capability loading |
| `MATERIAL` | Feature or meaningful change | Decisions, phase routing, evidence and durable closure |
| `PROGRAM` | Product, module or transformation | Full lifecycle, broader orchestration and multi-turn governance |

A typo should not be governed like a platform build.

Low-risk `MICRO` work remains intentionally lightweight while sensitive or
irreversible work can still escalate.

---

## 2. Lifecycle

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

| Phase | Responsibility |
|---|---|
| `ORIENT` | Read repository state, constraints and active work |
| `DISCOVER` | Identify the real decision and resolve material unknowns |
| `RESEARCH` | Gather authoritative domain, technical or regulatory evidence |
| `BRAINSTORM` | Compare materially different approaches |
| `SPECIFY` | Define approved behavior, architecture, controls and acceptance criteria |
| `PLAN` | Create bounded implementation tasks, dependencies and verification |
| `IMPLEMENT` | Build through approved phase-relevant capabilities |
| `VERIFY` | Execute behavioral, integration, security and quality checks |
| `POLISH` | Improve usability and finishing quality where relevant |
| `RELEASE` | Apply readiness gates and produce a truthful handoff |

The lifecycle is adaptive rather than ceremonial.

```bash
python scripts/agent_runtime.py replan-phases \
  --add-phase VERIFY \
  --reason "Stored credentials require explicit security verification."
```

A replan:

- can use only registered lifecycle phases;
- cannot remove the current phase;
- cannot erase a phase already completed with evidence;
- requires a reason;
- is persisted in turn history.

---

# Better decisions before better code

For `MATERIAL` and `PROGRAM` work, Escapement expects the runtime to identify:

```text
Actual decision
Known facts
Material assumptions
High-impact unknowns
Recommended defaults
Consequences of choosing differently
Improved execution brief
Research requirement
Phase plan
Capability readiness
```

A user should not need to write a perfect prompt.

Escapement attempts to improve the decision before implementation begins.

When a user is present, material questions should receive real answers rather
than being silently self-resolved.

The kernel rule is:

> **Understand enough. Improve the decision. Build. Test. Prove. Persist.**

---

# Bounded context engineering

Escapement does not treat a large context window as permission to load everything.

```text
Always loaded
└── compact kernel

Project relevant
├── project state
├── project context
└── domain context

Phase relevant
├── doctrine packs
├── native skills
├── specialist strengths
├── fresh-context agents
└── governed external candidates

Persisted afterward
├── decisions
├── phase history
├── artifacts
├── evidence
└── next action
```

Current enforced limits include:

```text
Kernel:                    <= 1,000 words
Automatic phase context:  <= 1,800 words
Invoked skill context:    <= 1,000 words
Doctrine packs:           <= 3 per phase
Native skills:
  MICRO                    <= 1
  MATERIAL                 <= 5
  PROGRAM                  <= 6
```

The design principle is:

> **Use more capabilities across phases, not more capabilities inside one context.**

---

# Capability orchestration

Escapement separates:

```text
what exists
```

from:

```text
what should be active now
```

## Capability layers

| Layer | Purpose |
|---|---|
| Kernel | Universal delivery doctrine and authority |
| Profile | Project or domain conventions |
| Doctrine packs | Compact phase-specific judgement |
| Native skills | Executable local procedures |
| Capability strengths | Specialist expertise used where strongest |
| Strategy adapters | Bounded methods from compatible approaches |
| Fresh-context agents | Isolated work for justified subproblems |
| External resources | Governed tools, skills, services, MCP servers and repositories |
| Evidence | Executed checks and durable proof |
| Handoff | State passed to the next session or module |

## Overlap is explicit

Escapement does not load every matching capability.

Relationships can include:

```text
BASELINE_PLUS_INTENSIFIER
SUBSTITUTE
COMPLEMENTARY
SEQUENTIAL
REFERENCE_ONLY
META_OBSERVER
```

A `SUBSTITUTE` group selects one primary capability rather than stacking competing approaches.

For external resources, displaced candidates can be retained as ordered fallbacks:

```text
Preferred external candidate
        ↓
cannot install / licence blocks adoption / unsuitable
        ↓
governed fallback candidate
```

This prevents rediscovery from scratch while still avoiding capability stacking.

Escapement's repository doctor also checks for drift between each resource's
declared `overlap_group` and the formal overlap-group membership that actually
governs routing.

---

# Governed external capabilities

Escapement currently catalogues **67 governed external resources**.

A catalogue entry means:

```text
classified
    ≠
installed
    ≠
active
    ≠
authorized
```

Candidates can carry:

- source;
- publisher;
- licence;
- licence status;
- adoption gate;
- activation mode;
- trigger conditions;
- overlap group;
- `use_when`;
- `do_not`;
- fallback relationships;
- authority boundaries.

Some candidates can be adopted directly where compatible.

Others may surface as:

```text
ASK BEFORE ADOPTING
VERIFY LICENCE FIRST
DISCOVERY ONLY
REFERENCE ONLY
```

The catalogue is a governed discovery layer, not an ambient tool marketplace.

---

# Durable project state

The repository, not the chat transcript, is the system of record.

An installed project can maintain:

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
DOMAIN_CONTEXT.md
SESSION_HANDOFF.md
feature_list.json
docs/decisions/DECISION_LOG.md
docs/PROGRAM_MODULES.json
.agent/runtime/ACTIVE_CONTEXT.md
.agent/runtime/CONTEXT_PACK.md
.agent/runtime/SESSION_MEMORY.md
.agent/runtime/current-turn.json
.agent/runtime/turns.jsonl
```

These files can preserve:

- approved decisions;
- rejected alternatives;
- lifecycle state;
- phase-plan revisions;
- domain evidence;
- implementation progress;
- shared module dependencies;
- executed checks;
- risks and deferrals;
- exact next action.

---

# Evidence-backed closure

Escapement treats verification as part of the runtime contract.

A deterministic check can be executed through:

```bash
python scripts/run_check.py \
  --name "unit-tests" \
  --scope tests \
  -- \
  python -m unittest discover -s tests -p "test_*.py"
```

A structured check record can preserve:

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

Before evidence is accepted, the runtime can validate:

- required fields;
- referenced outputs;
- output hashes;
- successful result;
- record identity.

Closure rules include:

- critical failed checks cannot become `PASS`;
- `MATERIAL` and `PROGRAM` work require structured evidence;
- incomplete required work remains `PARTIAL` or failed;
- handoff states exactly what was built, checked, deferred and approved.

Escapement therefore attempts to distinguish:

```text
"The agent says it tested it"
```

from:

```text
"An executed check produced recorded evidence"
```

---

# Multi-module PROGRAMs

A PROGRAM may contain many modules and many turns.

Escapement maintains project-owned module state for:

- modules;
- dependencies;
- shared artifacts;
- status;
- cross-module consistency.

Example:

```bash
python scripts/program_modules.py set-program --name "CRM Platform"

python scripts/program_modules.py add-shared \
  --path docs/specs/SCHEMA.md

python scripts/program_modules.py add-module \
  --id billing \
  --name "Billing"

python scripts/program_modules.py add-module \
  --id portal \
  --name "Customer Portal" \
  --depends-on billing
```

A module cannot advance beyond specification without checking registered shared artifacts.

Declared incomplete dependencies block downstream advancement.

For iterative testing and conformance work, the registry can also be cleared
through a guarded CLI path:

```bash
python scripts/program_modules.py reset --confirm
```

The explicit `--confirm` is intentional: reset is destructive state mutation.

---

# Security and authority

Escapement gives reversible exploration more freedom than consequential actions.

Explicit approval is expected before operations such as:

- installing new dependencies;
- adopting external skills, plugins or MCP servers;
- using credentials;
- exposing confidential information;
- changing schemas or RBAC;
- destructive actions;
- production deployment;
- licence-sensitive reuse;
- security testing.

External information may inform reasoning.

It does not automatically acquire authority.

The same rule applies to host-generated recommendations:

> **Host feedback is evidence, not authority.**

A recommendation produced by Claude, Codex, Gemini, Antigravity or another host
is checked against the repository before Escapement changes itself.

---

# Evidence across hosts

Escapement is repository-native, but host integration is not assumed to be identical.

The project distinguishes:

```text
instructions are available
```

from:

```text
the runtime is actually active and behaving correctly
```

## Claude Code

Claude Code currently has the strongest accumulated real-use evidence.

Escapement provides automatic runtime hook packaging and native skill surfaces for
Claude Code, and much of the harness has been developed and exercised through it.

## Google Antigravity + Gemini

Escapement has been exercised directly through Google Antigravity using Gemini.

That host-conformance pass produced multiple recommendations. Escapement did not
accept them automatically.

Each was checked against the live source:

- a missing PROGRAM-registry reset path was confirmed and implemented;
- richer lifecycle errors were already present and therefore not duplicated;
- a proposed ablation-file change was based on a premise mismatch and was rejected;
- dependency-graph visualization was recognized as a real design question but not
  silently implemented as a small patch.

The confirmed reset gap became a guarded CLI capability with regression tests.

This demonstrates an important Escapement operating pattern:

```text
Different host/model
      ↓
Run real work
      ↓
Observe friction
      ↓
Host proposes findings
      ↓
Verify findings against source
      ↓
Accept real gaps
Reject false positives
Separate design decisions
      ↓
Implement smallest correct mechanism
      ↓
Add regression evidence
```

Antigravity reads `AGENTS.md` natively, so it does not require a separate pointer file.

## Gemini CLI

Gemini CLI uses `GEMINI.md` as its bootstrap surface.

Escapement includes and tests this bootstrap rather than assuming Gemini CLI will
discover the same repository instructions as another host.

## Codex

Codex support has moved beyond packaging-only integration.

Current Codex-specific work includes:

- automatic hook packaging;
- bounded low-risk `MICRO` behavior;
- escalation for sensitive work;
- truthful context accounting;
- durable recovery-state hydration;
- capability-audit alignment;
- Codex App Server rate-limit and usage reads;
- update-event handling;
- source-labelled persistence;
- explicit recognition of the 300-minute / five-hour window;
- conservative 75%, 90% and 100% resource thresholds;
- hook trust documentation;
- before/after compatibility evidence.

Escapement deliberately keeps **token activity** separate from **rate-limit enforcement**.

The evidence boundary is also explicit: offline integration and policy behavior
can be tested deterministically, while live account quota/reset information remains
environment-dependent. Fixtures and mocks are not labelled as live observations.

## GitHub Copilot and other repository-aware hosts

Escapement provides repository bootstrap guidance for hosts without automatic
runtime hooks.

That does not mean equivalent end-to-end conformance has been demonstrated on
every host.

The project avoids turning "can read the instructions" into a claim of
"validated behavioral equivalence."

---

# Evidence from real use

Escapement has been exercised through real repository builds, adversarial scenarios,
regression tests, multi-host conformance work and end-to-end delivery flows.

Four detailed case studies are currently published:

1. [Vanilla vs. Governed Implementation](reports/CASE_STUDY_vanilla_vs_governed.md)
2. [Full PROGRAM-Tier Claims Platform Build](reports/CASE_STUDY_claims_platform_program_build.md)
3. [Invoice Reconciliation PROGRAM Build](reports/CASE_STUDY_invoice_reconciliation_program_build.md)
4. [Four-Module CRM PROGRAM Build](reports/CASE_STUDY_crm_platform_multi_module_program.md)

Observed failures from real work have resulted in framework changes including:

- PROGRAM sequencing controls;
- dependency registration;
- guarded PROGRAM reset;
- integration verification;
- stale-runtime detection;
- deterministic UI-quality gates;
- baseline field validation;
- browser-level verification;
- context-budget enforcement;
- host-bootstrap requirements;
- external-capability fallback chains;
- licence-aware adoption gates;
- Codex resource-governance behavior;
- source-manifest/README count-drift detection;
- overlap-group tag drift detection.

The operating pattern is:

```text
Real build or conformance test
    ↓
Observed failure or gap
    ↓
Verify the finding
    ↓
Identify smallest correct harness layer
    ↓
Implement mechanism
    ↓
Add regression evidence
```

"Battle-tested" in this repository means repeatedly exercised and challenged
against real work.

It does **not** mean broad production adoption or statistical proof of superiority.

---

# What Escapement currently proves

Escapement currently has evidence for:

```text
✓ deterministic harness behavior
✓ routing and capability-selection behavior
✓ context-budget enforcement
✓ overlap resolution
✓ governed fallback behavior
✓ licence-aware adoption controls
✓ known failure-mode controls
✓ structured lifecycle behavior
✓ evidence-backed closure
✓ PROGRAM dependency behavior
✓ installation and drift behavior
✓ source-count consistency checks
✓ overlap metadata consistency checks
✓ deterministic regression testing
✓ harness-component ablation
✓ real Antigravity/Gemini conformance findings
✓ Codex offline compatibility and resource-governance behavior
```

Escapement does **not currently claim**:

```text
○ statistically demonstrated superiority over vanilla agents
○ equivalent behavior across every host
○ live Codex account quota observability in every environment
○ broad production-scale adoption
○ universal reduction in cost or token usage
○ that every catalogued capability improves outcomes
○ that deterministic routing tests measure final task quality
```

This distinction is intentional.

---

# Escapement Bench v1

Escapement Bench separates three different questions:

```text
Claim 1
Does Escapement behave as designed?

Claim 2
Does Escapement reduce known agent failure modes?

Claim 3
Does the same model produce better outcomes with
Escapement than without it?
```

The deterministic benchmark currently addresses Claims 1 and 2.

`escapement-bench-v1` now contains **100 deliberately authored cases**.

The full routing corpus currently contains **122 passing evaluations**.

The benchmark has been expanded by auditing previously untested router surfaces,
not simply by padding existing categories. Added coverage includes areas such as:

- MICRO behavior;
- ARTIFACT register routing;
- material-question coverage;
- motion routing;
- browser-verification substitution;
- engineering baseline/intensifier behavior;
- agent-blueprint triggers;
- parallel assessment;
- overlap/fallback behavior;
- licence/adoption behavior.

The benchmark also records authoring mistakes and unresolved findings rather than
silently tuning the router until every self-authored expectation passes.

Claim 3 requires a different experimental design:

```text
same task
same model
same host
same tools
same execution budget

Vanilla
    vs
Escapement-governed

independently graded outcome
```

Escapement does not treat deterministic routing tests as proof of end-to-end model superiority.

See:

[`docs/decisions/ESCAPEMENT_BENCH_V1.md`](docs/decisions/ESCAPEMENT_BENCH_V1.md)

---

# The harness measures itself

Escapement does not treat more doctrine as automatically better.

## Observability

```bash
python scripts/escapement.py observability --root <target>
```

Observability can report:

- closure-result distribution;
- task-tier distribution;
- phase replans;
- selected-but-unused skills;
- context-budget rejection;
- overlap rejection;
- routing behavior.

An empty report is not interpreted as proof of a healthy harness.

It may simply mean formal turns were not closed.

## Ablation

Escapement can ask:

> **Does this component change anything the current corpus can measure?**

```bash
python scripts/escapement.py ablate
python scripts/escapement.py ablate design-intelligence-constitution
python scripts/escapement.py ablate decision-coach
```

The ablation harness:

1. copies the repository to a throwaway workspace;
2. removes one declared component from that copy only;
3. executes the shared evaluation corpus;
4. compares control and ablated behavior;
5. reports factual differences.

Canonical source files are not modified.

In an earlier 22-case routing corpus, removing
`design-intelligence:constitution` reduced passing cases from `22/22` to `13/22`.

That historical result demonstrates that the component was exercised by that corpus.

A null result is interpreted differently:

> **No measurable difference means the current corpus did not exercise the component.
> It does not prove that the component is useless.**

Escapement deliberately does not manufacture a universal "harness score" from
deterministic routing tests.

---

# Source-of-truth drift detection

Escapement now checks some of its own public evidence claims.

The repository doctor computes live values for:

- tracked repository files;
- native skills;
- capability strengths;
- external resources;
- routing evaluations;
- unit tests.

Those values are compared against `manifest.json` and supported README inventory
patterns.

If the declared state drifts from the real repository state, doctor fails.

This exists because count drift happened repeatedly during rapid development.

The principle is simple:

> **Claimed state should be checked against actual state whenever it can be computed.**

The same doctor also detects stale `overlap_group` tags when a resource's display/audit
metadata no longer matches the formal overlap membership that governs routing.

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

Escapement separates framework-managed files from project-owned state.

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

## 4. Verify installation

```bash
python scripts/escapement.py doctor --root .
```

## 5. Inspect capabilities

```bash
python scripts/escapement.py catalog list --catalog skills
python scripts/escapement.py catalog list --catalog resources
python scripts/escapement.py catalog list --catalog patterns
python scripts/escapement.py catalog search "browser test"
```

Current catalogue:

```text
35 native skills
21 agent patterns
67 governed external resources
```

A catalogue entry is not an installation.

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

# Safe installation and updates

Escapement distinguishes:

| File class | Behavior |
|---|---|
| Framework-managed | Installed and updated by Escapement |
| Project-owned | Created as seeds and then preserved |
| Runtime-generated | Produced during work and retained as evidence/state |

Preview an update:

```bash
python scripts/escapement.py update /path/to/project
```

Apply safe framework updates:

```bash
python scripts/escapement.py update /path/to/project --apply
```

Repair missing framework files:

```bash
python scripts/escapement.py repair /path/to/project
```

Detect drift:

```bash
python scripts/escapement.py doctor --root /path/to/project
```

User-modified managed files are reported as conflicts rather than silently overwritten.

---

# Current validation

Current repository validation is recorded in [`manifest.json`](manifest.json).

```text
Version:                      6.3.0
Validated baseline:           2026-08-07

Routing evaluations:         122 / 122 PASS
Unit tests:                  189 / 189 PASS
Runtime doctor:               0 failures
Repository doctor:            0 failures, 0 warnings
Security gate:                0 findings
Unit tests:                  186 / 186 PASS

Runtime doctor:                0 failures
Repository doctor:             0 failures
Repository warnings:           0

Security gate:                 0 findings
Self-test:                    PASS
Fresh-install lifecycle:      PASS

Kernel:                       795 / 1000 words
Native skills:                 35
Capability strengths:          58
Governed external resources:   67
Repository files:             280
Published case studies:         4
```

Remaining boundaries include:

- external capability execution remains host-dependent;
- live network research remains host-dependent;
- real parallel-agent dispatch remains host-dependent;
- strict per-skill evidence mapping remains future work;
- some Codex live-account resource data remains environment-dependent.

---

# Escapement and Quantum Escapement

Escapement v1 and Quantum Escapement are separate lineages.

```text
ESCAPEMENT

Stable repository-native governed harness
        ↓
Real builds
Real failures
Real tests
Real routing evidence
Real lifecycle evidence
Real host-conformance evidence
Real ablation
        ↓
EMPIRICAL BASELINE
```

```text
QUANTUM ESCAPEMENT

Separate experimental research lineage
        ↓
Uncertainty-aware execution
Strategy ensembles
Value of Information
Delayed commitment
State coupling
State Memory Fabric
Adaptive execution strategy
        ↓
RESEARCH HYPOTHESIS
```

Escapement v1 remains the control and evidence base.

Quantum Escapement asks whether a more adaptive execution architecture can
outperform that baseline under controlled experiments.

> **v1 is evidence, not baggage.**

---

# Future direction

Escapement itself should remain stable, measurable and repository-native.

Future work may include:

- broader host conformance;
- live paired execution benchmarks;
- stronger cross-host equivalence tests;
- improved observability;
- stricter evidence attribution;
- richer context-health measurement;
- dependency-graph visualization for large PROGRAMs;
- additional governed capability evaluation;
- further compatibility improvements.

Escapement should not claim future capabilities before implementation and
validation support them.

---

# Documentation

Key references:

- [`AGENTS.md`](AGENTS.md) — Escapement kernel
- [`AGENT_RUNTIME.md`](AGENT_RUNTIME.md) — runtime behavior
- [`SECURITY.md`](SECURITY.md) — security boundaries
- [`manifest.json`](manifest.json) — current validated baseline
- [`GEMINI.md`](GEMINI.md) — Gemini CLI bootstrap
- [`.codex/`](.codex/) — Codex integration
- [`docs/CAPABILITY_STRENGTH_MAP.md`](docs/CAPABILITY_STRENGTH_MAP.md) — specialist capability map
- [`docs/OVERLAP_ANALYSIS.md`](docs/OVERLAP_ANALYSIS.md) — capability overlap
- [`docs/REFERENCE_CATALOG.md`](docs/REFERENCE_CATALOG.md) — governed external references
- [`docs/decisions/ESCAPEMENT_BENCH_V1.md`](docs/decisions/ESCAPEMENT_BENCH_V1.md) — benchmark design
- [`reports/VALIDATION_v6.3.md`](reports/VALIDATION_v6.3.md) — validation report

---

# Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Contributions should preserve Escapement's core discipline:

```text
Observed failure
      ↓
Verify the finding
      ↓
Smallest correct mechanism
      ↓
Implementation
      ↓
Regression evidence
      ↓
Keep, change or remove
```

New doctrine should not be added merely because it sounds useful.

Mechanisms should earn their complexity.

---

# Licence

Escapement is **source-available**, not OSI-approved open source.

The source may be used for evaluation, learning, non-commercial experimentation
and attributed internal use subject to [`LICENSE.md`](LICENSE.md).

Commercial redistribution, resale, white-labelling, hosted resale and substantial
republication require written permission.

Third-party resources retain their own licences and adoption restrictions.

See:

- [`LICENSE.md`](LICENSE.md)
- [`NOTICE.md`](NOTICE.md)
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)

---

<div align="center">

## Escapement

**Understand enough. Improve the decision. Build. Test. Prove. Persist.**

**Host feedback is evidence, not authority.**

**Escapement does not upgrade the model. It upgrades how the model works.**

</div>
