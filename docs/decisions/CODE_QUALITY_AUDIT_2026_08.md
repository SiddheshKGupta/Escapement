# Code Quality Audit — v1, August 2026

```text
DATE      2026-08-10
SCOPE     scripts/ (14 modules) and tests/, deterministic tools only
TRIGGER   "have you actually cleaned the vibecoded codebase, or are you
          just layering more AI on top?"
TOOLS     ruff 0.1.5, flake8 6.1.0 (mccabe), pyflakes 3.1.0,
          stdlib ast for cycles, dead defs and duplication
VERDICT   9 real findings. 4 fixed with proof. 5 reported, not acted on.
          No structural rot found.
```

## Fallow does not apply here

Fallow analyses **TypeScript, JavaScript, CSS, Vue, Svelte and Astro**.
Escapement v1 is **pure Python**. Fallow cannot read a line of it.

The *idea* transfers; the tool does not. The Python equivalents were used
instead: `ruff` (subsumes pyflakes, mccabe and a subset of bandit),
`flake8`, and stdlib `ast` for the analyses none of them do.

## What was clean

Stated first because a clean result is a result, and reporting only
findings would misrepresent the codebase.

```text
circular dependencies         0   import graph is a clean DAG
unreferenced module functions 0   no dead public functions
third-party runtime imports   0   stdlib only, verified by AST
unused dependencies           N/A there are none to be unused
commented-out code (ERA001)   0
duplicate function bodies     1   and it is justified -- see F-9
```

The import graph is strictly layered, with `capability_router` as the
shared core and nothing importing upward:

```text
agent_runtime    -> capability_router, codex_resources, run_check
capability_audit -> capability_router
escapement       -> capability_router
eval_harness     -> capability_router
```

For a codebase built largely with coding-assistant help, no cycles and
no dead functions is a better result than expected, and it is the part
of the reviewer's challenge that the evidence answers directly.

## Findings

### Fixed — evidence supports the change

**F-1 · Dead import.** `scripts/escapement.py` imported `os`, unused.
`ruff F401`. Removed.

**F-2 · Duplicate dictionary key.** `capability_router.py` declared
`"500-ai-agents-projects"` twice, lines 137 and 162. `ruff F601`.

The values were **byte-identical**, so the second silently overwrote the
first with the same data and no behaviour depended on it. Verified equal
before deleting rather than assumed — an unequal pair would have been a
real routing bug and a different fix.

**F-3 · Dead parameter.** `local_viewer.page(token)` never read `token`.
Confirmed by AST and by grep: the function body contains no reference,
and the page carries no `<script>` or `fetch`, so it is fully
server-rendered. Parameter removed.

**F-4 · Stale licence claims in three documents.** Three places still
described "Escapement's source-available core" after the Apache-2.0
relicence — missed by the relicence PR itself.

Corrected, and the guidance is now **stronger rather than weaker**:
copying AGPL or GPL code into a permissive core is worse than into a
proprietary one, because downstream users receive it under Apache-2.0
terms they cannot lawfully exercise over copyleft material.

**F-5 · Seven blind exception handlers.** `ruff BLE001`. All seven were
the same shape:

```python
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    ...
```

Narrowed to `(OSError, ValueError)`, which covers every realistic
failure — `JSONDecodeError` and `UnicodeDecodeError` both subclass
`ValueError`.

This is the one fix that changes behaviour, deliberately. Previously an
`AttributeError` or `TypeError` from a genuine bug in the `try` block
was caught and reported as *"invalid check record"* or silently returned
a default. Real bugs were being relabelled as malformed input. They now
propagate.

### Reported, not acted on

**F-6 · 13 functions over the complexity threshold.** `ruff C901`.

```text
select_phase_strengths   35     evaluate                29
command_doctor           25     manifest_count_check    22
build_context_pack       19     render                  18
command_close            17     select_skills           16
query_resource_state     14     command_advance         12
load_checks              11     select_external         11
scan_mcp                 11
```

Not refactored. There is no observed failure attributable to any of
them, they are the most heavily exercised code in the repository, and
"a metric says this looks ugly" is not evidence. Splitting a 35-branch
router on that basis risks behaviour change for a number.

Worth admitting: **`manifest_count_check` at 22 is partly my doing** —
grouping the README drift patterns raised it. It was 19 before.

**F-7 · `/api/data` has no in-page consumer.** `local_viewer` serves a
JSON endpoint that the rendered page never calls. It is plausibly
intentional for scripted access with the token. Evidence is
insufficient to call it dead, so it stays.

**F-8 · Two more unused arguments.** `build_context_pack(prompt)` and
`make_record(target)`. Both are stable signatures with callers; the
churn outweighs the gain.

**F-9 · `sha256_file` duplicated** in `escapement.py` and
`run_check.py`, structurally identical. **Justified, not fixed.**
`run_check.py` is deliberately standalone — it is the evidence runner,
and giving it an import dependency on the CLI to save three lines would
couple the thing that records evidence to the thing being recorded.
Duplication is the cheaper trade here.

**F-10 · 55 `S603` subprocess warnings.** Ruff flags every
`subprocess.run`. After the `--shell` removal all call sites use literal
argv with `shell=False`. Not actionable; noise from a rule that cannot
see the argument is trusted.

## Not measured

Stated rather than left as an implied pass:

```text
branch coverage        coverage.py is not installed; untested branches
                       were NOT measured. 196 tests pass, which is not
                       the same claim.
type consistency       mypy not installed
security scanning      bandit not installed; ruff's S rules cover part
duplication across
  non-function scope   only function bodies were compared
```

## Method

```bash
python -m ruff check scripts/ tests/ --select F,E9,C90,S,BLE,ERA,ARG,B,SIM,RET,PIE
python -m ruff check scripts/ --select C901        # complexity
python -m compileall -q scripts/
# stdlib ast: internal import graph, cycle detection, unreferenced
# module-level defs, normalised function-body hashing for duplication
```

Every fix was verified by the full suite, not by the tool that found it.

## Conclusion

The reviewer's challenge was fair to ask and the answer is now
evidenced: **the residue found was small and shallow.** One dead import,
one duplicate key with identical values, one dead parameter, three stale
sentences, and seven over-broad handlers. No cycles, no dead functions,
no dependency rot, no copied-in code.

The real weaknesses are elsewhere and already recorded: complexity in
the router and doctor, and the absence of coverage measurement. Neither
is "vibecoded residue"; both are ordinary engineering debt.
