# AgentGuard Positioning Skill

> Use this file before any job interview, consulting pitch, or LinkedIn post that involves AgentGuard.
> All claims below are backed by specific code or files in `~/projects/agentguard/`.

---

## What AgentGuard Is

AgentGuard is a production-deployed responsible AI governance layer that demonstrates how to safely deploy AI agents in enterprise environments — using confidence-based routing, human-in-the-loop review, SQLite audit logging, and an explainability report endpoint. It's live at [agentguard-delta.vercel.app](https://agentguard-delta.vercel.app).

**Note on demo scope:** The README describes an insurance claims triage demo. The actual deployed version (`src/claude.js`, `src/governance.js`) implements *job application screening* — the governance patterns are identical, but the domain context shifted. The live site title is "Job Application Screening." Don't describe it as insurance claims in an interview unless you update the demo first.

---

## Core Features Found (with file evidence)

| Feature | Where it lives | What it actually does |
|---|---|---|
| Confidence scoring | `src/claude.js` — `confidence: integer 0-100` returned by Claude | Claude returns a 0–100 confidence score with explicit band rules in the system prompt (85–100: obvious, 70–84: mostly clear, 55–69: borderline, 0–54: genuinely ambiguous) |
| Confidence-based routing | `src/governance.js` — `AUTO_APPROVE_THRESHOLD = 80` | Decisions ≥80% confidence auto-approve; <80% go to pending/human queue |
| Human-in-the-loop | `src/governance.js` — `reviewApplication()` | Three actions: approve, reject, override (with reason field). Override reason stored in DB |
| Full audit trail | `src/audit.js` — SQLite `decisions` table | Every decision logged: input, claim_type, priority, handler, confidence, reasoning, outcome, latency_ms, model, reviewed_by, override_reason, timestamp |
| Explainability report | `src/audit.js` — `getReport()` + `/report.html` | Live stats: auto-approval rate, human intervention rate, avg confidence, avg latency, outcome breakdown by type, recent rejections with reasoning |
| Rate limiting (safety control) | `src/server.js` — `AI_CALL_LIMIT = 30` | In-memory cap prevents runaway API costs — demonstrates cost governance awareness |
| Model transparency | `src/audit.js` — `model` column in DB | The specific model used for each decision is logged. Every row is queryable. |
| Vercel deployment | `vercel.json`, live URL | Production-deployed, not just local. Shows real shipping, not just prototyping. |

---

## Interview Talking Points

### 1. Confidence-Based Routing — The Core Governance Pattern

**Claim:** "I built a system where AI confidence determines whether a decision auto-executes or escalates to a human — with explicit thresholds tied to risk level."

**Evidence:** `src/governance.js` line 4: `const AUTO_APPROVE_THRESHOLD = 80;`. The system prompt in `src/claude.js` defines four confidence bands with explicit semantics — 0–54 means "human review, no exceptions." The routing logic is deterministic: `confidence >= 80 → auto_approved`, else `→ pending`.

**How to deploy in interviews:**
> "When asked about AI safety/governance: 'One of the core patterns I implemented in AgentGuard is confidence-based routing. The AI scores every decision 0–100. Above 80%, it auto-executes. Below 80%, it queues for human review. The bands are defined upfront — 55–69 means borderline, 0–54 means genuinely ambiguous, human required. That threshold is a business decision, not a technical one, and I designed the system so it can be adjusted without touching core logic.'"

---

### 2. Persistent Audit Trail with Model Attribution

**Claim:** "Every AI decision is logged with full context — including which model made it, how long it took, and what happened after human review."

**Evidence:** `src/audit.js` — the `decisions` table captures: `input`, `confidence`, `reasoning`, `outcome`, `override_reason`, `latency_ms`, `model`, `reviewed_by`, `timestamp`. The `model` column specifically means you can audit which model version made which call — relevant for compliance or model migration.

**How to deploy in interviews:**
> "When asked about accountability or audit: 'I built a full decision log — every AI call is stored with the input, the model used, confidence score, reasoning, latency, and what the human reviewer did with it — approve, reject, or override with a reason. That means you can reconstruct every decision retroactively. You can ask: how often does the AI get overridden? On what types of cases? That's what an enterprise risk team actually needs.'"

---

### 3. Human Override with Captured Reasoning

**Claim:** "Human reviewers can override AI decisions, and the override reason is stored — creating a feedback loop that can train future model improvements."

**Evidence:** `src/governance.js` — `reviewApplication()` accepts action `"override"` and stores `overrideReason` via `audit.reviewDecision()`. The DB column `override_reason` persists this. The `/api/report` endpoint surfaces recent rejections and overrides in the explainability view.

**How to deploy in interviews:**
> "When asked about human-in-the-loop: 'It's not just an approval button. The reviewer can override the AI recommendation and record *why*. That override reason is stored in the audit log. In a real deployment, that data becomes a labeled dataset — you know exactly where the model was wrong and what the right answer was. That's how you close the governance loop instead of just adding a human as a rubber stamp.'"

---

### 4. Explainability Report — Governance Metrics, Not Just Logs

**Claim:** "I built a governance reporting endpoint that surfaces auto-approval rates, human intervention rates, and failure patterns — the metrics a compliance or risk team would actually ask for."

**Evidence:** `src/audit.js` — `getReport()` returns: `autoApprovalRate`, `humanInterventionRate`, `avgConfidence`, `avgLatency`, `confidenceByType`, `outcomeBreakdown`, `recentRejections`. These are served via `GET /api/report` and visualized in `/report.html`.

**How to deploy in interviews:**
> "When asked about explainability: 'Audit logs are necessary but not sufficient. I added a report layer that aggregates: what percentage of decisions did the AI auto-handle vs. escalate? What's the average confidence by decision type? What are the recent rejections and why? That's the difference between a log you ignore and a governance dashboard you actually review in a quarterly risk meeting.'"

---

### 5. Rate Limiting as Cost Governance

**Claim:** "The system includes a hard cap on AI API calls per instance — demonstrating awareness that AI governance includes cost controls, not just accuracy controls."

**Evidence:** `src/server.js` — `const AI_CALL_LIMIT = 30;` with a 429 response and clear error message when exceeded. This is a simple but real control.

**How to deploy in interviews (use as a supporting point, not a lead):**
> "One thing people don't think about in AI governance is cost controls. I added a rate limit — the demo caps at 30 AI calls per cold start, returns a 429 with a clear message, and explains why. In production, that would be per-user or per-org. You need spending guardrails alongside safety guardrails."

---

## Consulting Pitch Angles

### 1. "Your AI is a black box. Mine can show you exactly what it did and why."
Target: Any SMB or mid-market client nervous about deploying AI in a customer-facing or ops workflow. Lead with the audit trail + explainability report. Demo `agentguard-delta.vercel.app/report`. Show them: auto-approval rate, human intervention rate, override log. Then say: "This is what responsible AI deployment looks like. I can build this into your workflow."

### 2. "You don't need to trust the AI. You need to trust the *system*."
Target: Clients in regulated industries (property management, construction, any with liability concerns). The pitch is that confidence-based routing *removes* the need for blind trust. Low-confidence decisions always go to a human. The AI is a triage layer, not a decision-maker. Use this to overcome "we're not ready for AI" objections.

### 3. "Before you scale AI, you need governance infrastructure."
Target: Clients who have tried AI tools (ChatGPT, basic automations) and are unsatisfied or burned. Frame AgentGuard as the missing layer — the thing that makes AI *deployable* vs. just *interesting*. Offer a governance layer build as a Phase 1 engagement: threshold calibration, audit logging, human review queue. It's a lower-risk entry point than a full automation overhaul.

---

## Honest Framing

### What JT CAN claim:
- "I built and deployed a production AI governance layer" — TRUE. Live at agentguard-delta.vercel.app.
- "It implements confidence scoring, human-in-the-loop, audit logging, and explainability reporting" — TRUE. All four are implemented in code, not just described.
- "The confidence thresholds are tunable business parameters, not hardcoded magic" — TRUE. `AUTO_APPROVE_THRESHOLD` is a single constant.
- "Every decision is logged with model attribution and latency" — TRUE. `model` and `latency_ms` columns in SQLite.
- "Override reasons are captured for feedback loop potential" — TRUE. Stored in DB.

### What JT should NOT over-claim:
- Do NOT say "enterprise-grade" without caveat — the DB is SQLite, the rate limit is in-memory (resets on cold start), and there's no auth on the review endpoints. It's a demo that demonstrates the *patterns*, not a production SaaS.
- Do NOT describe the demo as "insurance claims triage" — the live version (`src/claude.js`) is job application screening. The README references claims, but the code was updated. Sync your language to what's actually deployed.
- Do NOT claim it has "multi-model support" — it's hardcoded to `anthropic/claude-sonnet-4-6` via OpenRouter. The `model` column logs it but doesn't switch it.
- Do NOT claim it has user authentication or role-based access — the `/api/review` endpoints have no auth. Fine for a demo, not for a pitch to a CISO.

---

## When to Lead With This

### Job interviews — lead with AgentGuard when:
- Role mentions: "responsible AI," "AI governance," "AI risk," "human-in-the-loop," "AI oversight," "AI implementation"
- Interviewer asks: "How do you ensure AI decisions are trustworthy?" or "What happens when the AI gets it wrong?"
- Company is in: financial services, insurance, healthcare, legal, government, or any regulated industry
- Role is: AI Solutions Architect, AI Implementation Lead, AI/ML Platform Engineer, or any title with "governance" or "responsible AI"
- You're competing against candidates who only have chatbot or RAG builds — this differentiates on the safety/oversight axis

### Consulting pitches — lead with AgentGuard when:
- Client is hesitant about AI ("we're not sure we trust it")
- Client is in a regulated or liability-sensitive industry
- Client has had a bad experience with AI tools before
- The conversation turns to "but what if it makes a mistake?"

### Don't lead with AgentGuard when:
- The role is pure ML engineering or data science (different skill set expected)
- The client wants pure automation speed (governance framing adds friction to the pitch)
- Early discovery calls where you haven't yet identified the client's risk tolerance
