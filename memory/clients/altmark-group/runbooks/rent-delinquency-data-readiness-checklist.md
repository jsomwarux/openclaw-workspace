# Altmark Rent Delinquency Workflow — Data Readiness Checklist

Created: 2026-05-06
Purpose: keep the rent delinquency workflow moving while Altmark cleans reporting/tenant ledgers, without starting automation against unreliable data.

## Current Situation
Yair said the office is overwhelmed, Matt is away, internal reporting needs cleanup, and many tenant ledgers need cleanup before the delinquency report is accurate. This is a data-readiness blocker, not a rejection of the workflow.

## Readiness Gate
Do **not** begin build work or external outreach logic until Altmark can provide a clean source report and confirms the 50% start deposit timing.

The workflow is ready to start when these five items are true:

1. **Source of truth named**
   - [ ] Altmark confirms the rent delinquency report/source system that should drive the workflow.
   - [ ] Report owner is named: Matt / Karen / Yair / other.
   - [ ] Report refresh cadence is known: daily / weekly / monthly / manual.

2. **Required fields present**
   - [ ] Tenant name / entity
   - [ ] Property / unit identifier
   - [ ] Current balance due
   - [ ] Amount overdue
   - [ ] Days past due or due date
   - [ ] Last payment date
   - [ ] Contact method available, if outreach is in scope
   - [ ] Internal owner / manager
   - [ ] Notes / special handling flag

3. **Ledger cleanup assumptions documented**
   - [ ] Credits/prepayments are not misread as delinquency.
   - [ ] Payment plans are clearly flagged.
   - [ ] Disputed balances are clearly flagged.
   - [ ] Legal/eviction-sensitive accounts are clearly flagged.
   - [ ] Recently paid balances have a cutoff rule.

4. **Sample output approved**
   - [ ] Altmark provides one cleaned sample report/export.
   - [ ] JT reviews the sample and returns an exception list.
   - [ ] Yair/Matt confirms the sample output matches how Altmark thinks about delinquency.

5. **Approval + payment boundary clear**
   - [ ] 50% start deposit timing confirmed before build begins.
   - [ ] Human approval required before any tenant-facing outreach.
   - [ ] No automated financial/accounting actions without explicit approval.

## Edge Cases To Ask About
| Edge Case | Why It Matters | Required Rule Before Automation |
|---|---|---|
| Payment plan tenants | They may be technically delinquent but should not receive normal outreach | Flag and route to manual review |
| Recently paid balances | Reports may lag behind payment posting | Add payment recency cutoff |
| Disputed charges | Outreach could create client-service or legal risk | Exclude or manual approval only |
| Partial payments | Need threshold logic | Define balance/age threshold |
| Multiple units / entities | Same tenant/entity may appear across units | Confirm grouping rule |
| Legal/eviction accounts | Sensitive workflow category | Exclude unless approved by Yair |
| Credits/prepayments | Can create false positives | Confirm balance sign logic |
| Missing contact info | Outreach cannot run cleanly | Route to data cleanup list |

## Draft Message JT Can Send Yair

> Yair — makes sense on the ledger/report cleanup. To keep the rent delinquency workflow clean and avoid building around bad data, I put together the minimum readiness checklist I’d want before I start that automation.
>
> The main things I’ll need are: the source delinquency report, required fields like tenant/property/balance/days past due/last payment, any flags for payment plans/disputes/legal accounts, and one cleaned sample export that Matt/Karen/Yair agree is accurate.
>
> Once that sample is ready, I can review it for edge cases before building the workflow. I’ll also wait for the 50% start deposit before build work begins, per the proposal.

## Acceptance Criteria For Starting Build
- Altmark sends a cleaned sample report/export.
- JT can identify clear automation rules and exception categories.
- Altmark confirms which records should be excluded or human-reviewed.
- Deposit timing is confirmed.
- Workflow build can begin without guessing against unreliable ledger data.

## Reusable Pattern
For property/family-office automation, delinquency outreach is not an “AI writing” problem first. It is a data-readiness and exception-routing problem. If ledgers are dirty, the highest-value implementation move is to define the clean input contract before automating outreach.
