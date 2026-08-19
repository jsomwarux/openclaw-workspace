# Acceptance Checklist — Marketsmith / Nexus SOW

Use this before calling any client deliverable "done." Acceptance must be proof-safe: verify delivery without exposing client-private data in reusable assets.

## Deliverable Boundary
- Deliverable: Nexus fixed-scope SOW covering all four signed deliverables.
- Client outcome it is meant to improve: faster, more repeatable Nexus dashboard and reporting delivery.
- In scope: all four SOW deliverables delivered, accepted, and independently re-verified by the client's technical lead on MSI systems as of 2026-08-17.
- Out of scope: net-new expansion work, new retainer, QA release-flow wiring, or additional agents beyond the signed SOW until MSI confirms priority and separately negotiates scope.
- Owner at client: technical lead for acceptance and walkthrough; budget owner only after technical lead routes scope conversation.
- JT owner: JT.

## Acceptance Criteria
| Criterion | Evidence Required | Owner | Status | Notes |
|---|---|---|---|---|
| Client can access/use the deliverable | Client confirmation | JT / Client | Accepted | Technical lead confirmed in writing to exec team on 2026-08-17 after independent re-verification on MSI systems |
| Primary workflow runs end-to-end | Client technical re-verification | JT / Client technical lead | Accepted | All four SOW deliverables accepted |
| Exceptions/failures are visible | Test/defect proof in private build record and anonymized case study | JT | Accepted | 11 real defects found in existing production code, confirmed and fixed; use only in case-study framing |
| Human approval gates are clear | Handoff / review boundary | JT / Client | Accepted for SOW | Follow-on scope stays with technical lead first; budget owner second |
| Rollback/support path is documented | Handoff note or accepted ownership | Client technical lead | Client-owned polish | Remaining polish items sit with client's technical lead |
| Open issues have owner/date | Client OS dashboard or issue list | Client technical lead | Accepted / client-owned | JT should not treat polish as open SOW work unless technical lead reopens it |
| Human-readable plan/review pack exists when acceptance requires judgment | Acceptance confirmation and case study | JT / Eve | Accepted | Proposal/content should point to anonymized case study instead of reconstructing |
| Demo/proof asset exists when the workflow can be shown | Private build record + anonymized case study | JT / Eve | Accepted | `ENGAGEMENT_BUILD_RECORD.md` never leaves JT's devices; `case-study-analytics-platform.md` is reusable in proposals |
| Payment/deposit status is clear | Invoice note | JT | Completion invoice sent | MSI-002 for $5,400 sent 2026-08-18, Net 15, due 2026-09-02; flag if unpaid 2026-09-03 |
| Privacy/redaction review completed | Permission gates recorded | JT / Eve | Complete | No client name publicly/client-facing until approved; internal hours-saved estimates blocked; 11-defects fact constrained to case-study framing |
| Handoff reviewed with client or internal owner | Client confirmation / walkthrough | JT / Client | Accepted; walkthrough follow-up open | Follow up on team walkthrough around 2026-08-25 |

## Proof-Safe Evidence Rules
- Redact names, addresses, account numbers, tenant/customer details, private financial values, tokens, and internal URLs before saving proof assets for reuse.
- Keep raw/private source files in `raw-inputs/` only; do not copy them into public case studies, posts, decks, or templates.
- Use synthetic or anonymized examples for reusable IP unless JT has explicit client permission.
- Never claim a metric until the source evidence exists and is linked here.
- No public or client-facing use of the client's name until they approve it.
- Client internal hours-saved estimates are blocked from proposals, posts, and pages until permission is granted; if ever used, attribute them as client estimates.
- The 11-defects fact is usable only in the case-study framing where it reads as the tool working. Never use it as commentary on their engineering.

## Handoff Notes
- Client-facing summary: all four SOW deliverables were delivered and accepted. Technical lead confirmed acceptance in writing to exec team on 2026-08-17 after independent re-verification on MSI systems.
- How to run / access: client-owned systems only; do not store private paths in reusable memory.
- How to pause / rollback: client technical lead owns remaining polish and release-flow decisions.
- Who to contact if it breaks: client technical lead first; JT responds only if pulled in through that lane.
- Next review date: team walkthrough follow-up around 2026-08-25; scope conversation routes through technical lead first, then budget owner.

## Weekly Escalation Rule
- If MSI-002 is unpaid on 2026-09-03, flag it as a cash follow-up.
- If the walkthrough produces a follow-on scope request, update this Client OS before any quote.
