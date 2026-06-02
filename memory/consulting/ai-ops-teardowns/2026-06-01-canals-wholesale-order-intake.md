# AI Ops Teardown - Canals Wholesale Order Intake Desk

Date: 2026-06-01
Current signal: Canals raised $35M to bring AI automation to wholesale distribution, reported 2026-05-29 by Unite.AI.
Source URL: https://www.unite.ai/canals-raises-35m-to-bring-ai-automation-to-the-8-2-trillion-wholesale-distribution-industry/
Niche: Wholesale Distribution Operations
Build tier: Tier 2 now. Tier 3 only after posted-teardown reply/DM signal or explicit JT priority.

## Business Context

Wholesale distributors still receive orders through messy channels: emails, PDFs, spreadsheets, handwritten notes, voice messages, and rep-forwarded customer requests. The business pressure is not only extraction. The hard part is getting from messy customer input to an ERP-ready order without corrupting SKU, quantity, pricing, inventory, margin, or approval state.

Canals' funding is a useful public signal because it points to a large, unglamorous workflow: order intake.

## Current Manual Process

1. Customer sends an order through email, PDF, spreadsheet, note, or voice message.
2. Sales or customer service reads it manually.
3. Someone identifies customer, SKU, quantity, unit, requested date, and attachments.
4. Someone checks catalog, customer-specific pricing, availability, and margin rules.
5. Exceptions move through ad hoc Slack/email/conversation.
6. A clean order is entered into the ERP.
7. The customer receives confirmation.

## Failure Modes

- Wrong unit count or pack size.
- SKU alias mismatch.
- Missing customer or ship-to detail.
- Customer-specific pricing conflict.
- Inventory or backorder ambiguity.
- Margin exception with no owner.
- Duplicate order from forwarded messages.
- No audit trail from source request to ERP-ready entry.

## Proposed AI Ops Workflow

| Step | Input | System action | Human boundary | Output |
|---|---|---|---|---|
| 1 | Email/PDF/spreadsheet/note/voice transcript | Normalize source into one intake queue | None | Intake record with source attached |
| 2 | Intake record | Extract customer, SKU, quantity, unit, requested date, attachments | Low-confidence fields route to review | Structured draft order |
| 3 | Draft order | Match SKU aliases, catalog records, customer pricing, inventory, and margin rules | Exceptions route to assigned owner | Clean order or exception packet |
| 4 | Exception packet | Draft the question and suggested resolution | Owner approves, edits, or rejects | Approved resolution |
| 5 | Clean order | Prepare ERP-ready entry and confirmation summary | Human approval before ERP post if risk threshold is met | ERP-ready draft |
| 6 | Approved output | Log source, extraction, edits, approver, timestamp, and result | None | Audit trail and weekly exception report |

## n8n Node Sketch

1. Trigger: shared inbox, uploaded file, or form intake.
2. Data source: email body, PDF attachment, spreadsheet, or transcript.
3. Clean/normalize: document parser + table normalization.
4. AI extraction/classification: customer, SKU, quantity, unit, requested date, notes, attachments.
5. Rules/thresholds: SKU confidence, pricing match, inventory state, margin threshold, duplicate detection.
6. Approval queue: route exception to customer service, sales, purchasing, or margin owner.
7. Notification: draft buyer confirmation or internal clarification.
8. Audit log: source, extracted fields, changes, approver, final state.
9. Error handling: low-confidence source goes to manual review; no silent ERP posting.

## Why This Is Reusable

This pattern applies across wholesale, supply houses, restaurant equipment, electrical distributors, plumbing/HVAC supply, and any order-heavy SMB where customers send work in their own format but the business needs clean ERP state.

## Content Hook

Canals just raised $35M for a wholesale problem every distributor recognizes: orders arrive messy.

## Proof-Safe Framing

- Public Canals funding signal only.
- No claim that Canals is a client.
- No private client names.
- No fake ROI, hours saved, client acceptance, or access to Canals' internal workflow.
- The workflow is JT's proposed implementation pattern, not a claim about Canals' internal product architecture.
