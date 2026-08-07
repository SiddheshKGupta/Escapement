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

A default exists for unattended runs (CI, no human in the loop) and to
make an interactive answer faster to give -- it is not permission to skip
asking.

When a live user is present:

- Present the material questions directly, with each default and its
  consequence stated -- do not silently substitute the default and
  continue as if they had answered.
- Wait for a real answer, or explicit instruction to proceed with the
  stated defaults, before advancing past `DISCOVER` on `MATERIAL` or
  `PROGRAM` work.
- The bigger the blast radius -- an architecture choice, a compliance
  rule, anything hard to reverse -- the less acceptable it is to have
  decided it without them, even under time pressure.

Silently self-answering is only correct when no user is available at all.

## Surface Relevant Capabilities

Name matched, not-yet-installed capabilities in the same response as the
material questions, not a separate report (`AGENTS.md`, step 8).

1. Check `capability-audit` for the actual request; name each match in one
   line -- what it is, why it matched, and a recommended yes/use-it or
   no/skip-it.
2. "Yes" is an explicit approval gate (`AGENTS.md`, Approval Gates) -- a
   registry name is a reviewed candidate, never an installed default.
3. No strong match: offer, do not silently perform, a research pass via
   `reference-router` for current external options; wait for go-ahead.

Skip this section for MICRO work.

## Grilling Intensifier

Explicit "grill me" / "stress-test this plan" / "challenge every
assumption" deepens this same procedure -- decision-coach stays canonical,
never activates on an ordinary feature request
(`catalog/overlap-matrix.json`, group `decision-interview`).

1. Map the plan's real branch points; inspect the repository per branch
   before asking.
2. Still cap at five material questions -- highest blast radius first,
   defer the rest.
3. State each branch's hidden assumption explicitly.

Adapted, original wording, from Matt Pocock's MIT `grilling` skill
(`github.com/mattpocock/skills/tree/main/skills/productivity/grilling`).
