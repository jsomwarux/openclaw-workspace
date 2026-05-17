# Saturday Prep Pack — Property / Family-Office AI Ops Teardown

Created: 2026-05-16 nightly autonomous leverage run  
Purpose: give JT one clean, proof-safe asset to post tomorrow without digging through the packet files.

## Strategic Use

Use this only if Altmark has no new PC handoff / acceptance / payment update to act on first.

Primary objective: create a warm, proof-led inbound surface for property/family-office diagnostic conversations while Yair referral asks remain gated by acceptance/payment clarity.

## Post Window

Best windows: Sunday 8–10 AM ET or 6–9 PM ET. If Sunday is missed, use Monday 8–10 AM ET.

## LinkedIn Post

Most AI implementations start in the wrong place.

If I were building AI ops for a property management or family-office team, I would not start with a chatbot.

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

## CTA Comment

If your team still tracks expirations, renewals, COIs, owner reports, or approval-heavy follow-up through spreadsheets and inboxes, the first step is not buying another platform.

It is mapping the workflow and finding the first exception queue worth building.

Diagnostic scope: https://docs.google.com/document/d/1B16BgQ-gd8KEkPV53zbDC6dg0J2PVqMmHxJWIsL2src/edit

## Reply If Someone Asks What This Looks Like

The simplest version is a short diagnostic first.

I map the workflow, source reports, approval points, failure modes, and data readiness. Then I recommend the first build only if there is a clean workflow worth automating.

For property/family-office teams, the best first workflows are usually insurance/COI expiration tracking, rent delinquency readiness, owner/vendor exception reporting, or QuickBooks/AppFolio export review.

One-pager: https://docs.google.com/document/d/1B16BgQ-gd8KEkPV53zbDC6dg0J2PVqMmHxJWIsL2src/edit

## Proof-Safety Check

Allowed:
- property/family-office teams
- insurance/COI/vendor-document expiration tracking
- spreadsheets, inboxes, local files, AppFolio/QuickBooks-style exports
- human approval
- audit trail
- anonymized workflow example
- "workflow I would build" / "example first system" language

Avoid:
- naming Altmark, Yair, Navid, Matt, or Aya
- saying the system is live for a named client
- claiming ROI, hours saved, records tracked, or reduced misses
- saying rent delinquency automation is live
- implying autonomous tenant/vendor/financial action

## After Posting

1. Save the posted URL to `memory/content/posted-log.jsonl`.
2. If there is a reply/DM, log company/contact/workflow in `memory/consulting/warm-lead-command-center.md`.
3. Route interested replies to the diagnostic one-pager, not a generic AI call.
