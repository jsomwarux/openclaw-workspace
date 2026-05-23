# Altmark Weekend Command Sheet — 2026-05-23

Purpose: keep Altmark momentum clean over the weekend by separating the revenue/proof gate from the infrastructure reliability work.

## Highest-Leverage JT Action
Send one tight confirmation note to Yair/Navid before doing any HTTPS/OAuth migration work.

> Yair/Navid — quick weekend closeout so I can keep the next step clean.
>
> Now that the workflow PC is installed, can we confirm:
> 1. Who has access/admin ownership for the installed PC and n8n/logs
> 2. Whether the insurance expiration workflow is accepted as live/useful, or what open items remain with owner/date
> 3. Final approval/payment status for the insurance workflow
> 4. Rent delinquency timing: deposit status and who owns the clean sample report/date
>
> Once those are clear, I’ll lock the support path and handle the HTTPS/Google OAuth reliability migration without mixing it into acceptance/payment.

## Decision Rule
Do **not** treat the HTTPS/Google OAuth migration as the top move until these are known:
- PC/admin access path
- Insurance workflow acceptance wording or open issues
- Payment/final approval status
- Rent delinquency deposit timing
- Clean sample report owner/date

Why: infrastructure reliability matters, but acceptance/payment clarity is the revenue and proof gate. Migrating infrastructure before admin/access ownership is confirmed creates avoidable risk.

## If They Confirm Acceptance
Capture immediately:
- Exact acceptance wording or close paraphrase.
- Final payment/approval status.
- Whether any issues remain and whether they block acceptance.
- One redacted proof candidate: screenshot/log/status summary with no sensitive policy/entity/network details.
- Permission boundary: internal-only, anonymized, named, or no reuse.

Then update:
- `client-os/dashboard.md`
- `client-os/weekly-updates.md`
- `client-os/acceptance-checklist-insurance-expiration.md`
- `proof-assets/acceptance-and-referral-sequence.md` only after payment/proof gate is clean

## If They Report Open Issues
Do not ask for referrals or proof permission yet.

Record:
| Issue | Blocks acceptance? | Owner | Due date | Next action |
|---|---|---|---|---|
|  |  |  |  |  |

Then patch the insurance runbook and dashboard from facts only.

## If They Do Not Reply
Monday morning move:
- Follow up once with the same four-point confirmation.
- Do not start rent delinquency build work.
- Do not run HTTPS/OAuth migration unless JT already has admin access + backup path.

## Safe Proof Claim If Gate Clears
Anonymized default only:

> Local-first automation infrastructure for a NYC family-office/property-operations team: sensitive files stay local, workflow runs are auditable, exceptions become visible, and financial/external actions remain human-approved.

Do not claim hours saved, ROI, named Altmark proof, tenant outreach automation, or client quote unless explicitly captured and permitted.

## Done State
This sheet is complete when the four confirmation points are recorded in Client OS and Mission Control no longer has infrastructure migration ranked above acceptance/payment clarity.
