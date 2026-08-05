---
name: reference-router
description: Use when a user asks to find, compare, install, or use an external skill, plugin, GitHub repository, CLI, MCP server, service, agent framework, or open-source component; also use when Escapement lacks a specialised capability. Do not install anything before licence, security, overlap, and approval review.
---

# External Reference and Capability Router

## Mandatory reads

- `catalog/capability-registry.json`
- `catalog/overlap-groups.json`
- `docs/REFERENCE_CATALOG.md`
- `SECURITY.md`
- `docs/decisions/DECISION_LOG.md`
- `THIRD_PARTY_NOTICES.md`

## Procedure

1. Define the capability gap precisely.
2. Search the catalogue by:
   - trigger;
   - type;
   - publisher;
   - use mode;
   - licence status.
3. Prefer, in order:
   - existing Escapement native capability;
   - already-approved project dependency;
   - external integration;
   - installable skill or plugin;
   - source adaptation;
   - new custom implementation.
4. Verify the current repository, release, licence, maintenance status, and
   security posture.
5. Check overlap with installed harnesses, skills, hooks, commands, MCP servers,
   and project dependencies.
6. State:
   - selected resource;
   - why it matches;
   - exact version or commit;
   - licence;
   - permissions/network/credential requirements;
   - alternatives rejected;
   - installation or adaptation plan;
   - validation plan.
7. Request approval when required.
8. Pin the version or commit.
9. Update third-party notices and the decision log.
10. Capture install and validation evidence.

## Decision states

```text
REFERENCE
ADAPT
INSTALL
INTEGRATE
REJECT
DEFER
```

## Required output

```text
Capability:
Selected resource:
Source:
Pinned version/commit:
Decision state:
Licence:
Why selected:
Alternatives rejected:
Overlap:
Security:
Data/credentials:
Approval:
Attribution:
Validation:
```

## Critical failures

- treating a public repository as automatically licensed;
- installing without approval;
- copying code from an unlicensed or incompatible source;
- executing remote install scripts without review;
- registering an MCP server silently;
- providing credentials without explicit approval;
- stacking overlapping harness installations;
- using offensive security tools without written authorisation.
