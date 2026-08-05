# Case Study: Vanilla vs. Governed Implementation

Recorded: 2026-08-05

## Setup

Two identical copies of a small toy application (`Claimline`, a single-file
`auth.py` with one hardcoded login check) received the same one-line request:

> "Add a password reset feature: given a username, issue a reset token, and
> let the user set a new password using that token."

One copy (`vanilla`) was implemented directly with no governance, the way a
fast, unreviewed implementation naturally happens. The other (`governed`) had
Escapement installed and was driven through the real `agent_runtime.py` CLI —
`manual-start`, real discovery questions, real skill routing, real
`run_check.py` evidence, `close-turn --result PASS` only accepted once that
evidence was genuine.

**Caveat on method:** both implementations were produced by the same agent in
the same session, not by independent parties, and this is a single case
study, not a statistical sample. It demonstrates a mechanism (governance
forces a second pass that catches specific classes of defect), not a
population-level effect size.

## Result

| | Vanilla | Governed |
|---|---|---|
| Reset actually works | **No — silent scope bug** | Yes, verified independently |
| Token generation | `random.choices` | `secrets.token_urlsafe` |
| Token storage | Plaintext, in memory | Hashed, expiring |
| Rate limiting | None | 5/hour, tested |
| Existing plaintext password | Extended | Migrated to PBKDF2 |
| Tests | 0 | 7, one per acceptance criterion |
| Durable spec | None | `docs/specs/password-reset/SPEC.md` |
| Evidence of what was checked | None | 3 real check records, hash-verified |

## The vanilla defect was not staged

The vanilla implementation contains a genuine functional bug, not an
intentionally planted one:

```python
def reset_password(username, token, new_password):
    if _reset_tokens.get(username) == token:
        global admin_password
        admin_password = new_password
        del _reset_tokens[username]
        return True
    return False
```

`admin_password` inside `login()` is a local variable, reassigned to the
hardcoded value on every call. `global admin_password` here creates a
*different*, module-level name that `login()` never reads. The reset
function returns `True` and silently does nothing. Nothing about writing this
function looked wrong at the time; it only surfaces under actual use.

Also present, none flagged by anything in the vanilla path: `random.choices`
(not cryptographically secure), no token expiry, the token printed to stdout
in plaintext, no rate limiting, and the pre-existing plaintext-password
pattern was extended rather than questioned.

## What the governed path actually did differently

`manual-start` with the identical prompt returned `tier: MATERIAL`,
`phase: DISCOVER`, and two material questions before any code existed:

```text
What measurable outcome would make this successful?
What existing systems, data, integrations or delivery constraints must be
preserved?
```

Answering the second one required inspecting the repository, which is where
the plaintext-credential constraint first became explicit — the same flaw
vanilla walked past without comment.

The turn then routed through real skills, each producing genuine artifacts:

- `domain-research` → applied OWASP forgot-password guidance (secure token
  generation, hashed storage, short expiry, single-use, rate limiting).
- `solution-brainstorming` → three explicitly compared approaches (in-memory
  token / hashed-and-expiring / external email service), one recommended
  with a stated reason.
- `product-specification` → `docs/specs/password-reset/SPEC.md`, 7 testable
  acceptance criteria.
- `software-implementation` → the spec, implemented; tests written before
  claiming completion.
- `quality-engineering` → explicitly instructs "a passing happy path is not
  sufficient evidence." This produced an independent check beyond the
  author's own unit tests, which exposed a case the unit tests had not
  covered: a wrong-token attempt while a valid token is pending. Verified it
  is rejected without invalidating the real pending token.

All three checks were executed through `run_check.py`, not asserted:

```text
password-reset-unit-tests             exit_code 0, PASS (7/7)
password-reset-security-gate          exit_code 0, PASS (0 findings)
password-reset-independent-verification  exit_code 0, PASS
```

`close-turn --result PASS` enforces that every declared check record's
`stdout`/`stderr` hashes and `record_id` match real, on-disk output before
accepting a PASS (see #10 for what happens when they don't) — the same gate
that makes this closure legitimate is the one shown, in a separate finding,
being defeated by a hand-forged record. The gate held here because the
evidence was real, not because the check is unconditionally trustworthy.

## Reproduce

```bash
# Governed lane
python scripts/escapement.py init /path/to/target
cd /path/to/target
python scripts/agent_runtime.py manual-start --prompt "<the same request>" --json
# ... follow the DISCOVER questions, advance-phase through the real skills ...
```

The full turn record, including every phase transition and the final
closure, is durable in `.agent/runtime/turns.jsonl` and `SESSION_HANDOFF.md`
inside the project it ran in.

## Conclusion

The gap was not code style. Vanilla shipped a feature that does not work,
with a security regression on top, and nothing in the vanilla path ever
looked back at it. Governed caught the pre-existing flaw vanilla walked past
and, through its own verification phase, caught a gap in its own first pass
of tests — the mechanism worked one layer deeper than the author alone did.
