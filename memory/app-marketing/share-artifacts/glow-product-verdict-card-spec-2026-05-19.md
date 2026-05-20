# Glow Index — Product Verdict Card Spec
Date: 2026-05-19
App: Glow Index
Owner: Eve
Status: ready for design/build planning

## Strategic Verdict
Glow Index should lead with a **Product Verdict Card**: a shareable, shopping-decision artifact that answers: **“Would I buy this, skip it, or compare it?”**

This is stronger than a generic scanner screenshot because skincare users already search and share around product-level decisions: ingredient checker pages, Reddit “is this safe/worth it?” threads, Sephora/Ulta review mining, TikTok shelf-shopping demos, and best-product roundups.

Guardrail: frame as consumer research and product discovery. No diagnosis, treatment, medical promises, fake testimonials, fake before/after, or guaranteed outcomes.

## Evidence From Market Patterns
- SkinSort has product discovery, ingredient analyzer, comparison, and ingredient database pages; search snippets emphasize checking what ingredients do and when they might irritate. Source: https://skinsort.com/ and https://skinsort.com/ingredient-analyzer
- SkinSort product/app positioning includes “Check your products. Discover new ones that'll work for your skin. Tell others what's good.” Source: https://apps.apple.com/us/app/skinsort-skincare-scanner/id6478040418
- OnSkin leads with barcode/photo/name scanning and understanding what is inside products. Source: https://onskin.com/
- Yuka’s broad consumer scanner loop is “scan labels in the blink of an eye” and get an at-a-glance evaluation. Source: https://yuka.io/en/
- INCIdecoder wins search intent with easy-to-understand ingredient explanations and product/ingredient lookup. Source: https://incidecoder.com/
- EWG Skin Deep teaches users to look beyond a rating by explaining hazard + data availability. Source: https://www.ewg.org/skindeep/understanding_skin_deep_ratings/
- Reddit users in r/AsianBeauty and r/SkincareAddiction repeatedly ask for ingredient checker apps/sites and mention SkinSort, INCIdecoder, OnSkin, Yuka, Think Dirty, and CosDNA. Sources: https://www.reddit.com/r/AsianBeauty/comments/1lj8vpe/whats_actually_a_good_app_for_checking_ingredients/ and https://www.reddit.com/r/SkincareAddiction/comments/1ez292u/personal_which_skincare_app_or_website_is_best/
- TikTok/IG shopping demos show users rating products at Sephora/Ulta and reacting to scanner verdicts; visible pattern is fast product-by-product “yes/no/why” shopping judgment, not long education. Example search results: https://www.tiktok.com/@blake.vicknair/video/7626175347763039508 and https://www.instagram.com/reel/DT8hJgFEtFK/

## Card Promise
**“A clean, shareable verdict for a product you’re considering — score, why, value check, and what to compare next.”**

## Primary Use Cases
1. User scans/searches a skincare product while shopping.
2. Glow Index returns a product card with a verdict.
3. User saves/shares the card to TikTok, IG Story, Pinterest, Reddit, or a group chat.
4. Card links back to product page or scan flow.

## Card Formats

### 1. Square Social Card
- Size: 1080x1080
- Best for: Instagram carousel, Reddit image, Pinterest, product roundup thumbnails
- CTA: “Check another product at Glow Index”

### 2. Vertical Story/TikTok Card
- Size: 1080x1920
- Best for: TikTok green-screen/video overlays, IG Stories, Pinterest Idea Pins
- CTA: “Scan/search before you buy”

### 3. Compact Product Page Embed
- Size: responsive web component
- Best for: SEO product pages, comparison pages, roundups
- CTA: “Compare with another product”

## Required Card Fields

### Header
- Product name
- Brand
- Category: cleanser / moisturizer / serum / sunscreen / treatment-adjacent / body / other
- Product image if available
- Timestamp: “Analyzed [Month YYYY]”

### Verdict Block
Use one of four labels:
- **Strong Buy Signal** — strong formula/value fit based on available product data
- **Worth Comparing** — promising, but compare against cheaper/simpler alternatives
- **Check Fit First** — useful for some users; read the flags before buying
- **Skip Signal** — weak value, unclear formula story, or better alternatives likely

Avoid: “safe,” “unsafe,” “toxic,” “will cure,” “will clear acne,” “dermatologist-approved” unless externally verified and attributed.

### Score Block
Suggested composite score: **Glow Score / 100**

Subscores:
- Formula clarity: 0-25
- Ingredient usefulness: 0-25
- Sensitivity flags: 0-20
- Value per ounce: 0-20
- Evidence/review signal: 0-10

Safer wording:
- “Sensitivity flags” not “irritation risk diagnosis.”
- “Ingredient usefulness” not “clinical effectiveness.”
- “Evidence/review signal” not “proven results.”

### Why It Scored This Way
Three bullets max:
- **Formula:** plain-language note about notable ingredients/functions.
- **Fit flags:** fragrance, essential oils, strong actives, alcohol, heavy occlusives, or other common watch-items when present.
- **Value:** price/oz vs category alternatives.

### Best-Fit / Watch-Out Tags
Use cautious tags:
- Fragrance-free
- Contains fragrance
- Minimal formula
- Active-heavy
- Budget-friendly
- Premium-priced
- Compare before buying
- Popular but pricey
- Barrier-supporting ingredients present
- Exfoliating ingredients present
- Retinoid/retinal present
- SPF product — follow label directions

Avoid tags that imply diagnosis/treatment:
- “Acne-safe” unless changed to “acne-prone shoppers often check these ingredients”
- “Rosacea-safe”
- “Eczema-safe”
- “Fixes hyperpigmentation.”

### Comparison Prompt
One line:
- “Compare against: [Product A] / [Product B] / [Category leaderboard]”

### Source/Methodology Footer
Small footer:
- “Consumer product analysis based on ingredient list, product claims, available reviews, and price data. Not medical advice.”

### QR/Link Area
- QR or short URL to product page
- UTM/source tag: `utm_source=share_card&utm_medium=organic&utm_campaign=glow_verdict_card`

## Visual Direction
- Look: clean beauty editorial + data card, not scary/toxin app.
- Palette: cream/off-white background, black text, subtle green/gold score accent, red/orange only for mild “watch-out” notes.
- Typography: large product name, big verdict label, readable bullets.
- Avoid alarmist hazard graphics, skull icons, medical symbols, or fake dermatology branding.

## Example Copy Skeleton

```text
[Brand] [Product]
Glow Score: 82/100
Verdict: Worth Comparing

Why:
• Formula: includes humectants + barrier-supporting ingredients.
• Watch-outs: contains fragrance; sensitive-skin shoppers may want to compare.
• Value: mid-priced for this category.

Compare before you buy:
[Alt 1] vs [Alt 2]

Consumer product analysis, not medical advice.
Scan/search another product: glowindex.co
```

## Product Requirements

### Data Inputs
- Product name, brand, category
- Full ingredient list
- Product image URL
- Price and size when available
- Retailer URLs when available
- Review count/rating snippets when available
- Existing Glow Index score/rank

### Generation Logic
1. Normalize product/category data.
2. Calculate subscore breakdown.
3. Generate verdict label.
4. Select 2-3 why bullets.
5. Add 1-2 comparison alternatives.
6. Render image card.
7. Store card URL + source tags.
8. Add share buttons.

### Export Options
- Download PNG
- Copy link
- Share to Pinterest
- Share to X
- Save to camera roll on mobile
- Copy Reddit-safe markdown snippet

## Tracking
Minimum fields:
- product_id
- card_variant
- source URL or app screen
- share destination if user chooses
- generated_at
- clicked_back_at
- downstream signup/search/scan event

UTM/source tags:
- `share_card_product_verdict`
- `share_card_category_leaderboard`
- `creator_demo_card`
- `reddit_answer_card`

## Guardrail Copy Bank
Use:
- “May be worth comparing if you’re sensitive to fragrance.”
- “Ingredient functions are simplified for shopping research.”
- “Check the full label and patch-test according to product directions.”
- “Not medical advice.”

Do not use:
- “This guarantees a skin outcome.”
- “This is condition-safe.”
- “Toxic/clean/dirty” as the main framing.
- “Expert-approved” or endorsement language unless directly sourced.

## Initial Product/Card Targets
Start with products people already search and debate:
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

## Promoted Experiment Cards

## Experiment: Product Verdict Card From Search Pages

App: Glow Index
Date created: 2026-05-19
Owner: Eve
Decision state: planned

### Source Pattern
Source URL(s):
- https://skinsort.com/ingredient-analyzer
- https://skinsort.com/compare
- https://incidecoder.com/
- https://www.ewg.org/skindeep/understanding_skin_deep_ratings/
Observed pattern: Competitors turn individual products/ingredients into durable search pages and simple verdict/explanation interfaces.
Proof of traction: Multiple competitors rank around ingredient checking/product databases; Reddit users repeatedly recommend SkinSort and INCIdecoder as lookup tools.
Audience: Skincare shoppers searching product name + “ingredients,” “review,” “safe,” “worth it,” “dupe,” “sensitive skin.”
Competitor/incumbent gap: Existing pages are often ingredient-heavy or hazard-heavy; Glow can own “buy/compare/skip” value-aware verdicts without medical claims.

### Hypothesis
If we create shareable verdict cards for high-search skincare products and attach them to SEO product pages, then users will click/search/share because the card answers the buying decision faster than ingredient databases.

### Asset Needed
- Creative/share artifact: Product Verdict Card PNG + product page embed
- Copy/hook: “Before you buy [Product], check the Glow verdict.”
- Landing/app destination: `/products/[brand-product-slug]`
- Tracking link/source tag: `utm_source=seo&utm_medium=product_page&utm_campaign=glow_verdict_card`

### Distribution
Channel: SEO + Pinterest + Reddit-safe answer snippets
Borrowed audience target, if any: roundup writers and skincare creators reviewing popular products
CTA: “Compare another product”
Run date: TBD

### Measurement
Primary metric: product-page organic clicks and share-card clickbacks
Secondary metric: scan/search events from card pages
24h result:
72h result:
7d result:

### Decision
Scale / iterate / kill:
Reason:
Next action: build 10 card mockups for high-search products and publish as test pages.

Score: 31/35
- Audience fit: 5
- Repeatability: 5
- Proof: 5
- Cost: 5
- Conversion intent: 5
- Shareability: 4
- Competition gap: 2

## Experiment: Creator Shopping Demo Card

App: Glow Index
Date created: 2026-05-19
Owner: Eve
Decision state: planned

### Source Pattern
Source URL(s):
- https://www.tiktok.com/@blake.vicknair/video/7626175347763039508
- https://www.tiktok.com/@chareesbeauty/video/7221220377911971078
- https://www.tiktok.com/@esmarianacruz/video/7476215927047015723
Observed pattern: TikTok/IG creators use fast in-store or product-by-product verdict formats; scanner apps become props in shopping demos.
Proof of traction: TikTok search results show repeated product rating/scanner demo formats for Sephora, Yuka, OnSkin, and acne-prone shopping decisions.
Audience: Skincare buyers watching “shop with me,” “Sephora rating,” “is this worth it,” and ingredient-checker content.
Competitor/incumbent gap: Most scanner demos are generic safety/clean claims. Glow can pitch a less alarmist “value + formula + compare” card.

### Hypothesis
If creators receive one ready-made Glow verdict card for a product they already planned to discuss, then they can use it as a visual prop and drive qualified clickbacks because it makes their product take more concrete.

### Asset Needed
- Creative/share artifact: 9:16 Product Verdict Card customized to creator’s reviewed product
- Copy/hook: “I ran this through Glow Index before buying.”
- Landing/app destination: product verdict page
- Tracking link/source tag: `utm_source=creator&utm_medium=short_form&utm_campaign=shopping_demo_card_[creator]`

### Distribution
Channel: TikTok/IG creator outreach
Borrowed audience target, if any: micro skincare creators in borrowed-audience list
CTA: “Want me to run your next product through Glow?”
Run date: TBD

### Measurement
Primary metric: clicks/searches from creator source tag
Secondary metric: shares/saves/comments asking for more products
24h result:
72h result:
7d result:

### Decision
Scale / iterate / kill:
Reason:
Next action: create 5 no-obligation sample cards for creator-relevant products.

Score: 29/35
- Audience fit: 5
- Repeatability: 4
- Proof: 4
- Cost: 5
- Conversion intent: 4
- Shareability: 5
- Competition gap: 2

## Experiment: Reddit “Comparison Answer” Card

App: Glow Index
Date created: 2026-05-19
Owner: Eve
Decision state: planned

### Source Pattern
Source URL(s):
- https://www.reddit.com/r/AsianBeauty/comments/1lj8vpe/whats_actually_a_good_app_for_checking_ingredients/
- https://www.reddit.com/r/AsianBeauty/comments/10co82x/ysk_these_three_different_websites_that_can_help/
- https://www.reddit.com/r/SkincareAddiction/comments/1i2wurg/product_question_is_there_a_way_to_scan_products/
Observed pattern: Reddit users ask for ingredient tools, product comparisons, and “is this right for me?” decision help. Helpful tool mentions appear when framed as one source among others.
Proof of traction: Search results surface multiple Reddit threads with direct tool recommendations and product-checking behavior.
Audience: r/SkincareAddiction, r/AsianBeauty, r/Ulta, r/Sephora users researching products before purchase.
Competitor/incumbent gap: Most tools are either too hazard-score oriented or too ingredient-database oriented; Glow can provide concise comparison cards with transparent caveats.

### Hypothesis
If we answer existing product-comparison questions with a transparent mini-analysis and optional Glow card, then high-intent users will click through because the artifact helps compare without sounding like an ad.

### Asset Needed
- Creative/share artifact: compact 2-product comparison card
- Copy/hook: “I compared these by ingredient list + price/oz; here’s the quick read.”
- Landing/app destination: `/compare/[product-a]-vs-[product-b]`
- Tracking link/source tag: `utm_source=reddit&utm_medium=answer&utm_campaign=glow_comparison_card`

### Distribution
Channel: Reddit/community value-first replies where allowed
Borrowed audience target, if any: subreddit communities, not mods unless requesting permission for recurring posts
CTA: “Full comparison here if useful.”
Run date: TBD

### Measurement
Primary metric: Reddit referral clicks
Secondary metric: saves/upvotes/replies asking for additional comparisons
24h result:
72h result:
7d result:

### Decision
Scale / iterate / kill:
Reason:
Next action: prepare 3 comparison pages before any Reddit posting.

Score: 27/35
- Audience fit: 5
- Repeatability: 3
- Proof: 4
- Cost: 5
- Conversion intent: 5
- Shareability: 3
- Competition gap: 2

## Build Priority
1. Static mockup of Product Verdict Card for 10 products.
2. Product-page embed with share/download buttons.
3. UTM/source tagging and clickback logging.
4. Creator-demo variant.
5. Comparison-card variant.

## Top Recommendation
Build the **SEO product-page embed + shareable PNG** first. It compounds, gives creators a real asset, gives Reddit a non-spammy destination, and becomes the base artifact for every other channel.
