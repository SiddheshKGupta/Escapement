# Orchestration Strategy

Use for MATERIAL and PROGRAM work requiring several stages, specialist reviews,
or multiple independent tasks.

Do not load every capability into one context.

```text
Orient
→ Discover
→ Research
→ Brainstorm
→ Specify
→ Plan
→ Implement
→ Verify
→ Release
```

Each phase receives a fresh, bounded context and the skills strongest for that
phase.

Parallelise only tasks with independent files or outputs, explicit contracts,
no shared mutable state, and a defined merge and verification owner.

Subagents return artifacts and evidence, not unstructured conversation.
