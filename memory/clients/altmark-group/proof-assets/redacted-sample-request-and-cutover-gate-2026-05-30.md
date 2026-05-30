# Altmark Rent Delinquency — Redacted Sample Request + Cutover Gate

Created: 2026-05-30

Purpose: convert the passed synthetic smoke test into the next Altmark client action without touching live tenant data or creating tenant-facing risk.

## Current State
- Synthetic dry run passed on 2026-05-29.
- Result: 8 rows processed; 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 unclassified.
- Safety result: no tenant-facing draft generated for manual-review, excluded, or cleanup rows.
- Evidence:
  - `client-os/outputs/rent-delinquency-synthetic-smoke-test-log-2026-05-29.md`
  - `client-os/outputs/rent-delinquency-synthetic-smoke-test-output-2026-05-29.csv`

## JT Send-Ready Message
Use this after confirming there is no newer Altmark reply already covering the same fields:

> I ran the rent delinquency workflow against a synthetic test file first, including recent payment, payment plan, dispute, legal/process-sensitive, credit/prepayment, missing contact, and missing required-field cases. The dry run passed: every row routed into the expected review, excluded, cleanup, or included queue, and nothing tenant-facing is generated without approval.
>
> To test against your real report safely, please send a redacted sample export with the columns intact. I also need:
>
> 1. the source report path/name or export process
> 2. the expected refresh cadence
> 3. the person who will review the output queue
> 4. any confirmed exception rules for payment plans, disputes, recent payments, legal/process-sensitive accounts, credits/prepayments, and missing contact info
>
> I’ll keep the first Altmark run in review-only mode until those are confirmed.

## Redacted Sample Requirements
Ask Altmark to preserve:
- Column headers.
- Row structure.
- Balance/aging/payment-date shape, with amounts optionally rounded or bucketed.
- Status flags for payment plan, dispute, legal/process-sensitive, recent payment, credit/prepayment, missing contact, and any special handling.

Ask Altmark to remove or replace:
- Tenant names.
- Phone numbers, emails, addresses, unit numbers, account numbers.
- Notes that reveal legal, personal, financial, or family details beyond the needed status flag.

## Client Input Gate
Live sample testing remains blocked until all are known:

| Required Input | Status | Notes |
|---|---|---|
| Redacted Altmark sample export with columns intact | Needed | Synthetic data is complete; real report shape still unknown. |
| Source report path/name or export process | Needed | Do not build around a one-off spreadsheet if a system export exists. |
| Refresh cadence | Needed | Daily, weekly, monthly, or manual determines scheduling and stale-data guardrails. |
| Named output reviewer | Needed | Owner must be able to approve included/manual-review/cleanup queues. |
| Exception rules | Needed | Payment plans, disputes, recent payments, legal/process-sensitive accounts, credits/prepayments, missing contact info. |

## First Live-Sample Test Rules
1. Use redacted sample only.
2. Run review-only mode.
3. Preserve source export unchanged.
4. Output queues: `included`, `manual_review`, `excluded`, `cleanup`.
5. No tenant-facing drafts unless Altmark explicitly approves draft generation scope.
6. Record row counts, skipped/flagged reasons, and approver state.
7. Any sensitive/legal/process row entering normal outreach is a stop condition.

## Acceptance / Cutover Gate
Rent delinquency is ready for first production cutover only when:
- redacted sample passes with clear reasons for every row
- output reviewer is named and understands the queue
- source report path and refresh cadence are confirmed
- exception rules are confirmed
- first live run is scheduled with reviewer available
- tenant-facing output remains draft/review-only
- rollback/manual fallback is documented

## Proof Boundary
This is internal delivery control. Do not use Altmark names, real tenant data, balances, legal status, or client-specific screenshots in public proof. Use only synthetic/anonymized proof unless Altmark later gives explicit permission.
