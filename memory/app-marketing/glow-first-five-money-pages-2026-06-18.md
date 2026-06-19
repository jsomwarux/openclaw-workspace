# Glow Index First Five Money Pages
Date: 2026-06-18

## Gate
Crawler access is now fixed live. The first SEO/GEO batch is live; measure it before building another page. Do not broaden into generic content or social volume.

Latest check:
- Command: `python3 scripts/glow_crawler_check.py`
- Result: `all_clear=true`
- Passing: `robots.txt`, `sitemap.xml`, `llms.txt`, `/rankings`, `/categories`, `/categories/serum` return 200 with no Cloudflare challenge.

Root cause found 2026-06-18:
- Glow's `proxy.ts` was sending discovery files and category routes to Clerk sign-in because they were missing from the public route matcher.
- The apparent Cloudflare 403 happens after the crawler follows the Clerk redirect to `accounts.glowindex.co`.
- Fix shipped in `/Users/jtsomwaru/projects/skincare-rankings/proxy.ts` via commit `329ed72` and verified live after production republish.

First content action is complete. Current action is measurement: verify GSC/GA4/source-tag reporting, then decide whether the next deploy batch deserves Replit rebuild credits.

Implementation status 2026-06-18:
- Pushed to `jsomwarux/skincare-rankings` through commit `3c60c25 Add Glow rankings index SEO context` (includes `2fa05cf Add Glow product page SEO source tagging`).
- Production republished from `3c60c25` and live verification passed: crawler `all_clear=true`, `/rankings` has the rankings extraction/source/schema context, and a live product detail page has the product analysis extraction/source/category-link context.
- Product page template updated with an explicit `AI skincare analysis` heading for extractability.
- Product detail analytics now sends source tag `glow_seo_product_analysis_20260618` on `view_product`.
- Product pages now link to the relevant category rankings page from the summary block.
- Existing FAQ, consumer-research disclaimer, Product JSON-LD, FAQ JSON-LD, and BreadcrumbList JSON-LD remain in place.

## Page Queue
### 1. Existing Product Analysis Upgrades
URL pattern: `/rankings/[id]`

Target query pattern:
- `[brand] [product] AI skincare analysis`
- `[brand] [product] review`

Why first:
- Route already exists.
- `/rankings` currently returns 200.
- Product-specific search has stronger purchase intent than broad education.

Build notes:
- Add direct-answer block.
- Add visible consumer-research disclaimer.
- Add FAQ section.
- Clarify AI consensus score vs user/consumer rating.
- Add BreadcrumbList/Product or SoftwareApplication-safe schema where appropriate.
- Noindex/hide products without enough analysis.

Source tag:
- `glow_seo_product_analysis_20260618`

### 2. AI Skincare Product Value Analyzer
URL: `/skincare-product-value-analyzer`

Target query:
- `skincare product value analyzer`

Why second:
- Safe value/transparency framing.
- Affiliate-adjacent without medical claims.
- Can be built as evergreen methodology/use-case page.

Direct-answer angle:
An AI skincare product value analyzer compares product facts such as price, category, formula transparency, and scoring rationale to help shoppers judge whether a product looks worth its cost. It is consumer research, not medical advice.

Source tag:
- `glow_seo_value_analyzer_20260618`

### 3. AI-Ranked Skincare Serums
URL: `/categories/serum`

Target query:
- `AI ranked skincare serums`

Why third:
- Category intent is high.
- Serum inventory appears to be the strongest safe category candidate.

Build gate:
- Minimum 10 tracked serum products and 5 analyzed serum products, matching `lib/seo.ts` category qualification.
- `/categories/serum` must return 200 to crawler.
- Disclaimer visible above/below ranking explanation.

Source tag:
- `glow_seo_category_serum_20260618`

### 4. Skincare Formula Transparency Score
URL: `/skincare-formula-transparency-score`

Target query:
- `skincare formula transparency score`

Why fourth:
- Turns scoring methodology into an AI-citable trust anchor.
- Supports product and category pages.

Direct-answer angle:
A skincare formula transparency score evaluates how clearly a product presents its formula, category fit, claims, pricing context, and available evidence. It is a shopper research signal, not a medical judgment.

Source tag:
- `glow_seo_formula_transparency_20260618`

### 5. AI Skincare Ingredient Checker
URL: `/ai-skincare-ingredient-checker`

Target query:
- `AI skincare ingredient checker`

Why fifth:
- Strong search-intent phrase.
- Useful if framed as ingredient-list/product-information review.

Build constraint:
- Use-case/methodology page only for now.
- Do not create ingredient directory pages until structured ingredient data exists.
- Avoid acne/eczema/rosacea/treatment positioning.

Source tag:
- `glow_seo_ingredient_checker_20260618`

## Measurement
Track weekly:
- indexed: yes/no;
- Search Console impressions/clicks;
- GA4 landing-page views;
- affiliate click or email capture;
- top-20 query count;
- AI citation observed: yes/no/source.

Post-deploy baseline artifact:
- `memory/app-marketing/glow-post-deploy-measurement-2026-06-18.md`

## Guardrails
- No medical advice.
- No cure/treat/diagnose language.
- No fake testimonials or before/after.
- No dermatologist endorsement unless verified.
- No dupe pages until structured similarity/formula-overlap criteria exist.
