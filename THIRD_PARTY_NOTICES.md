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

## Web Design Guidelines extension (adapted from the Vercel Web Interface Guidelines)

```text
Name: Web Interface Guidelines / vercel-labs web-design-guidelines skill
Source URL: https://github.com/vercel-labs/web-interface-guidelines
  (guidelines content, fetched at review time)
  https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md
  (skill packaging, method reference only)
Pinned version or commit: guidelines repository main; skill file reviewed at
  commit ba46938889d4e58635362fb8f618e1178ac3ec46 (2026-01-16).
Licence: split. vercel-labs/web-interface-guidelines is MIT (GitHub licence
  API reports spdx_id MIT). vercel-labs/agent-skills publishes NO licence --
  no LICENSE, LICENSE.md, COPYING or NOTICE file at its root, no `license`
  field in its package.json (which is marked "private": true), and the GitHub
  licence API reports null. It is therefore treated as all-rights-reserved,
  not as permissively licensed, and no file of it is copied.
Copyright/NOTICE retained: attribution and both source URLs recorded in
  extensions/web-design-guidelines/ (component.json, files/docs/integrations/
  web-design-guidelines.md) and catalog/capability-registry.json
  (id: vercel-web-interface-guidelines); no source file copied.
Files or capability used: the review method described by the upstream skill --
  fetch the canonical guidelines at review time, check the named files against
  them, report terse file:line findings -- and, at runtime, the MIT guidelines
  text itself, fetched from its own repository and never vendored here.
Changes made: ADAPTED, NOT COPIED. extensions/web-design-guidelines/files/
  skills/web-design-guidelines/SKILL.md is original wording. It adds Escapement
  bindings the upstream skill does not have: DESIGN.md and enterprise-ui-review
  outrank the checklist on conflict, the fetched guidelines revision is recorded
  as evidence, and no vendored copy of the guidelines may be reviewed against.
  The component is marked approval_required: true, so install needs --approved.
Reason selected: adopting Escapement for UI work alone (the ui-ux bundle) wants
  an external, current, public interface checklist that enterprise-ui-review can
  be verified against, rather than only the harness's own judgement.
Alternatives rejected: copying or lightly editing the upstream SKILL.md
  (rejected -- its repository grants no licence to copy it, so any vendored
  copy would be a licence violation regardless of how small); embedding a
  snapshot of the MIT guidelines text in this repository (rejected -- the
  guidelines change and a frozen copy would silently review against stale
  rules; MIT would permit it, staleness is the objection); a new native skill
  under skills/ (rejected -- external, approval-gated, network-fetching
  capability belongs in extensions/, as perplexity-research already does).
Security review: no code executed, no credentials. One outbound HTTPS fetch of
  a public raw.githubusercontent.com Markdown file at review time; that fetched
  text is data to check code against, not instructions to execute.
Validation evidence: `component install extension web-design-guidelines
  <target> --approved` exercised into a throwaway target (approval gate
  confirmed to refuse the same command without --approved); `doctor --root .`
  PASS, 0 failures, 0 warnings.
Approved by: reviewed per user request 2026-09-15.
Date: 2026-09-15
```
