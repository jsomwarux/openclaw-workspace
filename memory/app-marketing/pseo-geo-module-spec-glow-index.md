# Glow Index pSEO/GEO Module Spec

Date: 2026-05-07
Status: spec-ready, build not started
Canonical production URL: https://glowindex.co

## Decision
Glow Index is now the best first pilot for a reusable App Marketing pSEO/GEO module.

Reason: Glow has live structured product data, consumer-search demand, category/comparison/ingredient query surfaces, and clear long-tail SEO upside. Build a safe 3-template pilot before scaling.

## Current implementation facts

Repo: `~/projects/skincare-rankings`
Stack: Next.js 16 App Router, React 19, Prisma/Postgres, Clerk, Stripe.
Production URL: `https://glowindex.co`
Existing routes:
- `/`
- `/rankings`
- `/rankings/[id]`
- `/vote`
- `/analysis-status`
- `/admin`
- `/robots.txt`
- `/sitemap.xml`

Existing sitemap:
- Includes home, rankings, and `/rankings/[id]` product detail URLs.
- Uses product IDs, not product slugs.

Existing robots:
- Allows normal crawlers plus GPTBot, ClaudeBot, PerplexityBot, Google-Extended.

Existing product data model:
- `Product`: id, name, brand, category, priceUsd, website, imageUrl, description, consensusScore, tier, lastAnalyzedAt.
- `Analysis`: productId, runId, llmName, stage, scores JSON, reasoning, consensusScore.
- Score dimensions: ingredient_efficacy, safety_profile, value_for_money, formula_transparency, skin_compatibility, sensory_usability.
- Categories: moisturizer, serum, cleanser, spf, treatment, eye cream, oil, toner, essence, exfoliant, mask, lip.

## Safety rules

Glow content must not make medical claims. This includes no medical/dermatology claims, no diagnosis/treatment language, and no cure/prevention wording.

Forbidden:
- diagnose, treat, cure, prevent disease
- dermatologist-recommended unless verified
- fake testimonials
- fake before/after claims
- best for acne/eczema/rosacea as a medical claim
- guarantees about irritation, safety, or results

Allowed framing:
- consumer research
- formula transparency
- ingredient evidence
- value comparison
- model consensus/disagreement
- marketing-claim skepticism
- non-medical category/routine language

Required disclaimer on every pSEO page:
> Glow Index is a consumer research tool, not medical advice. Scores are based on product information and AI analysis of ingredients, pricing, evidence, and marketing claims. Patch test new products and consult a qualified professional for skin conditions or medical concerns.

## Reusable pSEO/GEO architecture

Every template should include:
1. Direct-answer block at top.
2. Product/data facts.
3. Model consensus/disagreement section.
4. Safe score explanation.
5. FAQ section.
6. JSON-LD schema.
7. Canonical URL.
8. Sitemap inclusion.
9. `llms.txt` entry for top-level template families.
10. Quality gate before publish.

## Pilot templates

### Template 1 — Product analysis page
Preferred future URL:
`/products/[brand-product-slug]`

Current equivalent:
`/rankings/[id]`

Purpose:
Rank for product-specific searches and AI answer citations.

Page sections:
- What is `[Brand] [Product]`?
- Glow Index score and tier.
- Why it scored this way.
- Score breakdown by dimension.
- Where the AI models agreed.
- Where the AI models disagreed.
- Price/value context.
- Who this might be useful for, phrased non-medically.
- What to double-check before buying.
- FAQ.
- Disclaimer.

Minimum data required:
- product name
- brand
- category
- price
- consensusScore or analyzed state
- at least one analysis reasoning field
- score dimensions parseable from JSON

Schema:
- Product
- AggregateRating only if clearly framed as Glow Index AI consensus, not user reviews
- FAQPage
- BreadcrumbList

Quality gate:
- Do not publish indexable product page if no analysis exists.
- If product is awaiting analysis, use noindex or keep current non-pSEO state.

### Template 2 — Category ranking page
URL:
`/categories/[category]`

Examples:
- `/categories/serum`
- `/categories/moisturizer`
- `/categories/spf`

Purpose:
Rank for category-level searches like "best AI-ranked serums" or "skincare product value analyzer serum" without medical claims.

Page sections:
- Direct answer: what Glow Index compares in this category.
- Ranked products in category.
- How scoring works for this category.
- Value-for-money standouts.
- Formula-transparency standouts.
- Products with strongest consensus.
- FAQ.
- Disclaimer.

Minimum data required:
- 5+ analyzed products in category preferred.
- If fewer than 3, page can exist but should not claim ranked category authority.

Schema:
- CollectionPage
- ItemList
- FAQPage

Quality gate:
- Do not use "best for acne/eczema/rosacea."
- Use "top-rated by Glow Index in [category]" or "highest-scoring [category] products in the current dataset."

### Template 3 — Comparison page
URL:
`/compare/[product-a]-vs-[product-b]`

Purpose:
Capture high-intent comparison searches and dupe/value analysis.

Page sections:
- Direct answer: how the products differ.
- Score comparison table.
- Price/value comparison.
- Ingredient/formula transparency comparison.
- Where one product scores higher.
- Where the difference is not decisive.
- Which product looks stronger for value/formula transparency/sensory usability, only if data supports it.
- FAQ.
- Disclaimer.

Minimum data required:
- both products analyzed
- both same/similar category preferred
- both have score breakdowns

Schema:
- WebPage
- Product for each compared product
- FAQPage
- BreadcrumbList

Quality gate:
- No "better for acne" or treatment-based comparison.
- Do not create comparison page if products are unrelated categories unless framed as broad value comparison.

## Later templates

### Ingredient education page
URL: `/ingredients/[ingredient]`

Current blocker:
Ingredient-level structured data is not in Prisma schema yet. Could be generated from analysis reasoning, but that risks unreliable extraction. Wait until ingredients are parsed/stored separately.

### Dupe/value page
URL: `/dupes/[product]`

Current blocker:
Needs defensible similarity logic. Do not build until category, price, and formula/ingredient overlap are structured.

### Concern pages
URL: `/best-[category]-for-[concern]`

Current blocker:
High medical-claim risk. Only build with careful non-medical framing and data support.

## Build sequence

### Step 1 — Data audit
Inspect production/local DB shape:
- product count
- analyzed product count
- category counts
- score JSON consistency
- reasoning quality
- products with imageUrl

Output file:
`memory/app-marketing/glow-pseo-data-audit.md`

### Step 2 — Slug strategy
Add safe product slug generation without breaking current `/rankings/[id]` links.
Options:
1. Keep `/rankings/[id]` and improve metadata/schema now.
2. Add `/products/[slug]` as canonical pSEO route while redirecting or linking from `/rankings/[id]`.

Recommendation:
Start with route enhancements + category pilot. Add product slugs only if build risk is low.

### Step 3 — 3-page pilot
Pilot pages:
1. Upgrade one existing analyzed product detail page for pSEO/GEO.
2. Add one category page for the category with most analyzed products.
3. Add one comparison page between two analyzed products in the same category.

### Step 4 — Index/crawl support
- Update sitemap with category/comparison routes.
- Add `llms.txt` explaining Glow Index, ranking method, product pages, category pages, and safety disclaimer.
- Ensure robots allows AI crawlers.

### Step 5 — Measurement
Add Glow to App Marketing OS metrics:
- product pages indexed
- top landing pages
- impressions/clicks when Search Console available
- directory referrals later
- TikTok/Pinterest later only after account/asset path exists

## Reusable blueprint requirement

This module should become reusable for future ensemble apps:
- config defines product/entity fields
- score dimensions
- safety rules
- templates allowed
- forbidden claims
- sitemap rules
- schema mapping
- minimum data quality threshold

Candidate future ports:
- Nash: token pages, token comparisons, methodology pages
- Vista: movie taste/rating pages if movie data becomes structured
- Action Arena: strategy/waitlist SEO pages after landing exists

## Recommendation
Build this next, but do it as a pilot:
- Data audit first.
- Then 3 templates/pages.
- Then scale only after build, crawl, and quality gates pass.
