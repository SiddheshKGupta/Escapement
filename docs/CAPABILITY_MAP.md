# Capability Map

## Architecture

```text
Kernel
→ Domain profile
→ Doctrine packs
→ Native skills
→ Capability strengths
→ Fresh-context agents
→ Approved external resources
→ Evidence and handoff
```

## Inventory

```text
Doctrine packs:         11
Native skills:          32
Capability strengths:   58
Agent patterns:         21
External resources:     54
Capability families:    10
Overlap groups:         10
Strategy adapters:      10
```

## Native Skills

| Skill | Phases | Overlap group |
|---|---|---|
| `project-discovery` | DISCOVER, SPECIFY | `discovery-planning` |
| `consulting-analysis` | DISCOVER, RESEARCH, BRAINSTORM, SPECIFY, VERIFY | `consulting-analysis` |
| `governance-risk-controls` | DISCOVER, SPECIFY, VERIFY | `governance-controls` |
| `finance-reporting` | RESEARCH, SPECIFY, IMPLEMENT, VERIFY | `finance-analysis` |
| `dashboard` | SPECIFY, IMPLEMENT, VERIFY | `dashboard-reporting` |
| `workflow` | DISCOVER, SPECIFY, IMPLEMENT, VERIFY | `workflow-design` |
| `engineering-review` | BRAINSTORM, SPECIFY, PLAN, IMPLEMENT, VERIFY | `engineering-review` |
| `design-system` | BRAINSTORM, SPECIFY | `design-direction` |
| `enterprise-ui-review` | IMPLEMENT, VERIFY, POLISH | `ui-quality` |
| `api-integration` | SPECIFY, PLAN, IMPLEMENT, VERIFY | `integration` |
| `artifact-production` | SPECIFY, IMPLEMENT, VERIFY, POLISH, RELEASE | `artifact-production` |
| `writing-quality` | IMPLEMENT, VERIFY, POLISH | `writing-quality` |
| `security-review` | RESEARCH, SPECIFY, PLAN, VERIFY, RELEASE | `security-review` |
| `release-readiness` | RELEASE | `release` |
| `reference-router` | DISCOVER, RESEARCH, BRAINSTORM, PLAN | `external-discovery` |
| `skill-governance` | DISCOVER, RESEARCH, PLAN, VERIFY | `meta-governance` |
| `decision-coach` | DISCOVER | `decision-discovery` |
| `domain-research` | RESEARCH | `domain-research` |
| `solution-brainstorming` | BRAINSTORM | `solution-brainstorming` |
| `delivery-planning` | PLAN | `delivery-planning` |
| `agent-orchestration` | PLAN, IMPLEMENT | `agent-orchestration` |
| `agent-blueprint-discovery` | RESEARCH, BRAINSTORM, PLAN | `agent-blueprint-discovery` |
| `product-specification` | SPECIFY | `product-specification` |
| `data-engineering` | SPECIFY, PLAN, IMPLEMENT, VERIFY | `data-engineering` |
| `frontend-implementation` | IMPLEMENT | `frontend-implementation` |
| `quality-engineering` | PLAN, IMPLEMENT, VERIFY, RELEASE | `quality-engineering` |
| `ai-agent-engineering` | SPECIFY, PLAN, IMPLEMENT, VERIFY | `ai-agent-engineering` |
| `automation-engineering` | SPECIFY, PLAN, IMPLEMENT, VERIFY | `automation-engineering` |
| `data-analysis` | RESEARCH, SPECIFY, IMPLEMENT, VERIFY | `data-analysis` |
| `legal-compliance-analysis` | RESEARCH, SPECIFY, VERIFY | `legal-compliance-analysis` |
| `investment-analysis` | RESEARCH, BRAINSTORM, SPECIFY, VERIFY | `investment-analysis` |
| `software-implementation` | IMPLEMENT | `software-implementation` |

## Capability Families

| Family | Canonical native skills | Fine-grained intents |
|---|---|---:|
| `business-consulting` | decision-coach, consulting-analysis, project-discovery | 11 |
| `governance-risk-controls` | governance-risk-controls, workflow, security-review | 11 |
| `finance-and-private-capital` | finance-reporting, consulting-analysis, dashboard | 12 |
| `product-management` | project-discovery, solution-brainstorming, delivery-planning | 18 |
| `data-engineering-and-analytics` | finance-reporting, dashboard, engineering-review, api-integration | 20 |
| `engineering` | engineering-review, api-integration, security-review, release-readiness | 27 |
| `ai-and-automation` | agent-blueprint-discovery, agent-orchestration, api-integration, security-review | 17 |
| `design-and-experience` | design-system, enterprise-ui-review, writing-quality | 13 |
| `documentation-and-artifacts` | artifact-production, writing-quality | 15 |
| `connectors-and-platforms` | api-integration, reference-router, security-review | 22 |

## Agent Patterns

Agents are fresh-context roles. They do not become permanent global personas.

| Agent | Name | Category | Use |
|---|---|---|---|
| `planner` | Planner | delivery | A material feature needs decomposition, dependencies, risks, and verification before implementation. |
| `evaluator` | Independent Evaluator | verification | Implementation needs assessment from a fresh context against explicit acceptance criteria. |
| `security-reviewer` | Security Reviewer | security | Auth, permissions, hooks, MCP, privacy, secrets, or deployment changes are material. |
| `browser-verifier` | Browser Verifier | frontend | A UI change needs accessibility-tree, interaction, screenshot, or responsive evidence. |
| `research-agent` | Grounded Research Agent | research | A task requires current external facts, primary-source discovery, or multi-step research. |
| `workflow-analyst` | Workflow Analyst | business-analysis | A process requires states, owners, exceptions, SLA, controls, and audit. |
| `dashboard-analyst` | Dashboard Analyst | analytics | Management needs traceable KPIs, drill-down, reconciliation, and decision support. |
| `design-system-architect` | Design System Architect | design | A product needs tokens, components, design-code handoff, or a product DESIGN.md. |
| `mcp-builder` | MCP Builder | integration | An approved external service should be exposed to agents through MCP. |
| `cleanup-agent` | Deterministic Cleanup Agent | maintenance | A repository needs dead-code or dependency cleanup with explainable proof. |
| `memory-architect` | Memory Architect | state | File-based state is insufficient and a project has a justified graph/vector memory requirement. |
| `harness-optimizer` | Harness Optimizer | harness | Repeated failures show that instructions, tools, environment, state, or feedback need adjustment. |
| `consulting-principal` | Consulting Principal | consulting | A material recommendation needs an independent management-outcome and implementation review. |
| `cto-reviewer` | CTO Reviewer | engineering | A product or architecture decision needs independent technical credibility, security, scale, and debt review. |
| `governance-reviewer` | Governance Reviewer | governance | A workflow or policy needs independent review of authority, controls, evidence, exceptions, and reporting. |
| `artifact-editor` | Artifact Editor | communication | A completed business artifact needs a fresh-context quality, structure, and style pass. |
| `decision-facilitator` | Decision Facilitator | discovery | A rough request contains hidden decisions or unclear success criteria. |
| `domain-standards-researcher` | Domain and Standards Researcher | research | Industry, jurisdiction, regulation, standards or current practice can change the recommendation. |
| `solution-architect-brainstormer` | Solution Brainstormer | planning | A material solution needs genuinely different alternatives before planning. |
| `parallel-work-coordinator` | Parallel Work Coordinator | orchestration | A plan contains independent tasks that can be delegated safely. |
| `agent-blueprint-scout` | Agent Blueprint Scout | agent-engineering | A domain problem may have an existing agent implementation worth reusing. |

## External Resources

See:

```text
docs/REFERENCE_CATALOG.md
catalog/capability-registry.json
```

External resources are never marked active merely because they are listed.

## Readiness States

```text
internal
installed
catalogued
optional
conditional
reference-only
preserved-unresolved
```

Generate a task-specific audit:

```bash
python scripts/escapement.py capability-audit "<task>" --markdown
```
