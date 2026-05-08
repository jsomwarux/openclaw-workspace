# Glow Index SEO/GEO Brief — Serum Category Page Pilot

Status: spec-ready, not built yet
Created: 2026-05-07
Target app: Glow Index
Canonical domain: https://glowindex.co
Recommended URL: `/categories/serum`

## Why this page first

Serum is the strongest seed category in the Glow catalog from the current audit: 38 seeded products, more than any other category. That makes it the safest first category page because it has enough product density to avoid a thin page.

This should be the first category-page pilot after the product-page GEO patch, before ingredient/dupe/concern pages.

## Primary query

AI skincare serum rankings

## Secondary queries

- best skincare serums AI ranked
- skincare serum comparison
- serum product rankings
- skincare serum value comparison
- AI skincare product rankings
- compare skincare serums

## Direct answer block

Glow Index ranks skincare serums by comparing products across six non-medical research dimensions: ingredient efficacy, safety profile, value for money, formula transparency, skin compatibility, and sensory usability. The serum category page should help shoppers compare formulas, price/value, score breakdowns, and model reasoning without treating the output as medical advice.

## Required page sections

1. H1: `AI-ranked skincare serums`
2. Direct answer block: what this page is and how serums are scored.
3. Top serum rankings table/grid:
   - Product name
   - Brand
   - Consensus score
   - Tier
   - Price
   - strongest score dimension if available
   - link to product detail page
4. How Glow Index scores serums:
   - ingredient efficacy
   - safety profile
   - value for money
   - formula transparency
   - skin compatibility
   - sensory usability
5. What to look for in a serum:
   - formula clarity
   - concentration/transparency where available
   - price/value
   - compatibility caveat
   - claim quality
6. FAQ:
   - What is the best serum on Glow Index?
   - How does Glow Index score serums?
   - Is this medical advice?
   - Does Glow Index replace a dermatologist?
   - Why use multiple AI models?
7. Safety disclaimer.
8. Internal links:
   - `/rankings`
   - top product detail pages
   - future category pages when built

## Schema

Recommended:
- CollectionPage
- ItemList for ranked products
- FAQPage
- BreadcrumbList

Avoid:
- MedicalWebPage unless medically reviewed, which it is not.
- Review/AggregateRating based on AI analysis as if it were consumer reviews.

## Quality gates before build

Do not build unless:
- At least 10 serum products exist in live data.
- At least 5 serum products have consensus scores and analyses.
- Page can show unique serum-specific content, not just a generic ranking grid.
- FAQ and safety language are present.
- Sitemap includes the category page.
- Robots/AI crawler access remains open.
- No medical/treatment claims are introduced.

## Guardrails

Allowed:
- “AI-ranked skincare serums.”
- “Consumer research.”
- “Compare formulas, value, and score breakdowns.”
- “Not medical advice.”

Banned:
- “Best serum for acne.”
- “Treats eczema.”
- “Dermatologist recommended.”
- “Clinically proven” unless source data proves it.
- Before/after language.
- Guaranteed results.

## Implementation notes

Likely files:
- `app/categories/[category]/page.tsx`
- `app/sitemap.ts`
- possibly `lib/category.ts` or helper function in existing DB layer

Use existing product data first. Do not add ingredient parsing in this pilot.

## Success metric

Initial success is technical, not traffic:
- page builds,
- page is indexable,
- sitemap includes it,
- direct answer/FAQ/schema present,
- no safety violations,
- product links work.

Traffic/search metrics come later after indexing.
