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
Needed:
1. GA4 property ID for each app/site:
   - Vista:
   - Nash Satoshi:
   - Glow Index, later:
2. Auth method. Best option: service account with Viewer access to the GA4 properties.
3. Secure credential path/env var, not pasted into docs:
   - `GOOGLE_APPLICATION_CREDENTIALS=/secure/path/service-account.json`
   - or equivalent existing Google auth if GA Data API access is available.

Preferred implementation:
- Add `scripts/app_marketing_connectors/ga4_metrics.py`.
- Fetch sessions/users/pageviews/events by landing page and source/medium.
- Normalize rows into `metrics-inbox.jsonl`.

### App Store Connect / Vista
Needed tomorrow:
1. Issuer ID
2. Key ID
3. Private key file path (`.p8`) stored securely outside repo/docs
4. App ID / bundle ID for Vista

Preferred env:
- `APPSTORE_ISSUER_ID`
- `APPSTORE_KEY_ID`
- `APPSTORE_PRIVATE_KEY_PATH`
- `APPSTORE_APP_ID` or app-specific registry value

Do not paste private key contents into chat/docs.

### X User Context — Optional Upgrade
Not required for baseline.
Needed only if we want private owned metrics:
- OAuth user-context credentials/scopes for owned posts.
- Use only if click/profile-click metrics are worth the setup.

## Cron Readiness
Do not create weekly scoreboard cron until:
- Discovery + collect pipeline runs idempotently.
- At least one week of ReelFarm/X metrics is populated.
- GA4/App Store access path is clear or explicitly deferred.

Current command sequence:
```bash
cd ~/.openclaw/workspace
python3 scripts/app_marketing_discover_posts.py
python3 scripts/app_marketing_collect_metrics.py
```
