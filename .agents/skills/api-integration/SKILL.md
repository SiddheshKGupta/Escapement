---
name: api-integration
description: Use for an API, connector, webhook, OAuth, endpoint, third-party service, MCP server, or system integration. Do not use for internal code with no external contract.
---

# API and MCP Integration

Define:

```text
Purpose | Owner | Provider | Endpoint/tool | Authentication | Permissions
Request/input | Response/output | Validation | Idempotency | Timeout | Retry
Rate limit | Error mapping | Audit | Secrets | Data classification
Observability | Fallback | Destructive/read-only annotations
```

Verify current official documentation. Keep secrets out of code and logs.
Validate both directions, define retries and idempotency, map errors safely, and
test failure and permission paths. New integrations require approval.

For MCP building, consult the Anthropic `mcp-builder` entry in the reference
catalogue and invoke `reference-router`.
