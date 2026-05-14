# Acceptance Checklist — [Client / Deliverable]

Use this before calling any client deliverable “done.” Acceptance must be proof-safe: verify delivery without exposing client-private data in reusable assets.

## Deliverable Boundary
- Deliverable:
- Client outcome it is meant to improve:
- In scope:
- Out of scope:
- Owner at client:
- JT owner:

## Acceptance Criteria
| Criterion | Evidence Required | Owner | Status | Notes |
|---|---|---|---|---|
| Client can access/use the deliverable | Screenshot, demo note, or client confirmation | JT / Client | Not started | |
| Primary workflow runs end-to-end | Run log, sample output, or demo recording | JT | Not started | |
| Exceptions/failures are visible | Error branch, exception list, or failure-log entry | JT | Not started | |
| Human approval gates are clear | Documented approval step before external/financial action | JT / Client | Not started | |
| Rollback/support path is documented | Runbook section or handoff note | JT | Not started | |
| Open issues have owner/date | Client OS dashboard or issue list | JT / Client | Not started | |
| Payment/deposit status is clear | Internal note only; no sensitive finance detail in proof asset | JT | Not started | |
| Privacy/redaction review completed | Redacted proof folder note or explicit no-proof-needed decision | JT / Eve | Not started | |
| Handoff reviewed with client or internal owner | Handoff note, Loom/demo note, or client confirmation | JT / Client | Not started | |

## Proof-Safe Evidence Rules
- Redact names, addresses, account numbers, tenant/customer details, private financial values, tokens, and internal URLs before saving proof assets for reuse.
- Keep raw/private source files in `raw-inputs/` only; do not copy them into public case studies, posts, decks, or templates.
- Use synthetic or anonymized examples for reusable IP unless JT has explicit client permission.
- Never claim a metric until the source evidence exists and is linked here.

## Handoff Notes
- Client-facing summary:
- How to run / access:
- How to pause / rollback:
- Who to contact if it breaks:
- Next review date:

## Weekly Escalation Rule
- If any row remains unaccepted for more than one weekly update cycle, update the client dashboard with the blocker and create/update one MC task.
- The MC task must include first action, why it matters, and done state.
- Do not split one deliverable into multiple vague follow-up tasks.
