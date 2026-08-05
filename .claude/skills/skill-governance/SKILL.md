---
name: skill-governance
description: Select, observe, score, improve, and retire skills. Use when multiple skills may apply, after skill-assisted work, or when a skill is ignored, redundant, costly, stale, or ineffective.
metadata:
  owner: V L & CO
  version: 1.0.0
---
# Skill Governance
## Route
Select one primary skill per capability. Reject overlaps.
## Declare
`Skill | Trigger | Phase | Output | Check | Permission | Budget`
## Execute
Follow selected skill. Do not mix alternatives. Save large output to file.
## Observe
Capture invocation, adherence, evidence, cost, and impact.
## Evaluate
1. Deterministic checks.
2. Contract checks.
3. Semantic/risk review.
4. Human gate where material.
## Score
Trigger 15 | Adherence 20 | Correctness 30 | Evidence 20 | Efficiency 10 | Clarity 5.
Pass >=85 and no critical failure.
## Decide
PASS keep; PARTIAL log; FAIL retry once; repeated fail propose edit; redundant merge/retire; not-needed improve trigger.
## Learn
Do not rewrite from one anecdote unless critical safety defect. Version changes and add tests.
## Output
Append JSON line to `logs/skill-usage.jsonl`; update `reports/SKILL_HEALTH.md`.
