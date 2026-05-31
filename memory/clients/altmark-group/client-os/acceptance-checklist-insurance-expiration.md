# Acceptance Checklist — Altmark Insurance Expiration Workflow

## Deliverable Boundary
- Deliverable: insurance expiration tracking workflow on Altmark's local/dedicated workflow setup.
- Client outcome it is meant to improve: surface insurance expirations/exceptions before they become urgent coverage gaps.
- In scope: local workflow handoff, visible logs/audit trail, acceptance confirmation, open-issue list, support/rollback path.
- Out of scope: public proof claims, additional workflows, or rent delinquency build work before separate deposit/data-readiness gates are met.
- Owner at client: Yair / Navid.
- JT owner: JT.

## Acceptance Criteria
| Criterion | Evidence Required | Owner | Status | Notes |
|---|---|---|---|---|
| Dedicated PC/access path is confirmed | Handoff note or access confirmation | JT / Navid | In progress | Current MC task now points to `proof-assets/monday-closeout-sheet-2026-05-25.md` / weekend sheet: confirm access/admin owner before HTTPS/OAuth migration. |
| Workflow is demonstrated or verified | Screenshot/log/demo note | JT / Yair/Navid | Live in production per status notes; proof screenshot/log not captured | Keep proof private until redacted. |
| Logs/audit trail are visible | Redacted screenshot or run log reference | JT | Not confirmed in Eve memory | |
| Open issues have owner/date | Dashboard/failure-log entry | JT | Not confirmed in Eve memory | |
| Client accepts first workflow as live/useful | Yair/Navid confirmation | Yair/Navid | Working as expected per status notes; explicit proof wording still needed | Referral ask waits on proof evidence and permission boundary. |
| Payment/final approval status is clear | Internal note only | JT | Final 50% paid per 2026-05-30 status | Do not keep treating payment as the proof blocker. |
| Support/rollback path is documented | `runbooks/insurance-expiration-workflow.md` section verified | JT | Drafted | |

## Proof-Safe Evidence Rules
- Redact tenant/property/entity names, policy numbers, internal file paths, financial details, credentials, local network details, and private screenshots before any proof asset.
- Use a synthetic/anonymized screenshot for public-facing property/family-office offer materials unless client explicitly approves real proof.
- Do not claim quantified savings/risk reduction until first accepted workflow run has measured evidence.

## Handoff Notes
- Current runbook: `../runbooks/insurance-expiration-workflow.md`.
- Current PC handoff checklist: `../runbooks/pc-handoff-checklist.md`.
- Next review: after handoff/acceptance confirmation.
