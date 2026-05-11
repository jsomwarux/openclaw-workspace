# AI Ops Teardowns — Backlog

## Priority Teardowns

### 1. Property Management — Insurance Expiration Exception Layer
Score: 29/30
Tier: 3 real n8n template candidate
Why: Direct Altmark adjacency, safe to generalize, buyer pain is clear.
Workflow: scan COI/insurance dates → flag expiring docs → draft follow-up → approval queue → daily exception summary → audit log.
Content angle: property managers do not need a chatbot; they need an exception layer for expiring docs.

### 2. Property Management — Rent Delinquency Data Readiness + Outreach Queue
Score: 28/30
Tier: 2 now, Tier 3 after clean sample data
Why: Strong Altmark adjacency, but tenant-facing outreach requires careful data readiness and human approval.
Workflow: ingest delinquency report → validate fields → flag missing/dirty ledgers → draft outreach → approval queue → cooldowns → summary.
Content angle: never automate tenant outreach from a dirty ledger.

### 3. Construction — Field Note to Owner Update
Score: 25/30
Tier: 2 mock workflow
Why: Strong construction ICP and content-friendly.
Workflow: foreman note/photo → classify issue → punch item → owner update draft → approval → daily log.
Content angle: the valuable AI workflow is not “chat with project docs”; it is turning messy field notes into accountable updates.

### 4. Wholesale Distribution — Order Status Exception Desk
Score: 24/30
Tier: 2 mock workflow
Why: Strong Spectrum/product catalog + wholesale ICP fit.
Workflow: order export + inventory ETA + inbox → exception detection → customer reply draft → rep approval → stale order report.
Content angle: customers do not need a portal if the team cannot see what is stuck.

### 5. Family Office — Cash Timing / Overdraft Risk Queue
Score: 23/30
Tier: 2 only unless sensitive data is mocked cleanly
Why: High buyer pain, high caution because financial actions must stay approval-only.
Workflow: bank balances + AP calendar + recurring obligations → risk flags → recommended transfer draft → CFO approval → audit log.
Content angle: AI should never move money autonomously; it should surface timing risk early.

### 6. Real Estate Brokerage — Distressed Property Deal Intake
Score: 21/30
Tier: 1/Tier 2
Why: Good broker pivot for Aya acquisition-dashboard learning.
Workflow: listing/source email → property facts → distress flags → buyer-fit score → broker summary.
Content angle: brokers need faster deal intelligence, not another CRM.

## Trend-Responsive Slots
Use only when a company/category is trending and maps to one of the above workflow families.

Template:
- Source / trend:
- Company/category:
- Ops bottleneck hypothesis:
- Buyer:
- Score:
- Tier:
- Draft/build decision:
