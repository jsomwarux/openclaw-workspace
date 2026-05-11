# AI Ops Teardown — Property Management Insurance Expiration Exception Layer

Date: 2026-05-10
Tier: 3 candidate
Score: 29/30

## Business Context
Property managers and family offices track insurance documents, COIs, vendor coverage, tenant requirements, and expirations across spreadsheets, inboxes, PDFs, portals, and staff memory.

The risk is not “no one knows what insurance is.”

The risk is that something expires quietly and no one sees it until a lender, owner, tenant, vendor, or internal stakeholder asks.

## Current Manual Process
- Someone maintains a spreadsheet or report.
- PDFs/emails arrive in inboxes.
- Expiration dates are checked manually or irregularly.
- Follow-ups are written from scratch.
- Owners/managers only see the issue after it is late.

## Failure Modes
- Expiring docs are missed.
- Follow-up timing depends on one person remembering.
- No clean audit trail exists.
- Managers see too much noise and not enough exceptions.
- The team cannot tell what is current, overdue, or waiting on someone else.

## Proposed AI Ops Workflow
| Step | Input | System action | Human boundary | Output |
|---|---|---|---|---|
| 1 | Spreadsheet/report export | Normalize entity, document type, expiration date, contact | None | Clean working table |
| 2 | Email/PDF folder | Extract doc dates and names where safe | Low-confidence extraction flagged | Candidate updates |
| 3 | Rules engine | Flag expiring in 30/14/7/0 days | Human can override | Exception queue |
| 4 | LLM draft | Draft follow-up email/SMS from approved template | Human approves before send | Ready-to-send message |
| 5 | Daily summary | Group by urgent/blocked/waiting | Manager reviews | Daily exception digest |
| 6 | Audit log | Log status, draft, approver, timestamp | None | Compliance/proof trail |

## n8n Node Sketch
1. Cron trigger: daily 8 AM.
2. Read spreadsheet/export from local folder or Google Drive.
3. Normalize rows with code node.
4. Optional PDF/email extraction node for newly received docs.
5. Rules node: expiration windows and missing required fields.
6. LLM node: generate follow-up draft only from approved template.
7. Approval queue: Airtable/Sheet/HTML dashboard/manual review.
8. Telegram/email daily summary to manager.
9. Append audit log to SQLite/CSV.
10. Error branch: notify operator when source file missing, malformed, or row count changes unexpectedly.

## Why This Is Reusable
This generalizes across:
- vendor COIs
- tenant insurance
- property documents
- lender reporting
- permit/license renewals
- family-office compliance checklists

## X Draft
property managers do not need another chatbot.

the first AI workflow I would build is an insurance expiration exception layer.

Inputs:
- COIs
- tenant/vendor records
- expiration dates
- inbox attachments

Flow:
1. scan the source file
2. flag what expires soon
3. draft the follow-up
4. manager approves
5. every action gets logged

AI is most useful when it shows what is about to break.

## LinkedIn Draft
Most AI implementations start in the wrong place.

If I were building AI ops for a property management team, I would not start with a chatbot.

I would start with insurance expirations.

The current process usually looks something like this:
- a spreadsheet tracks policies or COIs
- PDFs sit in inboxes or folders
- someone manually checks dates
- follow-ups depend on memory
- managers only see the issue when it is already late

The workflow I would build:
1. ingest the source spreadsheet or report
2. normalize property, tenant/vendor, document type, and expiration date
3. flag anything expiring in 30/14/7 days
4. draft the follow-up from an approved template
5. route the risky part to a human for approval
6. log every status change, draft, approver, and timestamp

The important part is not that AI writes an email.

The important part is that the business knows what is expiring, who owns it, what is blocked, and what needs approval.

That is where AI implementation actually starts.
