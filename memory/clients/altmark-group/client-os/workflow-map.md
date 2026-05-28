# Workflow Map — Altmark Rent Delinquency Outreach

## Current State
1. Altmark needs a reliable rent delinquency report before automation can begin.
2. Internal reporting and tenant ledgers need cleanup before the report is accurate.
3. Matt is away and the office is overwhelmed, so the blocker is operational/data readiness, not lack of interest.
4. JT should not automate tenant-facing outreach from an unreliable ledger/report.

## Roles / RACI
| Step | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Clean/source delinquency report | Matt / Altmark team | Yair | Karen / JT | JT |
| Confirm required fields + edge cases | JT | Yair | Matt / Karen | Navid if infrastructure affected |
| Review cleaned sample export | JT | Yair | Matt / Karen | Altmark ops |
| Build workflow after deposit | JT | Yair | Navid | Matt / Karen |
| Approve any tenant-facing outreach | Yair / Altmark owner | Yair | JT | Relevant property owner/manager |

## Systems Involved
- Altmark rent delinquency report / internal reporting export
- Tenant ledgers
- Dedicated workflow PC / local automation environment
- Future workflow output: exception list, approval queue, outreach draft/output if approved

## Edge Cases / Exceptions
- Payment plans
- Recently paid balances / report lag
- Disputed balances
- Partial payments
- Multiple units/entities for same tenant
- Legal/eviction-sensitive accounts
- Credits/prepayments creating false positives
- Missing contact information

## Target State
1. Altmark provides a cleaned delinquency report/source export.
2. Workflow validates required fields and routes exceptions to manual review.
3. JT/Altmark approve rules before any tenant-facing language is generated.
4. Human approval remains required before external outreach.
5. Logs/audit trail show what records were processed, skipped, flagged, or approved.

## Automation Boundary
- Manual judgement to preserve: legal/eviction-sensitive accounts, disputes, payment plans, special relationships, final external-send approval.
- Repeatable steps to automate: report intake, field validation, delinquency categorization, exception detection, owner assignment, draft generation/status output.
- Human approval gates: source report acceptance, edge-case rules, deposit/start approval, tenant-facing outreach send approval.


## 2026-05-26 Status Update
- Rent delinquency workflow is no longer paused: Altmark paid the initial 50%, and JT is actively building it.
- Current phase: testing preparation.
- Required testing artifacts: sample input report, validation rules, exception cases, skipped/flagged record reasons, human approval state, generated output/draft format, and production cutover checklist.
- Keep tenant-facing outreach human-approved. Legal/eviction-sensitive, disputed, payment-plan, recent-payment, and ledger-lag records must remain exception-gated.

## 2026-05-27 Testing Pack
- Acceptance checklist: `acceptance-checklist-rent-delinquency.md`.
- Runbook: `../runbooks/rent-delinquency-workflow.md`.
- Testing sequence: validate required fields, run edge-case rows, confirm included/skipped/flagged reasons, verify approval state, then document production cutover.
- Default proof boundary: synthetic/anonymized examples only until Altmark explicitly approves proof reuse.
