---
name: ai-agent-engineering
description: Use to specify, build or review AI agents, LangGraph or LangChain systems, RAG, tool calling, memory, structured extraction, multi-agent workflows, evaluations, human approval and agent deployment. Do not deploy a catalogue blueprint without validating the exact repository.
---

# AI Agent Engineering

Define:

```text
Outcome | Users | Model role | Inputs | State | Memory | Tools
Knowledge | Orchestration | Human approval | Guardrails | Evaluation
Observability | Cost | Privacy | Failure handling | Deployment
```

1. Decide whether an agent is necessary; prefer deterministic software for
   deterministic work.
2. Define the agent boundary and allowed autonomy.
3. Use explicit schemas for state, tools and outputs.
4. Separate retrieval, reasoning, action and verification.
5. Apply least privilege and human approval to sensitive actions.
6. Design retries, idempotency, timeouts and fallbacks.
7. Build task-specific evaluations before production use.
8. Record model, prompt, tool, data and version lineage.
9. Monitor quality, latency, cost, failures and unsafe behaviour.

An impressive demo is not production readiness.
