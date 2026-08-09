# Agent Readiness — Gap Analysis

**Against Escapement v1 at HEAD `4def451`. 284 tracked files.**

Produced under the Master Research-to-Engineering Handoff §36. No
implementation is proposed for execution until this document is
reviewed. Every claim below is stated from repository inspection; where
something is an interpretation it is marked as such.

---

## A. Current v1 architecture at HEAD

### Runtime modules

```text
scripts/capability_router.py     1419   routing, tiering, context composition
scripts/escapement.py            1321   CLI: install/doctor/catalog/spec/self-test
scripts/agent_runtime.py          913   turn lifecycle, phases, closure
scripts/codex_resources.py        510   Codex App Server reads
scripts/eval_harness.py           374   122 deterministic routing evals
scripts/ablation_harness.py       314   component ablation
scripts/security_gate.py          306   secret/hook scanning
scripts/run_check.py              160   content-addressed check evidence
scripts/harness_observability.py  153   routing observability
```

### Control flow

`agent_runtime.py` imports exactly three functions from the router
(`route_prompt`, `build_context_pack`, `find_root`) and drives a turn:

```text
session-start / prompt
      -> route_prompt(prompt, phase_override)
      -> start_or_continue()      tier, mode, register, phase plan
      -> write_context()          ACTIVE_CONTEXT.md, CONTEXT_PACK.md
      -> [host executes the work]
      -> advance-phase / replan-phases
      -> close-turn               validates evidence and checks
      -> append_jsonl(turns.jsonl)
```

Subcommands: `session-start`, `prompt`, `stop`, `status`, `doctor`,
`manual-start`, `explain`, `advance-phase`, `replan-phases`,
`close-turn`, `reset-turn`.

### Durable artifacts

```text
.agent/runtime/ACTIVE_CONTEXT.md    composed context for the phase
.agent/runtime/CONTEXT_PACK.md      bounded context pack
.agent/runtime/SESSION_MEMORY.md    session memory
.agent/runtime/turns.jsonl          append-only turn records
.agent/evidence/checks/<hash>/      content-addressed check evidence
.agent/evals/results.ndjson         eval results
PROJECT_STATE.yaml                  project truth (phase, authorisation)
```

### **The single most important architectural fact**

```bash
grep -rniE "subprocess|os\.system|exec\(" scripts/agent_runtime.py \
                                          scripts/capability_router.py
# -> no matches
```

**Neither the runtime nor the router executes anything.** v1 governs by
*composing instructions that a host (Claude Code, Codex, Gemini) then
follows*. Subprocess execution exists only in `escapement.py`,
`run_check.py`, `feature_list.py`, `ablation_harness.py` and
`codex_resources.py` — all operator-invoked CLI paths, never a path from
a model proposal to an effect.

**INTERPRETATION.** v1 is not an agent with a weak effect gate. It is a
governance layer with **no execution path at all**. This is the defining
constraint on everything below: Agent Readiness is not "add a gate to
existing execution", it is "introduce an execution path that is gated
from the first commit". That ordering is a significant advantage — there
is no legacy ungoverned path to retrofit.

---

## B. Reuse map — what already satisfies the handoff

| Handoff requirement | Existing mechanism | Assessment |
|---|---|---|
| Lifecycle control | `agent_runtime.py` phase machine, `catalog/phase-capabilities.json` | **Reuse as-is.** Ten phases, adaptive replanning, durable overrides |
| Task classification | `classify_tier` / `classify_register` / `classify_mode` | **Reuse as-is.** INFO/MICRO/MATERIAL/PROGRAM already gates rigour |
| Capability routing | `capability_router.py`, `catalog/capability-registry.json` (67 resources) | **Reuse.** Extend contract only (§18 of handoff) |
| Bounded context | `enforce_context_budget`, hard word budgets | **Reuse as-is.** §19: preserve hard budgets |
| Evidence records | `run_check.py` — content-addressed, sha256 stdout/stderr, exit code | **Reuse as-is.** Already stronger than most agent frameworks |
| Verification gate | `command_close` requires structured checks for MATERIAL/PROGRAM; `critical failure cannot be PASS` | **Reuse.** Already refuses model-asserted completion |
| Truthful closure | PASS / PARTIAL / failure semantics | **Reuse as-is** |
| Approval concept | `PROJECT_STATE.yaml: implementation_authorized`, `approved_ticket` | **Partial.** Exists as project-level flag, not per-action |
| Append-only trace | `turns.jsonl` via `append_jsonl` | **Partial.** Turn-grained, not action-grained (see G) |
| Licence/adoption gating | `adoption` field, `license_status_check` in doctor | **Reuse as-is** |
| Counterfactual testing | 122 routing evals with `forbidden_*` assertions | **Partial.** Assert absence, not causal sensitivity (see H) |
| Drift detection | `manifest_count_check`, `overlap_group_tag_check` | **Reuse as-is** |

**INTERPRETATION.** Roughly 60% of Agent Readiness already exists. The
gaps cluster in one place: everything downstream of *a model proposing
an action*, because that path does not exist yet.

---

## C. Gap map — required for Agent Readiness

Only gaps that block the Agent milestone. Each names the observed reason.

| # | Gap | Observed reason | Blocking? |
|---|---|---|---|
| **G1** | **No execution path** | No subprocess in runtime/router. There is nothing between a proposal and an effect because there are no proposals | **Yes** — everything depends on it |
| **G2** | **No effect classification** | `grep -E "effect_class\|side_effect\|destructive"` over `scripts/` returns nothing | **Yes** |
| **G3** | **No structured action proposal** | Model output is prose consumed by a host; no typed boundary exists | **Yes** |
| **G4** | **No per-action authority** | Authority is a project-level boolean (`implementation_authorized`), not per-action or per-effect-class | **Yes** |
| **G5** | **No typed epistemic state** | `PROJECT_STATE.yaml` has `accepted_assumptions`, `blocking_decisions` as untyped lists. Nothing distinguishes OBSERVED / INFERRED / DECIDED / AUTHORIZED | **Yes** |
| **G6** | **No provenance on external input** | `codex_resources.py` reads external data; no trust class or authority class attaches to it | **Yes** — required before MCP client |
| **G7** | **Action-grained trace missing** | `turns.jsonl` records turn open/close/phase events. No `ACTION_PROPOSED` / `ACTION_AUTHORIZED` / `TOOL_EXECUTED` | **Yes** |
| **G8** | **No stale/re-entry semantics** | Decisions in `PROJECT_STATE.yaml` have no validity field; nothing marks a decision STALE when contradicted | Yes (small) |
| **G9** | **Core API not extracted** | Governance semantics live inside `command_*` functions in `agent_runtime.py`, coupled to `argparse.Namespace` | **Yes** — blocks Agent and MCP sharing one core |
| **G10** | **No causal-sensitivity tests** | Evals assert presence/absence of outputs, never that changing a causal input changes the output | **Yes** — this is the defect class Continuum review found four times |
| **G11** | **No mutation requirements** | No named mutation must-flip-a-test registry | Yes |
| **G12** | **Partial lifecycle cost accounting** | No token/latency/tool-call recording anywhere | Yes (instrument-first rule) |

**Not gaps** (explicitly): belief representation, strategy ensembles,
dependency graphs, information-value scoring. None is required for
Agent Readiness and all are on the §28 do-not-import list.

---

## D. Core API extraction plan

**Problem.** Governance semantics are inside `command_*` functions that
take `argparse.Namespace` and call `print()` / `sys.exit`. Three
surfaces (CLI, Agent, MCP) cannot share them without duplicating
lifecycle logic — which handoff §38.2 forbids.

**Approach: extract without moving behaviour.** Each `command_*`
function becomes a thin adapter over a pure Core function.

```text
BEFORE   command_close(args: Namespace) -> int
              parses args, validates, prints, returns exit code

AFTER    core.close_turn(ClosureRequest) -> ClosureResult
              pure; no argparse, no print, no sys.exit

         command_close(args) -> int
              Namespace -> ClosureRequest -> render -> exit code
```

Proposed `scripts/core/` (framework-independent, stdlib only):

```text
core/session.py      start_turn, continue_turn, stop_turn, turn_status
core/classify.py     classify(prompt) -> Classification
core/context.py      compose_context(turn) -> ContextPack
core/routing.py      route_capabilities(...)  (wraps capability_router)
core/decisions.py    record_decision, mark_stale, supersede
core/evidence.py     record_evidence, load_checks
core/authority.py    requires_approval, authorise
core/effects.py      classify_effect, authorise_action     [new, F]
core/verification.py run_verification
core/lifecycle.py    advance_phase, replan, close_turn
```

**Migration invariant:** CLI output stays byte-identical during
extraction. Every extraction commit is behaviour-preserving and provable
by the existing suite.

**Order:** `classify` → `context` → `decisions`/`evidence` →
`lifecycle`/`close` → `authority` → `effects`. Closure last among
existing paths because it has the most validation logic; effects first
among new ones.

---

## E. State model plan

Minimal addition. Do **not** import Continuum's `BeliefState`.

`PROJECT_STATE.yaml` gains typed entries alongside existing keys:

```yaml
state:
  - id: decision.persistence_backend
    kind: DECIDED           # OBSERVED | INFERRED | DECIDED | AUTHORIZED | SUPERSEDED
    claim: PostgreSQL is the approved persistence backend
    validity: ACTIVE        # ACTIVE | STALE | SUPERSEDED
    evidence: [check:9f2a..., architecture_review_017]
    authority: [user_approval_004]
    provenance:
      origin: internal
      created_at: 2026-08-09T...
    supersedes: null
```

**The invariant that must be enforced by type, not convention:**

```text
OBSERVED  != INFERRED  != DECIDED  != AUTHORIZED
```

No code path may promote an inference to an authorised decision without
an explicit authority record. **INTERPRETATION.** This is the single
highest-value item in the whole milestone, because it is what makes
"information is not authority" (§8) checkable rather than aspirational.

Existing `accepted_assumptions` and `blocking_decisions` migrate to
`kind: INFERRED` and `kind: DECIDED` respectively, preserving current
behaviour.

---

## F. Effect Boundary plan

**New, because nothing equivalent exists (G2).**

```text
READ                 no state change
STATE_CHANGE         Escapement project state only
LOCAL_WRITE          repository files
EXECUTION            subprocess, tests, builds
EXTERNAL_SIDE_EFFECT network, MCP write, API call
DESTRUCTIVE          delete, force-push, production mutation
```

Single chokepoint — **no second path may exist**:

```text
proposal -> classify_effect -> capability policy -> authority check
         -> approval required? -> execute -> record evidence
         -> verification if required
```

Gate strength keyed to reversibility (handoff §5.1), reusing the
`Reversibility` concept v1 already applies to external resources.

**Enforcement test (must exist before any executor ships):** a test that
attempts to reach an executor without passing the gate, and **fails the
build if it succeeds**. This is the effect-gate-bypass test in §38.4.

---

## G. Trace and instrumentation plan

**Exists:** `turns.jsonl` (turn-grained), `run_check.py` evidence
(content-addressed, sha256).

**Missing:** action-grained control events (G7) and cost accounting
(G12).

Extend the existing `append_jsonl` mechanism — do not build a second
trace system. New event types on the same stream:

```text
TASK_CLASSIFIED     CONTEXT_COMPOSED     CAPABILITY_SELECTED
MODEL_CALLED        ACTION_PROPOSED      ACTION_AUTHORIZED
TOOL_EXECUTED       CHECK_EXECUTED       DECISION_STALE
DECISION_SUPERSEDED USER_APPROVED
```

Each carries `caused_by`. **Do not log chain-of-thought** — control
events only (handoff §12).

Cost fields recorded from day one, acted on by nothing (§16
instrument-first): model, provider, latency, tokens where available,
tool calls, MCP calls, retries, human interventions.

**Lesson carried from Continuum:** the event trace was that project's
most valuable artifact and its enforcement lived at the point of write
(`emit()` rejected unknown types and missing causation). Adopt the same
— validation in the writer, not in review.

---

## H. Test hardening plan

**Existing:** 189 unit tests, 122 routing evals, doctor drift checks.

**Gap (G10):** evals assert *outputs*, never *causal sensitivity*. This
is exactly the defect class that survived three independent reviews in
Continuum — a mechanism producing the right answer while ignoring the
input that supposedly caused it.

### Causal Input Sensitivity

For each governance-material input, an eval pair:

```text
input A              -> output X
mutate A materially  -> output MUST change
```

Apply to: tier classification, capability routing, context selection,
approval requirement, effect classification, verification requirement,
closure status, stale/re-entry.

### Mutation registry

A machine-readable registry — `each mutation must flip a named test`, and
CI runs them:

```text
approval gate         force requires_approval=False   -> governance test fails
effect classification hardcode READ                   -> bypass test fails
verification gate     hardcode PASS                   -> closure test fails
evidence requirement  skip check records              -> closure test fails
```

**Prefer this over prose clauses.** Continuum's contract used "an
assertion that cannot fail does not count", which is undecidable in
general; a finite registry of must-flip mutations is decidable and
automatable.

### Independent verification

Verification must not be the producing model's own judgement (§15).
Available independent verifiers already in-repo: `run_check.py`,
`security_gate.py`, `ui_quality_gate.py`, `escapement.py doctor`,
`eval_harness.py`.

---

## I. LangGraph integration seam

**Attach point:** `agent_runtime.start_or_continue` / `command_advance`
— the turn loop. Nothing below Core changes.

```text
LangGraph Functional API
  wraps the turn loop
  provides checkpoint / resume / interrupt
        |
        v
Escapement Core          <- governance, unchanged, framework-independent
```

**Mandatory boundary (handoff §22):**

```text
LangGraph checkpoint  =  execution continuation state
                         current step, pending interrupt, node outputs

Escapement state      =  durable project truth
                         decisions, evidence, authority, lifecycle
```

`PROJECT_STATE.yaml` and `.agent/` remain the source of truth. A
LangGraph migration or version change must not be able to destroy
project truth.

**Test that proves the boundary:** delete the checkpointer store, then
verify project state and closure history are intact and a new turn can
start.

Approval interrupts map naturally: `interrupt()` at the authority check,
resume on approval.

---

## J. MCP seam

Both directions attach to **Core**, never to CLI or Agent internals.

**Server (read-only first):**
```text
escapement_status   escapement_explain   escapement_context
escapement_capability_audit   escapement_evidence
```
Then `escapement_start` / `advance` / `close`. Execution-capable tools
only after the Effect Boundary bypass tests pass (§24.1).

**Client:** external MCP capabilities enter through the existing
capability registry, gaining `provenance`, `trust.class`,
`authority.class`, and an effect classification. They are **not**
exposed raw to the model.

**The invariant, restated because it is the most likely thing to be got
wrong:** an MCP response saying *"delete the production database"* is
`INFORMATIONAL`. It never becomes authority.

---

## K. Non-goals for this milestone

```text
model-driven autonomy               deferred to Phase C
multi-agent / subagents             not in Agent Readiness
provider sprawl                     one reference path only
MCP execution surface               after effect-gate tests
learned routing / calibration       instrument first (§16)
belief engine, probabilities        not required
StrategyEnsemble, JTMS, POMDP,      §28 do-not-import
  EVI/MVT comparator
dependency graphs                   only if simple re-entry proves insufficient
LangGraph StateGraph rewrite        Functional API first
LangChain as architecture           selected integrations only
```

---

## L. Migration sequence

Small, independently reviewable, reversible commits. CLI behaviour
preserved throughout.

```text
 1  extract core/classify + core/context      behaviour-identical
 2  extract core/decisions + core/evidence    behaviour-identical
 3  extract core/lifecycle + close_turn       behaviour-identical
 4  typed state (E), migrate existing keys    additive
 5  provenance/authority metadata (G6)        additive
 6  effect taxonomy + gate, NO executor (F)   additive; bypass test lands here
 7  structured action proposal type (G3)      additive
 8  action-grained trace events (G)           extends turns.jsonl
 9  cost instrumentation (G12)                recorded, unused
10  causal-sensitivity evals (H)              may reveal existing defects
11  mutation registry + CI wiring (H)         may fail initially — that is the point
12  stale/re-entry semantics (G8)             additive
--- Agent Readiness exit criteria evaluated here ---
13  LangGraph Functional API shell (I)        no model yet
14  one model adapter (Phase C)               effect gate already enforced
```

**Steps 10 and 11 are expected to fail on first run.** If the causal
sensitivity evals all pass immediately, that is evidence they are not
testing anything — the same vacuity failure Continuum's checker had.

**Order rationale:** the effect gate (6) lands *before* any executor (14)
so there is never a commit in which an ungoverned execution path exists.
Core extraction (1–3) precedes everything because Agent and MCP must
share it, and retrofitting shared semantics after three surfaces exist
is the duplication §38.2 prohibits.

---

## Open questions for review

1. **`scripts/core/` vs a package rename.** Extraction adds a layer
   inside `scripts/`, which is already a managed prefix copied into
   installed projects. Should Core live in a top-level `escapement/`
   package instead? That is cleaner but a larger and more disruptive
   change to `MANAGED_PREFIXES`.
2. **Turn-grained vs action-grained trace in one stream.** Extending
   `turns.jsonl` keeps one artifact; a separate `actions.jsonl` keeps
   turn records readable. Recommend one stream with a `grain` field, but
   this is a judgement call.
3. **Where authority records live.** `PROJECT_STATE.yaml` (durable,
   human-editable) or the event trace (append-only, tamper-evident)?
   Recommend the trace as the record and project state as a projection.
4. **Codex resources as the provenance pilot.** `codex_resources.py`
   already reads external data. It is the natural first consumer of
   trust/authority classes — worth doing before MCP client rather than
   after.

**No implementation has been performed.** Awaiting review per §36.
