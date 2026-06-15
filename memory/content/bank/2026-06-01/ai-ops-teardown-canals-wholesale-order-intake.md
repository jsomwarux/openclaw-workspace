# AI Ops Teardown - Canals Wholesale Order Intake Desk

## LinkedIn Draft

A distributor can receive a PDF, spreadsheet, voice note, and handwritten order before lunch.

Canals just raised $35M in wholesale automation because that mess still exists at scale.

One buyer emails a PDF. Another sends a spreadsheet. A rep forwards a voice note. A handwritten line item comes in with the wrong unit count.

The ERP still needs a clean order, price check, inventory check, exception owner, and confirmation back to the customer.

If I were mapping an AI implementation for a distributor in this lane, I would start with a shared order-intake desk.

It would read emails, PDFs, spreadsheets, and notes. It would extract customer, SKU, quantity, unit, requested date, and attachments. Then it would check catalog data, customer-specific pricing, inventory, and margin rules before anything hits the ERP.

When the order is clean, it drafts the ERP-ready entry and confirmation summary.

When something is off, it routes the exception to the right owner with the original source attached.

I would keep the build details private: field confidence, duplicate detection, margin thresholds, owner routing, audit logs, and approval rules.

Customers keep sending orders the way they already do. The distributor gets a cleaner intake layer before bad data reaches the system everyone depends on.

## CTA Comment

If messy order intake is the workflow holding the team together, start with an order-intake readiness checklist and diagnostic: inputs, exception owners, approval rules, ERP handoff, and audit trail before anything autonomous.

## Metadata

Date: 2026-06-01
Status: review-ready; not posted
Recommended first platform: LinkedIn

Supporting teardown: `memory/consulting/ai-ops-teardowns/2026-06-01-canals-wholesale-order-intake.md`
Current signal: Canals raised $35M to automate wholesale distribution workflows, reported 2026-05-29 by Unite.AI.
Source URL: https://www.unite.ai/canals-raises-35m-to-bring-ai-automation-to-the-8-2-trillion-wholesale-distribution-industry/

Score: 26/30
Build tier: Tier 2 now; Tier 3 candidate only after post signal or explicit JT priority.

## X Draft

Canals raising $35M is a signal that messy distributor order intake is finally getting attention.

PDFs.
Spreadsheets.
Voice notes.
Wrong unit counts.
Customer-specific pricing.
ERP-ready entry.

The AI implementation I would build: a shared order-intake desk that cleans the order, checks the rules, and routes exceptions before bad data hits the ERP.

## Buyer Relevance

Wholesale distributors recognize messy order intake immediately. The post uses a current company/funding signal, then translates it into a workflow JT can credibly map from his product catalog and operations background.

## Proof-Safe Framing

- Public company/news signal only.
- Canals is not represented as a client.
- No private client names.
- No fake ROI, hours saved, client acceptance, or internal access claims.
- Workflow is framed as what JT would build, not what Canals built internally.
- Public post explains the implementation shape, not the exact build recipe. Do not publish node stack, prompts, data schema, routing thresholds, vendor choices, or proprietary workflow logic.

## Reply/DM Routing

Route relevant wholesale/distribution operator replies to the order-intake workflow diagnostic path in `memory/drafts/ai-operations-diagnostic-one-pager.md` and the consulting pipeline. If a reply is property/family-office specific, route it instead to `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md`.

## Posted-Log Instruction

Only after JT posts and provides a public URL, append exactly one JSONL entry to `memory/content/posted-log.jsonl`:

```json
{"date":"2026-06-03","platform":"LinkedIn","title":"Canals Wholesale Order Intake Desk","source":"memory/content/bank/2026-06-01/ai-ops-teardown-canals-wholesale-order-intake.md","url":"PUBLIC_URL_HERE","posted":true,"cta":"ai-operations-diagnostic","reply_route":"memory/drafts/ai-operations-diagnostic-one-pager.md"}
```

If JT defers, do not write a posted-log record. Update `memory/consulting/ai-ops-teardowns/delivery-calendar.md` with the reason and next review date.
