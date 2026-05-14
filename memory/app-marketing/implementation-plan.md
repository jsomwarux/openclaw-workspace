# App Marketing OS — Implementation Plan

## Decision
App marketing is now a first-class North Star system. The goal is to create reusable distribution infrastructure for current and future apps while preserving the existing systems that already work. JT's laptop owns ReelFarm slideshow execution; Eve owns strategy, tracking, assets, and adjacent distribution systems.

## Phase 1 — Foundation (done / in progress)
Status: started 2026-05-06

Completed:
- Audited current systems.
- Created OS spec.
- Created app registry.
- Created weekly scoreboard template.
- Created directory/backlink backlog.
- Created SEO backlog.
- Created ASO checklist.
- Created future-app onboarding template.
- Created metrics inbox + parser: `memory/app-marketing/metrics-inbox.jsonl` and `scripts/app_marketing_metrics.py`.
- Created post registry + automated collector skeleton: `memory/app-marketing/post-registry.jsonl`, `scripts/app_marketing_collect_metrics.py`, and `scripts/app_marketing_connectors/`.
- Created first public connector: Reddit public score/comments/removal-status fetcher.
- Created asset map: `memory/app-marketing/asset-map.md`.

Files:
- `memory/app-marketing/audit-2026-05-06.md`
- `memory/app-marketing/os-spec.md`
- `memory/app-marketing/app-registry.md`
- `memory/app-marketing/weekly-scoreboard.md`
- `memory/app-marketing/directory-submissions.md`
- `memory/app-marketing/seo-backlog.md`
- `memory/app-marketing/aso-checklist.md`
- `memory/app-marketing/future-app-template.md`

## Phase 2 — Measurement First
Priority: highest

Why:
- Current Vibe Marketing performance log has only 6 entries and all metrics are pending/zero.
- Queue has 119 valid entries but weak feedback.
- The system cannot optimize without true performance data.

Tasks:
1. Do not duplicate JT's laptop ReelFarm slideshow automation.
2. API-first measurement: use `memory/app-marketing/post-registry.jsonl` as canonical list of posted items and `scripts/app_marketing_collect_metrics.py` to collect available platform metrics.
3. Use connector priority: Reddit public metrics first; X API if credentials/tier allow; ReelFarm/TikTok analytics if endpoint/export exists; App Store Connect for Vista after secure metadata auth plus vendor-number/reporting access; web analytics after a concrete provider/property/log path is mapped.
4. Manual metrics inbox remains fallback only: append rows to `memory/app-marketing/metrics-inbox.jsonl`, then run `python3 scripts/app_marketing_metrics.py`.
5. Keep the weekly App Marketing Scoreboard cron measurement-first: if connector status reports blocked products, generate measurement-fix tasks instead of more content volume.

Current done state:
- Metrics inbox exists.
- Parser exists and py_compile passes.
- Empty inbox writes a clear “No metrics entries yet” block to the scoreboard.

Remaining done state:
- Weekly scoreboard shows real Vista and Nash metrics from JT laptop/ReelFarm/X/Reddit outputs.
- `memory/app-marketing/app-store-metrics-status.json` reports Vista App Store reporting ready or a precise Apple-side blocker; current known blocker is `APPSTORE_VENDOR_NUMBER` / reporting permissions.
- `memory/app-marketing/web-analytics-status.json` has at least one concrete source mapped for Vista/Nash/Glow, or precise provider blockers.
- Performance log rows move from `pending` to actual score labels once metrics are available.

## Phase 3 — Asset Fixes
Priority: high

Tasks:
1. Confirm whether JT's laptop ReelFarm setup already has the needed Vista/Nash/Glow screenshots.
2. If yes, do not recreate Drive screenshot automation. Instead document screenshot asset locations and naming conventions in `memory/app-marketing/asset-map.md`.
3. If Mac mini systems still generate review docs, keep Drive screenshot folders as optional support assets, not blockers.

Done state:
- Eve knows where canonical screenshots live and can reference them in prompts/strategy.
- No duplicate screenshot pipeline is created unless needed.

## Phase 4 — Durable Discovery
Priority: high

Tasks:
1. Create Vista directory submission pack.
2. Create Nash Satoshi directory submission pack.
3. Draft first SEO page outline for Vista: `1–100 movie rating app` or `Letterboxd alternative for precise movie ratings`.
4. Draft first SEO page outline for Nash: `Game theory crypto analysis` or `Nash Satoshi methodology`.
5. Decide where pages live: app site, jtsomwaru.com, or separate landing pages.

Done state:
- At least one directory submission pack per active app.
- At least one SEO page outline per active app.

## Phase 5 — Product Registry Expansion
Priority: medium-high

Tasks:
1. Add Action Arena to the relevant marketing registry only after there is a landing/waitlist page or beta target.
2. Keep Action Arena primarily in Sports GM/@dynastyjig until launch assets exist.
3. Add Dynasty Fantasy Football Simulator separately if/when it needs marketing automation.
4. Glow Index is active for durable discovery planning, but remains crawlability/measurement blocked before scale; fix crawler access and metric source before pSEO expansion or TikTok/ReelFarm volume.

Done state:
- No product conflation.
- No generic product-promo content for sports apps.

## Phase 6 — Patch Existing Generators Carefully
Priority: after Phases 2–5

Potential Vibe Marketing patches:
- Tighten Reddit rule: default to no product mention unless subreddit-safe; skip if no compliant community-native angle.
- Add App Marketing OS registry read step.
- Add weekly scoreboard write/read step.
- Add directory/SEO/ASO action recommendation in Telegram summary.

Potential Sports GM patches:
- Add Action Arena prelaunch waitlist metric once page exists.
- Keep product references banned by default.

Do not patch until there is a clear owner surface and regression check.

## Immediate Next Best Action
Build/verify the measurement handoff, not ReelFarm automation. Metrics are still the bottleneck, but execution lives on JT's laptop.

Recommended next task:
- Define a lightweight weekly metrics input format for JT's laptop/ReelFarm output, then have Eve update the App Marketing scoreboard from that input.

## Phase 2 Update — Planned-to-Posted Reconciliation (2026-05-07)
Status: implemented

What changed:
- `scripts/app_marketing_discover_posts.py` now treats planned registry rows as canonical.
- When ReelFarm/TikTok or X discovery finds a live post matching a planned draft by platform, product, account, date window, and hook similarity, it updates the planned row with exact `url_or_id`, `post_id`, `video_id`, `status: posted`, `posted_date`, `discovered_at`, and `planned_url_or_id`.
- If no planned row matches, discovery appends a new live row as before.
- `scripts/app_marketing_connectors/reelfarm_metrics.py` now exposes `post_id`, `video_id`, and account in normalized rows so registry and metrics can preserve exact identifiers.

Verification:
- `python3 -m py_compile scripts/app_marketing_discover_posts.py scripts/app_marketing_connectors/reelfarm_metrics.py scripts/app_marketing_collect_metrics.py` passed.
- Current live registry run: no new reconciliation because the two planned Nash methodology assets have not been posted yet.
- Temp-registry regression test passed: one planned row updated to one posted row, with no duplicate appended.

Done state:
- Approved/planned app-marketing drafts can now become traceable posted rows automatically once ReelFarm/X discovery sees the live post.
- This closes the draft -> posted -> metric chain for mapped accounts.

## Phase 2 Update — Weekly Experiment Calendar (2026-05-07)
Status: implemented

What changed:
- Added `scripts/app_marketing_experiment_calendar.py`.
- Script generates `memory/app-marketing/experiment-calendar.md` from metrics, optimization rules, latest test brief, and planned registry rows.
- Calendar defines named weekly experiments with hypothesis, channel, post plan, success threshold, retire/rework rule, and evidence.
- Current experiments: Vista rating precision retest, Nash ranking/model update, Nash model-consensus slideshow.
- Product-content agent now must map every generated item to a named experiment or skip with `NO_EXPERIMENT_MATCH`.
- Weekly scoreboard cron now runs experiment calendar after analyze and uses it for next-test recommendations.

Done state:
- Product marketing now has a measurement-backed decision layer: posts are tests with success/failure rules, not random output.

## Phase 4 Update — Durable Discovery Layer (2026-05-07)
Status: started

What changed:
- Added `scripts/app_marketing_durable_discovery.py`.
- Generated `memory/app-marketing/durable-discovery-plan.md` with one weekly compounding discovery action and backlog queue.
- Created `memory/app-marketing/seo-briefs-vista-1-100-movie-rating-app.md` as the first Vista SEO page brief tied to the measured rating-precision winner.
- Created `memory/app-marketing/directory-packs-nash-satoshi.md` as a draft-only Nash directory submission pack. No external submissions made.

Done state now achieved:
- Durable discovery is no longer just a backlog; it has a weekly action surface.
- First SEO brief and first directory pack exist for active apps.

## Phase 4 Update — Vista SEO Page Implemented (2026-05-07)
Status: implemented on jtsomwaru.com

What changed:
- Added Vista SEO blog page to jtsomwaru.com: `/blog/one-hundred-point-movie-rating-app`.
- Page targets `1–100 movie rating app` / precise movie ratings and links to the Vista project page.
- jtsomwaru.com sitemap includes blog posts automatically through `getAllPosts()`.
- `public/llms.txt` updated so AI crawlers see the Vista precision-rating page.
- Verification: `npm run build` and `npm run lint` passed.

## Phase 4 Update — Vista Directory Pack (2026-05-07)
Status: draft-ready

What changed:
- Verified Vista SEO page is live at `https://jtsomwaru.com/blog/one-hundred-point-movie-rating-app`.
- Verified sitemap includes the Vista SEO page and `llms.txt` includes the Vista 1–100 movie rating resource.
- Created `memory/app-marketing/directory-packs-vista.md` with Product Hunt, Uneed, AlternativeTo, Indie Hackers, and niche-directory copy.
- Updated `memory/app-marketing/asset-map.md` with current canonical Vista screenshot paths from jtsomwaru.com.

Guardrail:
- No external directory submissions made. Submit only after JT approves directory target and screenshots.

## Follow-up Task — Vista Uneed Submission (2026-05-07)
Status: pending JT review/submission

First action:
- Open `memory/app-marketing/directory-packs-vista.md` and review the `Uneed Submission — Review-Ready` section.

Why it matters:
- Vista now has a live 1–100 movie rating SEO page, and Uneed is a low-ceremony durable backlink/listing before any Product Hunt launch.

Done looks like:
- Choose 3–5 screenshots from `~/projects/jtsomwaru-com/public/images/vista/`.
- Submit Vista to Uneed.
- Paste the submitted URL back so Eve can update `directory-submissions.md` and tracking.

Note:
- Mission Control task creation returned HTTP 500 twice on 2026-05-07, so this follow-up is tracked here until MC task API recovers.

## Phase 4 Update — Glow Index Active (2026-05-07)
Status: priority changed

What changed:
- JT clarified Glow Index has launched and is live.
- Verified canonical production URL `https://glowindex.co` returns 200.
- Updated `memory/app-marketing/app-registry.md`: Glow Index is now active, not pending.
- Updated `memory/app-marketing/seo-backlog.md`: Glow is now the highest active pSEO/GEO opportunity.
- Updated `MEMORY.md` Current Apps / Products with live Glow status and marketing guardrails.

Strategic implication:
- The next best automated app marketing build is a reusable pSEO/GEO module, piloted on Glow Index with a small safe 3-page/template pilot before scaling to hundreds/thousands of pages.

Guardrails:
- No medical/dermatology claims.
- No diagnosis/treatment wording.
- No fake testimonials or before/after claims.
- No large programmatic page generation until data shape, uniqueness threshold, crawl/index rules, and safe-claim template are defined.

## Next Build Task — Glow pSEO/GEO Data Audit (2026-05-07)
Status: next recommended implementation task

First action:
- In `~/projects/skincare-rankings`, inspect Prisma/production-safe product data shape and generate `memory/app-marketing/glow-pseo-data-audit.md`.

Why it matters:
- Glow Index is now live at `https://glowindex.co` and is the best first pilot for reusable programmatic SEO/GEO. But safe pSEO requires knowing product counts, analyzed counts, category distribution, score JSON consistency, image coverage, and whether comparison/category pages can be unique enough.

Done looks like:
- Data audit file exists.
- It identifies the first 3 safe pilot pages/templates.
- It confirms whether to enhance existing `/rankings/[id]` pages first or add new `/products/[slug]`, `/categories/[category]`, and `/compare/[a]-vs-[b]` routes.
- It lists claim guardrails and noindex rules for unanalyzed/thin pages.

## Phase 4 Update — Glow pSEO Data Audit (2026-05-07)
Status: completed static/code audit; runtime DB audit still needed

What changed:
- Created `memory/app-marketing/glow-pseo-data-audit.md` from live URL verification and repo inspection.
- Confirmed Glow has strong pSEO/GEO foundations already: product detail route, dynamic sitemap, AI-crawler-friendly robots, Product JSON-LD, and score dimensions.
- Identified safest pilot sequence: upgrade `/rankings/[id]` product pages first, then add `/categories/[category]`, then add one comparison page only after runtime analyzed-data check.

Important blocker:
- Direct one-off Prisma query failed because Prisma 7 generated client requires project adapter config. Use the app's existing `lib/db.ts` path or a runtime-safe audit script before making indexable category/comparison pages.

Recommendation:
- Next build step is `glow-pseo-data-audit-runtime.md`: production/runtime product counts, analyzed counts, category counts, valid score JSON, image coverage, and comparison candidates.

## Phase 4 Update — Glow Product Page GEO Patch (2026-05-07)
Status: local commit created

Commit:
- `79fed5f Improve Glow product page GEO` in `~/projects/skincare-rankings`

Changes:
- Product detail pages at `/rankings/[id]` now include a direct-answer `Glow Index summary` block for AI extraction.
- Added visible FAQ section with non-medical safety framing.
- Added FAQPage and BreadcrumbList JSON-LD.
- Replaced potentially ambiguous `AggregateRating` schema with safer `additionalProperty` fields for `Glow Index AI consensus score` and tier.
- Updated `public/llms.txt` with canonical `https://glowindex.co`, current scoring dimensions, citation guidance, and medical-claim guardrails.

Verification:
- `DATABASE_URL='postgresql://user:pass@localhost:5432/glowindex' npm run build` passed.
- `npm run lint` is not a clean gate in this repo because generated Prisma client files and pre-existing lint issues fail lint. The touched files passed targeted content checks, and build passed.

Open deployment step:
- Commit is local. Push/deploy should happen after confirming remote/deploy posture.

## Phase 4 Update — Glow Product Page GEO Patch Pushed (2026-05-07)
Status: pushed

Final commit:
- `d28afc6 Improve Glow product page GEO`
- Repo: `~/projects/skincare-rankings`
- Remote: `origin/main` (`jsomwarux/skincare-rankings`)

Rebase/deploy note:
- Initial push was rejected because remote had newer mobile/privacy/terms work.
- Rebasing preserved remote changes, including mobile image fix and privacy/terms routes.
- Build initially caught a TypeScript issue after rebase (`tierLabel` import/order); fixed before push.
- Final build passed with dummy DATABASE_URL: `DATABASE_URL='postgresql://user:pass@localhost:5432/glowindex' npm run build`.

Deployment note:
- GitHub push completed. Replit may require fresh build/redeploy for production to show changes, matching Glow's known Replit deployment behavior.

## Phase 4 Update — Glow Active Loop Wired (2026-05-07)
Status: implemented

Changes:
- Added Glow to the deterministic weekly experiment calendar as `Glow product-page GEO baseline`.
- Promoted Glow to the selected weekly durable discovery action: `Glow category-page pilot: serum rankings`.
- Created `memory/app-marketing/directory-packs-glow-index.md` for skincare-safe directory submissions.
- Created `memory/app-marketing/seo-briefs-glow-serum-category-page.md` as the first category-page pilot spec.
- Added a Glow SEO deployment marker row to `memory/app-marketing/post-registry.jsonl` for `https://glowindex.co/rankings` with commit `d28afc6`.
- Patched weekly App Marketing scoreboard cron to include Glow Index in its goal, read experiment/durable plans explicitly, and report a Glow section.

Verification:
- `python3 -m py_compile scripts/app_marketing_experiment_calendar.py scripts/app_marketing_durable_discovery.py` passed.
- Metrics/analyze/calendar/durable scripts passed.
- Experiment calendar now reports 4 experiments.
- Durable discovery now selects Glow Index serum category pilot.
- Registry has 30 rows, including 1 Glow SEO baseline row.

## Phase 4 Update — Glow Category SEO Pilot Shipped (2026-05-07)
Status: pushed

Commit:
- `a414640 Add Glow category SEO pilot`
- Repo: `~/projects/skincare-rankings`

Changes:
- Added reusable dynamic route `app/categories/[category]/page.tsx`.
- First intended pilot: `/categories/serum`.
- Page includes direct-answer copy, ranked product list, FAQ, non-medical disclaimer, CollectionPage JSON-LD, ItemList JSON-LD, FAQPage JSON-LD, and BreadcrumbList JSON-LD.
- Added thin-page gate: category page returns 404 unless it has at least 10 products and at least 5 analyzed products.
- Updated sitemap to include only category pages that pass the same product/analyzed-count gate.

Verification:
- Seed audit showed 100 products and 38 serum products.
- Public `/rankings` confirms 100 products scored/listed.
- Build passed with dummy DATABASE_URL after commit and rebase check.
- Safety checks passed: no medical schema, no aggregate-rating misuse, disclaimer present, FAQ/schema present.

Deployment note:
- GitHub push completed. Replit needs fresh rebuild/redeploy for `/categories/serum` and sitemap category URLs to appear in production.

## Phase 4 Update — Glow Category SEO Internal Linking (2026-05-07)
Status: pushed

Commit:
- `be0233c Link Glow category SEO pilot`
- Repo: `~/projects/skincare-rankings`

Changes:
- Added a first-party link from `/rankings` to `/categories/serum` so the serum category pilot is not orphaned.
- Updated `public/llms.txt` to list category pages and the serum rankings pilot explicitly.
- Added `llms.txt` quality-gate note: category pages only when enough products/analyzed scores exist; ingredient/dupe/concern pages should not be inferred unless listed.

Verification:
- Build passed with dummy `DATABASE_URL` after commit/rebase.
- External generic fetchers still hit Cloudflare challenge on Glow, so production validation relies on JT visual confirmation plus first-party deploy/rebuild.

Deployment note:
- Replit needs fresh rebuild/redeploy after `be0233c` for the rankings internal link and updated `llms.txt` to appear in production.

## Phase 4 Update — Glow SEO Batch Surfaces Shipped (2026-05-07)
Status: pushed

Commit:
- `2d4cbed Batch Glow SEO page surfaces`
- Repo: `~/projects/skincare-rankings`

Changes:
- Added shared SEO helper module `lib/seo.ts` for category gates, category copy, product slugs, and canonical site constants.
- Added `/categories` quality-gated category index with direct-answer copy, FAQ/schema, Breadcrumb schema, and non-medical disclaimer.
- Refactored `/categories/[category]` to use shared helper gates/copy.
- Added `/compare/[pair]` for safe same-category comparisons only when both products exist and have analyzed scores. No compare URLs are generated in sitemap to avoid a huge/thin compare graph.
- Added `/products/[slug]` redirect aliases for UX/shareability only. These are intentionally NOT listed in sitemap or treated as standalone citation surfaces.
- Updated `/rankings` internal links to category index + serum page.
- Updated `public/llms.txt` with safe page families and explicit exclusions for ingredient/dupe/concern/acne/eczema/rosacea/treatment pages.
- Updated sitemap to include `/categories`, qualified category pages, and canonical ranking product pages only.

Safety decisions:
- Skipped ingredient pages, dupe pages, concern pages, and condition pages because current structured data does not support unique safe content.
- Skipped generated compare URLs in sitemap to avoid thin/combinatorial SEO.
- Removed redirect-only product aliases from sitemap/LLM citation surfaces after review.

Verification:
- Safety checks passed: category gates, same-category compare gate, analyzed-product compare gate, no AggregateRating/review misuse, no MedicalWebPage schema, llms exclusions present.
- Build passed with dummy `DATABASE_URL` after commit/rebase.

Deployment note:
- Replit needs one fresh rebuild/redeploy from GitHub main at `2d4cbed`.

## Phase 4 Update — Glow Post-Deploy Next Action (2026-05-07)
Status: next action advanced

After JT confirmed the Glow SEO batch was rebuilt/redeployed, generic crawler-style fetches still hit Cloudflare `Just a moment` for category pages, sitemap, and llms.txt. The App Marketing OS durable-discovery selector was updated so the next action is no longer building the serum page. It is now:
- Glow directory pack + screenshot selection + JT approval for first listing.
- Crawlability verification/fix for `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, and `/categories/serum`.

Reason:
- More page generation is lower leverage than making existing pages discoverable and tracked.
- Ingredient/dupe/concern/condition pages remain blocked until structured data supports unique safe pages.

## Phase 4 Update — AppKittie Competitive Intelligence Candidate (2026-05-10)
Status: evaluated, not yet wired

What changed:
- Evaluated AppKittie from Jacob Rodri's X post as an app-growth intelligence source.
- AppKittie exposes filters for revenue, downloads, launch/update date, growth, ads, creators, keywords, and reviews via dashboard/API/MCP.
- Recommendation: add as a manual weekly competitor-intel input first; automate only after JT provides an API key/subscription and one report proves useful.

Done state for adoption:
- Create one AppKittie report for Glow/Vista using ≤20 apps.
- Convert at least one competitor pattern into a named experiment.
- If useful, add `scripts/app_marketing_appkittie_intel.py` with credit-safe caching and include it in weekly scoreboard flow.
