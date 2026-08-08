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
