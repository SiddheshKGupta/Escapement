# Codex Resource Repairs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair three reproduced Codex resource-adapter defects without changing shared, Claude, or Gemini files.

**Architecture:** Keep the public adapter API unchanged. Validate persisted resource windows at the policy boundary, govern only from valid 300-minute windows, and continuously drain App Server stderr into a bounded diagnostic tail. The three fixes share the same implementation and test files, so they execute sequentially rather than through conflicting parallel edits.

**Tech Stack:** Python 3 standard library, `unittest`, JSONL subprocess transport.

## Global Constraints

- Modify only `scripts/codex_resources.py` and `tests/v6_3/test_codex_resources.py`.
- Do not modify shared runtime/router files, Claude files, Gemini files, manifests, historical reports, or benchmark v1.
- Add no dependency.
- Write and run each regression test before its production change.
- Keep valid persisted-state round trips backward compatible.
- Resource enforcement uses only validated 300-minute windows.
- Retain at most a bounded stderr tail; never allow child stderr to block stdout protocol progress.

---

### Task 1: Restrict policy governance to valid five-hour windows

**Files:**
- Modify: `tests/v6_3/test_codex_resources.py`
- Modify: `scripts/codex_resources.py`

**Interfaces:**
- Consumes: `assess_resource_policy(state: dict[str, Any] | None, *, now_epoch: float | None = None) -> dict[str, Any]`
- Produces: `_validated_five_hour_windows(state: dict[str, Any] | None) -> list[dict[str, Any]]`

- [ ] **Step 1: Write the failing weekly-window regression**

Add a test that supplies only this literal state and asserts `UNOBSERVED`, refresh required, and no block:

```python
state = {
    "windows": [{
        "limit_id": "codex",
        "bucket": "secondary",
        "used_percent": 100,
        "window_duration_mins": 10_080,
        "resets_at": 1_700_600_000,
    }],
    "five_hour_windows": [],
}
policy = assess_resource_policy(state, now_epoch=1_700_000_000)
self.assertEqual(policy["mode"], "UNOBSERVED")
self.assertTrue(policy["needs_refresh"])
self.assertFalse(policy["block_new_turn"])
```

- [ ] **Step 2: Verify RED**

Run:

```powershell
python -m unittest tests.v6_3.test_codex_resources.CodexResourceStateTest.test_non_five_hour_window_never_governs_policy
```

Expected: FAIL because the weekly window currently produces `EXHAUSTED`.

- [ ] **Step 3: Implement exact five-hour selection**

Add a helper that accepts only dictionaries with a non-empty string `limit_id`,
`bucket` in `{"primary", "secondary"}`, numeric non-boolean `used_percent`, exact
integer duration `300`, and numeric-or-null `resets_at`. Use
`five_hour_windows` when that field is a list; fall back to filtering `windows`
only when `five_hour_windows` is absent, for old persisted snapshots.

Replace the current fallback from an empty `five_hour_windows` list to all
windows with this helper.

```python
def _validated_five_hour_windows(state):
    if not isinstance(state, dict):
        return []
    raw = state.get("five_hour_windows")
    if not isinstance(raw, list):
        raw = state.get("windows", [])
    if not isinstance(raw, list):
        return []
    validated = []
    for value in raw:
        window = _validated_window(value)
        if window and window["window_duration_mins"] == FIVE_HOUR_WINDOW_MINS:
            validated.append(window)
    return validated
```

- [ ] **Step 4: Verify GREEN**

Run the focused test and then the complete Codex resource test module. Both must pass.

- [ ] **Step 5: Commit**

Commit only the two owned files with message `Fix five-hour Codex quota selection`.

### Task 2: Reject malformed persisted resource state safely

**Files:**
- Modify: `tests/v6_3/test_codex_resources.py`
- Modify: `scripts/codex_resources.py`

**Interfaces:**
- Consumes: `load_resource_state(path: Path) -> dict[str, Any] | None`
- Produces: defensive policy behavior for invalid windows; no new public API

- [ ] **Step 1: Write failing malformed-state regressions**

Add one direct-policy test with a 300-minute window missing `bucket` and one
persistence test writing that malformed JSON to a temporary file. Assert that
policy evaluation returns `UNOBSERVED` without raising and that loading rejects
the invalid persisted envelope instead of returning crashable state.

```python
malformed = self.snapshot(82)
del malformed["five_hour_windows"][0]["bucket"]
self.assertEqual(
    assess_resource_policy(malformed, now_epoch=1_700_000_000)["mode"],
    "UNOBSERVED",
)

with tempfile.TemporaryDirectory() as temp:
    path = Path(temp) / "state.json"
    path.write_text(json.dumps(malformed), encoding="utf-8")
    self.assertIsNone(load_resource_state(path))
```

- [ ] **Step 2: Verify RED**

Run the two new tests. Expected failures are the current `KeyError: 'bucket'`
and acceptance of the invalid persisted state.

- [ ] **Step 3: Implement minimal defensive validation**

Reuse the Task 1 window validator in `assess_resource_policy`. In
`load_resource_state`, reject an envelope unless it has schema version `1.0`, a
known source, string observation time, object `rate_limits` and `usage`, and list
`windows` and `five_hour_windows`; reject it if any contained window is invalid
for its declared duration. Return `None` for invalid JSON or invalid envelopes.

```python
def _validated_resource_state(value):
    if not isinstance(value, dict):
        return None
    if value.get("schema_version") != "1.0":
        return None
    if value.get("source") not in {"LIVE_HOST_DATA", "FIXTURE", "MOCK"}:
        return None
    if not isinstance(value.get("observed_at"), str):
        return None
    if not isinstance(value.get("rate_limits"), dict):
        return None
    if not isinstance(value.get("usage"), dict):
        return None
    for key in ("windows", "five_hour_windows"):
        raw = value.get(key)
        if not isinstance(raw, list):
            return None
        normalized = [_validated_window(item) for item in raw]
        if any(item is None for item in normalized):
            return None
    return value
```

- [ ] **Step 4: Verify GREEN**

Run both new tests, the persistence round-trip test, and the complete Codex
resource test module. All must pass.

- [ ] **Step 5: Commit**

Commit only the two owned files with message `Validate persisted Codex resource state`.

### Task 3: Drain App Server stderr without deadlock

**Files:**
- Modify: `tests/v6_3/test_codex_resources.py`
- Modify: `scripts/codex_resources.py`

**Interfaces:**
- Consumes: `query_resource_state(command: Sequence[str], *, source: str = "LIVE_HOST_DATA", timeout_seconds: float = 15) -> dict[str, Any]`
- Produces: `_drain_stderr(stream: Any, chunks: deque[str]) -> None`

- [ ] **Step 1: Write the failing large-stderr integration regression**

Create the existing temporary fixture server pattern, but write and flush one
MiB to stderr before processing stdin. Then emit valid initialize, rate-limit,
and usage responses. Call `query_resource_state(..., timeout_seconds=5)` and
assert the returned five-hour window and usage values.

```python
fixture.write_text(
    textwrap.dedent("""
        import json
        import sys

        sys.stderr.write("x" * (1024 * 1024))
        sys.stderr.flush()
        for line in sys.stdin:
            message = json.loads(line)
            method = message.get("method")
            if method == "initialize":
                result = {"userAgent": "fixture"}
            elif method == "account/rateLimits/read":
                result = {"rateLimits": {
                    "limitId": "codex",
                    "primary": {"usedPercent": 81, "windowDurationMins": 300,
                                "resetsAt": 1700000600},
                    "secondary": None,
                }}
            elif method == "account/usage/read":
                result = {"summary": {"lifetimeTokens": 99}}
            else:
                continue
            print(json.dumps({"id": message["id"], "result": result}), flush=True)
    """),
    encoding="utf-8",
)
state = query_resource_state(
    [sys.executable, str(fixture)], source="FIXTURE", timeout_seconds=5
)
self.assertEqual(state["five_hour_windows"][0]["used_percent"], 81)
self.assertEqual(state["usage"]["summary"]["lifetimeTokens"], 99)
```

- [ ] **Step 2: Verify RED**

Run only the new test. Expected: FAIL with an App Server request timeout because
the child blocks on the undrained stderr pipe.

- [ ] **Step 3: Implement bounded concurrent stderr drainage**

Import `deque`, create `deque(maxlen=16)`, and start a daemon thread before the
first request. The drain helper reads 4 KiB chunks until EOF and appends them to
the bounded deque. On `AppServerError`, append a sanitized last 4 KiB stderr tail
to the exception when present. Preserve the existing cleanup and timeout behavior.

```python
def _drain_stderr(stream, chunks):
    while True:
        chunk = stream.read(4096)
        if not chunk:
            return
        chunks.append(chunk)

stderr_chunks = deque(maxlen=16)
stderr_thread = threading.Thread(
    target=_drain_stderr,
    args=(process.stderr, stderr_chunks),
    daemon=True,
)
stderr_thread.start()
```

- [ ] **Step 4: Verify GREEN**

Run the new integration test and the complete Codex resource module. Both must
pass with no timeout.

- [ ] **Step 5: Commit**

Commit only the two owned files with message `Drain Codex App Server stderr`.

### Task 4: Integrated verification and scope proof

**Files:**
- Verify only; no implementation edit expected

**Interfaces:**
- Consumes: all repaired behavior
- Produces: deterministic evidence and protected-path confirmation

- [ ] **Step 1: Run focused tests**

```powershell
python -m unittest tests.v6_3.test_codex_resources
```

Expected: all Codex resource tests pass.

- [ ] **Step 2: Run related runtime tests**

```powershell
python -m unittest tests.v6_3.test_agent_runtime tests.v6_3.test_codex_resources
```

Expected: all tests pass.

- [ ] **Step 3: Run the full repository suite**

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Expected: the three new regressions and all previously passing tests pass. If the
known README terminology failure remains, report it as pre-existing and protected;
do not modify README or its shared consistency test.

- [ ] **Step 4: Prove file scope**

```powershell
git diff origin/main --name-only
```

Expected paths are the Codex benchmark specification/plan plus
`scripts/codex_resources.py` and `tests/v6_3/test_codex_resources.py`; no shared,
Claude, or Gemini path appears.

- [ ] **Step 5: Independent review**

Review the final diff against the three reproductions, test mutations, error
handling, subprocess cleanup, and protected-file contract before completion.
