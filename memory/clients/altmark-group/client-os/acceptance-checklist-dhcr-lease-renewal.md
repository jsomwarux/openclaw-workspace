# Acceptance Checklist — DHCR Lease Renewal Automation Phase 1

Client: Altmark Group
Workflow: DHCR Lease Renewal Automation, Phase 1 legal-rent renewals only
Prepared: 2026-05-27
Source: `memory/clients/altmark-group/dhcr-lease-renewal-proposal-review-2026-05-26.md`

## Scope Confirmation
- [ ] 50% kickoff payment received: $1,750
- [ ] Phase 1 confirmed as legal-rent renewals only
- [ ] Preferential-rent renewals explicitly excluded or flagged for Phase 2
- [ ] Approved recipient(s) confirmed for generated form emails
- [ ] Current RGB rates confirmed and entered into configurable settings
- [ ] Sample completed RTP-8 reference stored privately

## Source Data Readiness
- [ ] Command center spreadsheet template created
- [ ] Matt populated required tenant/unit/property fields
- [ ] DHCR Rent Roll report available for every included property
- [ ] Current rent roll/current deposits reconciled against DHCR source
- [ ] Legal-rent vs preferential-rent status is present for every unit
- [ ] Entity-name mapping by property reviewed
- [ ] Blank/invalid/ambiguous rows route to exception list instead of PDF generation

## Calculation Accuracy
- [ ] 1-year renewal calculation verified: legal rent × (1 + 1-year RGB rate)
- [ ] 2-year standard calculation verified: legal rent × (1 + 2-year RGB rate)
- [ ] 2-year stacked calculation verified when split-year RGB rules apply
- [ ] Additional security deposit calculation verified
- [ ] Zero/negative additional deposit case handled cleanly
- [ ] RGB rates editable without code changes
- [ ] Test cases include at least one normal row, one missing-field row, one preferential-rent row, and one edge-date row

## PDF / Form Generation
- [ ] RTP-8 PDF fields mapped for tenant name, address, apartment, entity, lease dates, rent options, security deposit, and computed fields
- [ ] Generated sample forms match Matt's reference expectations
- [ ] Preferential-rent rows do not generate Phase 1 forms
- [ ] File names are consistent and non-ambiguous
- [ ] Generated PDFs are stored/sent only through approved private channels

## Automation Behavior
- [ ] Daily scan identifies leases reaching 120-day generation window
- [ ] Generated forms are emailed to Matt with same-day summary
- [ ] Google Sheet `form generated date` writes back correctly
- [ ] `form sent date` is manually updateable without breaking the workflow
- [ ] 95-day reminder identifies generated-but-not-sent forms
- [ ] Weekly 150-day digest lists upcoming expirations and status
- [ ] Workflow logs include run result, generated count, skipped count, and exception count

## Human Review Boundary
- [ ] Matt confirms he reviews every generated form before mailing
- [ ] Workflow does not send forms to tenants
- [ ] Workflow does not interact with AppFolio
- [ ] Workflow does not countersign or make legal decisions
- [ ] Exception cases are visible for human resolution

## Handoff / Support
- [ ] Runbook created or updated for trigger, config, spreadsheet columns, failure modes, and rollback
- [ ] Owner knows how to update RGB rates annually
- [ ] Owner knows how to mark forms sent
- [ ] Backup/export path documented for spreadsheet and generated forms
- [ ] Open issues logged with owner/date
- [ ] Matt/Yair gives written approval for production use
- [ ] Final 50% payment requested/received after approval: $1,750

## Proof Boundary
- [ ] Any screenshots/logs used for proof are redacted or synthetic
- [ ] No tenant names, unit numbers, legal rent values, deposits, or property-specific sensitive details are shared publicly
- [ ] Public case-study/referral wording stays anonymized unless Altmark gives explicit permission
