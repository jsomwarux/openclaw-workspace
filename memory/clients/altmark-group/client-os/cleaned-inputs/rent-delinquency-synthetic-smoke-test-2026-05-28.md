# Rent Delinquency Synthetic Smoke Test

Created: 2026-05-28

CSV fixture: `rent-delinquency-synthetic-smoke-test-2026-05-28.csv`

## Purpose
Give JT a non-sensitive first-pass fixture for the Altmark rent delinquency workflow before a clean client export is available.

## Expected Queue Counts
| Queue | Expected Count | Case IDs |
|---|---:|---|
| included | 1 | RD-001 |
| manual_review | 4 | RD-002, RD-003, RD-004, RD-005 |
| excluded | 1 | RD-006 |
| cleanup | 2 | RD-007, RD-008 |

## Pass Criteria
- Workflow preserves source rows and emits exactly one classification per row.
- Included queue contains only RD-001.
- Manual-review queue includes recent payment, payment plan, dispute, and legal-sensitive cases.
- Excluded queue contains the credit/prepayment case.
- Cleanup queue contains missing-contact and missing-required-field cases.
- Run log records 8 input rows, 1 included, 4 manual review, 1 excluded, 2 cleanup, and 0 unclassified rows.
- No tenant-facing draft is generated unless the row is approved after manual review.

## Notes For Live Testing
- This fixture is synthetic and safe to keep in reusable proof/client-ops notes.
- Replace synthetic names and balances with a redacted client export only after Altmark confirms the source report and exception flags.
- If the workflow cannot represent one of these queues, update the workflow before running live data.
