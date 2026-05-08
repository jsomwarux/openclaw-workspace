# Glow Index — JT Action Checklist

Created: 2026-05-07
Goal: make the deployed Glow SEO/GEO surfaces discoverable and ready for directory/backlink distribution.

## Current state

Built and deployed in repo `jsomwarux/skincare-rankings`:
- Product-page GEO improvements.
- `/categories` index.
- gated `/categories/[category]` pages.
- `/categories/serum` pilot.
- safe `/compare/[pair]` route.
- redirect-only `/products/[slug]` aliases.
- sitemap + `llms.txt` updates.

Do not build more routes yet.

---

## JT Step 1 — Confirm production pages in browser

Open these in a normal browser:

1. https://glowindex.co/rankings
2. https://glowindex.co/categories
3. https://glowindex.co/categories/serum
4. https://glowindex.co/llms.txt
5. https://glowindex.co/sitemap.xml

Reply to Eve with:
- `Glow pages visible` if all load.
- Or paste the failing URL/error if one fails.

Why this matters:
- Generic crawler-style tools are hitting Cloudflare `Just a moment`, so browser confirmation tells us the deploy is alive while we separately fix crawler access.

---

## JT Step 2 — Take/select screenshots for directory submissions

Need 3–5 screenshots. Use desktop screenshots first unless a directory asks for mobile.

Recommended screenshots:

### Required 1 — Homepage / hero
URL: https://glowindex.co
Capture: headline + above-the-fold positioning.
Purpose: shows what Glow Index is.

### Required 2 — Rankings page
URL: https://glowindex.co/rankings
Capture: visible ranked product list + score/tier UI.
Purpose: proves this is a ranking/research product.

### Required 3 — Product analysis page
URL: pick any fully analyzed product from rankings.
Capture: product score + score breakdown/reasoning/FAQ if visible.
Purpose: proves depth beyond a list.

### Optional 4 — Serum category page
URL: https://glowindex.co/categories/serum
Capture: category intro + top serums.
Purpose: proves SEO/category discovery surface.

### Optional 5 — llms/sitemap proof
Usually not needed for directories, but useful for internal proof.

Screenshot instructions:
1. Open the page.
2. Use macOS screenshot: `Cmd + Shift + 5`.
3. Choose `Capture Selected Window` or `Capture Selected Portion`.
4. Save files with this naming:
   - `glow-homepage-hero.png`
   - `glow-rankings.png`
   - `glow-product-analysis.png`
   - `glow-serum-category.png`
5. Put them in one folder.
6. Send/upload them to Eve, or tell Eve the local folder path if they are on the Mac mini.

Quality rules:
- No browser tabs full of private info.
- No admin pages.
- No screenshots showing API keys, account info, or private data.
- Prefer clean browser window, 1440px-ish width if possible.

---

## JT Step 3 — Cloudflare / crawler-access check

This is the most important technical blocker for AI SEO/GEO.

Problem:
- Eve's crawler-style fetches hit Cloudflare `Just a moment` for `/categories`, `/categories/serum`, `/sitemap.xml`, and `/llms.txt`.
- Humans can see pages, but AI/search bots may not.

If Glow uses Cloudflare dashboard:
1. Open Cloudflare dashboard.
2. Select `glowindex.co`.
3. Go to Security / WAF / Bot settings.
4. Check if Bot Fight Mode, Super Bot Fight Mode, JS Challenge, or Managed Challenge is applied globally.
5. Add skip/allow rules for these paths:
   - `/robots.txt`
   - `/sitemap.xml`
   - `/llms.txt`
   - `/rankings*`
   - `/categories*`
6. If Cloudflare lets you choose verified bots, allow major search/AI crawlers:
   - Googlebot
   - Bingbot
   - Applebot
   - GPTBot
   - ClaudeBot
   - PerplexityBot
7. Save.
8. Tell Eve: `Cloudflare crawler rules updated`.

If Glow does not use Cloudflare directly:
1. Check Replit/domain/proxy settings for bot protection or challenge pages.
2. Look for any setting that forces JS challenge before static files.
3. Static crawler files should be public without JS:
   - `/robots.txt`
   - `/sitemap.xml`
   - `/llms.txt`
4. Tell Eve what setting you find.

Do not weaken all security if there is a narrow path allow/skip option.

---

## JT Step 4 — Approve first directory target

Recommended first directory: Uneed.

Why Uneed first:
- Low ceremony.
- Good backlink/discovery surface.
- Less launch-day pressure than Product Hunt.

Use copy from:
`memory/app-marketing/directory-packs-glow-index.md`

Uneed fields:
- Name: Glow Index
- URL: https://glowindex.co
- Tagline: AI-powered skincare rankings without brand hype.
- Description: Glow Index compares skincare products with multi-model AI analysis across ingredients, value, transparency, safety profile, skin compatibility, and usability. It helps shoppers research formulas and marketing claims before buying. Not medical advice. Not a dermatologist recommendation. Consumer research only.
- Categories: AI, Beauty, Consumer Products
- Tags: skincare, beauty tech, AI skincare, skincare rankings, product research, formula comparison, value comparison

Before submitting:
- attach selected screenshots.
- avoid medical claims.
- avoid “best for acne/eczema/rosacea.”
- avoid dermatologist language.

After submitting:
- paste the listing URL to Eve.
- Eve will update `directory-submissions.md`, App Marketing scoreboard, and tracking.

---

## JT Step 5 — Do not do Product Hunt yet

Hold Product Hunt until:
- screenshots are selected,
- first users/traffic exist,
- 10–20 supporters are lined up,
- first comment/story is drafted,
- launch-day posts are prepared.

Product Hunt is a launch wave, not the first backlink.

---

## Eve-owned follow-ups

Eve owns:
- update directory tracker after JT submits.
- update App Marketing OS scoreboard.
- rerun crawlability checks after Cloudflare settings change.
- prepare Futurepedia / TAAFT / AlternativeTo submissions.
- keep pSEO expansion blocked until structured data supports it.

Eve does not submit externally without JT approval.
