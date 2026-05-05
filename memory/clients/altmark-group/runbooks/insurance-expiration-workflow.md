# Altmark Insurance Expiration Workflow Runbook

## Workflow Purpose
Track insurance documents/expiration dates, surface upcoming expirations, and create a clear audit trail so coverage gaps are visible before they become urgent.

## Current Status
Workflow finished per JT update. Needs acceptance confirmation, screenshots, and final payment/approval status if not already complete.

## Inputs
- Insurance policy/certificate documents
- Vendor/property/account identifiers
- Expiration dates
- Review status
- Follow-up owner

## Outputs
- Expiration tracker
- Upcoming expiration alerts
- Missing/expired coverage exceptions
- Review/audit log
- Owner-ready status summary

## Human-in-Loop Rules
- Do not send sensitive or external follow-up without human approval.
- Flag uncertain extraction results for review.
- Escalate missing documents and near-term expirations.

## Acceptance Criteria
- Workflow identifies active/expired/upcoming insurance items.
- Test dataset matches expected expiration results.
- Exceptions are visible in one place.
- Yair/Navid can understand how to review status.
- Logs show when the workflow ran and what changed.

## Open Items
- Add screenshots.
- Confirm final acceptance.
- Confirm payment status.
- Capture edge cases from first real use.
