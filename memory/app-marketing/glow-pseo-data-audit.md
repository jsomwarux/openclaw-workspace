# Glow Index pSEO/GEO Data Audit

Date: 2026-05-07
Status: audit complete enough for pilot planning; production DB counts still need authenticated/runtime confirmation before implementation.
Canonical URL: https://glowindex.co
Repo inspected: `~/projects/skincare-rankings`

## Executive take
Glow Index is ready for a pSEO/GEO pilot, but not a mass page rollout yet.

The codebase already has the right foundation:
- Next.js App Router.
- Dynamic product detail pages at `/rankings/[id]`.
- Dynamic sitemap that includes product pages.
- Robots allows AI crawlers including GPTBot, ClaudeBot, PerplexityBot, and Google-Extended.
- Product/analysis schema supports scoring, reasoning, categories, price, image, and brand.

The safest first build is:
1. Improve existing product detail pages for AI-search extraction.
2. Add category pages for high-volume categories.
3. Add comparison pages only after confirming analyzed products and score data quality.

Do not start ingredient pages yet. Ingredient-level structured data does not exist in Prisma.

## Live verification
- `https://glowindex.co` returns HTTP 200.
- Page title: `Glow Index — AI-Powered Skincare Rankings`.
- Homepage copy confirms 4 independent AI analyses and transparent 0–100 scoring.

## Project files inspected
- `tasks/lessons.md`
- `package.json`
- `prisma/schema.prisma`
- `app/page.tsx`
- `app/rankings/[id]/page.tsx`
- `app/sitemap.ts`
- `app/robots.ts`
- `app/api/products/route.ts`
- `lib/types.ts`
- `lib/db.ts`
- `components/ProductCard.tsx`
- `scripts/seed.ts`

## Existing data model

### Product
Fields:
- `id`
- `name`
- `brand`
- `category`
- `priceUsd`
- `website`
- `imageUrl`
- `description`
- `consensusScore`
- `tier`
- `lastAnalyzedAt`
- `analyses`
- `votes`
- `createdAt`

### Analysis
Fields:
- `productId`
- `runId`
- `llmName`
- `stage`
- `scores` JSON string
- `reasoning`
- `consensusScore`

### Score dimensions
From `lib/types.ts`:
- ingredient_efficacy, max 30
- safety_profile, max 20
- value_for_money, max 20
- formula_transparency, max 15
- skin_compatibility, max 10
- sensory_usability, max 5

These are strong enough for extractable product and category pages.

## Seed/catalog shape
Seed script contains 100 products.

Category distribution from `scripts/seed.ts`:
- serum: 38
- moisturizer: 19
- spf: 8
- toner: 7
- eye cream: 7
- treatment: 5
- oil: 4
- cleanser: 4
- essence: 3
- mask: 2
- exfoliant: 2
- lip: 1

Top represented brands:
- The Ordinary: 9
- Tatcha: 4
- Drunk Elephant: 4
- SkinCeuticals: 4
- CeraVe: 4
- La Roche-Posay: 4
- Glow Recipe: 3

Important limitation:
- Seed catalog is not proof of production analyzed counts.
- Production DB should be audited through the deployed app/runtime or safe admin endpoint before publishing indexable category/comparison pages.

## Existing SEO/GEO foundation

### Sitemap
`app/sitemap.ts` already:
- exports dynamic sitemap
- includes `https://glowindex.co`
- includes `https://glowindex.co/rankings`
- includes product URLs at `https://glowindex.co/rankings/${id}`
- uses `lastAnalyzedAt` as lastModified for product pages

### Robots
`app/robots.ts` already allows:
- `*`
- `GPTBot`
- `ClaudeBot`
- `PerplexityBot`
- `Google-Extended`

### Product metadata
`app/rankings/[id]/page.tsx` already generates metadata:
- title includes brand/name and score
- description includes category and 4 AI models
- keywords include product, brand, category, skincare review, AI skincare ranking
- OpenGraph article title/description

### Product schema
Product detail page already outputs JSON-LD Product with AggregateRating when score exists.

Concern:
- AggregateRating can be interpreted as user review rating. It should be clarified or supplemented so Glow's score is clearly AI consensus/research output, not consumer rating.

## First pilot recommendation

### Pilot 1 — Upgrade existing `/rankings/[id]` product pages
Priority: highest.

Why:
- Route already exists.
- Sitemap already includes these pages.
- Product data and analyses already load there.
- Lowest implementation risk.

Upgrade checklist:
- Add a direct-answer block near top:
  `Glow Index analyzed [Brand] [Product] as a [category] using 4 AI models. It currently scores [score]/100 based on ingredient efficacy, safety profile, value, transparency, skin compatibility, and sensory usability.`
- Add visible disclaimer: consumer research, not medical advice.
- Add FAQ section with 4–6 extractable questions.
- Add BreadcrumbList schema.
- Clarify JSON-LD rating language or add Review/FAQ schema so AI systems understand the score source.
- Add model consensus/disagreement summary if extractable from existing analyses.
- Add `noindex` or no pSEO expansion for products with no consensusScore/analysis.

### Pilot 2 — Add `/categories/[category]`
Priority: high after product page upgrade.

Best first categories by seed inventory:
1. serum
2. moisturizer
3. spf

Recommended first category: `serum`.

Why:
- Highest catalog depth in seed data: 38 products.
- Strong skincare search intent.
- Less medical-risky than concern pages if framed around formula/value/transparency.

Safe page angle:
`AI-ranked skincare serums by formula, value, transparency, and model consensus.`

Avoid:
- best serum for acne
- best serum for eczema
- best serum for rosacea
- treatment/cure language

Minimum production requirement:
- 5+ analyzed serum products preferred.
- If fewer than 3 analyzed products, do not publish indexable category page yet.

### Pilot 3 — Add one comparison page
Priority: after production data audit.

Candidate pair selection criteria:
- same category
- both analyzed
- both have score breakdowns
- meaningful price/value contrast
- enough reasoning to produce unique copy

Likely comparison families from seed catalog:
- The Ordinary serum vs higher-priced serum
- CeraVe moisturizer vs luxury moisturizer
- Drunk Elephant serum vs comparable serum
- SPF comparison within same category

Do not choose comparison page until production analyzed data is confirmed.

## Do not build yet

### Ingredient pages
Reason: ingredients are not structured in Prisma.
Risk: extracting from reasoning text could hallucinate or misrepresent formulas.

Build only after adding a structured ingredient table or reliable parser.

### Concern pages
Reason: high medical-claim risk.
Examples to avoid for now:
- best skincare for acne
- best moisturizer for eczema
- best serum for rosacea

If built later, use careful framing like:
- `how Glow Index evaluates skincare products for formula transparency and safety profile`
not medical suitability.

### Dupe pages
Reason: no structured ingredient similarity or formula-overlap model yet.
Build later only after similarity criteria exist.

## Data audit still needed before code changes

The direct Prisma query failed because Prisma 7 generated client requires the project's adapter config. Use the app's existing `lib/db.ts` adapter path or a small Next/API-safe script to audit production/runtime data.

Audit fields needed:
- total products
- analyzed products
- category counts
- analyzed category counts
- products with images
- products with descriptions
- products with valid score JSON
- products with stage 2 analysis
- top categories by analyzed product count
- comparison pairs by same category and score/value contrast

Output should go to:
`memory/app-marketing/glow-pseo-data-audit-runtime.md`

## Quality gates for implementation

A page can be indexable only if:
- it has unique product/category/comparison content
- it has no medical claim language
- it includes the consumer-research disclaimer
- it has FAQ/direct answer structure
- it has valid schema
- it is included in sitemap only when data is sufficient
- build and lint pass

## Recommended next implementation task
Create a runtime-safe audit script or one-off route-local command that uses `lib/db.ts`, then produce `glow-pseo-data-audit-runtime.md`.

After that, implement:
1. product page GEO upgrade
2. serum category page if production data supports it
3. one comparison page if two same-category analyzed products support it
