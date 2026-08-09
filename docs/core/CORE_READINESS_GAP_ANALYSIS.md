# Escapement Core — Readiness Gap Analysis

**Against Escapement v1 at HEAD `4def451`. 284 tracked files.**

Produced under `ESCAPEMENT_CORE_MASTER_HANDOFF.md` §36. No
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
constraint on everything below: Core Readiness is not "add a gate to
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

**INTERPRETATION.** Roughly 60% of Core Readiness already exists. The
gaps cluster in one place: everything downstream of *a model proposing
an action*, because that path does not exist yet.

---

## C. Gap map — required for Core Readiness

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
Core Readiness and all are on the §28 do-not-import list.

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

### The dimensional separation

The first draft used one enum mixing four unrelated concepts:
`OBSERVED | INFERRED | DECIDED | AUTHORIZED | SUPERSEDED`. That collapses
epistemic origin, decision status, authority and lifecycle validity into
a single axis — the exact error Continuum spent weeks learning to avoid
(`StrategyBelief` conflated belief with utility).

**Challenge to the four-dimension proposal.** Separating the axes is
right, but two of the proposed four are not orthogonal. A state item
cannot be both `epistemic=OBSERVED` and `decision_status=DECIDED` — an
observation is not a decision. Two nullable fields make illegal states
representable (`OBSERVED` + `DECIDED`), which is the mirror image of
collapsing concepts: a sum type modelled as a product type.

Authority and validity **are** genuinely orthogonal — any kind can be
authorised or not, active or stale. So one discriminator plus two
orthogonal axes:

```yaml
state_item:
  kind:       OBSERVATION | INTERPRETATION | DECISION   # exactly one
  authority:  INFORMATIONAL | AUTHORIZED                # orthogonal
  validity:   ACTIVE | STALE | SUPERSEDED               # orthogonal
  provenance:
    origin:      internal | external
    source:      <capability id>
    produced_by: <action or actor id>
    at:          <timestamp>
```

Worked examples:

```text
external MCP response      kind=OBSERVATION    authority=INFORMATIONAL  validity=ACTIVE
model conclusion           kind=INTERPRETATION authority=INFORMATIONAL  validity=ACTIVE
proposed architecture      kind=DECISION       authority=INFORMATIONAL  validity=ACTIVE
approved architecture      kind=DECISION       authority=AUTHORIZED     validity=ACTIVE
contradicted decision      kind=DECISION       authority=AUTHORIZED     validity=STALE
```

Human approval changes **only** `authority`. The object does not change
semantic identity — a decision does not *become* an authorisation.

### Unresolved tension, surfaced rather than decided

**Can an `OBSERVATION` ever be `AUTHORIZED`?** Authority governs
permission; a fact confers none. For observations the field is always
`INFORMATIONAL` — a constant carrying no information, which argues for
kind-specific fields.

Counter-argument, and the reason the current recommendation keeps it:
an always-present field means no code path can forget to check it, and
there is no shape in which a *missing* field could read as authorised.
Defensive uniformity over minimal modelling. **Worth revisiting once
there is a real MCP input surface.**

### The invariant enforced by type, not convention

```text
OBSERVATION != INTERPRETATION != DECISION
INFORMATIONAL != AUTHORIZED
```

No code path may raise `authority` to `AUTHORIZED` without an
`ACTION_AUTHORIZED` or `USER_APPROVED` event in the trace. **INTERPRETATION.**
This is what makes "information is not authority" checkable rather than
aspirational, and it is the state-level counterpart of the
`ActionProposal` / `AuthorizedAction` split in section F.

### Migration of existing keys

`PROJECT_STATE.yaml`'s `accepted_assumptions` become
`kind: INTERPRETATION`; `blocking_decisions` become `kind: DECISION,
authority: INFORMATIONAL`. Current behaviour is preserved; the fields
gain structure rather than changing meaning.

**Design note:** state typing (E) and provenance (G6) should be
*designed together* even if committed separately. An `OBSERVATION` with
unknown provenance is close to useless — the whole point is being able to
answer "where did this come from and what was it allowed to establish?"

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

### The type boundary — enforced structurally, not by discipline

A model produces untrusted reasoning output. An executor accepts only
authorised authority. **These must be different types**, so that bypass
is a type error rather than a code-review miss.

```python
proposal   = ActionProposal(...)        # untrusted; anyone may construct
decision   = effect_gate.evaluate(proposal)
authorized = decision.authorized()      # ONLY the gate can construct this
executor.execute(authorized)            # accepts AuthorizedAction only
```

```python
executor.execute(proposal)              # must not type-check
```

`AuthorizedAction` has no public constructor. It is producible only by
the effect gate, after effect classification, policy check, authority
check and any required approval. This is the runtime equivalent of the
state invariant in section E:

```text
untrusted reasoning output  !=  executable authority
observed != inferred != decided != authorized
```

**INTERPRETATION.** This is the single clearest thing Core can do
differently from generic agent frameworks, which typically pass a
loosely-typed tool call straight from model output to a dispatcher.

### The chokepoint

```text
ActionProposal
      -> classify_effect
      -> capability policy
      -> authority check
      -> approval required?
      -> AuthorizedAction        (gate-only construction)
      -> Executor
      -> evidence
      -> verification if required
```

Gate strength keyed to reversibility (handoff §5.1), reusing the
`Reversibility` concept v1 already applies to external resources.

**Enforcement tests, required before any executor ships:**

1. A test attempting to reach an executor without the gate — **build
   fails if it succeeds**.
2. A test attempting to construct `AuthorizedAction` outside the gate —
   must fail.
3. A test that a `DESTRUCTIVE` proposal without approval is denied and
   the denial is evented.

## G. Trace and instrumentation plan

**Exists:** `turns.jsonl` (turn-grained), `run_check.py` evidence
(content-addressed, sha256).

**Missing:** action-grained control events (G7) and cost accounting
(G12).

Extend the existing `append_jsonl` mechanism — do not build a second
trace system, and do not split causal history across files. One typed
event model, queryable by turn or by action:

```yaml
event_id:
event_type:
turn_id:
action_id:      # null for turn-grained events
caused_by:
actor:
timestamp:
payload:
```

Event types on the single stream:

```text
TURN_STARTED        TASK_CLASSIFIED      CONTEXT_COMPOSED
CAPABILITY_SELECTED MODEL_CALLED
ACTION_PROPOSED     ACTION_DENIED        ACTION_AUTHORIZED
ACTION_EXECUTED     EVIDENCE_RECORDED    CHECK_EXECUTED
DECISION_RECORDED   DECISION_STALE       DECISION_SUPERSEDED
USER_APPROVED       TURN_CLOSED
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
multi-agent / subagents             not in Core Readiness
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
 4  typed state (E)                           additive; designed with 5
 5  provenance/authority metadata (G6)        additive; designed with 4
 6  effect taxonomy + gate, NO executor       additive
 7  ActionProposal / AuthorizedAction types   gate-only construction
 8  action-grained trace events (G)           one typed event model
 9  cost instrumentation (G12)                recorded, unused
10  causal-sensitivity evals (H)              may reveal existing defects
11  mutation registry + CI wiring (H)         may fail initially
12  stale/re-entry semantics (G8)             additive

--- CORE READINESS exit criteria evaluated here ---

13  LangGraph Functional API shell (I)        no model, no executor yet
14  Executor interface, deterministic         Executor.execute(AuthorizedAction)
15  one reference executor                    READ + bounded local EXECUTION only
16  executor bypass / adversarial validation  must fail the build if bypassable
17  one model adapter                         proposes only; cannot execute
18  model proposes through the existing gate  first autonomous path
```

### The ordering invariant

```text
Effect Gate   exists before
Executor      exists before
Model         can propose executable actions
```

Stated as a permanent repository rule:

> **Governance precedes execution; execution precedes autonomy.**

A model adapter (17) is **not** an executor. The model proposes
`run pytest`, `write file`, `call MCP tool` — something must still turn
an authorised proposal into an effect, and that thing is introduced at
14–16, fully deterministic and adversarially tested, *before* any model
can reach it.

**No commit may introduce an ungoverned model-controlled execution
path.** Steps 6–7 land before 14, and 14–16 land before 17.

**Steps 10 and 11 are expected to fail on first run.** If the causal
sensitivity evals all pass immediately, that is evidence they are not
testing anything — the same vacuity failure Continuum's checker had.

**Order rationale:** the effect gate (6) lands *before* any executor (14)
so there is never a commit in which an ungoverned execution path exists.
Core extraction (1–3) precedes everything because Agent and MCP must
share it, and retrofitting shared semantics after three surfaces exist
is the duplication §38.2 prohibits.

---

## Naming and repository structure

Settled after this analysis was drafted:

```text
Escapement
├── Escapement Core          <- independent repository derived from v1 history
│   ├── governed runtime
│   ├── AI agent
│   ├── MCP server
│   └── MCP client
│
└── Continuum                <- research programme, frozen architecture
```

No new product name is introduced. The agent and MCP surfaces are what
Core evolves to support, not separate products.

Core is created by **cloning v1, preserving full Git history, and
pushing as a new independent repository**. There is deliberately **no
GitHub fork relationship**: PRs must not default upstream, and the
repository must be freely private-able. The word *fork* is avoided in
Core documentation because GitHub assigns it a specific meaning.

Escapement v1 remains the independent stable baseline. Core diverges
independently. Core may become public only after Core Readiness and the
first governed execution path have received independent review.

**Consequence for section D.** Open question 1 is resolved by the
independent-repository decision: Core does not need to live under
`scripts/core/` and does not have to disturb v1's `MANAGED_PREFIXES`. In
a fresh repository Core can be a top-level package from the first
commit, which is the cleaner structure previously judged too disruptive.

**Consequence for this document.** It is a bridge artifact — an analysis
*of* v1 *for* Core. It is retained in v1 so the reason for the split
stays legible in v1's history, and it carries into Core through the
preserved clone history.

## Open questions for review

1. ~~`scripts/core/` vs a package rename.~~ **Resolved by the independent-repository
   decision** — Core is a separate repository, so a top-level package is
   available without disturbing v1's managed prefixes.
2. **Turn-grained vs action-grained trace in one stream.** Extending
   `turns.jsonl` keeps one artifact; a separate `actions.jsonl` keeps
   turn records readable. Recommend one stream with a `grain` field, but
   this is a judgement call.
3. ~~Where authority records live.~~ **Resolved.** Both, with distinct
   roles and no duplicate truth:

   ```text
   EVENT TRACE      authoritative historical record — what happened
   PROJECT_STATE    current projection            — what is true now
   ```

   ```text
   USER_APPROVED action_17
         -> append immutable event        (authoritative)
         -> projection updates            (derived)
         -> action_17.authority = AUTHORIZED
   ```

   If projection and history disagree, rebuild state from events or
   **fail loudly** — never silently prefer one. This gives replay a
   legitimate, bounded role without importing Continuum's replay
   architecture.
4. **Codex resources as the provenance pilot.** `codex_resources.py`
   already reads external data. It is the natural first consumer of
   trust/authority classes — worth doing before MCP client rather than
   after.

**No implementation has been performed.** Awaiting review per §36.
