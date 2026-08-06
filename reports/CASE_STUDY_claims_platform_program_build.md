# Case Study: A Full PROGRAM-Tier Build, Two Real Bugs Found by the Process

Recorded: 2026-08-06

## Setup

A `PROGRAM`-tier request against `Claimline` (the same toy app from the
vanilla-vs-governed case study): *"Build a claims management platform ...
claims CRUD with a status workflow, RBAC for admin/adjuster/viewer, a KPI
dashboard, one external payout webhook integration, and a release
readiness checklist."* Driven through the real `agent_runtime.py` CLI --
`manual-start`, all ten phases, real skill routing, real `run_check.py`
evidence, genuine parallel subagent dispatch, closed with an honest
`PARTIAL`, not a rubber-stamped `PASS`.

## What the lifecycle actually produced

`DISCOVER` surfaced two material questions (regulatory context,
approval/segregation-of-duties) and, through genuine repository inspection
rather than assumption, the fact that the existing credential was stored in
plaintext -- a real constraint the request never mentioned. `BRAINSTORM`
compared three architectures and gave a reason for the one chosen.
`SPECIFY` produced a durable spec with 8 testable acceptance criteria.
`PLAN` made a real, justified parallel-dispatch decision (below). `VERIFY`
found and fixed two bugs neither module's own tests had caught (below).
`RELEASE` refused to call the result production-ready, and said why.

**Caveat on method, same as the previous case study:** one agent, one
session -- not independent parties, not a statistical sample.

## The parallel-dispatch decision, and why it was justified rather than performative

`models.py` (the claim record and status machine) was built first,
sequentially -- everything else reads its shape. Once it existed,
`permissions.py` (RBAC) and `dashboard.py` (KPI computation) were
genuinely independent: separate files, no shared mutable state, each with
an explicit contract from the spec's own tables, no ordering dependency
between them. Both were dispatched as parallel subagents against that
shared interface. `webhook.py` stayed sequential, since it needed
`permissions.py`'s actual interface once it existed, not an assumed one.

Both subagents returned real, independently verified work: 15 and 3 tests
respectively, all genuinely executed. This is the concrete criteria from
`AGENTS.md`'s "Agents and Parallel Work" section applied, not merely
invoked because the tool exists.

## Bug 1: a cross-module KPI bug neither module's own tests caught

`CLOSED` is reachable from both `APPROVED` (a claim that was paid, then
closed) and `REJECTED` (a claim that was denied, then closed). `status`
alone cannot tell these apart. `dashboard.py`'s `recovery_rate()` computed
over `{APPROVED, PAID, CLOSED}` -- which silently included rejected claims
that happened to reach the same terminal status a genuinely-approved claim
can reach, diluting the metric:

```text
A claim rejected outright (claimed 1000, recovered 0), then closed.
A claim genuinely paid out in full (claimed 500, recovered 500).

Reported recovery rate: 33% (500 / 1500 -- the rejected claim's
claimed_amount counted against a metric it was never eligible for)
Correct recovery rate: 100% (500 / 500 -- only the genuinely
approved claim should count)
```

Neither `permissions.py`'s nor `dashboard.py`'s own test suite exercised
this specific cross-status-path scenario -- each module's tests were
internally consistent and passed. It surfaced only because the integration
owner (this session) deliberately traced an edge case neither subagent had
reason to anticipate in isolation. Fixed at the source: `models.py` gained
an explicit `was_approved` flag, set the moment a claim first reaches
`APPROVED`, so `recovery_rate()` no longer has to infer intent from a
terminal status two different paths can produce.

## Bug 2: a real, generalizable framework bug, found using the framework on itself

Running the security gate as a genuine `VERIFY`-phase check (not a
dedicated bug hunt) produced a `HIGH` finding inside
`.escapement/backups/<timestamp>/scripts/security_gate.py` -- a backup
created by an earlier `update --apply` in this same session. The gate's
own `powershell-download-exec` detection pattern is stored as literal
regex source text inside `security_gate.py`; a backup copy of that file
matches its own pattern. This is not a one-off: it fires on every backup
of `security_gate.py` ever created, in every project that has run
`update`/`repair`, and `--fail-on high` treats it as blocking. Reported and
fixed upstream in the escapement repository itself
([PR #14](https://github.com/SiddheshKGupta/escapement/pull/14)), not just
patched locally.

## The honest release verdict

`release-readiness`'s gates were applied for real, not rubber-stamped:

| Gate | Verdict |
|---|---|
| Acceptance complete | Yes -- 8/8 |
| Structured checks pass | Yes -- 40/40, security gate clean |
| Security and permissions reviewed | Yes -- RBAC and maker-checker independently tested at both the role and identity layers |
| Persistence, monitoring, human approval | **No** -- in-memory store only, no real webhook endpoint ever exercised, no approver available in this session |

**Closed as `PARTIAL`, not `PASS`.** The workflow, RBAC, and KPI logic are
genuinely implemented and verified -- not a stub -- but calling this
release-ready would be exactly the false confidence this framework exists
to prevent. A green test suite is not production evidence when the
persistence layer and human sign-off are openly missing, not silently
assumed away.

## What this demonstrates that the first case study didn't

The vanilla-vs-governed study showed the gap between doing work with and
without governance. This one shows what governance catches *within
itself* under real, non-trivial conditions: parallel work integrated
correctly because someone was accountable for the seam between two
subagents' otherwise-correct outputs, and the framework's own tooling was
verified with the same scrutiny applied to the feature it was checking --
not exempted because it's infrastructure rather than product code.
