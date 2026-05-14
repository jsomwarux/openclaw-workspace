# Automation Candidates — Altmark Group

| Candidate | Manual Trigger | Frequency | Pain | Inputs | Outputs | Edge Cases Known | Ready To Automate? | Notes |
|---|---|---:|---|---|---|---|---|---|

## Altmark Candidate Sequence — 2026-05-05
1. Insurance expiration tracking — finished; acceptance pending. Productize only after acceptance evidence exists, using synthetic/anonymized data.
2. Rent delinquency outreach — next paid workflow; blocked until clean source report, exception rules, and 50% deposit timing.
3. Loan management — later buildout candidate; needs source-of-truth and approval/rollback boundaries.
4. WhatsApp AI bot — later/high-complexity candidate; requires clear human-in-loop, escalation, opt-out, and audit rules.
5. Flagstar to QuickBooks automation — later candidate; financial workflow requires audit trail, rollback, and human approval before posting.
6. Cash management & overdraft prevention — later candidate; high sensitivity, strict human approval.

## Reusable IP Candidates
| Candidate | Source | Productized Asset | Privacy Boundary | Status |
|---|---|---|---|---|
| Insurance expiration exception layer | Finished Altmark workflow | n8n template with sample CSV, dry-run, approval queue, audit log, error branch | Synthetic policy/entity data only | MC task exists |
| Rent delinquency data-readiness gate | Client-side ledger/reporting blocker | Input contract + exception-routing checklist | No real tenant names, balances, legal flags, or contact details | Checklist exists |

