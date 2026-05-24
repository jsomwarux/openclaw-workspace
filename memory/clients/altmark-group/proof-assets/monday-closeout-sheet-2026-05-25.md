# Altmark Monday Closeout Sheet — 2026-05-25

Purpose: turn the installed PC + finished insurance workflow into a clean acceptance/payment/proof gate, without letting infrastructure migration blur the commercial closeout.

## Monday Objective
Get one source-of-truth answer from Yair/Navid on four things:

1. **Access/admin owner** — who can access the workflow PC, n8n, and logs now that it is installed.
2. **Acceptance/open issues** — whether the insurance expiration workflow is accepted as live/useful, or exactly what remains with owner/date.
3. **Payment/final approval** — whether the insurance workflow final payment/approval step is complete or what is needed.
4. **Rent delinquency readiness** — deposit timing and who owns the clean sample report/date.

## Copy JT Can Send

> Yair/Navid — quick Monday closeout so I can keep the next step clean.
>
> Now that the workflow PC is installed, can we confirm:
> 1. Who has access/admin ownership for the installed PC and n8n/logs
> 2. Whether the insurance expiration workflow is accepted as live/useful, or what open items remain with owner/date
> 3. Final approval/payment status for the insurance workflow
> 4. Rent delinquency timing: deposit status and who owns the clean sample report/date
>
> Once those are clear, I’ll lock the support path and handle the HTTPS/Google OAuth reliability migration without mixing it into acceptance/payment.

## Decision Rule
Do not start or prioritize the HTTPS/Google OAuth migration until at least the access/admin owner and backup path are known.

Why: the migration is reliability work; acceptance/payment clarity is the revenue gate. If the URL/OAuth work breaks or needs client decisions before the commercial facts are captured, it creates avoidable confusion.

## If Acceptance Is Confirmed
Record immediately:

| Field | Capture |
|---|---|
| Acceptance wording | Exact quote or close paraphrase |
| Payment/final approval | Paid / approved / pending / blocker |
| Open issues | Issue, owner, due date, blocks acceptance? |
| Proof evidence | Redacted screenshot/log/status summary only |
| Permission boundary | Internal-only / anonymized / named / no reuse |
| Referral readiness | Positive enough for 2–3 qualified intros? yes/no |

Then update:
- `client-os/dashboard.md`
- `client-os/weekly-updates.md`
- `client-os/acceptance-checklist-insurance-expiration.md`
- `memory/networking/contacts.md` Yair ledger
- `proof-assets/acceptance-and-referral-sequence.md` only if payment/proof gate is clean

## If Open Issues Remain
Do not ask for referrals or proof permission. Log this table:

| Issue | Blocks acceptance? | Owner | Due date | Next action |
|---|---|---|---|---|
|  |  |  |  |  |

Then patch the dashboard/runbook from verified facts only.

## Safe Proof Claim If Gate Clears
Anonymized default only:

> Local-first automation infrastructure for a NYC family-office/property-operations team: sensitive files stay local, workflow runs are auditable, exceptions become visible, and financial/external actions remain human-approved.

Do not claim hours saved, ROI, named Altmark proof, tenant outreach automation, or client quote unless explicitly captured and permitted.

## Done State
This sheet is complete when the four confirmation points are recorded in Client OS and Mission Control no longer has infrastructure migration ranked above acceptance/payment clarity.
