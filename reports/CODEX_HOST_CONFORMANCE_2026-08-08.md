# Escapement v1 × Codex Host-Conformance & Resource-Governance Report

## 1. Environment

```text
Date: 2026-08-08
Repository commit: ab2b7ea3d5f65a547ef0f6e57476f5ae6ccaa656
Escapement version: 6.3.0
Codex host/version: Codex desktop, version UNKNOWN
Codex model: UNKNOWN
Operating system: Microsoft Windows NT 10.0.19045.0
PowerShell: 5.1.19041.7548
Python: 3.12.13, bundled Codex workspace runtime
App Server version/status: NOT OBSERVABLE; Escapement v6.3 has no App Server adapter
```

The configured workspace did not exist when this task started. Codex cloned the repository from `https://github.com/SiddheshKGupta/Escapement` into `C:\Smart_EPP_Operating_Platform`. This prevented a clean automatic session-start observation in a repository that existed before task creation.

## 2. Baseline Health

```text
Repository doctor: PASS, 0 failures and 0 warnings
Runtime doctor: PASS, 0 failures; kernel 795/1000 words
Unit tests: PASS, 165/165 in 303.615 seconds
Routing evals: PASS, 72/72
Security: PASS, 0 findings
Self-test: NOT COMPLETED; user stopped the redundant nested run after the component checks above had passed
```

Commands used the repository's own entry points with Codex's bundled Python 3.12.13. The complete unit suite, routing corpus, doctors, and security gate provide enough baseline evidence to separate pre-existing repository health from Codex integration findings.

## 3. Codex Integration Discovery

| Area | Implementation | Evidence level |
| --- | --- | --- |
| AGENTS/kernel | `AGENTS.md` is the governing kernel | Codex supplied it as repository instructions on a later turn |
| Hooks | `.codex/hooks.json` declares SessionStart, UserPromptSubmit, and Stop commands | Code exists; automatic execution not observed |
| Hook wrappers | `scripts/escapement-hook.ps1` and `.sh` invoke `agent_runtime.py` | Manual execution validated |
| Skills | 35 skills mirrored under `.agents/skills` | Codex exposed them as `escapement:*` skills on a later turn |
| Plugin packaging | `.codex-plugin/plugin.json` points to hooks and skills | Packaging discovered; marketplace or host loading not proved |
| App Server | No adapter, client, protocol schema, or invocation path | NOT IMPLEMENTED |
| Rate limits | No read or update handler | NOT IMPLEMENTED |
| Usage | No usage read path | NOT IMPLEMENTED |
| Interrupt and steer | No App Server `turn/interrupt` or `turn/steer` path | NOT IMPLEMENTED |

Repository authority follows the order in `AGENTS.md`: platform and user instructions, approved decisions, nearest kernel, active phase/profile, selected skills, then external references. `PROJECT_STATE.yaml`, `PROJECT_CONTEXT.md`, and `DOMAIN_CONTEXT.md` hold project state and context. `.agent/runtime` holds generated turn state. `.agent/evidence`, `.agent/evals`, and `.agent/security` hold generated evidence. `SESSION_HANDOFF.md` is the durable handoff.

## 4. Automatic Bootstrap

```text
Observed: NOT OBSERVABLE for clean SessionStart; FAIL for prompt-hook execution on later turns
Evidence: the repository did not exist at initial task startup. After cloning, no .agent directory appeared until manual invocation. On a later user prompt, current-turn.json retained prompt_count=1 and the prior updated_at value.
```

Codex did discover `AGENTS.md` and `.agents/skills` after the repository became the active workspace. Codex did not run `.codex/hooks.json` for the later user prompt. Instruction discovery and hook execution therefore have different results.

## 5. Manual Bootstrap

```text
Required: YES
Command: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/escapement-hook.ps1 session-start
Prompt command: JSON prompt piped to the same wrapper with event `prompt`
Result: PASS
Turn: TURN-ea1d586fd145
Tier: PROGRAM
Phase: DISCOVER
Host/session ID: codex-desktop-current-task
```

Direct execution of the PowerShell script failed under the host execution policy. The exact `-ExecutionPolicy Bypass` shape declared in `.codex/hooks.json` succeeded. The manual Windows pipeline replaced some non-ASCII prompt characters with `?`; this result applies to the manual pipeline used in this run, not to an unobserved native Codex hook invocation.

## 6. App Server Contract Matrix

| Method | Implemented | Offline validated | Live validated |
| --- | --- | --- | --- |
| `account/rateLimits/read` | NO | NO | NO |
| `account/rateLimits/updated` | NO | NO | NO |
| `account/usage/read` | NO | NO | NO |
| `turn/start` | NO | NO | NO |
| `turn/steer` | NO | NO | NO |
| `turn/interrupt` | NO | NO | NO |
| `turn/completed` | NO | NO | NO |

Repository-wide searches found these method names only in the experiment prompt or future-scope documentation. No current script, test, fixture, catalog entry, or protocol definition implements them. Escapement's local runtime turn model is not a Codex App Server `turn/start` implementation.

## 7. Live Codex Resource State

```text
Rate-limit read: NOT OBSERVABLE
Usage read: NOT AVAILABLE
Reset information: NOT OBSERVABLE
Update event: NOT OBSERVABLE
Data source: none; the repository exposes no supported mechanism
```

The run did not substitute fixture data for live account data. No live or mock values were recorded for quota, usage, account tier, model allowance, remaining availability, or reset time.

## 8. Rate-Limit / Quota Persistence

Escapement v6.3 persists no Codex rate-limit or usage state. `current-turn.json`, context files, turn logs, observability output, and the program fixture contained no resource schema or resource values. The framework cannot route or interrupt from data it does not retrieve.

## 9. Resource-Aware Runtime Behavior

| Behavior | Result |
| --- | --- |
| Routing | NOT IMPLEMENTED |
| Context reduction from quota | NOT IMPLEMENTED |
| Agent or parallelism reduction | NOT IMPLEMENTED |
| Conservation or convergence | NOT IMPLEMENTED |
| Program slicing from quota | NOT IMPLEMENTED |
| Verification changes | NOT IMPLEMENTED |
| Resource warning or checkpoint | NOT IMPLEMENTED |
| App Server interruption | NOT IMPLEMENTED |

Classification: `NO`. README and future-scope documents also identify quota-aware routing and budget enforcement as future work.

## 10. Before/After Resource Delta

| Metric | Before | After | Source |
| --- | ---: | ---: | --- |
| Usage | NOT OBSERVABLE | NOT OBSERVABLE | No repository mechanism |
| Rate-limit state | NOT OBSERVABLE | NOT OBSERVABLE | No repository mechanism |
| Reset window | NOT OBSERVABLE | NOT OBSERVABLE | No repository mechanism |

Resource delta observable: `NO`.

## 11. Classification Results

| Prompt | Classification | Expected runtime behavior | Observed |
| --- | --- | --- | --- |
| Explain `PROJECT_STATE.yaml` | INFO | No material runtime turn | INFO, no phase plan, no skills, no checks |
| Fix a spelling mistake in a user-facing message | MATERIAL | MICRO, one skill, compact closure | MATERIAL with DISCOVER, RESEARCH, PLAN, IMPLEMENT, VERIFY and a success question |
| Add blank username validation and tests | MATERIAL | MICRO, bounded implementation and test | MATERIAL with the same broad ceremony and user/success questions |
| Add authentication | MATERIAL | Decision gate and structured verification | MATERIAL; two questions; implementation stopped until authority arrived |
| Build four-module claims platform | PROGRAM | Full phased program governance | PROGRAM; four material questions and full lifecycle |

The INFO, MATERIAL, and PROGRAM boundaries worked for the first, fourth, and fifth prompts. Both intended MICRO prompts over-classified as MATERIAL. This blocked the requested MICRO execution unless the agent bypassed runtime classification, which the benchmark forbade.

## 12. MICRO Result

```text
Tier: MATERIAL, contrary to the intended MICRO scenario
Phases: ORIENT, DISCOVER, RESEARCH, PLAN, IMPLEMENT, VERIFY
Capabilities: decision-coach, project-discovery, lifecycle-planning
Files: none
Commands: agent_runtime.py explain --prompt <scenario>
Verification: classification output inspected; no implementation verification ran
Evidence: actual router JSON recorded in this run
Closure: scenario stopped as a routing failure; no false MICRO PASS
Resource delta: NOT OBSERVABLE
```

Codex did not modify Escapement core to force the scenario through a MICRO path.

## 13. MATERIAL Decision Gate

```text
Decision identified: authority to proceed with benchmark defaults for the authentication scenario
Questions: primary users/final decision-maker; measurable success outcome
Implementation stopped: YES
User authority respected: YES
Resolution: user authorized recommended defaults for experiment and benchmark decisions
```

The generated questions were generic. The router did not ask authentication-specific questions about identity source, session model, MFA, recovery, trust boundaries, or role policy. That limits the value of the gate even though the stop behavior worked.

## 14. Capability Routing

Direct phase routing for the CSV reconciliation API produced this selection:

| Phase | Capability | Selected | Used | Evidence |
| --- | --- | ---: | ---: | --- |
| DISCOVER | decision-coach, project-discovery, lifecycle-planning | YES | YES, routing audit | Direct `capability_router.py --phase DISCOVER` |
| SPECIFY | data-engineering, reporting-standard, api-integration, product-specification | YES | YES, routing audit | Direct phase output |
| PLAN | data-engineering, api-integration, delivery-planning | YES | YES, routing audit | Direct phase output |
| IMPLEMENT | data-engineering, api-integration, software-implementation | YES | YES, routing audit | Direct phase output |
| VERIFY | data-engineering, api-integration, quality-engineering | YES | YES, routing audit | Direct phase output |

The router selected three or four native skills per phase and stayed within its five-skill MATERIAL limit. `capability-audit` displayed generic catalog skills for several phases rather than the task-specific skills returned by direct phase routing. Consumers can receive two different capability plans for the same prompt.

External candidates included Karpathy Guidelines and Superpowers. The benchmark installed nothing. Recommendation: skip installation during host conformance because equivalent host capabilities were already available and installation would alter the test environment.

## 15. Truthful Closure

```text
Completed: negative closure-gate test
Missing: structured check records required for PROGRAM PASS
Evidence: close-turn returned exit 1 with `PROGRAM PASS requires structured checks`
Closure: PASS rejected; current turn remained open
Next action: close the benchmark with an evidence-backed PARTIAL result after writing this report
```

The throwaway PROGRAM fixture later closed as PARTIAL without claiming implementation or checks. Its handoff named the blocker and exact next action.

## 16. PROGRAM Result

The test used an ignored fresh installation at `.agent/runs/codex-program-benchmark`.

```text
Program: Claims Management Platform
Modules: Intake, Assessment, Approval, Reporting
Dependencies: Assessment -> Intake; Approval -> Assessment; Reporting -> Approval
Shared artifacts: PROJECT_CONTEXT.md, DOMAIN_CONTEXT.md
Slice completed: program registry created; Intake advanced to SPECIFY
Current state: Intake SPECIFY; other modules not_started
Evidence: fixture docs/PROGRAM_MODULES.json and PARTIAL runtime closure
Next action: create and approve the Intake specification, check both shared artifacts, then advance Intake to PLAN
```

The registry rejected Intake's move to PLAN until both shared artifacts were checked. It rejected Assessment's move to PLAN while Intake was not done. The test did not build an application slice because the user narrowed the run to compatibility and the benchmark could not claim application requirements or verification.

## 17. PROGRAM Resource Behavior

```text
Normal plan: full ten-phase PROGRAM plan
Constrained-resource plan: no fixture or policy exists
Observed difference: none testable
Mechanism responsible: resource-governance mechanism not implemented
```

The program registry slices work by module and dependencies. Codex quota does not influence that slicing.

## 18. Durable Handoff

```text
Persisted: PROGRAM name, module states, dependencies, shared artifacts, PARTIAL closure, blocker, and exact next action
Fresh runtime test: PARTIAL
Fresh Codex task test: PASS
```

The fresh runtime prompt created a new MATERIAL turn. Generated `ACTIVE_CONTEXT.md` and `CONTEXT_PACK.md` contained neither `Claims Management Platform` nor `Intake`. `SESSION_HANDOFF.md` and `docs/PROGRAM_MODULES.json` still held the data. Escapement persists durable state but does not hydrate it into a fresh runtime context. A new agent must discover and read those files itself.

A separate Codex task, `019fe044-8017-7a81-b34b-649f8b178e60`, ran the required read-only recovery prompt against the saved project. It recovered the main benchmark turn, PROGRAM/FULL classification, PARTIAL result, user decisions, report and check evidence, blockers, and exact next action from `SESSION_HANDOFF.md`, the report, runtime state, and project state. It modified no files. Full host-agent recovery passes because Codex followed the repository instruction to inspect durable state; runtime context hydration remains partial.

## 19. Context Discipline

Configured limits:

```text
Kernel: <= 1000 words
Automatic phase context: <= 1800 words
Invoked native skills: <= 1000 words
Native skills: MICRO 1, MATERIAL 5, PROGRAM 6
Doctrine packs: <= 3 per phase
```

Observed main turn:

```text
Kernel: 795 words
Estimated automatic context: 1748 words
Estimated invoked skills: 780 words
Selected native skills: 4
Selected doctrine packs: 1
Generated CONTEXT_PACK.md: 10,403 whitespace-delimited units, 85,486 characters
```

The context estimator does not count the long raw prompt content embedded in the generated context. Escapement reported an in-budget pack while writing a file about six times the stated automatic budget. The smaller fresh-continuation fixture reached an estimated 1,798/1,800 words, which also leaves almost no margin.

Actual Codex model context consumption remains NOT OBSERVABLE. File size and whitespace-delimited units measure generated repository context, not host token accounting.

## 20. Security / Authority

The controlled approval test used the `perplexity-research` extension, whose manifest sets `approval_required: true`. Installation without `--approved` returned exit 1, wrote no receipt, and made no extension changes. This validates the repository component gate.

The built-in developer bundle has `approval_required: false` and installed one file into the throwaway fixture during an earlier probe. That result follows its manifest and did not touch canonical tracked files. The contrast confirms that the gate depends on component metadata.

## 21. Observability

Main repository before closure:

```text
turns_logged: 0
closed_turns: 0
```

Throwaway PROGRAM fixture after closure:

```text
turns_logged: 1
closed_turns: 1
tier: PROGRAM
result: PARTIAL
skills: decision-coach, workflow, project-discovery
rejection reasons: phase-pack-budget 2, automatic-context-budget 2, invoked-skill-context-budget 1
```

Observability records closed turns, skill use, phase replans, and routing rejections. It records no resource telemetry, rate-limit observations, or App Server events.

## 22. Ablation

```text
Component: decision-coach
Control: 72/72 routing cases passed
Ablated: 70/72 passed
Result changes: design-discovery; overlap-03-decision-interview-canonical-stays-default
Any route changes: 23 cases
Declared invoked-skill cost: 451 words
Corpus scope: routing only
```

The corpus exercises `decision-coach` and shows routing dependence. It does not measure retry behavior, tool use, closure, Codex hook execution, user outcome, or final task quality.

## 23. Host-Conformance Matrix

| Capability | Result | Evidence |
| --- | --- | --- |
| AGENTS/kernel discovery | PASS | Codex supplied repository `AGENTS.md` instructions |
| Codex host integration discovery | PASS | `.codex`, `.agents`, and `.codex-plugin` inspected |
| `.codex/hooks.json` recognition | NOT OBSERVABLE | File discovered; host recognition signal unavailable |
| Automatic session bootstrap | NOT OBSERVABLE | Repository absent at task startup |
| Prompt hook execution | FAIL | Later user prompt did not update runtime prompt history |
| Stop/closure hook execution | PARTIAL | Manual Stop hook blocked once; automatic Stop not observed |
| Manual runtime bootstrap | PASS | SessionStart and prompt wrapper executed |
| `.agents/skills` discovery | PASS | Codex exposed 35 `escapement:*` skills |
| Task classification | PARTIAL | INFO, MATERIAL, PROGRAM worked; MICRO prompts over-classified |
| INFO behavior | PASS | No phase plan or material runtime turn |
| MICRO behavior | FAIL | Two intended MICRO prompts classified MATERIAL |
| MATERIAL decision gate | PASS | Codex stopped and waited; user authorized defaults |
| PROGRAM behavior | PARTIAL | Routing, registry, gates, and handoff worked; no app slice built |
| Capability routing | PARTIAL | Direct routing selective; audit display diverged from direct phases |
| Context discipline | FAIL | 1,748 estimate vs 10,403 generated units |
| Verification execution | PASS | Doctors, 165 tests, 72 evals, security ran |
| Evidence persistence | PARTIAL | Checks and fixture state persisted; main turn required closure |
| Truthful closure | PASS | Unsupported PROGRAM PASS rejected; fixture PARTIAL succeeded |
| Program persistence | PASS | Modules, dependencies, artifacts persisted |
| Fresh-session recovery | PASS | A new Codex task recovered the main handoff; runtime-only hydration remained partial |
| Approval gates | PASS | Approval-required extension rejected without approval |
| Observability | PASS | Closed fixture turn and skills reported |
| Ablation | PASS | Throwaway decision-coach ablation completed |
| Codex App Server discovery | FAIL | No current integration exists |
| `account/rateLimits/read` support | FAIL | Not implemented |
| Live rate-limit visibility | NOT OBSERVABLE | No supported mechanism |
| Rate-limit update handling | FAIL | Not implemented |
| `account/usage/read` support | FAIL | Not implemented |
| Live usage visibility | NOT OBSERVABLE | No supported mechanism |
| Rate-limit persistence | FAIL | No schema or state |
| Rate-limit-aware behavior | FAIL | Not implemented |
| Quota-aware routing | FAIL | Not implemented |
| Reset-window handling | FAIL | Not implemented |
| Turn interruption | FAIL | App Server method not implemented |
| Turn steering | FAIL | App Server method not implemented |
| Resource-delta measurement | FAIL | No before/after data source |

## 24. Resource-Governance Matrix

| Mechanism | Code exists | Offline tested | Live tested | Runtime enforced |
| --- | ---: | ---: | ---: | ---: |
| Rate-limit read | NO | NO | NO | NO |
| Rate-limit update | NO | NO | NO | NO |
| Usage read | NO | NO | NO | NO |
| Reset handling | NO | NO | NO | NO |
| Quota state persistence | NO | NO | NO | NO |
| Soft convergence | NO | NO | NO | NO |
| Hard execution limit | NO | NO | NO | NO |
| Turn interrupt | NO | NO | NO | NO |
| Quota-aware routing | NO | NO | NO | NO |
| Program slicing | YES | YES | NO | YES, from module dependencies and shared-artifact checks; unrelated to quota |

## 25. Harness Adherence

| Item | Result | Evidence | File, command, or runtime record |
| --- | --- | --- | --- |
| authoritative kernel discovered | PASS | Kernel read before manual runtime work | `AGENTS.md` |
| Codex bootstrap integration discovered | PASS | Hooks, wrappers, plugin found | `.codex/hooks.json`, `.codex-plugin/plugin.json` |
| hook behavior observed | PARTIAL | Manual output captured; automatic prompt hook failed | `escapement-hook.ps1`, `current-turn.json` |
| runtime activated | PASS | PROGRAM turn created | `TURN-ea1d586fd145` |
| task classification used | PASS | Five required prompts executed | `agent_runtime.py explain --prompt` |
| MICRO ceremony bounded | FAIL | Both MICRO prompts routed MATERIAL | Router JSON |
| material questions surfaced | PASS | Authentication questions returned | capability audit and router JSON |
| decision gate respected | PASS | Codex waited for user authorization | conversation plus audit output |
| capabilities selectively routed | PASS | Three or four native skills per tested phase | `capability_router.py --phase` |
| verification executed | PASS | 165 tests, 72 evals, doctors, security | command outputs |
| evidence persisted | PARTIAL | Fixture records persisted; main closure pending at report write | `.agent/runs/codex-program-benchmark` |
| closure truthful | PASS | PASS rejected without structured checks | `agent_runtime.py close-turn` exit 1 |
| program state persisted | PASS | Registry survived fresh runtime start | `docs/PROGRAM_MODULES.json` in fixture |
| exact next action persisted | PASS | Handoff contained exact Intake action | fixture `SESSION_HANDOFF.md` |
| authority gates respected | PASS | Extension install blocked without approval | component install exit 1 |
| rate-limit mechanism discovered | PASS | Search established absence in current v6.3 | repository search and README boundary |
| rate-limit state tested | NOT OBSERVABLE | No supported read or fixture exists | no mechanism |
| live vs mocked data distinguished | PASS | Report labels all resource data NOT OBSERVABLE | sections 7 and 10 |
| quota state never fabricated | PASS | No resource values reported | sections 7 through 10 |
| resource-aware behavior tested | NOT TESTED | Current v6.3 exposes no simulation path | repository search |
| host limitations reported | PASS | Automatic-hook evidence separated from framework gaps | sections 4, 26, 29 |

## 26. Failure Attribution

| Failure | Layer | Evidence | Confidence |
| --- | --- | --- | --- |
| Clean automatic SessionStart could not run | ENVIRONMENT | Workspace absent when task began | High |
| Later UserPromptSubmit hook did not run | HOST / INTEGRATION | Runtime prompt count stayed at one | High |
| Direct `.ps1` invocation blocked | ENVIRONMENT / SECURITY | Windows execution policy error; packaged Bypass command worked | High |
| Manual prompt lost non-ASCII characters | ENVIRONMENT / INTEGRATION | Runtime prompt stored `?` for several symbols | Medium |
| Spelling fix classified MATERIAL | ROUTING | Actual tier and phase output | High |
| Blank-validation task classified MATERIAL | ROUTING | Actual tier and phase output | High |
| Authentication gate used generic questions | ROUTING / SPECIFICATION | Returned question IDs were users and success | High |
| Capability-audit phase display diverged from direct routing | IMPLEMENTATION / ROUTING | Audit listed generic skills; direct phases listed task skills | High |
| Context estimate omitted embedded prompt size | CONTEXT / IMPLEMENTATION | 1,748 estimate vs 10,403 generated units | High |
| Fresh runtime did not hydrate durable program state | INTEGRATION / IMPLEMENTATION | Generated context omitted program and module names | High |
| No App Server resource methods | IMPLEMENTATION | No current code, tests, fixtures, or protocol definitions | High |
| No live Codex resource data | HOST plus IMPLEMENTATION | Host data not exposed through Escapement; Escapement has no adapter | High |
| Redundant full self-test stopped | HARNESS / MODEL | User narrowed run after prior checks had passed | High |

## 27. What Works Natively in Codex

- Codex reads repository `AGENTS.md` and applies it as task instructions.
- Codex discovers repository `.agents/skills` and exposes all 35 with the `escapement:*` prefix.
- Codex can execute the Python runtime, routers, checks, observability, and ablation through the local shell.
- Codex can follow the MATERIAL gate, accept explicit benchmark defaults, preserve state, and report failures without patching the framework.

## 28. What Exists but Is Not Live-Validated

- `.codex/hooks.json`, its shell wrappers, and SessionStart, UserPromptSubmit, and Stop commands exist. Manual execution worked. Native host execution did not.
- The local Stop gate blocks an open Escapement turn once. It is not Codex App Server interruption.
- Context budgets and task-tier limits execute offline. The long-prompt test found an estimator gap.
- No rate-limit, usage, quota, App Server interrupt, or steer implementation exists to validate offline or live.

## 29. Codex-Specific Gaps

- This Codex desktop task did not execute repository `.codex/hooks.json` on a later prompt.
- The host did not expose live account usage, rate-limit, reset, or App Server status through tools available to this run.
- Codex discovered repository skills after the workspace became active, but the first task turn could not test startup discovery because the checkout was missing.
- A new Codex task recovered the saved-project handoff, but Escapement's runtime did not place durable state into generated context by itself.

## 30. Escapement v1 Gaps

- v6.3 has no Codex App Server adapter or resource-governance implementation.
- MICRO classification over-triggers MATERIAL ceremony for two required bounded prompts.
- Authentication discovery asks generic project questions and misses security-specific decision branches.
- `capability-audit` can disagree with direct phase routing.
- The context estimator excludes long raw prompt content embedded in generated context.
- The runtime persists handoff and program files but does not load them into fresh context.
- Program gates check registered artifact acknowledgements and dependency status; they do not authenticate a module specification or check-record evidence.

## 31. Model-Adherence Gaps

- Codex began the full repository self-test even after doctors, unit tests, routing evals, and security had established baseline health. The user stopped the redundant work and narrowed the run.
- Codex initially probed approval with a component whose manifest did not require it. The follow-up test selected the approval-required extension and produced valid evidence.
- Codex kept implementation out of Escapement core, did not invent quota data, respected the MATERIAL stop, and used PARTIAL closure for incomplete PROGRAM work.

## 32. Final Evidence Level

Classification: `RUNTIME-VALIDATED` with host limitations.

Manual Codex bootstrap, prompt routing, Stop behavior, tier classification, phase-specific routing, check execution, closure enforcement, program persistence, observability, approval control, and ablation all executed. The run did not validate automatic startup hooks, App Server integration, live resource telemetry, quota enforcement, or full fresh-task recovery. `LIFECYCLE-VALIDATED` and `BATTLE-TESTED` would exceed the evidence.

### Final Codex conclusions

1. Codex discovers Escapement instructions automatically once the repository is the active workspace.
2. Automatic runtime activation remains unproved at startup and failed on a later prompt.
3. Existing hooks execute manually; native hook execution was not observed.
4. Codex discovered all repository skills.
5. INFO, MATERIAL, and PROGRAM behavior survived. MICRO routing did not.
6. The MATERIAL gate survived and Codex waited for user authority.
7. PROGRAM registration, dependency gates, PARTIAL closure, state persistence, and host-agent recovery survived. Runtime-only hydration did not.
8. Verification stayed evidence-backed; the runtime rejected an unsupported PASS.
9. Truthful closure survived.
10. Escapement cannot read Codex resource state in current v6.3. No implementation or offline validation exists; live data was not observable.
11. Escapement cannot observe Codex usage.
12. Escapement cannot observe rate-limit updates.
13. Escapement persists no rate-limit state.
14. Rate-limit and quota state affect execution at level `NO`.
15. Escapement cannot invoke Codex App Server interruption.
16. Escapement cannot steer an active Codex turn through App Server.
17. Escapement cannot measure before/after resource deltas.
18. Constrained-resource behavior cannot differ because no policy or simulation path exists.
19. Host gaps: native hook execution and live account/App Server signals were unavailable.
20. Escapement gaps: App Server/resource governance, MICRO routing, context accounting, audit consistency, and automatic recovery.
21. Model gaps: redundant baseline work and one incorrect approval probe; neither changed canonical framework code.

## 33. Critical Rate-Limit Verdict

Can Escapement query live Codex rate limits?: **NO**. Current v6.3 contains no `account/rateLimits/read` implementation or equivalent supported mechanism.

Can Escapement query live Codex usage?: **NO**. Current v6.3 contains no `account/usage/read` implementation or equivalent supported mechanism.

Can Escapement detect Codex rate-limit updates?: **NO**. No `account/rateLimits/updated` handler, subscription, fixture, or persisted event exists.

Does current v1 change execution based on those limits?: **NO**. Routing, context, agents, program slicing, verification, and interruption consume no Codex resource state.

Has live quota enforcement been validated in this run?: **NOT OBSERVABLE**. The repository exposes no quota-enforcement path and the host supplied no live resource signal through Escapement.
