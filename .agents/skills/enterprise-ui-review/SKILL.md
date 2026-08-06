---
name: enterprise-ui-review
description: Use for new UI, redesign, frontend implementation, screen or component review, responsive work, accessibility, generic AI appearance, or usability problems. Do not use for backend-only work.
---

# Enterprise UI Review

Review:

1. user and task;
2. information architecture;
3. navigation and location;
4. hierarchy and density;
5. action hierarchy;
6. forms, tables, filters, and drill-down;
7. loading, empty, error, permission, success, and stale states;
8. keyboard and focus;
9. accessibility;
10. responsiveness;
11. brand and `DESIGN.md`;
12. motion;
13. dead controls.

Read `docs/standards/design-intelligence.md` as the governing design authority. Use Impeccable for audit/hardening and Emil Kowalski skills for motion review when installed and relevant.

Use real browser evidence when available. Capture screenshots and commands as
structured evidence.

## This checklist gets skipped in real use -- check for it, don't just trust it

This skill routes correctly at IMPLEMENT/VERIFY/POLISH for UI work, but
routing only puts the checklist in front of an agent -- it doesn't force
the agent to actually apply it before calling the work done. Run:

```bash
python scripts/ui_quality_gate.py <frontend-src-dir>
```

before closing a POLISH phase on UI-touching work. It scans for concrete,
detectable signals -- responsive breakpoints, motion transitions,
`prefers-reduced-motion`, `:focus-visible`, loading-state and error-state
handling -- the same items 3/4/7/8 above already name. A clean
report is not proof of good UX; it is proof those items were not silently
skipped the way frontend-implementation's own doctrine was, in practice,
skipped before this existed.
