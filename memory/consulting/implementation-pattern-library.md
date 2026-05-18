# Implementation Pattern Library

Reusable consulting implementation patterns extracted from client-safe workflow case files. Use anonymized/synthetic examples only.

## Rent Delinquency Data Readiness — 2026-05-18

Source case file: `memory/consulting/workflow-case-files/rent-delinquency-data-readiness-2026-05-18.md`  
Governance audit: `memory/consulting/workflow-case-files/rent-delinquency-governance-readiness-audit-2026-05-18.md`

### Pattern: Readiness-before-outreach queue
- **Reusable trigger:** Any workflow where bad source data could trigger wrong customer/vendor/tenant communication.
- **Inputs:** Report export, required fields, notes, hold flags, approval owner.
- **Outputs:** Ready / Blocked / Needs Review queue with visible reason codes.
- **Guardrails:** No external action without approval; stale, missing, duplicate, legal/dispute, do-not-contact, or ambiguous rows route to review/blocked.
- **Best fit:** Property management, family office, wholesale customer follow-up, vendor compliance, AR follow-up, insurance/COI tracking.

### Pattern: Dirty-report reason codes
- **Reusable trigger:** CSV/export-heavy operations workflow with manual cleanup before action.
- **Inputs:** Source report, schema assumptions, allowed date window, required field list.
- **Outputs:** Standard taxonomy: missing, stale, duplicate, ambiguous, hold, payment-plan, low-confidence extraction, schema drift.
- **Guardrails:** Reason codes must be visible to the approver and written to the audit log.

### Pattern: Draft-only sensitive communication
- **Reusable trigger:** Collections, vendor exceptions, owner reports, tenant communications, or finance-adjacent workflows.
- **Inputs:** Verified row, approved template, recipient/contact context, approval owner.
- **Outputs:** Draft message plus source evidence and approval status.
- **Guardrails:** Human approves final text and send; no legal, financial, policy, or sensitive commitments generated automatically.
