---
name: ai-governance-readiness
description: Create a practical AI governance/readiness audit for SMB consulting prospects or clients before building an AI workflow, agent, automation, or diagnostic. Use when JT needs an implementation-safety checklist, client-ready readiness audit, approval-boundary map, rollout guardrails, or risk review for AI operations work, especially property management, family office, construction, wholesale, skilled trades, HubSpot/Salesforce/n8n workflows, or local-first systems.
---

# AI Governance Readiness Audit

Use this to turn “we should use AI” into a controlled implementation plan an operator, CFO, controller, owner, or ops lead can trust.

Default buyer frame: **control, approval, audit trail, and rollback** — not policy theater.

## Core output

Produce a client-ready audit with these sections:

1. **Executive verdict**
   - `Ready`, `Ready after cleanup`, or `Not ready yet`
   - 1-sentence reason
   - recommended first safe build, or the blocker to fix first

2. **Workflow scope**
   - workflow name
   - business owner
   - users/approvers
   - source systems/files
   - external parties affected, if any
   - what the system may do vs must never do

3. **Readiness scorecard**
   Score each 1–5 and explain briefly:
   - Source data reliability
   - Field/format consistency
   - Exception clarity
   - Approval path clarity
   - PII/financial/sensitive-data exposure
   - Human review feasibility
   - Logging/auditability
   - Rollback/manual fallback
   - Business value/frequency
   - Implementation complexity

4. **AI boundary map**
   Use four buckets:
   - `Can automate`: deterministic steps, formatting, status checks, summaries from known data
   - `Can draft`: messages, notes, classifications, summaries requiring approval
   - `Must approve`: external sends, tenant/vendor/client-facing action, financial updates, record changes, escalations
   - `Must not automate`: payments, transfers, legal/compliance decisions, account credentials, irreversible deletes, sensitive client commitments

5. **Failure modes and guardrails**
   For each likely failure mode, define detection + response:
   - missing/malformed source file
   - row count or schema change
   - duplicate record / ambiguous owner
   - low-confidence extraction
   - stale data
   - hallucinated or unsupported text
   - wrong recipient / sensitive detail leakage
   - integration/API failure
   - human approval not received

6. **Acceptance criteria**
   Include concrete gates before launch:
   - sample export approved
   - golden test cases pass
   - redaction rules verified
   - human approval screen/review path accepted
   - audit log writes correctly
   - error branch tested
   - rollback/manual process documented

7. **Pilot plan**
   - first 1–2 week scope
   - pilot users
   - success metrics
   - excluded scope
   - daily/weekly review cadence
   - go/no-go condition for expansion

## Strong defaults for JT’s consulting lane

- Start with **exception queues**, not autonomous action.
- Prefer **local-first or client-owned storage** when workflows touch finance, tenants, vendors, property records, or internal files.
- LLMs should draft, summarize, classify, and explain. Deterministic rules should decide dates, thresholds, required fields, routing windows, and pass/fail checks.
- Every sensitive workflow needs a human approval step before anything leaves the business or changes a source system.
- Proof claims require measured evidence. Do not invent ROI, hours saved, record counts, or compliance outcomes.

## Property / family-office checklist

Extra checks for property management, real estate, and family-office workflows:

- Tenant/vendor names, balances, policy numbers, bank details, leases, ledgers, and owner reports are sensitive by default.
- Rent delinquency automation is readiness-gated: clean report, ledger assumptions, owner approval, message approval, and deposit/timing clarity before build work.
- Insurance/COI workflows are safer first builds because the system can flag expirations and prepare follow-ups without taking financial action.
- Never imply autonomous tenant outreach, collections action, payment action, or legal/compliance decisioning unless explicitly scoped and approved.

## Output style

Be direct and buyer-readable. Avoid generic governance jargon.

Use this tone:

> This workflow is a good first build, but not because AI is clever. It is a good first build because the source report is reliable, the exception rules are clear, and the risky action can stay behind a human approval step.

Avoid:
- “responsible AI framework” without concrete controls
- broad AI transformation language
- fake certainty
- unsupported security/compliance claims
- naming clients or using confidential details without permission

## Final recommendation format

End every audit with:

```markdown
## Recommendation
Verdict: [Ready / Ready after cleanup / Not ready yet]
First safe build: [specific workflow]
Do first: [single next action]
Do not do yet: [highest-risk premature move]
Expansion trigger: [what must be true before scaling]
```
