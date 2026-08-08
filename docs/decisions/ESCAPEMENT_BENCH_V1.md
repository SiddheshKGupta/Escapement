# Escapement Bench v1

Deterministic evaluation suite for two of Escapement's three benchmark
claims, scoped to what runs in this environment without live paired agent
execution.

```text
Claim 1: Escapement behaves as designed.
Claim 2: Escapement reduces known agent failure modes.
Claim 3: With the same model, Escapement improves quality/reliability/
         efficiency over vanilla execution.
```

## Why claim 3 is out of scope for this suite

Claims 1 and 2 reduce to checking `route_prompt()`, `decision_questions()`,
and phase/closure output against an expected signal -- the same mechanism
`eval_harness.py` and `ablation_harness.py` already use. No live model
call, no cost, no wall-clock beyond routing.

Claim 3 asks something categorically different: does the same model
produce a *better outcome* with Escapement than without it. That needs two
real completions per task (vanilla vs. governed), a way to grade the
result (tests passing, requirement satisfaction, human review), and a
budget for both. Fifty paired live-execution cases is a materially bigger
commitment than fifty deterministic routing checks -- not a corner cut
here, a different piece of work. Proposed starting scope, not built in
this suite: 5-10 paired cases, single model, single host, identical task/
tool access/time budget, with the harness's own `pass@k` vs `pass^k`
distinction applied to reliability, not just success rate.

### Prior art for that design

Graft (`nanonets-graft` in the capability registry) has already run this
shape of experiment for a context layer rather than a governance layer,
and it is worth reading before building ours. It reports a 162-run
controlled efficiency comparison holding the agent, the file tools and
the task fixed so that only the context differs, and separately reports
SWE-bench Verified graded by the official harness rather than by its own
scoring. Two things transfer regardless of whether its numbers hold up
elsewhere: isolating a single variable while everything else stays
identical, and outsourcing the grading to a harness the authors do not
control. Both are the parts of claim 3 that are easy to get wrong in a
self-authored benchmark. Its published figures are cited here as method,
not as evidence about Escapement -- nothing in that comparison has been
reproduced here.

## Suite: `evals/escapement-bench-v1/evals.json`

50 cases, run via `python scripts/eval_harness.py run --suite escapement-bench-v1`.

```text
Claim 1 (15 cases)
  budget-enforcement            5   -- MICRO/MATERIAL/PROGRAM skill and
                                       context ceilings hold under load
  overlap-resolution            5   -- forbidden-pair and baseline-vs-
                                       intensifier rules hold
  explicit-invocation-discipline 5  -- grilling/prompt-master/prime-agent
                                       fire only on their trigger language,
                                       not on adjacent-sounding requests

Claim 2 (35 cases)
  ambiguity-trap                 5  -- a prompt that omits exactly one
                                       material fact gets asked about it;
                                       a prompt that already answers it
                                       does not get re-asked
  capability-selection-trap      5  -- a distractor keyword present in an
                                       unrelated task does not pull in the
                                       matching specialist skill
  reversibility-trap             5  -- irreversible/production language
                                       raises the bar; reversible/local
                                       language does not
  regulated-data-domain-language 5  -- PHI/PII/biometric/financial/legal-
                                       privilege data described in plain
                                       domain language (not jargon) still
                                       routes the right specialist, across
                                       four domains beyond the healthcare
                                       case the underlying fix (finding #3,
                                       PR #36) was built and tuned against
  tier-domain-neutrality         5  -- PROGRAM-vs-MATERIAL classification
                                       generalises to five domains beyond
                                       the four (clinical/logistics/lending/
                                       claims) used while building finding
                                       #1's fix
  data-handling-question-gen.    5  -- the consent/retention question
                                       (finding #4) generalises beyond
                                       healthcare and is correctly
                                       suppressed once actually answered
  false-positive-over-triggering 5  -- five new external-candidate PRs
                                       (#30-36) stay silent on ordinary,
                                       unrelated requests
```

Every case's `claim`/`category` fields are carried into the eval record
for reporting; `eval_harness.py`'s corpus-sharing principle (established
by the ablation harness) applies here too -- this suite extends the
existing runner and schema rather than forking a new one.

## What building this actually found

Two categories of finding, and it matters which is which.

**A real, fixed gap.** `security-review`'s trigger vocabulary covered PHI/
PII/consent (finding #3) but not biometric data (fingerprint, facial
recognition) -- a fingerprint check-in feature routed no security
specialist at all. Added `biometric` as a trigger, directly extending an
already-established pattern with the same justification (universally
recognised sensitive personal data category, not a novel judgment call).
Verified the existing 22-case corpus still passes after the change (no
regression from broadening the match).

**Three real, evidenced, *not* fixed gaps** -- `governance-risk-controls`'
trigger vocabulary (`governance/risk/control/compliance/RCSA/audit`)
does not include production-deployment, live-customer-data, or HR-access-
control language, so:

- a production schema migration touching live customer records
  (`reversibility-01`) routes only `software-implementation`;
- deploying an authentication change to production
  (`reversibility-05`) routes `security-review` but not
  `governance-risk-controls`;
- HR disciplinary/performance records with role-based visibility
  (`regulated-data-04`) routes neither.

Three independent cases converging on the same root cause is a pattern,
not a fluke -- but it was **deliberately not patched reactively**. Adding
triggers one case at a time to make a benchmark you wrote yourself pass is
how a router gets overfit to its own test set rather than actually
improved. The `biometric` fix above was kept because it extends an
existing, already-justified pattern; these three are recorded as a genuine
finding for a real design pass on `governance-risk-controls`' trigger
vocabulary, not resolved by three more one-off keyword additions.

## Authoring bugs found while building this suite (not framework bugs)

Worth recording because two are non-obvious and would recur in any future
suite built the same way:

- `evaluate()`'s `material` check is unconditional (`route["material"] !=
  bool(expected.get("material"))`), unlike `tier`/`mode`/`register`, which
  are skipped when unset. Every case needs `"material": true` explicit if
  the tier isn't INFO -- 42 of 50 cases failed on this alone on the first
  run, none of them a real routing problem.
- `external_candidates` in `expected` only ever checked *required*
  presence; there was no way to assert "must not appear." Added
  `forbidden_external_candidates`, mirroring the `forbidden_skills`/
  `forbidden_packs`/`forbidden_strengths` pattern already established.
- `MATERIAL_WORDS` is a fixed, bounded verb list (`build, create, fix,
  design, ...`). A prompt using an unlisted-but-natural verb (`give`,
  `make`, `run`, `sketch`, `store`, `let`) classifies INFO -- no runtime
  turn, no material questions, and (found empirically) `external_candidates`
  is still computed and populated even on an INFO-tier route, despite INFO's
  own doctrine stating it creates no runtime turn. That inconsistency is
  logged here, not fixed -- in practice `agent_runtime.py`'s `manual-start`
  never persists a turn for INFO, so the field is computed but never acted
  on; whether `route_prompt()` should compute it at all for INFO is a real
  but separate question from this suite's scope.
- The `authority` material question's guard matches the literal word
  `workflow` (among others) regardless of whether the described action is
  actually reversible -- a negative-control case using "workflow" in a
  reversible-action prompt failed for the wrong reason (word match, not
  semantic irreversibility) until the word was removed from the prompt.
  Documents that the mechanism is keyword-based, not a semantic
  reversibility detector, which is itself worth knowing when reading
  `reversibility-*` results as evidence.

## Result

50/50 passing on a clean run, after fixing the authoring bugs above and
one real trigger gap. Re-run the full corpus (`python scripts/eval_harness.py
run`) after any change to `capability_router.py`'s trigger/classification
logic -- 72/72 across both suites confirms no regression to the existing
22-case corpus from the `biometric` trigger addition.
