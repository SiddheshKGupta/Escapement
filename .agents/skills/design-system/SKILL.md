---
name: design-system
description: Create an original product design system with client brand taking precedence over external references. Selects one archetype, defines colour, typography, spacing, shape, and motion tokens, and produces DESIGN.md. Use for any design, brand, colour, typography, layout, motion, or responsive work before implementation.
trigger: "Design, brand, colour, typography, layout, motion, responsive, DESIGN.md."
---

# Design System

Read `docs/standards/design-intelligence.md` before deciding anything.

## Precedence

```text
Client brand
→ Product requirements
→ Product DESIGN.md
→ Enterprise standards
→ External references
```

A client brand rule always overrides an external reference.

## Steps

1. Establish the dominant idea. One sentence. Everything else serves it.
2. Select exactly one archetype from design-intelligence §4. Record why, and which archetypes were rejected.
3. Define tokens:

`Canvas | Surface | Border | Text primary | Text secondary | Accent | Success | Warning | Danger | Focus`

4. Define typography scale, weight strategy, and the spacing base.
5. Define radius, elevation, and motion durations.
6. Write or update `DESIGN.md` from `docs/templates/DESIGN.template.md`.
7. State adopted and rejected reference patterns explicitly.

## Rules

- Colour carries meaning. Decorative colour is not a token.
- Typography creates hierarchy before colour or weight is used.
- Density follows the task. Operational screens are dense; marketing is not.
- Every component needs states, not only an appearance.
- Restraint creates identity. One accent, applied consistently, beats five.

## Licensing

Do not copy protected logos, typefaces, imagery, or trade dress. Adopt principles, not assets.

## Output

- `DESIGN.md` with tokens, archetype, and rationale.
- Adopted and rejected reference patterns.
- Handover to `enterprise-ui-review` for implementation review.
