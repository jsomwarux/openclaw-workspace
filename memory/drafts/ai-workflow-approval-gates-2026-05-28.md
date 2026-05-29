# AI Workflow Approval Gates Drafts - 2026-05-28

Purpose: review-only content draft from the 2026-05-28 heartbeat content lane. Do not post automatically.

Source proof:
- `memory/content/recent-builds.md` entry: Altmark Rent Delinquency Testing Pack
- `memory/research/altmark-rent-delinquency-nonpayment-risk-check-2026-05-28.md`
- `memory/clients/altmark-group/client-os/acceptance-checklist-rent-delinquency.md`
- `memory/clients/altmark-group/runbooks/rent-delinquency-workflow.md`

## LinkedIn Draft

Tenant outreach is where property management automation can go wrong fast.

A rent report can look clean and still hide the records that should never enter a normal message flow:

prior notices
recent payments
disputes
legal status
payment plans
missing contact data

The first job of the workflow is not to write the message.

The first job is to decide which rows are safe to touch, which rows need review, and which rows should stop before any tenant-facing draft exists.

That is the difference between a demo and a real operating system.

Demo logic says: report in, message out.

Production logic says: validate fields, isolate exceptions, keep an approval state, log every skipped reason, and start in review-only mode.

The AI part can help classify and draft.

The business value comes from the gates around it.

## X Draft

### Option A

The risky part of tenant outreach automation is not the writing.

It is knowing which records should never reach the writing step.

### Option B

Report in, message out is a demo.

Validate, flag, route, approve, log is a workflow.

### Option C

AI can draft the tenant message.

The workflow has to decide whether a message should exist.

That is the part most demos skip.

## Notes

- Keep this review-only until JT chooses a posting slot.
- Do not mention Altmark by name unless explicitly approved.
- Keep the public proof claim broad: approval-gated delinquency workflow for property operations.
