# Failure Log — [Client]

Every miss becomes training data. Log failures the same day.

| Date | Workflow/Campaign | What Failed | Root Cause | Signal Missed | Fix | Reusable Pattern | Owner |
|---|---|---|---|---|---|---|---|
| 2026-05-06 | Rent Delinquency Outreach | Workflow cannot safely start yet because the delinquency report is not reliable. | Internal reporting and tenant ledgers need cleanup; Matt is away and the office is overwhelmed. | Data readiness was not yet explicit as an acceptance gate before automation. | Created `runbooks/rent-delinquency-data-readiness-checklist.md`; require cleaned sample export, edge-case flags, and deposit timing before build. | Property/family-office outreach automation must start with an input contract and exception routing, not generated messages. | JT / Altmark |
