# Altmark Rent Delinquency - Yair Approve/Edit Packet

Created: 2026-06-12
Owner: JT sends; Eve drafts only.
Status: draft for approval/edit. Do not send automatically.
Drive: https://docs.google.com/document/d/17yM9wJenUlnbefye1EMF_sbpyVXTm8t5v80Xt1Kf3Lw/edit

## Send Goal
Convert the rent delinquency workflow block from open-ended client homework into one approve/edit decision.

## JT Message Draft

Yair,

I put the rent delinquency workflow into an approve/edit format so you do not have to build the process from scratch.

Below are the default touch points I would use for the first supervised batch. If these are directionally right, reply **APPROVED** and I will run the first batch in review-only mode Thursday. If you want edits, just mark the lines you want changed.

I only need one small source item before the run: please forward one sample AppFolio delinquency email or export you already use today. You can redact tenant names, unit numbers, emails, balances, and notes. I only need the column/field shape and wording pattern.

Recommended sender: Altmark operations inbox or the normal property-management sender already used for tenant notices.

Recommended reply-to: the team inbox/person who already handles delinquency replies, not my email.

## Draft Touch 1 - Friendly Reminder

Subject: Past-due balance reminder

Hi [Tenant First Name],

Our records show a past-due balance for [Property/Unit]. If you already submitted payment, thank you and no action is needed.

If payment is still pending, please submit it through the usual payment portal or reply with any payment-status update so the team can review the account.

Thank you,
[Altmark Team Name]

## Draft Touch 2 - Firm Notice

Subject: Past-due balance follow-up

Hi [Tenant First Name],

We are following up because the account for [Property/Unit] still appears past due.

Please submit payment or reply with an update by [Date]. If there is an existing payment plan, recent payment, dispute, or account issue, reply with that context so the team can route it correctly before any next step.

Thank you,
[Altmark Team Name]

## Draft Touch 3 - Escalation / Review Needed

Subject: Account review needed

Hi [Tenant First Name],

This is a final follow-up before the account is moved into the next internal review step.

Please submit payment or reply with status by [Date]. If this account is already in a payment plan, dispute, legal/process-sensitive status, recent-payment state, or credit/prepayment state, reply with that information so the team can prevent the wrong next action.

Thank you,
[Altmark Team Name]

## Defaults for First Supervised Batch
- Run mode: review-only.
- Tenant-facing output: drafts only until approved by Altmark.
- Queues: included, manual review, excluded, cleanup.
- Stop conditions: missing contact info, legal/process-sensitive status, disputes, payment plans, recent payments, credits/prepayments, or unclear required fields.
- Proof capture: row counts, queue counts, exception reasons, and approval state only. No tenant-private data reused publicly.

## JT Close

If this works, reply **APPROVED** and forward one sample AppFolio delinquency email/export. I will run the first supervised batch Thursday in review-only mode and send you the queue for approval before anything goes out.

## Evidence / Boundaries
- Synthetic dry run passed on 2026-05-29: 8 rows processed; 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 unclassified.
- Evidence path: `memory/clients/altmark-group/client-os/outputs/rent-delinquency-synthetic-smoke-test-log-2026-05-29.md`
- Public proof remains blocked until acceptance and permission/anonymization gates clear.
