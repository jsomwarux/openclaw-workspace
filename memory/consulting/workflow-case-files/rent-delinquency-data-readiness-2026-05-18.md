# Workflow Case File — Rent Delinquency Data Readiness Queue

Created: 2026-05-18 nightly autonomous leverage run  
Purpose: validate the Implementation Intelligence System Phase 0 with one anonymized, buyer-safe property/family-office workflow case file.

## Data Handling / Redaction Protocol
- Client/workflow is treated as anonymized property/family-office context.
- No tenant names, account numbers, unit-specific balances, ledgers, private file paths, credentials, legal advice, or client-specific proof are included.
- Claims are labeled as verified, client-stated, inferred, unverified/TODO, or blocked.
- This file is reusable methodology; it is not public client proof.

## Case File Metadata
- **Workflow name:** Rent delinquency data-readiness queue
- **Client / anonymized label:** Property/family-office operations team
- **Industry / vertical:** Property management / family office
- **Business owner:** CFO, controller, property operations lead, or asset manager
- **Users / approvers:** Property ops staff, reporting owner, manager/approver, final sender if outreach is later approved
- **Date created:** 2026-05-18
- **Source materials reviewed:** `memory/content/bank/2026-05-17/ai-ops-teardown-rent-delinquency-readiness.md`; `memory/consulting/ai-ops-teardowns/2026-05-17-rent-delinquency-readiness.md`; `memory/clients/altmark-group/runbooks/rent-delinquency-data-readiness-checklist.md`; `skills/ai-governance-readiness/SKILL.md`
- **Sensitivity level:** High
- **External-action risk:** Draft-only until explicit approval; tenant-facing sends must require human approval and may require legal/client review.

## 1. Intake Summary
- **Business goal:** Create a safer queue that separates delinquency rows ready for review/outreach from rows blocked by dirty data, ambiguous status, payment plans, disputes, missing contacts, or approval gaps.
- **Current pain:** Teams want rent delinquency automation, but the report often cannot be trusted without ledger cleanup and human context.
- **Why now:** A dirty report can make automation dangerous: wrong balance, wrong recipient, stale status, or inappropriate outreach.
- **Frequency / volume:** Usually weekly or monthly; higher-volume operators may review daily during collection windows. Volume is unverified/TODO for each client.
- **Economic event:** Collection readiness, avoided tenant/vendor/client mistakes, saved review labor, reduced escalation risk.
- **Success definition:** Operators can see what is ready, what is blocked, why it is blocked, who owns cleanup/approval, and what happened after approval.
- **Constraints:** No autonomous tenant outreach; no legal/compliance decisions; no financial updates; source report and ledger assumptions must be approved before build.

## 2. Current-State Workflow Map

| Step | Actor | Tool/System | Input | Action | Output | Friction / Failure Mode |
|---|---|---|---|---|---|---|
| 1 | Reporting owner | Property system / ledger / spreadsheet | Delinquency report export | Exports current delinquency data | CSV/XLSX/PDF report | Export may be stale, missing fields, or based on uncleared ledgers. |
| 2 | Ops staff | Spreadsheet / inbox / notes | Report + tenant notes | Manually scans balances, days late, payment plan notes | Informal review list | Payment plans and exceptions may live outside the report. |
| 3 | Manager / approver | Spreadsheet / email / meeting | Review list | Decides who is safe to contact, who is blocked, and who needs research | Approved/blocked rows | Criteria may be implicit; owner/approval trail may be missing. |
| 4 | Staff / system draft-only | Templates / email draft / message draft | Approved clean rows | Drafts outreach or internal follow-up | Draft messages / task list | Wrong data can produce wrong message; tenant-facing language needs approval. |
| 5 | Approver | Review queue | Draft + source row + flags | Approves, edits, or rejects draft | Approved send / hold / correction task | Approval bottlenecks can leave stale drafts. |
| 6 | Staff / authorized sender | Email/SMS/portal/manual process | Approved draft | Sends or logs next action according to client policy | Communication/status update | External action must not occur without explicit approval and policy fit. |
| 7 | Ops owner | Log / audit trail | Action result | Records status, owner, timestamp, and follow-up | Audit log + next queue | Without logs, team cannot prove what happened or avoid duplicate follow-up. |

## 3. Systems, Data, and Access
- **Source systems/files:** Delinquency report export, tenant ledger, payment-plan notes, contact data, manager exception notes.
- **Destination systems/files:** Review queue, approval log, follow-up tracker, optional draft message queue.
- **Data fields required:** Property, unit, tenant identifier, balance, days late or aging bucket, last payment date, contact method, notes/payment plan flag, do-not-contact/legal/dispute flag, approval status, source report date.
- **Data quality issues:** Missing contacts, stale balances, duplicate tenants/units, partial ledger cleanup, ambiguous payment-plan status, notes outside report, inconsistent aging thresholds.
- **Access owner:** Reporting owner and property ops lead; named backup required before launch.
- **Local-first/client-owned storage need:** Strong. Tenant balances, ledgers, contacts, and collection context are sensitive.
- **Integration/API constraints:** CSV/export-first is safest. API or direct-system writeback should be excluded from the first build unless client explicitly approves and test cases pass.

## 4. Exceptions and Hidden Dependencies
- **Missing data:** Tenant/contact/last payment/payment-plan fields missing.
- **Malformed input:** Unexpected column names, PDF exports, merged cells, blank rows, currency formatting issues.
- **Duplicate records:** Same tenant/unit across multiple rows, multiple leases, guarantor/roommate ambiguity.
- **Ambiguous owner/assignee:** No clear staff owner for cleanup or approval.
- **Stale data:** Report exported before recent payment or ledger correction.
- **Deadline/threshold changes:** Client changes outreach threshold, grace period, or aging bucket logic.
- **Human approval delays:** Drafts become stale if approval happens days after source report.
- **External party non-response:** Tenant/vendor response changes status but source report is not updated.
- **Legal/dispute/do-not-contact holds:** Any row with a hold must route to manual review and must not generate tenant-facing action.

## 5. Approval-Boundary Map

| Bucket | Actions |
|---|---|
| Can automate | Ingest report; validate schema; normalize fields; calculate aging from source date; flag missing/stale/duplicate rows; group rows by ready/blocked/review-needed; create internal summary; write audit log. |
| Can draft | Internal notes, manager summaries, cleanup requests, and tenant-facing message drafts for rows that pass readiness checks. |
| Must approve | Any tenant-facing message, balance/payment-plan language, escalation, status change in a source system, legal/dispute exception, or final ready-for-outreach decision. |
| Must not automate | Payments/transfers, legal/compliance decisions, account edits, source-ledger modifications, autonomous tenant outreach, irreversible deletes, sensitive commitments, or bypassing client collection policy. |

## 6. First Safe Build Recommendation
- **Recommended first build:** Rent delinquency readiness queue with blocked/ready/review-needed segmentation, approval notes, and audit logging. Draft outreach only after clean-row checks pass and only behind human approval.
- **Why this is safe enough:** The system starts by validating data and routing exceptions instead of contacting tenants or editing financial records.
- **Why this creates value:** It reduces manager uncertainty and exposes cleanup work before automation creates risk.
- **Excluded scope:** Autonomous sends, legal/dispute handling, source-system writeback, payment actions, final collections decisioning.
- **Human approval step:** Manager reviews source row, flags, draft, and audit trail before any external action.
- **First prototype artifact:** Synthetic CSV + queue output showing Ready / Blocked / Needs Review rows with reason codes and approval owner.
- **Expansion trigger:** Two clean reporting cycles with approved sample export, stable schema, logged approvals, and no high-severity failure cases.

## 7. Golden + Failure Test Cases

| Case | Input | Expected Output | Risk Covered | Pass/Fail |
|---|---|---|---|---|
| Golden 1 | Clean row with tenant/unit/balance/days late/contact/last payment/no holds/source date | Ready for manager approval; draft internal/outreach text allowed only as draft | Happy path | TODO |
| Failure 1 | Missing contact or missing tenant identifier | Blocked: missing required field; cleanup owner assigned; no draft | Missing data | TODO |
| Failure 2 | Duplicate tenant/unit rows with different balances | Needs Review: duplicate/ambiguous balance; no draft | Duplicate/ambiguous owner | TODO |
| Failure 3 | Row has legal/dispute/do-not-contact note | Blocked: sensitive hold; manual review only; no outreach draft | Wrong-recipient/sensitive/legal risk | TODO |
| Failure 4 | Last payment date after report date or source file older than allowed window | Needs Review: stale/inconsistent source; no external action | Stale data | TODO |
| Failure 5 | Payment plan appears in notes but no structured flag exists | Needs Review: payment-plan ambiguity; manager approval required | Hidden dependency | TODO |

## 8. Launch Acceptance Checklist
- [ ] Source sample approved
- [ ] Field/schema assumptions documented
- [ ] Golden cases pass
- [ ] Failure cases route safely
- [ ] Human approval screen/review path accepted
- [ ] Audit log writes correctly
- [ ] Error branch tested
- [ ] Manual fallback documented
- [ ] Owner/backup owner named
- [ ] Client signoff or pilot go/no-go captured

## 9. Rollback / Manual Fallback
- **Pause/kill switch:** Disable scheduled ingest; mark queue read-only; route to manual spreadsheet review.
- **Manual process if automation fails:** Use latest approved export and checklist; manually mark Ready / Blocked / Needs Review with reason codes.
- **Recovery owner:** Reporting owner + manager/approver.
- **Escalation path:** Any legal/dispute/do-not-contact/payment-plan ambiguity goes to manager/client policy owner, not automation.
- **Data restore/reconciliation need:** Preserve source export hash/name/date and action log; reconcile status changes against next approved report.

## 10. Runbook Skeleton
- **What it does:** Validates delinquency report readiness and creates an approval-safe exception queue.
- **When it runs:** On approved source export cadence; recommended manual trigger or scheduled after report generation.
- **Who owns it:** Reporting owner; backup owner required.
- **Where outputs go:** Internal queue/dashboard + audit log; no external sends by default.
- **How to review/approve:** Approver reviews source row, reason codes, draft, and flags; approves/edits/rejects with timestamp.
- **Common errors:** Missing field, schema drift, duplicate tenant/unit, stale report, legal/dispute hold, payment-plan ambiguity.
- **How to pause/restart:** Pause ingest/scheduler; restart only after source sample and schema are reconfirmed.
- **Who to contact:** Client operations owner first; JT/support only after source export owner confirms report is valid.

## 11. Post-Launch Review Notes
- **Date reviewed:** TODO
- **Actual usage:** TODO
- **Errors/failures:** TODO
- **Manual overrides:** TODO
- **User confusion:** TODO
- **Approval bottlenecks:** TODO
- **Recommended iteration:** TODO
- **Retainer/support opportunity:** Weekly exception review, report cleanup support, expansion into owner reporting or insurance/COI expiration queues after acceptance.

## 12. Lessons Captured
- **Discovery lesson:** Delinquency automation is mostly a data-readiness and approval-boundary problem before it is a messaging problem.
- **Governance/risk lesson:** Tenant-facing actions, balances, and collection language belong behind explicit approval and client policy boundaries.
- **Build lesson:** Deterministic validation and reason codes should do the first pass; LLMs can draft explanations only from verified fields.
- **Testing lesson:** Failure cases matter more than the happy path because the risky rows are exactly where automation can cause harm.
- **Handoff/runbook lesson:** The client needs a visible manual fallback and source-report owner, not just a running workflow.
- **Client communication lesson:** Sell the safer queue, not autonomous collections.

## 13. Reusable Patterns Extracted

| Pattern | Reusable Trigger | Inputs | Outputs | Guardrails | Where to add |
|---|---|---|---|---|---|
| Readiness-before-outreach queue | Any workflow where bad source data could trigger wrong customer/vendor/tenant communication | Report export, required fields, notes, hold flags, approval owner | Ready / Blocked / Needs Review queue with reason codes | No external action without approval; stale/ambiguous rows blocked | `memory/consulting/implementation-pattern-library.md` |
| Dirty-report reason codes | CSV/export-heavy ops workflows with manual cleanup | Source report + schema assumptions | Standard reason-code taxonomy: missing, stale, duplicate, ambiguous, hold, payment-plan | Reason codes must be visible to approver and logged | `memory/consulting/implementation-pattern-library.md` |
| Draft-only sensitive communication | Collections, vendor exceptions, owner reports, or finance-adjacent workflows | Verified row + approved template + recipient context | Draft message plus source evidence | Human approves final text and send; no legal/financial commitments | `memory/consulting/implementation-pattern-library.md` |

## Recommendation
Verdict: Ready after cleanup  
First safe build: Rent delinquency readiness queue with synthetic sample data, reason codes, and human approval path.  
Do first: Get one approved source export and define required fields, blocked-row rules, owner, and approval path.  
Do not do yet: Do not automate tenant outreach, source-system updates, legal/dispute decisions, payment actions, or build against dirty ledgers.  
Expansion trigger: Two clean reporting cycles with stable schema, approved sample export, passed failure tests, and manager acceptance of the approval queue.
