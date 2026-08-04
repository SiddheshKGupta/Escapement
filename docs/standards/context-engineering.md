# Context Engineering

## Goal
Give the agent the smallest complete context needed for the current decision.

## Context Pack
`Goal | Mode | Scope | Non-goals | State | Exact files | Rules | Data/permissions | Acceptance | Blockers | Skills | Checks`

## Four Moves
1. Write durable facts to repo files.
2. Select only relevant files and skills.
3. Compress old work into state/handoff.
4. Isolate independent work in subagents; return short evidence.

## Budget
- Root file = map, not encyclopedia.
- Task pack target <= 1,000 words.
- Skill target <= 300 lines; details in references.
- Cap/filter command output or save to file.
- Load references only on trigger.

## Context Rot Check
- Goal still visible?
- Facts current?
- Scope changed?
- Old logs crowding task?
- Handoff needed?
- Can work be isolated?

## Never
- Load whole repo by default.
- Treat chat as source of truth.
- Keep superseded context active.
