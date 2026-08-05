---
name: security-review
description: Use for authentication, RBAC, permissions, secrets, hooks, MCP servers, privacy, PII, payments, deployments, external integrations, vulnerabilities, or authorised security testing. Do not perform offensive testing without explicit written permission and scope.
---

# Security Review

Read:

- `SECURITY.md`
- `docs/standards/security.md`
- `docs/standards/privacy-observability.md`
- `catalog/external-resources.json`

Review:

```text
Assets | Trust boundaries | Data | Identity | Permissions | Secrets
Inputs | Dependencies | Hooks | MCP | Network | Logging | Abuse cases
Detection | Recovery | Approval
```

Run the defensive security gate. External pentest tools require written target
authorisation, scope, exclusions, sandbox, credential policy, and evidence
handling. Never test third-party targets without permission.
