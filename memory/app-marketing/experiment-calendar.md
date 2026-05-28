# App Marketing OS — Experiment Calendar

Week of: 2026-05-25
Generated: 2026-05-25

## Rule
Every generated product post should map to a named experiment, a success threshold, and a retire/rework rule. If it does not, skip it.

## Inputs used
- Metrics rows: 123
- Latest test brief: `test-briefs-2026-05-07.md`
- Planned rows currently waiting for live post IDs: 5

## Required Experiment Card + Measurement Spine
- Before any experiment becomes a Mission Control execution task, fill `memory/app-marketing/experiment-card-template.md` or an equivalent experiment-card section.
- Pattern score gate: only promote patterns scoring **24+/35** via `memory/app-marketing/winning-pattern-research-protocol.md`, unless the task is a measurement/crawlability/infrastructure fix.
- Required tracking fields: app, experiment name, channel, source URL/post URL, source tag or UTM, creative type, target audience, CTA, run date, 24h metric, 72h metric, 7d metric, downstream metric, decision, attribution confidence.
- Source-tag convention: `vista_tiktok_rating_precision_YYYYMMDD`, `nash_x_rankdelta_YYYYMMDD`, `glow_seo_category_[page]_YYYYMMDD`, or a similarly specific tag from `measurement-spine.md`.

## This Week’s Experiments

### 0. Vista-first artifact sprint setup
- **Channel:** X + SEO/AI-search planning
- **Hypothesis:** Vista's movie-taste identity mechanics can create more shareable low-cost artifacts than equal-effort posting across all apps.
- **Post plan:** Build one weekly artifact pack before posting: 5 Vista-led draft posts, 3 visual card concepts, source tags, CTAs, and a manual-approval gate.
- **Success threshold:** Pack is ready for JT approval with source tags and each post maps to a named artifact/test.
- **Retire/rework rule:** Do not scale to more than 5-7 total app posts/week until one format shows measurable traction.
- **Evidence:** Grok/X scan favored recent visual demo/taste/ranking posts; current App Marketing OS already identifies share artifacts as the missing acquisition loop.

### 1. Glow product-page GEO baseline
- **Channel:** SEO/GEO
- **Hypothesis:** Direct-answer product summaries, safe schema, FAQs, and llms.txt should create a stronger AI-search foundation before social fanout.
- **Post plan:** Verify deployed product-page GEO patch, then monitor indexed/crawlable product pages. Do not create TikTok volume until tracking and assets exist.
- **Success threshold:** Product pages show summary/FAQ/schema live and `llms.txt` is accessible; next week, move to one category-page pilot if crawl surfaces are healthy.
- **Retire/rework rule:** Do not build ingredient/dupe/concern pages until structured data supports unique, safe pages.
- **Evidence:** Glow is active at https://glowindex.co; product-page GEO patch pushed in `d28afc6`; no social metrics baseline yet.

### 2. Vista rating precision retest
- **Channel:** TikTok/ReelFarm
- **Hypothesis:** Specific movie + exact rating-number tension beats relationship-compatibility hooks.
- **Post plan:** 1 ReelFarm slideshow using a specific movie/rating hook. Use the latest test brief unless metrics reject it.
- **Success threshold:** ≥2x Vista TikTok baseline or ≥500 views, whichever is lower while sample is thin.
- **Retire/rework rule:** Do not run relationship-compatibility again until rating precision gets another clean test or compatibility has real proof.
- **Evidence:** Best observed Vista TikTok topic: rating_precision; best="IMDb gave Midsommar a 7.1. that's the wrong number." views=1114

### 3. Nash ranking/model update
- **Channel:** X @NashSatoshi
- **Hypothesis:** Specific rankings/model updates beat abstract methodology explainers.
- **Post plan:** 1 rankings/model-disagreement post only if live ranking/token details are available. Otherwise skip.
- **Success threshold:** ≥1.5x Nash X baseline or ≥300 impressions while sample is thin.
- **Retire/rework rule:** Avoid direct links, vague question prompts, and generic methodology explainers unless tied to a new live page/update.
- **Evidence:** Best observed Nash X topic: model_consensus; best="We upgraded to GPT-5.4, Gemini 3.1 Pro, and Opus 4.6 for this week's updated analyses.\n\nAnd it produced quite different " views=1177

### 4. Nash model-consensus slideshow
- **Channel:** TikTok/ReelFarm
- **Hypothesis:** Model-consensus/game-theory hooks with a concrete number beat vague “watch this” slides.
- **Post plan:** 1 slideshow around 4-AI agreement/disagreement. Add token/score only if live proof is visible.
- **Success threshold:** ≥2x Nash TikTok baseline or ≥150 views while sample is thin.
- **Retire/rework rule:** Never approve “watch this” or unclear title slides again.
- **Evidence:** Best observed Nash TikTok topic: game_theory_explainer; best="Crypto Isn't A Guessing Game. It's A Math Problem Most Traders Refuse To Solve." views=200

## Active Execution Queue
Tracking schema: `memory/app-marketing/experiment-tracking-schema.md`
Queue file: `memory/app-marketing/experiment-queue-2026-05-19.jsonl`

### Planned Experiments
1. `vista_tastecard_filmtok_soft_20260519` — gated borrowed-audience soft prompt after Taste Card prompt asset.
2. `nash_aiagents_receipt_x_20260519` — 2 public AI Agents ranking receipts before analyst/newsletter outreach.
3. `glow_productverdict_seo_batch1_20260519` — Product Verdict Card + 10 verdict pages before creator/writer outreach.

Rule: no outreach/send task should be marked ready until its gate is satisfied and a source tag is assigned.

## Do Not Test This Week
- Vista relationship compatibility unless a real proof asset exists. Current winner is rating precision.
- Glow TikTok/ReelFarm volume until account, assets, and metric path are confirmed.
- Glow ingredient/dupe/concern pSEO pages until structured data supports unique safe pages.
- Nash generic methodology explainers without a live ranking, model-update, or methodology-page launch angle.
- Any “watch this” TikTok/ReelFarm title or unclear slideshow hook.

## Measurement Requirement
- Every approved draft must create or update a planned row in `memory/app-marketing/post-registry.jsonl` with source tag/UTM, creative type, target audience, CTA, run date, and attribution confidence when known.
- Discovery must reconcile planned rows to exact live post IDs before performance is judged.
- Record 24h/72h/7d result windows before scale/iterate/kill decisions.
- If a post cannot be tracked, do not use it as evidence for future strategy.
