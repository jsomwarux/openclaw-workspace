# Glow Index Post-Deploy SEO/GEO Measurement
Date: 2026-06-18

## Scope
Measure the live Glow SEO/GEO batch before any new Replit rebuild.

Live deploy:
- Commit: `3c60c25 Add Glow rankings index SEO context`
- Includes: crawler public-route fix `329ed72`, product-analysis SEO/GEO pass `2fa05cf`, and rankings-index SEO/GEO context `3c60c25`.
- Source tags:
  - `glow_seo_product_analysis_20260618`
  - `glow_seo_rankings_index_20260618`

## Live Verification
Command: `python3 scripts/glow_crawler_check.py`

Result:
- `all_clear=true`
- `robots.txt`, `sitemap.xml`, `llms.txt`, `/rankings`, `/categories`, and `/categories/serum` all return `200`.
- No Cloudflare challenge detected.

Googlebot-style fetch markers:
- `/rankings`: `AI skincare rankings for product research`, `glow_seo_rankings_index_20260618`, `CollectionPage`, `ItemList`, and `FAQPage` present.
- `/rankings/cmmv3rvfk001i6zawetmdagv3`: `AI skincare analysis`, `glow_seo_product_analysis_20260618`, and a `/categories/` internal link present.
- `/categories/serum`: live and crawlable with `AI-ranked skincare serums`, `Compare skincare serums`, `consumer research`, and `ItemList`.
- `/llms.txt`: includes the rankings-index canonical discovery hub language and consumer-research framing.

## Baseline Analytics
GA4 property:
- Glow property: `537965547`
- Measurement ID: `G-YH902137XF`

Search Console:
- Property: `sc-domain:glowindex.co`
- 2026-06-11 to 2026-06-18 query rows: `glow index`, 0 clicks, 1 impression, average position 8.
- Page filter for `/rankings`: no Search Console page rows yet.

GA4 today:
- `/rankings/cmmv3rvfk001i6zawetmdagv3`: 2 pageviews, 4 events.
- `/rankings/cmmv3rwio002p6zawwdg577kf`: 2 pageviews, 4 events.
- Event totals today: `page_view` 8, `view_product` 4.

Collector baseline:
- `python3 scripts/app_marketing_collect_metrics.py` completed with `APP_MARKETING_METRICS_OK entries=253 errors=0`.
- It appended 0 new rows because current stored rows already covered the latest supported weekly GA4/GSC windows.
- Latest stored Glow weekly web row for 2026-06-11 to 2026-06-17 shows 0 GA4 sessions/pageviews/events and 1 Search Console impression for `glow index`.

## Measurement Gap
GA4 is receiving page and event data, including `view_product`, but `source_tag` is not queryable yet through the GA4 Data API.

Verification:
- GA4 metadata does not expose `customEvent:source_tag`.
- `properties/537965547:runReport` with dimension `customEvent:source_tag` returns HTTP 400: `Field customEvent:source_tag is not a valid dimension`.
- Analytics Admin API read works: listing `properties/537965547/customDimensions` returned status 200 and count 0.
- Analytics Admin API create does not work with the current OAuth token: creating event-scoped `source_tag` returned HTTP 403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT` for `AnalyticsAdminService.CreateCustomDimension`.

Implication:
- The site-side source tags are present and event payloads include the field, but GA4 reporting cannot segment by source tag until `source_tag` is registered as a custom event-scoped dimension in GA4 Admin.
- The current connector token can read analytics/admin state but cannot create the reporting dimension. Fix requires either GA4 UI setup or a new OAuth grant with Analytics Admin edit scope.

## Decision
Do not start another Glow build or Replit rebuild now.

`/categories/serum` is live and crawlable, but it should be treated as a measurement candidate, not the next automatic deploy. The stricter live code gate remains:
- `CATEGORY_MIN_PRODUCTS = 10`
- `CATEGORY_MIN_ANALYZED = 5`

Next deploy batch should wait until the baseline shows one of:
- `/rankings` or product-detail pages getting early GSC impressions/clicks.
- Product-detail `view_product` and landing-page views increasing after indexing.
- AI citation/extraction evidence appears.
- GA4 source-tag reporting is fixed so campaign/page impact can be segmented.

## Next Check
1. Register `source_tag` as an event-scoped custom dimension in GA4 Admin for Glow:
   - Property: Glow Index / `537965547`.
   - Custom dimension scope: Event.
   - Event parameter: `source_tag`.
   - Display name: `Source tag`.
2. Recheck in 24-48h that `customEvent:source_tag` is available through the GA4 Data API. Data may only populate for events collected after the custom dimension is registered.
3. Run a 72h check on 2026-06-21:
   - crawler still `all_clear=true`;
   - GSC page/query rows for `/rankings` and product URLs;
   - GA4 landing-page views for `/rankings` and `/rankings/[id]`;
   - `view_product` count;
   - AI citation/extraction observations.
4. Run a 7d check on 2026-06-25 before approving any `/categories/serum`, value-analyzer, or methodology deploy batch.
