# Passive Income Strategist — 2026-05-13

## Executive Summary
- Ideas evaluated: 6
- BUILD: 1
- WATCH: 4
- PASS / skipped duplicate: 1
- Recommended next action: build only **WalkthroughProof** as a narrow evidence-artifact MVP. Do not open PickyBowl, FreelanceRate, StudioChurn, or WhitelistFlow until their validation triggers fire.
- Runway context: JT's near-term priority remains consulting cash, Altmark proof, Marketsmith/warm leads, and job-market optionality. Passive-income builds should only proceed if they are low-support, portfolio-reusable, and can be delegated to a coding agent without pulling JT into daily ops. WalkthroughProof fits because it reuses JT's property/audit-trail edge and can become consulting proof; the rest are either distribution-heavy, support-heavy, or less strategically aligned.
- Evidence note: live saturation checks were limited to the local `scripts/web_search.py` path. It returned useful results for running route planners and sparse/no result sets for the other exact-name queries. Judgments below use Scout evidence, current Mission Control state, niche-intel files, prior strategist reports, and conservative listicle-risk analysis rather than pretending exhaustive SERP proof.

## Existing Passive-Income Board Cross-Reference
Active or relevant Mission Control passive-income tasks found before analysis:
- `[Score 7.2] RouteSafe — safer running route planner` — status `todo`
- `[Score 7.1] RouteSafe scout/validation track` — status `todo`
- `[PI] Build: PDRN Decoder — turn PDRN skincare hype into ranked buying decisions` — status `todo`
- `[PI] Build: CollectionProof — photo-to-insurance inventory for collectors` — status `todo`
- `[PI] Validate: Spreadsheet-to-Agent Desk — productize shadow spreadsheet replacement` — status `todo`
- `[PI] Validate: RuleWatch NYC — compliance-change monitor for ops-heavy SMBs` — status `todo`

Result: **RouteVibe** is marked 🔁 ALREADY QUEUED because it has the same core mechanism and target audience as RouteSafe: running route planning around safety/comfort/vibe constraints.

## Saturation Filter Results
| Idea | Saturation Result | Decision |
|---|---|---|
| WalkthroughProof | Not a generic passive-income listicle idea. Property inspection software exists, but renter-first dispute-ready evidence artifacts are narrower. | Passed |
| PickyBowl Index | Dog-food affiliate/review content is crowded. The topper-specific scoring wedge is differentiated but still adjacent to saturated pet affiliate SEO. | Passed to analysis, capped at WATCH |
| RouteVibe | Running route planners exist and live search returned multiple planner/listicle results. Also already queued as RouteSafe. | 🔁 Already queued / skipped |
| FreelanceRate Receipts | Freelance calculators and pricing guides are common; sourced quote receipts are sharper but buyer willingness is unproven. | Passed to analysis, capped at WATCH |
| StudioChurn Radar | Dance-studio software alternatives are saturated; churn/exception layer on top of exports is differentiated. | Passed to analysis, capped at WATCH due support/onboarding |
| WhitelistFlow RP | FiveM/Discord whitelist tooling exists, but not a generic passive-income listicle idea. Market is speculative and support-heavy. | Passed to analysis, capped at WATCH |

## 🔁 Already Queued Ideas
- **RouteVibe** → existing MC tasks: `[Score 7.2] RouteSafe — safer running route planner` and `[Score 7.1] RouteSafe scout/validation track` (`todo`). Skipped deep analysis to avoid duplicate PI tasks.

---

# Full Analysis + Scorecards

## WalkthroughProof
**Verdict:** 🟢 BUILD THIS | Score: 7.4/10

### Value Proposition Test
This helps renters and small landlords create a dispute-ready move-in/move-out condition report from room photos in under 15 minutes.

### Market Demand Validation
The buyer pain is concrete: security-deposit loss, blame for pre-existing damage, and the anxiety of not knowing whether photos are enough. Photos are already part of the workflow, so the product does not require new behavior. The Scout found recent Reddit demand for rental inspection checklists and broad advice to photograph everything, while existing property-inspection tools are mostly built for property managers, not renters.

Revenue ceiling for a solo operation: **$2K–$5K/mo** from one-off $9 reports and small-landlord subscriptions; **$5K–$20K/mo** only if it becomes a broader tenant/landlord evidence vault with SEO and relocation-agent integrations.

### Competition Landscape
Competition exists: Property360, Keyturn, PHOTO iD, generic move-in checklist PDFs, landlord/property-management inspection apps. The weak spot is positioning. Most tools are operational platforms for managers; WalkthroughProof should be a lightweight evidence artifact for a renter or small owner who wants neutral, timestamped, exportable proof without learning inspection software.

The winning angle is **renter-first dispute proof**: photo hashes, room checklist, neutral defect wording, PDF/ZIP export, and optional JSON schema for relocation/property agents. Beginners get this wrong by trying to automate legal conclusions or detect every defect perfectly. JT should avoid liability by positioning it as documentation assistance, not legal advice or guaranteed damage detection.

### Vision Fit
- **Model task:** OCR/screenshot understanding, object/defect spotting, room categorization, checklist generation, neutral description writing.
- **Defensibility beyond generic prompting:** structured room/defect schema, source-photo hashes, timestamped artifact, PDF/ZIP export, recurring tenant vault, and property-audit language from JT's Altmark/family-office work.
- **Risk:** legal/liability risk if marketed as winning disputes. Use “organized documentation,” “neutral condition report,” and “evidence packet,” not legal guarantees.
- **Economics:** a photo batch can likely be processed for <$0.25–$0.75 if images are compressed and batched. A $9 report supports usage as long as free scans are capped.

### Agent-Native Fit
A relocation/renter agent could call WalkthroughProof during a move checklist, submit a room/photo batch, and store the returned PDF + JSON defects in a tenant vault. The output is narrow and agent-readable: PDF, ZIP, JSON room/defect schema, image hashes, timestamps. Human approval boundary is clean: user reviews descriptions before finalizing the PDF. This serves humans now and agents later.

### Behavioral Demand
- **Primary motive:** fear of loss + control/certainty.
- **Emotional trigger:** “I might lose $1,500 because I forgot to document this.”
- **Identity fit:** smarter renter / prepared small landlord.
- **Action urgency:** move-in/move-out windows create a hard deadline.
- **Ethical boundary:** no fake legal certainty, no scare tactics beyond honest deposit-protection framing.

### Build Reality
Coding agent builds: Next.js upload flow, room checklist UI, image compression/storage, vision extraction queue, Claude neutral-description layer, review/edit screen, PDF/ZIP generator, Stripe one-off payment, basic report archive, and optional JSON export. Existing JT infrastructure fits: Next.js, Vercel/Replit, Claude/Gemini vision, OpenClaw cron for SEO/demo content, and property/family-office niche knowledge for approval/audit framing.

Operating cost at scale: Vercel/Supabase/R2 $20–$50/mo, domain $15/year, AI vision + Claude variable but likely <$0.75/report with capped images, Stripe fees. Realistic build timeline: **2 weeks** for MVP; 3–4 weeks if adding account vault + landlord branding.

### Autonomous Marketing
Primary channel is SEO + short-form proof demos. Search terms: “move in inspection checklist photos,” “security deposit photo proof,” “rental inspection report app,” “move out condition report,” “apartment walkthrough checklist.” The product output creates shareable before/after screenshots: messy camera roll → clean defect ledger + PDF.

Best launch seed: renter/property subreddits with a non-sales beta post: “I built a tool that turns move-in apartment photos into a neutral condition report — what would make this actually useful before move-out?”

### Longevity
Security deposits, rental disputes, move-in/move-out documentation, and small-landlord paperwork are durable. What could kill it: landlord/property-manager platforms adding renter-side reporting, legal/compliance mistakes, or privacy concerns around interior photos. The position strengthens if JT builds a small corpus of defect wording, room checklists, and evidence formats over time.

## WalkthroughProof — Full Build Blueprint

### 1. The Opportunity
WalkthroughProof is a one-purpose evidence-artifact product: upload move-in/move-out photos, get a timestamped condition ledger, checklist, and dispute-ready PDF/ZIP. It works now because renters already take photos but do not organize them into something credible. It should still work in 3–5 years because rental turnover and deposit disputes are secular, not trend-dependent. The AI angle makes the artifact fast: room grouping, neutral defect descriptions, missing-checklist prompts, and export formatting.

### 2. Positioning for Profit
- **Smartest niche:** NYC/urban renters and small landlords doing self-managed move-ins/move-outs.
- **Defensibility:** source-photo hashes, structured room/defect schema, evidence packet format, growing library of neutral inspection language, and property-ops audit-trail credibility from JT's consulting work.
- **What beginners get wrong:** they build “AI home inspection” and imply diagnosis/legal outcomes. JT should build “documentation assistant + evidence packet” with review/approval before export.

### 3. Step-by-Step Build Instructions
**Phase 1 — MVP (Days 1–7):**
1. Create a new Next.js app or clone the smallest working app scaffold from JT's portfolio stack; name it `walkthroughproof`.
2. Build `/new-report`: address optional, move-in/move-out toggle, room list, upload up to 30 compressed photos.
3. Add storage using Supabase Storage or Cloudflare R2; save photo metadata, timestamp, file hash, room label, and original filename.
4. Create `analyze-photo-batch` job: vision model returns room, visible issue candidates, confidence, and suggested checklist items; Claude converts candidates into neutral descriptions.
5. Build review UI where user edits/accepts each defect line before final report generation.
6. Generate PDF + ZIP: cover page, room checklist, accepted defect ledger, source photo appendix, hash/timestamp table.
7. Add Stripe test payment: $9 unlocks full PDF/ZIP; free preview shows 3 findings and watermark.

**Phase 2 — Traction (Days 8–30):**
1. Add SEO landing pages: `/move-in-inspection-checklist`, `/security-deposit-photo-proof`, `/move-out-condition-report`.
2. Add a sample report with fake/demo apartment photos.
3. Launch beta post in renter/property communities; collect 10 reports processed manually/semiautomatically if needed.
4. Add report share link and “download evidence packet” email delivery.
5. Add small-landlord plan: branded template, unlimited reports, $49/mo.

**Phase 3 — Scale (Days 31–90):**
1. Add tenant vault/accounts for report history.
2. Add relocation-agent/property-manager API endpoint returning JSON + PDF.
3. Add recurring SEO pages for city/state move-out rules, carefully framed as documentation guides, not legal advice.
4. Build OpenClaw weekly demo-content cron: anonymized before/after examples, checklist posts, and SEO refresh suggestions.
5. Add affiliate/referral partnerships: renters insurance, moving checklist sites, relocation services.

- **Minimum viable version:** no accounts, no mobile app, no landlord dashboard, no legal advice, no automated demand letter. Just upload → review findings → pay → export PDF/ZIP.
- **Full tech stack:** Next.js + Vercel, Supabase Postgres + Storage or Cloudflare R2, Gemini/OpenAI vision, Claude for neutral copy, React PDF/Puppeteer PDF generator, Stripe Checkout, PostHog/analytics, OpenClaw cron for SEO/demo content.
- **Operating cost at scale:** $30–$100/mo fixed plus <$0.75/report AI/storage variable if images are capped/compressed.
- **Realistic build timeline:** 10–14 days via coding agent for MVP; 3–4 weeks for polished account/vault version.

### 4. Monetization
- **How first dollar comes in:** user uploads photos, previews the report, pays $9 through Stripe to unlock PDF/ZIP export.
- **Pricing model:** free preview; $9 one-off report; $19/mo renter vault; $49/mo small-landlord branded reports; later $2–$5/report API for relocation/checklist agents.
- **Affiliate programs / revenue splits:** optional renters-insurance or moving-services affiliate later. Do not make affiliate the first revenue path.
- **Path to $3K/month:** 250 one-off reports × $9 = $2,250 + 40 renter vault subs × $19 = $760.
- **Path to $10K/month:** 500 one-off reports × $9 = $4,500 + 75 landlord subs × $49 = $3,675 + 100 renter subs × $19 = $1,900.

### 5. Marketing Strategy (Autonomous — runs without JT)
**Primary channel:** SEO pages + renter-community proof demos.

**Week 1 launch post:**
- Platform: Reddit
- Community/subreddit: r/Apartmentliving, r/Renters, local NYC renter communities if rules allow
- Post format: “I built X, here is the output, roast the checklist before I charge for it.”
- Hook: “I got tired of move-in photos living in a camera roll, so I built a report generator for deposit disputes.”

**Ongoing autonomous marketing stack:**
- SEO: weekly new/updated pages around move-in/move-out documentation queries.
- TikTok/Reels: 15–30s before/after demos: camera roll → defect ledger → PDF.
- Reddit/X: answer renter documentation questions with checklist snippets, not spam.

**SEO strategy:**
- Primary search terms: move in inspection checklist photos; security deposit photo proof; rental inspection report app; apartment walkthrough checklist; move out condition report.
- Content pages to create: “Move-In Photo Checklist,” “Security Deposit Evidence Packet,” “How to Document Apartment Damage Before Move-Out,” “Small Landlord Move-In Report Template.”
- Timeline to first organic traffic: 6–12 weeks; faster if seeded through renter communities.

**Viral / referral mechanism:** the report summary screenshot is the share moment: “Here is the proof packet I made before move-out.” Natural referrals happen around moving season and roommate/friend advice.

**Paid acquisition:** avoid initially. CAC likely hard to prove until conversion rates on SEO/community traffic are known.

**What to do in Month 1 manually:**
1. Process 10 beta reports and inspect output quality.
2. Collect 3 anonymized before/after demos.
3. Ask one renter/property contact whether they would pay $9 before moving.
4. Tune defect language to be neutral and non-legal.

### 6. Automation Stack
- **What to automate first:** report generation from upload to PDF/ZIP after human review.
- **Full automation sequence:** user uploads photos → model groups/labels → Claude drafts neutral findings → user reviews/edits → Stripe unlock → PDF/ZIP generated → report emailed/stored → weekly cron generates anonymized demo/SEO snippets.
- **AI's role in the product:** image triage, room labeling, defect candidate extraction, neutral wording, missing-photo checklist prompts.
- **AI's role in marketing:** create checklist posts, SEO refreshes, and demo captions from anonymized sample reports.
- **How ongoing time approaches zero:** support is mostly payment/export issues; model output is user-approved before final, reducing dispute over AI accuracy.
- **OpenClaw integration:** new weekly `walkthroughproof-content` cron after launch; optional report-quality audit cron sampling failed/low-confidence analyses.

### 7. Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral Demand | Uniqueness | Competition | Agent-Native Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 8.0 | 7.2 | 7.5 | 7.0 | 6.8 | 8.5 | 8.0 | 6.5 | +0.2 |
**Weighted total:** 7.4/10

---

## PickyBowl Index
**Verdict:** 🟡 WATCH | Score: 6.6/10

### Value Proposition Test
This helps dog owners with picky or sensitive-stomach dogs choose a topper matched to dog needs, budget, and kibble in under 5 minutes.

### Analysis
Demand is real: pet owners spend emotionally, dog-food toppers have strong Scout momentum, and “what should I buy?” anxiety is recurring. But the market is affiliate-content heavy, and JT has no owned pet audience. The scoring wedge is useful, but it risks becoming another product-ranking site competing with Chewy, Business Insider, Whole Dog Journal, BetterPet, and review SEO incumbents.

The product could work if tied to a proprietary dog-profile quiz and TikTok affiliate format, but compliance matters: no veterinary claims, no allergy/medical promises, and careful language around sensitive stomachs. Agent-native fit is decent because a pet-shopping agent could request JSON product rankings, but human buyer trust and distribution are the hard parts.

### TikTok Shop / Social Commerce Fit
Affiliate-first and low inventory risk. Best content mechanic: “3 toppers for picky senior dogs ranked by price-per-serving and ingredient simplicity.” Compliance risk is moderate because pet-health claims can drift into pseudo-medical advice.

### Watch Trigger
Promote only if one of these happens: (1) JT has a repeatable Glow-style product-ranking engine ready to clone in <3 days, (2) TikTok Shop affiliate data shows multiple dog-topper products with strong creator conversion, or (3) a pet niche partner/account can distribute it.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral Demand | Uniqueness | Competition | Agent-Native/Social Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 7.5 | 7.0 | 8.0 | 6.0 | 6.8 | 8.0 | 5.8 | 4.5 | +0.2 |
**Weighted total:** 6.6/10

---

## RouteVibe
**Verdict:** 🔁 ALREADY QUEUED / SKIP | Score: n/a

RouteVibe is not a bad idea, but it is already represented by RouteSafe on the Mission Control board. Live search also returned multiple running route planner products/listicles, which confirms this category is not empty. The sharper route-planning wedge remains validation-first: static NYC scorecards + waitlist before building a dynamic planner.

Existing tasks:
- `[Score 7.2] RouteSafe — safer running route planner`
- `[Score 7.1] RouteSafe scout/validation track`

No new MC task created.

---

## FreelanceRate Receipts
**Verdict:** 🟡 WATCH | Score: 6.8/10

### Value Proposition Test
This helps freelancers decide what to charge for a specific client scope and produce a sourced quote rationale in under 10 minutes.

### Analysis
The psychological pain is excellent: embarrassment avoidance, underpricing fear, and quote confidence before sending a proposal. The agent-native artifact is also strong: JSON ranges, cited comparable rates, confidence level, and a client-ready paragraph that a proposal agent could buy mid-task.

The problem is willingness to pay and competition shape. Freelancers already search for free calculators, Reddit advice, rate guides, and marketplace comparables. A $7 micro-report might convert, but only if the output feels more credible than a prompt to ChatGPT. The hardest part is not build; it is trust, source quality, and distribution into freelancer communities without looking like another generic calculator.

### Agent-Native Fit
Good. A proposal-writing agent could call this endpoint while drafting a quote. Output should be JSON, markdown, and source-cited PDF. Pricing could be $3/report API or $7 human report. Still, human demand today needs validation before BUILD.

### Watch Trigger
Promote if JT can validate with 10 freelancers/consultants and at least 3 say they would pay $7 before sending a quote, or if a consulting/pricing content channel starts generating inbound questions about rates.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral Demand | Uniqueness | Competition | Agent-Native Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 7.0 | 7.5 | 8.0 | 5.8 | 6.3 | 8.2 | 6.5 | 5.5 | +0.3 |
**Weighted total:** 6.8/10

---

## StudioChurn Radar
**Verdict:** 🟡 WATCH | Score: 6.9/10

### Value Proposition Test
This helps dance/music/martial-arts studio owners spot churn, weak classes, waitlist gaps, no-shows, and overdue tuition from exported reports before the next enrollment cycle.

### Analysis
This is strategically strong for JT, but it is not passive enough yet. It maps cleanly to the `Spreadsheet-to-Agent Desk` and exception-dashboard thesis: do not replace Mindbody/DanceStudioPro; sit above exports and show what needs action. The buyer pain is real because local studios live and die by enrollment cycles, late tuition, no-shows, and parent communication.

The issue is onboarding/support. Every studio export will be messy, software-specific, and emotionally tied to revenue. Without a warm studio owner or repeatable sample export, this becomes a productized consulting workflow, not a passive-income app. That may still be worth doing under consulting, but it should not become another passive-income build until the schema/template is proven.

### Agent-Native Fit
Strong in theory: an owner ops agent can upload weekly exports and receive JSON exceptions + owner-ready emails. Human buyer value exists today. But trust and setup are the blockers.

### Watch Trigger
Promote if JT gets one real studio export or one owner call validating the top 5 exceptions and confirming willingness to pay $79/mo. Better path: fold it into **Spreadsheet-to-Agent Desk** as a vertical demo, not a standalone product.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral Demand | Uniqueness | Competition | Agent-Native Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 7.5 | 6.2 | 7.8 | 5.5 | 7.5 | 7.8 | 8.0 | 6.0 | +0.2 |
**Weighted total:** 6.9/10

---

## WhitelistFlow RP
**Verdict:** 🟡 WATCH | Score: 6.2/10

### Value Proposition Test
This helps FiveM/GTA RP server owners review whitelist applications, flag low-effort/AI-spam answers, and route staff decisions faster during launch or growth periods.

### GTA VI / FiveM Lens
This is the right kind of GTA/FiveM idea: a shovel for server owners, not a generic GTA content site. It avoids asset theft and does not depend on GTA VI internals. It can be prototyped with Discord + n8n + Claude + a lightweight dashboard.

The downgrade is support burden. Discord bots, Tebex/QBCore role sync, server-specific rules, and nontechnical admins create fragile installs and ongoing questions. Direct X signal was weak this week, and the Scout itself calls this speculative/watchlist-grade. Do not mark green solely because GTA VI attention is huge.

### Agent-Native Fit
Moderate. A server-owner ops agent could request weekly applicant risk summaries and audit logs. But this is SaaS/operator tooling, not a clean one-shot agent-purchasable endpoint.

### Watch Trigger
Promote if one of these happens: (1) a real RP server owner asks for whitelist automation, (2) Tebex/Cfx marketplace distribution path becomes clear, or (3) GTA VI/FiveM demand spikes with concrete server-owner complaints about application backlogs.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral Demand | Uniqueness | Competition | Agent-Native Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 6.5 | 5.5 | 7.0 | 5.8 | 6.8 | 7.0 | 8.5 | 5.5 | +0.1 |
**Weighted total:** 6.2/10

---

# Portfolio Commentary
WalkthroughProof fits JT's long-term passive-income portfolio better than another generic ranking site because it is a narrow confidence artifact: messy user input becomes a decision-ready output people will pay for at a deadline. It also reinforces the same property/family-office audit-trail story JT is using in consulting, which means the build can double as proof for Altmark-style buyers instead of distracting from near-term cash.

# Final Recommendation
Build **WalkthroughProof** only. Treat the MVP as both a passive-income product and a consulting proof asset: “I turn messy operational evidence into structured, reviewable, exportable artifacts.”

Do not build RouteVibe separately. Do not start PickyBowl, FreelanceRate, StudioChurn, or WhitelistFlow until their triggers fire.
