# Privacy and Observability

## Default posture

```text
Local
Minimal
Transparent
User-controlled
Exportable
No hidden telemetry
```

Escapement records only what is required to understand and verify the delivery
process.

## Local records

```text
.agent/runtime/
.agent/evidence/
.agent/evals/
.agent/runs/
.agent/security/
```

These directories are ignored by Git by default.

Shared continuation state is deliberately smaller:

```text
PROJECT_STATE.yaml
PROJECT_CONTEXT.md
feature_list.json
SESSION_HANDOFF.md
docs/specs/
docs/decisions/
```

## Prohibited telemetry

Escapement core must not:

- upload prompts, source code, or command output;
- collect user identity or cross-project tracking identifiers;
- use cookies or advertising identifiers;
- transmit runtime traces without explicit opt-in;
- hide analytics inside hooks;
- sell or share user data.

## Evidence hygiene

Before exporting a run:

1. inspect stdout and stderr;
2. redact secrets and personal data;
3. remove unnecessary source excerpts;
4. retain hashes and result metadata;
5. record who approved the export.

## Local viewer

The viewer must:

- bind to `127.0.0.1`;
- use an unguessable token;
- avoid external scripts, fonts, and analytics;
- read files directly from disk;
- stop when the process exits.

## Metrics

Useful local metrics include:

- open and closed turns;
- feature states;
- check pass/fail;
- retries;
- time to verified completion;
- context-pack size;
- skill selection and overlap;
- evaluation pass rate;
- security findings by severity.

Metrics should measure delivery behaviour, not individual surveillance.
