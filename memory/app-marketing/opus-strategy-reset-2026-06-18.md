# App Marketing OS — Opus Strategy Reset
Date: 2026-06-18

## Decision
Adopt the Opus 4.8 strategy with one correction: measurement is not "missing" equally across all apps. Glow and Nash already have GA4/Search Console mapped; the missing layer is a decision scoreboard that blocks unfocused execution.

Operating rule: consulting cash/proof comes first. App marketing gets less than 10 hours/week and cannot outrank Yair/Altmark, Petri/HPM/Superior M2s, or proof assets.

## Portfolio Order
1. **Action Arena — gate sprint, then park.** Close the App Store submission path by 2026-07-15 or pause until next preseason. Build the 20-commissioner list, but do not launch publicly until football season.
2. **Glow Index — primary ongoing app bet.** SEO/GEO money pages, methodology trust anchor, indexing checks, and affiliate/email conversion are the only recurring app-growth lane.
3. **Nash Satoshi — capped.** One human-reviewed research receipt/week max. Measure methodology-page clicks and waitlist signups, not impressions.
4. **Vista — paused.** Monitor existing SEO/App Store surfaces only. No taste-card build, FilmTok/ReelFarm scaling, directory push, or new feature work until a controlled share-to-install test is approved or consulting cash reaches $10K/month.

Paid UGC/creator overlay: pause for all apps except a future capped Action Arena kickoff test. Action Arena can test 2-3 creators through SideShift or Home From College only after the app is live, attribution is ready, the invite/league loop is instrumented, and the budget/scale threshold is written. Nash is a hard no; Glow is low priority and requires compliance scripting.

## Week 1 Execution Queue
### 1. Action Arena Submission Blocker
Source/build path is found: `/Users/jtsomwaru/projects/action-arena` from private GitHub repo `jsomwarux/action-arena`. The blocker is now EAS/TestFlight/App Store submission readiness, not more app marketing strategy.

Progress on 2026-06-18:
- removed hardcoded Supabase/Odds keys from `eas.json` preview/production profiles;
- added `eas-build-pre-build` so EAS runs the production mock-data guard before builds;
- documented required EAS secrets in README and App Store submission docs;
- verified TypeScript, production mock-data guard, and iOS Expo export.

Next execution step: confirm EAS secrets + App Store Connect/TestFlight status, then produce or locate the submission build.

Done state:
- source repo or build system path identified;
- current App Store Connect/TestFlight status recorded;
- single next submission action written down;
- if source is missing/unavailable, JT gets one concrete ask instead of a broad "where is it?"

### 2. Glow Index SEO Gate
`python3 scripts/glow_crawler_check.py` on 2026-06-18 still reports `all_clear=false`.

Current failing paths:
- `https://glowindex.co/robots.txt` — 403 Cloudflare challenge
- `https://glowindex.co/sitemap.xml` — 403 Cloudflare challenge
- `https://glowindex.co/llms.txt` — 403 Cloudflare challenge
- `https://glowindex.co/categories` — 403 Cloudflare challenge
- `https://glowindex.co/categories/serum` — 403 Cloudflare challenge

Passing path:
- `https://glowindex.co/rankings` — 200

First Glow action: fix narrow Cloudflare/Replit access for discovery and category paths before building net-new pages.

First five page candidates after crawler gate:
1. `/rankings/[id]` product analysis upgrades for existing analyzed products.
2. `/skincare-product-value-analyzer`.
3. `/categories/serum`.
4. `/skincare-formula-transparency-score`.
5. `/ai-skincare-ingredient-checker` as a use-case/methodology page only, not ingredient-directory pages.

### 3. Weekly Scoreboard
Create one Friday decision view with these rows:

| App | Status | This week metric | Decision rule |
|---|---|---|---|
| Action Arena | Gate sprint | source/build status, submission blocker, commissioner count | submit by 2026-07-15 or pause |
| Glow Index | Push | crawl/index status, impressions, clicks, top-20 pages, affiliate/email events | improve/publish only after crawl/index path is clean |
| Nash Satoshi | Cap | methodology-page visits, receipt clicks, waitlist signups | 30 days impressions with no clicks/signups = cap to monthly |
| Vista | Pause | passive SEO/App Store only | no work unless explicit un-pause trigger |

### 4. Nash Weekly Receipt Cap
Keep only one weekly receipt if there is a real ranking delta or model disagreement. Every draft must be research-only, no advice, no returns, no performance claims, and must link to methodology/waitlist.

### 5. Vista Hold
Archive or demote all Vista active-build/share-artifact/directory/ReelFarm tasks that imply immediate execution. Keep only passive measurement or explicit un-pause-trigger notes.

## Do Not Implement Yet
- Product Hunt.
- Broad directory pushes.
- Vista taste-card build.
- Daily Nash drafts.
- TikTok/ReelFarm scaling.
- Paid UGC creator spend, except the gated Action Arena kickoff test after app live + attribution ready.
- Any external posting automation.
- New app features unless a named submission/conversion blocker requires code.
