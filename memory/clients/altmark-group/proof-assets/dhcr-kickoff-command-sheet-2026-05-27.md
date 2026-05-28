# Altmark DHCR Lease Renewal Automation — Kickoff Command Sheet

Date prepared: 2026-05-27
Source proposal review: `memory/clients/altmark-group/dhcr-lease-renewal-proposal-review-2026-05-26.md`

## Decision
Treat DHCR Lease Renewal Automation as the next paid workflow **after rent delinquency deployment/test acceptance**, unless Altmark explicitly prioritizes it earlier.

## Commercial Snapshot
- Phase 1: Legal-rent renewals only
- Price: $3,500
- Start payment: $1,750
- Final payment: $1,750 upon delivery and approval
- Timeline: 1–2 weeks from kickoff
- Command center spreadsheet template due: within 2 days of kickoff
- Phase 2: preferential-rent renewals, separately scoped after Phase 1 validates

## JT's Tomorrow Move
If rent delinquency status is stable enough to discuss the next workflow, send a short kickoff alignment note to Yair/Matt:

> For the DHCR lease renewal workflow, I’m going to keep Phase 1 tight: legal-rent renewals only, using Matt’s command center spreadsheet as the source of truth. Before I start, I need three things confirmed: populated spreadsheet owner/date, current RGB rates, and which properties/units are included in Phase 1. Preferential-rent units stay out of scope until Phase 2 so we don’t generate incorrect renewal forms.

## Inputs To Collect Before Build
| Input | Owner | Required? | Notes |
|---|---|---:|---|
| 50% kickoff payment | Yair / Altmark | Yes | $1,750 before build starts. |
| Populated command center spreadsheet | Matt | Yes | Required fields below. |
| Current RGB rates | Matt/Yair | Yes | Official NYC RGB Order #57 confirms 3.0% 1-year and 4.5% 2-year for leases commencing 2025-10-01 through 2026-09-30. Reconfirm before production use if any lease commencement falls outside that window. |
| Sample completed RTP-8 | Matt | Yes | Proposal says already provided. Store private; do not use in public proof. |
| DHCR Rent Roll for each property | Matt | Yes | 2490 3rd Ave already provided per proposal; confirm remaining properties. |
| Approved email recipient(s) | Matt/Yair | Yes | Forms contain tenant/legal rent data; do not widen recipients casually. |
| Phase 1 unit inclusion list | Matt | Yes | Legal-rent units only. Preferential-rent units excluded/flagged. |

## Command Center Spreadsheet Required Fields
- entity name
- property address
- apartment number
- tenant name
- apartment status
- legal registered rent
- current security deposit on file
- lease start date
- lease end date
- legal-rent vs preferential-rent flag/status
- form generated date
- form sent date
- exception/status notes

## Non-Negotiable Boundaries
- Do not send forms directly to tenants.
- Do not write to AppFolio.
- Do not include preferential-rent units in Phase 1 generation.
- Do not hardcode RGB rates.
- Do not generate a form when required fields are blank or ambiguous; route to exception list.
- Matt reviews/prints/mails/countersigns/updates AppFolio.

## Current Rate Source Check
- Verified 2026-05-27 against NYC Rent Guidelines Board Apartment/Loft Order #57.
- Applies to rent stabilized apartment leases commencing between 2025-10-01 and 2026-09-30.
- Phase 1 rate layer should store the effective date window with the rates, not just the percentage values.
- Source: https://rentguidelinesboard.cityofnewyork.us/2025-26-apartment-loft-order-57/

## Build Sequence
1. Confirm kickoff payment + Phase 1 scope.
2. Create command center spreadsheet template within 2 days.
3. Matt populates tenant/unit/property data.
4. Validate schema and produce exception list before any PDF generation.
5. Build configurable RGB rate layer.
6. Build RTP-8 PDF field mapping for legal-rent units.
7. Build 120-day generation trigger + daily Matt email summary.
8. Build generated/sent tracking writes back to Google Sheets.
9. Build 95-day reminder for generated-not-sent forms.
10. Build weekly 150-day upcoming expiration digest.
11. Run controlled test batch.
12. Matt verifies sample forms.
13. Launch production with runbook + support path.

## Acceptance Gate
Do not mark delivered until `client-os/acceptance-checklist-dhcr-lease-renewal.md` is green.

## Proof / Referral Angle
Reusable angle: deadline-sensitive regulated document workflow with exception tracking, human review, local/private data boundaries, and audit visibility.

Proof-safe phrasing only until permission exists:
> Built a local-first lease-renewal deadline workflow for a NYC property/family-office operator that generates review-ready renewal packets, flags exceptions, and keeps human approval before tenant communication.
