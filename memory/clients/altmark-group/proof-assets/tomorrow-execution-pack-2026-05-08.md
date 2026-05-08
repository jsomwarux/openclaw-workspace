# Altmark Tomorrow Execution Pack — 2026-05-08

Purpose: give JT one clean sequence for the next Altmark touchpoint: PC handoff, insurance workflow acceptance, payment/deposit clarity, rent delinquency data readiness, then referral/proof packaging only after acceptance.

## Highest-Leverage Objective
Turn the first Altmark delivery into a clean accepted workflow and preserve momentum on the next paid workflow without building against dirty rent-ledger data.

## 10-Minute Prep Before Contacting Yair
- Open `runbooks/pc-handoff-checklist.md`.
- Open `runbooks/insurance-expiration-workflow.md`.
- Open `runbooks/rent-delinquency-data-readiness-checklist.md`.
- Confirm what proof screenshots can be captured without exposing sensitive data.
- Keep the ask narrow: handoff date/time + acceptance criteria + payment/deposit/data-readiness clarity.

## Recommended Message To Send Yair First
> Yair — quick check so I can make the handoff clean: what date/time works best for dropping off the dedicated workflow PC?
>
> For acceptance, I’d like to keep it simple: PC installed/accessed on-site, insurance expiration workflow verified, logs/audit trail shown, and any open issues written down with owner/date.
>
> Also want to confirm the status on the insurance workflow approval/payment and the 50% deposit timing for rent delinquency before I start that next build.
>
> On rent delinquency, makes sense that the ledger/report cleanup needs to happen first. Once Matt/Karen have one cleaned sample report, I can review it for edge cases before building anything around it.

## If Yair Says The Office Is Still Overwhelmed
Use this shorter fallback:

> Totally fine. I won’t start the rent delinquency build until the source report is reliable. The only thing I’d like to lock for now is the PC handoff/insurance workflow acceptance, then we can pick up rent delinquency once Matt/Karen have a cleaned sample export.

## Handoff Acceptance Checklist
- [ ] PC installed/accessed on-site.
- [ ] Altmark knows what the dedicated PC is for.
- [ ] Insurance expiration workflow demonstrated or dry-run verified.
- [ ] Logs/audit trail shown.
- [ ] Open issues captured with owner/date.
- [ ] Yair/Navid acceptance confirmed in writing or clearly paraphrased in notes.
- [ ] Insurance workflow approval/payment status confirmed.
- [ ] Rent delinquency 50% deposit timing confirmed before build work.

## Proof Capture Checklist
Capture only redacted/non-sensitive proof:
- [ ] Workflow status/tracker screenshot with sensitive names/accounts hidden.
- [ ] Log/audit screenshot proving a run occurred and changed or evaluated state.
- [ ] Before/after workflow map: manual tracking → local workflow + exception/audit trail.
- [ ] Acceptance quote or paraphrase from Yair/Navid.
- [ ] First metric when available: insurance records tracked, exceptions surfaced, review time saved, or missed-expiration risk reduced.

## Rent Delinquency Gate
Do **not** build until these are true:
- [ ] Source report/system is named.
- [ ] Report owner is named.
- [ ] Required fields exist: tenant/entity, property/unit, balance due, overdue amount, days past due/due date, last payment date, contact method if outreach is in scope, internal owner, notes/special handling.
- [ ] Edge cases are flagged: payment plans, disputes, legal/eviction accounts, recent payments, credits/prepayments, partial payments, multiple entities/units.
- [ ] Cleaned sample export is approved by Altmark.
- [ ] 50% start deposit timing is confirmed.
- [ ] Human approval remains required before any tenant-facing outreach.

## Referral Ask Timing
Do **not** ask Yair for intros yet unless the first workflow is accepted and payment/approval status is clean.

After acceptance, use `proof-assets/yair-referral-ask-script.md` and position it as:

> local-first automation for family-office back-office workflows that are too sensitive or too messy for generic SaaS.

## One-Line Proof Positioning
Local-first automation infrastructure for a NYC family-office/property-operations team: sensitive documents stay local, workflows produce audit trails, and financial or external actions stay human-approved.

## Files To Have Open
- `memory/clients/altmark-group/status.md`
- `memory/clients/altmark-group/runbooks/pc-handoff-checklist.md`
- `memory/clients/altmark-group/runbooks/insurance-expiration-workflow.md`
- `memory/clients/altmark-group/runbooks/rent-delinquency-data-readiness-checklist.md`
- `memory/clients/altmark-group/proof-assets/yair-referral-ask-script.md`
