# AI Governance Readiness Audit — Rent Delinquency Data Readiness Queue

Created: 2026-05-18 nightly autonomous leverage run  
Source case file: `memory/consulting/workflow-case-files/rent-delinquency-data-readiness-2026-05-18.md`

## 1. Executive Verdict

**Verdict:** Ready after cleanup.

This is a strong first AI operations workflow only if the team treats it as a readiness and approval queue first, not autonomous collections.

**Recommended first safe build:** rent delinquency data-readiness queue with blocked/ready/review-needed segmentation, reason codes, human approval, and audit logging.

**Primary blocker to fix first:** one approved source export with required fields, known ledger assumptions, blocked-row rules, and a named approval owner.

## 2. Workflow Scope

- **Workflow name:** Rent delinquency data-readiness queue
- **Business owner:** CFO, controller, property operations lead, or asset manager
- **Users / approvers:** reporting owner, property ops staff, manager/approver, final authorized sender if outreach is later approved
- **Source systems/files:** delinquency export, tenant ledger, payment-plan notes, contact file, manager exception notes
- **External parties affected:** tenants, guarantors, property managers, legal/compliance contacts if escalated

### What the system may do
- Ingest an approved source export.
- Validate required fields and schema.
- Flag stale, duplicate, missing, ambiguous, legal/dispute, do-not-contact, or payment-plan rows.
- Group rows into Ready / Blocked / Needs Review.
- Draft internal summaries and draft-only outreach from verified data.
- Log source row, reason codes, draft, reviewer, approval status, and timestamp.

### What the system must never do
- Send tenant-facing messages without human approval.
- Make legal/compliance decisions.
- Update financial records or ledgers.
- Trigger payments, transfers, or account changes.
- Override do-not-contact/legal/dispute/payment-plan holds.
- Invent balances, last-payment dates, tenant context, or collection language not supported by source data.

## 3. Readiness Scorecard

| Area | Score | Notes |
|---|---:|---|
| Source data reliability | 2/5 | The workflow is valuable precisely because delinquency exports can be stale or require ledger cleanup. Launch requires an approved sample export. |
| Field/format consistency | 3/5 | CSV/export-first can work, but schema drift and notes outside structured fields are likely. |
| Exception clarity | 3/5 | Core exceptions are clear: missing, stale, duplicate, payment plan, legal/dispute, do-not-contact, ambiguous unit/contact. Client-specific rules still need confirmation. |
| Approval path clarity | 2/5 | Must name the manager/approver, backup owner, and final sender before pilot. |
| PII/financial/sensitive-data exposure | 5/5 risk | Tenant names, balances, ledgers, contact info, and collection context are sensitive. Local-first/client-owned storage is strongly preferred. |
| Human review feasibility | 4/5 | A readiness queue is reviewable if it shows source row, reason code, draft, and approval controls in one place. |
| Logging/auditability | 4/5 | Easy to design into the first build; mandatory before pilot. |
| Rollback/manual fallback | 4/5 | Manual spreadsheet review remains the fallback; automation can be paused safely if no source-system writes or sends occur. |
| Business value/frequency | 4/5 | High buyer relevance for property/family-office operators if delinquency review happens weekly/monthly and consumes manager trust/time. |
| Implementation complexity | 3/5 | Moderate. Validation/queue is manageable; source-system integration and tenant messaging should stay out of v1. |

## 4. AI Boundary Map

| Bucket | Actions |
|---|---|
| Can automate | Report ingest, schema validation, field normalization, aging calculation from source date, reason-code assignment, Ready / Blocked / Needs Review queue creation, internal summary generation, audit-log writes. |
| Can draft | Internal cleanup notes, manager summaries, draft-only outreach for rows that pass readiness checks, follow-up task descriptions. |
| Must approve | Any tenant-facing draft, balance/payment-plan language, escalation, final ready-for-outreach decision, source-system status update, legal/dispute exception handling. |
| Must not automate | Payments, transfers, legal/compliance decisions, ledger/source-record edits, autonomous tenant outreach, deletion of records, sensitive commitments, bypassing collection policy or do-not-contact holds. |

## 5. Failure Modes and Guardrails

| Failure mode | Detection | Response / guardrail |
|---|---|---|
| Missing/malformed source file | File absent, wrong type, unreadable, required columns missing | Fail closed; notify reporting owner; no queue or draft output. |
| Row count or schema change | Row count swings outside agreed threshold or columns renamed/removed | Pause run; require owner approval of new export/schema. |
| Duplicate record / ambiguous tenant or unit | Same tenant/unit appears with conflicting balances/status | Route to Needs Review; no external draft. |
| Low-confidence extraction | OCR/PDF parsing uncertainty or notes parsing ambiguity | Mark low confidence; show source excerpt; require manual review. |
| Stale data | Source export older than allowed window or last-payment date conflicts with report date | Route to Needs Review; require fresh export. |
| Hallucinated or unsupported text | Draft references facts not present in verified row/template | Template-lock draft; show source fields; require approval; reject unsupported claims. |
| Wrong recipient / sensitive detail leakage | Missing/ambiguous contact, legal/dispute/do-not-contact flag, payment-plan ambiguity | Block row; no tenant-facing draft; manager review only. |
| Integration/API failure | Queue/log write fails or downstream service unavailable | Stop before external action; keep source export; alert owner; manual fallback. |
| Human approval not received | Draft remains pending beyond approved window | Expire draft; require fresh source data before approval/send. |

## 6. Acceptance Criteria

Before launch:
- [ ] Approved source sample exists and is stored under client-approved handling rules.
- [ ] Required fields are documented: property/unit/tenant identifier, balance, aging/days late, last payment, contact, notes/payment plan, hold flags, approval status, source date.
- [ ] Golden test case passes.
- [ ] Missing, duplicate, stale, legal/dispute, payment-plan, and do-not-contact failure cases route safely.
- [ ] Human approval screen/review path is accepted by the business owner.
- [ ] Audit log writes source row ID/date, reason code, draft, reviewer, decision, and timestamp.
- [ ] Error branch fails closed and does not send or update external systems.
- [ ] Manual fallback is documented.
- [ ] Owner and backup owner are named.
- [ ] Pilot go/no-go captured from client.

## 7. Pilot Plan

- **Scope:** 1–2 week pilot using one approved export format and synthetic/redacted test data before any real tenant-facing draft process.
- **Pilot users:** reporting owner, manager/approver, one ops reviewer.
- **Success metrics:** percent of rows classified; number of blocked rows with clear reason; approval turnaround; manual corrections; false-ready rows; false-blocked rows; user trust score after review.
- **Excluded scope:** autonomous sends, source-system writeback, legal/dispute automation, payments/transfers, broad tenant communication rules, multi-property schema variants until v1 passes.
- **Cadence:** daily review during first export cycle; weekly owner review after pilot.
- **Go/no-go for expansion:** expand only after two clean cycles with stable schema, accepted approval queue, no high-severity failure, and clear owner comfort.

## Recommendation
Verdict: Ready after cleanup  
First safe build: rent delinquency data-readiness queue with reason codes, draft-only outputs, human approval, and audit logs.  
Do first: approve one clean sample export and define blocked-row rules, approval owner, backup owner, and manual fallback.  
Do not do yet: automate tenant outreach, edit ledgers/source systems, make legal/dispute decisions, or build against dirty reports.  
Expansion trigger: two clean reporting cycles with stable schema, passed failure tests, logged approvals, and manager acceptance.
