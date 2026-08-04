# Harness Engineering

Harness = `Instructions + Context + State + Skills + Tools + Tests + Gates + Feedback`.

## Loop
`Define → Context → Route → Execute small step → Observe → Deterministic checks → Semantic/risk review → Accept/Retry/Escalate/Stop → Record → Improve from repeated evidence`

## Guardrails
- Turn/retry budget per ticket.
- Active skill budget.
- Human gate for schema, auth, destructive, paid, production, scope.
- Deterministic checks before LLM review.
- No skill rewrite from one failure.
- No score without evidence.

## Ticket Score
- Correctness 40
- Requirement coverage 20
- Test evidence 15
- Security/data safety 10
- Efficiency 10
- Handoff 5

Pass >=85 and no critical failure.

## Improve or Retire
Improve after repeated failure, missed trigger, failed validation, or excess cost.
Retire if duplicate, unused across 5 relevant tasks, no measurable impact, stale, unsafe, or incompatible.
