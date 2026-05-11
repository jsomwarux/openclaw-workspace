# AppKittie Evaluation — 2026-05-10

## Trigger
JT shared Jacob Rodri's X post: find fast-growing apps by filtering AppKittie for apps doing >$50K/mo and launched <6 months ago.

Post data pulled from X:
- Text: “how to find these fast-growing apps in 20 seconds: 1. go to appkittie.com 2. filter by apps making over $50k/mo 3. filter by apps launched under 6 months ago...”
- Metrics at fetch: 1 like, 367 impressions, 4 bookmarks.
- The quote-linked thread about Wayk/alarm app had much stronger signal: ~7.5K likes / 3.6M impressions, claiming a mission-based alarm app hit ~$200K MRR in 3 months via TikTok format.

## What AppKittie Is
App Store / Google Play intelligence platform with dashboard, API, and MCP/agent positioning.

Docs/source facts checked:
- App database: claims 2M+ mobile apps.
- List endpoint supports filtering/sorting by source, category, revenue, downloads, growth window, reviews, release/update timestamp, Meta ads, Apple Search Ads, creator partnerships, contact emails, language, and more.
- Get-app endpoint returns app metadata, descriptions, screenshots, IAPs, historical data, revenue/download estimates, creator partnerships, creator videos, Meta/Apple ads, contact data, and reviews.
- API credit model: list apps costs 1 credit per app returned; app detail costs 1 credit/request; keyword difficulty costs 10 credits/keyword.
- AppKittie has MCP/agent docs and API key support, so it can become agent-readable if JT subscribes/provides API key.

## Fit for App Marketing OS
Verdict: **Yes, high fit — but as a weekly competitive-intel input, not as a build-idea firehose.**

Best use:
1. Find fast-growing apps adjacent to Vista / Glow Index / future apps.
2. Extract their marketing pattern: hook, premise, creative format, CTA, landing/store promise, price/IAP, ad/creator channel, screenshot structure, keywords.
3. Convert the pattern into **one named experiment** in `memory/app-marketing/experiment-calendar.md`.
4. Apply only if it maps to a current app and a measurable channel.

Do not use it to blindly chase app ideas. The dangerous failure mode is building another random app because a category is hot.

## Best Filters to Start
Use small limits to control credits.

### Glow Index / skincare
- source=apple_mobile or google_mobile
- categories=Health & Fitness,Lifestyle
- minRevenue=50000
- releasedAfter = now minus ~180 days
- growthPeriod=30d
- growthType=positive
- sortBy=growth
- hasMetaAds=true OR hasCreators=true

### Vista / entertainment taste apps
- categories=Entertainment,Lifestyle,Photo & Video
- search terms: movie, film, rating, taste, recommendation, tracker, watchlist
- minRevenue=10000 initially, because niche movie apps may be smaller
- sortBy=growth or revenue

### Future app discovery
- minRevenue=50000
- releasedAfter last 180 days
- growthType=positive
- hasCreators=true OR hasMetaAds=true
- exclude games unless explicitly researching game mechanics.

## Weekly Report Shape
`memory/app-marketing/competitor-intel/YYYY-MM-DD-appkittie.md`

For each app:
- App / category / launch age / estimated monthly revenue / downloads / growth period.
- Marketing channel evidence: Meta ads, Apple ads, creator videos, TikTok/creator handles, screenshots, keywords.
- Winning pattern: hook, visual structure, CTA, promise, price/IAP, onboarding/store conversion clue.
- Apply to JT app: Vista / Nash / Glow / Action Arena / future app.
- Experiment candidate: exact post/page/screenshot/test to run.
- Confidence: High/Medium/Low, because AppKittie revenue/downloads are estimates.

## Recommendation
Create one Mission Control task to add AppKittie as an optional App Marketing OS data source. Do not add a recurring cron until an API key/subscription exists and one manual report proves signal quality.
