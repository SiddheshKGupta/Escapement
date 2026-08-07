# External Reference Catalogue

Escapement currently preserves **61** external skills, plugins,
tools, repositories, MCP servers, services and reference systems.

A catalogue entry is a reviewed candidate, not an installed capability. A
resource may be `reference-only`, an `optional` skill, a `conditional`
integration, an external runtime integrated separately, an architecture
reference, or a `META_OBSERVER` -- see [Status meanings](#status-meanings)
below. Being catalogued here never means being active by default.

Machine-readable source:

```text
catalog/capability-registry.json
```

Subskill strengths:

```text
catalog/skill-strengths.json
```

Overlap decisions:

```text
catalog/overlap-matrix.json
```

## Activation contract

```text
Capability gap
→ Search native skills and strengths
→ Select the strongest lifecycle phase
→ Resolve overlap
→ Verify exact source and licence
→ Inspect scripts, hooks, network, credentials and permissions
→ Request approval
→ Pin a version or commit
→ Install or integrate
→ Validate
→ Record attribution and evidence
```

A public repository is not automatically installed, safe, maintained or
compatible.

## Status meanings

| Status | Meaning |
|---|---|
| `preferred-policy` | Recommended behavioural baseline |
| `optional` | May be installed after review |
| `optional-preferred-*` | Strong specialist for a particular phase |
| `conditional` | Requires a demonstrated need and extra governance |
| `reference-only` | Use for principles or design evidence |
| `discovery-only-until-validated` | Use to find exact implementations; never deploy the catalogue entry itself |
| `discouraged-legacy` | Existing-project compatibility only |
| `preserved-unresolved` | Retained but disabled until exact source is confirmed |

# Catalogue

## awesome-design-md

- ID: `voltagent-awesome-design-md`
- Kind: `reference-repository`
- Source: https://github.com/VoltAgent/awesome-design-md
- Publisher: VoltAgent
- Licence: **MIT**
- Licence status: `verified-in-prior-review`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `design-reference`
- Permitted modes: `reference`, `adapt`
- Trigger cues: `design system`, `visual direction`, `brand`, `layout`, `colour`, `typography`, `motion`

### Core strength

A product needs a design archetype, component language, visual benchmark, or product-specific DESIGN.md.

### Do not

Do not copy protected logos, proprietary fonts, imagery, screenshots, or another company's trade dress.

## Perplexity AI GitHub organisation

- ID: `perplexity-org`
- Kind: `organisation-index`
- Source: https://github.com/perplexityai
- Publisher: Perplexity AI
- Licence: **Per-repository**
- Licence status: `must-verify-per-resource`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `research-freshness`
- Permitted modes: `reference`
- Trigger cues: `research`, `search`, `evaluation`, `CLI distribution`, `supply chain`, `MCP`

### Core strength

An agent needs current patterns for research tooling, evaluation runners, safe binary distribution, or developer-tool inventory.

### Do not

Do not assume every public repository in an organisation has the same licence.

## api-platform-developers

- ID: `perplexity-api-platform-developers`
- Kind: `skills-and-plugin-repository`
- Source: https://github.com/perplexityai/api-platform-developers
- Publisher: Perplexity AI
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `research-freshness`
- Permitted modes: `integrate`, `adapt`
- Trigger cues: `Perplexity`, `live web search`, `page snippets`, `Sonar migration`, `docs MCP`

### Core strength

The project needs official Perplexity Agent Skills, a Claude/Codex plugin example, or live documentation through MCP.

### Do not

Do not make Perplexity credentials or the docs MCP mandatory for Escapement core.

## pplx CLI

- ID: `perplexity-cli`
- Kind: `external-cli`
- Source: https://github.com/perplexityai/perplexity-cli
- Publisher: Perplexity AI
- Licence: **No licence file observed during review**
- Licence status: `unverified-restrict-copying`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `research-freshness`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `live search`, `grounded web research`, `query-relevant snippets`, `Perplexity CLI`

### Core strength

A user explicitly wants Perplexity-backed current web search or snippets and can provide an API key.

### Do not

Do not copy repository code into Escapement or claim open-source reuse until a licence is present and verified.

## search_evals

- ID: `perplexity-search-evals`
- Kind: `evaluation-framework`
- Source: https://github.com/perplexityai/search_evals
- Publisher: Perplexity AI
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `evaluation`
- Permitted modes: `reference`, `adapt`
- Trigger cues: `evaluation`, `benchmark`, `grader`, `cost accounting`, `resumable run`, `trace`

### Core strength

Escapement needs reproducible eval suites, provider adapters, task traces, resumable runs, or cost/evidence accounting.

### Do not

Do not import paid-provider assumptions or third-party benchmark data without accepting their separate terms.

## Bumblebee

- ID: `perplexity-bumblebee`
- Kind: `security-inventory-tool`
- Source: https://github.com/perplexityai/bumblebee
- Publisher: Perplexity AI
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `security-testing`
- Permitted modes: `integrate`, `reference`, `adapt`
- Trigger cues: `dependency inventory`, `skill inventory`, `MCP inventory`, `supply-chain`, `self-test`, `NDJSON`

### Core strength

A security review needs read-only package, skill, editor-extension, or MCP inventory from local metadata.

### Do not

Do not expose credentials found in MCP env blocks or broaden scans beyond approved roots.

## Perplexity MCP server

- ID: `perplexity-modelcontextprotocol`
- Kind: `mcp-repository`
- Source: https://github.com/perplexityai/modelcontextprotocol
- Publisher: Perplexity AI
- Licence: **Verify current repository licence**
- Licence status: `must-verify`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `research-freshness`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `Perplexity MCP`, `research MCP`, `search tool server`

### Core strength

A project wants Perplexity search through MCP rather than a CLI.

### Do not

Do not register remote MCP servers silently or make network access part of the default core.

## Codescythe

- ID: `perplexity-codescythe`
- Kind: `code-analysis-tool`
- Source: https://github.com/perplexityai/codescythe
- Publisher: Perplexity AI
- Licence: **Verify current repository licence**
- Licence status: `must-verify`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `code-review`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `dead code`, `unused exports`, `unused files`, `dependency path`, `cleanup`

### Core strength

A TypeScript or JavaScript repository needs deterministic dead-code analysis or dependency-path explanation.

### Do not

Do not run destructive fixes without a clean branch, tests, and explicit approval.

## AppFlowy

- ID: `appflowy`
- Kind: `product-repository`
- Source: https://github.com/AppFlowy-IO/AppFlowy
- Publisher: AppFlowy-IO
- Licence: **AGPL-3.0**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `session-memory`
- Permitted modes: `reference`, `integrate-separately`
- Trigger cues: `local-first`, `workspace`, `data ownership`, `self-hosting`, `extensible blocks`

### Core strength

Designing local-first state, user-owned data, extensible workspace architecture, or self-hosted collaboration.

### Do not

Do not copy AGPL code into Escapement's source-available core without a deliberate licence decision.

## Plausible Analytics

- ID: `plausible-analytics`
- Kind: `product-repository`
- Source: https://github.com/plausible/analytics
- Publisher: Plausible Insights
- Licence: **AGPL-3.0-or-later**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `observability`
- Permitted modes: `reference`, `integrate-separately`
- Trigger cues: `privacy analytics`, `local observability`, `simple dashboard`, `no cookies`, `self-hosting`

### Core strength

Designing privacy-first observability, minimal dashboards, transparent metrics, or optional self-hosted analytics.

### Do not

Do not embed AGPL application code into Escapement core without licence review.

## Spec Kit

- ID: `github-spec-kit`
- Kind: `specification-framework`
- Source: https://github.com/github/spec-kit
- Publisher: GitHub
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `harness-methodology`
- Permitted modes: `reference`, `adapt`, `integrate`
- Trigger cues: `constitution`, `specification`, `implementation plan`, `tasks`, `converge`, `preset`, `bundle`

### Core strength

New or material work needs a constitution, executable specification, technical plan, task breakdown, or convergence review.

### Do not

Do not duplicate its whole command surface in Escapement when an optional integration is sufficient.

## 500+ AI Agent Projects & Use Cases

- ID: `500-ai-agents-projects`
- Kind: `agent-pattern-catalogue`
- Source: https://github.com/ashishpatel26/500-AI-Agents-Projects
- Publisher: Ashish Patel
- Licence: **MIT**
- Licence status: `verified-from-readme`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `agent-pattern-catalogue`
- Permitted modes: `reference`
- Trigger cues: `agent pattern`, `industry use case`, `framework comparison`, `example agent`

### Core strength

An agent needs to discover relevant implementation patterns or comparable industry use cases.

### Do not

Do not treat inclusion in a catalogue as proof of safety, quality, maintenance, or licence compatibility.

## Learn Harness Engineering

- ID: `walkinglabs-learn-harness-engineering`
- Kind: `course-and-reference-repository`
- Source: https://walkinglabs.github.io/learn-harness-engineering/en/
- Publisher: Walking Labs
- Licence: **MIT**
- Licence status: `verified-from-project-docs`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `harness-methodology`
- Permitted modes: `reference`, `adapt`
- Trigger cues: `harness`, `state persistence`, `feature list`, `verification loop`, `session lifecycle`, `observability`

### Core strength

Creating, assessing, or teaching the instructions, tools, environment, state, and feedback subsystems of a harness.

### Do not

Do not load the complete course into every task or confuse a prompt file with a complete harness.

## harness-creator skill

- ID: `walkinglabs-harness-creator`
- Kind: `agent-skill`
- Source: https://github.com/walkinglabs/learn-harness-engineering/tree/main/skills/harness-creator
- Publisher: Walking Labs
- Licence: **MIT**
- Licence status: `verified-from-skill-docs`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `harness-methodology`
- Permitted modes: `install`, `adapt`, `reference`
- Trigger cues: `create harness`, `assess harness`, `improve harness`, `harness benchmark`

### Core strength

A project lacks a harness or needs a structured five-subsystem assessment.

### Do not

Do not install it on top of overlapping native Escapement harness skills without an overlap decision.

## Penpot

- ID: `penpot`
- Kind: `design-platform`
- Source: https://github.com/penpot/penpot
- Publisher: Kaleidos
- Licence: **MPL-2.0**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `design-reference`
- Permitted modes: `integrate`, `reference`, `adapt-with-file-level-obligations`
- Trigger cues: `design tokens`, `design-code workflow`, `SVG`, `CSS`, `design MCP`, `self-hosted design`

### Core strength

A product needs open design tokens, inspectable design-to-code workflows, or an optional design MCP/API.

### Do not

Do not copy branding or assume a design file alone proves implementation correctness.

## HelixDB

- ID: `helixdb`
- Kind: `database-and-cli`
- Source: https://github.com/HelixDB/helix-db
- Publisher: HelixDB
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `session-memory`
- Permitted modes: `integrate`, `reference`, `adapt`
- Trigger cues: `agent memory`, `knowledge graph`, `vector graph`, `local database`, `one-shot bootstrap`

### Core strength

A project genuinely needs graph-vector memory, knowledge graphs, or a local agent data layer.

### Do not

Do not make a database mandatory for Escapement's file-based core or add it merely to appear agentic.

## Agent Reach

- ID: `agent-reach`
- Kind: `capability-installer`
- Source: https://github.com/Panniantong/agent-reach
- Publisher: Panniantong
- Licence: **MIT**
- Licence status: `verified-from-readme`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `research-freshness`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `internet access`, `social search`, `video transcript`, `RSS`, `platform connector`, `doctor`

### Core strength

A user explicitly needs internet/platform access not already available through approved tools.

### Do not

Do not bypass platform protections, harvest credentials, or install broad internet capabilities without explicit approval.

## agent-browser

- ID: `agent-browser`
- Kind: `browser-automation-cli`
- Source: https://github.com/vercel-labs/agent-browser
- Publisher: Vercel Labs
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `browser-automation`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `browser test`, `UI verification`, `accessibility snapshot`, `screenshot`, `web workflow`

### Core strength

A frontend or end-to-end task needs real browser evidence, accessibility-tree interaction, screenshots, or DOM inspection.

### Do not

Do not browse authenticated or sensitive sites without approval or use browser automation as proof when business data is fabricated.

## GSD Core

- ID: `gsd-core`
- Kind: `context-and-phase-framework`
- Source: https://github.com/gsd-build/get-shit-done
- Publisher: Open GSD
- Licence: **MIT**
- Licence status: `verified-from-readme`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `harness-methodology`
- Permitted modes: `reference`, `integrate`, `adapt`
- Trigger cues: `context rot`, `phase loop`, `fresh subagent`, `discuss plan execute verify ship`

### Core strength

A project needs phase-level context isolation, fresh execution contexts, or a discuss-plan-execute-verify-ship loop.

### Do not

Do not run parallel agents when tasks share mutable state or when the repository lacks merge and verification controls.

## mcp-builder skill

- ID: `anthropic-mcp-builder`
- Kind: `agent-skill`
- Source: https://github.com/anthropics/skills/tree/main/skills/mcp-builder
- Publisher: Anthropic
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `mcp-building`
- Permitted modes: `install`, `adapt`, `reference`
- Trigger cues: `build MCP`, `MCP server`, `tool schema`, `MCP evaluation`

### Core strength

A project is approved to build an MCP server for an external API or service.

### Do not

Do not expose broad destructive endpoints, secrets, or an unbounded API surface to agents.

## find-skills skill

- ID: `vercel-find-skills`
- Kind: `agent-skill`
- Source: https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md
- Publisher: Vercel Labs
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `external-discovery`
- Permitted modes: `install`, `adapt`, `reference`
- Trigger cues: `find a skill`, `install a skill`, `missing capability`, `skill marketplace`

### Core strength

A task requires a specialised capability that Escapement core does not own.

### Do not

Do not recommend or install a skill solely because it ranks highly or has many installs.

## ECC

- ID: `ecc`
- Kind: `agent-harness-ecosystem`
- Source: https://github.com/affaan-m/ECC
- Publisher: Affaan Mustafa
- Licence: **MIT**
- Licence status: `verified-from-readme`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `harness-methodology`
- Permitted modes: `reference`, `integrate-selectively`
- Trigger cues: `agent harness`, `doctor`, `repair`, `continuous learning`, `agent security`, `cross-runtime sync`

### Core strength

Reviewing cross-runtime distribution, doctor/repair, installation conflict detection, skill packaging, or harness security.

### Do not

Do not copy its hundreds of agents/skills into Escapement core or imply full platform parity.

## Strix

- ID: `strix`
- Kind: `security-testing-tool`
- Source: https://github.com/usestrix/strix
- Publisher: Strix AI
- Licence: **Apache-2.0**
- Licence status: `verified-from-readme`
- Registry status: `catalogued`
- Activation: `on-demand`
- Overlap group: `security-testing`
- Permitted modes: `integrate-authorised-only`, `reference`
- Trigger cues: `pentest`, `dynamic security test`, `proof of concept`, `DAST`, `security scan`

### Core strength

The user has explicit authorisation to dynamically assess a local, owned, or approved target in a sandbox.

### Do not

Do not autonomously attack public or third-party targets, run exploits without permission, or place offensive capability in Escapement core.

## Stop Slop

- ID: `stop-slop`
- Kind: `agent-skill`
- Source: https://github.com/hardikpandya/stop-slop
- Publisher: Hardik Pandya
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `on-demand`
- Overlap group: `writing-quality`
- Permitted modes: `install`, `reference`
- Trigger cues: `remove AI tells`, `human prose`, `slop`, `writing cleanup`, `generic AI wording`, `AI wording`, `polish prose`

### Core strength

A complete human-facing draft needs a final anti-slop pass after content and judgement are correct.

### Do not

Do not load for code-only work or use it as a substitute for substantive writing.

## Task Observer

- ID: `task-observer`
- Kind: `meta-skill`
- Source: https://github.com/rebelytics/one-skill-to-rule-them-all
- Publisher: rebelytics
- Licence: **Attribution-required open licence; verify current file**
- Licence status: `must-verify`
- Registry status: `conditional`
- Activation: `explicit-opt-in`
- Overlap group: `skill-learning`
- Permitted modes: `install`, `reference`
- Trigger cues: `observe tasks`, `suggest skills`, `learn patterns`, `continuous improvement`

### Core strength

A long-running project wants to observe repeated task patterns and propose candidate skills.

### Do not

Do not let it modify skills automatically or observe sensitive sessions without approval.

## Taste Skill

- ID: `taste-skill`
- Kind: `agent-skill-suite`
- Source: https://github.com/Leonxlnx/taste-skill
- Publisher: Leonxlnx
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `choose-one-design-director`
- Overlap group: `design-director`
- Permitted modes: `install`, `reference`
- Trigger cues: `anti-slop frontend`, `design taste`, `layout`, `motion`, `density`, `generic AI styling`, `design skill`

### Core strength

A frontend project needs a strong external design director with adjustable variance, motion, and density.

### Do not

Do not load alongside Impeccable or Open Design as a second full design director.

## Open Design

- ID: `open-design`
- Kind: `design-platform-and-skill-suite`
- Source: https://github.com/nexu-io/open-design
- Publisher: Nexu
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `choose-one-design-director`
- Overlap group: `design-director`
- Permitted modes: `integrate`, `install`, `reference`
- Trigger cues: `local design studio`, `design systems`, `prototype`, `design artifact`, `plugin`

### Core strength

A project needs a local-first design workspace, broad design-skill suite, or artifact-first design workflow.

### Do not

Do not install the full platform merely for a small UI review or combine it with another full design suite.

## Emil Kowalski Design Skills

- ID: `emil-kowalski-skill`
- Kind: `agent-skill-suite`
- Source: https://github.com/emilkowalski/skill
- Publisher: Emil Kowalski
- Licence: **Verify current repository licence**
- Licence status: `must-verify`
- Registry status: `optional`
- Activation: `narrow-motion-specialist`
- Overlap group: `motion`
- Permitted modes: `install`, `reference`
- Trigger cues: `animation review`, `motion`, `easing`, `interaction polish`

### Core strength

A UI needs specialised motion judgement or animation review.

### Do not

Do not use motion to compensate for weak hierarchy or load the full suite for static enterprise screens.

## Impeccable

- ID: `impeccable`
- Kind: `agent-skill-and-cli`
- Source: https://github.com/pbakaus/impeccable
- Publisher: Paul Bakaus
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `choose-one-design-director`
- Overlap group: `design-director`
- Permitted modes: `install`, `integrate`, `reference`
- Trigger cues: `design audit`, `polish UI`, `anti-pattern detection`, `UX writing`, `responsive`

### Core strength

A frontend needs one comprehensive design skill plus deterministic anti-pattern checks.

### Do not

Do not load with Taste Skill or Open Design as a second primary design director.

## Superpowers

- ID: `superpowers`
- Kind: `agent-methodology-plugin`
- Source: https://github.com/obra/superpowers
- Publisher: Jesse Vincent / Prime Radiant
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `choose-one-external-methodology`
- Overlap group: `harness-methodology`
- Permitted modes: `install`, `reference`
- Trigger cues: `TDD`, `systematic debugging`, `brainstorming`, `subagent development`, `plan execution`

### Core strength

A team explicitly wants the Superpowers methodology for development execution.

### Do not

Do not combine its full lifecycle hooks with ECC or GSD without an overlap decision.

## Claude Mem

- ID: `claude-mem`
- Kind: `memory-plugin`
- Source: https://github.com/thedotmack/claude-mem
- Publisher: thedotmack
- Licence: **AGPL-3.0 for main package; verify subcomponents**
- Licence status: `verified-with-obligations`
- Registry status: `conditional`
- Activation: `choose-one-session-memory`
- Overlap group: `session-memory`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `persistent memory`, `semantic session history`, `memory search`, `long-running project`

### Core strength

Local file handoffs are insufficient and the project accepts a background memory service and its licence.

### Do not

Do not install by default, duplicate Escapement state, or capture confidential sessions without a privacy decision.

## Graphify

- ID: `graphify`
- Kind: `code-knowledge-skill-and-cli`
- Source: https://github.com/Graphify-Labs/graphify
- Publisher: Graphify Labs
- Licence: **Apache-2.0 and MIT components**
- Licence status: `verified`
- Registry status: `conditional`
- Activation: `on-demand`
- Overlap group: `code-knowledge`
- Permitted modes: `install`, `integrate`, `reference`
- Trigger cues: `knowledge graph`, `large codebase`, `architecture map`, `relationship query`

### Core strength

A large or heterogeneous repository needs deterministic relationship mapping beyond ordinary file search.

### Do not

Do not index sensitive material through external backends without approval or use it for a small codebase.

## gstack

- ID: `gstack`
- Kind: `agent-role-skill-suite`
- Source: https://github.com/garrytan/gstack
- Publisher: Garry Tan
- Licence: **Verify current repository licence**
- Licence status: `must-verify`
- Registry status: `optional`
- Activation: `choose-one-external-methodology`
- Overlap group: `harness-methodology`
- Permitted modes: `install`, `reference`
- Trigger cues: `CEO review`, `engineering plan review`, `design review`, `QA`, `release review`

### Core strength

A project explicitly wants role-based plan reviews or fresh-context specialist reviews.

### Do not

Do not install its full workflow alongside Superpowers or ECC without deciding which system owns orchestration.

## Everything Claude Code / ECC

- ID: `everything-claude-code`
- Kind: `harness-ecosystem`
- Source: https://github.com/affaan-m/everything-claude-code
- Publisher: Affaan Mustafa
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `choose-one-external-methodology`
- Overlap group: `harness-methodology`
- Permitted modes: `install`, `reference`
- Trigger cues: `agent harness`, `rules`, `agents`, `skills`, `hooks`, `memory optimisation`

### Core strength

A user wants ECC components or profiles that Escapement does not provide.

### Do not

Do not install the full profile on top of Escapement hooks and native skills; use component-level selection.

## Context7

- ID: `context7`
- Kind: `documentation-mcp`
- Source: https://github.com/upstash/context7
- Publisher: Upstash
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `on-demand`
- Overlap group: `research-freshness`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `current library docs`, `API documentation`, `framework version`, `technical docs`

### Core strength

Implementation depends on current external library documentation.

### Do not

Do not use it as the source of truth for the project's own code or business rules.

## Last30Days

- ID: `last30days`
- Kind: `research-skill`
- Source: https://github.com/mvanhorn/last30days-skill
- Publisher: Matt Van Horn
- Licence: **Verify current repository licence**
- Licence status: `must-verify`
- Registry status: `optional`
- Activation: `on-demand`
- Overlap group: `research-freshness`
- Permitted modes: `install`, `reference`
- Trigger cues: `last 30 days`, `recent discourse`, `Reddit`, `X`, `YouTube`, `HN`

### Core strength

A decision benefits from recent community signals rather than only authoritative documentation.

### Do not

Do not use social discourse as authoritative evidence or load it for stable facts.

## Skill UI

- ID: `skill-ui`
- Kind: `legacy-capability-reference`
- Source: Source pending confirmation
- Publisher: Pending confirmation
- Licence: **Unknown**
- Licence status: `source-required`
- Registry status: `preserved-unresolved`
- Activation: `disabled-until-source-confirmed`
- Overlap group: `external-discovery`
- Permitted modes: `reference`
- Trigger cues: `skill UI`

### Core strength

Retained from the original capability set pending exact source confirmation.

### Do not

Do not install or attribute this entry until the exact repository is confirmed.

## Claude Code Review

- ID: `claude-code-review`
- Kind: `managed-code-review-service`
- Source: https://code.claude.com/docs/en/code-review
- Publisher: Anthropic
- Licence: **Commercial managed service**
- Licence status: `not-open-source-service`
- Registry status: `optional`
- Activation: `choose-one-code-review`
- Overlap group: `code-review`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `PR review`, `managed code review`, `multi-agent review`

### Core strength

A supported organisation wants Anthropic's managed PR review service.

### Do not

Do not present it as open source or use it in addition to another expensive full review workflow without reason.

## Ponytail

- ID: `ponytail`
- Kind: `minimal-code-skill-and-plugin`
- Source: https://github.com/DietrichGebert/ponytail
- Publisher: Dietrich Gebert
- Licence: **Verify current repository licence**
- Licence status: `must-verify`
- Registry status: `optional`
- Activation: `on-demand`
- Overlap group: `engineering-minimalism`
- Permitted modes: `install`, `reference`
- Trigger cues: `minimal code`, `overengineering`, `lazy senior dev`, `code bloat`

### Core strength

An agent repeatedly overbuilds bounded implementation tasks.

### Do not

Do not let minimalism remove validation, security, observability, or approved requirements.

## Mobbin

- ID: `mobbin`
- Kind: `commercial-design-reference`
- Source: https://mobbin.com
- Publisher: Mobbin
- Licence: **Commercial service/content terms**
- Licence status: `not-open-source`
- Registry status: `reference-only`
- Activation: `on-demand`
- Overlap group: `design-reference`
- Permitted modes: `reference`
- Trigger cues: `mobile pattern`, `product UI reference`, `screen flow`

### Core strength

A designer needs real-product interaction and screen references.

### Do not

Do not scrape, redistribute, or copy protected screens and assets.

## Refero

- ID: `refero`
- Kind: `design-reference`
- Source: https://refero.design
- Publisher: Refero
- Licence: **Website content terms**
- Licence status: `not-code-resource`
- Registry status: `reference-only`
- Activation: `on-demand`
- Overlap group: `design-reference`
- Permitted modes: `reference`
- Trigger cues: `web app reference`, `page pattern`, `component inspiration`

### Core strength

A product needs curated web and product references.

### Do not

Do not copy protected layouts or assets as trade dress.

## Recent

- ID: `recent-designs`
- Kind: `design-reference`
- Source: https://recent.design
- Publisher: Recent
- Licence: **Website content terms**
- Licence status: `not-code-resource`
- Registry status: `reference-only`
- Activation: `on-demand`
- Overlap group: `design-reference`
- Permitted modes: `reference`
- Trigger cues: `recent design`, `website inspiration`, `current visual trend`

### Core strength

A task needs a current design-reference shortlist.

### Do not

Do not let trend references override brand, usability, or enterprise density.

## 21st.dev

- ID: `21st-dev`
- Kind: `component-reference-and-service`
- Source: https://21st.dev
- Publisher: 21st.dev
- Licence: **Per component/project; verify**
- Licence status: `must-verify`
- Registry status: `optional`
- Activation: `on-demand`
- Overlap group: `component-source`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `component inspiration`, `React component`, `UI block`

### Core strength

A project needs a component starting point compatible with its stack.

### Do not

Do not introduce copied components without licence, dependency, accessibility, and design-system review.

## shadcn/ui

- ID: `shadcn-ui`
- Kind: `component-system`
- Source: https://github.com/shadcn-ui/ui
- Publisher: shadcn
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `on-demand`
- Overlap group: `component-source`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `shadcn`, `React components`, `Radix`, `component library`

### Core strength

A React project explicitly chooses shadcn/ui as its component foundation.

### Do not

Do not add it to a project with an established incompatible component system.

## GSAP

- ID: `gsap`
- Kind: `motion-library`
- Source: https://github.com/greensock/GSAP
- Publisher: GreenSock
- Licence: **GSAP standard licence; verify current terms**
- Licence status: `special-terms`
- Registry status: `optional`
- Activation: `approved-dependency`
- Overlap group: `motion`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `GSAP`, `timeline animation`, `scroll animation`, `complex motion`

### Core strength

The approved interaction genuinely requires advanced timeline or scroll animation.

### Do not

Do not add it for ordinary transitions or without dependency and licence review.

## Headroom.js

- ID: `headroom-js`
- Kind: `interaction-library`
- Source: https://github.com/WickyNilliams/headroom.js
- Publisher: WickyNilliams
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `approved-dependency`
- Overlap group: `motion`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `hide header on scroll`, `headroom`, `scroll header`

### Core strength

A product specifically needs scroll-aware header behaviour.

### Do not

Do not add a dependency when a small native implementation already exists and is tested.

## Playwright

- ID: `playwright`
- Kind: `browser-testing-framework`
- Source: https://github.com/microsoft/playwright
- Publisher: Microsoft
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `preferred-when-existing`
- Activation: `choose-one-browser-driver`
- Overlap group: `browser-automation`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `browser test`, `E2E`, `visual test`, `accessibility test`

### Core strength

A project needs robust browser automation and either already uses Playwright or approves it.

### Do not

Do not install it solely for a tiny static inspection.

## Andrej Karpathy Coding Guidelines

- ID: `karpathy-guidelines`
- Kind: `behavioural-skill`
- Source: https://github.com/forrestchang/andrej-karpathy-skills
- Publisher: forrestchang / derived from Andrej Karpathy observations
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `preferred-policy`
- Activation: `baseline-engineering-policy`
- Overlap group: `engineering-behaviour`
- Permitted modes: `adapt`, `install`, `reference`
- Trigger cues: `assumptions`, `simple code`, `surgical changes`, `goal-driven`, `overengineering`

### Core strength

Engineering work needs explicit assumptions, simplicity, surgical changes and verifiable goals.

### Do not

Do not duplicate the same guidance through another always-loaded minimalism rule.

## UI/UX Pro Max

- ID: `ui-ux-pro-max`
- Kind: `design-intelligence-skill-and-cli`
- Source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Publisher: NextLevelBuilder
- Licence: **Repository reports MIT; CLI materials may differ. Verify selected release and component.**
- Licence status: `mixed-verify-selected-component`
- Registry status: `optional-preferred-design-research`
- Activation: `phase-adapter`
- Overlap group: `design-authority`
- Permitted modes: `install`, `integrate`, `reference`
- Trigger cues: `UI UX Pro`, `design system generator`, `palette`, `font pairing`, `UX guideline`, `chart recommendation`

### Core strength

A UI task benefits from searchable product-type, style, palette, typography, UX, chart or stack recommendations.

### Do not

Do not let generated recommendations override DESIGN.md or the design intelligence constitution.

## Anthropic Frontend Design

- ID: `frontend-design`
- Kind: `frontend-implementation-skill`
- Source: https://github.com/openclaw/skills/tree/main/skills/qrucio/anthropic-frontend-design
- Publisher: Community packaging of frontend-design guidance
- Licence: **Verify source repository licence**
- Licence status: `must-verify`
- Registry status: `optional`
- Activation: `phase-adapter`
- Overlap group: `design-authority`
- Permitted modes: `install`, `reference`
- Trigger cues: `frontend design`, `production-grade frontend`, `anti-slop interface`

### Core strength

An approved design specification needs production-grade frontend implementation.

### Do not

Do not use as the design constitution or alongside multiple primary art-direction systems.

## Playwright MCP

- ID: `playwright-mcp`
- Kind: `browser-automation-mcp`
- Source: https://github.com/microsoft/playwright-mcp
- Publisher: Microsoft
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `choose-one-browser-driver`
- Overlap group: `browser-verification`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `Playwright MCP`, `persistent browser context`, `accessibility tree`

### Core strength

Exploratory or long-running agent browser loops benefit from persistent accessibility-tree state.

### Do not

Do not prefer MCP over CLI or project tests when token efficiency and deterministic test code are more important.

## Stagehand

- ID: `stagehand`
- Kind: `ai-browser-automation-framework`
- Source: https://github.com/browserbase/stagehand
- Publisher: Browserbase
- Licence: **MIT**
- Licence status: `verify-current-release`
- Registry status: `optional`
- Activation: `approved-browser-automation`
- Overlap group: `browser-verification`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `Stagehand`, `self-healing browser automation`, `natural-language browser`

### Core strength

Production browser automation needs a controlled blend of code, natural language, caching and self-healing.

### Do not

Do not add it for ordinary end-to-end tests or without reviewing network, model and credential requirements.

## Cypress

- ID: `cypress`
- Kind: `browser-testing-framework`
- Source: https://github.com/cypress-io/cypress
- Publisher: Cypress.io
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `preferred-when-existing`
- Activation: `choose-one-browser-driver`
- Overlap group: `browser-verification`
- Permitted modes: `integrate`, `reference`
- Trigger cues: `Cypress`, `Cypress tests`

### Core strength

The project already uses Cypress or explicitly selects it as the browser test framework.

### Do not

Do not introduce Cypress into a Playwright-based project without a migration reason.

## Puppeteer MCP Server

- ID: `puppeteer-mcp`
- Kind: `legacy-browser-mcp`
- Source: https://github.com/modelcontextprotocol/servers-archived
- Publisher: Model Context Protocol community archive
- Licence: **Per archived repository/package**
- Licence status: `archived-security-review-required`
- Registry status: `discouraged-legacy`
- Activation: `existing-project-only`
- Overlap group: `browser-verification`
- Permitted modes: `reference`
- Trigger cues: `Puppeteer MCP`

### Core strength

An existing approved project depends on the archived Puppeteer MCP server and migration is not immediate.

### Do not

Do not select for new projects; prefer maintained Playwright CLI/MCP or project-native tests.

## Prime Agent

- ID: `prime-intellect-prime-agent`
- Kind: `external-agent-runtime`
- Source: https://github.com/PrimeIntellect-ai/prime-agent
- Publisher: Prime Intellect
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `conditional`
- Activation: `integrate-separately-or-adapter`
- Overlap group: `harness-methodology`
- Permitted modes: `reference`, `integrate-separately`, `adapter`
- Trigger cues: `run a long-lived background coding agent`, `persistent REPL`, `recursive subagents`, `detachable agent sessions`, `JSON RPC`, `Prime Agent`

### Core strength

A project explicitly needs a separate long-running agent runtime, background or detachable sessions, persistent REPL execution, recursive subagents, or retained goals, schedules and heartbeats.

### Do not

Do not classify it as a skill, let it and Escapement co-own lifecycle phase, task state, memory, permissions, skill promotion, verification or closure, or describe its processes as a security sandbox.

## Understand Anything

- ID: `egonex-understand-anything`
- Kind: `code-knowledge-plugin`
- Source: https://github.com/Egonex-AI/Understand-Anything
- Publisher: Egonex AI
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `on-demand-read-only-analysis`
- Overlap group: `code-knowledge`
- Permitted modes: `install`, `integrate`, `reference`
- Trigger cues: `understand this codebase`, `architecture map`, `unfamiliar codebase`, `dependency map`, `business-domain flows`, `impact of this diff`, `knowledge graph`, `codebase tour`

### Core strength

Onboarding into a large or unfamiliar codebase, creating an architecture or dependency map, extracting business-domain flows, performing guided codebase tours, or analysing change impact -- when ordinary repository inspection is no longer sufficient. The strongest immediate integration candidate reviewed in this batch.

### Do not

Do not run full indexing automatically, index confidential repositories without approval, enable automatic commit hooks without approval, or treat the generated graph as the only source of truth instead of supporting evidence.

## Evolver

- ID: `evomap-evolver`
- Kind: `agent-evolution-meta-observer`
- Source: https://github.com/EvoMap/evolver
- Publisher: EvoMap
- Licence: **GPL-3.0-or-later for the current published release**
- Licence status: `verified-review-required-per-release`
- Registry status: `conditional`
- Activation: `review-mode-only`
- Overlap group: `skill-learning`
- Permitted modes: `reference`, `integrate-separately`
- Trigger cues: `analyse the harness logs`, `recurring failures`, `auditable improvement to our agent workflow`, `repeated routing failures`, `self-evolution`, `skill evolution`

### Core strength

A project has meaningful runtime history, logs, repeated failure patterns, or closed-turn evidence (see `scripts/harness_observability.py`) that a self-improvement pass could act on.

### Do not

Do not allow automatic modification of AGENTS.md, automatic mutation of native skills, automatic edits to policy or project state, a continuous loop by default, or sending repository logs to a network service without approval. Do not copy GPL code into Escapement's source-available core without a deliberate licence decision.

## Agency Agents

- ID: `agency-agents`
- Kind: `agent-role-catalogue`
- Source: https://github.com/msitarzewski/agency-agents
- Publisher: msitarzewski
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `reference-only`
- Activation: `selective-reference`
- Overlap group: `agent-pattern-catalogue`
- Permitted modes: `reference`, `adapt-selectively`
- Trigger cues: `specialist agent role`, `fresh-context reviewer`, `domain persona for this review`, `agent persona`

### Core strength

Identifying a missing specialist reviewer, drafting a fresh-context agent contract, comparing role definitions, or discovering deliverable structures.

### Do not

Do not install the complete roster, load multiple personas into a single phase, or treat personality wording or persona success metrics as verified expertise or independent evidence.

## Prompt Master

- ID: `nidhinjs-prompt-master`
- Kind: `prompt-export-skill`
- Source: https://github.com/nidhinjs/prompt-master
- Publisher: Nidhin Joseph Nelson
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional-reference`
- Activation: `explicit-cross-tool-prompt-export`
- Overlap group: `prompt-shaping`
- Permitted modes: `reference`, `adapt`, `install-explicitly`
- Trigger cues: `convert this approved specification into a`, `write a prompt for`, `export this brief for`, `export this Escapement brief`

### Core strength

A user wants an approved Escapement brief converted into a prompt for another tool: Claude Code, Codex, Cursor, Copilot, an image or video generation tool, n8n, Zapier, Make, or another specialised AI system.

### Do not

Do not make it part of every coding turn or let it replace Escapement-owned discovery, material questions, business or domain context, architecture decisions, approval gates, scope, acceptance criteria or verification requirements. Do not repeat unverified promotional claims such as zero wasted tokens, perfect prompt, universal accuracy or full memory retention.

## Matt Pocock Grilling / Grill Me

- ID: `mattpocock-grilling`
- Kind: `decision-interview-skill`
- Source: https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling
- Publisher: Matt Pocock
- Licence: **MIT**
- Licence status: `verified`
- Registry status: `optional`
- Activation: `explicit-user-invocation`
- Overlap group: `decision-interview`
- Permitted modes: `adapt`, `install-explicitly`, `reference`
- Trigger cues: `grill me`, `stress-test my plan`, `stress-test this plan`, `challenge every assumption`, `challenge this architecture`, `find the hidden assumptions`, `interview me before implementation`

### Core strength

The user explicitly asks to be grilled, stress-tested, or challenged on a plan or design before implementation begins. Adapted with original wording as the Grilling Intensifier section of `skills/decision-coach/SKILL.md` -- see [OVERLAP_ANALYSIS.md](OVERLAP_ANALYSIS.md).

### Do not

Do not activate implicitly for an ordinary feature request. Do not let it skip Escapement's own rules: inspect the repository before asking, ask no more than five material questions per round, always give a recommended default and consequence, and wait for confirmation before implementing.

## Cloudflare OS

- ID: `cloudflare-os`
- Kind: `agent-workspace-and-security-architecture`
- Source: https://github.com/cloudflare/cloudflare-os
- Publisher: Cloudflare
- Licence: **Apache-2.0**
- Licence status: `verified`
- Registry status: `reference-only`
- Activation: `architecture-reference`
- Overlap group: `agent-workspace-platform`
- Permitted modes: `reference`, `integrate-separately`
- Trigger cues: `secure enterprise agent workspace`, `narrow access to company systems`, `sandboxed AI-generated internal apps`, `approval layer for agent side effects`, `Cloudflare OS`, `Gatekeeper`

### Core strength

A task concerns agent workspace design, capability-based security, sandboxed AI-built apps, human approval of side-effecting actions, or narrow resource introduction to agents.

### Do not

Do not present it as a drop-in skill, add Cloudflare Workers dependencies to Escapement core, copy its full application architecture, or imply Escapement currently provides Cloudflare OS-style sandboxing or that Gatekeepers have been integrated rather than only referenced.



# Third-party usage record

When any external capability is actually installed, copied, adapted or invoked
against project data, update:

```text
THIRD_PARTY_NOTICES.md
docs/decisions/DECISION_LOG.md
.escapement-install.json
```

Record:

```text
Exact source
Tag or commit
Licence
Files or capability used
Changes made
Network and credential requirements
Data handled
Approval
Validation evidence
Removal or rollback path
```
