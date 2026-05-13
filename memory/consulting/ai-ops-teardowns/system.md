# AI Ops Teardowns — Operating System

Created: 2026-05-10

## Purpose
Turn timely company/category research into buyer-relevant workflow demos that show JT's AI implementation taste, Altmark-style operational thinking, and n8n execution ability.

This is a consulting proof engine, not a random trend-chasing content gimmick.

## Core Format
**If I were building AI ops for [company/category], I would not start with a chatbot. I would automate [specific invisible workflow] first.**

Every teardown must show:
1. The operational bottleneck.
2. The current messy/manual process.
3. The proposed workflow map.
4. The human approval / exception boundary.
5. The n8n/AI architecture.
6. The buyer-relevant outcome.
7. What this proves about implementation.

## Topic Selection Rule
Prefer **trending categories with operational pain**, not trending logos for their own sake.

Strong topics:
- property management / family offices
- construction / field ops
- wholesale distribution / inventory / order status
- skilled trades / scheduling / quoting
- healthcare admin / clinics where compliant and non-medical
- insurance / document renewal / compliance
- finance-heavy SMBs / cash management / reconciliation
- real estate brokers / distressed property workflows

Weak topics:
- consumer social apps
- AI startups with no clear ops pain
- companies trending because of drama only
- anything requiring confidential assumptions about a real company
- workflows that imply access to private systems without clearly labeling as hypothetical

## Scoring Rubric
Score 1–5 each:
- **ICP fit:** Would this attract property/ops/construction/wholesale/family-office buyers?
- **Workflow specificity:** Is there a real process with inputs, steps, exceptions, and output?
- **Reusable template potential:** Could this become a repeatable n8n workflow or consulting offer?
- **Content strength:** Would a reader learn something concrete in <60 seconds?
- **Proof adjacency:** Does this connect to Altmark/Aya/Spectrum credibility without exposing client-private info?
- **Build feasibility:** Can a mock or template be built in <2 hours, or real n8n workflow in <1 day?

Verdict:
- 24–30: Build real n8n demo/template + post.
- 18–23: Draft content + diagram only.
- 12–17: Save as backlog.
- <12: skip.

## Build Depth Tiers
### Tier 1 — Content-only teardown, 30–45 min
Use when timely but not worth building.
Deliverable: X post + LinkedIn draft + simple workflow map.

### Tier 2 — Mock workflow, 1–2 hours
Use when strong content/proof but no reusable integration yet.
Deliverable: workflow diagram, pseudo n8n node list, X/LinkedIn drafts.

### Tier 3 — Real n8n template, 0.5–1 day
Use only when reusable for Altmark-like buyers.
Deliverable: importable n8n workflow/template, sample data, runbook, screenshots, X/LinkedIn drafts.

## Guardrails
- Do not imply a company is a client unless it is.
- Use public/hypothetical framing: “If I were building AI ops for...”
- Do not expose Altmark private details; use generalized patterns.
- No autonomous financial actions in examples. Use human approval queues.
- No tenant/legal/medical advice. Flag, draft, route, log.
- Every real workflow must include dry-run mode, audit log, and error/fallback path.
- Build only reusable templates; do not build bespoke demos for random trending companies.

## Weekly Workflow
Recurring runner: `AI Ops Teardown Weekly Draft` cron (`f96cc24f-55e6-4064-a075-b897156a22f2`) runs Sundays 7:15PM ET from `agents/ai-ops-teardown/weekly-prompt.md`.

1. Find 3–5 buyer-relevant companies/categories from current proof lanes, niche intel, X/news/AppKittie/industry sources.
2. Convert each into an ops bottleneck hypothesis.
3. Score using the rubric.
4. Pick one teardown only if it scores 18+; otherwise write `SKIP_WEEK — [reason]`.
5. Produce Tier 1 or Tier 2 by default.
6. Escalate to Tier 3 only if it maps to Altmark/family-office/property/ops offer.
7. Save output under `memory/consulting/ai-ops-teardowns/YYYY-MM-DD-[slug].md`.
8. If post-ready, save drafts under `memory/content/bank/[YYYY-MM-DD]/`.
9. Update delivery calendar and create/update the JT review/post Mission Control task.
10. Add/reuse n8n templates under the appropriate project only after reading project lessons.

## Content CTA Rules
Primary CTA is proof, not a hard sell.
Good endings:
- “AI is most useful when it becomes the exception layer.”
- “The workflow matters more than the model.”
- “This is where AI implementation actually starts.”

Avoid:
- “DM me to build this” on every post.
- Overclaiming savings without evidence.
- Naming private/client details.

## Draft Delivery Contract
The system is not complete unless JT receives review-ready drafts, not just saved files.

Default cadence:
- **Sunday evening:** source scan + score 3–5 topics.
- **Monday morning:** deliver one review-ready LinkedIn draft + one X draft for the highest-scoring teardown.
- **Wednesday:** if the teardown is Tier 3 or built as a real n8n template, deliver a deeper LinkedIn case-study/proof post.
- **Friday:** deliver one compressed tactical insight from the same teardown or skip if no new angle exists.

Delivery format:
1. Send concise Telegram summary with the recommended first post.
2. Include local file path.
3. State whether it is: ready to post / needs JT edit / waiting on workflow build.
4. If LinkedIn-ready, include the full draft in the message unless >3,500 chars.
5. Create or update a Mission Control task only for JT-only review/posting or a real build.

## Source Scan Inputs
Use these in priority order:
1. Existing active client/proof lanes: Altmark, Aya, Marketsmith, family-office/property ops.
2. Warm opportunity categories from MEMORY.md and current efforts.
3. AppKittie / app-growth intel only when it maps to a business-ops workflow.
4. X/news trends only when a trending company/category reveals a workflow pattern relevant to JT's ICP.
5. Generic trend lists are weak unless converted into a specific ops bottleneck.

## Teardown-to-Template Escalation Rule
Only build a real n8n template when all are true:
- Score is 24+.
- The workflow maps to property/family-office/construction/wholesale/skilled-trade ops.
- Inputs can be mocked safely with synthetic data.
- The workflow demonstrates exception handling, approval, audit log, and failure path.
- The result can be reused in outreach, portfolio, or client delivery.

Otherwise, produce content/diagram only.

## Output Bundle Checklist
Each teardown bundle must include:
- Workflow teardown file.
- X draft.
- LinkedIn draft.
- Recommended first platform.
- One-line buyer relevance.
- Build tier decision.
- If Tier 2/3: pseudo n8n node list or real n8n template task.
- Posted-log follow-up instruction if JT posts it.

## Niche Intelligence Library Input
Before scoring a teardown, read the relevant `memory/niche-intel/` file if it exists. Use it to identify buyer pain, common workflow, trust issue, content angle, and kill/defer rule. If no niche file exists, create a short one only when the niche is likely to recur.
