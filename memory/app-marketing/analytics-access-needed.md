# App Marketing OS — Analytics Access Needed

## Already Working

### ReelFarm / TikTok
Status: working.
- API key exists in env.
- `GET /tiktok/accounts` works.
- `GET /tiktok/posts` works and returns views, likes, comments, shares, bookmarks.
- Discovery now auto-populates `post-registry.jsonl`.
- Metrics collector updates `metrics-inbox.jsonl` and `weekly-scoreboard.md`.

Mapped accounts:
- `@nashsatoshi` → `nash-satoshi`
- `@mashed386` → `vista`
- `@glow.index` → `glow-index`

### X
Status: partially working.
- `X_BEARER_TOKEN` exists in env.
- Public metrics connector works for tweet IDs/URLs.
- Account discovery works for recent posts from `@NashSatoshi` and `@jts_14`.
- Public metrics include impressions, likes, replies, reposts/quotes, bookmarks when returned.

Limit:
- Private metrics such as URL clicks/profile clicks require user-context auth, not just bearer token.
- Shared `@jts_14` account posts are filtered conservatively to avoid polluting app analytics.

## Needed From JT / Setup

### Google Analytics / GA4
Status: blocked on property IDs/auth/provider mapping. `scripts/app_marketing_connectors/web_metrics.py` emits readiness/status so weekly reviews can identify the exact gap without asking JT for manual daily metrics. Mapping schema/template: `memory/app-marketing/web-analytics-mapping-template.md`.

Needed:
1. GA4 property ID for each app/site:
   - Vista: unmapped
   - Nash Satoshi: unmapped
   - Glow Index: unmapped
2. Auth method. Best option: service account with Viewer access to the GA4 properties.
3. Secure credential path/env var, not pasted into docs:
   - `GOOGLE_APPLICATION_CREDENTIALS=/secure/path/service-account.json`
   - or equivalent existing Google auth if GA Data API access is available.

Preferred implementation:
- Add one concrete mapping per app in `memory/app-marketing/account-map.json` using the template file.
- Then add provider-specific fetching only for mapped sources; do not guess providers.
- Normalize sessions/users/pageviews/events by landing page and source/medium into `metrics-inbox.jsonl`.

### App Store Connect / Vista
Status: metadata auth works; reporting metrics blocked on vendor-number/reporting access.
- Existing env/config includes `APPSTORE_ISSUER_ID`, `APPSTORE_KEY_ID`, `APPSTORE_PRIVATE_KEY_PATH`, and `APPSTORE_VISTA_APP_ID`.
- Smoke test verified Vista app metadata: app id `6758186885`, bundle `com.jsomwaru.vista`, name `VISTA - Movie Taste Profiles`.
- `scripts/app_marketing_connectors/app_store_metrics.py` has a non-secret readiness probe and status writer.
- Current status file: `memory/app-marketing/app-store-metrics-status.json`.
- Current known blocker: `reporting_status: vendor_number_needed` / Apple reporting permissions.
- Mission Control task created: `Vista: add App Store vendor number for reporting metrics`.

Still to implement/verify:
1. Securely add `APPSTORE_VENDOR_NUMBER` in the approved env/config surface; do not paste it into docs/chat.
2. Run the App Store connector and, if Apple permits reporting, normalize downloads/product-page/reporting rows into `metrics-inbox.jsonl`.
3. If Apple returns agreement/permission errors, JT must complete Apple-side agreements or grant the API key the required reporting permissions.

Do not paste private key, vendor number, or Apple account secrets into chat/docs.

### X User Context — Optional Upgrade
Not required for baseline.
Needed only if we want private owned metrics:
- OAuth user-context credentials/scopes for owned posts.
- Use only if click/profile-click metrics are worth the setup.

## Cron Readiness
Weekly scoreboard cron is active; it must stay measurement-first:
- Discovery + collect pipeline runs idempotently.
- ReelFarm/X metrics are populated when available.
- GA4/App Store blocked status must generate measurement-fix tasks, not more content-volume tasks.

Current command sequence:
```bash
cd ~/.openclaw/workspace
python3 scripts/app_marketing_discover_posts.py
python3 scripts/app_marketing_collect_metrics.py
```
