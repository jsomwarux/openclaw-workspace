# App Marketing OS — Operating Spec

## Mission
Build a reusable, low-manual-work marketing system for JT's current and future apps so every product gets distribution strategy, measurement, iteration, and durable discovery by default.

This is not a replacement for Vibe Marketing, ReelFarm, Content Scheduler, or Sports GM. It is the control layer above them.

## Core Principle
Every app needs:
1. A clear audience.
2. A clear promise.
3. One product-led share artifact.
4. One primary acquisition loop.
5. One borrowed-audience strategy.
6. One secondary durable discovery channel.
7. A weekly metric and tracking/source-tag path.
8. A no-manual-work default path where possible.
9. A kill/pause/continue rule.

No app should be “built and hoped into visibility.”

## System Map

### Existing Systems
- **Vibe Marketing Agent** (`agents/vibe-marketing/`): Existing product X, TikTok concept/copy, Reddit drafts, monthly LinkedIn. It should not be treated as the long-term OS root.
- **ReelFarm Intel OS** (`memory/reelfarm/`): TikTok slideshow trend intelligence from Social Growth Engineers + analytics input. JT's laptop/ReelFarm setup owns actual slideshow creation/posting execution. This is a separate daily/weekly cron, but it is an upstream intelligence source for App Marketing OS and should inform TikTok/ReelFarm hook/format recommendations.
- **Content Scheduler/Calendar** (`agents/content-scheduler/`, `agents/content-calendar/`): JT personal brand content.
- **Sports GM** (`skills/sports-gm/SKILL.md`): @dynastyjig growth and sports product demand creation.

### New OS Files
- `memory/app-marketing/audit-YYYY-MM-DD.md` — system audits.
- `memory/app-marketing/os-spec.md` — this spec.
- `memory/app-marketing/app-registry.md` — app stage/channel/metric source of truth.
- `memory/app-marketing/weekly-scoreboard.md` — weekly performance review.
- `memory/app-marketing/directory-submissions.md` — directory/backlink backlog.
- `memory/app-marketing/seo-backlog.md` — SEO/comparison/use-case page backlog.
- `memory/app-marketing/aso-checklist.md` — App Store optimization loops.
- `memory/app-marketing/future-app-template.md` — onboarding template for new apps.
- `memory/app-marketing/metrics-collection-status.json` — latest connector run status, skipped platform counts, failures, and non-secret readiness probes for App Store/web/X/ReelFarm/Reddit.
- `memory/app-marketing/web-analytics-mapping-template.md` — accepted schema for GA4/Search Console/Vercel/Plausible/PostHog/local-log mappings before social volume scales.
- `memory/app-marketing/ga4-integration-reference.md` — canonical GA4/Search Console setup and debugging reference; read before new app launches, client GA setup advice, or analytics troubleshooting. Property registry table is the source of truth for queryable properties and must stay synced with `account-map.json`.
- `memory/app-marketing/generated-mission-control-tasks.json` — latest deduped task-generator output; weekly review must inspect created/duplicate/error counts before claiming task sync is healthy.
- `memory/app-marketing/winning-pattern-research-protocol.md` — daily/weekly/monthly research protocol for finding successful app acquisition patterns.
- `memory/app-marketing/experiment-card-template.md` — required template before turning a pattern into a task.
- `memory/app-marketing/share-artifact-roadmap.md` — product-led share artifact roadmap by app.
- `memory/app-marketing/borrowed-audience-playbook.md` — target-record and pitch rules for creator/newsletter/community distribution.
- `memory/app-marketing/competitor-mining-protocol.md` — monthly competitor/review mining protocol.
- `memory/app-marketing/measurement-spine.md` — required source-tag/UTM/result fields for every acquisition experiment.

## Channel Roles

### TikTok / ReelFarm

### TikTok Shop / Social Commerce Intel
Role: watch fast-moving commerce patterns that can inform Glow Index, future POD/digital products, affiliate tests, and content hooks.

Rules:
- Treat TikTok Shop as a validation/distribution channel, not an inventory business by default.
- Prefer affiliate, POD, digital downloads, paid reports, or app-led commerce. Avoid inventory, shipping, returns, and customer support drag.
- For Glow Index, use only safe skincare/product-discovery angles: no medical claims, fake results, fake testimonials, or before/after claims.
- Every commerce idea must map to an owned asset: app, SEO page, email capture, product ranking, printable/template, or reusable content series.
- Save findings under `memory/app-marketing/competitor-intel/` or passive-income reports; do not create posting/shop automations without explicit approval.
Role: scalable rented-channel reach. JT runs the actual ReelFarm slideshow automations on his laptop; Eve supports strategy, hook/slide recommendations, performance tracking, and reusable assets.

Use for:
- Vista movie taste hooks.
- Nash Satoshi crypto/game-theory hooks.
- Glow Index skincare skepticism/ingredient hooks once active.
- Future apps where slideshow-native formats exist.

Rules:
- Keep JT's laptop ReelFarm setup as the execution layer.
- Eve should not duplicate or replace that automation on the Mac mini.
- Optimize from real analytics, not taste alone.
- Do not increase recommended volume until metrics capture is reliable.

### X
Role: account-native thesis building and occasional product discovery.

Systems:
- Vibe Marketing for product X.
- Content Scheduler for JT personal brand.
- Sports GM for @dynastyjig.

Rules:
- Do not create a second X generator.
- Optimize existing systems around account roles and performance feedback.
- Product accounts should not become generic founder diaries.

### Reddit
Role: careful community-native discussion, not promotion.

Rules:
- Existing Vibe Marketing Reddit system remains the generator.
- Default format should be discussion, analysis, or useful prompt.
- Product mention should be absent by default unless subreddit-safe.
- Never default to “I built X for Y.”
- If no compliant angle exists, skip Reddit for that app that week.

### SEO / Programmatic Pages
Role: durable search discovery.

Use for:
- Vista alternatives/comparison/use-case pages.
- Nash Satoshi methodology/game-theory pages.
- Action Arena prelaunch sports strategy pages.
- Glow Index ingredient/skincare analyzer pages.

Rules:
- Every app gets a small SEO page map before/around launch.
- Prioritize high-intent comparison and use-case pages.



### x402 / Agentic Commerce Readiness
Role: future-facing distribution and monetization lens for products that could become agent-readable or agent-purchasable.

Rules:
- Treat x402 as a content/product-readiness lens, not a default app feature.
- Use for API/data/report/workflow-endpoint products where agents might pay per result.
- Prioritize agent-readable outputs: JSON, markdown, CSV, PDF, API response, webhook, source-cited artifact.
- Every x402 idea must include receipts, audit trail, spend controls, pricing, docs, auth, and human approval boundaries where relevant.
- Do not add wallet/payment functionality to JT apps without explicit approval and a clear revenue case.
- Source: `memory/consulting/agent-ready-revenue-layer/positioning.md`.

### AppKittie / App Store Intelligence
Role: competitive app-growth intelligence and pattern extraction.

Use for:
- finding fast-growing apps adjacent to Vista, Glow Index, Nash Satoshi, Action Arena, and future app ideas;
- extracting hooks, creator/ad formats, screenshots, ASO keywords, IAP/pricing, and landing/store promises;
- turning competitor patterns into named weekly experiments.

Rules:
- Read-only. Do not copy creatives or wording; extract structure/pattern only.
- Treat AppKittie revenue/download figures as directional estimates, not truth.
- Use small API limits and cache results; list-app calls cost credits per app returned.
- Save reports under `memory/app-marketing/competitor-intel/`.
- Do not create a recurring cron until JT provides an AppKittie API key/subscription and one manual report proves signal quality.
- Every AppKittie insight must map to a concrete experiment in `experiment-calendar.md`, an ASO/screenshot change, or a durable SEO/directory action; otherwise skip it.


### Behavioral Demand Lens
Role: make sure app ideas and marketing tests are not merely useful, but emotionally legible enough for users to act.

Rules:
- Use `memory/app-marketing/behavioral-demand-lens.md` before generating app-marketing experiments or reviewing passive-income app ideas.
- Every named experiment should state motive, trigger, belief challenged, identity reinforced, anxiety resolved, and desired action.
- Do not use dark patterns, fake scarcity, fake authority, medical fear, financial promises, or shame.
- If a draft is logically correct but emotionally flat, rewrite or skip unless it serves SEO/durable discovery.

### Competitor Ad Intelligence
Role: read-only creative intelligence from paid-market signals.

Use for:
- extracting competitor hooks, offers, CTAs, visual frames, and landing-page patterns;
- improving organic product content and SEO pages;
- validating whether a niche has paid demand.

Rules:
- Read-only only.
- Do not connect ad accounts, create campaigns, change budgets, upload creatives, or touch spend without explicit JT approval.
- Treat ad patterns as creative evidence, not proof of organic performance.
- Save reports under `memory/app-marketing/competitor-intel/`.
- Current priority: staged, not skipped. Run before major launch/SEO/directory pushes or when hooks are weak.

### Directories / Backlinks
Role: compounding passive discovery and launch surfaces.

Rules:
- Every app gets a reusable submission pack.
- Track submitted / pending / rejected / accepted.
- Prioritize permanent listings and niche directories.

### ASO
Role: App Store discovery and conversion.

Use for App Store apps:
- Vista now.
- Future iOS apps.

Track:
- title/subtitle keywords.
- screenshots.
- first three screenshot hooks.
- description.
- reviews/ratings.
- competitor keyword positioning.

## Current App Strategy

### Vista
Stage: active.
Primary loop: Vista-first artifact-led growth sprint: movie taste/ranking cards, 1-100 rating hooks, and taste match/clash comparisons.
Secondary loops: App Store optimization, SEO/AI-search comparison pages, directory submissions, and limited ReelFarm/TikTok tests after manual-post/tracking gates are healthy.
Reddit: careful movie discussion/rating-system posts; no hard app pitch.
X: @jts_14 for build/product/milestones, not heavy product spam.
Weekly metric: TikTok views/saves/comments, App Store downloads, landing visits if available.
Current cadence rule: 5-7 total app posts/week across the whole portfolio, not 4-5 posts/week per app. Vista should receive 60-70% of the app-marketing slots during the next sprint.

### Nash Satoshi
Stage: active.
Primary loop: secondary weekly ranking-receipt and model-disagreement content tied to live data.
Secondary loops: SEO methodology pages, crypto/tool directories, X account growth.
Reddit: crypto game-theory/methodology discussion; product absent or lightly referenced only when safe.
X: @NashSatoshi methodology/rankings only; no return promises.
Weekly metric: site visits, ranking page visits, X engagement, TikTok engagement.
Current cadence rule: 1-2 weekly app-marketing slots unless a strong live ranking update creates a timely artifact.

### Glow Index
Stage: active for durable discovery planning; crawlability/measurement blocked before scale.
Primary current loop: skincare SEO/GEO, directory readiness, and safe product/category discovery surfaces.
Primary future loop: dedicated skincare TikTok/ReelFarm only after measurement source is connected.
Secondary loops: ingredient/product comparison pages, beauty directories, and education-first skincare content.
Reddit: very high caution; skincare subs are strict and skeptical. Default to research/ingredient education, not app promo.
Weekly metric: site visits/search clicks/product searches first; TikTok engagement only after account/execution + metrics path is confirmed.
Current blocker: `https://glowindex.co` returns 403 Cloudflare challenge for `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/categories`, and `/categories/serum`; do not expand pSEO or rely on category/directory crawlability until `python3 scripts/glow_crawler_check.py` reports all routes clear.
Current cadence rule: no recurring social volume. Use SEO/AI-search and safe page assets first.

### Action Arena
Stage: priority build/prelaunch.
Definition: fantasy football league structure + sports betting strategy. Players join leagues, receive a weekly fake budget (default $100), and compete on profit through straight bets, parlays, and teasers. No real money is wagered.
Primary loop: @dynastyjig native sports betting/fantasy strategy content with Action Arena as invisible backdrop.
Secondary loops: prelaunch waitlist, SEO pages around fake-money sports betting league / betting strategy league / fantasy football betting game, football-season launch plan.
Reddit: strategy prompts and league-mechanics discussions only; no direct product pitch by default.
Weekly metric: @dynastyjig engagement, waitlist signups when live, beta testers, league creation once built.

### Dynasty Fantasy Football Simulator
Stage: separate sports product lane.
Primary loop: @dynastyjig dynasty strategy content with simulator as invisible backdrop.
Secondary loops: SEO around dynasty simulator / fantasy football manager game once build exists.
Do not conflate with Action Arena.

## Weekly App Marketing Review
Every week, produce a short report:
1. What shipped/posted by app.
2. Metrics by app/platform.
3. Best-performing hook or format.
4. Worst-performing hook or format.
5. ReelFarm/Social Growth Engineers trend pattern to apply or ignore.
6. What to double down on.
7. What to retire.
8. One durable discovery action: directory, SEO, ASO, competitor ad intel, or screenshot asset.
9. One decision needed from JT, only if blocked.

Mandatory self-improvement layer:
- Read `memory/app-marketing/self-improvement-rules.md` before recommending more output.
- Assign each app/channel/experiment one decision state: `CONTINUE`, `DOUBLE_DOWN`, `REWORK`, `MEASURE_FIRST`, `PAUSE`, or `KILL`.
- If a channel is `MEASURE_FIRST`, generate measurement-fix tasks instead of more content-volume tasks.
- After metrics + experiment refresh, run `python3 scripts/app_marketing_task_generator.py --execute` so optimal next actions are pushed to Mission Control with dedupe, owner, first action, why, done state, references, and guardrails.

## File/Ownership Recommendation
Short term: keep existing X/Reddit/TikTok prompt files under `agents/vibe-marketing/` to avoid breaking crons and queue assumptions.

Medium term: create a cleaner `agents/app-marketing/` or `memory/app-marketing/systems/` structure and migrate only after mapping all cron/script dependencies. Recommended target split:
- `agents/app-marketing/product-content/` — product X, Reddit, LinkedIn drafts.
- `memory/reelfarm/` — TikTok slideshow intelligence and laptop-execution notes.
- `skills/sports-gm/` — @dynastyjig, Action Arena, Dynasty Simulator.
- `agents/content-scheduler/` — JT personal brand only.

Do not move files until imports, cron prompts, scripts, and queue paths are updated together.

## Implementation Rule
Before changing any live generator, queue, or cron:
1. Read this OS spec.
2. Read the target system's AGENT.md/SKILL.md.
3. Check queue and performance state.
4. Make the smallest patch.
5. Verify output with a dry run or file inspection.
