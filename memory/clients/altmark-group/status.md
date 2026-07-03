# Altmark Group — Client Status

Last updated: 2026-07-02

## Client
- Company: Altmark Group
- Website: https://www.altmarkgroup.com/
- Primary contact / decision maker: Yair, CFO
- Additional stakeholder: Navid for infrastructure/server/QuickBooks Desktop environment
- Source: JT update on 2026-04-30 + attached revised proposal PDF

## How It Started
Yair reached out to JT on Twitter asking whether JT was able and willing to build automation systems for Altmark. JT replied yes. Yair invited JT to Altmark's Bronx office. They reviewed the needed systems in person. JT created the revised AI Operations Build proposal and has been working on the tasks since.

## Proposal Summary
Proposal title: AI Operations Build — Prepared for Altmark Group — Revised Proposal — April 2026

### Foundation Infrastructure Setup — $4,000
Foundation is billed separately but delivered alongside the first use case. Goal: live infrastructure and working workflow within the same 2-week window.

Includes:
- Working session with Navid to assess server infrastructure, network, and QuickBooks Desktop environment
- Deploy/configure self-hosted automation server on Altmark's network
- Establish secure local access to required files and systems
- Configure monitoring, logging, backup workflow, and credential storage
- Document setup so Altmark owns/understands what is running

### Workflow / Use Case Buildout
Proposal pricing summary:
- Foundation — Infrastructure Setup: $4,000
- Insurance Expiration Tracking: $2,250
- Loan Management: $5,750
- WhatsApp AI Bot: $9,000
- Flagstar to QuickBooks Automation: $4,500
- Cash Management & Overdraft Prevention: $4,750
- Rent Delinquency Outreach: $4,500
- Total: $34,750
- Monthly support & maintenance: $1,500/month, 3-month minimum, begins after buildout is complete

Payment structure from proposal:
- Foundation ($4,000) paid in full at kickoff
- Each use case: 50% to start, 50% upon delivery and approval

Known active/current workflows from JT update:
1. Insurance expiration workflow — launched in production, working as expected after a few minor updates, and final 50% paid.
2. Dedicated PC setup — installed in Altmark office last week and running production workflow environment.
3. Rent delinquency workflow — initial 50% paid; JT is actively building and about to start testing.
4. DHCR Lease Renewal Automation Phase 1 — Altmark requested a new legal-rent renewal workflow; JT created a $3,500 proposal; Eve reviewed it on 2026-05-26 and created kickoff/acceptance/runbook assets on 2026-05-27. Sequence after rent delinquency deployment/testing unless Altmark explicitly reprioritizes.

## Current Status
- Active client engagement.
- Insurance expiration workflow is live in production and working as expected after a few minor updates.
- Altmark paid the final 50% for the insurance expiration workflow.
- Dedicated PC for workflows was installed in Altmark's office last week.
- Rent delinquency workflow is active. 2026-07-02 execution path from JT: finish setting up Conductor on Beelink, follow Danny's guide and set up everything needed, configure everything else needed for the rent delinquency bot, then use Fable for final playbook review before deploy/payment closeout. Altmark paid the initial 50%; 2026-05-29 synthetic dry run passed with 8 rows classified into 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 unclassified, and 0 tenant-facing drafts from sensitive/cleanup rows.
- Altmark pitched an additional workflow request: DHCR Lease Renewal Automation Phase 1, legal-rent renewals only. Proposal reviewed and delivery assets prepared. Next step after rent delinquency deployment/testing: confirm $1,750 kickoff payment, populated command center spreadsheet owner/date, current RGB rates, Phase 1 included units/properties, approved email recipients, and DHCR rent rolls for all included properties.

## Revenue / Payment Status
- Total proposed buildout: $34,750.
- Foundation Infrastructure Setup: $4,000, paid in full at kickoff per proposal.
- Insurance Expiration Tracking: $2,250; launched in production and final 50% paid.
- Rent Delinquency Outreach: $4,500; initial 50% paid, remaining $2,250 blocked on Yair sending source/export/reviewer/cadence/exception-rule inputs.
- Monthly support & maintenance: $1,500/month with 3-month minimum after buildout completion.

## Timeline From Proposal
- Everything starts with Navid infrastructure session.
- Foundation + first use case can be live within 2 weeks of that session.
- Full buildout across all six use cases: 8–10 weeks.

## Security / Positioning Notes
- Local-first/self-hosted posture: data, financial records, and documents stay in Altmark's building.
- Altmark owns everything; no vendor lock-in or SaaS dependency.
- AI calls are controlled/sanitized; minimum necessary data sent.
- Human-in-the-loop for sensitive/financial actions.
- Full audit trail for workflow actions.

## Immediate Next Actions
- 2026-07-02: finish setting up Conductor on Beelink.
- 2026-07-02: follow Danny's guide and configure everything needed for the rent delinquency bot.
- 2026-07-02: run Fable final playbook review before deploy/payment closeout.
- Update Client OS proof/payment gates to reflect insurance workflow live + paid.
- For rent delinquency: synthetic testing is complete; use `proof-assets/redacted-sample-request-and-cutover-gate-2026-05-30.md` to request/confirm the redacted Altmark sample export and live-sample prerequisites with Yair.
- 2026-06-06: Plan Review Pack applied to the rent delinquency gate at `proof-assets/rent-delinquency-plan-review-pack-2026-06-06.md`; use it to review source report, reviewer, cadence, exception rules, and proof boundary before first Altmark sample run.
- 2026-05-29 synthetic dry-run passed: see `client-os/outputs/rent-delinquency-synthetic-smoke-test-log-2026-05-29.md` and `client-os/outputs/rent-delinquency-synthetic-smoke-test-output-2026-05-29.csv`. First Altmark sample remains review-only until source/export/reviewer/exception gates clear.
- Capture proof-safe evidence from the live insurance workflow: redacted screenshots, run logs, acceptance wording, and before/after workflow summary.
- DHCR Lease Renewal Automation proposal has been reviewed. Use `proof-assets/dhcr-kickoff-command-sheet-2026-05-27.md`, `client-os/acceptance-checklist-dhcr-lease-renewal.md`, and `runbooks/dhcr-lease-renewal-workflow.md` after rent delinquency deployment/testing or if Altmark explicitly pulls this forward.
- Prepare support/maintenance/retainer path after the second workflow proves stable.
- 2026-05-22 Friday command sheet prepared: `proof-assets/friday-command-sheet-2026-05-22.md`. Use it to separate acceptance/payment proof capture from the HTTPS/Google OAuth reliability work.
- 2026-05-23 weekend command sheet prepared: `proof-assets/weekend-command-sheet-2026-05-23.md`. Treat acceptance/payment/access confirmation as the top move before HTTPS/OAuth migration.
- 2026-05-23 nightly closeout added Monday execution assets: `proof-assets/monday-closeout-sheet-2026-05-25.md` and `proof-assets/referral-readiness-gate-2026-05-23.md`.
- 2026-05-25 nightly added Tuesday branch sheet: `proof-assets/tuesday-closeout-branch-sheet-2026-05-26.md`. Use it after the Monday closeout based on reply state: confirmed facts → update Client OS/proof gate; partial reply → one missing-field follow-up; no reply → short closeout bump. Keep HTTPS/OAuth migration and referral asks blocked until acceptance/access/payment facts are clear.
- 2026-05-27 nightly converted the DHCR Lease Renewal proposal into delivery assets: `proof-assets/dhcr-kickoff-command-sheet-2026-05-27.md`, `client-os/acceptance-checklist-dhcr-lease-renewal.md`, and `runbooks/dhcr-lease-renewal-workflow.md`. Phase 1 is legal-rent renewals only; preferential-rent renewals remain Phase 2.
- Capture proof asset after PC delivery + workflow acceptance: "local-first automation infrastructure for property/operations team with insurance-expiration workflow live."

## Strategic Expansion Opportunity
Yair mentioned he may be able to connect JT to ~15 other family offices in the NYC area that would likely be interested in similar automation systems.

End goal for Altmark:
1. Finish the proposed Altmark systems cleanly.
2. Convert Altmark into monthly support/maintenance retainer.
3. Keep building additional automation systems Altmark needs.
4. Work with Yair to package the Altmark implementation as a referral/case-study wedge into other NYC family offices.

Strategic implication: Altmark is not just project revenue. It is a beachhead client for a repeatable family-office automation offer.

## 2026-05-13 Client OS Hardening
- Added proof-safe acceptance checklist for insurance expiration workflow: `client-os/acceptance-checklist-insurance-expiration.md`.
- Added reusable IP log: `client-os/reusable-ip-log.md`.
- Added explicit raw/cleaned/output privacy boundaries under `client-os/`.
- Current blocker remains unchanged: PC/access path, workflow acceptance, and payment/deposit clarity must be confirmed before proof/referral push or next build.
