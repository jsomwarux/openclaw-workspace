Purpose: review-only X draft from the 2026-06-18 heartbeat content lane. Do not post automatically.

Source proof:
- Glow crawler gate passed after the public-route fix.
- Product SEO/GEO pass shipped in `jsomwarux/skincare-rankings` commit `2fa05cf`.
- Verification: source assertion, lint, build, and `scripts/glow_crawler_check.py` all passed.

Platform: X
Lane: App Growth / App Marketing OS as builder-credibility proof

Draft:

Glow crawler access passed on `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, and `/categories/serum`, so I did not make five new SEO pages.

I pushed `2fa05cf` to upgrade the product pages that already had intent:

- `AI skincare analysis` heading on `/rankings/[id]`
- source tag `glow_seo_product_analysis_20260618` on `view_product`
- category links out of each product page
- validation log still shows `all_clear=true`

Boring order, but probably the right one:

make it crawlable
tag the traffic
improve the page with intent
then add volume
