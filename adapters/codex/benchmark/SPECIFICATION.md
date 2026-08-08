# Escapement Codex Benchmark v2 Specification

- Status: Approved direction; implementation pending
- Version: 0.1.0
- Baseline commit: `f0e6991`
- Primary owner and final decision-maker: repository owner
- Primary users: Escapement maintainers and Codex users evaluating governed delivery

## Outcome

Produce reproducible evidence about whether the same Codex configuration completes
representative software-delivery tasks more reliably with the Escapement Codex
adapter than without it. The benchmark must also expose Codex-specific defects
without changing shared Escapement behavior or the Claude and Gemini integrations.

Success means:

1. deterministic preflight and simulated resource scenarios are reproducible;
2. the 128-run confirmatory design can be executed from frozen fixtures;
3. every scored result is traceable to immutable raw evidence;
4. vanilla and Escapement lanes differ only by the pinned Codex adapter;
5. no benchmark implementation change touches protected repository surfaces;
6. reproducible Codex-only defects receive a regression test before repair.

## Scope

### Launch scope

- Codex-only adapter benchmark under `adapters/codex/benchmark/`.
- Existing 122 routing evaluations and Codex resource contracts as preflight.
- Twelve simulated App Server resource-window scenarios.
- Sixteen-run live shakedown excluded from confirmatory inference.
- One-hundred-and-twenty-eight-run paired confirmatory study.
- Optional thirty-two-run live ablation study reported separately.
- Append-only evidence, deterministic hidden grading, and generated summaries.
- Parallel repair of reproducible Codex-adapter or benchmark defects.

### Non-goals

- Changing Escapement's shared runtime, router, skill catalogue, or doctrine.
- Modifying Claude, Gemini, or host-agnostic integration files.
- Rewriting historical reports or benchmark v1 evidence.
- Intentionally exhausting a live Codex quota window.
- Claiming that simulated resource fixtures are live account observations.
- Claiming universal superiority from this repository-sized study.
- Using an LLM judge to override deterministic failures.

## Protected-file contract

Benchmark construction is additive. The following remain unchanged:

- `AGENTS.md`, `AGENT_RUNTIME.md`, `README.md`, `SESSION_HANDOFF.md`;
- `manifest.json`, `feature_list.json`, `DOMAIN_CONTEXT.md`;
- `scripts/agent_runtime.py`, `scripts/capability_router.py`, `scripts/escapement.py`;
- `catalog/**`, `profiles/**`, `skills/**`, `.agents/skills/**`;
- `CLAUDE.md`, `.claude/**`, `.claude-plugin/**`;
- `GEMINI.md` and Gemini-specific configuration;
- existing `evals/**`, schemas, tests, historical reports, and benchmark-v1 decisions;
- existing `.codex/**`, `.codex-plugin/**`, and `scripts/codex_resources.py`, unless a
  separately reviewed Codex-only defect owns the change.

The benchmark preflight records hashes for protected paths and fails if a benchmark
run changes them.

## Experimental design

### Stages

1. **Deterministic preflight** — execute the existing 122 routing cases, focused
   Codex resource contracts, schema validation, and protected-file hashing.
2. **Simulated resources** — execute 12 labelled fixture scenarios. These are never
   counted as live observations.
3. **Live shakedown** — 4 workloads × 2 lanes × 2 repetitions = 16 runs. Use this
   only to validate fixtures, graders, isolation, and evidence capture.
4. **Freeze** — pin prompt, fixture, public-contract, hidden-grader, adapter, model,
   host-setting, schedule, and scoring hashes.
5. **Confirmatory study** — 16 workloads × 2 lanes × 4 fresh repetitions = 128 runs.
6. **Optional ablation** — 8 workloads × full/ablated Escapement × 2 repetitions =
   32 exploratory runs, never pooled with the confirmatory comparison.

### Lanes

- `VANILLA_CODEX`: neutral task fixture without the Escapement adapter.
- `ESCAPEMENT_CODEX`: identical configuration with only the pinned Codex adapter.

The runner must hold constant the account cohort, model, reasoning setting, host version, prompt,
fixture, tools, permissions, network policy, time limit, and hidden grader. If a
comparability-critical setting is unavailable or equality cannot be established,
exclude the pair from primary analysis; never infer it.

Each workload/repetition is a paired block. Every workload has two `AB` and two `BA`
orders in a precommitted schedule. Use a fresh Codex task, session, process, and
materialization for every run, with no inherited messages, steering, memory, Git
state, caches, results, or `.agent` state. Live blocks run serially with no other
Codex activity on the same account. Concurrent repair work must be offline or use a
separate recorded account.

### Treatment manifest

Before freeze, generate and sign an adapter manifest that lists every treatment file,
content hash, target path, and activation step. The Escapement lane consists only of
that manifest: root `AGENTS.md`, the pinned runtime and router dependencies, canonical
skills installed as `.agents/skills`, Codex hooks, generated phase context, and the
Codex resource-policy adapter. The vanilla lane receives the same neutral fixture but
none of those files or activation steps. Any treatment-manifest change creates a new
benchmark version.

## Workload catalogue

| ID | Workload | Critical hidden behavior |
|---|---|---|
| W01 | Bounded user-facing typo | Exact intended change; no collateral files |
| W02 | Blank-username validation | Valid, blank, whitespace, null, boundary cases |
| W03 | Pagination off-by-one | First, middle, final, and empty pages |
| W04 | Quoted CSV parser | Delimiters, quotes, malformed input, encoding |
| W05 | Idempotent webhook retry | Duplicate, timeout, retry, exactly-once effect |
| W06 | RBAC permission leak | Positive and negative role/permission matrix |
| W07 | Sensitive-data log redaction | Required redaction without destructive over-redaction |
| W08 | Reversible schema migration | Forward/backward compatibility and row preservation |
| W09 | Reconciliation engine | Duplicates, precision, unmatched records |
| W10 | Approval state machine | Invalid transitions, maker-checker, recovery |
| W11 | Performance regression | Correctness plus fixed median/p95 workload |
| W12 | Keyboard/focus accessibility | Tab order, focus restoration, activation semantics |
| W13 | API contract evolution | Backward compatibility and error contract |
| W14 | Multi-file refactor | Behavioral equivalence and scope discipline |
| W15 | Interrupted-task recovery | Handoff discovery, no repeated work, exact next action |
| W16 | PROGRAM first slice | Dependency/shared-artifact gates and truthful closure |

Every task must be locally solvable without network access or a new dependency.

## Resource-window scenarios

The deterministic resource suite covers:

1. 0%;
2. 74.9%;
3. 75%;
4. 89.9%;
5. 90%;
6. 99.9%;
7. 100%;
8. expired/stale window;
9. no observable window;
10. update notification;
11. high token activity with normal quota;
12. competing primary and secondary windows.

Primary live confirmatory blocks require a fresh, live, source-labelled resource read
and start only below 70% of the governing five-hour window.
At 75% no new block starts; at 90% checkpoint; at 100% block. If a paired block
crosses a policy band or reset boundary, exclude it from primary analysis and rerun
both lanes after reset. `NOT_OBSERVABLE` resource state permits only a separately
predeclared secondary cohort and can never enter the primary analysis. The benchmark
never deliberately burns quota to reach a threshold.

The simulated scenario file supplies a fixed clock, source label, raw window payload,
and expected `mode`, `action`, `block_new_turn`, `needs_refresh`, governing-window
identity, and five-hour classification for every case.

## Run lifecycle and statuses

`lifecycle_status` is one of `PLANNED`, `MATERIALIZED`, `RUNNING`, `CAPTURED`,
`GRADED`, `INCLUDED`, `EXCLUDED`, or `INFRA_ERROR`. `task_outcome` is independently
one of `PASS`, `FAIL`, `PARTIAL`, `TIMEOUT`, `INTERRUPTED`, or `NOT_GRADED`.
Allowed combinations and transitions are schema-enforced.

`INFRA_ERROR` and predeclared exclusions are not scored. At most one controller-only
retry is permitted for a pair under identical frozen hashes. Every attempt remains in
the event log and attrition is reported by lane and reason. Task timeout, interruption,
or incomplete work is a scored failure. Every workload declares acceptable closure
outcomes; W16 requires `PASS`, while a truthful `PARTIAL` may retain truthfulness
points but remains a binary failure.

## Evidence contract

Raw evidence is append-only NDJSON plus content-addressed per-run artifacts under
`.agent/evals/codex-bench-v2/<run-id>/`. Summary reports are generated from those
records and are never hand-edited as the source of truth.

Each event has a globally unique event ID, run ID, monotonically increasing sequence,
previous-event hash, and content hash. A run may have exactly one terminal event.
Aggregation deduplicates by event ID, rejects divergent duplicate sequence numbers,
and includes only the latest valid hash chain ending in a terminal event.

Each run records:

- schema/benchmark version, run ID, workload, lane, repetition, pair, and order;
- repository, fixture, adapter, prompt, public-contract, and grader-bundle hashes;
- host, model, reasoning setting, permissions, network, and timeout policy;
- start/end timestamps, duration, termination reason, and exclusion reason;
- source-labelled pre/post resource snapshots and governing policy band;
- commands, exit codes, durations, retries, tool events, and redactions;
- patch and untracked-artifact hashes, final response, and closure claim;
- hidden checks, criticality, actual result, and evidence pointer;
- binary success, rubric components, efficiency measures, and grader version.

Hidden graders are supplied externally through `--grader-bundle`; the supplied hash
must equal the frozen hash before execution. The bundle path and related environment
variables are not passed to the agent child process. Hidden graders are never placed
in the agent workspace. Grading occurs after agent termination, and lane blinding is
mandatory for any subjective review.

## Grading and analysis

Primary binary success requires all critical hidden checks, no permission or
protected-scope violation, required artifacts, and a closure claim consistent with
evidence. A critical failure or fabricated `PASS` makes the run unsuccessful and
caps its diagnostic score below 50.

The primary estimand is the mean, across 16 workloads, of the Escapement-minus-vanilla
difference in four-run success rate. The one-sided superiority hypothesis is
`H0: delta <= 0` versus `H1: delta > 0` at alpha 0.05, tested with an exact
workload-cluster sign-flip randomization test over all `2^16` assignments. The minimum
practically relevant effect is 0.15. Before freeze, a seeded simulation must report
power for that effect; below 80% power the study is labelled exploratory or expanded
before execution. Missing pairs are not imputed in the primary analysis. A sensitivity
analysis treats missing outcomes once as lane failures and once as lane successes.

Diagnostic score:

| Dimension | Points |
|---|---:|
| Correctness | 50 |
| Requirement coverage | 20 |
| Non-regression and scope discipline | 10 |
| Evidence truthfulness | 10 |
| Task-specific controls or quality | 10 |

Efficiency remains separate: wall time, median/p95 latency, tool calls, command
retries, context words, patch size, and token activity. Token activity is never
reported as tokens remaining.

Every workload provides machine-readable rubric anchors, scoring rules, criticality,
and missing/not-applicable handling so independent deterministic graders agree.

Report per lane:

- execution success rate over 64 runs;
- workloads with at least one of four successful repetitions;
- workloads successful in all four repetitions;
- the primary exact cluster randomization result;
- a descriptive paired McNemar result, explicitly not used for inference;
- workload-clustered percentile-bootstrap intervals using 10,000 draws, workload as
  the resampling unit, and fixed seed `20260808` for score and efficiency deltas;
- complete-pair, attrition, and missing-outcome sensitivity results.

Efficiency is normalized within workload as a paired lane delta. No per-workload p95
is reported from four repetitions; pooled percentiles are labelled as workload-mix
descriptions rather than treatment estimates. The 16-cluster sample limitation is
stated prominently.

## Parallel defect-repair protocol

1. Reproduce against the pinned clean baseline.
2. Classify as Codex adapter, benchmark, shared, Claude, Gemini, historical evidence,
   environment, or false positive.
3. Repair only Codex-adapter or benchmark defects within an explicitly owned file set.
4. Add a failing regression test before changing implementation.
5. Apply the smallest fix and run the focused check plus protected-file verification.
6. Keep repairs in a separate commit from benchmark capability work.
7. Record protected-surface defects without editing them.
8. A treatment, prompt, fixture, grader, schedule, or scoring change after freeze creates
   a new benchmark version and restarts all 128 confirmatory runs. Only controller-only
   infrastructure failure under identical frozen hashes may rerun a pair.

## Launch acceptance criteria

1. All new benchmark tests pass from a clean checkout.
2. The runner validates configuration and emits a deterministic schedule without
   launching Codex unless `--execute-live` is explicitly provided.
3. Dry-run mode materializes isolated fixtures and never exposes hidden graders.
4. Schema validation rejects missing hashes, invalid status transitions, unsupported
   lanes, ambiguous resource sources, and simulated data labelled as live.
5. Aggregation distinguishes scored failures, timeouts, exclusions, infrastructure
   errors, and `NOT_OBSERVABLE` fields.
6. Protected-file preflight fails on any changed protected path.
7. Simulated resource thresholds behave exactly at 75%, 90%, and 100%.
8. A run interrupted during capture can resume without duplicating a scored record or
   accepting a broken event hash chain.
9. No live quota is consumed by unit tests, dry runs, or simulated scenarios.
10. No shared, Claude, Gemini, existing Codex integration, or historical evidence file
    is changed by benchmark implementation.
11. W11 uses three warm-ups and ten timed iterations on the same recorded machine;
    its deterministic workload must have coefficient of variation at most 10%, and a
    regression fails at a paired median slowdown above 20%.
12. W15 exposes immutable stage markers and mutation IDs; repeated work means repeating
    a completed mutation or rerunning a completed destructive stage.
13. W16 declares exact required slice artifacts and succeeds only with a truthful
    `PASS`; truthful `PARTIAL` is retained as diagnostic evidence but fails binary success.

## Optional ablation definition

The v2 optional ablation removes only `decision-coach` from the frozen Escapement
treatment manifest. Its predeclared expectation is reduced decision-question and
requirement-coverage performance. Workloads W05, W06, W08, W09, W10, W13, W15, and
W16 are selected before execution because their fixtures contain material decision or
control ambiguity. The ablation mechanism and selection cannot change after freeze.

## Later options

- Cross-host Claude/Gemini comparison after the Codex study stabilizes.
- Thin generated Codex distribution repository after benchmark evidence demonstrates
  an independent release or maintenance need.
- Broader model matrix and external independent reproduction.
- Optional LLM-based qualitative review reported only as secondary evidence.
