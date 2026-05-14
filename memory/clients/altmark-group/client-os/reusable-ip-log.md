# Reusable IP Log — Altmark Group

| Date | Source Workflow | Reusable Pattern | What To Productize | Privacy Boundary | Next Asset | Owner | Status |
|---|---|---|---|---|---|---|---|
| 2026-05-13 | Insurance expiration tracking | Property/family-office back offices need local-first exception tracking with audit trail and human approval. | Reusable insurance expiration exception layer / n8n template with sample CSV, dry-run, approval queue, audit log, error branch. | No real tenant/entity/policy/network details; use synthetic sample data. | Existing MC task: Build reusable n8n template: insurance expiration exception layer. | Eve / JT | Candidate |
| 2026-05-13 | Rent delinquency pause | Tenant outreach automation should start with a clean input contract and exception routing, not message generation. | Rent delinquency data-readiness checklist + approval-gated outreach workflow template. | No real tenant ledgers, balances, legal status, or contact details in reusable assets. | Use existing `runbooks/rent-delinquency-data-readiness-checklist.md` as seed. | Eve / JT | Candidate |
