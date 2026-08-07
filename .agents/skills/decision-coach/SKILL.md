---
name: decision-coach
description: Use at the start of MATERIAL or PROGRAM work when the user has a rough request, unclear success criteria, hidden trade-offs or missing decisions. Ask only high-impact questions, recommend defaults and produce a better execution brief.
---

# Decision Coach

1. Identify the actual decision and desired outcome.
2. Inspect available project state before asking questions.
3. Separate known facts, assumptions and material unknowns.
4. Ask at most five questions whose answers can change the solution.
5. For each question provide:
   - why it matters;
   - recommended default;
   - consequence of another choice.
6. Produce an improved execution brief containing scope, non-goals, users,
   domain, constraints, outputs, acceptance and verification.
7. Stop discovery when planning can proceed safely.

Do not ask the user to rewrite their prompt from scratch.

## A recommended default is a proposal, not a substitute for asking

A recommended default exists so a genuinely unattended run (CI, a batch
job, no human in the loop) has something reasonable to proceed on, and so
an interactive user has less work to do when they *do* answer -- confirming
a default is faster than answering from nothing. It is not permission to
skip asking.

When a live user is present in the conversation:

- Present the material questions to them directly, in your response, with
  each recommended default and its consequence stated -- do not silently
  substitute the default and continue as if they had answered.
- Wait for their actual answer, or their explicit instruction to proceed
  with the stated defaults, before advancing past `DISCOVER` on `MATERIAL`
  or `PROGRAM` work.
- The bigger the decision's blast radius -- an architecture choice, a
  compliance-sensitive rule, anything hard to reverse once code exists --
  the less acceptable it is to have decided it without them, even under
  time pressure or mid-demo.

Silently self-answering and moving on is only correct when no user is
available to ask at all.

## Grilling Intensifier

An explicit request to be "grilled," to "stress-test" a plan, or to have
every assumption "challenged" activates a deeper round of this same
procedure rather than a different one. decision-coach remains canonical;
grilling never activates on an ordinary feature request (see
`catalog/overlap-matrix.json`, group `decision-interview`).

1. Build a short decision tree of the plan's real branch points --
   architecture choice, data model, external dependency, irreversible
   action -- instead of one flat list of questions.
2. Walk it branch by branch. For each branch, inspect the repository first;
   only ask what inspection could not answer.
3. Still cap the round at five material questions. If the tree has more
   branches than that, ask the five with the largest blast radius and name
   the rest as deferred, not dropped.
4. State the hidden assumption behind each branch explicitly -- an
   assumption surfaced and confirmed is the point of grilling, not a side
   effect.
5. Stop once the plan's real branch points have been named and confirmed or
   defaulted; grilling is a deeper pass over the same plan, not a second
   plan.

Inspired by the design-tree/question-frontier method in Matt Pocock's
`grilling` skill (`https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling`,
MIT). This section is original wording adapted for Escapement's own rules,
not a copy of that skill's text.
