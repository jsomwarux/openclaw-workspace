# Friday Rent Delinquency Smoke-Test Sheet — 2026-05-29

Purpose: give JT one clean Friday sequence to test the Altmark rent delinquency workflow without using live tenant data or creating tenant-facing risk.

## Highest-Leverage Friday Move
Run the synthetic rent delinquency fixture through the workflow, verify queue counts/reasons, then decide whether the workflow is ready for a redacted Altmark sample export.

Source files:
- `../client-os/cleaned-inputs/rent-delinquency-synthetic-smoke-test-2026-05-28.csv`
- `../client-os/cleaned-inputs/rent-delinquency-synthetic-smoke-test-2026-05-28.md`
- `../client-os/acceptance-checklist-rent-delinquency.md`
- `../runbooks/rent-delinquency-workflow.md`

## Test Sequence
1. Load the synthetic CSV into the rent delinquency workflow.
2. Run in dry-run/review-only mode.
3. Export or screenshot the output queues and run log.
4. Confirm every input row has exactly one classification: `included`, `manual_review`, `excluded`, or `cleanup`.
5. Confirm no tenant-facing draft is generated for manual-review, excluded, or cleanup rows.
6. Record any failed case in `../client-os/failure-log.md` with owner/date.

## Expected Result
| Queue | Expected Count | Case IDs |
|---|---:|---|
| Included | 1 | RD-001 |
| Manual review | 4 | RD-002, RD-003, RD-004, RD-005 |
| Excluded | 1 | RD-006 |
| Cleanup | 2 | RD-007, RD-008 |

The run log should show 8 input rows, 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 unclassified, and approval state still locked.

## Must-Pass Edge Cases
- RD-002 recent payment stays out of normal outreach until live balance is confirmed.
- RD-003 payment plan routes to manual review.
- RD-004 dispute routes to manual review.
- RD-005 legal/process-sensitive flag routes to manual review and cannot produce a normal tenant-facing draft.
- RD-006 credit/prepayment is excluded.
- RD-007 missing contact method goes to cleanup.
- RD-008 missing unit/property identifier goes to cleanup or fails loudly.

## Friday Decision Gate
After the dry run, choose one:

| Result | Next action |
|---|---|
| All counts/reasons pass | Ask Altmark for the redacted sample source export, named output reviewer, source report path, and refresh cadence. |
| Counts pass but reasons are unclear | Fix reason labels before live sample testing. |
| Any sensitive row enters normal outreach | Stop. Patch routing before any live sample. |
| Required fields can be silently skipped | Stop. Add fail-loud cleanup behavior before any live sample. |

## Message If Dry Run Passes
Use this only after the synthetic test passes:

> I ran the rent delinquency workflow against a synthetic test file first, including recent payment, payment plan, dispute, legal/process-sensitive, credit, missing contact, and missing required field cases. It is ready for a redacted Altmark sample export. To test against your real report safely, I need the source report path/export, the owner who will review the output queue, and the refresh cadence you expect for the report.

## Proof / Referral Guardrail
Do not use this as public proof. It is an internal delivery-control artifact. Public or referral proof still requires accepted client output, permission/anonymization, and proof-safe evidence.
