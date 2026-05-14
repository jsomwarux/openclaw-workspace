# App Marketing OS — Web Analytics Mapping Template

Purpose: give each active app exactly one measurable web analytics source before increasing content volume.

## Where to map sources
Edit: `memory/app-marketing/account-map.json`

Accepted source groups/keys:
- `google_analytics`: GA4 rows with `property_id`.
- `search_console`: Search Console rows with `site_url`.
- `web_analytics`: generic rows for Vercel/Plausible/PostHog/local CSV/log exports.

Accepted mapping fields:
- `property_id` — GA4 property ID or provider property ID.
- `site_url` — Search Console URL property/domain property.
- `log_path` — local CSV/export path with at least `date,page,views` or `date,page,pageviews`.
- `vercel_project` — Vercel project name/id when Vercel Analytics API is wired.
- `plausible_site_id` — Plausible site identifier.
- `posthog_project_id` — PostHog project identifier.

## JSON examples

```json
{
  "google_analytics": [
    {
      "product_slug": "vista",
      "provider": "ga4",
      "property_id": "GA4_PROPERTY_ID_HERE",
      "status": "mapped_pending_auth",
      "notes": "Requires GA4 service-account Viewer access via secure env path."
    }
  ],
  "search_console": [
    {
      "product_slug": "glow-index",
      "provider": "search_console",
      "site_url": "https://glowindex.co/",
      "status": "mapped_pending_auth"
    }
  ],
  "web_analytics": [
    {
      "product_slug": "nash-satoshi",
      "provider": "local_csv",
      "log_path": "~/exports/nash-satoshi-web-analytics.csv",
      "status": "mapped_local_export"
    }
  ]
}
```

## Active products that must not stay unmapped
- `vista`
- `nash-satoshi`
- `glow-index`

## Validation

```bash
cd ~/.openclaw/workspace
python3 scripts/app_marketing_connectors/web_metrics.py
python3 scripts/app_marketing_collect_metrics.py
```

Done state: `memory/app-marketing/web-analytics-status.json` removes the app from `blocked_products`, or records a precise provider/auth/log-path blocker.

Guardrails:
- Do not paste GA4/Search Console/Vercel/Plausible/PostHog secrets into this file or account-map.
- Use env/approved secure config for credentials only.
- If all three apps are blocked for two consecutive weekly reviews, do not increase ReelFarm/TikTok/social volume. Fix measurement first.
