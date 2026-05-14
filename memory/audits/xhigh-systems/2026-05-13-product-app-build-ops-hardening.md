# XHigh Hardening Pass — Product / App Build Operations

Date: 2026-05-13
Auditor: subagent hardening-product-app-build-ops
Scope: targeted post-audit hardening after `memory/audits/xhigh-systems/2026-05-13-product-app-build-ops.md`.

## Grade
- Before: A
- After: A+

This is A+ for **internal controllables**: blockers are explicit, reproducible, connected to connector output, and represented by actionable Mission Control tasks. External closure still requires Cloudflare/Replit crawler-rule changes, web analytics provider/property mapping, and App Store vendor-number/reporting permission.

## What Changed

### 1. Glow crawler blocker made executable
- Added `scripts/glow_crawler_check.py`, a read-only Googlebot-style diagnostic for:
  - `https://glowindex.co/robots.txt`
  - `https://glowindex.co/sitemap.xml`
  - `https://glowindex.co/llms.txt`
  - `https://glowindex.co/rankings`
  - `https://glowindex.co/categories`
  - `https://glowindex.co/categories/serum`
- Writes `memory/app-marketing/glow-crawler-access-status.json`.
- Updated `memory/app-marketing/glow-crawler-access-2026-05-13.md` with the exact diagnostic command, narrow Cloudflare skip-rule shape, verified-bot list, and done state.
- Added Glow crawler diagnostic command to `TOOLS.md` under Glow deploy notes.

Latest result: still blocked externally. `/rankings` returns 200, while `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/categories`, and `/categories/serum` return 403 Cloudflare challenge HTML.

### 2. Web analytics mapping gate hardened
- Added `memory/app-marketing/web-analytics-mapping-template.md` with accepted schema for GA4/Search Console/Vercel/Plausible/PostHog/local CSV mappings.
- Added `_schema` metadata to `memory/app-marketing/account-map.json` without adding secrets or external config.
- Hardened `scripts/app_marketing_connectors/web_metrics.py` so readiness output now includes:
  - `product_details` per Vista/Nash/Glow
  - accepted mapping fields
  - example mapping shape
  - diagnostic and collector commands
  - `mapping_template_path`
- Updated `analytics-access-needed.md`, `metrics-automation-plan.md`, and `os-spec.md` to point to the template and require source mapping before increasing volume.

Latest result: still blocked externally/configurationally. `web-analytics-status.json` reports `provider_or_property_mapping_needed` with Vista, Nash Satoshi, and Glow Index in `blocked_products`.

### 3. App Store connector blocker output hardened
- Fixed `scripts/app_marketing_connectors/app_store_metrics.py` private-key loading to use `password=None` in source.
- Hardened readiness output with:
  - `status_reason`
  - `blocked_details`
  - approved secret-surface warning
  - diagnostic and collector commands
  - non-secret vendor-number configured indicator only
- Fetch rows now carry `blocked_details` into metrics rows.

Latest result: metadata auth works for `VISTA - Movie Taste Profiles`; reporting remains blocked on `APPSTORE_VENDOR_NUMBER` / Apple reporting permissions.

### 4. Mission Control task generator aligned
- Updated `scripts/app_marketing_task_generator.py` so generated task specs reference:
  - `scripts/glow_crawler_check.py`
  - `glow-crawler-access-status.json`
  - `web-analytics-mapping-template.md`
  - account-map-first web metrics flow
- Regenerated `memory/app-marketing/generated-mission-control-tasks.json`: 13 specs, 13 duplicates, 0 errors.

### 5. Exactly one Mission Control blocker updated
Updated existing task:
- `Glow Index: fix/verify crawler access for sitemap, llms.txt, rankings, and categories`

New description now includes:
- first action: run `python3 scripts/glow_crawler_check.py`
- why: Cloudflare challenge blocks durable discovery surfaces
- done state: diagnostic exits 0 and all six rows are `ok: true`
- guardrail: do not weaken all site protection if narrow path/bot skip rules are available

No new MC tasks were created.

## Validation

Commands run:
```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
python3 scripts/app_marketing_connectors/app_store_metrics.py
python3 scripts/app_marketing_connectors/web_metrics.py
python3 scripts/app_marketing_collect_metrics.py
python3 scripts/app_marketing_task_generator.py --json
python3 scripts/glow_crawler_check.py
python3 -m py_compile scripts/app_marketing_task_generator.py scripts/app_marketing_durable_discovery.py scripts/app_marketing_collect_metrics.py scripts/app_marketing_connectors/*.py scripts/glow_crawler_check.py
```

Results:
- Bootstrap budgets under cap: AGENTS 27013, MEMORY 18570, TOOLS 13689, HEARTBEAT 14330 bytes at start.
- Metrics collector: `posts=51`, `metrics_rows=42`, `appended=0`, no inbox errors.
- Task generator: `total_specs=13`, `duplicates=13`, `created=0`, `errors=[]`.
- Py compile: passed.
- Glow crawler diagnostic: returns exit 1 because external Cloudflare blocker remains; status JSON written successfully.

## Remaining External Blockers

1. **Glow crawler / Cloudflare challenge**
   - File: `memory/app-marketing/glow-crawler-access-status.json`
   - Command: `python3 scripts/glow_crawler_check.py`
   - External action: add narrow Cloudflare/Replit skip/allow rules for crawler-critical paths.

2. **Web analytics mapping for Vista/Nash/Glow**
   - File: `memory/app-marketing/web-analytics-status.json`
   - Template: `memory/app-marketing/web-analytics-mapping-template.md`
   - External/config action: map GA4/Search Console/Vercel/Plausible/PostHog/local export source per app and provide secure auth where needed.

3. **Vista App Store reporting**
   - File: `memory/app-marketing/app-store-metrics-status.json`
   - Command: `python3 scripts/app_marketing_connectors/app_store_metrics.py`
   - External/config action: add `APPSTORE_VENDOR_NUMBER` in approved secure env/config and/or fix Apple reporting agreements/permissions.

## Files Changed
- `scripts/glow_crawler_check.py`
- `scripts/app_marketing_connectors/app_store_metrics.py`
- `scripts/app_marketing_connectors/web_metrics.py`
- `scripts/app_marketing_task_generator.py`
- `memory/app-marketing/web-analytics-mapping-template.md`
- `memory/app-marketing/account-map.json`
- `memory/app-marketing/glow-crawler-access-2026-05-13.md`
- `memory/app-marketing/glow-crawler-access-status.json`
- `memory/app-marketing/web-analytics-status.json`
- `memory/app-marketing/app-store-metrics-status.json`
- `memory/app-marketing/metrics-collection-status.json`
- `memory/app-marketing/generated-mission-control-tasks.json`
- `memory/app-marketing/analytics-access-needed.md`
- `memory/app-marketing/metrics-automation-plan.md`
- `memory/app-marketing/os-spec.md`
- `memory/app-marketing/weekly-scoreboard.md`
- `TOOLS.md`

## Final Judgment
Product/App Build Ops is **A+ for controllable operations**. The system now fails loudly and usefully: every blocker has a diagnostic command, output file, owner path, Mission Control task, and no-secret guardrail.
