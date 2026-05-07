# App Marketing OS — Operating Spec

## Mission
Build a reusable, low-manual-work marketing system for JT's current and future apps so every product gets distribution strategy, measurement, iteration, and durable discovery by default.

This is not a replacement for Vibe Marketing, ReelFarm, Content Scheduler, or Sports GM. It is the control layer above them.

## Core Principle
Every app needs:
1. A clear audience.
2. A clear promise.
3. One primary discovery loop.
4. One secondary durable discovery channel.
5. A weekly metric.
6. A no-manual-work default path.
7. A kill/pause/continue rule.

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

## Channel Roles

### TikTok / ReelFarm
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
Primary loop: ReelFarm/TikTok movie taste slideshows.
Secondary loops: App Store optimization, SEO comparison pages, directory submissions.
Reddit: careful movie discussion/rating-system posts; no hard app pitch.
X: @jts_14 for build/product/milestones, not heavy product spam.
Weekly metric: TikTok views/saves/comments, App Store downloads, landing visits if available.

### Nash Satoshi
Stage: active.
Primary loop: dedicated crypto methodology content + ReelFarm/TikTok.
Secondary loops: SEO methodology pages, crypto/tool directories, X account growth.
Reddit: crypto game-theory/methodology discussion; product absent or lightly referenced only when safe.
X: @NashSatoshi methodology/rankings only; no return promises.
Weekly metric: site visits, ranking page visits, X engagement, TikTok engagement.

### Glow Index
Stage: pending/blocked until app + engine + deployment are reliable.
Primary future loop: dedicated skincare TikTok/ReelFarm.
Secondary loops: skincare SEO, ingredient/product comparison pages, beauty directories.
Reddit: very high caution; skincare subs are strict and skeptical. Default to research/ingredient education, not app promo.
Weekly metric once active: site visits, product searches, TikTok engagement, signup/email capture if available.

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
