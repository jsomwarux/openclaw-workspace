# App Marketing OS — Metrics Automation Plan

## Goal
Automate app/content performance measurement as much as possible so JT does not manually track every post.

Manual metrics entry remains a fallback only.

## Platform-by-Platform Feasibility

### X / Twitter
Feasibility: high if X API access/auth is available.

What can be automated:
- public metrics: likes, replies, reposts/retweets, quotes, bookmarks if available by endpoint/tier
- owned/private metrics with user auth: impressions and richer engagement metrics, depending on X API tier and permissions
- post lookup by URL/id
- account-level recent posts

Best path:
1. Store posted X post URLs/IDs in App Marketing OS or existing content logs.
2. Use X API to fetch metrics daily/weekly.
3. Append normalized rows to `memory/app-marketing/metrics-inbox.jsonl`.
4. Run `python3 scripts/app_marketing_metrics.py`.

Open requirement:
- Verify current X API credentials/access tier and whether owned-account private metrics are available.

Fallback:
- public metric scrape/search for likes/replies/reposts only; no impressions.

### Reddit
Feasibility: medium-high for public engagement; low for true impressions/views.

What can be automated:
- score/upvotes-ish count
- comments count
- removed/deleted status
- subreddit
- permalink
- account post history if authenticated or public enough

What likely cannot be reliably automated:
- true post impressions/views/insights for all posts.

Best path:
1. Store Reddit post URLs/permalinks.
2. Fetch public JSON/OAuth API metrics: score, comments, removal status.
3. Treat removal/non-removal and comments as more important than raw upvote count.
4. Normalize to metrics inbox.

Fallback:
- user sends URL only; Eve fetches public metrics.

### TikTok / ReelFarm
Feasibility: uncertain via ReelFarm; possible via TikTok APIs only with the right account/API permissions.

Known state:
- ReelFarm `/videos` endpoint worked and returns video records/status metadata.
- Sampled ReelFarm endpoint did not expose performance metrics.
- JT laptop owns ReelFarm execution, so Mac mini should not duplicate posting.

Possible automation paths, ranked:
1. ReelFarm API metrics endpoint if it exists — best because it aligns with current workflow.
2. TikTok Display/Business/creator APIs if account type and permissions allow owned video metrics.
3. Laptop-exported CSV/JSON from ReelFarm/TikTok analytics synced to workspace.
4. Screenshot OCR only as last resort.

Best immediate next step:
- Inspect ReelFarm API docs/endpoints for analytics support.
- If absent, create laptop-side export convention: one CSV/JSON dropped weekly into `memory/app-marketing/imports/`.

### App Store / Vista
Feasibility: high once Apple reporting vendor number/permissions are available.

Current state:
- `scripts/app_marketing_connectors/app_store_metrics.py` exists and passes non-secret readiness.
- App Store metadata auth works for Vista (`VISTA - Movie Taste Profiles`).
- Reporting is blocked on `APPSTORE_VENDOR_NUMBER` / Apple reporting permissions, not on missing metadata credentials.
- Status file: `memory/app-marketing/app-store-metrics-status.json`.

What can be automated after reporting access:
- downloads / app units
- product page views or equivalent acquisition/reporting rows where Apple permits
- ratings/reviews where endpoint permissions allow

Best path:
1. Securely add `APPSTORE_VENDOR_NUMBER` in the approved env/config surface; never paste it into docs/chat.
2. Run `python3 scripts/app_marketing_connectors/app_store_metrics.py`.
3. If `reporting_status` becomes `sales_report_ready`, normalize Vista rows into `metrics-inbox.jsonl` via `scripts/app_marketing_collect_metrics.py`.
4. If Apple returns role/agreement errors, create a one-time JT Apple-side action task with the exact error.

Do not store Apple private key, vendor number, or account secrets in workspace docs.

### Website Analytics — Nash / Vista / Glow
Feasibility: depends on analytics provider.

Current state:
- `scripts/app_marketing_connectors/web_metrics.py` emits readiness and supports local CSV/log paths.
- Mapping template: `memory/app-marketing/web-analytics-mapping-template.md`.
- `memory/app-marketing/web-analytics-status.json` currently reports Vista, Nash Satoshi, and Glow Index blocked because no GA4/Search Console/Vercel/Plausible/PostHog property or local `log_path` is mapped.

Options:
- GA4 / Google Search Console property IDs with service-account access.
- Vercel Analytics API if available.
- Plausible/PostHog if installed.
- Server logs/local CSV export if self-hosted/Replit logs can be exported.

Best path:
- Add one concrete source per app to `memory/app-marketing/account-map.json` (`property_id`, `site_url`, `log_path`, `vercel_project`, `plausible_site_id`, or `posthog_project_id`).
- Run `python3 scripts/app_marketing_connectors/web_metrics.py` and verify the app leaves `blocked_products`.
- Add provider-specific fetching only after the source mapping exists; do not guess providers.

## Recommended Architecture

`memory/app-marketing/post-registry.jsonl`
- canonical record of what was actually posted
- fields: date, product_slug, platform, account, post_id, url, hook, source_system, campaign, content_id

`memory/app-marketing/metrics-inbox.jsonl`
- normalized raw metric rows from all connectors
- already created

`scripts/app_marketing_collect_metrics.py`
- orchestrator
- reads post registry
- calls platform connectors
- writes normalized rows to metrics inbox
- calls `scripts/app_marketing_metrics.py`

Connector modules:
- `scripts/app_marketing_connectors/x_metrics.py`
- `scripts/app_marketing_connectors/reddit_metrics.py`
- `scripts/app_marketing_connectors/reelfarm_metrics.py`
- `scripts/app_marketing_connectors/app_store_metrics.py`
- `scripts/app_marketing_connectors/web_metrics.py`

## Automation Cadence

Daily lightweight:
- X public/private post metrics
- Reddit score/comments/removal
- ReelFarm/TikTok if API exists

Weekly deeper:
- App Store Connect
- website analytics
- scoreboard interpretation
- double-down/retire recommendations

## Decision Layer

Each week, App Marketing OS should label:
- winner: materially beats baseline
- promising: above average but needs repeat
- neutral: no signal
- loser: below baseline 3 times or removed/flagged
- blocked: missing metrics

Do not increase volume until enough rows exist to establish baseline.

## Next Build Order

1. Create `post-registry.jsonl` and connector skeletons.
2. Implement Reddit public metrics first — easiest and no private credentials likely needed for basic score/comments.
3. Implement X metrics if credentials/access exist.
4. Inspect ReelFarm docs/API for metrics endpoint; if none, define laptop CSV/JSON export.
5. Add Vista App Store vendor-number/reporting access, then normalize App Store rows if Apple permits reporting.
6. Add concrete web analytics mappings/log paths for Vista, Nash, and Glow; until then weekly scoreboard must label those products `MEASURE_FIRST` for web metrics.
