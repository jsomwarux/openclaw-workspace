# AI Ops Teardown — Rent Delinquency Data Readiness + Outreach Queue

Date: 2026-05-10
Tier: 2 now; Tier 3 only after clean sample data exists
Score: 28/30

## Business Context
Rent delinquency automation sounds simple until the source data is messy.

If the ledger/report is wrong, AI does not make the process faster. It makes the wrong process louder.

## Current Manual Process
- Pull delinquency report from property/accounting system.
- Manually review balances, tenant names, units, payment status, and notes.
- Clean edge cases in spreadsheets or by staff memory.
- Draft outreach manually.
- Managers chase status through messages and inboxes.

## Failure Modes
- Tenant ledger is stale or inconsistent.
- Report excludes important notes or payment plans.
- Outreach goes to the wrong person or says the wrong amount.
- Staff hesitate because they do not trust the report.
- There is no clean “ready for outreach / blocked / needs review” queue.

## Proposed AI Ops Workflow
| Step | Input | System action | Human boundary | Output |
|---|---|---|---|---|
| 1 | Delinquency export | Validate required fields | Stop if schema/data quality fails | Data readiness report |
| 2 | Ledger/report rows | Flag missing fields, stale balances, duplicate tenants, payment-plan notes | Human confirms edge cases | Clean exception queue |
| 3 | Approved queue | Draft outreach from approved templates | Human approves before send | Ready-to-send emails/SMS |
| 4 | Cooldown rules | Prevent duplicate/frequent outreach | Human can override | Safer cadence |
| 5 | Summary | Group ready/blocked/sent/needs review | Manager reviews | Daily delinquency ops report |
| 6 | Audit log | Log amount, draft, approver, sent status | None | Compliance trail |

## n8n Node Sketch
1. Manual/Cron trigger after clean export is dropped.
2. Read CSV/XLSX export.
3. Validate required fields: tenant, unit, property, amount, days late, contact, last payment, notes.
4. Code node calculates data-quality score and blocks unsafe rows.
5. LLM node summarizes edge-case notes only after validation passes.
6. Rules node assigns row status: ready, missing data, payment-plan review, stale ledger, duplicate.
7. LLM node drafts outreach only for ready rows.
8. Approval queue for manager.
9. Send branch only after approval.
10. Audit log + daily summary.

## Why This Is Reusable
This pattern applies to any sensitive outreach workflow where bad data creates operational/legal/customer risk.

## X Draft
never automate tenant outreach from a dirty ledger.

The first workflow is not “AI writes the email.”

It is:
1. validate the report
2. flag bad rows
3. separate ready vs blocked
4. draft only from clean data
5. require human approval
6. log every action

AI should make risky work safer before it makes it faster.

## LinkedIn Draft
Rent delinquency automation sounds obvious until the source data is messy.

If I were building AI ops for a property management team, I would not start by letting AI send tenant messages.

I would start with data readiness.

The current process usually breaks before the message is written:
- the delinquency report is stale
- tenant ledgers need cleanup
- payment plans live in notes or staff memory
- balances need review
- managers do not fully trust the export

The workflow I would build first:
1. ingest the delinquency report
2. validate required fields
3. flag missing, stale, duplicate, or edge-case rows
4. separate “ready for outreach” from “needs review”
5. draft messages only for clean rows
6. require human approval before anything is sent
7. log amount, draft, approver, and status

The goal is not autonomous collections.

The goal is a safer exception queue: what is ready, what is blocked, who owns it, and what needs approval.

AI should make risky work safer before it makes it faster.
