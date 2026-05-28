# Altmark Rent Delinquency Workflow Runbook

Created: 2026-05-27

## Workflow Purpose
Convert a cleaned Altmark rent delinquency report into an approval-gated exception/output queue with clear auditability, human review, and no unapproved tenant-facing action.

## Current Status
- Initial 50% payment received.
- Active phase: build/testing.
- Test gate: `../client-os/acceptance-checklist-rent-delinquency.md`.
- Earlier input-contract gate: `rent-delinquency-data-readiness-checklist.md`.

## Inputs
- Clean rent delinquency report/export.
- Tenant/entity identifier.
- Property/unit identifier.
- Current balance and overdue amount.
- Days past due or due date.
- Last payment date.
- Internal owner/manager.
- Contact method only if outreach/draft generation is in scope.
- Flags for payment plan, dispute, legal/eviction, recent payment, credits/prepayments, missing contact, and special handling.

## Processing Rules
1. Validate required fields before categorizing records.
2. Fail loudly or create a data-cleanup queue when required fields are missing.
3. Categorize records into included, manual-review, excluded, and cleanup states.
4. Keep legal/eviction-sensitive, disputed, payment-plan, recent-payment, credit/prepayment, and missing-contact records out of normal outreach.
5. Generate tenant-facing language only in draft/review mode and only if Altmark has approved that scope.
6. Log row counts, transformations, skipped reasons, flagged reasons, and errors.

## Outputs
- Review queue for true delinquency candidates.
- Manual-review queue for sensitive/ambiguous records.
- Data-cleanup queue for missing or malformed inputs.
- Optional outreach drafts, never auto-sent.
- Run log with timestamp, input source, row counts, exception counts, and approver state.

## Human-In-The-Loop Rules
- Altmark approves source report and exception rules before production use.
- Yair or named Altmark owner approves any tenant-facing outreach.
- JT does not automate financial/accounting actions.
- Records with legal, disputed, payment-plan, recent-payment, or credit/prepayment signals default to manual review.

## Acceptance Criteria
- Test cases in `../client-os/acceptance-checklist-rent-delinquency.md` pass on non-sensitive/redacted sample data.
- Output owner can interpret every included/skipped/flagged reason.
- Logs prove what ran and what changed.
- Production cutover starts in review-only mode.
- Open issues are recorded in `../client-os/failure-log.md` with owner/date.

## Rollback / Manual Fallback
- Keep the original source report/export unchanged.
- Preserve a pre-run copy before first live use.
- If validation fails, stop workflow output and return the data-cleanup queue to Altmark.
- If tenant-facing draft rules are disputed, disable draft generation and continue exception reporting only.

## Reusable Pattern
Rent delinquency automation is primarily an input-contract and exception-routing system. The reusable family-office/property-ops pattern is: validate ledger data, isolate sensitive exceptions, create a review queue, and require human approval before any external communication.

