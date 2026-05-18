# AI Ops Teardown - Rent Delinquency Data Readiness Queue

Date: 2026-05-17
Slug: rent-delinquency-readiness
Selected topic: Property / family-office rent delinquency data readiness before tenant outreach
Score: 28/30
Build tier: Tier 2 now. Tier 3 only after a posted teardown produces operator reply/DM signal, or JT explicitly prioritizes a synthetic-data build.
Recommended first platform: LinkedIn
CTA target: `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md`

## Why This Topic Cleared The Bar

Property and family-office teams often treat rent delinquency automation like a messaging problem. The safer first workflow is a readiness queue: which rows are clean enough to act on, which are blocked, and which need manager review before any tenant-facing message is drafted.

This is buyer-relevant because delinquency reports, tenant ledgers, payment-plan notes, stale balances, and manager approvals are real operating inputs. It also supports JT's current consulting positioning without naming private client work or claiming unverified results.

## Source Scan

### Current proof-lane inputs
- `memory/content/current-efforts.md`: Altmark/family-office/property ops is the top consulting proof lane; rent delinquency workflow is paused until reporting and tenant-ledger hygiene are cleaned up first.
- `memory/niche-intel/property-family-office.md`: best first workflows include rent delinquency report cleanup, approved outreach prep, owner/vendor exception reporting, and audit trails.
- `memory/consulting/ai-ops-teardowns/backlog.md`: rent delinquency readiness scored 28/30 as Tier 2 now, Tier 3 after clean sample data.

### Public/current category signal
- Buildium 2026 property management tech content emphasizes maximizing existing software and measuring operations impact, which supports a workflow-first angle rather than a new-platform pitch.
- Public rent-ledger and delinquency workflow materials consistently frame ledgers, overdue balances, payment records, and escalation steps as core property-management inputs. Use this only as category context, not as proof of JT outcomes.

## Candidate Scores

| Candidate | ICP fit | Specificity | Template potential | Content strength | Proof adjacency | Build feasibility | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Rent delinquency data readiness + approved outreach queue | 5 | 5 | 5 | 5 | 4 | 4 | 28 | Pick. Strong property/family-office fit, timely Altmark adjacency, proof-safe if framed as category/hypothetical. |
| Insurance / COI expiration exception tracking | 5 | 5 | 5 | 4 | 5 | 5 | 29 | Already has an active unposted bundle and MC task. Do not duplicate this week. |
| Family-office cash timing / overdraft risk review queue | 5 | 4 | 4 | 4 | 4 | 3 | 24 | Strong but more sensitive. Keep approval-only and use later. |
| Construction field note to owner update | 4 | 5 | 4 | 4 | 3 | 5 | 25 | Good future X-first post, but less aligned with current family-office wedge. |
| Wholesale order status exception desk | 4 | 5 | 5 | 4 | 3 | 4 | 25 | Strong future teardown, but less tied to the current diagnostic offer. |

## Business Context

If I were building AI ops for a property management or family-office team, I would not start by letting AI contact tenants.

I would start by checking whether the delinquency data is clean enough to trust.

The workflow is not about autonomous collections. It is about turning a messy report into a reviewable queue with status, blockers, approvals, and an audit trail.

## Current Manual Process

1. A property/accounting system exports a delinquency report.
2. Staff manually review tenant, unit, balance, days late, contact, last payment, and notes.
3. Edge cases live across ledgers, payment plans, inboxes, texts, and staff memory.
4. Managers decide which rows are safe to contact.
5. Outreach is drafted manually or copied from templates.
6. Follow-up status is tracked in spreadsheets, inboxes, or informal notes.

## Failure Modes

- Report is stale or excludes recent payments.
- Tenant name, unit, balance, or contact fields are missing.
- Payment-plan notes are not visible in the export.
- Duplicate tenants or duplicate units appear across reports.
- A row looks delinquent but needs manager/legal review.
- Outreach drafts quote the wrong amount or go to the wrong contact.
- There is no clear ready, blocked, sent, or needs-review queue.
- There is no audit trail showing source amount, draft, approver, send status, and timestamp.

## Proposed AI Ops Workflow

| Step | Input | System action | Human boundary | Output |
|---|---|---|---|---|
| 1 | Delinquency CSV/XLSX export | Validate required columns and freshness | Stop if schema or date fails | Data-readiness report |
| 2 | Tenant rows and ledger fields | Flag missing fields, stale balances, duplicates, odd amounts, and payment-plan notes | Manager reviews blocked/ambiguous rows | Ready vs blocked queue |
| 3 | Notes and payment-plan fields | Summarize only the operational reason a row needs review | No legal advice or tenant action | Review reason per row |
| 4 | Approved ready rows | Draft outreach from approved templates | Human approval required before send | Draft message queue |
| 5 | Cooldown/status table | Prevent duplicate or too-frequent outreach | Human override only | Safer contact cadence |
| 6 | Approval decision | Log approver, decision, source amount, draft, send status, and timestamp | Human owns final decision | Audit trail |
| 7 | Daily summary | Group ready, blocked, needs review, approved, sent, and stale rows | Manager reviews before action | Delinquency ops brief |

## n8n Node Sketch

1. Trigger: manual upload or scheduled folder watch for delinquency export.
2. Spreadsheet/File node: read CSV/XLSX.
3. Code node: normalize tenant, unit, property, balance, days late, contact, last payment date, notes.
4. Validation node: required fields, export date, duplicate detection, amount sanity checks.
5. Rules node: assign row status: ready, missing data, stale balance, payment-plan review, duplicate, manager review.
6. LLM node: summarize review reason only for non-ready rows. No legal advice.
7. LLM node: draft outreach only for ready rows using approved templates.
8. Approval queue: Airtable/Sheet/Notion/local UI depending on client environment.
9. Send branch: disabled by default; only executes after explicit approval.
10. Audit log: append source row hash, status, draft, approver, action, timestamp, and error state.
11. Daily digest: manager summary of ready, blocked, approved, stale, and error rows.
12. Error branch: quarantine malformed files and notify operator without drafting messages.

## Exception Logic

Rows should be blocked, not drafted, when:
- balance or days-late value is missing
- export date is stale
- tenant/contact field is missing
- unit/property mapping is ambiguous
- payment-plan note exists
- recent payment field conflicts with balance
- duplicate row appears for tenant/unit
- row is marked legal, dispute, hold, bankruptcy, eviction, deceased, or do-not-contact
- any confidence threshold is below the client's approval standard

## Human-In-The-Loop Boundary

The system can validate, classify, summarize, draft, and log.

A human must approve:
- whether a row is contact-ready
- any tenant-facing message
- any escalation sequence
- any override of blocked rows
- any changes to approved templates or cooldown rules

The system should never autonomously send tenant notices, make legal judgments, waive balances, apply fees, or change ledger data.

## Buyer Outcome

The buyer gets a cleaner operating view:
- what rows are ready
- what rows are blocked
- why each row is blocked
- who needs to approve it
- what draft is waiting
- what happened after approval

That is more valuable than a chatbot because it protects trust before speed.

## Why This Is Reusable

The same pattern applies to any sensitive operations workflow where bad source data creates business risk:
- tenant/vendor follow-up
- insurance expirations
- loan/document deadlines
- owner reporting
- AP/cash timing review
- compliance renewal tracking

## Build Tier Decision

Tier 2 now: content + workflow map + pseudo n8n node list.

Do not build a real n8n template yet. Even though the score is high, tenant-facing workflows are sensitive and should stay gated until:
1. this teardown is posted and produces operator reply/DM signal, or
2. JT explicitly prioritizes the build, and
3. the build uses synthetic data only, with no client/private tenant records.

## Proof-Safe Framing Note

Use category/hypothetical language only. This is proof-safe framing: no private client names, no fake client claims, no private data, no ROI or hours-saved claims, and no autonomous tenant action. Do not name Altmark, Aya, Yair, Matt, Navid, or any private client. Do not claim ROI, hours saved, collection improvement, client acceptance, or tenant outcome. Do not imply autonomous tenant action.

## Diagnostic CTA

Buyer-safe CTA: route property/family-office replies to `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md`.

Suggested CTA comment:

> Worth doing a 30-minute workflow diagnostic? I can map the report, data-readiness issues, approval points, and first safe automation worth building before anything tenant-facing runs.

## Posted-Log Follow-Up Instruction

If JT posts this, append exactly one JSONL entry to `memory/content/posted-log.jsonl` only after a public URL exists:

```json
{"date":"2026-05-17","platform":"LinkedIn","title":"Rent Delinquency Data Readiness Queue","source":"memory/content/bank/2026-05-17/ai-ops-teardown-rent-delinquency-readiness.md","url":"PUBLIC_URL_HERE","posted":true,"cta":"family-office-ai-ops-diagnostic","reply_route":"memory/consulting/family-office-ai-ops-diagnostic-one-pager.md"}
```

If JT defers, do not write a posted-log entry. Update `delivery-calendar.md` with the defer reason and next review date.
