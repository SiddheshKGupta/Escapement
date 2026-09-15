# Web Design Guidelines Extension

This optional extension lets an agent review interface code against the public
Web Interface Guidelines instead of against its own recollection of good
practice.

Sources:

1. Guidelines content, fetched at review time:
   `https://github.com/vercel-labs/web-interface-guidelines`
   (raw: `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`)
2. Method reference only, not installed:
   `https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md`

## Licence position

The guidelines repository is MIT. The `vercel-labs/agent-skills` repository that
packages the upstream skill has **no LICENSE file, no NOTICE, and no `license`
field in its `package.json`**, and the GitHub API reports its licence as null;
its `package.json` is marked `private`. It is therefore treated as
all-rights-reserved.

Consequences, which this extension observes:

- the upstream `SKILL.md` is **not** copied, vendored, or paraphrased closely --
  `files/skills/web-design-guidelines/SKILL.md` is original wording describing
  the same method;
- the guidelines themselves are fetched from the MIT repository at review time,
  not embedded here;
- the component is marked `approval_required`, so installing it needs
  `--approved`.

Before activation:

- confirm the guidelines repository licence has not changed;
- re-check whether `vercel-labs/agent-skills` has since published a licence;
- pin and record the guidelines revision used for a given review;
- update `THIRD_PARTY_NOTICES.md`;
- capture the review output as evidence.

The checklist is a verification aid, not a design authority. `DESIGN.md` and
`enterprise-ui-review` remain authoritative where they conflict with it.
