# Altmark Rent Delinquency — Redacted Sample Risk Gate

Created: 2026-05-30

Purpose: tighten the first real-report sample gate after the synthetic dry run, before any Altmark tenant data or tenant-facing draft path is used.

## Current Delivery State
- Synthetic smoke test passed on 2026-05-29: 8 rows processed; 1 included, 4 manual review, 1 excluded, 2 cleanup, 0 unclassified.
- Safety result: no tenant-facing draft was generated for manual-review, excluded, or cleanup rows.
- Current blocker is not workflow logic. It is real source-report shape and approval context.
- Next client ask remains: redacted sample export with columns intact, source report path/export process, refresh cadence, named reviewer, and confirmed exception rules.

## Official Process Signals Checked
- NY Courts says nonpayment proceedings are for unpaid rent and, before starting a case, the landlord must first demand that the tenant pay rent or move out. Source: https://www.nycourts.gov/node/56731
- NY Courts NYC Housing guidance says a rent demand must be written and delivered at least 14 days before the court case is started. Source: https://ww2.nycourts.gov/COURTS/nyc/housing/startingcase.shtml
- NY Courts notes payment can be a defense in a nonpayment case, and full payment before the court date can end the case. Source: https://www.nycourts.gov/help/homes-evictions/common-defenses-landlord-tenant-case
- NY Courts guidance on nonpayment stays says later full payment can affect warrants before actual eviction. Source: https://www.nycourts.gov/new-york-city-housing-court/stays-after-entry-judgment-nonpayment-proceeding
- NY HCR notes rent-stabilized tenants can file overcharge complaints and DHCR may order rent reduction/refund when overcharge is found. Source: https://hcr.ny.gov/rent-increases-and-rent-overcharge

## Risk Translation For The First Redacted Sample
Do not treat a balance-only delinquency row as outreach-ready. A redacted sample needs enough fields to separate ordinary unpaid-rent candidates from records that require human review.

Required sample indicators:
- report date and balance as-of date
- last payment date and payment-after-report marker if available
- payment plan, dispute, legal/process, prior demand/case/notice, credit/prepayment, missing contact, and special-handling markers
- source system/report name and refresh cadence
- owner/reviewer for each output queue

Default routing:
- `included`: only clear delinquency candidate, no sensitive flags, required fields present, and no post-report payment ambiguity
- `manual_review`: payment plan, dispute, prior demand/case/notice, legal/process-sensitive, recent payment, payment-after-report, special handling, or unclear reviewer state
- `excluded`: credit/prepayment/negative balance or explicit exclusion marker
- `cleanup`: missing required fields, malformed dates/amounts, missing contact when outreach drafts are in scope

## Cutover Guard
The first Altmark real-report run should remain review-only. If any legal/process-sensitive, disputed, payment-plan, recent-payment, post-report-payment, credit/prepayment, or missing-required-field row enters the normal outreach-ready queue, stop and revise the rules before continuing.

## Proof Boundary
This note is internal client-delivery control, not legal advice and not public proof. Public proof remains blocked until accepted client output exists and Altmark grants permission or anonymization terms.
