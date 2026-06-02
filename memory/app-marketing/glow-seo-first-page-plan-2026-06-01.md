# Glow Index SEO-First Safe Page Plan — 2026-06-01

Status: planning brief, no site edits made

## Executive Read
Glow Index should not receive a social-volume push yet.

The safer growth route is SEO/GEO page work after crawlability and claim-safety gates are explicit. Current crawler status still shows Cloudflare challenges on key discovery paths, so the first implementation gate is crawler access, not more content.

## Source Inputs
- `memory/app-marketing/vista-first-growth-sprint-2026-05-27.md`
- `memory/app-marketing/glow-pseo-data-audit.md`
- `memory/app-marketing/glow-crawler-access-status.json`
- `memory/app-marketing/glow-crawler-access-2026-05-13.md`
- `memory/app-marketing/seo-backlog.md`

## Current Gate Status
Verified on 2026-06-01 with `python3 scripts/glow_crawler_check.py`: `all_clear=false`.

| Gate | Current state | Decision |
|---|---|---|
| Homepage live | `https://glowindex.co` previously verified live | Pass |
| `/rankings` route | returns 200 in crawler check | Pass |
| `robots.txt` | 403 Cloudflare challenge in crawler check | Blocked |
| `sitemap.xml` | 403 Cloudflare challenge in crawler check | Blocked |
| `llms.txt` | 403 Cloudflare challenge in crawler check | Blocked |
| `/categories` | 403 Cloudflare challenge in crawler check | Blocked |
| `/categories/serum` | 403 Cloudflare challenge in crawler check | Blocked |
| Product data model | product/analysis/category/score fields exist | Pass for product/category pilot |
| Ingredient pages | structured ingredient table absent | Blocked |
| Concern pages | medical-claim risk | Blocked |
| Dupe pages | no structured similarity criteria | Blocked |

## First Implementation Gate
Before building or submitting new indexable pages, rerun:

```bash
cd ~/.openclaw/workspace
python3 scripts/glow_crawler_check.py
```

Done state:
- `robots.txt` returns 200.
- `sitemap.xml` returns 200.
- `llms.txt` returns 200.
- `/rankings` returns 200.
- `/categories` returns 200 or is intentionally absent with no indexable category links.
- `/categories/serum` returns 200 only when category pages exist.

Preferred fix:
Use a narrow Cloudflare/Replit skip rule for discovery files and category/ranking paths. Do not disable all protection globally.

## Safe Language Guardrails
Allowed:
- consumer research
- product analysis
- formula transparency
- value-for-money
- ingredient evidence
- AI consensus score
- model agreement / model disagreement
- category comparison by product facts

Avoid:
- medical advice
- treatment/cure language
- diagnosis language
- "best for acne/eczema/rosacea"
- dermatologist endorsement unless verified
- fake before/after claims
- fake user stories
- dupe claims without structured similarity evidence

Required disclaimer:
Glow Index is a consumer research tool, not medical advice. Product scores are based on available product information and AI analysis, not diagnosis or treatment guidance.

## Five Safe Page Candidates

### 1. AI Skincare Product Value Analyzer
Recommended URL: `/skincare-product-value-analyzer`

Target query:
`skincare product value analyzer`

Search intent:
The user wants help deciding whether a skincare product is worth the price.

Page angle:
Glow Index evaluates product value using price, category, formula transparency, and AI model reasoning.

Direct answer:
A skincare product value analyzer compares product facts such as price, category, ingredient evidence, transparency, and scoring rationale to help shoppers judge whether a product looks worth its cost. Glow Index frames this as consumer research, not medical advice.

Safe because:
It focuses on value and transparency, not medical outcomes.

Schema:
- FAQPage
- SoftwareApplication

Build dependency:
Can be built as an evergreen methodology/use-case page before category pages, as long as crawler access is fixed.

### 2. AI Skincare Ingredient Checker
Recommended URL: `/ai-skincare-ingredient-checker`

Target query:
`AI skincare ingredient checker`

Search intent:
The user wants help reading ingredient lists and understanding product positioning.

Page angle:
Glow Index uses product data and model reasoning to help shoppers inspect ingredient claims, formula transparency, and value.

Direct answer:
An AI skincare ingredient checker helps summarize visible product information and flag questions about formula transparency, value, and marketing claims. It should not replace medical or dermatology advice.

Safe because:
It is framed as product-information review, not treatment guidance.

Blocked piece:
Do not create ingredient directory pages until structured ingredient data exists. This can be a use-case/methodology page only.

Schema:
- FAQPage
- SoftwareApplication

### 3. AI-Ranked Skincare Serums
Recommended URL: `/categories/serum`

Target query:
`AI ranked skincare serums`

Search intent:
The user wants category-level product comparison.

Page angle:
Glow Index compares serums by AI consensus, value, formula transparency, and available product facts.

Direct answer:
An AI-ranked skincare serum page groups serum products by category and compares them using score, model reasoning, value, and formula transparency. It should avoid medical claims and focus on consumer research.

Safe because:
Serum has the deepest seed inventory, and the page can rank by product facts instead of concerns.

Build requirements:
- 5+ analyzed serum products preferred.
- Minimum 3 analyzed serum products.
- Product images/descriptions available.
- Direct crawler access to `/categories/serum`.
- Disclaimer visible.

Schema:
- CollectionPage
- ItemList
- FAQPage

### 4. Skincare Formula Transparency Score
Recommended URL: `/skincare-formula-transparency-score`

Target query:
`skincare formula transparency score`

Search intent:
The user wants to understand how product transparency is evaluated.

Page angle:
Glow Index can explain its scoring dimensions without claiming medical authority.

Direct answer:
A skincare formula transparency score evaluates how clearly a product presents its formula, category fit, product claims, pricing context, and available evidence. It is a research signal for shoppers, not a medical judgment.

Safe because:
It turns an existing score dimension into an educational page.

Schema:
- Article
- FAQPage

### 5. Glow Index Product Analysis Pages
Recommended URL pattern: `/rankings/[id]`

Target query:
`[brand] [product] AI skincare analysis`

Search intent:
The user is researching a specific product.

Page angle:
Existing product pages should become more extractable for AI search before new pSEO expansion.

Direct answer template:
Glow Index analyzed [Brand] [Product] as a [category] using multiple AI model perspectives. The page summarizes consensus score, formula/value reasoning, transparency signals, and safety-profile considerations for consumer research.

Safe because:
The route already exists and can be upgraded with structured extraction blocks and disclaimers.

Build requirements:
- Hide/noindex products without enough analysis.
- Add direct-answer block.
- Add FAQ section.
- Clarify AI consensus score vs consumer rating.
- Add BreadcrumbList schema.

## Recommended Build Order
1. Fix crawler access for discovery files and category/ranking routes.
2. Upgrade existing `/rankings/[id]` product pages with direct-answer blocks, disclaimer, FAQ, and schema clarity.
3. Build `/skincare-product-value-analyzer` as the safest evergreen use-case page.
4. Build `/categories/serum` only after analyzed serum count is confirmed.
5. Build `/skincare-formula-transparency-score` as an educational support page.

## Blocked Until Later
- Ingredient directory pages: blocked until structured ingredient data exists.
- Concern pages: blocked because medical-claim risk is too high.
- Dupe/value-alternative pages: blocked until structured similarity or formula-overlap criteria exist.
- Before/after social posts: blocked.
- Reddit skincare promotion: hold unless education-first and community-native.

## First Action For Implementation
Run the crawler check and fix the 403 challenge on discovery paths. If crawler access is still blocked, do not build more pages. Create the Cloudflare/Replit access fix task instead.

## Success Metrics
- Crawler check passes for discovery files.
- Search Console begins showing impressions for Glow product/category/methodology queries.
- AI-search checks can retrieve and cite product/value/formula transparency pages.
- No page uses medical, fake-testimonial, before/after, or unsupported "best for condition" claims.
