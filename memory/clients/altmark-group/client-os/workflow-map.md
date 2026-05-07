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
