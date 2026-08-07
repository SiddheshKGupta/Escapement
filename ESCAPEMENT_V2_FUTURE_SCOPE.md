# Escapement v2.0
## Future Scope of Work

> **Status:** Future roadmap only  
> **Target:** Escapement v2.0  
> **Principle:** Keep the repository-native harness stable, evidence-based, low-token, and battle-tested before expanding the product surface.

---

## 1. Purpose

Escapement v2.0 should evolve the project from a repository-native AI-assisted delivery harness into a portable execution control plane for coding agents and AI-assisted delivery environments.

The objective is not to turn Escapement into another model provider, another coding agent, another MCP marketplace, or another large prompt framework.

The objective is to preserve the current strengths of Escapement while making them available through cleaner interfaces, smarter execution controls, broader host compatibility, provider-aware routing, and stronger cross-host evidence.

The intended evolution is:

```text
Repository-native harness
        ↓
Stable Escapement core
        ↓
Provider-aware execution control
        ↓
Portable host/provider adapters
        ↓
CLI + MCP + plugins
        ↓
Cross-host validation
        ↓
Optional team and enterprise surfaces
```

Escapement should remain provider-agnostic, model-agnostic, host-aware, and repository-centered.

---

# 2. Proposed v2.0 Identity

> **A provider-agnostic execution control plane for AI-assisted software delivery.**

This positioning should only become public once the implementation and cross-host validation support it.

Escapement v2.0 should not be defined as "an MCP server".

MCP should be one interface into the Escapement core.

```text
                         ESCAPEMENT CORE
                                │
               ┌────────────────┼────────────────┐
               │                │                │
          Runtime Engine   Policy Engine   Execution Governor
               │                │                │
               └────────────────┼────────────────┘
                                │
                         Stable Core API
                                │
      ┌─────────────────────────┼─────────────────────────┐
      │                         │                         │
     CLI                    MCP Server                Host Plugins
                                                        │
                                   ┌────────────────────┼────────────────────┐
                                   ↓                    ↓                    ↓
                              Claude Code             Codex             Gemini CLI
```

The same core should also support broader hosts, gateways, and local runtimes through adapters.

---

# 3. Integration Taxonomy

One of the major v2.0 architecture rules is that Escapement should not treat every external AI environment as the same kind of thing.

Cursor, OpenRouter, Ollama, Kiro, Claude Code, and Kimi are not equivalent integration surfaces.

Escapement should distinguish at least four classes:

```text
HOST ADAPTER
Where the agent actually operates.

PROVIDER ADAPTER
The model provider and model-capability layer.

GATEWAY ADAPTER
A routing layer that provides access to multiple model providers.

LOCAL RUNTIME ADAPTER
A local inference system.
```

Recommended interfaces:

```text
HostAdapter
ProviderAdapter
GatewayAdapter
LocalRuntimeAdapter
```

This separation should prevent provider, billing, quota, model, and host assumptions from leaking into the Escapement kernel.

---

# 4. Target Ecosystem Coverage

## 4.1 Initial Reference Hosts

These should be the first deeply validated host implementations:

```text
Claude Code
Codex
Gemini CLI
```

They should become the reference implementations for the adapter architecture because they represent materially different execution environments.

---

## 4.2 Major Developer Hosts

The architecture should explicitly support future adapters for:

```text
Cursor
Kiro
GitHub Copilot
Kimi Code / Kimi CLI
OpenCode
Cline
Windsurf
Google Antigravity
Aider
other repository-aware coding agents
```

Support should be capability-based rather than logo-based.

Escapement must not claim full support merely because a host can read `AGENTS.md`.

Each adapter should declare what is actually supported.

---

## 4.3 Direct Model Providers

Potential provider adapters include:

```text
Anthropic
OpenAI
Google
Moonshot / Kimi
Mistral
DeepSeek
Qwen-compatible providers
other API-accessible model providers
```

These provider adapters should describe model capabilities and economics, not host lifecycle behavior.

---

## 4.4 Model Gateways

Potential gateway adapters include:

```text
OpenRouter
LiteLLM
enterprise model gateways
custom OpenAI-compatible gateways
```

A gateway adapter may expose multiple providers and models through one billing or routing surface.

This is especially important for future execution-channel optimization.

---

## 4.5 Local Inference Runtimes

Potential local-runtime adapters include:

```text
Ollama
LM Studio
vLLM
llama.cpp-compatible runtimes
other local OpenAI-compatible endpoints
```

Local execution should be treated as a first-class option where:

- privacy matters;
- marginal token cost should be near zero;
- the task is narrow enough for the available local model;
- quality requirements allow it;
- data should remain on-device or on-premise.

Local models should not automatically replace frontier or workhorse cloud models for high-risk decisions.

---

# 5. Feature Detection Before Brand Detection

Escapement should avoid logic like:

```python
if host == "cursor":
    ...
elif provider == "openrouter":
    ...
elif model == "kimi":
    ...
```

throughout the codebase.

Instead, runtime behavior should be based on declared capabilities.

Potential host capabilities:

```text
repository_instructions
automatic_bootstrap
lifecycle_hooks
MCP
tool_use
model_selection
model_discovery
quota_discovery
token_usage
turn_interrupt
subagents
parallel_execution
worktree_support
persistent_state
plugin_support
```

Potential model capabilities:

```text
tool_use
structured_output
reasoning_control
context_size
vision
code_strength
agentic_execution
local_execution
cost
latency
streaming
long_context
```

The selection path should become:

```text
Task requirements
      ↓
Required capabilities
      ↓
Available execution channels
      ↓
User policy + economics
      ↓
Best eligible route
```

---

# 6. Adapter Capability Manifests

Every host/provider/runtime adapter should expose a capability manifest.

Example host manifest:

```yaml
host: cursor

capabilities:
  repository_instructions: true
  automatic_bootstrap: true
  lifecycle_hooks: partial
  mcp: true
  model_selection: true
  model_discovery: true
  quota_discovery: false
  token_usage: partial
  turn_interrupt: unknown
  subagents: true
  parallel_execution: true
  worktrees: host_dependent
```

Example local runtime:

```yaml
runtime: ollama

capabilities:
  local: true
  model_discovery: true
  token_usage: true
  context_window_discovery: true
  privacy_local: true
  tool_use: model_dependent
  reasoning_control: model_dependent
  monetary_cost_tracking: not_required
```

Escapement should use these manifests to determine which governance mechanisms can actually be enforced.

---

# 7. Stable Escapement Core API

## Objective

Move fundamental runtime logic behind a stable internal API so the CLI, MCP server, plugins, tests, and future interfaces all use the same implementation.

### Proposed structure

```text
escapement/
├── core/
│   ├── runtime.py
│   ├── routing.py
│   ├── context.py
│   ├── policy.py
│   ├── evidence.py
│   ├── programs.py
│   └── state.py
│
├── execution/
│   ├── governor.py
│   ├── budgets.py
│   ├── model_router.py
│   ├── channel_router.py
│   └── failure_attribution.py
│
├── adapters/
│   ├── hosts/
│   │   ├── claude_code.py
│   │   ├── codex.py
│   │   ├── gemini_cli.py
│   │   ├── cursor.py
│   │   ├── kiro.py
│   │   ├── kimi.py
│   │   └── ...
│   │
│   ├── providers/
│   │   ├── anthropic.py
│   │   ├── openai.py
│   │   ├── google.py
│   │   ├── moonshot.py
│   │   └── ...
│   │
│   ├── gateways/
│   │   ├── openrouter.py
│   │   ├── litellm.py
│   │   └── ...
│   │
│   └── local/
│       ├── ollama.py
│       ├── lmstudio.py
│       └── ...
│
└── interfaces/
    ├── cli.py
    └── mcp.py
```

The real capability should be something like:

```python
result = runtime.start_turn(...)
```

The CLI, MCP server, plugins, tests, and adapters should all call the same core.

---

# 8. Installable Package

Potential distribution:

```text
pip
pipx
uvx
GitHub release
host plugin
MCP package
```

Possible future usage:

```bash
pipx install escapement
```

or:

```bash
uvx escapement init .
```

Installation and updates must preserve:

- framework-managed files;
- project-owned state;
- runtime-generated evidence;
- external-resource governance;
- backups;
- drift detection;
- safe repair;
- rollback.

---

# 9. Execution Governor

The Execution Governor should become one of the defining v2.0 capabilities.

## 9.1 Objective

Control:

- execution channel;
- provider;
- gateway;
- model;
- reasoning level;
- context;
- tokens;
- quota;
- monetary budget;
- wall-clock time;
- subagents;
- parallelism;
- retries.

The objective is to maximize useful delivery within the user's actual resource constraints.

---

## 9.2 Execution Channels

Escapement should think in execution channels, not only models.

Example:

```yaml
execution_channels:

  claude_subscription:
    type: host_subscription
    host: claude-code
    provider: anthropic

  codex_subscription:
    type: host_subscription
    host: codex
    provider: openai

  openrouter:
    type: payg_gateway
    gateway: openrouter
    budget_usd: 25

  local:
    type: local_runtime
    runtime: ollama
```

Future selection could consider:

```text
quality required
privacy
latency
available allowance
monetary price
context requirement
model availability
host capability
user preference
```

This is more durable than routing only among model names.

---

## 9.3 Provider Capability Handshake

Before routing:

```text
Identify host
        ↓
Identify provider / gateway / local runtime
        ↓
Identify authentication mode
        ↓
Identify billing mode where possible
        ↓
Discover model availability
        ↓
Discover quota / rate limits where possible
        ↓
Apply user execution policy
        ↓
Create runtime capability map
```

Escapement should distinguish:

```text
AVAILABLE
Can this execution channel access the model?

ENTITLED
Is the model included in the user's current subscription or allowance?

AFFORDABLE
Does it fit quota or monetary policy?

APPROPRIATE
Does the task materially benefit from it?
```

---

## 9.4 Model Roles

Core policy should use roles:

```text
STANDARD
Strong default for ordinary work.

REASONER
Higher-capability model for planning, architecture,
diagnosis, and difficult decisions.

FRONTIER
Highest available capability for exceptional,
high-value or unresolved work.

ECONOMY
Optional lower-cost capability when quality policy permits.
```

Provider mappings should live in adapters or data files.

Example only:

```yaml
claude:
  standard: sonnet
  reasoner: opus
  frontier: fable
  economy:
    enabled: false
```

Do not permanently encode model version numbers into the kernel.

---

## 9.5 Claude Quality Floor

For the current Claude strategy, Escapement should allow Sonnet-class capability to act as the default quality floor.

Haiku-class routing should not be automatic merely because it is cheaper.

Economy routing should be explicitly enabled by policy or used only for narrow background work where quality has been demonstrated.

The architecture must still allow this policy to change later as model families change.

---

## 9.6 Local Runtime Strategy

Local runtimes such as Ollama should be usable for suitable workloads.

Candidate tasks:

```text
repository indexing
historical log summarization
classification
structured extraction
observability analysis
garbage-collection analysis
low-risk repetitive transformations
offline/private analysis
```

Example:

```text
Task: summarize 40 historical turn records

Local model capable? YES
Sensitive data? YES
Quality requirement: MODERATE

→ Ollama
→ no cloud token consumption
→ data remains local
```

Counter-example:

```text
Task: select distributed transaction architecture

Materiality: HIGH
Local model confidence: LOW

→ do not use local economy route
→ use REASONER or FRONTIER channel
```

---

## 9.7 Billing Modes

Support:

```text
subscription
subscription + paid usage
PAYG / API
team / business
enterprise
gateway-managed
local
unknown / host-managed
```

Subscription optimization:

- preserve quota;
- respect reset windows;
- reserve weekly allowance;
- avoid consuming premium-model quota unnecessarily.

PAYG optimization:

- per-task monetary ceilings;
- project budget;
- approval thresholds;
- provider cost comparison.

Local optimization:

- quality;
- privacy;
- latency;
- device capacity;
- context limits.

---

## 9.8 Execution Modes

### CONSERVE

```text
Protect quota and spend aggressively.
Prefer STANDARD.
Use local or cheaper eligible channels where quality permits.
Reduce parallelism.
Frequent checkpoints.
```

### BALANCED

```text
STANDARD for execution.
REASONER for material decisions.
FRONTIER only for exceptional work.
Use local execution for suitable background work.
```

### QUALITY

```text
Higher willingness to use REASONER.
FRONTIER available for high-complexity work.
Larger execution envelopes.
```

### PRIVATE

```text
Prefer local or organization-controlled inference.
Escalate to external providers only with approval.
```

### CUSTOM

User-defined.

Recommended default:

```text
BALANCED
```

---

## 9.9 Escalation and De-escalation

Example:

```text
STANDARD implementation
        ↓
verification failure
        ↓
STANDARD retry
        ↓
same root cause unresolved
        ↓
REASONER diagnosis
        ↓
STANDARD implementation
```

FRONTIER models should usually advise, diagnose, plan, or review rather than perform routine implementation.

---

## 9.10 Budget Governor

Potential controls:

```text
token budget
provider quota delta
weekly allowance delta
financial cost
wall-clock time
subagent count
parallel thread count
retry count
context size
```

Behavior:

```text
70% of envelope
→ stop broad exploration
→ converge
→ finish smallest coherent slice
→ verify
→ persist handoff

100% of envelope
→ interrupt where supported
→ PARTIAL / BLOCKED
→ exact next action
```

PROGRAM work should be sliced rather than allowed to consume an entire allowance in one run.

---

# 10. Local Escapement MCP Server

## Objective

Expose the core through a compact MCP interface.

MCP is an interface, not Escapement's identity.

Initial target:

```text
local-first
stdio
no mandatory remote service
no central telemetry
no production credentials by default
repository remains system of record
```

### Read-oriented tools

```text
escapement_status
escapement_inspect
escapement_explain_route
escapement_capability_audit
escapement_execution_plan
escapement_context_health
escapement_observability
```

### State-changing tools

```text
escapement_start_turn
escapement_replan
escapement_advance_phase
escapement_register_module
escapement_close_turn
```

### Later execution tools

```text
escapement_run_check
escapement_execute_slice
escapement_interrupt
```

---

# 11. MCP Resources

Potential resources:

```text
escapement://project/state
escapement://project/context
escapement://domain/context
escapement://turn/current
escapement://capabilities/active
escapement://program/modules
escapement://evidence/latest
```

This should reduce the need for every host to understand Escapement's physical file layout.

---

# 12. MCP Risk Classes

Every exposed capability should carry Escapement-enforced risk classification:

```text
READ
STATE_CHANGE
EXECUTION
EXTERNAL_SIDE_EFFECT
DESTRUCTIVE
```

Risk policy must be enforced by Escapement itself.

---

# 13. Tool Context Broker

External tools and MCP definitions should be progressively discovered.

```text
Capability index
      ↓
Search / route
      ↓
Small shortlist
      ↓
Load detailed schemas
      ↓
Invoke selected tool
```

The model should not receive the complete schema of every external resource in every turn.

---

# 14. Host Adapter Layer

Adapters should be planned for:

```text
Claude Code
Codex
Gemini CLI
Cursor
Kiro
GitHub Copilot
Kimi Code / Kimi CLI
OpenCode
Cline
Windsurf
Google Antigravity
Aider
other repository-aware agents
```

Each adapter should define:

```text
instruction discovery
automatic hooks
manual bootstrap
MCP
model discovery
model selection
quota discovery
token usage
interrupt support
subagents
parallel work
worktrees
plugin system
persistent state
known limitations
```

---

# 15. Provider, Gateway, and Local Runtime Layer

Potential adapters:

## Providers

```text
Anthropic
OpenAI
Google
Moonshot / Kimi
Mistral
DeepSeek
Qwen-compatible providers
```

## Gateways

```text
OpenRouter
LiteLLM
enterprise gateways
custom OpenAI-compatible gateways
```

## Local runtimes

```text
Ollama
LM Studio
vLLM
llama.cpp-compatible runtimes
```

The architecture should allow new adapters without modifying the core execution logic.

---

# 16. Host Conformance Lab

Suggested structure:

```text
evals/hosts/
├── shared/
├── claude-code/
├── codex/
├── gemini-cli/
├── cursor/
├── kiro/
├── kimi/
├── copilot/
└── ...
```

Measure:

```text
Kernel discovered?
Runtime invoked?
Task classified correctly?
Material questions respected?
Phase plan followed?
Capabilities routed?
Approval gates respected?
Evidence created?
PARTIAL handled truthfully?
Context consumed?
Token / quota usage?
Wall time?
Final functional result?
```

Support should be published by evidence level.

Potential levels:

```text
DISCOVERED
BOOTSTRAP-VALIDATED
RUNTIME-VALIDATED
LIFECYCLE-VALIDATED
BATTLE-TESTED
HOST-LIMITED
EXPERIMENTAL
```

---

# 17. Context Utility and Context-Rot Detection

Measure:

```text
kernel tokens
project-context tokens
domain-context tokens
skill tokens
tool-schema tokens
tool-result tokens
conversation tokens
external-evidence tokens
generated tokens
```

Potential command:

```bash
escapement context-health
```

Use observed degradation rather than one universal fixed reset threshold.

---

# 18. Context and Tool Trust Firewall

Potential provenance classes:

```text
USER_AUTHORIZED
TRUSTED_PROJECT
APPROVED_INTERNAL
APPROVED_EXTERNAL
UNTRUSTED_WEB
UNTRUSTED_REPOSITORY
UNTRUSTED_MCP_OUTPUT
DERIVED_MEMORY
```

Core rule:

```text
Untrusted information may influence reasoning.

Untrusted information does not establish authority.
```

Untrusted context must not independently authorize privileged operations.

---

# 19. Worktree Isolation Manager

Potential commands:

```bash
escapement isolate create billing
escapement isolate run billing
escapement isolate verify billing
escapement isolate merge billing
escapement isolate destroy billing
```

Each task should receive isolated branch/worktree, runtime state, evidence, and host context where supported.

---

# 20. Sprint Contracts

Example:

```yaml
slice: billing-engine

objective:
  calculate lease invoices correctly

inputs:
  - approved schema
  - approved tax rules

done_when:
  - billing calculation implemented
  - API exposed
  - negative scenarios handled
  - unit tests pass
  - reconciliation evidence produced

must_not:
  - change approved schema without approval
  - add dependency without approval

verification:
  - unit-tests
  - reconciliation-check
```

---

# 21. Failure Attribution Engine

Suggested categories:

```text
REQUIREMENT
SPECIFICATION
CONTEXT
ROUTING
TOOL
MODEL
PROVIDER
HOST
IMPLEMENTATION
INTEGRATION
ENVIRONMENT
SECURITY
HARNESS
```

The attribution engine should distinguish model weakness from host limitation, provider limitation, poor context, routing failure, and implementation failure.

---

# 22. Harness Ablation Lab

Potential registry:

```text
catalog/harness-components.json
```

Potential command:

```bash
escapement ablate decision-coach
```

Compare:

```text
success rate
verification rate
token use
wall time
tool calls
user corrections
retries
specification defects
final quality
```

The purpose is to learn which mechanisms are genuinely load-bearing.

---

# 23. Harness Garbage Collector

Potential command:

```bash
escapement gc --check
```

Detect:

```text
unused native skills
routed-but-never-used capabilities
duplicate rules
overlapping doctrine
oversized skill files
obsolete provider aliases
dead external repositories
deprecated MCP references
stale documentation
orphaned decisions
stale evidence
unreferenced artifacts
```

GC should recommend or prepare reviewable changes, not autonomously rewrite doctrine.

---

# 24. Portable Execution Trace

Potential trace fields:

```text
turn ID
host
provider
gateway
local runtime
model role
resolved model
reasoning level
execution mode
parent agent
subagents
context-pack hashes
skills selected
skills invoked
external capabilities
tool calls
files changed
commands
check IDs
token usage
quota movement
financial cost
wall time
commit
closure result
```

Potential exporters:

```text
Escapement JSONL
OpenTelemetry / OTLP
Agent-trace compatible export
```

---

# 25. Outcome Contract

Potential file:

```text
PROJECT_OUTCOME.yaml
```

Example:

```yaml
primary_outcome:
  reduce invoice reconciliation effort

success:
  - unmatched transactions visible
  - every KPI traceable to records
  - month-end reconciliation reproducible

priorities:
  correctness: 1
  auditability: 2
  usability: 3
  delivery_speed: 4

constraints:
  - no fabricated business data
  - no production writes without approval

execution:
  mode: balanced

non_goals:
  - predictive analytics
  - ERP replacement
```

---

# 26. Plugin and Distribution Layer

Potential future surfaces:

```text
Claude Code plugin
Codex / OpenAI plugin packaging where supported
Gemini integration package
Cursor integration package
Kiro integration package
Kimi integration package
MCP registry listing
GitHub release package
```

Plugins should remain distribution wrappers around the same Escapement core.

---

# 27. Optional Escapement UI

Possible future management view:

```text
ESCAPEMENT
────────────────────────────────

Project       Smart Leasing
Tier          PROGRAM
Phase         IMPLEMENT

Execution     BALANCED
Host          Claude Code
Provider      Anthropic
Channel       Subscription
Model Role    STANDARD

Context       47%
Task Budget   31%
Weekly Quota  62% remaining

Capabilities
✓ software-implementation
✓ api-integration
✓ governance-risk-controls

Evidence
✓ unit tests
○ integration
○ UI verification
```

Potential UI:

- execution-plan review;
- approvals;
- context health;
- quota/budget visibility;
- model/channel routing explanation;
- phase history;
- program modules;
- evidence;
- failure attribution;
- host conformance;
- observability.

---

# 28. Optional Remote / Team Escapement

Potential capabilities:

```text
shared policy
approved external capability catalogue
organization model/provider policy
organization budgets
team observability
shared capability governance
central audit records
managed approvals
host compatibility reporting
private gateway support
local/on-prem inference policy
```

Remote Escapement should remain optional.

---

# 29. Proposed v2.0 Delivery Sequence

## Phase 1: Internal Architecture

```text
Stable Core API
Adapter interfaces
Execution Governor architecture
Execution policy schema
Refactor CLI onto Core API
```

## Phase 2: Provider-Aware Execution

```text
Model roles
Execution channels
Billing modes
Quality floor
Budget Governor
Escalation / de-escalation
Claude adapter
Codex adapter
Gemini adapter
OpenRouter adapter
Ollama adapter
Execution-plan reporting
```

## Phase 3: Portability

```text
Installable package
Local MCP server
MCP Resources
Risk classification
Tool Context Broker
```

## Phase 4: Cross-Host Expansion

```text
Cursor
Kiro
Kimi
Copilot
OpenCode
Cline
Windsurf
Antigravity
other adapters
```

## Phase 5: Cross-Host Reliability

```text
Host Conformance Lab
Codex battle testing
Gemini lifecycle testing
Cursor lifecycle testing
Kiro lifecycle testing
Kimi lifecycle testing
Cross-host evidence comparison
```

## Phase 6: Harness Intelligence

```text
Context health
Failure attribution
Sprint contracts
Harness ablation
Harness garbage collector
Portable tracing
```

## Phase 7: Productization

```text
Host plugins
MCP registry distribution
Optional management UI
Optional remote/team control plane
```

---

# 30. Proposed v2.0 Exit Criteria

Escapement should not become v2.0 merely because an MCP server exists.

Recommended threshold:

```text
[ ] Stable internal Core API
[ ] Existing CLI migrated to Core API
[ ] HostAdapter interface
[ ] ProviderAdapter interface
[ ] GatewayAdapter interface
[ ] LocalRuntimeAdapter interface
[ ] Execution Governor implemented
[ ] Claude adapter validated
[ ] Codex adapter validated
[ ] Gemini adapter validated
[ ] At least one gateway adapter validated
[ ] At least one local-runtime adapter validated
[ ] Budget controls validated on real Codex usage
[ ] Model routing respects user policy and availability
[ ] Local MCP server
[ ] MCP risk controls
[ ] Host Conformance Lab
[ ] Real-project lifecycle completed on Claude Code
[ ] Real-project lifecycle completed on Codex
[ ] Cross-host evidence documented
[ ] Backward-compatible v1.x installation path
[ ] Upgrade path from v1.x
[ ] Security review complete
[ ] Validation suite clean
[ ] Honest boundaries documented
```

Cursor, Kiro, Kimi, Copilot, OpenCode, Cline, Windsurf, Antigravity, and other hosts can continue to expand through adapter milestones without blocking initial v2.0 if the adapter architecture itself is proven.

---

# 31. Explicit Non-Goals

Escapement v2.0 should not automatically become:

- a mandatory hosted SaaS;
- an LLM provider;
- a mandatory model gateway;
- another AI coding agent;
- a mandatory vector database;
- a giant MCP marketplace;
- an autonomous self-rewriting framework;
- an unrestricted multi-agent swarm;
- a replacement for Git;
- a replacement for CI/CD;
- a production deployment platform;
- an unrestricted security testing platform;
- a central store for user source code;
- a system that requires frontier models;
- a system that assumes every user has the same subscription;
- a system that assumes cloud inference is always preferable;
- a system that assumes local inference is always sufficient.

---

# 32. Compatibility Principle

A user should still be able to:

```text
install Escapement
        ↓
use the repository as system of record
        ↓
run a supported coding agent
        ↓
receive structured context, routing, governance,
verification and handoff
```

without:

```text
creating an Escapement account
running a remote MCP service
buying another subscription
using one specific model provider
using one specific gateway
enabling central telemetry
```

---

# 33. Recommended v2.0 Architecture

```text
                                USER
                                  │
                                  ↓
                       ┌─────────────────────┐
                       │    ESCAPEMENT       │
                       │   EXECUTION PLAN    │
                       └──────────┬──────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  ↓               ↓               ↓
             Policy Engine   Context Engine   Program State
                  │               │               │
                  └───────────────┼───────────────┘
                                  ↓
                       EXECUTION GOVERNOR
                                  │
          ┌───────────────────────┼───────────────────────┐
          ↓                       ↓                       ↓
   Channel Router           Budget Governor          Model Router
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  ↓
                         ADAPTER RESOLUTION
                                  │
             ┌────────────────────┼────────────────────┐
             ↓                    ↓                    ↓
        Host Adapter        Provider/Gateway      Local Runtime
             │                    │                    │
     ┌───────┼────────┐      ┌────┼─────┐        ┌────┼────┐
     ↓       ↓        ↓      ↓    ↓     ↓        ↓         ↓
  Claude   Codex   Cursor  Anth. OpenAI Router  Ollama   LM Studio
             │
             ↓
         EXECUTION
             │
      ┌──────┼─────────┐
      ↓      ↓         ↓
   Tools   Agents   Repository
      │      │         │
      └──────┼─────────┘
             ↓
        VERIFICATION
             ↓
          EVIDENCE
             ↓
     FAILURE ATTRIBUTION
             ↓
       OBSERVABILITY
             ↓
      DURABLE HANDOFF
```

---

# 34. Strategic Positioning

Escapement v1.x is primarily a repository-native governed harness.

Escapement v2.0 can become:

> **A provider-agnostic execution control plane for AI-assisted software delivery, combining bounded context, capability routing, execution-channel selection, model and budget governance, verification, evidence, and durable project state across agent hosts.**

This positioning should only be adopted when implementation and validation support it.

Until then, everything in this document remains future scope rather than a current product claim.

---

# 35. Guiding Rule for v2.0

When considering another mechanism:

```text
Observed failure
      ↓
Can deterministic tooling solve it?
      ↓
Can runtime policy solve it?
      ↓
Can context routing solve it?
      ↓
Can an existing capability solve it?
      ↓
Only then add new doctrine.
```

The goal of v2.0 should not be to make Escapement larger.

The goal should be to make Escapement more:

```text
portable
measurable
economical
enforceable
provider-agnostic
host-aware
privacy-aware
adaptable
```

while preserving the disciplined repository-native model of v1.x.
