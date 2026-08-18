# Acceptance Checklist — Marketsmith / Nexus SOW

Use this before calling any client deliverable “done.” Acceptance must be proof-safe: verify delivery without exposing client-private data in reusable assets.

## Deliverable Boundary
- Deliverable: Nexus fixed-scope SOW covering dashboard/onboarding/agent support deliverables.
- Client outcome it is meant to improve: faster, more repeatable Nexus dashboard and reporting delivery.
- In scope: SOW deliverables JT reports finished as of 2026-08-17.
- Out of scope: net-new expansion work, new retainer, or additional agents beyond the signed SOW until Ed/Marketsmith confirms priority and scope.
- Owner at client: Ed / Sam / Marketsmith team, exact acceptance owner to confirm.
- JT owner: JT.

## Acceptance Criteria
| Criterion | Evidence Required | Owner | Status | Notes |
|---|---|---|---|---|
| Client can access/use the deliverable | Screenshot, demo note, or client confirmation | JT / Client | JT-reported finished; acceptance pending | Ask closed acceptance question against SOW section 10 / internal dev-test standard |
| Primary workflow runs end-to-end | Run log, sample output, or demo recording | JT | JT-reported finished; evidence pending | Confirm four deliverables meet acceptance criteria and both agents are packaged/in use |
| Exceptions/failures are visible | Error branch, exception list, or failure-log entry | JT | Pending | Capture any known open issues before expansion |
| Human approval gates are clear | Documented approval step before external/financial action | JT / Client | Pending | Needed for any future agent/automation lane |
| Rollback/support path is documented | Runbook section or handoff note | JT | Pending | Include in closeout note if needed |
| Open issues have owner/date | Client OS dashboard or issue list | JT / Client | Pending | Ask for open issues in closeout thread |
| Human-readable plan/review pack exists when acceptance requires judgment | `plan-review-pack.md`, Drive doc, Proof-style link, or explicit no-review-needed decision | JT / Eve | Not started | |
| Demo/proof asset exists when the workflow can be shown | MP4, GIF, screenshots, or explicit no-demo-needed decision | JT / Eve | Not started | |
| Payment/deposit status is clear | Internal note only; no sensitive finance detail in proof asset | JT | Kickoff paid; completion pending | Remaining $5,400 gated on completion/acceptance terms |
| Privacy/redaction review completed | Redacted proof folder note or explicit no-proof-needed decision | JT / Eve | Not started | |
| Handoff reviewed with client or internal owner | Handoff note, Loom/demo note, or client confirmation | JT / Client | Not started | |

## Proof-Safe Evidence Rules
- Redact names, addresses, account numbers, tenant/customer details, private financial values, tokens, and internal URLs before saving proof assets for reuse.
- Keep raw/private source files in `raw-inputs/` only; do not copy them into public case studies, posts, decks, or templates.
- Use synthetic or anonymized examples for reusable IP unless JT has explicit client permission.
- Never claim a metric until the source evidence exists and is linked here.

## Handoff Notes
- Client-facing summary: JT reports all SOW deliverables finished on 2026-08-17. Use an acceptance-only closeout note first; do not bundle future-work pitch into the acceptance request.
- How to run / access: TODO after client handoff evidence.
- How to pause / rollback: TODO if applicable to delivered agents/workflows.
- Who to contact if it breaks: JT during handoff/support window unless a Marketsmith owner is named.
- Next review date: propose 20-minute expansion conversation with Ed in a separate note after acceptance.

## Weekly Escalation Rule
- If any row remains unaccepted for more than one weekly update cycle, update the client dashboard with the blocker and create/update one MC task.
- The MC task must include first action, why it matters, and done state.
- Do not split one deliverable into multiple vague follow-up tasks.
