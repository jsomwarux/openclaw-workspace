# Glow Index — 10 Product Verdict Pages Status
Date: 2026-05-19
Repo checked: `/Users/jtsomwaru/projects/skincare-rankings`

## Status
Could not verify live/local analyzed product pages from the current repo database because:
- `DATABASE_URL` Postgres connection refused locally during Prisma lookup.
- `prisma/dev.db` in this repo exists but is empty.

The repo seed list does include several target products, but seed presence is not proof of live/analyzed verdict pages.

## Target 10 verdict-page candidates
1. CeraVe Hydrating Facial Cleanser — present in `scripts/seed.ts`; analysis status unverified.
2. Vanicream Gentle Facial Cleanser — not found in repo seed/search; needs add.
3. La Roche-Posay Toleriane Double Repair Moisturizer — seed has close match `Toleriane Double Repair Face Moisturizer`; confirm naming before publishing.
4. COSRX Advanced Snail 96 Mucin Power Essence — present in `scripts/seed.ts`; analysis status unverified.
5. The Ordinary Niacinamide 10% + Zinc 1% — present in `scripts/seed.ts`; analysis status unverified.
6. Paula’s Choice 2% BHA Liquid Exfoliant — seed has close match `Skin Perfecting 2% BHA Liquid Exfoliant`; confirm naming before publishing.
7. Anua Heartleaf 77 Soothing Toner — not found in repo seed/search; needs add.
8. Beauty of Joseon Relief Sun — not found in repo seed/search; needs add.
9. Tower 28 SOS Daily Barrier Recovery Cream — seed has `SOS Daily Rescue Facial Spray`, not the requested cream; needs add.
10. Drunk Elephant Protini Polypeptide Cream — not found in `scripts/seed.ts`; present only as a quick-request suggestion in `components/SeedSuggestions.tsx`; needs add unless already live in production DB.

## Exact add/analyze checklist
Use production/admin flow; do not create fake verdict pages.

1. Open the deployed admin/product management path with `ADMIN_KEY` available.
2. For each missing product, create a product record with brand, exact product name, category, and real price:
   - Vanicream Gentle Facial Cleanser — cleanser
   - Anua Heartleaf 77 Soothing Toner — toner
   - Beauty of Joseon Relief Sun — spf
   - Tower 28 SOS Daily Barrier Recovery Cream — moisturizer
   - Drunk Elephant Protini Polypeptide Cream — moisturizer
3. Confirm close-match products use the SEO target names or intentionally keep canonical names:
   - La Roche-Posay Toleriane Double Repair Moisturizer vs `Toleriane Double Repair Face Moisturizer`
   - Paula’s Choice 2% BHA Liquid Exfoliant vs `Skin Perfecting 2% BHA Liquid Exfoliant`
4. Trigger analysis for unanalyzed products via existing admin/batch analyze route:
   - `/api/batch-analyze?key=[ADMIN_KEY]&mode=unanalyzed&limit=10`
   - Use smaller batches if the engine queue is unstable.
5. After callbacks complete, verify each product has:
   - `Product.consensusScore` not null
   - `Product.lastAnalyzedAt` not null
   - at least one stage-2 `Analysis`
6. Visit each `/rankings/[id]` page and confirm the Product Verdict Card appears above the Glow Index summary.
7. After deploy, run crawler access diagnostic from workspace:
   - `cd ~/.openclaw/workspace && python3 scripts/glow_crawler_check.py`

## Evidence gathered
- `grep` in repo found target/close-match products in `scripts/seed.ts` and `components/SeedSuggestions.tsx`.
- Local Prisma Postgres query failed with `ECONNREFUSED`.
- Local `prisma/dev.db` is empty and has no `Product` table.
