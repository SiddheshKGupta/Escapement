---
name: web-design-guidelines
description: Use to check interface code against the current public Web Interface Guidelines for accessibility, interaction, and layout defects. Do not use without approval and a fetch of the guidelines at review time.
---

# Web Design Guidelines Review

1. Read `docs/integrations/web-design-guidelines.md`.
2. Fetch the guidelines fresh at review time from
   `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`.
   Do not review against a remembered or vendored copy.
3. Confirm the files or glob under review. Ask if none was named.
4. Read those files and check each guideline against them.
5. Report one finding per line as `file:line` plus the rule broken, shortest first.
   Report nothing where nothing is broken; do not pad the list.
6. Record which guidelines revision was fetched, as evidence.

This is a checklist pass, not design authority. `DESIGN.md` and
`enterprise-ui-review` outrank it where they disagree. Do not copy the
guidelines text into the repository -- fetch it, cite it, and leave it upstream.
