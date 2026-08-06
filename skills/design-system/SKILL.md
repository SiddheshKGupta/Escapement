---
name: design-system
description: Use for design direction, brand, colour, typography, layout, visual style, animation, motion, responsiveness, design tokens, or creation/update of DESIGN.md. Also use when UI looks generic or inconsistent. Do not use for backend-only work.
---

# Product Design Constitution and System

Read:

- `docs/standards/design-intelligence.md`
- approved client brand material;
- existing `DESIGN.md`;
- `docs/standards/ui.md`;
- relevant entries in `docs/REFERENCE_CATALOG.md`.

Precedence:

```text
Approved product requirements and accessibility obligations
→ Product DESIGN.md and brand configuration
→ docs/standards/design-intelligence.md
→ Phase-specific design specialists
→ External references and component sources
```

Select one primary archetype and at most one narrow secondary influence. State
adopted and rejected patterns. Define colour roles, typography, spacing,
geometry, layout, components, states, motion, responsiveness, and
accessibility. Validate a representative screen.

Do not copy protected branding, images, proprietary fonts, or trade dress.

External specialists must declare the constitution sections applied and may not silently override them.

## Present the archetype and token direction, do not silently pick one

The same rule as `decision-coach`'s discovery questions applies here,
because visual direction is a material decision too: whichever theme,
palette, and layout a scaffold or starting template happens to ship with
is not a decision anyone made. Selecting a *different* one without saying
so is not a decision either -- it is a second silent default.

When a live user is present:

- State the candidate archetype(s) and the token direction (palette,
  typography, density, layout shape) before implementing them.
- Wait for a real answer, or their explicit instruction to proceed with
  the stated recommendation -- do not treat "build the frontend" as
  implicit permission to also decide what it looks like.
- If the current state (inherited from scaffolding, an existing screen,
  or a prior turn) was never actually chosen by anyone, say so explicitly
  rather than defending it as if it were.

Silently choosing and moving on is only correct when no user is
available to ask at all -- the same boundary `decision-coach` draws.
