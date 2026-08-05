# External References, Skills, Plugins, and Repositories

Reviewed: 2026-08-05  
Machine-readable catalogue: `catalog/external-resources.json`

## Purpose

This file records every external repository, skill, plugin, course, and tool
used as an Escapement reference.

It tells an agent:

- when a resource is relevant;
- whether to integrate it, adapt it, or use it only as reference;
- which licence was observed;
- what approval is required;
- what must not be copied or executed automatically.

## Important licence rule

**A public GitHub repository is not automatically open source.**

Before copying or modifying source:

1. inspect the licence at the exact tag or commit;
2. confirm compatibility with the target project's licence;
3. preserve copyright, licence, and NOTICE obligations;
4. record the dependency or adapted material in third-party notices;
5. request approval for a new dependency, plugin, MCP server, CLI, or service.

### Usage modes

| Mode | Meaning |
|---|---|
| `reference` | Learn principles; do not copy substantial source |
| `adapt` | Reuse or modify under the verified licence and attribution obligations |
| `install` | Install the published skill after approval and source review |
| `integrate` | Use it as an external tool, service, plugin, CLI, or MCP |
| `integrate-separately` | Keep it as a separate deployed/licensed system |
| `integrate-authorised-only` | Use only with explicit scope and authorisation |

## Agent decision sequence

```text
Capability gap
→ Search this catalogue
→ Match trigger and use case
→ Verify current source and licence
→ Inspect security and overlap
→ Prefer integration over copying
→ Request required approval
→ Pin version or commit
→ Record attribution and evidence
→ Install/use
→ Validate
```

## Global prohibitions

The agent must not:

- assume every resource listed here is safe to copy;
- silently install tools, skills, plugins, MCP servers, or dependencies;
- provide credentials to a tool without explicit approval;
- combine overlapping harness systems without a conflict decision;
- run offensive security tooling without written authorisation and scope;
- copy protected branding, imagery, proprietary fonts, or trade dress;
- treat catalogue popularity as proof of quality.

# Catalogue


## awesome-design-md

- Publisher: VoltAgent
- Type: `reference-repository`
- URL: https://github.com/VoltAgent/awesome-design-md
- Licence: **MIT**
- Licence status: `verified-in-prior-review`
- Permitted Escapement mode: `reference`, `adapt`
- Trigger cues: `design system`, `visual direction`, `brand`, `layout`, `colour`, `typography`, `motion`

### Use when

A product needs a design archetype, component language, visual benchmark, or product-specific DESIGN.md.

### How the agent should use it

Read only the relevant company DESIGN.md files, extract principles, and create an original system under client-brand precedence.

### Do not

Do not copy protected logos, proprietary fonts, imagery, screenshots, or another company's trade dress.

### What Escapement takes from it

The 73-company design-intelligence synthesis and design-system routing.

## Perplexity AI GitHub organisation

- Publisher: Perplexity AI
- Type: `organisation-index`
- URL: https://github.com/perplexityai
- Licence: **Per-repository**
- Licence status: `must-verify-per-resource`
- Permitted Escapement mode: `reference`
- Trigger cues: `research`, `search`, `evaluation`, `CLI distribution`, `supply chain`, `MCP`

### Use when

An agent needs current patterns for research tooling, evaluation runners, safe binary distribution, or developer-tool inventory.

### How the agent should use it

Select a specific repository from this catalogue and verify its current licence before reuse.

### Do not

Do not assume every public repository in an organisation has the same licence.

### What Escapement takes from it

Research extension, resumable evals, content-addressed records, self-tests, and safe installers.

## api-platform-developers

- Publisher: Perplexity AI
- Type: `skills-and-plugin-repository`
- URL: https://github.com/perplexityai/api-platform-developers
- Licence: **Apache-2.0**
- Licence status: `verified`
- Permitted Escapement mode: `integrate`, `adapt`
- Trigger cues: `Perplexity`, `live web search`, `page snippets`, `Sonar migration`, `docs MCP`

### Use when

The project needs official Perplexity Agent Skills, a Claude/Codex plugin example, or live documentation through MCP.

### How the agent should use it

Prefer installing the official skill/plugin or using it as the model for portable Agent Skills. Pin a release or commit.

### Do not

Do not make Perplexity credentials or the docs MCP mandatory for Escapement core.

### What Escapement takes from it

Portable skills, plugin manifests, optional docs MCP, and an official research extension.

## pplx CLI

- Publisher: Perplexity AI
- Type: `external-cli`
- URL: https://github.com/perplexityai/perplexity-cli
- Licence: **No licence file observed during review**
- Licence status: `unverified-restrict-copying`
- Permitted Escapement mode: `integrate`, `reference`
- Trigger cues: `live search`, `grounded web research`, `query-relevant snippets`, `Perplexity CLI`

### Use when

A user explicitly wants Perplexity-backed current web search or snippets and can provide an API key.

### How the agent should use it

Use the released CLI as an optional external dependency after approval. Verify checksum and current terms.

### Do not

Do not copy repository code into Escapement or claim open-source reuse until a licence is present and verified.

### What Escapement takes from it

Checksum-verified releases, atomic updates, JSON stdout, and agent-friendly CLI design.

## search_evals

- Publisher: Perplexity AI
- Type: `evaluation-framework`
- URL: https://github.com/perplexityai/search_evals
- Licence: **MIT**
- Licence status: `verified`
- Permitted Escapement mode: `reference`, `adapt`
- Trigger cues: `evaluation`, `benchmark`, `grader`, `cost accounting`, `resumable run`, `trace`

### Use when

Escapement needs reproducible eval suites, provider adapters, task traces, resumable runs, or cost/evidence accounting.

### How the agent should use it

Adapt the run-directory, config-hash, resume, trace, and summary patterns to local harness evaluations.

### Do not

Do not import paid-provider assumptions or third-party benchmark data without accepting their separate terms.

### What Escapement takes from it

Resumable executable evaluations and inspectable per-task traces.

## Bumblebee

- Publisher: Perplexity AI
- Type: `security-inventory-tool`
- URL: https://github.com/perplexityai/bumblebee
- Licence: **Apache-2.0**
- Licence status: `verified`
- Permitted Escapement mode: `integrate`, `reference`, `adapt`
- Trigger cues: `dependency inventory`, `skill inventory`, `MCP inventory`, `supply-chain`, `self-test`, `NDJSON`

### Use when

A security review needs read-only package, skill, editor-extension, or MCP inventory from local metadata.

### How the agent should use it

Prefer invoking Bumblebee externally. Reuse its read-only, profile-based, NDJSON, confidence, and self-test patterns where useful.

### Do not

Do not expose credentials found in MCP env blocks or broaden scans beyond approved roots.

### What Escapement takes from it

Read-only inventory profiles, structured NDJSON, confidence levels, and built-in self-test.

## Perplexity MCP server

- Publisher: Perplexity AI
- Type: `mcp-repository`
- URL: https://github.com/perplexityai/modelcontextprotocol
- Licence: **Verify current repository licence**
- Licence status: `must-verify`
- Permitted Escapement mode: `integrate`, `reference`
- Trigger cues: `Perplexity MCP`, `research MCP`, `search tool server`

### Use when

A project wants Perplexity search through MCP rather than a CLI.

### How the agent should use it

Install as an optional project MCP after explicit approval, review its tools, permissions, network access, and credential storage.

### Do not

Do not register remote MCP servers silently or make network access part of the default core.

### What Escapement takes from it

Optional freshness and research integrations through a narrow MCP boundary.

## Codescythe

- Publisher: Perplexity AI
- Type: `code-analysis-tool`
- URL: https://github.com/perplexityai/codescythe
- Licence: **Verify current repository licence**
- Licence status: `must-verify`
- Permitted Escapement mode: `integrate`, `reference`
- Trigger cues: `dead code`, `unused exports`, `unused files`, `dependency path`, `cleanup`

### Use when

A TypeScript or JavaScript repository needs deterministic dead-code analysis or dependency-path explanation.

### How the agent should use it

Use as an external check after approval. Run doctor/explain before destructive fix mode and capture output through structured evidence.

### Do not

Do not run destructive fixes without a clean branch, tests, and explicit approval.

### What Escapement takes from it

Narrow deterministic contracts, doctor commands, explainability, and safe destructive-mode gates.

## AppFlowy

- Publisher: AppFlowy-IO
- Type: `product-repository`
- URL: https://github.com/AppFlowy-IO/AppFlowy
- Licence: **AGPL-3.0**
- Licence status: `verified`
- Permitted Escapement mode: `reference`, `integrate-separately`
- Trigger cues: `local-first`, `workspace`, `data ownership`, `self-hosting`, `extensible blocks`

### Use when

Designing local-first state, user-owned data, extensible workspace architecture, or self-hosted collaboration.

### How the agent should use it

Reuse architectural principles or integrate as a separate service under its licence. Review AGPL obligations before copying code.

### Do not

Do not copy AGPL code into Escapement's source-available core without a deliberate licence decision.

### What Escapement takes from it

Privacy-first local control, cross-platform reliability, and extensible building blocks.

## Plausible Analytics

- Publisher: Plausible Insights
- Type: `product-repository`
- URL: https://github.com/plausible/analytics
- Licence: **AGPL-3.0-or-later**
- Licence status: `verified`
- Permitted Escapement mode: `reference`, `integrate-separately`
- Trigger cues: `privacy analytics`, `local observability`, `simple dashboard`, `no cookies`, `self-hosting`

### Use when

Designing privacy-first observability, minimal dashboards, transparent metrics, or optional self-hosted analytics.

### How the agent should use it

Adopt privacy and simplicity principles or integrate a separately deployed instance under its licence.

### Do not

Do not embed AGPL application code into Escapement core without licence review.

### What Escapement takes from it

Local-only telemetry by default, transparent metrics, and clutter-free observability.

## Spec Kit

- Publisher: GitHub
- Type: `specification-framework`
- URL: https://github.com/github/spec-kit
- Licence: **MIT**
- Licence status: `verified`
- Permitted Escapement mode: `reference`, `adapt`, `integrate`
- Trigger cues: `constitution`, `specification`, `implementation plan`, `tasks`, `converge`, `preset`, `bundle`

### Use when

New or material work needs a constitution, executable specification, technical plan, task breakdown, or convergence review.

### How the agent should use it

Use Spec Kit directly or adapt its phases and extension/preset/bundle model with attribution.

### Do not

Do not duplicate its whole command surface in Escapement when an optional integration is sufficient.

### What Escapement takes from it

Constitution → specify → plan → tasks → implement → converge, plus extensions, presets, and bundles.

## 500+ AI Agent Projects & Use Cases

- Publisher: Ashish Patel
- Type: `agent-pattern-catalogue`
- URL: https://github.com/ashishpatel26/500-AI-Agents-Projects
- Licence: **MIT**
- Licence status: `verified-from-readme`
- Permitted Escapement mode: `reference`
- Trigger cues: `agent pattern`, `industry use case`, `framework comparison`, `example agent`

### Use when

An agent needs to discover relevant implementation patterns or comparable industry use cases.

### How the agent should use it

Search the catalogue, inspect the linked source project, and independently verify that project's licence and quality.

### Do not

Do not treat inclusion in a catalogue as proof of safety, quality, maintenance, or licence compatibility.

### What Escapement takes from it

A curated agent-pattern registry rather than hundreds of always-loaded agents.

## Learn Harness Engineering

- Publisher: Walking Labs
- Type: `course-and-reference-repository`
- URL: https://walkinglabs.github.io/learn-harness-engineering/en/
- Source repository: https://github.com/walkinglabs/learn-harness-engineering
- Licence: **MIT**
- Licence status: `verified-from-project-docs`
- Permitted Escapement mode: `reference`, `adapt`
- Trigger cues: `harness`, `state persistence`, `feature list`, `verification loop`, `session lifecycle`, `observability`

### Use when

Creating, assessing, or teaching the instructions, tools, environment, state, and feedback subsystems of a harness.

### How the agent should use it

Use relevant lectures, templates, and projects; compare weak and strong harness outcomes; preserve attribution.

### Do not

Do not load the complete course into every task or confuse a prompt file with a complete harness.

### What Escapement takes from it

Repository as system of record, feature-state primitives, lifecycle bootstrap, verification, and clean session closure.

## harness-creator skill

- Publisher: Walking Labs
- Type: `agent-skill`
- URL: https://github.com/walkinglabs/learn-harness-engineering/tree/main/skills/harness-creator
- Licence: **MIT**
- Licence status: `verified-from-skill-docs`
- Permitted Escapement mode: `install`, `adapt`, `reference`
- Trigger cues: `create harness`, `assess harness`, `improve harness`, `harness benchmark`

### Use when

A project lacks a harness or needs a structured five-subsystem assessment.

### How the agent should use it

Install through the skills ecosystem or reference its SKILL.md; run its evaluations before adopting changes.

### Do not

Do not install it on top of overlapping native Escapement harness skills without an overlap decision.

### What Escapement takes from it

Harness assessment, templates, reference patterns, and benchmark-oriented skill development.

## Penpot

- Publisher: Kaleidos
- Type: `design-platform`
- URL: https://github.com/penpot/penpot
- Licence: **MPL-2.0**
- Licence status: `verified`
- Permitted Escapement mode: `integrate`, `reference`, `adapt-with-file-level-obligations`
- Trigger cues: `design tokens`, `design-code workflow`, `SVG`, `CSS`, `design MCP`, `self-hosted design`

### Use when

A product needs open design tokens, inspectable design-to-code workflows, or an optional design MCP/API.

### How the agent should use it

Prefer integration through its API/MCP or adopt open-standard design-token concepts. Review MPL file-level obligations before code reuse.

### Do not

Do not copy branding or assume a design file alone proves implementation correctness.

### What Escapement takes from it

Design tokens as shared source of truth and programmable design-code integration.

## HelixDB

- Publisher: HelixDB
- Type: `database-and-cli`
- URL: https://github.com/HelixDB/helix-db
- Licence: **Apache-2.0**
- Licence status: `verified`
- Permitted Escapement mode: `integrate`, `reference`, `adapt`
- Trigger cues: `agent memory`, `knowledge graph`, `vector graph`, `local database`, `one-shot bootstrap`

### Use when

A project genuinely needs graph-vector memory, knowledge graphs, or a local agent data layer.

### How the agent should use it

Integrate as an optional data service after architecture approval; adapt its one-shot bootstrap and explainable local setup patterns.

### Do not

Do not make a database mandatory for Escapement's file-based core or add it merely to appear agentic.

### What Escapement takes from it

A guided one-shot bootstrap and optional structured memory backend.

## Agent Reach

- Publisher: Panniantong
- Type: `capability-installer`
- URL: https://github.com/Panniantong/agent-reach
- Licence: **MIT**
- Licence status: `verified-from-readme`
- Permitted Escapement mode: `integrate`, `reference`
- Trigger cues: `internet access`, `social search`, `video transcript`, `RSS`, `platform connector`, `doctor`

### Use when

A user explicitly needs internet/platform access not already available through approved tools.

### How the agent should use it

Use its safe mode, local credential model, doctor, and primary/fallback provider approach after reviewing every installed tool.

### Do not

Do not bypass platform protections, harvest credentials, or install broad internet capabilities without explicit approval.

### What Escapement takes from it

Capability doctor, safe mode, fallback routing, and agent-friendly configuration.

## agent-browser

- Publisher: Vercel Labs
- Type: `browser-automation-cli`
- URL: https://github.com/vercel-labs/agent-browser
- Licence: **Apache-2.0**
- Licence status: `verified`
- Permitted Escapement mode: `integrate`, `reference`
- Trigger cues: `browser test`, `UI verification`, `accessibility snapshot`, `screenshot`, `web workflow`

### Use when

A frontend or end-to-end task needs real browser evidence, accessibility-tree interaction, screenshots, or DOM inspection.

### How the agent should use it

Install as an optional external CLI, pin its version, restrict allowed domains, and capture commands/screenshots as evidence.

### Do not

Do not browse authenticated or sensitive sites without approval or use browser automation as proof when business data is fabricated.

### What Escapement takes from it

Agent-readable accessibility snapshots, early interaction failure, and browser-based verification.

## GSD Core

- Publisher: Open GSD
- Type: `context-and-phase-framework`
- URL: https://github.com/gsd-build/get-shit-done
- Current repository: https://github.com/open-gsd/gsd-core
- Licence: **MIT**
- Licence status: `verified-from-readme`
- Permitted Escapement mode: `reference`, `integrate`, `adapt`
- Trigger cues: `context rot`, `phase loop`, `fresh subagent`, `discuss plan execute verify ship`

### Use when

A project needs phase-level context isolation, fresh execution contexts, or a discuss-plan-execute-verify-ship loop.

### How the agent should use it

Integrate directly or adopt focused context-isolation and phase-verification patterns.

### Do not

Do not run parallel agents when tasks share mutable state or when the repository lacks merge and verification controls.

### What Escapement takes from it

Fresh-context phase execution, lean main sessions, and verified shipping.

## mcp-builder skill

- Publisher: Anthropic
- Type: `agent-skill`
- URL: https://github.com/anthropics/skills/tree/main/skills/mcp-builder
- Licence: **Apache-2.0**
- Licence status: `verified`
- Permitted Escapement mode: `install`, `adapt`, `reference`
- Trigger cues: `build MCP`, `MCP server`, `tool schema`, `MCP evaluation`

### Use when

A project is approved to build an MCP server for an external API or service.

### How the agent should use it

Install or read the skill; research the current MCP specification; design concise tools, schemas, annotations, errors, pagination, and evaluations.

### Do not

Do not expose broad destructive endpoints, secrets, or an unbounded API surface to agents.

### What Escapement takes from it

MCP quality workflow, tool discoverability, output schemas, annotations, and realistic evaluations.

## find-skills skill

- Publisher: Vercel Labs
- Type: `agent-skill`
- URL: https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md
- Licence: **MIT**
- Licence status: `verified`
- Permitted Escapement mode: `install`, `adapt`, `reference`
- Trigger cues: `find a skill`, `install a skill`, `missing capability`, `skill marketplace`

### Use when

A task requires a specialised capability that Escapement core does not own.

### How the agent should use it

Search the skills ecosystem, check source reputation and maintenance, inspect the skill, verify its licence, then request installation approval.

### Do not

Do not recommend or install a skill solely because it ranks highly or has many installs.

### What Escapement takes from it

Reference-router skill and a quality gate before external skill installation.

## ECC

- Publisher: Affaan Mustafa
- Type: `agent-harness-ecosystem`
- URL: https://github.com/affaan-m/ECC
- Licence: **MIT**
- Licence status: `verified-from-readme`
- Permitted Escapement mode: `reference`, `integrate-selectively`
- Trigger cues: `agent harness`, `doctor`, `repair`, `continuous learning`, `agent security`, `cross-runtime sync`

### Use when

Reviewing cross-runtime distribution, doctor/repair, installation conflict detection, skill packaging, or harness security.

### How the agent should use it

Study or integrate narrowly selected capabilities; avoid overlapping full installations in the same agent runtime.

### Do not

Do not copy its hundreds of agents/skills into Escapement core or imply full platform parity.

### What Escapement takes from it

Doctor/repair, official-source warning, install-conflict prevention, security scanning, and support matrix honesty.

## Strix

- Publisher: Strix AI
- Type: `security-testing-tool`
- URL: https://github.com/usestrix/strix
- Licence: **Apache-2.0**
- Licence status: `verified-from-readme`
- Permitted Escapement mode: `integrate-authorised-only`, `reference`
- Trigger cues: `pentest`, `dynamic security test`, `proof of concept`, `DAST`, `security scan`

### Use when

The user has explicit authorisation to dynamically assess a local, owned, or approved target in a sandbox.

### How the agent should use it

Run as an external optional tool with a written scope, exclusions, credentials policy, target approval, and structured evidence.

### Do not

Do not autonomously attack public or third-party targets, run exploits without permission, or place offensive capability in Escapement core.

### What Escapement takes from it

Local run viewer, evidence-rich findings, CI security gates, and sandboxed external security integrations.


# Attribution practice

For any installed or adapted external resource, update:

```text
THIRD_PARTY_NOTICES.md
docs/decisions/DECISION_LOG.md
.escapement-install.json or the project dependency manifest
```

Record:

```text
Name
Source URL
Pinned version or commit
Licence
Files or capability used
Changes made
Reason selected
Alternatives rejected
Security review
Validation evidence
```

# Maintenance

Re-check links, licences, archive status, and recommended install methods before
each Escapement release. A licence status of `must-verify` or
`unverified-restrict-copying` means reference or external integration only until
a current licence is confirmed.
