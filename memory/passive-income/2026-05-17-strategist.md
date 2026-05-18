# Passive Income Strategist — 2026-05-17

## Handoff
- **Scout file evaluated:** `memory/passive-income/2026-05-17-scout.md`
- **Pre-strategist handoff:** PASS — same-day Scout file exists, is non-empty, complete, and predates strategist run.
- **Mission Control active PI tasks before updates:** WalkthroughProof, Spreadsheet-to-Agent Desk validation, RuleWatch NYC validation, CollectionProof, PDRN Decoder.
- **Search note:** Local Brave search path returned usable saturation checks. Results were strongest for broad-market terms, not exact product names, so confidence is medium-high rather than exhaustive.

## Executive Decision
Two ideas clear the build bar this week:
1. **LabelLaunder** — the cleanest low-support, affiliate-friendly, pSEO-compatible visual utility.
2. **HomeGym FitCheck** — a credible InteriorAI-style niche with strong affiliate economics and visual shareability.

The rest should not consume build cycles yet. SafeRun is close but map/mobile complexity and prior RouteSafe overlap make it a WATCH. ScaleSub Chef is useful but too easy to replicate with generic AI unless it earns a niche data moat. Landlord Maintenance Desk is better as consulting IP or a validation card than passive SaaS. FiveM Tebex Ledger is a real shovel wedge, but support/install fragility keeps it below BUILD.

## Saturation Filter Results

| Idea | Saturation Check | Result |
|---|---|---|
| LabelLaunder | `LabelLaunder passive income` surfaced generic passive-income pages, not garment-care app listicles. `garment care label app` shows GINETEX/iPhone symbol lookup, but not a fabric-risk + affiliate workflow. | **Passed** — existing symbol decoders, not saturated as a passive-income niche. |
| SafeRun Routes | Exact passive-income search was noisy. Route-planner search shows Motera, Komoot, route generators, and safety-adjacent apps. Prior pipeline has RouteSafe history. | **Passed saturation but WATCH** — crowded route planning and prior overlap. |
| ScaleSub Chef | `ScaleSub Chef passive income` hit chef side-hustle listicles, not substitution tools. Substitution search shows NYT, Food Network, Allrecipes, macro alternatives. | **Passed saturation, but crowded utility surface.** |
| HomeGym FitCheck | Fitness passive-income listicles are broad. `home gym layout app equipment fit` shows RoomSketcher, Technogym, GymSmith, Planner5D. | **Passed with competition** — design tools exist, but photo-first apartment fit scoring is not listicle-saturated. |
| Landlord Maintenance Desk | Landlord passive-income results are saturated around rentals themselves. Maintenance spreadsheet search shows many templates. | **Passed only as narrow exception desk** — broad landlord/property management is saturated. |
| FiveM Tebex Ledger | Search shows Tebex monetization docs, passive-business FiveM scripts, Discord-role tooling, and server monetization threads. | **Passed** — not saturated as an audit/reconciliation tool, but fragile support surface. |

## Verdict Summary

| Idea | Verdict | Score | Primary Blocker / Reason |
|---|---:|---:|---|
| LabelLaunder | 🟢 BUILD THIS | 7.6/10 | Strong fear-of-ruining trigger, low support, affiliate/pSEO fit. |
| SafeRun Routes | 🟡 WATCH | 6.7/10 | Prior RouteSafe overlap, map/mobile complexity, safety trust burden. |
| ScaleSub Chef | 🟡 WATCH | 6.4/10 | Useful but generic-AI substitution risk; needs proprietary macro/texture rules. |
| HomeGym FitCheck | 🟢 BUILD THIS | 7.3/10 | Strong visual affiliate wedge; must avoid revisions/support creep. |
| Landlord Maintenance Desk | 🟡 WATCH | 6.6/10 | Great consulting IP, weak passive autonomy; already adjacent to Spreadsheet-to-Agent Desk validation. |
| FiveM Tebex Ledger | 🟡 WATCH | 6.8/10 | Real niche pain, but server-owner install/support burden is likely high. |

---

# Full BUILD Blueprints

## LabelLaunder
**Verdict:** 🟢 BUILD THIS | **Score:** 7.6/10

### 1. The Opportunity
A photo-first garment-care decoder for people buying or washing expensive cashmere, wool, silk, delicate resale, and high-maintenance fabrics. The user snaps a care label or product page and gets a plain-English risk report: wash/dry risk, shrink/bleed warning, detergent recommendations, and safe-at-home vs dry-clean guidance. This works now because resale/luxury clothing anxiety and cashmere-shampoo interest are rising, while existing tools mostly decode symbols instead of answering the real fear: “Will I ruin this?” In 3–5 years, the need persists because fabric care, resale shopping, and delicate-material purchases are not going away.

### 2. Positioning for Profit
- **Smartest niche:** “Don’t ruin expensive clothes” — cashmere, wool, silk, delicate resale, and luxury basics. Avoid broad laundry advice.
- **Defensibility:** Build a fabric/brand/risk corpus over time: label symbols, material blends, wash-risk heuristics, product recommendations, and user outcomes. The moat is not OCR; it is the care-risk database and SEO pages for specific fabrics/brands.
- **What beginners get wrong:** They build a generic laundry-symbol decoder. JT’s version sells reassurance and buyer protection: risk score, warning, and product/action recommendation.

### 3. Step-by-Step Build Instructions
**Phase 1 — MVP (Days 1–7):**
1. Create a Next.js app with a single upload flow: image upload → OCR/vision extraction → structured care-symbol/material JSON.
2. Seed a `fabric_rules.json` file for cashmere, merino wool, silk, linen, rayon/viscose, denim, and blends with safe-language warnings.
3. Build the Claude interpretation prompt to output: fabric, care symbols, risk score, “safe at home?” answer, top 3 warnings, product recommendations, and disclaimer.
4. Add affiliate-ready product slots for wool/cashmere shampoo, mesh bags, drying racks, fabric combs, and steamers.
5. Deploy on Vercel/Replit, verify one cashmere label and one silk/blend label produce useful reports.

**Phase 2 — Traction (Days 8–30):**
1. Create 30 SEO pages: “how to wash cashmere sweater,” “can you machine wash wool,” “wash silk blouse,” “dry clean only meaning,” etc.
2. Publish 10 short-form posts using real public product examples: “This $180 sweater label has one trap.”
3. Add a $7 “Closet Care Audit” PDF that lets users upload up to 10 garments.
4. Add email capture: “Save your garment-care card.”

**Phase 3 — Scale (Days 31–90):**
1. Add saved wardrobe reminders and seasonal care emails.
2. Add brand/fabric-specific pages from anonymized reports.
3. Add TikTok Shop / Amazon affiliate ranking pages for cashmere shampoos and delicate-care tools.
4. Add `/api/care-risk` JSON endpoint for resale/wardrobe agents.

- **Minimum viable version:** One photo upload, risk report, 5 fabric families, affiliate product cards, 10 SEO pages. No accounts, no saved closet, no reminders.
- **Full tech stack:** Next.js + Vercel/Replit + image upload storage + low-cost vision/OCR + Claude/Gemini interpretation + JSON fabric rules + Stripe for audit PDF + Amazon/TikTok Shop/ShareASale affiliate links + OpenClaw content cron.
- **Operating cost at scale:** ~$25–$120/mo depending on image volume; per analysis likely <$0.03–$0.08 if using low-cost OCR/vision + compact LLM output.
- **Realistic build timeline:** 7–10 days for MVP via coding agent; 3–4 weeks for pSEO/affiliate-ready version.

### 4. Monetization
- **How first dollar comes in:** User clicks an affiliate detergent/care-tool link or buys a $7 Closet Care Audit PDF after a free scan.
- **Pricing model:** Free single scan; $7 one-off closet audit; $6/mo premium for saved garments, reminders, travel/laundry mode.
- **Affiliate programs / revenue splits:** Amazon Associates and TikTok Shop for laundry-care tools; brand-specific affiliate programs for Laundress-style products where available. Expect low-single-digit to 10% commissions depending program.
- **Path to $3K/month:** 30,000 monthly visitors × 8% affiliate click × $1 average EPC = $2,400 + 100 audit PDFs × $7 = $700 → ~$3,100/mo.
- **Path to $10K/month:** 100,000 monthly visitors + 400 audit PDFs/mo + a small premium base of 500 users × $6/mo.

### 5. Marketing Strategy (Autonomous — runs without JT)
**Primary channel:** SEO + TikTok/short-form affiliate content around “expensive garment mistake” hooks.

**Week 1 launch post:**
- Platform: Reddit / TikTok / X
- Community/subreddit: r/laundry, r/femalefashionadvice-style communities only if rules allow; otherwise X/TikTok first.
- Post format: “I built a tool that tells you if you’re about to ruin a sweater.”
- Hook: “Most care-label apps translate symbols. They don’t tell you if your $250 sweater survives the wash.”

**Ongoing autonomous marketing stack:**
- SEO cron: generate and refresh fabric/brand care pages weekly.
- Short-form script cron: 3 weekly “label teardown” scripts using public product pages.
- Affiliate page updater: refresh detergent/tool recommendations monthly.

**SEO strategy:**
- Primary terms: “how to wash cashmere,” “cashmere shampoo,” “care label symbols,” “can you wash silk,” “dry clean only at home.”
- Pages: “Cashmere Wash Risk Checker,” “Wool Care Label Decoder,” “Silk Blouse Washing Guide,” “Dry Clean Only: Safe or Not?”
- Timeline to first organic traffic: 6–10 weeks for long-tail pages; faster if TikTok drives branded searches.

**Viral / referral mechanism:** The output is inherently shareable: “This label scored 82/100 risk.” People share expensive-item warnings and before-wash decisions.

**Paid acquisition:** Skip until affiliate EPC and audit conversion are measured.

**What to do in Month 1 manually:**
1. Test 25 real labels and correct the fabric rules.
2. Make 10 public teardown examples.
3. Apply to affiliate programs.
4. Seed one Reddit/X/TikTok launch post.
5. Add source/disclaimer language so trust feels serious.

### 6. Automation Stack
- **What to automate first:** SEO/content generation for fabric/brand care pages and weekly label teardown scripts.
- **Full automation sequence:** User uploads image → OCR/vision extracts label/material → Claude maps symbols/material to risk rules → report generated → affiliate products injected → optional PDF generated → anonymized insights feed SEO/content queue.
- **AI's role in product:** Extract label data, interpret risk using constrained rules, produce concise warnings/recommendations.
- **AI's role in marketing:** Generate fabric-care pages and short-form scripts from real product examples.
- **How ongoing time approaches zero:** Once rules, templates, and affiliate slots are stable, JT only reviews monthly product recommendations and edge-case failures.
- **OpenClaw integration:** Weekly pSEO/page refresh cron; weekly short-form script cron; monthly affiliate product audit.

### 7. Scores
**Vision Fit:** OCR + object/text understanding for labels/product pages. Defensible beyond generic prompting through fabric rules, brand/fabric pages, saved wardrobe history, and affiliate marketplace. Risk is moderate if it overclaims; use safe language and “risk guidance, not guarantee.” Per-analysis economics support free scans if affiliate/PDF conversion exists.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Native Bonus | TikTok/Social Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 8 | 8 | 8 | 6 | 8 | 8 | 6 | +0.1 | +0.2 |

**Weighted total:** 7.6/10

---

## HomeGym FitCheck
**Verdict:** 🟢 BUILD THIS | **Score:** 7.3/10

### 1. The Opportunity
A photo-based apartment/home-gym fit checker that turns room photos, dimensions, goals, and budget into a compact equipment plan with clearance warnings and ranked shopping recommendations. This works because compact treadmills and smart fitness equipment are trending, but users still waste money on equipment that does not fit their space, ceiling, noise constraints, or training goals. The AI angle makes the output room-specific instead of generic “best home gym equipment.” In 3–5 years, home fitness, hybrid work, and compact-space optimization should remain durable.

### 2. Positioning for Profit
- **Smartest niche:** Apartment and small-room gyms under 150 sq ft, especially low ceilings and renters.
- **Defensibility:** Build a database of equipment dimensions, clearance rules, noise/flooring constraints, and room-type templates. Over time, pSEO pages and affiliate conversion data improve the recommendations.
- **What beginners get wrong:** They build a generic design inspiration app. JT’s version is a buyer-protection fit check: “Will this fit, will it be safe, and what should I buy?”

### 3. Step-by-Step Build Instructions
**Phase 1 — MVP (Days 1–7):**
1. Build a Next.js upload form: room photos, dimensions, ceiling height, budget, goals, apartment/home checkbox.
2. Seed an equipment catalog with 40 compact products: treadmills, adjustable dumbbells, folding benches, racks, bands, bikes, mats.
3. Build a vision + rules pipeline that estimates constraints and asks for missing measurements instead of hallucinating.
4. Generate a report: usable zones, clearance risks, equipment shortlist, “do not buy” warnings, and affiliate links.
5. Add Stripe one-shot checkout for a $12 FitCheck report.

**Phase 2 — Traction (Days 8–30):**
1. Create pSEO pages for “best compact treadmill for apartment,” “home gym low ceiling rack,” “small bedroom gym layout,” etc.
2. Publish 10 visual teardown posts: “This apartment gym setup fails the clearance check.”
3. Add one free calculator: “Will this treadmill fit?” as top-of-funnel.
4. Build before/after report templates for shareability.

**Phase 3 — Scale (Days 31–90):**
1. Add brand/product comparison pages from affiliate catalog.
2. Add saved room profiles and seasonal deal alerts.
3. Add `/api/fit-check` for shopping agents.
4. Add generated mock layout images only after the rules engine works; do not start with image generation.

- **Minimum viable version:** User provides photos + dimensions; app returns report + 8 product recommendations. No revisions, no custom design service, no mobile app.
- **Full tech stack:** Next.js + Vercel/Replit + image upload + vision model + Claude rules + product catalog JSON/SQLite + Stripe + Amazon/Rogue/Walmart/brand affiliate links + OpenClaw pSEO/content cron.
- **Operating cost at scale:** ~$40–$150/mo plus per-analysis vision/LLM costs around $0.05–$0.20 depending image count.
- **Realistic build timeline:** 10–14 days for MVP; 4 weeks for polished affiliate/pSEO version.

### 4. Monetization
- **How first dollar comes in:** User pays $12 for a room-specific FitCheck report or clicks an affiliate equipment link after a free fit calculator.
- **Pricing model:** Free “will it fit?” single-product check; $12 one-shot layout report; $29 premium report with two generated alternatives; optional $6/mo deal/watchlist layer.
- **Affiliate programs / revenue splits:** Amazon Associates, Walmart, Rogue/fitness brand programs where available. High-ticket equipment makes even low commission rates meaningful.
- **Path to $3K/month:** 200 paid reports × $12 = $2,400 + $600 affiliate commissions from equipment clicks.
- **Path to $10K/month:** 500 paid reports × $12 = $6,000 + $4,000 affiliate commissions from high-ticket equipment and recurring deal pages.

### 5. Marketing Strategy (Autonomous — runs without JT)
**Primary channel:** SEO + short-form visual teardown content.

**Week 1 launch post:**
- Platform: Reddit/X/TikTok
- Community/subreddit: r/homegym carefully, if self-promo allowed; otherwise X/TikTok + SEO.
- Post format: “I built a tool that tells you whether home-gym equipment actually fits your room.”
- Hook: “A compact treadmill can still be a $600 mistake if your room fails the clearance check.”

**Ongoing autonomous marketing stack:**
- SEO pages: product-fit and room-type pages weekly.
- Short-form scripts: 3 room/equipment teardown posts weekly.
- Deal monitor: monthly affiliate product refresh.

**SEO strategy:**
- Primary search terms: “best compact treadmill for apartment,” “home gym low ceiling,” “small home gym layout,” “will treadmill fit in room,” “folding treadmill apartment.”
- Pages: “Apartment Treadmill Fit Checker,” “Low Ceiling Home Gym Guide,” “Best Compact Rack for Small Room,” “Home Gym Clearance Checklist.”
- Timeline to first organic traffic: 8–12 weeks; affiliate pages can compound over 6–12 months.

**Viral / referral mechanism:** Visual reports make natural before/after content. People like posting “rate my setup”; the app turns that into a score and shopping plan.

**Paid acquisition:** Only test paid search after report conversion and affiliate EPC are proven.

**What to do in Month 1 manually:**
1. Analyze 30 public home-gym photos and document recurring fit mistakes.
2. Build the equipment catalog from real dimensions.
3. Manually review first 20 reports to catch hallucinated measurements.
4. Apply for affiliate programs.
5. Publish 10 teardown posts.

### 6. Automation Stack
- **What to automate first:** Product catalog refresh + pSEO page generation from equipment dimensions and room constraints.
- **Full automation sequence:** User uploads photos/dimensions → vision extracts room/equipment clues → rules engine checks clearances → Claude writes constrained report → affiliate products injected → Stripe/PDF delivery → anonymized report topics feed content queue.
- **AI's role in product:** Interpret photos, ask for missing measurements, produce human-readable fit report.
- **AI's role in marketing:** Generate teardown posts and SEO comparison pages from catalog data.
- **How ongoing time approaches zero:** After the catalog/rules stabilize, monthly product refresh is the main maintenance.
- **OpenClaw integration:** Weekly content cron, monthly affiliate catalog audit, error-report review digest.

### 7. Scores
**Vision Fit:** Visual task is room/equipment understanding plus OCR/manual dimensions. Defensible beyond generic prompting through product dimension database, clearance rules, affiliate catalog, and pSEO pages. Risk is moderate because fit/safety cannot rely on guessed measurements; require user dimensions and disclaimers. Per-analysis cost supports one-shot pricing.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Native Bonus | TikTok/Social Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 7 | 7 | 8 | 7 | 8 | 7 | 5 | +0.1 | +0.2 |

**Weighted total:** 7.3/10

---

# WATCH / PASS Analysis

## SafeRun Routes
**Verdict:** 🟡 WATCH | **Score:** 6.7/10

**Value proposition test:** Helps women, night runners, heat-sensitive runners, and travel runners find a safer/more comfortable route before a run. Passes specificity.

**Why not BUILD:** The user pain is real, but route planning is crowded and the product drifts toward mobile/map complexity fast. “Safety” also creates trust/liability expectations. Prior RouteSafe history means this should be revived only if a narrow wedge is chosen: hotel/travel-run route packs or shade/heat scoring, not a full route planner.

**Agent-native fit:** Travel agents could purchase a $3 safe-run PDF/JSON for hotel itineraries, but that is future-facing. Human buyer value exists today, yet distribution would be the hard part.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Native Bonus | TikTok/Social Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 6 | 5 | 7 | 6 | 8 | 6 | 4 | +0.2 | +0.1 |

**Weighted total:** 6.7/10

**Blocking condition to turn green:** Reduce scope to “Travel Run Route Pack for hotel guests” or “Shade/Heat Route Score” with one city and no mobile app.

## ScaleSub Chef
**Verdict:** 🟡 WATCH | **Score:** 6.4/10

**Value proposition test:** Helps macro-focused home cooks and bakers swap missing ingredients while preserving grams, macros, texture, and allergens during a recipe. Passes specificity.

**Why not BUILD:** Demand is real and immediate, but the category is crowded with substitution charts, recipe sites, and generic AI answers. It only becomes interesting if JT builds a constrained rules engine with USDA/Open Food Facts data and texture-role scoring. Otherwise it is “ask ChatGPT, but with a nicer UI.”

**Agent-native fit:** Meal-planning agents could call it when pantry constraints conflict with a recipe. Output can be JSON with macro delta and confidence. That is a nice bonus, not enough for BUILD.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Native Bonus | TikTok/Social Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 8 | 7 | 6 | 5 | 7 | 5 | 4 | +0.2 | +0.1 |

**Weighted total:** 6.4/10

**Blocking condition to turn green:** Build a public substitution benchmark: “macro delta + texture risk” for 100 common swaps, then use that as the moat.

## Landlord Maintenance Desk
**Verdict:** 🟡 WATCH | **Score:** 6.6/10

**Value proposition test:** Helps 2–20 unit landlords turn tenant maintenance texts/photos/emails into prioritized tickets and weekly owner/vendor summaries within minutes. Passes specificity.

**Why not BUILD:** This is strategically aligned with JT’s consulting lane, but it is not passive enough. Small landlords create messy support, integrations, and trust issues. It belongs as consulting IP or a validation template under the existing Spreadsheet-to-Agent Desk / property-ops lane before becoming self-serve SaaS.

**Niche intel applied:** Property/family-office intel says these buyers need local-first exception layers, approvals, and audit trails. Tenant-facing or financial automation without clean data is a kill/defer. This idea should stay approval-first and not pretend full autonomy.

**Agent-native fit:** Strong in theory: property-manager agents can normalize incoming maintenance data into JSON tickets and owner digests. Human buyer value exists today. But distribution and trust are harder than build.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Native Bonus | TikTok/Social Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 5 | 7 | 5 | 7 | 8 | 7 | 5 | +0.3 | +0.0 |

**Weighted total:** 6.6/10

**Blocking condition to turn green:** Validate with one micro-landlord or Altmark-style workflow and prove the weekly digest reduces manual follow-up without support load.

## FiveM Tebex Ledger
**Verdict:** 🟡 WATCH | **Score:** 6.8/10

**Value proposition test:** Helps FiveM/QBCore server owners reconcile Tebex purchases, Discord roles, whitelist priority, and in-server entitlements nightly so paying players get the right perks and stale perks are removed. Passes specificity.

**GTA/FiveM lens:** This is the right kind of GTA VI shovel product: server owner/admin buyer, reusable script/template, clear ops problem, no copyrighted assets, and does not require JT to run a server. The downgrade is support burden: Discord/Tebex/QBCore installs are fragile, buyers may be nontechnical, and payment/role bugs create angry support tickets.

**Agent-native fit:** Good: a server-ops agent can run a nightly entitlement diff and produce JSON/CSV plus suggested Discord-role actions for owner approval.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Native Bonus | TikTok/Social Bonus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 6 | 6 | 6 | 6 | 8 | 8 | 5 | +0.2 | +0.0 |

**Weighted total:** 6.8/10

**Blocking condition to turn green:** Find 5 active server-owner complaints about entitlement/payment-role drift or ship a non-hosted audit script with install docs and no support promise.

---

# Already Queued / Prior Pipeline Overlap
- **SafeRun Routes / RouteSafe:** Prior state shows RouteSafe was pushed on 2026-04-26, but the current Mission Control active `[PI]` list did not show an active RouteSafe card. Treated as fresh for scoring, but not recommended as BUILD because the overlap and map/safety complexity remain real.
- **Landlord Maintenance Desk:** Adjacent to active Mission Control validation cards: `[PI] Validate: Spreadsheet-to-Agent Desk` and `[PI] Validate: RuleWatch NYC`. Not identical enough to skip, but close enough that it should remain validation/consulting IP before build.

# Mission Control Task Requirements
For every 🟢 BUILD idea, Mission Control should have exactly one active self-contained card:
- `[PI] Build: LabelLaunder — don’t ruin expensive clothes`
- `[PI] Build: HomeGym FitCheck — apartment gym fit reports`

# Portfolio Commentary
LabelLaunder and HomeGym FitCheck fit JT’s passive-income portfolio better than another broad app because they are narrow visual scorers with clear affiliate surfaces, one-shot paid reports, and pSEO compounding. They sit alongside Glow Index and Nash Satoshi as “rank/score/decision” properties — the pattern is not more SaaS, it is small trust artifacts that help people avoid bad purchases.
