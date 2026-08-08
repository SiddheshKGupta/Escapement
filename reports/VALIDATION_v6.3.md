# Escapement v6.3 Validation Report

Validated: 2026-08-07  
Release: `6.3.0 — Capability Strength Orchestration`

## Results

| Check | Result |
|---|---|
| Python syntax | PASS — 13 scripts |
| Kernel budget | PASS — 795 / 1000 words |
| Automatic context | PASS — tested packs below 1,800 words |
| Invoked skill context | PASS — tested routes below 1,000 words |
| Routing evaluations | PASS — 122 / 122 |
| Unit tests | PASS — 172 / 172 |
| Runtime doctor | PASS — 0 failures |
| Repository doctor | PASS — 0 failures, 0 warnings |
| Native skill synchronisation | PASS — 35 / 35 |
| Security gate | PASS — 0 findings |
| Fresh installation | PASS |
| Full self-test | PASS — 0 failures |
| Real-project lifecycle | PASS — fresh install through RELEASE and truthful PARTIAL closure |
| Organisation neutrality | PASS |

## Behaviour verified

### Decision support

- MATERIAL and PROGRAM requests generate high-impact questions.
- Each question includes a recommended default and consequence.
- The runtime produces an improved execution prompt.
- INFO requests create no material runtime turn.

### Design

- `design-intelligence.md` is active for every design phase.
- UI/UX Pro Max appears in research/specification.
- Taste appears in brainstorming.
- frontend-design appears in implementation.
- Impeccable appears in verification/polish.
- Emil appears only when motion is relevant.
- Competing design directors do not appear in the same phase.

### Engineering overlap

- Karpathy remains the baseline.
- Ponytail activates only when minimalism pressure is justified.
- Complete-term matching prevents accidental substring routes.
- Generic technical work has specification, implementation and quality
  fallbacks.

### Domain capability

- AI-agent work uses blueprint discovery, agent engineering and quality
  verification.
- Legal work pairs source analysis with governance and workflow.
- Investment work pairs investment, finance and domain research.
- Data pipeline/dashboard work can combine data and frontend procedures.

### Research

- Authoritative sources remain first.
- Last30Days and Agent Reach are supporting channels.
- The 500+ agent catalogue is treated as discovery-only.
- Browser frameworks are selected rather than stacked.

### Real-project lifecycle

- Fresh installation creates `docs/plans/`.
- Framework tests are not copied into product repositories.
- Complex multi-module builds classify as PROGRAM.
- A single turn advances through all lifecycle phases.
- The final closure remains PARTIAL when planned modules are incomplete.

### Runtime

- Open turns continue.
- Phase advancement reloads phase-specific context.
- The readiness audit reports detected, active and candidate capabilities.
- MATERIAL and PROGRAM completion requires structured evidence.
- Critical failures cannot pass.

## Commands

```bash
python scripts/eval_harness.py run
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/agent_runtime.py doctor
python scripts/escapement.py doctor --root .
python scripts/security_gate.py --fail-on high
python scripts/escapement.py self-test
```

## Release status

**PASS**
