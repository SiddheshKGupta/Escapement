# KPI Catalogue

| KPI | Meaning | Formula | Unit | Period | Source | Freshness | Drill-down | Reconciliation |
|---|---|---|---|---|---|---|---|---|
| Active Employers | Employers with an active contract | Count distinct active employer IDs | Count | As of date | Contract master | Daily | Employer list | Count equals active records |
| Monthly Order Value | Approved order value in selected month | Sum approved order amount | INR | Month | Order ledger | Daily | Order list | Sum equals filtered ledger |
| Claim Recovery Rate | Amount collected divided by approved claim amount | Collected / Approved | % | FY/Q/Month | Claim and collection ledgers | Daily | Claim ageing | Numerator and denominator traceable |
