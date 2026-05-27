# Altmark DHCR Lease Renewal Automation — Proposal Review

Source: Attached PDF `Altmark_DHCR_Lease_Renewal_Proposal---7d6ffb15-c244-47b6-8246-a6a05e8af12b.pdf`; extracted text saved at `memory/clients/altmark-group/dhcr-lease-renewal-proposal-extracted.txt`.

## Executive Summary
Altmark requested a new DHCR lease renewal automation. This is the next workflow after the rent delinquency workflow is deployed. Phase 1 covers legal-rent renewals only for roughly 2/3 of rent-stabilized units, about 40 leases. Preferential-rent renewals are explicitly out of scope and should become Phase 2 after Phase 1 is live and validated.

Price: $3,500. Payment: 50% ($1,750) to start, 50% ($1,750) upon delivery and approval. Timeline: 1–2 weeks from kickoff to delivery, with command center spreadsheet template provided within 2 days of starting. After Matt populates tenant data, build/test can be completed within one week.

## Workflow Objective
Prevent missed DHCR/RTP-8 renewal timing and manual rent-calculation errors by automatically generating completed RTP-8 renewal lease PDFs from a command center spreadsheet, tracking generation/sent status, and reminding Matt before the 90-day statutory deadline.

## Scope — Phase 1 Legal Rent Renewals Only
- Daily automated scan of command center spreadsheet for upcoming lease expirations.
- At 120 days before expiration: generate completed RTP-8 Renewal Lease Form as a filled PDF.
- Calculate 1-year and 2-year renewal rent options using configurable RGB percentages.
- Support stacked 2-year increases for split-year RGB increases.
- Calculate additional security deposit required for each renewal option.
- Populate tenant information, owner/entity information, lease dates, and computed fields.
- Email completed forms to Matt with daily summary of all renewals generated.
- At 95 days before expiration: reminder for any forms not marked sent, with 90-day statutory deadline highlighted.
- Weekly summary digest of upcoming expirations in next 150 days, form status, and deadline tracking.
- Track renewal activity in Google Sheets: form generated date and form sent date.

## Explicit Non-Scope / Human Boundary
- Workflow does not send forms directly to tenants.
- Workflow does not interact with AppFolio.
- Matt reviews each form for accuracy, prints/mails to tenants, countersigns returned forms, and updates AppFolio.
- Preferential-rent units are out of Phase 1 and require Phase 2 because they need additional form fields, dual legal/preferential rent calculations, and a supplemental form.

## Inputs / Source of Truth
Command Center Spreadsheet maintained by Matt, combining DHCR Rent Roll and current rent roll data. Required fields:
- entity name
- property address
- apartment number
- tenant name
- apartment status
- legal registered rent
- current security deposit on file
- lease start date
- lease end date

Additional inputs needed:
- Current RGB rates confirmed. Proposal states current rates: 3.0% for 1-year, 4.5% for 2-year.
- Sample completed RTP-8 form, already provided.
- DHCR Rent Roll report for each property; proposal says already provided for 2490 3rd Ave.

## Outputs
- Filled RTP-8 renewal lease PDF per qualifying upcoming expiration.
- Daily email to Matt with completed forms + summary.
- 95-day reminder email for unmarked sent forms.
- Weekly 150-day upcoming expiration digest with status/deadline tracking.
- Google Sheets tracking columns: form generated date, form sent date.

## Calculation Logic
- 1-year renewal: Legal Rent × (1 + 1-year RGB rate).
- 2-year standard: Legal Rent × (1 + 2-year RGB rate).
- 2-year stacked: Legal Rent × (1 + year 1 rate) × (1 + year 2 rate).
- Additional security deposit: New legal rent minus current deposit on file.
- RGB rates must be configurable because Matt updates them annually.

## Acceptance Criteria
Phase 1 should not be considered delivered until:
1. Command center spreadsheet template is created and Matt can populate required fields.
2. Test data run generates RTP-8 forms for legal-rent units only.
3. Matt verifies sample forms for tenant/entity/property/lease-date/rent/security-deposit accuracy.
4. 120-day generation trigger works on sample or controlled production-like data.
5. 95-day reminder correctly identifies generated-but-not-sent forms.
6. Weekly 150-day digest lists upcoming expirations and statuses accurately.
7. Generated/sent tracking columns write back to Google Sheets without corrupting source data.
8. RGB rates are editable without code changes.
9. Preferential-rent units are excluded or clearly flagged out of Phase 1.
10. Matt confirms approval for delivery and production use.

## Key Risks / Edge Cases
- Incorrect legal registered rent or lease end dates in source spreadsheet will produce wrong forms.
- Preferential rent units accidentally included in Phase 1 could create incorrect renewal documents.
- Entity name varies by property; address always uses 2447 Third Ave, c/o Matt Grabina per proposal. This needs careful mapping.
- RGB rates change annually; hardcoding them would create maintenance risk.
- Stacked 2-year increases need exact DHCR/RGB rule confirmation each year.
- Security deposit calculation can be negative or zero if current deposit exceeds/equals new rent; handle gracefully.
- Blank tenant/property/lease fields should block form generation and route to exception list.
- Multiple tenants, vacancies, non-stabilized units, or status changes need clear inclusion/exclusion rules.
- Date window logic must handle weekends/holidays without missing 120/95/90-day deadlines.
- Email attachments may contain sensitive tenant info; keep delivery limited to approved recipient(s).

## Security / Privacy
Contains tenant names, lease dates, legal rents, security deposit amounts, property/entity data, and DHCR forms. Keep local-first where possible, avoid public proof with real tenant/property data, and use redacted/synthetic examples for content, portfolio, or referral material.

## Recommended Delivery Sequence After Rent Delinquency
1. Confirm kickoff/payment and Phase 1 only: legal rent renewals.
2. Create command center spreadsheet template within 2 days.
3. Matt populates required data.
4. Validate schema and identify exclusions/exceptions, especially preferential-rent units.
5. Build form-fill logic and RGB/config layer.
6. Build 120-day generation trigger, email summary, tracking writes.
7. Build 95-day reminder and weekly 150-day digest.
8. Run sample test forms for Matt review.
9. Fix calculation/form-field issues.
10. Production launch + runbook + support path.

## Mission Control Task Recommendations
- Altmark DHCR: kickoff + collect populated command center spreadsheet.
- Altmark DHCR: build/test legal-rent RTP-8 form generation.
- Altmark DHCR: implement 95-day reminder + weekly digest.
- Altmark DHCR: create acceptance test sheet and runbook.
- Altmark DHCR Phase 2: park preferential-rent renewal automation as future expansion after Phase 1 validation.

## Reusable IP / Proof Potential
Strong reusable family-office/property-ops proof angle: deadline-sensitive compliance workflow with human review, local data control, audit trail, and regulated document generation. Public proof must be anonymized; safest content angle is “deadline + exception tracking for regulated lease renewals,” not tenant specifics.
