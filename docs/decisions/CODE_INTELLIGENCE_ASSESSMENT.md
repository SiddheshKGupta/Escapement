# Code Intelligence — assessment against v1 and Core

```text
DATE     2026-08-10
TRIGGER  external review asking whether Escapement treats deterministic
         code intelligence as first-class, prompted by Fallow (JS/TS)
VERDICT  concept NOT accounted for as evidence. One narrow gap is earned
         and should be filled. A generic CodeIntelligence subsystem is
         NOT earned and should not be built.
```

## The eight questions, answered from the repository

### 1. Have we already accounted for this concept explicitly?

**No.** Partially, and only as routing targets.

```text
"code intelligence"  0 occurrences in any file
\bAST\b              0 occurrences
"static analysis"    0
"call graph"         0
"LSP" / tree-sitter  0
import ast           0 -- v1 parses no Python anywhere
```

### 2. If yes, where exactly?

Six resources are catalogued, all `on-demand` external tools:

```text
perplexity-codescythe        code-review            code-analysis-tool
sanyuan-skills               code-review            code review skill
claude-code-review           code-review            managed service
graphify                     memory-and-knowledge   code knowledge graph
egonex-understand-anything   memory-and-knowledge   read-only analysis
nanonets-graft               memory-and-knowledge   code context layer
```

They appear in `catalog/capability-registry.json` and the overlap groups.
They appear in **no ADR and nowhere in the evidence model.**

### 3. Deterministic evidence, or an optional tool the LLM may call?

**An optional tool the LLM may call.** Unambiguously.

The runtime knows exactly two record types:

```text
record_type: "check"   a command ran -- exit code, stdout/stderr sha256
record_type: "eval"    routing evaluation
```

Closure evidence is a list of **file paths that must exist**. So a
code-intelligence tool can be run through `run_check.py`, and what gets
recorded is *that it exited 0*. Its findings land in `stdout.txt`, hashed
but never parsed. Nothing can consume what it found.

### 4. Does the verification plane consume structural evidence?

**No.** It consumes two things: an exit code, and whether a file exists.

This is the precise gap. Not "we have no code intelligence" — v1 can
already run any analyser. It is that **an analyser's findings cannot
become evidence**; only its exit status can.

### 5. Should a generic `CodeIntelligence` capability exist in Core?

**Not now, and ADR-004 forbids building it** — no Core subsystem is
authorized until `EXPERIMENT_CORE_000` runs and a failed invariant
survives the reduction ladder.

But the reviewer's flow already has a home in the design without a new
plane:

```text
untrusted worker proposes diff
        -> code intelligence + independent CI       these are EVIDENCE
        -> trusted verdict                          this is CLOSURE
```

`CORE_EPISODE_SCHEMA_v0.1.md` has a verification strength ladder
`NONE < ASSERTED < CHECKED < INDEPENDENT < ADVERSARIAL`. Deterministic
structural analysis is `CHECKED`, or `INDEPENDENT` when the analyser was
not authored in the episode. **The schema already has the slot.** What
it lacks is a typed evidence kind so findings, rather than exit codes,
can fill it.

That is a field, not a subsystem, and it is the one thing worth
reserving now — because retrofitting an evidence kind onto recorded
episodes is the migration the schema-first ordering exists to avoid.

### 6. Should v1 MCP expose read-only structural queries?

**It should expose what v1 actually knows, which is repository structure,
not code structure.**

v1 has three deterministic checks — `manifest_count_check`,
`license_status_check`, `overlap_group_tag_check` — plus routing
explanation, capability audit and evidence records. All are real and all
are worth exposing.

`callers`, `dead code`, `impact`, `architecture violations` require
analysis v1 does not perform. Exposing them over MCP would mean building
the analysis first. That is the tail wagging the dog: MCP is an
interface to capability, not a reason to acquire it.

### 7. Are we duplicating what Fallow already solves?

**Not currently.** v1 performs no AST, symbol, dependency or duplication
analysis, so there is nothing to duplicate.

The risk is prospective and worth naming: building a general AST /
dependency-graph / duplication / complexity layer would duplicate
Fallow (JS/TS), tree-sitter, every language server, and the six tools
already catalogued. **Escapement should own the evidence contract, not
the analysers.** Language-specific adapters are exactly the part to
delegate.

### 8. Smallest architectural change

Not an interface. **Make the effect surface audit a `doctor` check,
AST-based.**

This is earned by an observed failure, and the failure is ours:

```text
claim     "v1 has no model-to-effect path"
method    grep for 3 patterns across 2 of 14 files
result    0 matches -> claim accepted into three documents and an ADR
truth     47 effect primitives in 7 files, including a shell=True site
          reachable from a model-written string in feature_list.json
```

That is precisely the failure mode the review describes: **the agent
manufacturing its own representation of the codebase by reading files.**
A dependency and call graph answers "what can reach `subprocess`?"
deterministically. Text search answers a different question and I
mistook one for the other.

The fix already recommended twice and never built:

```text
enumerate effect primitives via ast, not regex
  FILESYSTEM_WRITE  PROCESS_EXECUTION  NETWORK  DESERIALIZATION
trace each to the callable entry points that reach it
fail on a new primitive that is not on the recorded baseline
```

Roughly 50 lines using the standard-library `ast` module. Python-only,
which is fine — v1 is Python. It is the first genuine code-intelligence
primitive in the repository, and it exists because something broke, not
because a category looked incomplete.

**A worked example of why AST beats text**, from this same change: the
new `test_run_check_no_shell.py` asserts no source file contains
`shell=True` — by scanning text. It would not catch `shell=flag`,
`shell=bool(x)`, or `**kwargs`. It is the same weak method that produced
the false claim, and an AST check would subsume it.

## Recommendation

```text
NOW        effect surface audit as an AST-based doctor check   EARNED
NOW        reserve a typed structural evidence kind in the
           Core episode schema (a field, not a subsystem)      CHEAP
LATER      v1 MCP exposes what v1 knows: routing, catalog,
           doctor, evidence -- not invented code intelligence
NOT NOW    generic CodeIntelligence interface                  UNEARNED
NEVER      our own AST/graph/duplication/complexity engine      DELEGATE
```

Extract an interface only when **three** analyses have each earned their
place the same way. An interface designed before its implementations is
the abstraction-for-single-use the contributing guide already rejects,
and Continuum's whole Phase I was one architecture designed ahead of the
problems it claimed to solve.

## What would change this verdict

A recorded failure where an agent working under v1 produced a wrong
change that structural analysis would have caught — a missed caller, a
cycle, a dead export treated as live. One such case moves dependency and
impact analysis from "unearned" to "earned", by the same route the
effect surface audit took.
