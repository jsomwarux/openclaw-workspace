# Glow Index — Product Verdict Card + 10 Verdict Pages Implementation Plan
Date: 2026-05-19
Repo: `/Users/jtsomwaru/projects/skincare-rankings`
Status: build-ready coding task

## Repo Evidence
- Next.js app with product detail pages:
  - `app/rankings/[id]/page.tsx`
  - `app/products/[slug]/page.tsx`
  - `app/compare/[pair]/page.tsx`
- Existing product data:
  - Prisma `Product` model has name, brand, category, priceUsd, website, imageUrl, description, consensusScore, tier.
  - `Analysis` model has scores and reasoning.
- Existing components:
  - `components/ConsumerVerdict.tsx`
  - `components/KeyFindings.tsx`
  - `components/ScoreBreakdown.tsx`
  - `components/ScoreDisplay.tsx`
- Lessons file read: `tasks/lessons.md`.

## Verdict
Build the Product Verdict Card as a reusable web component first, then embed it on existing product detail pages. Use browser-native screenshot/manual save for MVP; add generated PNG export after the card proves useful.

## Product Goal
Create concrete assets before creator/writer outreach:

`product page → verdict card → share/save/link → creator/writer has something specific to reference`

## MVP Scope
### Component
Create:
- `components/ProductVerdictCard.tsx`

Props:
```ts
interface ProductVerdictCardProps {
  product: Product;
  analyses: Analysis[];
  averageScores: AnalysisScores | null;
}
```

### Placement
Embed on:
- `app/rankings/[id]/page.tsx`
- optional later: `app/products/[slug]/page.tsx`

Place after product header / before detailed paywall content where it can serve as SEO/shareable public summary.

## Verdict Labels
Use safe labels from spec, but replace any too-strong shopping language:
- `Strong Research Signal`
- `Worth Comparing`
- `Check Fit First`
- `Skip Signal`

Avoid:
- safe / unsafe
- toxic / clean / dirty
- will treat / will clear
- expert-approved unless directly sourced

## Required Card Fields
- product name
- brand
- category
- product image if available
- Glow Score / 100
- verdict label
- 3 why bullets:
  - formula
  - fit flags/watch-items
  - value
- comparison prompt
- footer: `Consumer product research based on available product data, ingredients, pricing, and AI analysis. Not skin guidance.`

## Data Derivation
Use available data first:
- score/tier from `product.consensusScore` / `product.tier`
- average dimension scores from existing `computeAverageScores()` in `app/rankings/[id]/page.tsx`
- key bullets can initially come from `KeyFindings` extraction logic or a new small helper using `analyses.reasoning`

Recommended helper:
- `lib/product-verdict.ts`

Functions:
- `deriveVerdictLabel(product, averageScores)`
- `deriveVerdictBullets(product, analyses, averageScores)`
- `deriveComparisonPrompt(product)`

## 10 Product Page Candidates
Use existing products if present; otherwise seed only after confirming data availability:
1. CeraVe Hydrating Facial Cleanser
2. Vanicream Gentle Facial Cleanser
3. La Roche-Posay Toleriane Double Repair Moisturizer
4. COSRX Advanced Snail 96 Mucin Power Essence
5. The Ordinary Niacinamide 10% + Zinc 1%
6. Paula’s Choice 2% BHA Liquid Exfoliant
7. Anua Heartleaf 77 Soothing Toner
8. Beauty of Joseon Relief Sun
9. Tower 28 SOS Daily Barrier Recovery Cream
10. Drunk Elephant Protini Polypeptide Cream

Do not create fake product pages. If products are missing, create an admin/seed task or use the existing vote/add-product flow.

## SEO Additions
Update metadata on product pages to mention:
- product verdict
- formula/value comparison
- score breakdown

Add structured data as Product + additionalProperty only. Do not add medical claim schema.

## Acceptance Criteria
- `ProductVerdictCard` renders for analyzed products.
- Card does not render misleading verdict for unanalyzed products.
- Page copy avoids medical/treatment/fake endorsement language.
- 10 product verdict pages are either live from existing products or listed as missing with exact add/analyze steps.
- `npm run build` passes.
- If product pages change, run crawler check after deploy: `python3 scripts/glow_crawler_check.py`.

## Replit Deployment Caveat
Replit deploy requires fresh build, not just redeploy. After changes:
1. pull latest code in Replit
2. run `npm run build`
3. redeploy / rebuild from scratch
4. verify live pages

## References
- `memory/app-marketing/share-artifacts/glow-product-verdict-card-spec-2026-05-19.md`
- `memory/app-marketing/outreach-packs/glow-borrowed-audience-pack-2026-05-19.md`
- `memory/app-marketing/experiment-queue-2026-05-19.jsonl`
- `/Users/jtsomwaru/projects/skincare-rankings/tasks/lessons.md`
