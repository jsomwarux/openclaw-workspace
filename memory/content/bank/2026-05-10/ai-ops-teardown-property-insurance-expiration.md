# AI Ops Teardown — Property Insurance Expiration

Source: `memory/consulting/ai-ops-teardowns/2026-05-10-property-insurance-expiration.md`

## Recommended First Post
Use LinkedIn first. This is closest to Altmark/family-office buyer language and should build consulting credibility.

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

## CTA Comment / Reply
If your team still tracks expirations, renewals, COIs, owner reports, or approval-heavy follow-up through spreadsheets and inboxes, the first step is not buying another platform.

It is mapping the workflow and finding the first exception queue worth building.

Diagnostic one-pager: `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md`
