# UI Standard

## Goal

Enterprise. Dense. Predictable. Fast.

## Use

- Neutral canvas
- client colour for primary action
- 1px borders
- `rounded-md` / `rounded-lg`
- 12–14px table text
- compact rows
- sidebar/header/breadcrumb
- filters + toolbar
- table for lists >5
- skeleton
- empty action
- error recovery
- keyboard
- focus
- status labels
- restrained motion

## Avoid

- AI gradients
- glow
- glass blur
- sparkle
- giant cards
- excessive whitespace
- random colours
- fake data
- dead buttons

## Required States

`loading | empty | error | permission | success | stale | partial`

## Brand

```text
Primary: var(--brand-color)
Hover: var(--brand-hover)
Soft: var(--brand-soft)
Builder signature: #53284F
Text base: #1C121B
```

## Check

- Can user act in 3 seconds?
- Can keyboard do main flow?
- Does every status mean something?
- Does mobile preserve priority?
- Does table remain usable?
