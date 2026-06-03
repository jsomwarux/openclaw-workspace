---
name: proposal-pdf
description: "Create a branded client proposal, quote, SOW, or priced scope as a PDF/HTML deliverable in JT's house style, with reconciled use-case pricing, timeline, assumptions, proof-safe language, and one final verification pass."
---

# Proposal PDF

Use for client-facing proposals and priced scopes. Drafts are internal until JT reviews and sends.

## Inputs
Ask once if missing:
- client name and contact
- proposal title and subtitle
- use cases with title, price, description, and recommendation note if any
- implementation timeline
- support/retainer line if any
- assumptions, exclusions, and access needed

## House Style
- Split header: title/subtitle left, prepared-for/date right.
- 4px blue accent line: `#4A6CF7` to `#6B8AFF`.
- Uppercase section labels in blue.
- Use-case cards: title left, price right, recommendation note in blue italic.
- Investment table: all line items reconcile to total.
- Footer: `JT Somwaru | jtsomwaru.com`.
- Body font: Helvetica/Arial, dark slate `#2D3748`, Letter size.

## Workflow
1. Build or copy `skills/proposal-pdf/assets/proposal_template.html`.
2. Fill all placeholders. Do not leave `{{PLACEHOLDER}}`.
3. Render HTML to PDF with WeasyPrint when available:
   ```bash
   python3 -c "from weasyprint import HTML; HTML('proposal.html').write_pdf('proposal.pdf')"
   ```
4. If WeasyPrint is unavailable, save the completed HTML and state that PDF render is blocked.
5. Upload substantive proposal deliverables to Drive for JT review.

## Content Rules
- Use independent AI implementation consultant framing.
- Do not imply a client is public proof unless permission exists.
- Price outcomes, not tasks. The proposal can mention workflows, integrations, dashboards, or agents, but the buyer should understand the operational result.
- If phasing exists, make it explicit in both use cases and investment table.
- Never bury monthly support in implementation total.

## Verification
- Prices reconcile to the total.
- No placeholders remain.
- Footer renders.
- No secrets or private client details appear.
- The proposal includes assumptions/access needed and next step.
