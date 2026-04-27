# Glow Index SEO Pipeline Audit — 2026-04-26

## Executive Summary
Glow Index is **not currently indexable**. The live app returns `robots.txt` with `Disallow: /`, has no sitemap, no `llms.txt`, no canonical tags detected, and no JSON-LD/schema markup detected. This blocks the entire programmatic SEO opportunity until fixed.

**Recommendation:** Fix crawlability first, then build the programmatic page engine. Do not spend time generating SEO content until robots/sitemap are live.

## Live Site Findings
Base URL: `https://skincare-rankings.replit.app`

### Crawlability
- `/robots.txt`: `User-agent: * Disallow: /` → **all crawling blocked**
- `/sitemap.xml`: returns 403
- `/llms.txt`: returns 403
- `/vote`: returns 403, likely protected/auth or server-side restriction

### URL Structure Detected
Homepage links expose:
- `/`
- `/rankings`
- `/vote`
- Individual ranking URLs like `/rankings/cmmv3rvfk001i6zawetmdagv3`

No product or ingredient URL patterns detected:
- `/products`: 0 matches
- `/product`: 0 matches
- `/ingredients`: 0 matches
- `/ingredient`: 0 matches

### Structured Data
No evidence detected in fetched HTML:
- `schema.org`: 0
- `application/ld+json`: 0
- canonical tags: 0

## SEO Pipeline Design

### Phase 0 — Crawlability Fix (blocking)
1. Replace `robots.txt` with:
   ```txt
   User-agent: *
   Allow: /
   Disallow: /admin
   Disallow: /api
   Sitemap: https://skincare-rankings.replit.app/sitemap.xml
   ```
2. Add `/sitemap.xml` route including:
   - `/`
   - `/rankings`
   - every public ranking page
   - every future product page
   - every future ingredient page
3. Add `/llms.txt` with plain-English site summary, canonical URLs, and key page groups.
4. Add canonical tags to all public pages.

### Phase 1 — Product Pages
Create indexable route:
- `/products/[slug]`

Each product analysis should generate:
- product name + brand
- Glow Score
- tier/rank
- concise reasoning
- best for / avoid if
- ingredient highlights
- dupes or alternatives
- FAQ section
- JSON-LD Product + Review schema

Target keywords:
- `[product name] review`
- `[brand] [product] worth it`
- `[product] ingredients`
- `[product] dupe`

### Phase 2 — Ingredient Pages
Create indexable route:
- `/ingredients/[slug]`

Generate from recurring actives across analyses:
- what it is
- what it does
- skin types it fits
- common pairing conflicts
- products containing it
- ranked product list
- FAQ section
- JSON-LD FAQPage schema

Target keywords:
- `[ingredient] for acne`
- `[ingredient] for sensitive skin`
- `is [ingredient] worth it`
- `[ingredient] vs [ingredient]`

### Phase 3 — Category Pages
Create indexable route:
- `/best/[category]`
- `/best/[category]/under-[price]`

Examples:
- `/best/moisturizers`
- `/best/serums-under-30`
- `/best/sunscreens-for-oily-skin`

Each page should include:
- ranked products
- quick comparison table
- scoring methodology
- buyer guide
- FAQ schema

### Phase 4 — Weekly Programmatic Posts
Auto-generate weekly editorial pages:
- `Best new products analyzed this week`
- `Top under-$30 products this week`
- `Most overhyped products this week`
- `Best products for sensitive skin this week`

These should link back to product, ingredient, and ranking pages.

## LLM Search / AI Citation Setup
Add `/llms.txt` with:
- site identity: Glow Index is a skincare product analysis and ranking engine
- methodology summary
- canonical page groups
- contact/source policy
- top pages

Add JSON-LD consistently:
- Product schema on product pages
- Review schema where score/reasoning exists
- FAQPage schema on product/ingredient/category pages
- BreadcrumbList schema on all nested routes

## Technical Implementation Notes
Likely app stack: Next.js on Replit.

Minimal implementation order:
1. `app/robots.ts` or static `public/robots.txt`
2. `app/sitemap.ts`
3. `public/llms.txt` or route handler
4. metadata/canonical helpers
5. product route + schema component
6. ingredient route + schema component
7. category route + internal links

## Done Criteria
- Google can fetch `/robots.txt` and is allowed to crawl public pages
- `/sitemap.xml` returns 200 with public URLs
- `/llms.txt` returns 200
- Public pages include canonical tags
- Product/ingredient/category pages render server-side crawlable content
- JSON-LD validates in Rich Results Test

## Mission Control Recommendation
Create build task for a coding agent:
**Title:** Build Glow Index crawlability + programmatic SEO routes
**First action:** In the Glow Index repo, add robots/sitemap/llms.txt and implement `/products/[slug]`, `/ingredients/[slug]`, and `/best/[category]` server-rendered routes with JSON-LD.
**Why:** Current robots.txt blocks all crawling, so Glow Index cannot rank or be cited by AI search.
**Done:** robots allows public crawling; sitemap/llms.txt return 200; product/ingredient/category URLs render crawlable content with canonical + JSON-LD.
