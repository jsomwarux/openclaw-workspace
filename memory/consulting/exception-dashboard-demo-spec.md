# Exception Dashboard Demo Spec

## Purpose
Build a reusable demo that makes the AI Operations Diagnostic tangible.

The demo should show the buyer the actual operating layer JT recommends: not a chatbot, but a dashboard of stuck work, changed state, approval needs, and audit trail.

## Buyer promise
“You do not need AI that talks more. You need a system that shows what changed, what is stuck, who owns it, and what needs approval.”

## Target verticals
- Family offices / property operators
- Construction and real estate teams
- Finance/back-office operations
- Hospitality/service businesses

## Core dashboard sections
1. **Stuck work**
   - Item
   - Workflow
   - Current status
   - Age
   - Owner
   - Reason stuck

2. **Changed since last review**
   - Item
   - Previous state
   - Current state
   - Source
   - Importance

3. **Approval needed**
   - Decision required
   - Dollar/risk impact
   - Recommended action
   - Human approver
   - Deadline

4. **Missing / expiring documents**
   - Document type
   - Vendor/property/account
   - Expiration/missing date
   - Owner
   - Follow-up status

5. **Audit trail**
   - Timestamp
   - Source system/file
   - AI/rule classification
   - Human action taken
   - Notes

## Demo datasets
### Family-office/property ops
- Insurance COI expiring in 14 days
- Rent delinquency over 30 days
- Missing vendor W-9
- Owner report changed since last week
- QuickBooks export failed

### Construction ops
- Job has no field update in 48 hours
- Change order awaiting approval
- Vendor delay mentioned in field note
- Budget variance above threshold
- Missing closeout photos

### Hospitality/service ops
- Guest issue awaiting manager follow-up
- Vendor invoice over estimate
- Staff schedule exception
- Maintenance issue not assigned
- VIP request aging without owner

## UI requirements
- Dark premium style matching jtsomwaru.com
- Filter by workflow, owner, risk, status
- Clear “needs approval” CTA
- Timeline/audit drawer per item
- Top summary cards: overdue, approval needed, high risk, changed today

## Build plan
1. Create static Next.js demo page or embedded project card.
2. Use mock data only.
3. Add screenshots/GIF for portfolio/proposals.
4. Link from AI Operations Diagnostic materials.
5. Reuse as live demo in warm-lead calls.

## Acceptance criteria
- A buyer understands the value in under 30 seconds.
- Demo is not tied to one vertical.
- No real client data included.
- Shows exception visibility, not generic analytics.
