---
name: automation-engineering
description: Use for n8n, workflow automation, scheduled jobs, event triggers, webhooks, background processing, notifications or operational automations. Do not automate an undefined or uncontrolled business process.
---

# Automation Engineering

Define:

```text
Trigger | Input | Rule | Steps | Owner | Credentials | Idempotency
Retry | Timeout | Human checkpoint | Exception | Alert | Audit | Recovery
```

1. Understand the process and control points first.
2. Separate deterministic automation from judgement requiring human review.
3. Use idempotency keys and duplicate protection.
4. Define retry, backoff, dead-letter and manual recovery.
5. Store credentials securely and minimise permissions.
6. Make every run observable with status, timestamps and error references.
7. Preserve evidence and audit events for material actions.
8. Test partial failure, replay, timeout, unavailable dependency and malformed
   input.
9. Provide an operational owner and runbook.

Do not hide a fragile manual process behind a workflow canvas.
