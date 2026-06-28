# App Marketing OS — Measurement Spine
Date: 2026-05-19

## Rule
Every acquisition experiment needs a source tag or it cannot teach the system.

## 2026-06-18 App Portfolio Gates
Use these app-specific north stars until the next written decision memo:

| App | Posture | North star | Activation | Stop / cap rule |
|---|---|---|---|---|
| Action Arena | Gate sprint | App Store submission status; 20 named kickoff commissioners | League created/joined; post-launch card built | Miss 2026-07-15 gate = pause until next preseason; dead week-2 retention = fix retention or pause |
| Glow Index | Push | Organic clicks/week; pages ranked top 20 | Affiliate click or email capture | 60-90 days with zero top-20 pages and zero AI citations = reassess niche/execution |
| Nash Satoshi | Cap | Methodology-page visits and research-only waitlist signups | Waitlist signup | 30 days of impressions with roughly zero page clicks/signups = cap to monthly or stop |
| Vista | Pause | Passive SEO/App Store monitoring only | Only relevant in un-pause test: card-driven install | Three-week card test below threshold confirms pause; no test until explicit trigger |

Scoreboard rule: impressions alone are never a success metric for Nash or Vista, and social views do not justify increased volume without downstream clicks/signups/downloads.

Paid UGC rule: paused by default. The only current exception is a capped Action Arena kickoff test after app-live + attribution gates are met. Its north star is per-creator attributable installs leading to league creation, not views. Scaling requires a written threshold and one creator clearing it. Nash is hard no; Glow requires compliance scripting and remains low priority.

## Minimum Tracking Fields
- app
- experiment name
- channel
- source URL / post URL
- source tag or UTM
- creative type
- target audience
- right-person reach definition
- right-person reach result or `UNAVAILABLE`
- CTA
- run date
- clicks or `UNAVAILABLE`
- installs/signups or `UNAVAILABLE`
- D1 retention or `UNAVAILABLE`
- D7 retention or `UNAVAILABLE`
- 24h metric
- 72h metric
- 7d metric
- downstream metric: download, signup, site visit, search click, waitlist, reply, or qualified lead
- unavailable metric fields and reason
- decision: scale / iterate / kill

## Metric Order
Judge app-distribution experiments in this order:
1. right-person reach
2. clicks
3. installs/signups
4. D1 retention
5. D7 retention

Views, impressions, likes, follows, and generic engagement can explain context, but they do not move an experiment to scale unless the ordered metrics above show real pull. If a metric cannot be measured yet, write `UNAVAILABLE` with the reason instead of leaving it blank.

## Link/Source Tag Convention
Use short source tags even when UTM links are unavailable:
- `vista_tiktok_rating_precision_YYYYMMDD`
- `vista_creator_tastecard_[creator]_YYYYMMDD`
- `nash_x_rankdelta_YYYYMMDD`
- `nash_newsletter_receipt_[name]_YYYYMMDD`
- `glow_tiktok_productverdict_[creator]_YYYYMMDD`
- `glow_seo_product_analysis_YYYYMMDD`
- `glow_seo_category_[page]_YYYYMMDD`
- `actionarena_ugc_[platform]_[creator]_YYYYMMDD`

## Active Glow SEO Source Tags
- `glow_seo_product_analysis_20260618` — first SEO/GEO pass on existing `/rankings/[id]` product analysis pages. Track GSC indexed/impressions/clicks, GA4 landing-page views, outbound affiliate/product clicks, email capture if present, and AI citation observations.
- `glow_seo_rankings_index_20260618` — same deploy batch as the first product-page pass; adds source-tagged rankings-index extraction copy and structured ItemList/FAQ context. Track `/rankings` GSC impressions/clicks, GA4 landing-page views, filter/search engagement, downstream product-detail clicks, and AI citation observations.
- Post-deploy baseline: `memory/app-marketing/glow-post-deploy-measurement-2026-06-18.md`.
- Current measurement gap: GA4 has page/event data, but `customEvent:source_tag` is not queryable until `source_tag` is registered as an event-scoped custom dimension in GA4 Admin. API read access works, but API create failed with `ACCESS_TOKEN_SCOPE_INSUFFICIENT`, so setup needs GA4 UI access or OAuth reauth with Analytics Admin edit scope.
- Post-deploy next action: fix source-tag reporting, then measure both Glow SEO source tags at 72h and 7d before burning another Replit rebuild on category or methodology pages.

## Fallback When Deep Links Are Not Available
- Record post URL.
- Record exact CTA/link destination.
- Record timestamp.
- Compare app/site metrics in the following 24h/72h/7d windows.
- Mark attribution confidence: high / medium / low.
