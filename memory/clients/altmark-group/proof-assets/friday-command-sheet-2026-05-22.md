# Altmark Friday Command Sheet — 2026-05-22

Purpose: make Friday's Altmark move concrete: turn installed PC + finished insurance workflow into accepted delivery, payment/deposit clarity, and safe next infrastructure work.

## Highest-Leverage JT Action
Use the short confirmation message with Yair/Navid before doing any deeper infrastructure changes.

> Yair — now that the workflow PC is installed, I want to close the loop cleanly on the first system.
>
> Can we confirm four things?
> 1. Who can access the installed PC and check the workflow/logs
> 2. Whether the insurance expiration workflow is accepted as live/useful, or what open items remain with owner/date
> 3. Status on final insurance workflow approval/payment
> 4. Rent delinquency timing: deposit status and who owns the clean sample report/date
>
> Once those are clear, I’ll document the support path, lock the next build sequence, and handle the HTTPS/Google OAuth reliability step without mixing it into acceptance.

## Why This Comes Before The HTTPS/OAuth Work
- Acceptance/payment clarity is the revenue/proof gate.
- HTTPS + Google OAuth is important infrastructure, but it should not obscure whether the first workflow is accepted.
- If admin access is not confirmed, infrastructure migration can create avoidable risk.

## Friday Sequence
1. Confirm installed PC access path and admin/session owner.
2. Confirm insurance workflow/logs are visible on the installed PC.
3. Capture exact client wording: accepted/live/useful vs open items.
4. Confirm final insurance approval/payment status.
5. Confirm rent delinquency deposit timing and clean sample report owner/date.
6. Only after access is clear: back up n8n/workflows before HTTPS/OAuth migration.
7. Update Client OS + proof gate from facts only.

## Acceptance Capture Table
Fill only from real confirmation.

| Gate | Status | Evidence / exact wording | Owner | Date |
|---|---|---|---|---|
| Installed PC access path known | Unknown |  | JT/Navid |  |
| Admin/session owner known | Unknown |  | JT/Navid |  |
| Insurance workflow visible on installed PC | Unknown |  | JT/Yair/Navid |  |
| Logs/audit trail visible | Unknown |  | JT/Navid |  |
| Open issues listed with owner/date | Unknown |  | JT/Yair/Navid |  |
| Acceptance wording captured | Unknown |  | Yair/Navid |  |
| Insurance approval/payment status known | Unknown |  | JT/Yair |  |
| Rent delinquency deposit timing known | Unknown |  | JT/Yair |  |
| Clean sample rent report owner/date known | Unknown |  | Yair/Matt/JT |  |

## If The Client Says “Accepted / Looks Good”
Immediately capture:
- Exact wording or paraphrase label.
- Whether final payment/approval is complete or pending.
- One redacted screenshot/log candidate for proof.
- Any caveats or open issues.

Then use `proof-assets/acceptance-and-referral-sequence.md`, but keep the referral ask blocked until payment/proof gate is clean.

## If There Are Open Issues
Do not push referral/proof.

Record:
- Issue
- Owner
- Due date
- Whether it blocks acceptance/payment
- Whether it blocks HTTPS/OAuth migration

## Proof-Safe Claim If Gate Clears
Anonymized default:

> Local-first automation infrastructure for a NYC family-office/property-operations team: sensitive files stay local, workflow runs are auditable, exceptions become visible, and financial/external actions remain human-approved.

Do not claim ROI, hours saved, named Altmark proof, rent delinquency automation live, autonomous tenant outreach, or client quote unless explicitly captured and permitted.

## Mission Control Done State
The top Altmark acceptance task is done only when access, acceptance wording, payment/approval status, rent deposit timing, and sample-report owner/date are recorded in Client OS or this sheet.
