<div align="center">

# Escapement

### A governed execution harness for AI-assisted software delivery

[![Version](https://img.shields.io/badge/version-6.3.0-53284F?style=flat-square)](VERSION)
[![CI](https://github.com/SiddheshKGupta/Escapement/actions/workflows/validate-standard.yml/badge.svg)](https://github.com/SiddheshKGupta/Escapement/actions/workflows/validate-standard.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.12%20%7C%203.13-3776AB?style=flat-square&logo=python&logoColor=white)](.github/workflows/validate-standard.yml)
[![Kernel](https://img.shields.io/badge/kernel-795%20%2F%201000-2F855A?style=flat-square)](AGENTS.md)
[![Native skills](https://img.shields.io/badge/native%20skills-35-2F855A?style=flat-square)](catalog/native-skills.json)
[![Unit tests](https://img.shields.io/badge/unit%20tests-189%20passing-2F855A?style=flat-square)](manifest.json)
[![Routing evals](https://img.shields.io/badge/routing%20evals-122%20%2F%20122-2F855A?style=flat-square)](evals/)
[![Licence](https://img.shields.io/badge/licence-Apache--2.0-4A5568?style=flat-square)](LICENSE)

</div>

## What Escapement does

Escapement is a repository-native execution harness for coding agents.

It adds a governed delivery layer around the model so that decisions, context, capability selection, implementation, verification and project state are handled explicitly.

The model still does the reasoning and generation. Escapement governs how that capability is used.

Its core operating model is:

```text
Specify → Route → Execute → Verify → Persist
```

The runtime expands this into ten phases:

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

The phases are adaptive. Future phases can be added or removed where justified. Completed phases with evidence cannot be erased.

## Current baseline

| Measure | Current state |
|---|---:|
| Version | `6.3.0` |
| Repository files | `286` |
| Kernel | `795 / 1000 words` |
| Native skills | `35` |
| Capability strengths | `58` |
| Agent patterns | `21` |
| Governed external resources | `67` |
| Overlap groups | `14` |
| Published case studies | `4` |
| Unit tests | `189 / 189 PASS` |
| Routing evaluations | `122 / 122 PASS` |
| Repository doctor | `0 failures, 0 warnings` |
| Security gate | `0 findings` |

The baseline is recorded in [`manifest.json`](manifest.json).

The repository doctor also checks selected README and manifest counts against the actual repository state. Drift is treated as a validation failure.

## Task tiers

Escapement applies different levels of control based on task size and consequence.

| Tier | Use | Treatment |
|---|---|---|
| `INFO` | Explanation, navigation, status | No material runtime turn |
| `MICRO` | Small bounded change | Minimal context and capability loading |
| `MATERIAL` | Feature or meaningful change | Decision review, routing, evidence and durable closure |
| `PROGRAM` | Product, module or transformation | Full lifecycle, multi-turn governance and dependency management |

Small work stays small. Sensitive or high-impact work receives more control.

## Decision discipline

For `MATERIAL` and `PROGRAM` work, the runtime identifies the decision before implementation.

A decision brief can include:

- known facts;
- assumptions;
- unresolved questions;
- recommended defaults;
- consequences of alternatives;
- research requirements;
- phase plan;
- capability readiness.

Where a user is present, material questions should be answered explicitly rather than silently assumed.

> **Understand enough. Improve the decision. Build. Test. Prove. Persist.**

## Context management

Escapement uses bounded, phase-specific context instead of one growing prompt.

Persistent project context includes:

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
DOMAIN_CONTEXT.md
SESSION_HANDOFF.md
feature_list.json
```

Phase context can include:

- doctrine packs;
- native skills;
- capability strengths;
- agent patterns;
- governed external candidates;
- project and domain state.

Current limits:

| Context area | Limit |
|---|---:|
| Kernel | `<= 1,000 words` |
| Automatic phase context | `<= 1,800 words` |
| Invoked skill context | `<= 1,000 words` |
| Doctrine packs | `<= 3 per phase` |
| Native skills, MICRO | `<= 1` |
| Native skills, MATERIAL | `<= 5` |
| Native skills, PROGRAM | `<= 6` |

The goal is not fewer capabilities. It is the right capability at the right phase.

## Capability orchestration

Escapement separates what exists from what should be active now.

| Layer | Role |
|---|---|
| Kernel | Universal operating rules and authority |
| Profiles | Project or domain conventions |
| Doctrine packs | Phase-specific judgement |
| Native skills | Local execution procedures |
| Capability strengths | Specialist expertise |
| Strategy adapters | Bounded external methods |
| Agent patterns | Fresh-context or specialist execution patterns |
| External resources | Governed tools, services and repositories |
| Evidence | Verification records |
| Handoff | State for the next turn or module |

Overlap between capabilities is explicit.

Relations include:

```text
BASELINE_PLUS_INTENSIFIER
SUBSTITUTE
COMPLEMENTARY
SEQUENTIAL
REFERENCE_ONLY
META_OBSERVER
```

`SUBSTITUTE` capabilities are not stacked by default.

For external resources, the router can retain an ordered fallback when the preferred option cannot be adopted.

The repository doctor also checks for drift between resource `overlap_group` tags and the formal overlap definitions used by routing.

## External resources

Escapement currently catalogues **67 governed external resources**.

Catalogue status does not mean installed, active or approved.

Each resource can carry:

- source;
- publisher;
- licence;
- licence status;
- activation mode;
- adoption requirement;
- overlap group;
- routing triggers;
- intended use;
- limitations;
- fallbacks.

A candidate may require approval or licence review before adoption.

External capability is treated as input to a decision, not as automatic authority.

## Repository state

The repository is the system of record.

Escapement persists:

- decisions;
- lifecycle state;
- phase changes;
- domain evidence;
- implementation progress;
- module dependencies;
- shared artifacts;
- check evidence;
- deferred items;
- next actions.

For `PROGRAM` work, module state is maintained through `docs/PROGRAM_MODULES.json`.

Example:

```bash
python scripts/program_modules.py set-program --name "CRM Platform"

python scripts/program_modules.py add-module \
  --id billing \
  --name "Billing"

python scripts/program_modules.py add-module \
  --id portal \
  --name "Customer Portal" \
  --depends-on billing
```

For controlled testing, persisted PROGRAM state can be cleared with:

```bash
python scripts/program_modules.py reset --confirm
```

## Verification and closure

Verification is part of the runtime contract.

Checks can be executed through:

```bash
python scripts/run_check.py \
  --name "unit-tests" \
  --scope tests \
  -- \
  python -m unittest discover -s tests -p "test_*.py"
```

A check record can preserve:

- command;
- scope;
- timing;
- exit code;
- result;
- stdout and stderr references;
- hashes;
- record identity.

`MATERIAL` and `PROGRAM` closure requires structured evidence.

Critical failed checks cannot become `PASS`.

Incomplete work remains `PARTIAL` or failed.

The handoff records what was completed, verified, deferred and approved.

## Host support and conformance

Escapement distinguishes between a host reading instructions and the runtime actually operating as intended.

### Claude Code

Claude Code has the deepest accumulated real-use evidence.

Escapement provides automatic runtime hooks and native skill packaging for Claude Code.

### Google Antigravity with Gemini

Escapement has been exercised through Google Antigravity using Gemini.

The conformance review produced several recommendations. Each was checked against the repository before action.

One confirmed gap was implemented: a guarded CLI reset for persisted PROGRAM state.

Other findings were either already handled, based on a premise that did not match the implementation, or left as separate design decisions.

The operating principle is:

```text
Host observation
→ Source verification
→ Confirmed gap
→ Smallest appropriate change
→ Regression evidence
```

Antigravity reads `AGENTS.md` natively.

### Gemini CLI

Gemini CLI uses [`GEMINI.md`](GEMINI.md) as its bootstrap surface.

Escapement includes and tests this path explicitly.

### Codex

Codex integration includes:

- automatic hook packaging;
- bounded `MICRO` execution;
- sensitive-work escalation;
- recovery-state hydration;
- context accounting;
- capability-audit alignment;
- App Server rate-limit and usage reads;
- update-event handling;
- source-labelled persistence;
- five-hour window recognition;
- 75%, 90% and 100% resource thresholds;
- hook trust guidance.

Offline integration and policy behaviour have been tested.

Live quota and reset data remain environment-dependent. In the recorded Windows test environment, the Codex desktop executable could not be read because of an access-denied condition. Mocks and fixtures are not presented as live observations.

### Other hosts

Escapement includes bootstrap guidance for GitHub Copilot and other repository-aware agents.

Equivalent behaviour is not assumed simply because a host can read the instruction files.

## Host feedback

Host and model recommendations are reviewed against the repository before changing Escapement.

This applies to Claude, Codex, Gemini and any other agent environment.

> **Host feedback is evidence, not authority.**

## Benchmarking

Escapement separates three claims:

1. It behaves as designed.
2. It reduces known agent failure modes.
3. It improves outcomes versus vanilla execution using the same model.

The current deterministic benchmark addresses Claims 1 and 2.

`escapement-bench-v1` contains **100 authored cases**.

The full routing corpus currently records **122 / 122 PASS**.

Coverage includes:

- MICRO routing;
- ARTIFACT routing;
- material questions;
- motion routing;
- browser-verification substitution;
- engineering baseline and intensifier behaviour;
- agent-blueprint triggers;
- parallel assessment;
- overlap and fallback behaviour;
- licence and adoption controls.

Claim 3 requires paired live execution with the same task, model, host, tools and execution budget, with independent or externally defined grading.

Escapement does not use routing tests as evidence of end-to-end superiority.

See [`docs/decisions/ESCAPEMENT_BENCH_V1.md`](docs/decisions/ESCAPEMENT_BENCH_V1.md).

## Observability and ablation

Observability:

```bash
python scripts/escapement.py observability --root <target>
```

It can report:

- closure outcomes;
- task tiers;
- phase replans;
- selected but unused skills;
- context-budget rejection;
- overlap rejection.

Ablation tests whether a component changes behaviour visible to the current corpus:

```bash
python scripts/escapement.py ablate
python scripts/escapement.py ablate design-intelligence-constitution
python scripts/escapement.py ablate decision-coach
```

The ablation harness works on a temporary copy of the repository.

In an earlier 22-case corpus, removing `design-intelligence:constitution` reduced passing cases from `22/22` to `13/22`.

That shows the component was exercised by that corpus. A null result only shows that the corpus did not demonstrate a measurable effect.

No universal harness score is derived from these routing tests.

## Evidence from real use

Four case studies are published:

1. [Vanilla vs. Governed Implementation](reports/CASE_STUDY_vanilla_vs_governed.md)
2. [Full PROGRAM-Tier Claims Platform Build](reports/CASE_STUDY_claims_platform_program_build.md)
3. [Invoice Reconciliation PROGRAM Build](reports/CASE_STUDY_invoice_reconciliation_program_build.md)
4. [Four-Module CRM PROGRAM Build](reports/CASE_STUDY_crm_platform_multi_module_program.md)

Real use has led to changes in:

- PROGRAM sequencing;
- dependency control;
- integration verification;
- stale-runtime detection;
- UI quality checks;
- browser verification;
- context budgets;
- host bootstrap;
- external fallback chains;
- licence gating;
- Codex resource governance;
- count-drift detection;
- overlap metadata validation.

The repository uses "battle-tested" in this limited sense: exercised against real work and used to identify concrete gaps. It is not a claim of broad production adoption.

## Evidence position

Current evidence supports:

- deterministic routing and capability selection;
- context-budget enforcement;
- overlap and fallback behaviour;
- licence-aware adoption controls;
- explicit lifecycle and PROGRAM state;
- structured evidence for material closure;
- install and drift validation;
- real use on Claude Code, Google Antigravity with Gemini, and Codex.

Current evidence does not establish:

- statistical superiority over vanilla execution;
- equivalent behaviour across every host;
- universal token or cost reduction;
- broad production adoption;
- live Codex quota visibility in every environment;
- final task quality from routing tests alone.

## Quick start

Clone:

```bash
git clone https://github.com/SiddheshKGupta/Escapement.git
cd Escapement
```

Install:

```bash
python scripts/escapement.py init /path/to/your-project
```

Verify:

```bash
python scripts/escapement.py doctor --root .
```

Inspect capabilities:

```bash
python scripts/escapement.py catalog list --catalog skills
python scripts/escapement.py catalog list --catalog resources
python scripts/escapement.py catalog list --catalog patterns
```

Start a governed turn:

```bash
python scripts/agent_runtime.py manual-start \
  --prompt "Build a controlled claims workflow" \
  --json
```

Explain routing:

```bash
python scripts/escapement.py explain \
  "Build a controlled claims workflow"
```

Inspect readiness:

```bash
python scripts/escapement.py capability-audit \
  "Build a controlled claims workflow" \
  --markdown
```

## Update and repair

Preview an update:

```bash
python scripts/escapement.py update /path/to/project
```

Apply it:

```bash
python scripts/escapement.py update /path/to/project --apply
```

Repair managed files:

```bash
python scripts/escapement.py repair /path/to/project
```

Check drift:

```bash
python scripts/escapement.py doctor --root /path/to/project
```

Project-owned state is preserved. Modified managed files are reported as conflicts rather than overwritten silently.

## Current boundaries

Escapement v1 remains repository-native and evidence-led.

Current boundaries:

- external capability execution is host-dependent;
- live network research is host-dependent;
- real parallel-agent dispatch is host-dependent;
- strict per-skill evidence mapping remains future work;
- some Codex resource data remains environment-dependent;
- cross-host conformance is not yet equivalent across all environments.

## Escapement and Escapement-Continuum

Escapement v1 is the empirical baseline.

[Escapement-Continuum](https://github.com/SiddheshKGupta/Escapement-Continuum) is a separate research lineage exploring uncertainty-aware execution, strategy selection and delayed commitment. It was previously called *Quantum Escapement*; the name was changed because the metaphor caused engineering errors rather than only marketing confusion.

It is `0.1.0-alpha` research and has not validated its thesis. Its first experiment has been independently scored three times and has not yet passed. It is not a successor, not a replacement, and not a reason to defer adopting v1.

v1 remains the control against which later architecture can be evaluated.

> **v1 is evidence, not baggage.**

## Documentation

- [`AGENTS.md`](AGENTS.md)
- [`AGENT_RUNTIME.md`](AGENT_RUNTIME.md)
- [`SECURITY.md`](SECURITY.md)
- [`manifest.json`](manifest.json)
- [`GEMINI.md`](GEMINI.md)
- [`.codex/`](.codex/)
- [`docs/CAPABILITY_STRENGTH_MAP.md`](docs/CAPABILITY_STRENGTH_MAP.md)
- [`docs/OVERLAP_ANALYSIS.md`](docs/OVERLAP_ANALYSIS.md)
- [`docs/REFERENCE_CATALOG.md`](docs/REFERENCE_CATALOG.md)
- [`docs/decisions/ESCAPEMENT_BENCH_V1.md`](docs/decisions/ESCAPEMENT_BENCH_V1.md)
- [`reports/VALIDATION_v6.3.md`](reports/VALIDATION_v6.3.md)

## Licence

Escapement is licensed under the **Apache License 2.0** — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

Apache-2.0 was chosen over MIT for its explicit patent grant (§3), which matters for organisations adopting a governance harness.

Third-party resources retain their own licences and adoption conditions. Nothing in the capability registry is vendored into this repository; listing a resource is a routing decision, not incorporation. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

[Escapement Core](https://github.com/SiddheshKGupta/Escapement-Core) is a **separate repository under different, non-open-source terms**. Apache-2.0 covers this repository only.

## Authorship

The idea, architecture, research direction and every material decision in Escapement are **Siddhesh Gupta's**.

AI agents — Claude, Codex, Gemini and others — were used as instruments inside that direction. Their contribution was execution, not authorship: implementing against a specification, running trial and error, building and executing benchmarks, adversarial testing, triaging failures, and updating repository files where doing so improved the repository.

They did not originate the concept, choose the strategy, or decide what the framework should become. Where an agent's finding conflicted with the direction, the direction governed — which is the same rule the framework applies to host feedback:

> **Host feedback is evidence, not authority.**

That division is deliberate, and it is part of the thesis rather than a disclaimer attached to it. Escapement exists to make capable models useful under explicit human direction rather than autonomous. A framework making that claim should be built the same way it asks others to work.

<div align="center">

**Escapement**

Governed execution. Explicit evidence. Durable project state.

</div>
