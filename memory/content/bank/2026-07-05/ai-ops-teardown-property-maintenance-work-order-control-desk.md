# AI Ops Teardown - Property Maintenance Work Order Control Desk

Recommended first platform: LinkedIn
Status: ready for JT review/post
Source teardown: `memory/consulting/ai-ops-teardowns/2026-07-05-property-maintenance-work-order-control-desk.md`
Current signal: Haven AI's June 25, 2026 post on action-taking property-management AI creating PMS work orders and assigning vendors.
Source URL: https://www.usehaven.ai/post/after-hours-answering-service-property-management
Build tier: Tier 2 now. Tier 3 gated until posted operator signal or explicit JT priority.

## LinkedIn Draft

A tenant call, a portal photo, and a vague "same issue again" email should not all become automatic work orders.

That is the control problem behind the latest property-management AI shift.

Haven AI described the 2026 version of action-taking as a service that can create a work order in the PMS, assign the vendor, pull unit and tenant data, and update the record as the issue progresses.

Useful, but that is also where the control layer matters.

A tenant calls after hours about a leak. Another sends a photo through the portal. A third emails "same issue again" with no unit detail. One request is routine. One is a duplicate. One needs manager approval before a vendor gets dispatched.

The PMS still needs a clean work order, the source attached, the right vendor route, the tenant update, and a record of who approved the edge case.

The workflow I would build starts with a maintenance work-order control desk.

It reads calls, emails, portal tickets, texts, photos, unit data, tenant history, vendor rules, and prior tickets.

It extracts the issue, unit, urgency, trade, missing detail, duplicate risk, and likely next step.

When the request is clean and low-risk, it drafts the PMS-ready work order.

When something is off, it routes the exception to a manager with the source attached and the stop reason visible.

AI should not make every maintenance decision.

It should make the routine path faster and make the risky path impossible to miss.

That is the first workflow I would audit for a property operator: maintenance intake to work-order control.

## X Draft

A tenant call, a portal photo, and a vague "same issue again" email should not all become automatic work orders.

That makes the approval layer more important, not less.

The workflow should know what can become a clean PMS draft and what has to stop for manager review.

## CTA Comment

If you run property operations and maintenance intake is still split across calls, email, portal tickets, texts, and manager approvals, I would start with a five-day Workflow Audit: map the first workflow, name the approval rules, and show what can safely become a draft.

## Posting Notes

- Public signal only. Haven AI is not a client.
- Do not claim this is deployed unless separately verified.
- If posted, save public URL to `memory/content/posted-log.jsonl`.
- Route property-operator replies to `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md` and the Workflow Audit call path.
