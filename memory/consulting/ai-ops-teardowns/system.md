# AI Ops Teardowns — Operating System

Created: 2026-05-10

## Purpose
Turn timely company/category research into buyer-relevant workflow demos that show JT's AI implementation taste, Altmark-style operational thinking, and n8n execution ability.

This is a consulting proof engine, not a random trend-chasing content gimmick.

AI Ops Teardowns should examine a trending company or trending operational problem in a niche relevant to JT, then have Eve/JT's agentic system produce the optimal AI workflow JT would build for that company/problem. The public post should demonstrate implementation judgment: why this problem matters now, what the workflow should do, where humans approve, and what the buyer would get.

## Core Format
**[Current company/problem signal] shows [niche] is ready for [specific workflow]. The AI ops workflow I would build is [workflow with inputs, decisions, approvals, and outputs].**

Every teardown must show:
0. The current signal: company, funding, product launch, market shift, regulation, buyer pain, or recurring niche problem.
1. The operational bottleneck.
2. The current messy/manual process.
3. The proposed workflow map.
4. The human approval / exception boundary.
5. The n8n/AI architecture.
6. The buyer-relevant outcome.
7. What this proves about implementation.

Preferred LinkedIn shape:
1. Translate the current signal into a buyer-recognizable bottleneck, not a news recap.
2. Show the operating scene with concrete inputs and failure modes.
3. Name the system of record or business process that still needs a clean output.
4. Introduce the workflow JT would build as an intake desk, router, review queue, or operating layer.
5. Explain what it reads, extracts, checks, drafts, routes, and preserves.
6. Close with the practical outcome: customers/operators keep working normally while the business gets cleaner data, clearer ownership, and fewer downstream errors.

Weak teardown smell:
- Generic "workflow before AI" advice with no current signal.
- Reusing the same approval-queue/exception-layer framing without a new company, niche, or problem.
- Hypothetical client-safe content that could apply to any business.
- A post that sounds like AI consulting advice instead of a teardown of a concrete company/problem.
- A hook that only summarizes the news instead of turning the news into an operational bottleneck.
- A close that says AI is useful in general instead of naming the before-it-hits-the-system outcome.

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

Selection bar:
- Current signal within the last 30 days unless explicitly marked evergreen.
- Clear relevance to JT's priority niches.
- Specific operational workflow with named inputs, failure modes, owner boundaries, and output.
- Enough public information to avoid confidential assumptions.
- Distinct angle from the last 45 days of posted/scheduled content.

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
- “Customers keep sending orders the way they already do. The distributor gets a cleaner intake layer before bad data hits the ERP.”
- “The operator keeps the existing front door. The workflow cleans the handoff before it reaches the system of record.”
- “[Buyer] gets [cleaner data / clearer ownership / faster confirmation] before [bad data / missed handoffs / stale work] becomes a downstream problem.”

When the post is buyer-facing, add a low-friction diagnostic CTA as a comment/reply or short closer. For property/family-office teardowns, route to `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md` and frame it as a workflow diagnostic, not a broad AI brainstorm.

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
1. Fresh company/category/problem signals from the last 30 days that map to JT's priority niches.
2. Existing active client/proof lanes: Altmark, Aya, Marketsmith, family-office/property ops.
3. Warm opportunity categories from MEMORY.md and current efforts.
4. AppKittie / app-growth intel only when it maps to a business-ops workflow.
5. Generic trend lists are weak unless converted into a specific ops bottleneck.

## Teardown-to-Template Escalation Rule
Only build a real n8n template when all are true:
- Score is 24+.
- The workflow maps to property/family-office/construction/wholesale/skilled-trade ops.
- Inputs can be mocked safely with synthetic data.
- The workflow demonstrates exception handling, approval, audit log, and failure path.
- The result can be reused in outreach, portfolio, or client delivery.
- Either the teardown has been posted and produced a real operator reply/DM signal, or JT explicitly prioritizes the build despite no market signal.

Otherwise, produce content/diagram only and keep the Tier 3 build task gated. Do not spend build time because a teardown scored well if distribution/reply signal has not happened yet.

## Review / Post / Defer Workflow
A teardown is not complete until JT makes one of two explicit decisions:

1. **Post:** JT publishes the draft and sends the URL back.
   - Append exactly one JSONL entry to `memory/content/posted-log.jsonl` with: `date`, `platform`, `title`, `source`, `url`, `posted: true`, `cta: "family-office-ai-ops-diagnostic"`, and `reply_route` when relevant.
   - Update the Mission Control review/post task to done only after the URL is captured.
   - Route any replies/DMs to `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md` or the matching diagnostic asset.

2. **Defer:** JT explicitly decides not to post now.
   - Do not mark posted.
   - Update the delivery calendar with defer reason and next review date.
   - Keep or update the Mission Control task with the next concrete action; close it only if a replacement task exists.

No agent may infer posting from intent, draft readiness, or banked content. A public URL is required evidence.

## First-Run Cron Verification
The weekly cron is configuration-validated until it has run at least once.
After the first scheduled Sunday run, verify:
- `openclaw cron runs --id f96cc24f-55e6-4064-a075-b897156a22f2 --limit 1` has a successful entry.
- Telegram delivery occurred or a saved output path exists.
- The generated teardown includes diagnostic CTA, proof-safe framing, posted-log instruction, and a Mission Control review/post task.
- No duplicate review/post or build task was created.

If any check fails, fix the prompt or task contract before the next Sunday run.

## Output Bundle Checklist
Each teardown bundle must include:
- Workflow teardown file.
- X draft.
- LinkedIn draft.
- Recommended first platform.
- One-line buyer relevance.
- Build tier decision.
- Diagnostic CTA or explicit reason no CTA is appropriate.
- Proof-safe framing note: public/hypothetical/category language, no fake client claims, no private client names, no unverified ROI/hours-saved/client-acceptance claims.
- If Tier 2/3: pseudo n8n node list or real n8n template task.
- Posted-log follow-up instruction if JT posts it.
- Mission Control JT review/post task with exact first action, why it matters, done state, and reply/DM routing.

## Niche Intelligence Library Input
Before scoring a teardown, read the relevant `memory/niche-intel/` file if it exists. Use it to identify buyer pain, common workflow, trust issue, content angle, and kill/defer rule. If no niche file exists, create a short one only when the niche is likely to recur.
