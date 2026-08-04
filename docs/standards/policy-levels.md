# Policy Levels

Every material rule should be classified.

| Level | Meaning | Default response |
|---|---|---|
| Mandatory | Required for correctness, security, or governance | Block on failure |
| Approval | Requires human decision | Pause and request approval |
| Recommended | Default approach | Follow unless justified |
| Conditional | Applies only when triggered | Load on trigger |
| Reference | Informational | Do not treat as binding |

Recommended metadata:

```yaml
rule_id: DATA-004
level: mandatory
applies_to:
  - dashboard
verification: automated
failure: block
```
