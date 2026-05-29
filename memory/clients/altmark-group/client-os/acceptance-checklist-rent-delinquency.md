# Acceptance Checklist — Altmark Rent Delinquency Workflow

Created: 2026-05-27

## Deliverable Boundary
- Deliverable: approval-gated rent delinquency workflow for Altmark's local workflow environment.
- Client outcome it is meant to improve: turn a cleaned delinquency report into a reviewed exception/output queue without relying on manual scanning.
- In scope: report intake, required-field validation, exception classification, skipped/flagged record reasons, human approval state, draft/output generation if approved, run log, and production cutover checklist.
- Out of scope: tenant-facing sends without Altmark approval, legal/eviction judgement, accounting writebacks, payment collection, or any automated financial action.
- Client owner: Yair / Matt / Karen, to be confirmed from current testing path.
- JT owner: JT.

## Required Test Inputs
| Input | Evidence Required | Owner | Status | Notes |
|---|---|---|---|---|
| Clean sample delinquency report | Redacted/sample export with columns intact | Altmark | Synthetic smoke test ready | Use `cleaned-inputs/rent-delinquency-synthetic-smoke-test-2026-05-28.csv` for pre-client testing; still need Altmark source export before live acceptance. |
| Source of truth | Named report/system/export path | Altmark | Needed | Do not rely on a one-off spreadsheet if a system report exists. |
| Required fields present | Tenant/entity, property/unit, balance, overdue amount, days/due date, last payment, owner, contact method if outreach is in scope | JT / Altmark | Needed | Missing fields should route to data cleanup, not silent failure. |
| Exception rules | Payment plans, disputes, legal/eviction, recent payments, credits/prepayments, missing contact info | Yair / Altmark | Needed | Sensitive accounts default to manual review. |
| Legal/process status | Prior rent demand, active case, notice/court status, or approved exclusion marker if Altmark tracks it | Altmark | Needed before tenant-facing drafts | Use only as internal review context. Do not infer legal status from balance alone. |
| Output owner | Person who reviews exceptions/output | Yair / Altmark | Needed | Must be named before production run. |

## Test Cases
| Case | Expected Result | Required Evidence | Status |
|---|---|---|---|
| Standard delinquent balance | Included in output with balance, age, owner, and next-step status | Screenshot/export row or redacted sample row | Synthetic row RD-001 ready |
| Recently paid but report still shows due | Flagged or excluded based on payment-recency cutoff | Test row + cutoff rule | Synthetic row RD-002 ready |
| Payment plan active | Routed to manual review, not normal outreach | Test row + flag rule | Synthetic row RD-003 ready |
| Disputed balance | Routed to manual review or excluded | Test row + dispute flag | Synthetic row RD-004 ready |
| Legal/eviction-sensitive account | Excluded unless Yair explicitly approves handling | Test row + approval rule | Synthetic row RD-005 ready |
| Prior demand/case/notice status present | Routed to manual review with `legal_process_sensitive`; no tenant-facing draft | Test row + legal/process flag | Research gate added 2026-05-28 |
| Payment after report date | Routed to manual review or excluded until live balance is confirmed | Test row + payment-after-report date | Research gate added 2026-05-28 |
| Credit/prepayment/negative balance | Excluded from delinquency output | Test row + balance-sign rule | Synthetic row RD-006 ready |
| Partial payment | Categorized by agreed threshold/age rule | Test row + threshold | Not tested |
| Multiple units/entity grouping | Grouped or separated per Altmark rule | Test rows + grouping decision | Not tested |
| Missing contact method | Included in cleanup queue, not outreach-ready queue | Test row + cleanup output | Synthetic row RD-007 ready |
| Missing required field | Workflow fails loudly or routes to data cleanup | Run log/error output | Synthetic row RD-008 ready |

## Acceptance Criteria
The workflow is accepted only when all are true:

- [ ] Sample input runs end to end on non-sensitive/redacted test data.
- [ ] Every included record has a clear reason it is included.
- [ ] Every skipped or flagged record has a clear skipped/flagged reason.
- [ ] Payment-plan, disputed, legal/eviction, recent-payment, and credit/prepayment edge cases are exception-gated.
- [ ] Prior rent demand, court/case, notice, or post-report payment signals cannot enter normal outreach.
- [ ] Human approval is required before any tenant-facing message leaves Altmark.
- [ ] Output owner can review the queue without asking JT how to interpret it.
- [ ] Run log shows input timestamp, row count, processed count, included count, skipped count, flagged count, errors, and approver state.
- [ ] Production cutover path is documented before the first live run.

## Production Cutover Checklist
- [ ] Current source report and refresh cadence confirmed.
- [ ] Backup/export copy saved before first live run.
- [ ] Non-sensitive smoke test completed on the dedicated workflow PC.
- [ ] First live run scheduled with Altmark reviewer available.
- [ ] Tenant-facing output starts in draft/review mode only.
- [ ] Rollback/manual fallback documented.
- [ ] Open issues recorded with owner/date in `failure-log.md`.
- [ ] Final acceptance wording captured after first reviewed production run.

## Proof-Safe Evidence Rules
- Do not store real tenant names, balances, unit numbers, contact info, legal status, or ledger notes in reusable proof assets.
- Use synthetic examples for public proof and referral materials unless Altmark explicitly approves a named/anonymized case study.
- Proof claim default: "approval-gated delinquency exception workflow for property operations" until measured results exist.
- Official-process context check: `../../../research/altmark-rent-delinquency-nonpayment-risk-check-2026-05-28.md`.
