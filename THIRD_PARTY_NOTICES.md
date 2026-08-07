# Third-Party Notices

This file records external code, skills, plugins, tools, services, templates,
and substantial adapted material used by Escapement or a consuming project.

No external resource is included merely because it appears in
`docs/REFERENCE_CATALOG.md`.

## Required record

```text
Name:
Source URL:
Pinned version or commit:
Licence:
Copyright/NOTICE retained:
Files or capability used:
Changes made:
Reason selected:
Alternatives rejected:
Security review:
Validation evidence:
Approved by:
Date:
```

## Grilling Intensifier (adapted from Matt Pocock's `grilling` skill)

```text
Name: grilling
Source URL: https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling
Pinned version or commit: main, reviewed 2026-08-07
Licence: MIT
Copyright/NOTICE retained: attribution and source URL recorded in
  skills/decision-coach/SKILL.md and catalog/capability-registry.json
  (id: mattpocock-grilling); no source file copied.
Files or capability used: the design-tree / question-frontier method
  described in the skill's own documentation, not its source text.
Changes made: rewritten in original wording as the "Grilling Intensifier"
  section of skills/decision-coach/SKILL.md, bounded by Escapement's
  existing decision-coach rules (repository-first inspection, five-question
  cap, recommended default and consequence, wait for confirmation).
Reason selected: explicit user request to stress-test/challenge a plan is
  a real, recurring need decision-coach did not previously intensify for.
Alternatives rejected: installing the external skill unmodified (rejected
  -- would let a second, uncoordinated question-asking procedure run
  outside decision-coach's rules); a new skills/ folder (rejected --
  the pattern used elsewhere in Escapement for externally-inspired but
  natively-owned behaviour is a capability-strength/doctrine addition, not
  a new skill directory; see karpathy-guidelines/ponytail).
Security review: no code executed, no network access, no credentials.
Validation evidence: tests/v6_3/test_external_candidates.py
  (DecisionGrillingSkillTest, RoutingTest.test_grilling_*).
Approved by: reviewed per user request 2026-08-07.
Date: 2026-08-07
```
