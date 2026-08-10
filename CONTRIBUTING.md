# Contributing

Escapement favours a small enforceable core.

Before proposing a change:

1. show a repeated failure or measurable need;
2. identify the smallest correct layer;
3. add or update an executable evaluation;
4. preserve project-owned state and safe update boundaries;
5. update documentation and release notes;
6. run:

```bash
python scripts/escapement.py self-test
python scripts/escapement.py security --fail-on high
```

External resources require licence verification and attribution.

## Licence of contributions

Escapement is licensed under the [Apache License 2.0](LICENSE).

**Inbound = outbound.** By submitting a contribution you agree that it is
licensed under Apache-2.0, on the terms in §5 of that licence, and you
confirm you have the right to license it that way.

No CLA is required and no copyright assignment is requested — you keep
copyright in what you write.

Do not paste third-party code into a contribution unless its licence
permits redistribution under Apache-2.0, and say so in the PR if you do.
GPL and AGPL material cannot be incorporated. Referencing an external
project in the capability registry is a routing decision and is not
incorporation; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for
the record required when material is actually used.
