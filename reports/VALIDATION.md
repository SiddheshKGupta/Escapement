# Escapement v6.0.0 Validation Report

Validated: 2026-08-05

## Results

| Check | Result |
|---|---|
| Python compilation | PASS — 8 scripts |
| Escapement doctor | PASS — 0 failures, 0 warnings |
| Native skill synchronisation | PASS — 10 skills |
| Feature-list validation | PASS |
| Router evaluations | PASS — 12/12 |
| Unit tests | PASS — 9/9 |
| Defensive security gate | PASS — 0 findings at time of packaging |
| Fresh installation | PASS |
| Fresh-install doctor | PASS |

## Scope

The tests cover safe installer/update behaviour, project-state preservation,
managed-file conflict handling, open-turn continuity, structured evidence,
critical-failure semantics, feature-state verification, reference-catalogue
quality, router behaviour, and fresh-install health.

## Not yet proven

This package has not been exercised inside every version of the Codex, Claude
Code, Cursor, Cline, or Roo Code host. Project hook approval and event payloads
should still be smoke-tested in each intended host before organisational
rollout. External integrations remain optional and require their own current
licence, security, credential, and compatibility review.
