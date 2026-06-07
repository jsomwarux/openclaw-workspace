# Altmark Rent Delinquency — Plan Review Pack

Created: 2026-06-06  
Reviewer: JT first, then Yair / Altmark output reviewer if JT wants to send a client-readable version.

## Objective
Move the rent delinquency workflow from a passed synthetic smoke test to a safe first Altmark sample review, without exposing live tenant data or allowing tenant-facing action before Altmark approves the rules.

## Current Understanding
- The workflow is for Altmark's local workflow environment.
- Synthetic testing passed on 2026-05-29: 8 rows processed into 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 unclassified.
- Sensitive rows did not generate tenant-facing drafts.
- The real report shape is still unknown.
- The next useful input is not more synthetic testing. It is a redacted Altmark source export with columns intact, plus reviewer/rule decisions.

## Scope
In scope:
- Intake a redacted sample delinquency export.
- Preserve the original source file unchanged.
- Validate required fields and column shape.
- Route rows into included, manual review, excluded, or cleanup queues.
- Record row counts, reasons, and approver state.
- Keep first Altmark run review-only.

Out of scope:
- Tenant-facing sends before explicit Altmark approval.
- Legal or eviction judgment.
- Accounting writebacks.
- Payment collection.
- Any automated financial action.

Assumptions:
- Altmark can provide a redacted export that keeps column headers and row structure.
- A named reviewer can approve or correct the output queue.
- Exception rules may vary from the synthetic assumptions and must be confirmed before cutover.

## Proposed Plan
1. JT asks Altmark for the redacted sample export, source report path/export process, refresh cadence, named output reviewer, and exception rules.
2. JT runs the first Altmark sample in review-only mode.
3. Eve/JT compare the output against the acceptance checklist and record any wrong routing, missing field, or ambiguous status.
4. If the redacted sample passes, schedule the first live run with the reviewer available.
5. Keep tenant-facing output in draft/review mode until Altmark explicitly approves production send scope.
6. Capture proof-safe evidence from synthetic/anonymized data only unless Altmark gives explicit permission.

## Review Points
Ask for judgment on these, not generic approval:
- Which Altmark report/export is the source of truth?
- Who is the output queue reviewer?
- What refresh cadence is realistic: daily, weekly, monthly, or manual?
- Which statuses must always route to manual review?
- Which statuses must always be excluded?
- What is good enough for the first review-only live sample?
- What must never create a tenant-facing draft?

## Acceptance Criteria
The workflow is not accepted until:
- A redacted Altmark sample runs end to end.
- Every included row has a clear inclusion reason.
- Every manual review, excluded, or cleanup row has a clear reason.
- Payment plan, dispute, legal/process-sensitive, recent payment, credit/prepayment, and missing-contact cases are safely gated.
- The output reviewer can understand the queue without asking JT to interpret it.
- The run log shows timestamp, row counts, queue counts, errors, and approver state.
- First production cutover has reviewer availability and rollback/manual fallback documented.

## Risks And Boundaries
- Privacy: do not store tenant names, phone numbers, emails, addresses, unit numbers, account numbers, balances, or legal notes in reusable proof assets.
- Legal/process risk: court, notice, prior demand, eviction, dispute, or post-report payment signals must not enter normal outreach.
- Data freshness risk: stale exports can create wrong action. Refresh cadence must be explicit.
- Approval risk: no tenant-facing message leaves review mode until Altmark approves scope.
- Proof boundary: public proof uses synthetic/anonymized examples only.

## Proof Assets
Available:
- `client-os/outputs/rent-delinquency-synthetic-smoke-test-log-2026-05-29.md`
- `client-os/outputs/rent-delinquency-synthetic-smoke-test-output-2026-05-29.csv`
- `client-os/acceptance-checklist-rent-delinquency.md`
- `proof-assets/redacted-sample-request-and-cutover-gate-2026-05-30.md`

Not available yet:
- Redacted Altmark source export.
- Altmark reviewer confirmation.
- Confirmed Altmark exception rules.
- First live-sample run log.

## Comment-Back Loop
Capture review comments in:
- `client-os/acceptance-checklist-rent-delinquency.md` for acceptance criteria or rule changes.
- `client-os/decision-log.md` for source report, reviewer, cadence, and cutover decisions.
- `client-os/failure-log.md` for any wrong routing or missing-field behavior.
- Mission Control task `Apply Plan Review Pack to Altmark rent delinquency gate` until this pack is reviewed and the next owner/date is set.

## Current Next Action
JT should either send the sample-request message from `proof-assets/redacted-sample-request-and-cutover-gate-2026-05-30.md` or confirm Altmark has already provided the five required inputs.
