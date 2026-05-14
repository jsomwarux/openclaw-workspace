# Acceptance Checklist — Aya StreetEasy Scraper

## Deliverable Boundary
- Deliverable: StreetEasy scraper/reporting support.
- Client outcome it is meant to improve: faster property/opportunity monitoring with less manual checking.
- In scope: source query/input definition, scrape/run method, output format, exception handling, handoff/support notes.
- Out of scope: unapproved scraping expansion, external publishing, or claims about results not verified by Aya.
- Owner at client: Aya contact TBD.
- JT owner: JT.

## Acceptance Criteria
| Criterion | Evidence Required | Owner | Status | Notes |
|---|---|---|---|---|
| Source/query inputs are defined | Input contract or example query saved in `cleaned-inputs/` | JT / Aya | Not started | Do not store sensitive client strategy in reusable templates. |
| Scraper runs end-to-end | Run log or sample output saved privately | JT | Not started | Redact addresses/private notes before proof reuse. |
| Output format is usable by Aya | Client confirmation or accepted sample output | Aya / JT | Not started | |
| Failure modes are documented | Failure-log entry for blocked/changed pages, captchas, missing fields, stale results | JT | Not started | |
| Support/rollback path exists | Runbook or dashboard note explaining rerun/pause/escalation | JT | Not started | |
| Payment/approval status is clear | Internal note in status/dashboard | JT | Not started | |

## Proof-Safe Evidence Rules
- Redact addresses, deal notes, owner names, financial assumptions, and any search strategy before public reuse.
- Only publish a case-study/proof claim after Aya confirms the output is useful or a concrete operational metric exists.

## Handoff Notes
- How to run/access: TBD.
- How to pause/rollback: TBD.
- Open issues: TBD.
- Next review date: TBD.
