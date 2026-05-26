# Altmark Tuesday Closeout Branch Sheet — 2026-05-26

Purpose: give JT one clean Tuesday move after the Monday closeout ask, based on what happened. This avoids drifting into infrastructure work or referral asks before the revenue/proof gate is actually clear.

## Tuesday Objective
Turn the installed PC + finished insurance workflow into one of three states:

1. **Accepted / paid path clear** → update Client OS, capture redacted proof, then consider support/migration/referral sequencing.
2. **Partial reply** → ask one targeted missing-field follow-up.
3. **No reply** → send one short closeout bump that protects the commercial gate without sounding needy.

## Branch A — If Yair/Navid Confirm Acceptance + Access + Payment/Approval

Record immediately before doing anything else:

| Field | Evidence to capture |
|---|---|
| Access/admin owner | Named person/role for PC, n8n, logs |
| Acceptance wording | Exact quote or close paraphrase that workflow is live/useful/accepted |
| Open issues | Issue, owner, due date, whether it blocks acceptance |
| Payment/final approval | Paid / approved / pending / blocker |
| Rent delinquency next step | Deposit timing + clean sample report owner/date |
| Proof boundary | Internal-only / anonymized / named / no reuse |

Then update:
- `client-os/dashboard.md`
- `client-os/weekly-updates.md`
- `client-os/acceptance-checklist-insurance-expiration.md`
- `proof-assets/anonymized-workflow-case-file-draft.md`
- `proof-assets/referral-readiness-gate-2026-05-23.md`

Only after those updates: decide whether HTTPS/OAuth migration can start from `runbooks/n8n-https-google-oauth-migration-plan-2026-05-21.md`.

## Branch B — If Reply Is Partial

Do **not** ask all four questions again. Ask only for the missing commercial/proof field.

### Missing access/admin owner
> Thanks, that helps. One missing piece before I touch the reliability migration: who should be the owner for PC/n8n/log access on your side?

### Missing acceptance/open issues
> Thanks, that helps. Can you confirm whether the insurance workflow is accepted as live/useful, or list any open items with owner/date so I can close the delivery notes cleanly?

### Missing payment/final approval
> Thanks, that helps. What is the current final approval/payment status for the insurance workflow so I can keep the next build sequence clean?

### Missing rent delinquency deposit/sample report
> Thanks, that helps. For rent delinquency, who owns the clean sample report and when should I expect the deposit/report readiness before build work starts?

## Branch C — If No Reply By Tuesday Midday

Use this short bump. Do not mention referrals, case study, or broad future work.

> Yair/Navid — bumping this so I can keep the closeout clean before changing anything on the infrastructure side.
>
> Main thing I need is confirmation on access owner, whether the insurance workflow is accepted/live or has open items, final approval/payment status, and rent delinquency deposit/sample-report timing.
>
> Once I have that, I’ll separate support/reliability work from the next paid workflow.

## What Not To Do Tuesday

- Do not start HTTPS/OAuth migration without access/admin owner + backup path.
- Do not ask Yair for referrals until acceptance/payment/proof gates are green.
- Do not publish or reuse an Altmark proof claim externally.
- Do not infer acceptance from silence.
- Do not start rent delinquency build work without deposit timing + clean sample report readiness.

## Proof-Safe Default If Asked What JT Built

Use only in private/warm context until proof boundary is known:

> Local-first automation infrastructure for a property/family-office operations team: sensitive files stay local, workflow runs are auditable, exceptions become visible, and external/financial actions remain human-approved.

## Done State
This sheet is complete when Tuesday produces either:
- confirmed acceptance/access/payment facts recorded in Client OS, or
- one targeted missing-field follow-up sent by JT, or
- a no-reply bump sent and the Mission Control task remains open.
