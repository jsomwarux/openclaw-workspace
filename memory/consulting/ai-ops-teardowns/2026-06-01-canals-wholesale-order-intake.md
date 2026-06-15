# AI Ops Teardown - Canals Wholesale Order Intake Desk

Date: 2026-06-01
Score: 26/30
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

## Public Post Boundary

The LinkedIn/X version should name Canals as the public signal and say what JT would build for a distributor in this lane: a shared order-intake desk that reads messy inputs, extracts order fields, checks catalog/pricing/inventory/margin rules, drafts clean ERP-ready output, and routes exceptions to the right owner.

Hold back the build recipe. Do not publish the exact node stack, prompts, schemas, confidence thresholds, duplicate-detection logic, vendor choices, or proprietary routing rules. The public value is the diagnostic map and operating shape; the paid value is implementation.

## Proof-Safe Framing

- Public Canals funding signal only.
- No claim that Canals is a client.
- No private client names.
- No fake ROI, hours saved, client acceptance, or access to Canals' internal workflow.
- The workflow is JT's proposed implementation pattern, not a claim about Canals' internal product architecture.

## Diagnostic CTA

Buyer-safe CTA/comment:

> If messy order intake is the workflow holding the team together, start with an order-intake readiness checklist and diagnostic: inputs, exception owners, approval rules, ERP handoff, and audit trail before anything autonomous.

Reply/DM routing: route relevant wholesale/distribution operator replies to the order-intake workflow diagnostic path in `memory/drafts/ai-operations-diagnostic-one-pager.md` and the consulting pipeline. If a reply is property/family-office specific, route it instead to `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md`.

## Posted-Log Instruction

Only after JT posts and provides a public URL, append exactly one JSONL entry to `memory/content/posted-log.jsonl`:

```json
{"date":"2026-06-03","platform":"LinkedIn","title":"Canals Wholesale Order Intake Desk","source":"memory/content/bank/2026-06-01/ai-ops-teardown-canals-wholesale-order-intake.md","url":"PUBLIC_URL_HERE","posted":true,"cta":"ai-operations-diagnostic","reply_route":"memory/drafts/ai-operations-diagnostic-one-pager.md"}
```

If JT defers, do not write a posted-log record. Update `memory/consulting/ai-ops-teardowns/delivery-calendar.md` with the reason and next review date.
