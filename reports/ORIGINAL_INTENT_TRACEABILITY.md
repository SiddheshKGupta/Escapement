# Original Intent Traceability — Escapement v6.3

Validated: 2026-08-05

## Purpose

Trace the repository from the original intent through the current architecture
and verify the system as a real installed project rather than only as isolated
router tests.

## Original intent and current status

| Original intent | Current implementation | Real-time result | Status |
|---|---|---|---|
| Low-token system | 644-word kernel; separate 1,800-word automatic and 1,200-word invoked-skill budgets | Live PROGRAM route used 1,709 automatic words and 461 invoked-skill words at DISCOVER | Proven |
| Agent should remember across turns | Open turn, phase history, active context, session memory and handoff files | One turn advanced across eight recorded phase completions and closed truthfully | Proven |
| Agent should ask the right questions | Decision Coach produces no more than five material questions with defaults and consequences | Live platform request produced two material questions and an improved execution prompt | Proven |
| Help the user make better decisions | Decision brief, domain research, brainstorming, specification and decision log | Modular controlled platform selected over microservices-first and autonomous-agent-first alternatives | Proven |
| Use domain expertise without organisation branding | `DOMAIN_CONTEXT.md`, domain-neutral profile and authoritative evidence ladder | Fresh project persisted regulated financial-services context and control assumptions | Proven |
| Suggest standards and current trends | Research plan routes primary web first, then Context7, Agent Reach or Last30Days when relevant | Router selected authoritative research plus Agent Reach and agent-blueprint discovery | Routing proven; live network research remains host-dependent |
| Use skills from planning onwards | Ten-phase lifecycle with native skills and specialist strengths per phase | Live run selected decision, research, brainstorming, specification, planning, implementation, verification, polish and release capabilities | Proven |
| Use Superpowers at its strengths | Brainstorming, writing-plans, TDD, subagent, parallel, review, verification and branch-finish mappings | Live route selected Superpowers strengths in the correct phases | Routing proven; actual plugin execution requires installation |
| Use parallel agents safely | Parallel assessment, independence rules, integration owner and whole-system verification | Live plan allowed parallel work only after shared contracts froze | Decision logic proven; real multi-agent dispatch remains host-dependent |
| Use 500+ AI Agents | Discovery-only blueprint adapter with exact linked-repository validation | Live research route selected 500+ agent blueprint discovery | Proven as discovery; no blind deployment |
| Use Agent Reach and Last30Days | Governed supporting research channels | Agent Reach selected in live route; Last30Days covered by tests | Routing proven; external execution requires network and approval |
| Preserve all skills, agents and plugins | Capability registry, 32 native skills, 58 strengths, 21 agents, 54 resources | Registry, readiness audit and native skill copies validated | Proven |
| Resolve overlaps intelligently | Semantic overlap matrix: baseline, intensifier, substitute, complementary, sequential, reference, observer | Karpathy baseline + Ponytail intensifier and design-specialist sequencing validated | Proven |
| Superior design guidance | `design-intelligence.md` is the supreme design constitution | Constitution remained active across all design phases | Proven |
| Use UI/UX Pro, Taste, Impeccable and Emil correctly | Research, art direction, implementation, verification/polish and motion roles are separated | Phase routing and non-collision tests passed | Proven |
| Enterprise-grade implementation | Native product, governance, data, frontend, AI, automation, legal, investment and quality skills | Live smoke implementation enforced maker-checker approval and invalid-transition rejection | Partially proven; full product not implemented |
| Evidence before PASS | Structured check records and truthful PARTIAL closure | Live lifecycle closed PARTIAL because only the workflow core was implemented | Proven |
| Fresh installation should work | Safe installer, seeds, doctors and self-test | Fresh project created required directories and completed lifecycle | Proven after patch |

## Real-time project journey

Scenario:

```text
Enterprise regulated claims platform
+ maker-checker workflow
+ dashboards
+ API and RBAC
+ responsive design and motion
+ bounded AI document triage
+ standards research
+ agent blueprint comparison
+ safe parallel work
```

Observed phase sequence:

```text
DISCOVER
→ RESEARCH
→ BRAINSTORM
→ SPECIFY
→ PLAN
→ IMPLEMENT
→ VERIFY
→ POLISH
→ RELEASE
→ PARTIAL closure
```

Produced artifacts:

```text
PROJECT_CONTEXT.md
DOMAIN_CONTEXT.md
docs/decisions/DECISION_LOG.md
docs/specs/claims-platform.md
DESIGN.md
docs/plans/claims-platform-plan.md
src/workflow.py
tests/test_workflow.py
reports/verification.md
reports/polish.md
reports/release.md
SESSION_HANDOFF.md
```

Implemented smoke behaviour:

- valid checker approval passes;
- maker approval is blocked;
- invalid state transition is blocked;
- evidence is recorded;
- incomplete modules prevent a false production PASS.

## Defects found by the real-time run

### 1. Missing plan directory

A fresh installation did not create `docs/plans/`.

**Fix:** added `docs/plans/.gitkeep` to project seeds.

### 2. Complex platform classified as MATERIAL

A broad multi-module platform request without the literal phrase “new platform”
was classified too narrowly.

**Fix:** added a scope heuristic for build/create/design/implement requests that
combine a platform, system, application or suite with several major modules.

### 3. Plural agent-blueprint language missed

“Agent blueprints” did not always match the singular trigger.

**Fix:** complete-word plural-aware agent and blueprint patterns.

### 4. Noisy candidates in DISCOVER

ECC and broad design-reference resources leaked into discovery merely because
of generic trigger words.

**Fix:** resource-phase restrictions now keep them in their relevant phases.

### 5. Framework tests polluted product test discovery

The installer copied Escapement's own tests into the product's root `tests/`
folder. Product test discovery therefore ran framework tests too.

**Fix:** framework tests remain in the Escapement repository and are no longer
installed into product repositories.

### 6. Real lifecycle was not previously a regression test

The controlled evaluation suite could pass even though a real project failed at
PLAN.

**Fix:** added `test_real_project_lifecycle.py`, which installs a fresh project,
runs all lifecycle phases and closes the turn.

## Remaining gaps

### External capability execution

The repository maps and audits external capability strengths, but it does not
yet provide one universal installer and invoker for every external system.
Actual execution of Superpowers, UI/UX Pro Max, Taste, Impeccable, Emil,
Agent Reach, Last30Days, Context7 and browser adapters depends on:

- installation in the host;
- exact version and licence;
- host support;
- network and credentials;
- user approval.

This is correctly reported as `catalogued` or an install/load candidate rather
than falsely presented as active.

### Real parallel-agent dispatch

The router and plan validate whether parallel work is safe, but the smoke test
did not launch multiple real agents. Actual dispatch depends on Codex/Claude
host capabilities and the installed methodology.

### Per-skill evidence granularity

The runtime verifies that selected native skills are declared used and that
phase evidence exists. It does not yet require a separate evidence record for
every individual skill. A future strict mode should map each selected skill to
its artifact or check.

### Live public research

This offline package test verified routing and research contracts, not current
internet results. Agent Reach, Last30Days and authoritative web research must be
exercised in a network-enabled host.

## Final judgement

Escapement now contains the intended architecture and its core machinery works
as one system.

```text
Decision support          — proven
Domain expertise          — proven
Phase orchestration       — proven
Low-token operation       — proven
Native skills             — proven
Design authority          — proven
Overlap governance        — proven
Evidence and memory       — proven
Fresh installation        — proven
External plugin execution — correctly modelled, host-dependent
Parallel agent execution  — governed, host-dependent
Live internet research    — governed, network-dependent
```

The repository is ready for live Codex/Claude host testing. It should not claim
that every external capability is installed or executed until that host-level
validation is performed.
