---
name: data-architecture
description: Use when a project needs persistent storage and no database technology has been chosen yet, or an existing choice is being reconsidered. Selects a database with stated trade-offs, then designs the schema and API surface together against that choice. Do not use for read-only analytics over an existing store -- see data-engineering.
---

# Data Architecture

Database choice, schema, and API are one decision, not three sequential
ones. A schema designed before the database is chosen gets redesigned once
it is; an API designed before the schema exists gets reshaped once it does.
Decide together, in this order, and record the decision durably.

## 1. Assess actual needs, not defaults

Before naming a technology, establish:

```text
Data shape       | relational, document, key-value, graph, time-series, blob
Consistency need | strict (ACID, cross-record invariants) or eventual is fine
Query pattern     | point lookups, joins/relations, full-text, analytical scans
Write volume      | single-writer toy, moderate, high-throughput
Concurrency       | single process, multi-process, distributed
Operational reality | embedded/serverless, self-hosted, managed service, existing infra
```

Read `DOMAIN_CONTEXT.md` and `PROJECT_CONTEXT.md` first -- do not assume
scale or consistency requirements the project has not stated.

## 2. Compare, then choose -- and ask

Compare at least two materially different options against the assessed
needs (not a coin flip between near-identical choices): e.g. embedded
SQL (SQLite) vs. a managed relational database (PostgreSQL) vs. a document
store (MongoDB) vs. no persistence yet (in-memory, for a genuine
throwaway prototype). State why the recommended one fits and what the
others would cost.

**This is a schema-level decision under `AGENTS.md`'s approval gates.**
Present the comparison and the recommended default to the user per
`decision-coach`'s rule: state it, wait for a real answer when a user is
present, do not silently pick and proceed. A wrong database choice is
expensive to reverse once real data and real code depend on it --
exactly the kind of decision that should not be made without them.

## 3. Design the schema against the chosen technology's real model

Not a generic ORM-agnostic sketch. If relational: tables, keys, foreign
keys, indexes, normalisation level, migration strategy. If document: 
collections, embedding vs. referencing, index strategy. Define for every
entity:

```text
Entity | Fields | Key | Relationships | Indexes | Constraints
Retention | Migration/versioning strategy | Owner
```

## 4. Design the API surface against the schema, not before it

Endpoints and request/response shapes should reflect what the schema can
actually answer efficiently -- do not design an API that implies a query
the schema cannot serve without a full scan, without deciding that
trade-off explicitly. Hand off to `api-integration` for the external
contract details (auth, retries, idempotency) once the shape is settled
here.

## 5. Record the decision

Persist the choice, the rejected alternatives, and why -- in the
project's decision log or spec, not only in chat. A later session must be
able to see this was a considered choice, not an assumption.

Do not introduce a new database technology as a silent default when the
project already has one established; that is a material architecture
change requiring the same approval gate as adopting one for the first
time.
