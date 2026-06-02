# AI Ops Teardown - Canals Wholesale Order Intake Desk

Date: 2026-06-01
Status: review-ready; not posted
Recommended first platform: LinkedIn
Supporting teardown: `memory/consulting/ai-ops-teardowns/2026-06-01-canals-wholesale-order-intake.md`
Current signal: Canals raised $35M to automate wholesale distribution workflows, reported 2026-05-29 by Unite.AI.
Source URL: https://www.unite.ai/canals-raises-35m-to-bring-ai-automation-to-the-8-2-trillion-wholesale-distribution-industry/
Build tier: Tier 2 now; Tier 3 candidate only after post signal or explicit JT priority.

## LinkedIn Draft

Canals just raised $35M around a problem every wholesale distributor recognizes: messy orders.

One buyer emails a PDF. Another sends a spreadsheet. A rep forwards a voice note. A handwritten line item shows up with the wrong unit count.

The ERP still needs a clean order, price check, inventory check, exception owner, and confirmation back to the customer.

The workflow I would build starts with a shared order-intake desk.

It reads emails, PDFs, spreadsheets, and notes. It extracts customer, SKU, quantity, unit, requested date, and attachments. Then it checks catalog data, customer-specific pricing, inventory, and margin rules.

When the order is clean, it drafts the ERP-ready entry.

When something is off, it routes the exception to the right owner with the source attached.

Customers keep sending orders the way they already do. The distributor gets a cleaner intake layer before bad data hits the ERP.

## X Draft

Canals raising $35M is really about messy distributor orders.

PDFs.
Spreadsheets.
Voice notes.
Wrong unit counts.
Customer-specific pricing.
ERP-ready entry.

The AI workflow I would build is an order-intake desk with exception routing before bad data hits the ERP.

## Buyer Relevance

Wholesale distributors recognize messy order intake immediately. The post uses a current company/funding signal, then translates it into a workflow JT can credibly map from his product catalog and operations background.

## Proof-Safe Framing

- Public company/news signal only.
- Canals is not represented as a client.
- No private client names.
- No fake ROI, hours saved, client acceptance, or internal access claims.
- Workflow is framed as what JT would build, not what Canals built internally.

## Posted-Log Instruction

Only after JT posts and provides a public URL, append exactly one JSONL entry to `memory/content/posted-log.jsonl`:

```json
{"date":"2026-06-03","platform":"LinkedIn","title":"Canals Wholesale Order Intake Desk","source":"memory/content/bank/2026-06-01/ai-ops-teardown-canals-wholesale-order-intake.md","url":"PUBLIC_URL_HERE","posted":true,"cta":"workflow-diagnostic","reply_route":"memory/consulting/proof-led-acquisition-packet-2026-05-13.md"}
```

If JT defers, do not write a posted-log record. Update `memory/consulting/ai-ops-teardowns/delivery-calendar.md` with the reason and next review date.
