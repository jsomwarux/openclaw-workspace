# Altmark Group — Client Status

Last updated: 2026-05-22

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
1. Insurance expiration workflow — just finished ($2,250 use case; final payment/approval status unknown)
2. Dedicated PC setup — done; to be delivered to Altmark office next week
3. Rent delinquency workflow — pending 50% deposit before work begins ($4,500 use case; deposit expected $2,250 if terms unchanged)

## Current Status
- Active client engagement.
- Insurance expiration workflow is finished.
- Dedicated PC for workflows was installed at Altmark's office on 2026-05-19. Capture handoff/access confirmation, acceptance wording, open issues, and payment/deposit clarity before referral or named proof use.
- Rent delinquency workflow is temporarily paused by client-side data readiness. On 2026-05-06, after JT asked whether Altmark had the updated rent delinquency tracker ready and was ready to move forward, Yair replied that Matt is away, the office has been overwhelmed, internal reporting still needs cleanup, and many tenant ledgers need cleanup before the delinquency report is accurate. Yair expects to pick it back up early next week.
- This is not a lost opportunity; it is a data hygiene/reporting blocker. Best next move is to help define the minimal clean input needed and keep momentum without starting build work before the report is reliable.

## Revenue / Payment Status
- Total proposed buildout: $34,750.
- Foundation Infrastructure Setup: $4,000, paid in full at kickoff per proposal.
- Insurance Expiration Tracking: $2,250; workflow finished, payment/approval status unknown.
- Rent Delinquency Outreach: $4,500; pending 50% deposit before work starts, expected $2,250 if terms unchanged.
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
- Confirm deposit/payment status.
- Prepare delivery checklist/runbook for dedicated PC handoff.
- Create runbook for insurance expiration workflow.
- For rent delinquency: use `runbooks/rent-delinquency-data-readiness-checklist.md` with Yair/Karen/Matt before build work begins. Required before starting: source report named, required fields present, ledger cleanup assumptions documented, edge cases flagged, cleaned sample export approved, and 50% deposit timing confirmed.
- Once ledger/report cleanup is ready and deposit arrives, begin rent delinquency workflow.
- 2026-05-22 Friday command sheet prepared: `proof-assets/friday-command-sheet-2026-05-22.md`. Use it to separate acceptance/payment proof capture from the HTTPS/Google OAuth reliability work.
- 2026-05-23 weekend command sheet prepared: `proof-assets/weekend-command-sheet-2026-05-23.md`. Treat acceptance/payment/access confirmation as the top move before HTTPS/OAuth migration.
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
