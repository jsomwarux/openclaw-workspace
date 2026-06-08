# PM Front Desk + Exception Desk Proof Spine

Status: Drafted 2026-06-07 for Tuesday property-management distribution and warm/reply-led consulting use.

Use this as the buyer-facing proof spine behind property-management posts, reply prompts, and diagnostic conversations. It is anchored to Altmark-style property-ops implementation patterns, but it does not claim unapproved client details or private metrics.

## Buyer Problem

A property-management team can have the right software and still lose work across the handoff.

Common surfaces:
- Resident or tenant emails
- Missed calls and voicemail transcripts
- Maintenance requests
- Vendor updates
- Owner approval messages
- Rent delinquency or lease-follow-up reports
- Staff notes and spreadsheets

The problem is not one inbox. The problem is that every intake item needs context, ownership, approval rules, and an exception path before it can safely move.

## Workflow Shape

### Front Desk

The front desk captures the incoming work and prepares the clean path.

It should:
- Classify the request or follow-up type
- Pull tenant, unit, vendor, owner, or lease context when available
- Identify urgency and aging
- Draft a next step when the source data is clean
- Log what was received and where the item landed
- Route routine work to the right queue or person

### Exception Desk

The exception desk governs the work the AI should not complete on its own.

It should flag:
- Missing source-of-truth data
- Sensitive tenant issues
- Legal-adjacent language
- Owner approval requirements
- Expensive or ambiguous vendor actions
- Duplicate tenant, unit, vendor, or owner records
- Payment or lease mismatches
- Stale status with no safe next step

The rule is simple: if the workflow cannot identify the source of truth, the owner, the allowed action, and the place the result should land, it creates a review item instead of improvising.

## Proof Boundary

Safe public proof:
- The workflow pattern
- The intake surfaces
- The approval and exception logic
- The local-first / human-review implementation stance
- Redacted examples of queues, checklists, and readiness criteria
- General property-ops categories: rent delinquency, maintenance, missed calls, owner approvals, lease follow-up

Do not publish without permission:
- Client name unless already public and approved for the exact claim
- Tenant data
- Financial/accounting records
- Private owner communications
- Legal-sensitive examples
- Unapproved before/after metrics

## Readiness Checklist Linkage

Use this proof spine with:

`memory/content/assets/property-management-ai-workflow-readiness-checklist.md`

That checklist answers the buyer question after the post lands: "Is my workflow ready for this, or would it break on the first exception?"

## Diagnostic Conversation Path

For a property-management operator, ask for one workflow only:
- Maintenance intake
- Missed-call follow-up
- Rent delinquency review
- Owner approvals
- Lease renewal follow-up
- Monthly owner reporting

Then pressure-test five fields:
- Intake source
- System of record
- Approval owner
- Exception types
- Review queue / output destination

If those five are clear, the workflow can usually be scoped. If they are not, the first paid step is a diagnostic/readiness cleanup, not a build.

## Reply Prompt

Short reply:

> The useful first pass is not "can AI answer tenants?" It is whether the intake source, system of record, approval owner, exception path, and review queue are clear enough to trust. I have a checklist for that if helpful.

Longer reply:

> I would start smaller than a chatbot. Pick one workflow: maintenance intake, missed calls, rent follow-up, owner approvals, or lease renewal. Then check whether the intake source, system of record, approval owner, exception path, and review queue are clear. If those are not clear, AI just moves the mess faster. If they are clear, the first workflow is usually straightforward to scope.

## Tuesday LinkedIn Spine

Use the post draft in:

`memory/content/bank/2026-06-08/pm-front-desk-exception-desk-linkedin.md`

Asset CTA:

> I can send the readiness checklist I use to pressure-test whether one of these workflows is safe to build.

## Warm Outreach Use

Use after a relevant conversation or reply, not as cold generic blast copy.

Best-fit buyer language:
- "We miss tenant/vendor follow-ups"
- "Maintenance requests fall through the cracks"
- "We need better owner visibility"
- "Our team lives in inboxes and spreadsheets"
- "We are not ready to let AI send anything directly"

Positioning line:

> I would build the first layer as a front desk plus an exception desk: capture the request, classify it, route clean work, and hold anything sensitive or ambiguous for human review.
