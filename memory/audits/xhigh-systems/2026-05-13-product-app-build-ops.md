# XHigh Systems Audit — Product / App Build Operations

Date: 2026-05-13
Auditor: subagent xhigh-audit-product-app-build-ops
Scope: Vista, Nash Satoshi, Glow Index, Action Arena, Dynasty Simulator, jtsomwaru.com, App Marketing OS, build queues, deployment rules, analytics connectors, Replit/Vercel docs, and Mission Control app/product tasks.

## Grade
- Before: A-
- After: A

Not A+ yet because the product/app layer still has three external/ops blockers:
1. Glow Index crawler access is still blocked by Cloudflare on discovery/category routes.
2. Web analytics are not mapped for Vista, Nash Satoshi, or Glow Index.
3. Vista App Store reporting needs `APPSTORE_VENDOR_NUMBER` / Apple reporting permission before downloads/reporting rows are available.

## Inventory

### Bootstrap budget check
Started with:
- `AGENTS.md`: 27013 bytes
- `MEMORY.md`: 18570 bytes
- `TOOLS.md`: 13689 bytes
- `HEARTBEAT.md`: 14330 bytes

All under budget.

### Product/app registry state
- `MEMORY.md` has current apps/products: jtsomwaru.com, Glow Index, Nash Satoshi, Vista, App Marketing OS, Sports GM / dynasty lane.
- `TOOLS.md` has deploy notes for jtsomwaru.com/Vercel, Glow Index/Replit, Nash Satoshi private repo, and App Marketing/Drive tooling.
- `memory/app-marketing/app-registry.md` covers Vista, Nash Satoshi, Glow Index, Action Arena, Dynasty Fantasy Football Simulator.
- `memory/app-marketing/os-spec.md` was stale for Glow Index; patched to active-but-measure-first/crawlability-blocked.

### Repos/docs inspected
- `/Users/jtsomwaru/projects/jtsomwaru-com/CLAUDE.md` — Vercel/Next build rules, portfolio/project list, llms/robots/sitemap requirements, Vista live on site.
- `/Users/jtsomwaru/projects/skincare-rankings/package.json` — Replit/Next build script: `prisma generate --schema=prisma/schema.prisma && next build`.
- `/Users/jtsomwaru/projects/nash-satoshi-2/CLAUDE.md` — startup protocol requires `PROJECT_CONTEXT.md` + `CHANGELOG.md`; build/check commands present.
- App Marketing OS files under `memory/app-marketing/`.
- Mission Control active tasks via `http://localhost:3000/api/tasks`.

### Live/product endpoint checks
Read-only GET checks:
- `https://jtsomwaru.com/blog/one-hundred-point-movie-rating-app` → 200, no Cloudflare challenge.
- `https://jtsomwaru.com/llms.txt` → 200.
- `https://nashsatoshi.com/rankings` → 200.
- `https://nashsatoshi.com/api/leaderboard` → 200.
- `https://glowindex.co/rankings` → 200.
- `https://glowindex.co/robots.txt` → 403.
- `https://glowindex.co/sitemap.xml` → 403.
- `https://glowindex.co/llms.txt` → 403.
- `https://glowindex.co/categories` → 403.
- `https://glowindex.co/categories/serum` → 403.

Nash probe:
- `python3 scripts/nash_rankings_probe.py --json --limit 5` → ok, 5 valid rankings, newest analysis age ~35.6h.

## Gate Scores

| Gate | Result | Notes |
|---|---|---|
| Build/deploy instructions current | PASS | jtsomwaru.com and Glow Replit deployment rules exist; Nash repo has CLAUDE workflow. |
| Analytics/metrics sources | PARTIAL | ReelFarm/X work; App Store metadata auth works; web analytics unmapped. |
| External blockers explicit | PASS AFTER PATCH | Glow crawler, web analytics, and App Store vendor-number blockers now explicit in docs/tasks/status. |
| MC task alignment | PASS AFTER PATCH | Updated Glow crawler + metrics tasks and created App Store vendor-number task. Generator now dedupes 13/13 active specs. |
| No stale launch checklists | PASS | Stale Vista launch task already demoted; current App Marketing tasks are action-oriented. |
| Proof/portfolio propagation | PASS | jtsomwaru.com docs include Vista; Glow portfolio task is blocked until public AI-search assets/crawler access are fixed. |
| Safe claims | PASS | Glow skincare safe-claim rules and Nash no-return/no-price-prediction guardrails are explicit. |
| Owner boundaries | PASS | JT owns external submissions/ReelFarm execution; Eve owns docs, metrics, strategy, connectors. |
| App status registry consistency | PASS AFTER PATCH | `os-spec.md` now matches Glow active status with crawlability/measurement scale blockers. |

## Patches Applied

### Documentation/status patches
- `memory/app-marketing/os-spec.md`
  - Updated Glow Index from stale `pending/blocked until app + engine + deployment are reliable` to active for durable discovery planning, but crawlability/measurement blocked before scale.
  - Added current Glow crawler blocker details.
- `memory/app-marketing/directory-submissions.md`
  - Updated Glow Index from `wait` to `draft-ready / crawlability blocked`.
  - Added crawler-fix prerequisite before directory submission reliance.
- `memory/app-marketing/metrics-automation-plan.md`
  - Replaced stale App Store “secure credential setup” wording with vendor-number/reporting-access blocker.
  - Added current web analytics readiness/log-path mapping requirement.
- `memory/app-marketing/analytics-access-needed.md`
  - Updated App Store status to metadata-auth-works / vendor-number-needed.
  - Updated cron readiness to reflect active weekly scoreboard and measurement-first behavior.
- `memory/app-marketing/implementation-plan.md`
  - Updated Measurement First and Glow registry expansion notes to current state.

### Script/connector patches
- `scripts/app_marketing_connectors/app_store_metrics.py`
  - Normalized emitted rows to include required scoreboard fields: `date`, `week_of`, `content_id_or_hook`, `url`, `views_or_impressions`.
  - Preserves non-secret `metadata_ready_vendor_number_needed` / `vendor_number_needed` blocker.
- `scripts/app_marketing_connectors/web_metrics.py`
  - Normalized blocked web analytics rows to include required scoreboard fields.
  - Rows now explain missing provider/property/log-path mapping without creating metrics inbox parse errors.
- `scripts/app_marketing_durable_discovery.py`
  - Made App Store status wording precise for vendor-number/reporting blockers.
- `scripts/app_marketing_task_generator.py`
  - Replaced stale `Vista: build App Store Connect metrics connector` task spec with current `Vista: add App Store vendor number for reporting metrics` spec.

### Metrics/status patches
- `memory/app-marketing/post-registry.jsonl`
  - Added status/check rows for Vista App Store readiness and Vista/Nash/Glow web analytics readiness.
- `memory/app-marketing/metrics-inbox.jsonl`
  - Removed four malformed connector-status rows from an intermediate run.
  - Recollected normalized App Store/web readiness rows.
- `memory/app-marketing/weekly-scoreboard.md`
  - Refreshed via collector with no metrics inbox errors.
- `memory/app-marketing/metrics-collection-status.json`
  - Refreshed with connector readiness and blocked products.
- `memory/app-marketing/generated-mission-control-tasks.json`
  - Refreshed; now 13/13 duplicate/active specs, 0 errors.

### Mission Control task changes
Updated existing tasks:
- `Glow Index: fix/verify crawler access for sitemap, llms.txt, rankings, and categories`
  - Replaced vague first action with specific `glow-crawler-access-2026-05-13.md` + Cloudflare/Replit crawler route fix path.
- `Glow Index: define metrics source before any TikTok/ReelFarm volume`
  - Replaced vague metrics-source task with concrete account-map + connector validation instructions.

Created one task:
- `Vista: add App Store vendor number for reporting metrics`
  - First action: securely add `APPSTORE_VENDOR_NUMBER`, then run App Store connector + collector.
  - Done state: `app-store-metrics-status.json` reports `sales_report_ready` or precise Apple-side permission/agreement blocker.

## Validation Results

Commands/gates run:
- `wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md` → all under budget.
- Read-only endpoint checks for jtsomwaru.com, Nash, Glow → results above.
- `python3 scripts/nash_rankings_probe.py --json --limit 5` → ok, valid live rankings.
- `python3 scripts/app_marketing_connectors/app_store_metrics.py` → metadata auth ok; `reporting_status=vendor_number_needed`.
- `python3 scripts/app_marketing_connectors/web_metrics.py` → `provider_or_property_mapping_needed`; blocked products Vista/Nash/Glow.
- `python3 scripts/app_marketing_collect_metrics.py` → posts=51, metrics_rows=42, appended=4, no inbox errors after patch.
- `python3 scripts/app_marketing_analyze.py` → ok.
- `python3 scripts/app_marketing_experiment_calendar.py` → ok, 4 experiments.
- `python3 scripts/app_marketing_durable_discovery.py` → ok, selected Glow directory/crawlability action.
- `python3 scripts/app_marketing_task_generator.py --json` → total_specs=13, duplicates=13, created=0, errors=[].
- `python3 -m py_compile scripts/app_marketing_task_generator.py scripts/app_marketing_durable_discovery.py scripts/app_marketing_collect_metrics.py scripts/app_marketing_connectors/*.py` → ok.
- Mission Control API PATCH/POST calls for task updates/creation → 200/success.

## Remaining Blockers

1. **Glow crawler access / public AI-search assets**
   - Current state: 403 Cloudflare challenge for `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/categories`, `/categories/serum`.
   - Task: `Glow Index: fix/verify crawler access for sitemap, llms.txt, rankings, and categories`.
   - Related existing task: `Fix Glow Index public AI-search assets before portfolio card`.
   - Done state: all discovery/category URLs return 200 without Cloudflare challenge.

2. **Web analytics source mapping**
   - Current state: `web-analytics-status.json` blocks Vista, Nash Satoshi, Glow Index.
   - Task: `Glow Index: define metrics source before any TikTok/ReelFarm volume`; Vista/Nash also need GA4/Search Console/Vercel/Plausible/PostHog/local log mapping.
   - Done state: each active app has `property_id`, `site_url`, or `log_path` in `account-map.json`, and connector status no longer blocks it.

3. **Vista App Store reporting**
   - Current state: metadata auth works; reporting needs `APPSTORE_VENDOR_NUMBER` / Apple reporting permissions.
   - Task: `Vista: add App Store vendor number for reporting metrics`.
   - Done state: App Store status reports `sales_report_ready` or precise Apple agreement/role blocker.

## Final Judgment
Product/App Build Ops is now **A**: safe, deployment-aware, measurable where current connectors allow, and aligned to JT's passive-income/app priorities.

A+ requires closing the three remaining blockers above, especially Glow crawler access and at least one reliable web analytics source.
