# Escapement

A repository-native governance harness for AI coding agents. The model reasons; Escapement controls how that capability is applied and what evidence a change must produce before it can be called done.

```text
Version              6.3.0
Python               3.10 | 3.12 | 3.13
Dependencies         none (standard library only)
Licence              Apache-2.0
```

## Install

```bash
git clone https://github.com/SiddheshKGupta/Escapement.git
cd Escapement
python scripts/escapement.py init /path/to/your-project
python scripts/escapement.py doctor --root /path/to/your-project
```

Installs into an existing repository. Managed files are tracked by hash; project-owned state is never overwritten. `update` reports conflicts instead of clobbering.

## Operating model

```text
Specify -> Route -> Execute -> Verify -> Persist
```

Expanded by the runtime into ten phases:

```text
ORIENT -> DISCOVER -> RESEARCH -> BRAINSTORM -> SPECIFY
-> PLAN -> IMPLEMENT -> VERIFY -> POLISH -> RELEASE
```

Phases are adaptive. Completed phases with evidence cannot be erased.

## Task tiers

Control scales with consequence, so small work stays small.

| Tier | Use | Treatment |
|---|---|---|
| `INFO` | explanation, navigation, status | no material runtime turn |
| `MICRO` | small bounded change | minimal context and capability loading |
| `MATERIAL` | feature or meaningful change | decision review, routing, evidence, durable closure |
| `PROGRAM` | product, module or transformation | full lifecycle, multi-turn governance, dependencies |

## Context budgets

Bounded, phase-specific context instead of one growing prompt.

```text
Kernel:                     <= 1,000 words
Automatic phase context:    <= 1,800 words
Invoked skill context:      <= 1,000 words
Doctrine packs:             <= 3 per phase
Native skills, MICRO:       <= 1
Native skills, MATERIAL:    <= 5
Native skills, PROGRAM:     <= 6
```

## Verification

```bash
python scripts/run_check.py   --name "unit-tests" --scope tests --   python -m unittest discover -s tests -p "test_*.py"
```

Writes a content-addressed record: command, scope, timing, exit code, result, output hashes.

`MATERIAL` and `PROGRAM` closure requires structured evidence. **A critical failed check cannot become `PASS`, and a model asserting success is not evidence.** Incomplete work stays `PARTIAL`.

## Commands

```bash
python scripts/escapement.py doctor --root .        # drift and integrity
python scripts/escapement.py explain "<task>"       # why this route
python scripts/escapement.py capability-audit "<task>" --markdown
python scripts/escapement.py catalog list --catalog skills
python scripts/escapement.py eval                   # routing evaluations
python scripts/escapement.py security --fail-on high
python scripts/escapement.py ablate <component>     # does it change behaviour?
python scripts/escapement.py observability --root . # closure, tiers, rejections
python scripts/escapement.py update <project> --apply
```

## Capability routing

Capabilities are catalogued with source, publisher, licence, licence status, activation mode, adoption requirement, overlap group, triggers and fallbacks. Catalogue status does not mean installed, active or approved.

Overlap is explicit — `SUBSTITUTE` capabilities are not stacked. Where a preferred external resource cannot be adopted, the router keeps an ordered fallback.

**Nothing in the registry is vendored into this repository.** Listing a resource is a routing decision, not incorporation.

## Current baseline

```text
Repository files:             289
Kernel:                       795 / 1000 words
Native skills:                35
Capability strengths:         58
Governed external resources:  67
Unit tests:                   196
Routing evaluations:          122
```

Recorded in [`manifest.json`](manifest.json). `doctor` recomputes these from the actual files and fails on drift; a measure the README stops stating produces a warning rather than passing silently.

## Hosts

| Host | State |
|---|---|
| Claude Code | deepest real-use evidence; runtime hooks and native skill packaging |
| Codex | hook packaging, bounded MICRO, escalation, App Server resource reads |
| Google Antigravity / Gemini | exercised; reads `AGENTS.md` natively |
| Gemini CLI | [`GEMINI.md`](GEMINI.md) bootstrap, tested |
| GitHub Copilot, others | bootstrap guidance only |

Equivalent behaviour is not assumed just because a host can read the instruction files. Host recommendations are checked against the repository before acting on them.

## Evidence position

Supported by current evidence:

- deterministic routing, capability selection, context-budget enforcement
- overlap and fallback behaviour, licence-aware adoption controls
- explicit lifecycle and PROGRAM state, structured evidence for closure
- install and drift validation
- real use on Claude Code, Antigravity/Gemini and Codex

**Not** established:

- statistical superiority over vanilla execution with the same model
- equivalent behaviour across every host
- universal token or cost reduction
- broad production adoption

`escapement-bench-v1` is 100 authored cases; the full routing corpus records 122/122. These test routing, not end-to-end task quality. See [`docs/decisions/ESCAPEMENT_BENCH_V1.md`](docs/decisions/ESCAPEMENT_BENCH_V1.md).

## Related repositories

```text
Escapement        this repository -- the stable line
Escapement Core   governed execution runtime; design phase, no implementation
Continuum         research programme; frozen, negative result
```

[Core](https://github.com/SiddheshKGupta/Escapement-Core) and [Continuum](https://github.com/SiddheshKGupta/Escapement-Continuum) are separate lines under different terms. Neither is a reason to defer adopting v1.

## Documentation

[`AGENTS.md`](AGENTS.md) · [`AGENT_RUNTIME.md`](AGENT_RUNTIME.md) · [`SECURITY.md`](SECURITY.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`docs/REFERENCE_CATALOG.md`](docs/REFERENCE_CATALOG.md) · [`docs/OVERLAP_ANALYSIS.md`](docs/OVERLAP_ANALYSIS.md) · [`reports/VALIDATION_v6.3.md`](reports/VALIDATION_v6.3.md)

## Licence

Apache-2.0 — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). Chosen over MIT for the explicit patent grant in section 3.

Third-party resources retain their own licences and adoption conditions; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Authorship

The idea, architecture, research direction and every material decision are **Siddhesh Gupta's**. AI agents were used as instruments inside that direction — implementing against a specification, running benchmarks, adversarial testing, triaging failures. They did not originate the concept or decide what the framework should become.

> Host feedback is evidence, not authority.
