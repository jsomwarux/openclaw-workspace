# App Marketing OS — Measurement Spine
Date: 2026-05-19

## Rule
Every acquisition experiment needs a source tag or it cannot teach the system.

## Minimum Tracking Fields
- app
- experiment name
- channel
- source URL / post URL
- source tag or UTM
- creative type
- target audience
- CTA
- run date
- 24h metric
- 72h metric
- 7d metric
- downstream metric: download, signup, site visit, search click, waitlist, reply, or qualified lead
- decision: scale / iterate / kill

## Link/Source Tag Convention
Use short source tags even when UTM links are unavailable:
- `vista_tiktok_rating_precision_YYYYMMDD`
- `vista_creator_tastecard_[creator]_YYYYMMDD`
- `nash_x_rankdelta_YYYYMMDD`
- `nash_newsletter_receipt_[name]_YYYYMMDD`
- `glow_tiktok_productverdict_[creator]_YYYYMMDD`
- `glow_seo_category_[page]_YYYYMMDD`

## Fallback When Deep Links Are Not Available
- Record post URL.
- Record exact CTA/link destination.
- Record timestamp.
- Compare app/site metrics in the following 24h/72h/7d windows.
- Mark attribution confidence: high / medium / low.
