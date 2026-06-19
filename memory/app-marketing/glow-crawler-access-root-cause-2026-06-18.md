# Glow Index Crawler Access Root Cause
Date: 2026-06-18

## Finding
The live crawler failure is not primarily a Cloudflare/Replit rule problem.

Fresh checks showed:
- `/` and `/rankings` return `200` from the app.
- `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/categories`, and `/categories/serum` redirect to Clerk sign-in when fetched without an authenticated session.
- `scripts/glow_crawler_check.py` follows those redirects to `accounts.glowindex.co`, where Cloudflare returns the observed `403` challenge.

Root cause:
- `proxy.ts` in `/Users/jtsomwaru/projects/skincare-rankings` only treated `/`, `/rankings`, `/privacy`, `/terms`, auth, API, and admin paths as public.
- Discovery files and category pages were missing from the Clerk public route matcher.

## Fix Prepared Locally
Changed `/Users/jtsomwaru/projects/skincare-rankings/proxy.ts` so these are public:
- `/categories`
- `/categories/(.*)`
- `/robots.txt`
- `/sitemap.xml`
- `/llms.txt`

Also scrubbed concrete-looking callback/admin secret examples from `DEPLOY_CHECKLIST.md` and logged the crawler/Clerk redirect lesson in `tasks/lessons.md`.

Pushed to GitHub:
- Repo: `jsomwarux/skincare-rankings`
- Branch: `main`
- Commit: `329ed72 Fix Glow crawler public routes`

## Verification
- Red check before patch: source-level crawler route assertion failed for all five missing public routes.
- Green check after patch: source-level crawler route assertion passed.
- `npm run lint`: exit 0, with two pre-existing `<img>` warnings in `app/compare/[pair]/page.tsx` and `app/rankings/[id]/page.tsx`.
- `DATABASE_URL='postgresql://postgres:password@localhost:5432/glowindex' npm run build`: exit 0, Next build compiled successfully and listed `/robots.txt`, `/sitemap.xml`, `/categories`, `/categories/[category]`, and `/rankings` routes.

Local runtime note:
- `next start` without production Clerk env returns `500` for pages because `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` is missing locally. Production already has Clerk env because `/rankings` returns live 200.

Live status:
- After push, `scripts/glow_crawler_check.py` still reports `all_clear=false`, so `glowindex.co` has not yet rebuilt from the pushed fix.
- After JT pulled, rebuilt, and republished, `scripts/glow_crawler_check.py` still reports `all_clear=false`. Header verification shows `https://glowindex.co/robots.txt` still returns a `307` Clerk redirect to `accounts.glowindex.co/sign-in`, followed by Cloudflare `403`; `/categories` also remains blocked, while `/rankings` remains `200`.
- After the actual production republish completed, `scripts/glow_crawler_check.py` reports `all_clear=true`. `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, and `/categories/serum` all return `200` with no Cloudflare challenge.

## Next Action
Access repair and the first SEO/GEO money-page pass are complete. Move to measurement:
1. Use `memory/app-marketing/glow-post-deploy-measurement-2026-06-18.md` as the baseline artifact.
2. Register `source_tag` as a GA4 event-scoped custom dimension so `customEvent:source_tag` becomes queryable.
3. Run 72h and 7d checks before approving another Replit rebuild.
4. Treat `/categories/serum` as a candidate only if live measurement plus the code gate justify it.

Done state:
- Crawler gate is complete.
- Product-analysis and rankings-index SEO/GEO pass is live.
- Next deploy decision is blocked on measurement, not crawler access.

## Acquisition Impact
This unlocks Glow's compounding acquisition path. Search, AI citation, and category/product landing pages cannot work if crawlers are sent to sign-in. Fixing public crawl access comes before new money pages, creator demos, or page submissions.
