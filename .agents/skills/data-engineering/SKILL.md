---
name: data-engineering
description: Use for ingestion, ETL or ELT, data pipelines, mapping, cleansing, validation, reconciliation, lineage, warehousing, dimensional models, semantic layers, file or API ingestion, data-quality monitoring, SQL or reporting datasets. Do not use for a simple isolated query with no reusable data flow.
---

# Data Engineering

For each dataset define:

```text
Source | Owner | Extraction | Frequency | Schema | Validation
Transformation | Deduplication | Enrichment | Storage | Lineage
Reconciliation | Serving | Retention | Access | Monitoring | Failure handling
```

Procedure:

1. Confirm the source of truth and volume.
2. Define idempotent ingestion and schema handling.
3. Validate completeness, validity, uniqueness, consistency, timeliness,
   accuracy, referential integrity and reconciliation.
4. Record rejected rows rather than silently dropping them.
5. Separate masters, transactions, events, documents and reporting aggregates.
6. Make transformations and lineage traceable.
7. Define control totals, freshness and recovery.
8. Verify with representative and failure data.

Describe repeatable large-scale data work as a pipeline, not merely analysis.
