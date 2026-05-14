# Property / Family-Office AI Operations Offer

Created: 2026-05-13

## Positioning Statement

JT builds AI operations systems for property and family-office teams that need cleaner visibility into aging work, missed deadlines, owner/vendor exceptions, human approvals, and audit trails without replacing the systems they already use.

The wedge is not “AI for real estate.” The wedge is: **show operators what is expired, missing, blocked, changed, risky, or approval-ready before it becomes an owner-visible problem.**

Primary lane: NYC-area family offices, real estate operators, and property operations teams with sensitive back-office workflows across AppFolio, QuickBooks/Desktop-style tools, spreadsheets, inboxes, banking portals, vendor documents, and owner reports.

Adjacent expansion lanes: property management firms, insurance operations, private lending/admin teams, and asset-heavy SMBs where the same exception/approval/audit pattern applies.

## Buyer and Pain Definition

### Best buyer

- Principal, CFO/controller, director of operations, asset manager, family-office operator, or trusted internal admin who owns back-office follow-through.
- They are not looking for a new enterprise platform. They already have systems and reports, but the operational truth lives between them.
- They care about sensitive data, privacy, approval control, and whether the workflow will still be understandable after the consultant leaves.

### Pain they feel

They usually describe the pain as:

- “We track it manually.”
- “Someone has to remember to check that report.”
- “The owner asks and we scramble.”
- “The data is in AppFolio/QuickBooks/spreadsheets, but not in one place.”
- “We do not want AI sending anything without approval.”
- “We have reports, but nobody trusts them enough to automate from them yet.”

What that really means:

- Expiring items are discovered late.
- Exception ownership is unclear.
- Financial or tenant-facing work depends on memory and manual review.
- Sensitive workflows are too risky for generic SaaS automation.
- Reports exist, but data readiness is not strong enough for autonomous action.
- Leadership lacks a clean daily/weekly view of what changed, aged, or needs approval.

### Core problem JT solves

Property/family-office teams do not need “AI strategy” first. They need an **exception layer**:

- what is missing
- what is expiring
- what changed
- what is blocked
- who owns it
- what can be drafted
- what requires approval
- what happened, when, and by whom

## Diagnostic Scope

### Diagnostic name

**Property / Family-Office AI Operations Diagnostic**

### Diagnostic promise

In 5–7 business days, JT maps the highest-risk operational workflows, scores them for automation readiness, and recommends the first AI-enabled workflow worth building.

The output is not a list of AI ideas. It is a practical implementation plan with source systems, failure points, human approval boundaries, data-readiness gaps, and a first-build scope.

### Workflows inspected

Prioritize 2–4 workflows from this list:

1. Insurance / COI / vendor-document expiration tracking
2. Rent delinquency readiness and approved outreach prep
3. Owner/vendor exception dashboard
4. Loan/debt deadline tracking
5. QuickBooks/bank/cash-risk review queues
6. Owner-ready weekly exception brief
7. Maintenance/vendor follow-up visibility
8. Report aging: what reports get pulled, reviewed, ignored, or manually reconciled

### Diagnostic activities

- Current-state workflow map: trigger, owner, source data, review path, approval path, output.
- Source-system inventory: AppFolio, QuickBooks, spreadsheets, inboxes, folders, banking exports, vendor documents, tenant ledgers, owner reports.
- Exception inventory: overdue, missing, stale, duplicate, risky, ambiguous, owner-needed, approval-needed.
- Manual handoff map: where data is copied, exported, emailed, renamed, reviewed, or retyped.
- Human-in-loop design: what can be flagged, summarized, drafted, or queued vs. what must require approval.
- Data-readiness score: required fields, freshness, sample report quality, edge cases, trust level.
- First-build recommendation: workflow, acceptance criteria, timeline, dependencies, risks, and next proposal.

### Diagnostic boundaries

JT does not promise autonomous financial, tenant-facing, or external action from the diagnostic. The diagnostic identifies what is safe to build first and what must stay human-approved.

## Deliverables

### Diagnostic deliverables

1. **Workflow map**
   - Current-state flow for each inspected workflow.
   - Owner, trigger, input, review point, approval point, and output.

2. **Exception inventory**
   - The exact classes of work that age, expire, get missed, or need escalation.
   - Sorted by frequency, business risk, and ease of detection.

3. **Data-readiness review**
   - Source report/files available.
   - Required fields.
   - Known messy rows and edge cases.
   - What must be cleaned before automation.

4. **Ranked first-build list**
   - Top 3 candidate workflows scored by impact, implementation complexity, data readiness, approval risk, and proof value.

5. **Human approval + audit design**
   - What the system may do automatically.
   - What it may only draft.
   - What requires explicit approval.
   - What gets logged.

6. **First workflow implementation brief**
   - Recommended first build.
   - Inputs/outputs.
   - Acceptance criteria.
   - Timeline.
   - Dependencies.
   - Fixed-scope proposal range.

### Implementation deliverables after diagnostic

For the first workflow build, deliver:

- Local-first or client-controlled workflow where appropriate.
- Source report/file ingestion.
- Exception detection rules.
- Operator review queue or dashboard.
- Daily/weekly summary.
- Drafted actions/messages where appropriate.
- Approval step before sensitive action.
- Audit log with status, timestamp, source, reviewer/approver, and action.
- Runbook for operating the workflow.
- Dry-run period before live use.
- Acceptance checklist.

## 3 Packaged First Workflows

## 1. Insurance Expiration Exception Layer

### Buyer pain

Insurance certificates, COIs, vendor documents, and policy dates live across spreadsheets, folders, inboxes, and staff memory. The team only notices a problem when something is already expired or an owner/vendor asks.

### First-build scope

A workflow that scans a source spreadsheet/report/folder on a schedule, flags upcoming and overdue expirations, prepares follow-up drafts, and logs status changes.

### Inputs

- Insurance/COI tracking spreadsheet or export
- Vendor/tenant/property records
- Document folders or inbox attachments if available
- Approved follow-up templates

### System behavior

- Normalize property, tenant/vendor, document type, expiration date, owner, and status.
- Flag 30/14/7-day upcoming expirations.
- Flag overdue, missing, malformed, and duplicate records.
- Draft follow-up messages from approved templates.
- Route follow-ups for human approval.
- Produce daily/weekly exception summary.
- Log every detected exception, draft, approval, sent status, and timestamp.

### Acceptance criteria

- Operator can see every upcoming and overdue expiration in one review path.
- Exceptions are grouped by urgency and owner.
- Follow-up drafts are prepared but not sent without approval.
- Audit log shows source, status, reviewer, and action.
- Dry-run matches manual review on a sample period before live use.

### Why this is the best first workflow

It is low-risk, visible, repeatable, and concrete. It proves the exception-layer concept without touching financial transfers or tenant-facing decisions.

## 2. Rent Delinquency Readiness Queue

### Buyer pain

Rent delinquency automation sounds valuable, but the source data is often not clean enough. Ledgers may be stale, payment plans may live in notes, balances may need review, and outreach should never go out from dirty data.

### First-build scope

A readiness queue that ingests delinquency reports, validates rows, separates “ready for draft” from “needs review,” prepares approved outreach drafts only for clean rows, and logs every decision.

### Inputs

- AppFolio/Buildium/Rent Manager/Yardi export or ledger report
- Tenant/property/unit fields
- Balance, aging, last payment, payment plan, notes, contact info
- Approved outreach templates
- Internal rules for exclusions and review-required cases

### System behavior

- Validate required fields.
- Flag stale, missing, duplicate, inconsistent, or edge-case rows.
- Separate accounts into:
  - ready for approved outreach draft
  - needs ledger review
  - payment-plan exception
  - missing contact/source issue
  - do-not-contact/manual review
- Draft messages only for clean rows.
- Require approval before any message leaves the business.
- Log amount, source report date, draft, reviewer, approval, and status.

### Acceptance criteria

- No outreach draft is created from incomplete or untrusted rows.
- Review-needed rows are visible with a reason, not buried in the export.
- Operator can approve or reject drafts from a clear queue.
- Every row has a status and audit trail.
- Workflow makes collections safer before it makes collections faster.

### Why this is a strong second workflow

It demonstrates judgment. Many consultants would rush to “AI writes the tenant email.” JT’s angle is better: **validate the operational record first, then draft only from clean data with approval.**

## 3. Owner / Vendor Exception Dashboard

### Buyer pain

Owners and operators do not need another static report. They need a weekly view of what changed, what aged, which vendors are blocked, which documents are missing, which approvals are waiting, and what needs escalation.

### First-build scope

A dashboard and summary workflow that consolidates owner/vendor exceptions from approved source reports and produces a clean operational review queue.

### Inputs

- Vendor follow-up spreadsheet
- Maintenance/vendor status reports
- Owner request logs
- Document expiration lists
- Loan/deadline trackers
- Email labels/folders where appropriate
- Approved escalation categories

### System behavior

- Pull from defined source reports/files.
- Flag aged, blocked, missing, changed, and approval-needed items.
- Group exceptions by property, owner, vendor, workflow, age, and severity.
- Produce owner/operator summary.
- Keep status changes and notes in an audit trail.
- Draft internal follow-up tasks or messages for approval.

### Acceptance criteria

- Operator can answer “what needs attention this week?” without manually rebuilding a report.
- Exceptions have owners, ages, and next actions.
- Dashboard avoids vanity metrics and focuses on stuck work.
- Sensitive or external actions remain approval-based.
- Weekly review becomes a repeatable operating rhythm.

### Why this expands the account

Once one workflow works, the buyer usually wants the same visibility pattern across more workflows. The dashboard becomes the operating layer for additional modules.

## Pricing Recommendation With Rationale

### Recommended pricing menu

1. **Paid Diagnostic: $2,500**
   - 5–7 business days
   - 2–4 workflows inspected
   - deliverables listed above
   - $1,250 credit toward a first workflow build if approved within 14 days

2. **Diagnostic + First Workflow Sprint: $8,500–$12,500**
   - diagnostic
   - one packaged workflow build
   - dry-run period
   - acceptance checklist
   - runbook
   - best for warm referrals where trust already exists

3. **First Workflow Build Only: $6,500–$10,000**
   - only when the workflow is already clear and source data exists
   - insurance expiration tends toward lower/mid range
   - rent delinquency readiness and dashboards tend toward mid/high range because approval logic and edge cases matter more

4. **Multi-Workflow AI Ops Layer: $18,000–$35,000**
   - foundation + 3–5 workflows
   - local/self-hosted setup where needed
   - dashboard/summary layer
   - audit logs and support handoff
   - 6–10 week delivery depending on systems and data readiness

5. **Support / Iteration Retainer: $750–$2,500/month**
   - monitoring
   - workflow changes
   - report format changes
   - edge-case handling
   - monthly exception review
   - additional small automations scoped separately

### Rationale

- Family-office/property buyers will not respect a cheap “AI audit.” The offer must feel serious enough to handle sensitive workflows.
- $2,500 is accessible for a referral-led diagnostic while still filtering tire-kickers.
- The first workflow needs enough budget for discovery, safe implementation, dry run, logging, approval design, and handoff.
- The real margin is expansion: once the exception/audit pattern works for one workflow, it can extend across documents, collections, owner reporting, bank/QuickBooks review, and vendor follow-up.
- Do not sell hourly unless the buyer already has a defined ongoing advisory relationship. Fixed-scope outcomes are cleaner.

## Sales Call Structure

### 1. Open with the workflow, not AI

Ask:

- “Which workflow causes the most last-minute scrambling right now?”
- “What gets missed if nobody remembers to check?”
- “What does the owner/operator ask for that takes too long to answer?”

Goal: make the conversation about operational failure points, not tools.

### 2. Identify the exception class

Ask:

- “Is the problem expiration, delinquency, missing documents, vendor follow-up, aging approvals, cash timing, or owner reporting?”
- “What does ‘bad’ look like when this workflow fails?”
- “How often do you find out too late?”

Goal: name the exception that the system should surface.

### 3. Map current source and owner

Ask:

- “What report or file tells the truth today?”
- “Who pulls it?”
- “Who reviews it?”
- “Where do the edge cases live?”
- “What would your team not trust AI to do?”

Goal: expose data readiness and approval boundaries.

### 4. Establish risk and approval boundaries

Ask:

- “What can be automatically flagged?”
- “What can be drafted?”
- “What must always require human approval?”
- “What should be logged for audit/history?”

Goal: reassure the buyer that this is not reckless autonomy.

### 5. Score the first build

Use the scoring logic:

- frequency
- business impact
- source data readiness
- implementation complexity
- approval risk
- proof value

Recommend one first workflow, not a menu of possibilities.

### 6. Close to diagnostic or sprint

Referral/warm buyer close:

> “The right next step is not a big AI project. I’d map the 2–4 workflows where things expire, age, or need approval, then pick the first safe build. If the data is clean enough, we can go straight from that into the first workflow sprint.”

Skeptical buyer close:

> “If the reports are not ready, the diagnostic will tell you that before you spend implementation money. That is the point.”

## Objection Handling

### “We already use AppFolio / QuickBooks / [system].”

Good. This is not a replacement. The offer sits around the tools you already use and turns reports/files into a clearer exception queue: what changed, what is missing, what is overdue, what needs approval.

### “Our data is messy.”

That is exactly why the diagnostic comes first. Messy data does not mean no automation. It means the first workflow may need to be a readiness queue, not an autonomous action flow.

### “We do not want AI sending messages.”

It should not, at least not first. The safer version drafts, flags, summarizes, and routes for approval. Human approval and logs are part of the design.

### “We handle this manually already.”

Manual is fine until the work ages silently. The value is not replacing the person. It is making the missed, expired, blocked, or approval-needed items visible before they become expensive.

### “Can our current software do this?”

Maybe partially. The question is whether it does it across your actual operating path: exports, spreadsheets, inboxes, document folders, approvals, and owner reporting. If the work still depends on someone remembering to check, there is a gap.

### “Is this secure?”

The right setup depends on the data. For sensitive property/financial workflows, JT can design local-first or client-controlled workflows, minimize data movement, avoid autonomous external actions, and keep audit logs.

### “What if the workflow breaks?”

The build should include dry-run mode, logs, error alerts, manual fallback, and a runbook. If a workflow cannot be safely operated when something changes, it is not ready to go live.

### “We need a bigger AI strategy.”

Start smaller. The fastest useful strategy is one workflow that proves how your business should handle exceptions, approvals, and audit trail. Then expand from that pattern.

### “Why not hire a developer?”

A developer can build what is specified. The harder part is knowing what should be built, what should not be automated, where the data is unreliable, and how the operator will actually approve and use it.

## Qualification / Disqualification Checklist

### Strong fit

- Real estate operator, family office, property operations team, private lending/admin team, or PM firm with operational complexity.
- Uses AppFolio, QuickBooks/Desktop-style tools, spreadsheets, inboxes, folders, banking portals, vendor/tenant reports, or owner reports.
- Has one clear workflow where missed/aged/expired work creates financial, compliance, owner, tenant, or vendor risk.
- Can provide sample reports/exports/files.
- Has a clear operator who owns the workflow.
- Accepts human approval for sensitive actions.
- Wants better visibility around existing systems, not a full software replacement.
- Budget exists for a serious diagnostic and implementation.

### Weak fit

- Buyer wants vague AI brainstorming with no workflow owner.
- No access to source reports, files, or exports.
- Workflow is low-frequency and low-impact.
- Buyer wants fully autonomous financial/tenant-facing action immediately.
- They expect AI to fix fundamentally unowned operations.
- They refuse to participate in data cleanup or approval design.
- They want a cheap chatbot demo, not an operational system.
- They are replacing core property/accounting software and need a platform selection project, not an exception layer.

### First-call qualification questions

1. What workflow do you check manually every week because missing it would hurt?
2. Where does the source data live?
3. Who owns the workflow today?
4. What happens when the workflow is missed?
5. What can be flagged automatically, and what needs approval?
6. Can you share a redacted sample report/export?
7. If this worked, what would you want to inspect next?

## Expansion Path After Diagnostic

### Phase 1 — Diagnostic

Map 2–4 workflows. Pick the first safe build. Identify data gaps and approval boundaries.

### Phase 2 — First workflow sprint

Build one narrow exception/approval workflow. Run dry-run mode. Validate against manual review. Deliver runbook and acceptance checklist.

### Phase 3 — Exception dashboard

Unify the first workflow into a broader operator view: overdue, missing, changed, approval-needed, owner/vendor-blocked, and next action.

### Phase 4 — Additional modules

Add adjacent workflows:

- insurance/document expirations
- rent delinquency readiness
- vendor follow-up
- loan/debt deadlines
- bank/QuickBooks review queue
- cash-risk alerts
- owner weekly exception brief

### Phase 5 — Operating cadence

Monthly review of:

- exceptions caught
- false positives
- report changes
- approval bottlenecks
- new workflow candidates
- owner-ready summaries

### Phase 6 — Referral proof package

After the client accepts the workflow and approves language, package a redacted proof asset:

- before/after workflow map
- screenshot of exception queue or logs with sensitive details removed
- acceptance quote/paraphrase if approved
- first metric if known
- expansion module menu

Do not claim time saved, revenue recovered, or risk reduced unless the client has verified it.
