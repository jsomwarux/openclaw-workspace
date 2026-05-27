# Runbook — DHCR Lease Renewal Automation Phase 1

Client: Altmark Group
Workflow: DHCR Lease Renewal Automation, legal-rent renewals only
Prepared: 2026-05-27

## Purpose
Generate review-ready RTP-8 renewal lease PDFs for legal-rent stabilized units before statutory renewal deadlines, while keeping Matt in control of review, mailing, countersignature, and AppFolio updates.

## Source Of Truth
Command center spreadsheet maintained by Matt.

Required columns:
- entity name
- property address
- apartment number
- tenant name
- apartment status
- legal registered rent
- current security deposit on file
- lease start date
- lease end date
- legal/preferential rent status
- form generated date
- form sent date
- exception/status notes

## Config Values
- 1-year RGB rate
- 2-year RGB rate
- stacked 2-year RGB rates when split-year increases apply
- approved email recipient(s)
- generation window: 120 days before lease expiration
- reminder window: 95 days before lease expiration
- weekly digest horizon: 150 days

Do not hardcode rates. Matt updates RGB rates annually.

## Workflow Logic
1. Scheduled scan reads command center spreadsheet.
2. Validate each row:
   - required fields present
   - legal-rent Phase 1 status confirmed
   - lease end date parseable
   - legal rent and security deposit numeric
3. Rows with missing/ambiguous/preferential data are skipped and added to exception list.
4. For rows at 120 days before expiration and not already generated:
   - calculate 1-year renewal rent
   - calculate 2-year renewal rent
   - calculate additional security deposit
   - populate RTP-8 PDF
   - email generated PDF(s) and summary to Matt
   - write `form generated date` back to sheet
5. At 95 days before expiration:
   - find generated forms without `form sent date`
   - email reminder with 90-day statutory deadline highlighted
6. Weekly:
   - send 150-day upcoming expiration digest with generated/sent/exception status

## Human Boundary
Matt reviews each generated form for accuracy, prints/mails to tenants, countersigns returned forms, and updates AppFolio.

The workflow must not:
- send forms directly to tenants
- interact with AppFolio
- include preferential-rent renewals in Phase 1
- generate forms from incomplete data
- make legal/compliance decisions without human review

## Test Cases
Before production, run a controlled test sheet with:
1. Normal legal-rent row with complete data
2. Row missing tenant or lease date
3. Preferential-rent row
4. Row with current deposit equal to or greater than new rent
5. Row inside 120-day window
6. Row inside 95-day reminder window with generated date but no sent date
7. Row outside all windows

Expected result:
- only valid legal-rent rows generate PDFs
- invalid/preferential rows appear in exception list
- reminders only trigger for generated-not-sent rows
- weekly digest includes all upcoming rows in 150-day horizon

## Failure Modes And Recovery
| Failure | Likely Cause | Recovery |
|---|---|---|
| No rows processed | Sheet permissions, renamed tab, empty data | Verify sheet URL/tab/access; run dry test. |
| Wrong rent values | Bad legal rent, wrong RGB config, preferential unit included | Stop generation, correct config/source data, regenerate affected forms only. |
| PDF fields misplaced | RTP-8 template mapping drift | Compare against Matt's sample, fix mapping, rerun controlled batch. |
| Emails missing attachments | PDF output path or email node error | Check workflow logs/output directory; resend to Matt only after verifying files. |
| Duplicate forms | Generated date not written/read | Use form generated date/idempotency key before generating. |
| Reminder noise | Sent date not maintained | Confirm Matt's marking process and sheet column validation. |

## Rollback
- Disable the scheduled trigger.
- Preserve the command center spreadsheet and generated PDFs.
- Do not delete generated files; mark superseded if re-generated.
- Notify Matt/Yair which rows/forms may need manual review.

## Acceptance
Use `client-os/acceptance-checklist-dhcr-lease-renewal.md` before delivery approval or final payment request.

## Proof-Safe Pattern
Anonymized reusable pattern: deadline-sensitive regulated document generation with exception routing, human review, and audit trail.
