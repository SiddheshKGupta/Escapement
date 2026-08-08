# Codex Compatibility and Resource-Governance Validation

## Result

Escapement 6.3.0 now passes its offline Codex compatibility contract for bounded-task routing, truthful context accounting, durable recovery, phase-consistent capability audits, and Codex resource governance. This report records the remediation of the findings in `CODEX_HOST_CONFORMANCE_2026-08-08.md`.

## Implemented changes

| Area | Result |
| --- | --- |
| Bounded MICRO routing | Short, low-risk spelling and validation changes route as `MICRO`; sensitive consent, credential, patient, financial, biometric, and legal work remains escalated. |
| Context accounting | Runtime totals report the generated pack size, and long prompts are compacted so the active pack remains within the 1,800-word phase budget. |
| Capability audit | Every phase audit reroutes the actual user prompt with an explicit phase override, keeping direct and audit routing consistent. |
| Durable recovery | Runtime context hydrates the compact session handoff and program-module state when they are present. |
| App Server resources | `scripts/codex_resources.py` performs the JSONL handshake and supports `account/rateLimits/read`, `account/rateLimits/updated`, and `account/usage/read`. |
| Five-hour window | A primary window with `windowDurationMins: 300` is explicitly recognized as the five-hour limit. |
| Token accounting | Token activity is recorded separately from rate-limit enforcement; token counts alone do not block work. |
| Resource persistence | Source-labelled state is validated against `schemas/codex-resource-state.schema.json` and persisted under `.agent/runtime`. |
| Conservative policy | New material turns conserve at 75%, converge/checkpoint at 90%, and block at 100%; open turns may finish and verification is never weakened. Expired stale state cannot block. |
| Codex hooks | Documentation now states that project hooks require exact-hash review and trust through Codex `/hooks`; static hook files alone do not prove execution. |

## Verification evidence

The implementation branch was checked through the repository entry points:

```text
python scripts/escapement.py self-test
Earlier complete implementation run: PASS; 0 failures
Unit suite: PASS; 176 tests
Routing evaluation: PASS; 72/72
Fresh-install doctor: PASS

Repeat on the final evidence-only tree: TIMEOUT after 700 seconds
Failure output before timeout: none

python -m unittest tests.v6_3.test_domain_neutral_tier_and_gaps tests.v6_3.test_readiness_audit tests.v6_3.test_runtime tests.v6_3.test_codex_resources
Final focused result: PASS; 33 tests

python scripts/escapement.py eval
Final result: PASS; 72/72

python scripts/escapement.py doctor
Final result: PASS; 0 failures; 0 warnings

python scripts/escapement.py security
Final result: PASS; 0 findings

git diff --check
Result: PASS
```

The timeout is reported as inconclusive rather than as a pass or a failure. The final focused checks cover every changed executable path. Resource-governance coverage validates the five-hour window, update notifications, offline usage reads, source labels, persistence, threshold policy, expired-state behavior, and separation of token activity from blocking decisions.

## Evidence boundary

The implementation and offline integration layers pass. A live App Server read was attempted against the Codex desktop executable but returned Windows `Access denied` (`WinError 5`) in this host environment, so live account quota, usage, and reset values remain **NOT OBSERVABLE** in this run. No fixture or mock value is presented as live data.

Hook execution also requires a trusted project installation and must be retested from a new Codex task after approving the exact hook configuration hash. Turn steering and interruption are outside this remediation and remain unimplemented.

## Operational usage

```powershell
python scripts/escapement.py codex-resources read
python scripts/escapement.py codex-resources status
```

These commands expose the last supported resource observation and its policy decision without conflating token volume with the five-hour rate-limit window.

## Approved Codex Performance Design

Status: approved in principle on 2026-08-08; implementation remains gated on review of this persisted specification.

### Outcome

Make Escapement feel native, predictable, and fast inside Codex without changing the behavior of the shared Escapement engine or any Claude/Gemini integration. The Codex adapter may remove redundant work and irrelevant ceremony, but it may not weaken tiering, risk escalation, lifecycle state, verification, evidence, or resource governance.

### Scope and protected files

Implementation is restricted to these existing Codex-specific files:

- `.codex/hooks.json`
- `scripts/codex_resources.py`
- `tests/v6_3/test_codex_resources.py`
- `reports/CODEX_COMPATIBILITY_VALIDATION_2026-08-08.md`

The following shared or other-host files must remain byte-for-byte unchanged:

- `AGENTS.md`, `README.md`, `manifest.json`, `feature_list.json`, and `SESSION_HANDOFF.md`
- `scripts/capability_router.py`, `scripts/agent_runtime.py`, and `scripts/escapement.py`
- `CLAUDE.md` and `.claude/**`
- `GEMINI.md` and Gemini configuration

No new tracked file or counted unit-test method will be introduced, avoiding manifest and inventory drift.

### Architecture and data flow

```text
Codex project hook
  -> existing Codex adapter (`scripts/codex_resources.py`)
     -> install process-local read caches
     -> call the unchanged shared router/runtime
     -> apply bounded Codex normalization when eligible
     -> emit a compact Codex context pack
     -> persist the existing runtime/resource formats
```

The adapter remains a thin host boundary. It must not become a second lifecycle engine or a fork of Escapement policy.

### Fast-path eligibility

The fast path is eligible only when the prompt clearly concerns local repository engineering, runtime performance, or a local deterministic benchmark. It is ineligible when the prompt needs current external information or contains legal, regulatory, medical, financial, credential, privacy, biometric, security-sensitive, production-deployment, or other material-risk signals.

For an eligible prompt, the adapter may:

- cache immutable catalog/profile reads for the lifetime of the hook process;
- suppress external domain research caused only by an incomplete `DOMAIN_CONTEXT.md` or the generic word `benchmark`;
- remove generic user/industry questions that cannot change a local developer-tool refactor;
- remove a falsely selected `RESEARCH` phase and select the already-applicable local engineering phase;
- render a Codex context pack no larger than 600 words.

It may not:

- lower the shared router's tier;
- remove `VERIFY` or structured-check requirements;
- change rate-limit, token-telemetry, five-hour-window, stale-state, or open-turn policy;
- activate an external capability without approval;
- label fixture/mock resource data as live;
- change shared persisted schemas.

### Failure handling and rollback

Any adapter exception must fail open to the unchanged shared runtime path and emit a source-labelled diagnostic without exposing prompt contents or credentials. A Codex-only environment switch will disable the fast path for rollback while retaining the standard runtime. No background daemon, new dependency, network call, or persistent cache service is permitted in this phase.

Changing `.codex/hooks.json` changes its trust hash. Codex must require review and approval of the exact new hook configuration before automatic execution resumes.

### Benchmark contract

Current measured baseline for the representative Codex performance-refactor prompt:

| Measure | Baseline | Acceptance |
| --- | ---: | ---: |
| Hot `route_prompt` latency | 228 ms median; 381 ms p95 | p95 below 75 ms |
| Cold Codex prompt/preview path | shared control `escapement.py explain`: 1.68-2.91 s | adapter below 1.0 s |
| Codex capability-audit path | shared control: 6.0-6.9 s | adapter below 2.0 s |
| Generated context | 1,102 words | no more than 600 words |
| Persisted active context observed in this task | 1,302-1,505 words | no more than 600 words for eligible prompts |

The adapter will expose deterministic preview, audit, and benchmark commands from `scripts/codex_resources.py`. The protected shared `escapement.py` commands remain unchanged and serve only as control measurements. The benchmark will run enough iterations to report median and p95, compare the unchanged control path with the Codex fast path in the same environment, and test three semantic fixtures:

1. local runtime benchmark: fast path eligible, no external research;
2. current external benchmark: fast path ineligible, research preserved;
3. sensitive or regulated request: fast path ineligible, tier and verification preserved.

Performance passes only when all latency/context targets and all semantic guardrails pass. A faster result that weakens routing or verification is a failure.

### Verification and evidence

The existing Codex resource test module will be extended without adding a counted test method. Verification will include:

- protected-file hash comparison before and after implementation;
- existing Codex resource tests;
- fast-path eligibility and exclusion assertions;
- fallback-path assertion;
- hook JSON validation;
- focused security gate;
- benchmark output persisted in this report with environment and source labels.

### Recommended follow-on improvements

After this bounded phase proves stable, the next Codex-specific improvements should be evaluated separately:

1. a `codex doctor` preflight that reports hook trust, Python availability, runtime writability, App Server visibility, and latency-budget status;
2. per-stage timing telemetry that stores durations and outcome labels but not prompt bodies;
3. a new-task smoke test that proves trusted hooks execute automatically;
4. a compatibility matrix for Codex desktop/CLI and supported Python versions;
5. a compact degraded-mode message when live quota data or App Server access is unavailable.

These are recommendations, not part of the approved performance implementation, and require their own evidence before adoption.
