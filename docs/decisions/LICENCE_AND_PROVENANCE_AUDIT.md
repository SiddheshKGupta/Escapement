# Licence and Provenance Audit — v1

```text
DATE      2026-08-10
COMMIT    64d75f0
SCOPE     licence state, contributor provenance, third-party material,
          external registry, readiness to relicense
VERDICT   provenance is clean; relicensing is technically unblocked
          and is a strategic decision that has not been made
```

## Summary

| Area | Result |
|---|---|
| Current licence | source-available, all rights reserved — **not** OSI |
| Contributor provenance | **clean** — 133/134 commits by the copyright owner |
| Vendored third-party code | **none** |
| Adapted third-party material | one, MIT, method-only, documented |
| External registry (67) | reference-only, correctly gated |
| Blocking issues for Apache-2.0 | **none found** |
| Gaps to close first | 4, listed in §6 |

## 1. Current licence state

`LICENSE.md` grants evaluation, learning, non-commercial experimentation
and attributed internal use. It reserves commercial redistribution,
resale, white-labelling, hosted resale and substantial republication,
and states plainly:

> This notice is not an OSI-approved open-source licence.

**The repository's self-description is accurate and consistent.** The
README badge reads `source-available`, and README line 582 repeats the
non-OSI statement. Nothing in the repository claims to be open source.
This is worth recording because it is the failure mode that would have
mattered most, and it is absent.

GitHub's licence classifier returns `NOASSERTION` — expected for a
custom text. Consequences: no licence shown in the sidebar, and the repo
is invisible to licence-filtered search. That is a *discoverability*
cost of the current licence, not a defect.

**The repository is public and has 1 fork.** Whatever that fork received
was received under the current terms. Relicensing operates forward only;
it does not retroactively alter what has already been distributed. Not a
blocker — but it is why relicensing is effectively one-way.

## 2. Contributor provenance — clean

```text
68  Siddhesh Gupta <63045116+SiddheshKGupta@users.noreply.github.com>
65  Siddhesh Gupta <siddheshgupta7@gmail.com>
 1  Claude <noreply@anthropic.com>
```

Two identities, one person, 133 of 134 commits. The single `Claude`
commit is model output, which does not create a separate human copyright
interest and is owned by the operator under Anthropic's terms.

**There is no third-party copyright holder to obtain consent from.**
This is the condition that usually blocks relicensing, and it does not
apply. Codex-authored PRs merged under the owner's identity do not
change this.

## 3. Third-party code — none vendored

```text
vendor/ third_party/ node_modules/ externals/   absent
foreign copyright headers                        none
SPDX-License-Identifier headers                  none
```

One adaptation is recorded in `THIRD_PARTY_NOTICES.md`: the *Grilling
Intensifier* in `skills/decision-coach/SKILL.md`, adapted from Matt
Pocock's `grilling` skill (MIT). The record states no source file was
copied and the method was rewritten in original wording, with
attribution retained. MIT permits this and is compatible with any
relicensing target.

The record is unusually complete — pinned review date, files affected,
changes made, alternatives rejected, security review, validation tests.
It is the standard the rest of the process should be held to.

## 4. External registry — reference is not derivation

67 resources, every one carrying `license` and `license_status`.

```text
licence status              adoption gate
49  verified                12  verify-licence-first
10  must-verify             12  approval-required
 2  verified-unlicensed
 2  not-open-source
 2  not-code-resource
 1  source-required
 1  special-terms
```

Copyleft and unlicensed resources are gated correctly:

```text
appflowy            AGPL-3.0              approval-required
plausible-analytics AGPL-3.0-or-later     approval-required
claude-mem          AGPL-3.0 (main pkg)   approval-required
evomap-evolver      GPL-3.0-or-later      review-mode-only
gsap                standard licence      approval-required
skill-ui            Unknown               disabled-until-source-confirmed
perplexity-cli      no licence observed   approval-required
awesome-claude-skills  all rights reserved  discovery-only
```

`skill-ui` being *disabled* until its source is confirmed, rather than
listed with a caveat, is the correct default and is applied.

**These resources appear only in catalogue, routing and evaluation
metadata** — `catalog/*.json`, `docs/OVERLAP_ANALYSIS.md`,
`evals/…/evals.json`, `scripts/capability_router.py`. That is naming and
routing, not incorporation. Referencing an AGPL project by name and
deciding whether to route to it does not make Escapement a derivative
work of it.

One nuance worth stating, since it is where this could go wrong later:
the boundary holds because nothing is *executed into* Escapement's
process or *copied* into its source. If Core later invokes an AGPL tool
in-process rather than as a separate program, that analysis changes.
Recorded now, while it costs nothing.

## 5. What Apache-2.0 would additionally require

Apache-2.0 is a superset of what MIT asks for. Beyond a `LICENSE` file:

```text
NOTICE file           exists, but would need Apache NOTICE semantics
                      (attribution propagated by downstream redistributors)
patent grant          Apache-2.0 §3 grants patent rights from
                      contributors -- this is a real grant, not boilerplate
inbound = outbound    CONTRIBUTING.md must state that contributions are
                      licensed under the project licence
per-file headers      conventional, not required
state changes         §4(b) requires modified files be marked
```

## 6. Gaps to close before any relicence

| # | Gap | Severity |
|---|---|---|
| 1 | `CONTRIBUTING.md` states **nothing** about the licence of inbound contributions | **blocking for open source** |
| 2 | 10 resources sitting at `must-verify` | non-blocking; open provenance debt |
| 3 | No `CODE_OF_CONDUCT.md` | conventional for public projects |
| 4 | No `CITATION.cff` | optional; useful given the research documents |

Gap 1 is the only one that must be fixed before relicensing. Without an
inbound=outbound statement, a future contribution's licence is
undetermined, and that is exactly the ambiguity this audit found absent
everywhere else.

`SECURITY.md` is present.

## 7. The decision, which is not mine to make

Nothing found here blocks Apache-2.0. That is a statement about
provenance, not a recommendation — the choice is strategic and
effectively irreversible, because code distributed under a permissive
licence cannot be recalled.

```text
KEEP SOURCE-AVAILABLE
+ commercial redistribution, resale and hosted resale stay reserved
+ Core's eventual commercial position stays open
- invisible to licence-filtered search; NOASSERTION in the sidebar
- many organisations will not adopt a non-OSI licence at all
- contributions from outsiders stay unlikely

APACHE-2.0
+ real adoption, citation and contribution become possible
+ explicit patent grant reassures corporate users -- the main reason
  to prefer it over MIT
+ matches the reviewers' "open governance" framing for Core
- resale and hosted resale become permitted, permanently
- one-way; a later source-available pivot only affects new versions

DUAL: v1 Apache-2.0, Core source-available
+ v1 earns adoption as the stable harness; Core keeps optionality
+ matches the stated division -- v1 proves the harness, Core
  industrialises the trust boundary
- two licences to explain, and the boundary must stay clean
```

The third option fits the sequencing decision in Core's ADR-005 most
closely, but it depends on a judgement about commercial intent that is
not recorded anywhere in the repository and should not be inferred.

## 8. Method

```bash
git log --format='%an <%ae>' | sort | uniq -c | sort -rn
gh api repos/SiddheshKGupta/Escapement --jq '.license.spdx_id'
grep -rniE "copyright \(c\)|copyright ©|SPDX-License-Identifier" .
ls -d vendor third_party node_modules externals
python - <<'PY'  # licence/adoption tallies over catalog/capability-registry.json
```

The registry tally should become a `doctor` check so licence drift is
caught per commit, in the same way `license_status` values already are.
