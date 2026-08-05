# Security Policy

## Trust model

Escapement installs repository-local instructions, skills, scripts, and
lifecycle hooks. A trusted coding agent may execute those files.

Review before approval:

```text
.codex/hooks.json
.claude/settings.json
scripts/agent_runtime.py
scripts/escapement.py
scripts/run_check.py
catalog/external-resources.json
```

Never approve hooks from an untrusted repository merely because the repository
looks familiar.

## Supported version

Security fixes are maintained for the latest tagged release.

## Reporting a vulnerability

Report privately to the repository owner or V L & CO. Do not include live
credentials, personal data, exploit payloads against third parties, or customer
confidential information in a public issue.

Include:

- affected version;
- operating system and agent runtime;
- reproduction steps;
- expected and actual behaviour;
- impact;
- proposed mitigation where known.

## Security gates

Approval is required before:

- authentication or RBAC changes;
- schema changes involving sensitive data;
- hooks or MCP server changes;
- new network services;
- secret or credential access;
- destructive actions;
- production deployment;
- external security testing.

## Offensive security tools

Escapement core is defensive.

External tools such as Strix may be used only when:

- the target is owned by the user or explicitly authorised;
- scope and exclusions are written;
- credentials and test data are approved;
- execution occurs in an appropriate sandbox;
- findings and proof are handled securely;
- the user controls whether remediation is applied.

## Local evidence

Runtime, evaluation, check, and security records are local by default under
`.agent/`. Review before sharing them because command output may contain paths,
source snippets, or business information.

## Secrets

Do not commit:

- API keys;
- tokens;
- passwords;
- private keys;
- cookies;
- session exports;
- production connection strings.

Use environment variables or approved secret managers. Logs must redact secret
values.

## External resources

Consult `docs/REFERENCE_CATALOG.md`.

Public visibility is not a licence. Verify the licence at the selected tag or
commit before copying code, skills, templates, or documentation.
