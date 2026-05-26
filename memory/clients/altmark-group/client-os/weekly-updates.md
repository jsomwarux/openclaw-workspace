# Weekly Updates — Altmark Group

## Week of 2026-05-19 — PC Installed / Acceptance Gate

### Wins
- Dedicated workflow PC was installed at Altmark's office on 2026-05-19.
- Delivery state moved from pre-handoff planning to post-install acceptance, access verification, payment clarity, and proof capture.
- Eve prepared the HTTPS + Google OAuth migration runbook for the next reliability step: `runbooks/n8n-https-google-oauth-migration-plan-2026-05-21.md`.

### Misses / Blockers
- Eve memory does not yet have Yair/Navid acceptance wording, final insurance workflow payment/approval status, or rent-delinquency deposit timing.
- Referral/proof reuse remains blocked until acceptance/payment clarity and redacted proof evidence are captured.

### What Changed In The Workflow
- The active gate is no longer “schedule PC handoff.” It is now: confirm who can access the installed PC, verify the insurance workflow/logs on-site, record open issues with owner/date, capture acceptance wording, and confirm next-payment/deposit status.

### Metrics Movement
- Installation milestone completed. Accepted workflows remain 0 confirmed in Eve memory until client acceptance wording is captured.

### Next Week's Plan
- JT uses `proof-assets/tuesday-closeout-branch-sheet-2026-05-26.md` after the Monday closeout ask to choose the exact next move: record confirmed facts, ask one missing-field follow-up, or send a short no-reply bump.
- Sequence is explicit: closeout/acceptance first, migration second. Do not infer acceptance from silence, and do not let HTTPS/OAuth migration outrank access/payment/proof capture.
- Use the HTTPS/OAuth runbook only after access/admin ownership and backup path are clear: back up n8n, move it to a stable HTTPS endpoint, publish/configure the Google OAuth app, reconnect credentials, and smoke-test a non-sensitive Sheets/Drive workflow.
- Eve updates the proof package only from verified facts and keeps the Yair referral ask blocked until `proof-assets/referral-readiness-gate-2026-05-23.md` is green.

### Client Decision / Input Needed
- Confirm installed PC access path and any open setup issues.
- Confirm insurance workflow accepted/live/useful wording and payment/approval status.
- Confirm rent-delinquency deposit timing and clean sample export owner/date.



## Week of 2026-05-13 — Delivery OS Hardening

### Wins
- Added proof-safe acceptance checklist for the insurance expiration workflow: `acceptance-checklist-insurance-expiration.md`.
- Added reusable IP log so insurance exception tracking and rent delinquency data-readiness can become templates without leaking private Altmark data.
- Added raw/cleaned/output folder READMEs with explicit privacy boundaries.

### Misses / Blockers
- Acceptance/payment status remains unconfirmed in Eve memory.
- Public proof/referral ask remains blocked until PC/access path, workflow acceptance, and payment/deposit clarity are clean.

### What Changed In The Workflow
- Delivery now has an explicit acceptance gate: access/use, end-to-end run, logs/audit trail, open issues, support/rollback, payment/deposit status, and redacted proof evidence.

### Metrics Movement
- Documentation completeness improved; client outcome metrics still wait on accepted workflow evidence.

### Next Week's Plan
- Use the existing Altmark MC task to lock PC handoff + acceptance/payment clarity.
- After acceptance, capture redacted proof and only then ask for warm family-office referrals.

### Client Decision / Input Needed
- Confirm first workflow is accepted/live/useful.
- Confirm open issues and payment/deposit timing.

## Week of 2026-05-12

### Focus
- Convert Altmark from “built” to accepted: PC handoff, insurance workflow verification, payment clarity, and clean next-workflow gate.

### Wins
- Wednesday execution pack prepared at `proof-assets/wednesday-execution-pack-2026-05-13.md` with exact send-first copy, acceptance criteria, post-call notes, and proof-capture checklist.
- Tuesday execution pack remains available at `proof-assets/tuesday-execution-pack-2026-05-12.md`.
- Existing runbooks/checklists already cover PC handoff, insurance workflow acceptance, and rent-delinquency data readiness.

### Blockers / Risks
- Handoff date/time still needs confirmation if not already locked.
- Insurance workflow approval/payment status is still unknown in Eve memory.
- Rent delinquency remains client-data-gated; building before a cleaned sample report would create rework and client risk.

### Next Action
- JT sends/uses the Wednesday execution message to lock the handoff/access path and acceptance/payment/deposit statuses.

### Decision Rule
- Referrals wait until the first workflow is accepted and payment/deposit status is clean.

## Week of 2026-05-05

### Wins
- Insurance expiration workflow is finished and ready for acceptance verification.
- Dedicated workflow PC has been set up for on-site delivery.
- Client OS/runbook structure is now in place for dashboard, metrics, decisions, failures, weekly updates, and repeatable IP.

### Misses / Blockers
- Insurance workflow acceptance/payment status is still unknown.
- PC handoff date/time still needs confirmation with Yair/Navid.
- Rent delinquency workflow is paused by Altmark-side reporting/ledger cleanup: Matt is away, office is overwhelmed, internal reporting needs cleanup, and tenant ledgers need cleanup before the delinquency report is accurate.
- Rent delinquency workflow should not begin until the data-readiness checklist is satisfied and the 50% deposit is confirmed.
- Proof/referral asset should wait until handoff + acceptance are clean.

### What Changed In The Workflow
- First workflow moved from build stage to acceptance/handoff stage.
- Delivery focus is now operational verification: install/access PC, run or demonstrate workflow, show logs/audit trail, document issues with owner/date.

### Metrics Movement
- Baseline/current metrics still need first real workflow data.
- First metrics to capture: number of insurance records tracked, number of upcoming/expired exceptions surfaced, review time saved, and missed-expiration risk reduced.

### Next Week's Plan
- Confirm PC delivery date/time.
- Complete on-site handoff with Navid/Yair.
- Verify insurance expiration workflow and logs/audit trail.
- Confirm insurance workflow acceptance/payment status.
- Send/use the rent delinquency data-readiness checklist before build work begins.
- Confirm rent delinquency deposit timing and start only after deposit + clean sample report.

### Client Decision / Input Needed
- Confirm PC handoff date/time.
- Confirm insurance expiration workflow acceptance and any remaining approval/payment step.
- Confirm who owns the cleaned rent delinquency source report and when a sample export will be ready.
- Confirm 50% deposit timing for rent delinquency workflow.
