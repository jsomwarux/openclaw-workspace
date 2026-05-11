# AI Ops Teardown — Rent Delinquency Data Readiness

Source: `memory/consulting/ai-ops-teardowns/2026-05-10-rent-delinquency-data-readiness.md`

## Recommended First Post
Use after the insurance-expiration post. Stronger as LinkedIn because it shows implementation judgment and risk control.

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
