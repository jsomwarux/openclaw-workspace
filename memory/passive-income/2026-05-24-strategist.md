# Passive Income Strategist — 2026-05-24

**Recovery note:** This report was generated manually after the 3 PM strategist cron returned `status=ok` but produced no strategist artifact and no Telegram delivery. Pre-strategist handoff check passed.

## Executive Summary
- **Ideas evaluated:** 6
- **Passed saturation filter:** 5/6
- **Recommended:** 2 BUILD, 3 WATCH, 1 PASS
- **BUILD:** EarStack Studio, VendorChase Desk
- **WATCH:** SubSwap Chef, GymPhoto Coach, RP Monetization Radar
- **PASS:** BeginnerAffiliate Brief
- **Already queued:** GymPhoto Coach is near-identical to existing MC task `[PI] Build: HomeGym FitCheck — apartment gym fit reports`; skipped duplicate build card.

**Portfolio commentary:** This week's best winner is not another generic AI tool; it is either a narrow visual paid artifact (EarStack Studio) or a productized exception desk from JT's actual consulting lane (VendorChase Desk). EarStack fits the Glow-style consumer ranking/affiliate portfolio; VendorChase fits the long-term “consulting patterns become reusable products” portfolio and has stronger JT defensibility than most B2C ideas.

## Saturation Filter Results
| Idea | Search result | Reddit result | Saturation verdict |
|---|---|---|---|
| EarStack Studio | Results were piercing guides/Pinterest/Byrdie, not passive-income listicles. | r/piercing has planning/opinion demand, not passive-income guru threads. | Passes — niche behavior exists; monetization angle not listicle-saturated. |
| SubSwap Chef | Results were Food Network/FoodSubs/NYT substitution references. | Reddit asks for food tools and substitution guides. | Passes saturation, but existing free reference content is strong competition. |
| VendorChase Desk | Search returned real-estate passive-income/property management content, not vendor-follow-up SaaS listicles. | Reddit focuses on PM income and landlord operations, not this micro-desk. | Passes — the exact exception layer is not overexposed. |
| GymPhoto Coach | Fitness passive-income listicles exist, but not photo-to-equipment-plan. | Reddit has personal trainer/passive-income threads and a direct “photo equipment → plan” demand receipt from scout. | Passes but already queued via HomeGym FitCheck-adjacent card. |
| BeginnerAffiliate Brief | Top results are Smart Passive Income, Udemy, generic beginner guides, and Reddit passive-income affiliate threads. | Multiple Reddit threads already frame affiliate marketing as passive income for beginners. | 🔴 Saturated — too close to guru/listicle territory. |
| RP Monetization Radar | Results show FiveM/Tebex monetization guides and many stores. | Reddit asks how servers make money and discusses monetization. | Passes narrowly if framed as data radar, not another guide/script store. |

## 🔁 Already Queued
- **GymPhoto Coach** overlaps with active MC task: `[PI] Build: HomeGym FitCheck — apartment gym fit reports` (`todo`). Same core mechanism: photo/visual gym context → personalized fitness/equipment planning. GymPhoto is more workout-plan focused and HomeGym FitCheck is more equipment-purchase focused, but they share enough stack, audience, and distribution that creating a separate build card would split focus. Recommendation: fold the hotel/apartment-gym workout-plan variant into the existing HomeGym FitCheck build as a Phase 2 report type.

## Full Scoring Snapshot
| Idea | Verdict | Score | Main blocker / reason |
|---|---:|---:|---|
| EarStack Studio | 🟢 BUILD THIS | 7.3/10 | Strong identity/commerce/visual wedge; must handle safety disclaimers carefully. |
| VendorChase Desk | 🟢 BUILD THIS | 7.6/10 | Best JT-shaped B2B wedge; less pure passive, but strongest defensibility. |
| SubSwap Chef | 🟡 WATCH | 6.7/10 | Real demand but crowded free SEO/reference landscape and low willingness to pay. |
| GymPhoto Coach | 🟡 WATCH / 🔁 queued-adjacent | 6.9/10 | Good demand receipt, but duplicate with HomeGym FitCheck and lower revenue ceiling. |
| BeginnerAffiliate Brief | 🔴 PASS | 4.6/10 | Saturated, guru-adjacent, trust/distribution problem bigger than build. |
| RP Monetization Radar | 🟡 WATCH | 6.6/10 | Interesting GTA/FiveM shovel, but community access and data reliability need validation first. |

---

## EarStack Studio
**Verdict:** 🟢 BUILD THIS | Score: 7.3/10

### 1. The Opportunity
EarStack Studio lets someone upload an ear photo and receive a curated-ear/stacked-lobe plan: placement ideas, spacing risks, healing sequence, jewelry style board, and affiliate product links. It works right now because `stacked lobes` has strong trend/search growth and the current user behavior is fragmented across Pinterest, piercer consultations, and Reddit “what should I add?” posts. It can still work in 3-5 years because body jewelry is identity-driven, repeat-purchase, visual, and not dependent on one platform trend. AI vision makes the first personalized draft cheap enough to sell as a $7-$12 paid artifact instead of requiring a human stylist/piercer for every plan.

### 2. Positioning for Profit
- **Smartest niche**: “Plan your stacked lobes before you book” for people with existing 1-3 lobe piercings considering the next 1-4 placements.
- **Defensibility**: The moat is a growing library of ear-shape examples, safe spacing rules, style tags, jewelry affiliate performance, and before/after plan templates — not generic image prompting.
- **What beginners get wrong**: They overpromise medical/piercing advice or make a generic jewelry moodboard. JT's version should be explicit: style planning + conversation prep for a licensed piercer, not diagnosis or guaranteed placement.

### 3. Step-by-Step Build Instructions
**Phase 1 — MVP (Days 1–7):**
1. Create a Next.js app with upload form: ear photo, current piercings, desired vibe, metal preference, budget, healing tolerance, and “when are you booking?”
2. Build a vision prompt/rules pipeline that detects visible lobes/cartilage/current jewelry and returns structured JSON: landmarks, current holes, suggested zones, uncertainty flags.
3. Seed 30 style templates: minimalist gold stack, asymmetrical silver, maximalist gems, office-safe, healing-first, low-budget, hypoallergenic.
4. Generate a report page with: suggested sequence, “ask your piercer” checklist, risks/unknowns, jewelry starter kit, affiliate links, and a shareable blurred preview.
5. Add Stripe checkout for a $9 one-time plan and deploy to Vercel; verify with 5 synthetic/example ear photos and manual safety disclaimers.

**Phase 2 — Traction (Days 8–30):**
1. Add pSEO pages: “stacked lobe ideas for small ears,” “second lobe placement ideas,” “gold curated ear starter plan,” etc.
2. Build a TikTok/Pinterest content loop: before photo → anonymized AI plan → “3 mistakes this avoids.”
3. Add jewelry affiliate feeds from Etsy/Amazon/BodyArtForms/Laura Bond-style brands where available.
4. Add “piercer consultation PDF” export for users to bring to appointments.
5. Collect opt-in before/after submissions to improve examples and social proof.

**Phase 3 — Scale (Days 31–90):**
1. Launch a $12/mo style board with seasonal jewelry drops and healing-stage reminders.
2. Add local piercer directory/referral pages if traffic clusters by city.
3. Add “gift mode” for friends buying jewelry based on someone’s existing stack.
4. Convert top performing plans into Pinterest pins and programmatic idea pages.
5. Add agent/API output: JSON plan + product list for personal shopping agents.

- **Minimum viable version**: Single-photo upload, one report, no account system, no local piercer directory, no subscription.
- **Full tech stack**: Next.js + Vercel + UploadThing/S3-compatible storage + low-cost vision model + Claude for structured plan text + Stripe Checkout + affiliate links + SQLite/Supabase style/product catalog + OpenClaw content cron.
- **Operating cost at scale**: ~$30-$90/mo hosting/storage + $0.02-$0.10 per vision/LLM report + domain + payment fees; affiliate/catalog tooling optional.
- **Realistic build timeline**: 7-10 days for MVP via coding agent; 3-4 weeks for polished affiliate/pSEO version.

### 4. Monetization
- **How first dollar comes in**: User pays $9 at Stripe checkout to unlock the full ear-stack plan after seeing a free teaser.
- **Pricing model**: Free teaser; $9 one-time plan; $19 premium plan with 3 style variants; $12/mo style board/healing reminders later.
- **Affiliate programs / revenue splits**: Jewelry/aftercare affiliate links via Amazon Associates, Etsy affiliates/creator links where available, BodyArtForms-style body jewelry affiliate programs if accepted; assume 3-10% commission.
- **Path to $3K/month**: 250 paid plans × $9 = $2,250 + ~$750 affiliate revenue from 750 clicks × 10% purchase × $100 AOV × 10% commission.
- **Path to $10K/month**: 700 paid plans × $9 = $6,300 + $2K-$3K affiliate + 150 subscribers × $12 = $1,800.

### 5. Marketing Strategy (Autonomous — runs without JT)
**Primary channel**: TikTok/Pinterest visual transformation content plus pSEO for stacked-lobe planning searches.

**Week 1 launch post**:
- Platform: TikTok + Reddit soft launch
- Community/subreddit: r/piercing for feedback only; no spammy pitch
- Post format: “I built a tool that turns an ear photo into a piercing plan — roast the safety/disclaimer approach.”
- Hook: “Your next lobe piercing is semi-permanent. I built a way to preview the plan before you book.”

**Ongoing autonomous marketing stack**:
- TikTok/Pinterest: 3 anonymized plan transformations/week with “placement mistakes to avoid.”
- SEO: weekly generation of 5 intent pages around ear shape/style/placement queries.
- Reddit/manual seed: occasional value-first comments only where users ask for planning help.

**SEO strategy**:
- Primary search terms: stacked lobe ideas, curated ear planner, second lobe placement, ear piercing stack ideas, how to plan ear piercings.
- Content pages to create: “Stacked lobe placement guide,” “Curated ear planner for minimalist gold jewelry,” “What to ask your piercer before stacked lobes.”
- Timeline to first organic traffic: 6-10 weeks; Pinterest can hit faster if visuals are strong.

**Viral / referral mechanism**:
- The output is visual and identity-relevant. Users can share blurred/marked-up ear plans and style boards.
- Natural share trigger: “Which option should I book?” polls on TikTok/Instagram/Reddit.

**Paid acquisition**: Skip until affiliate conversion and paid-plan conversion are proven; if tested, cap CPA at <$4 for $9 plan.

**What to do in Month 1 manually (before automation)**:
1. Validate with 15 Reddit/Pinterest examples manually.
2. Ask 2 piercers for safety/disclaimer feedback.
3. Create 20 seed style pages.
4. Manually choose first affiliate jewelry list.
5. Post 5 transformation demos from permissioned or stock/sample images.

### 6. Automation Stack
- **What to automate first**: Report generation and affiliate product matching.
- **Full automation sequence**: User uploads → vision extracts landmarks/uncertainty → Claude generates plan from rule templates → Stripe unlocks report → email/PDF delivered → OpenClaw queues anonymized content if user opted in → weekly cron refreshes affiliate products and pSEO pages.
- **AI's role in the product**: Vision identifies ear/jewelry context; Claude converts structured observations into style options, sequence, and piercer questions.
- **AI's role in marketing**: Generates safe captions, pSEO pages, and transformation post drafts from anonymized plans.
- **How ongoing time approaches zero**: After Month 3, JT reviews safety exceptions and affiliate performance monthly; reports/content run automatically.
- **OpenClaw integration**: New weekly cron for pSEO ideas, affiliate link health, opt-in transformation draft queue, and conversion summary.

### 7. Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Purchasable Fit |
|---|---|---|---|---|---|---|---|---|
| 7 | 8 | 7 | 8 | 7 | 8 | 8 | 6 | 5/10 |
**Weighted total:** 7.3/10

**TrustMRR reality check:** Adjacent creator/commerce comps validate narrow paid artifacts and affiliate-commerce tooling, but no direct ear-planning MRR comp. Adds only slight confidence; demand evidence comes from visual identity behavior, not TrustMRR.

**Vision Fit:** Strong. The model task is constrained visual planning, but defensibility requires rules, disclaimers, templates, and product matching beyond generic prompting. Estimated AI cost per report can stay below $0.10.

---

## VendorChase Desk
**Verdict:** 🟢 BUILD THIS | Score: 7.6/10

### 1. The Opportunity
VendorChase Desk turns property/family-office vendor chaos into an exception queue: stuck jobs, owed updates, next approved follow-up, owner-ready summary, and audit trail. It works now because property and family-office operators still run critical work through spreadsheets, inboxes, texts, and memory even when they own PM software. It should still work in 3-5 years because vendor coordination, owner reporting, and approval boundaries are durable operational problems. AI makes the weekly summary/follow-up draft cheap; JT's edge is knowing not to automate sends from dirty data.

### 2. Positioning for Profit
- **Smartest niche**: Small NYC-area property managers/family offices with 10-150 doors/assets and recurring contractor/vendor follow-ups.
- **Defensibility**: JT can turn real consulting patterns into templates: exception taxonomy, approval states, owner summary format, and local-first deployment. Each client/workflow improves the template library.
- **What beginners get wrong**: They build a chatbot or full PM platform. The buyer needs an approval-first exception layer around existing systems, not another place to enter work orders.

### 3. Step-by-Step Build Instructions
**Phase 1 — MVP (Days 1–7):**
1. Create a local-first Next.js/SQLite dashboard with CSV import for work orders/vendor threads: property, vendor, last update, promised date, status, owner visibility.
2. Add rules that flag stale items: no update in N days, promised date missed, missing vendor, owner-facing blocker, needs approval.
3. Build Claude summary generator for `stuck_items.json`, owner weekly summary, and next follow-up draft — all source-cited to imported rows.
4. Add approval states: draft, approved, sent manually, skipped, escalated; log every action.
5. Seed with synthetic property/vendor data and one Altmark-shaped example; verify no message can be sent automatically.

**Phase 2 — Traction (Days 8–30):**
1. Package as a $199 template/checklist plus $49/mo hosted/private dashboard.
2. Create a demo video: “Owner asks what happened with the repair. Here is the answer in 30 seconds.”
3. Build import adapters for Gmail-export CSV, AppFolio-style work orders, and generic spreadsheet.
4. Add weekly PDF/markdown owner report export.
5. Use consulting outreach/proof assets to validate with 3 property/family-office prospects.

**Phase 3 — Scale (Days 31–90):**
1. Add inbox ingestion via n8n/Gmail labels for vendor update extraction.
2. Add client-specific rulesets: insurance, repairs, inspections, utilities, permits.
3. Add source-cited API outputs for agents: stuck_items.json, next_actions.csv, owner_summary.md.
4. Turn repeated workflows into installable templates.
5. Build light onboarding wizard to reduce setup support.

- **Minimum viable version**: CSV import + exception dashboard + weekly summary + draft follow-ups. No inbox sync, no AppFolio integration, no automated messaging.
- **Full tech stack**: Next.js + local SQLite/Supabase option + CSV importer + Claude API + n8n ingestion later + Stripe + PDF/Markdown export + OpenClaw weekly summary cron.
- **Operating cost at scale**: $20-$100/mo hosting/AI for small hosted customers; local-first installs can run nearly free after setup. Support burden is the real cost.
- **Realistic build timeline**: 1 week for demo/MVP; 3-4 weeks for sellable template; longer if inbox integrations are included.

### 4. Monetization
- **How first dollar comes in**: Sell a $199 VendorChase setup template/checklist or a $49/mo dashboard to a property operator after demoing their own spreadsheet.
- **Pricing model**: $199 one-time template; $49/mo for up to 25 active work orders; $149/mo for local-first/family-office install; consulting upsell separate.
- **Affiliate programs / revenue splits**: None needed. This is B2B subscription/template revenue.
- **Path to $3K/month**: 30 customers × $49 = $1,470 + 8 template sales/month × $199 = $1,592.
- **Path to $10K/month**: 50 customers × $149 local-first/pro tier = $7,450 + 15 template/setup sales × $199 = $2,985.

### 5. Marketing Strategy (Autonomous — runs without JT)
**Primary channel**: Consulting-led demos + LinkedIn proof content; SEO later for “vendor follow-up property management spreadsheet.”

**Week 1 launch post**:
- Platform: LinkedIn
- Community/subreddit: property-management LinkedIn + targeted outbound, not broad Reddit
- Post format: “I rebuilt a vendor follow-up spreadsheet as an exception queue.”
- Hook: “A family office does not need a chatbot for repairs. It needs to know which vendor is about to embarrass them with the owner.”

**Ongoing autonomous marketing stack**:
- LinkedIn: weekly teardown of one vendor/follow-up failure mode.
- Email/outreach: one demo screenshot personalized to property/family-office prospects.
- SEO: monthly pages for work-order follow-up templates and owner summary examples.

**SEO strategy**:
- Primary search terms: property management vendor follow up, work order follow up template, owner report property management, contractor update tracker, property management exception dashboard.
- Content pages to create: “Vendor follow-up tracker template,” “Owner-ready repair summary example,” “Why property work orders still get stuck after PM software.”
- Timeline to first organic traffic: 3-6 months; outbound/proof content is faster.

**Viral / referral mechanism**:
- Low viral consumer potential. Referral comes from operators sharing a clean owner summary template or family-office peers seeing the demo.

**Paid acquisition**: Skip. Use consulting outreach and proof assets first.

**What to do in Month 1 manually (before automation)**:
1. Build demo with synthetic data and one real-client-inspired pattern.
2. Ask 3 property/family-office contacts for workflow feedback.
3. Record 2-minute Loom-style demo.
4. Draft one LinkedIn teardown and one outbound message.
5. Validate whether buyers prefer $199 template, $49/mo hosted, or $149/mo local-first.

### 6. Automation Stack
- **What to automate first**: Weekly stale-vendor detection and owner summary generation.
- **Full automation sequence**: Import spreadsheet/inbox rows → normalize vendor/job records → detect stale/missing/blocked items → generate draft follow-ups and owner summary → human approves/sends → audit log updates → weekly OpenClaw digest sends internal summary.
- **AI's role in the product**: Summarize messy notes, classify blockers, draft follow-ups, and produce owner-facing summaries from cited rows.
- **AI's role in marketing**: Generate anonymized teardown posts and prospect-specific demo blurbs from template examples.
- **How ongoing time approaches zero**: For template customers, self-serve import and weekly cron do the work; JT only improves templates monthly and handles support edge cases.
- **OpenClaw integration**: Use OpenClaw cron for weekly owner summary preview, data freshness guard, and template health report.

### 7. Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Purchasable Fit |
|---|---|---|---|---|---|---|---|---|
| 9 | 7 | 7 | 6 | 8 | 8 | 8 | 7 | 8/10 |
**Weighted total:** 7.6/10

**TrustMRR reality check:** Local business/agency software and analytics/data comps validate paid operational certainty. The realistic solo ceiling is lower than enterprise SaaS but $3K-$10K/mo is plausible if setup/support is controlled.

**Agent-native fit:** Strong. The same artifact humans want — stuck items, next actions, owner summary, approvals — is exactly what a property-ops agent would call mid-task. Human value exists today, so this is not imaginary-agent vaporware.

---

## SubSwap Chef
**Verdict:** 🟡 WATCH | Score: 6.7/10

**Value proposition test:** Helps home cooks/allergy households replace a missing ingredient with a ranked safe substitute in under 60 seconds without ruining texture/flavor. Passes.

**Analysis:** Demand is real and durable, especially for mid-cook fear-of-waste. Saturation is not from passive-income guru content, but the SERP is full of strong free references: Food Network, FoodSubs, NYT, Old Farmer's Almanac, and many charts. The winning wedge would need to be “risk of ruining this exact dish” plus allergies/pantry profile, not a generic substitute lookup.

**TrustMRR reality check:** Adjacent AI utility subscriptions validate narrow recurring tools, but the $5/mo consumer subscription is fragile. TrustMRR does not prove users will pay for an ingredient-substitution tool when free content ranks well.

**Behavioral demand:** Strong moment-of-need, but low willingness to subscribe. One-shot or API pricing may work better than consumer SaaS.

**Scorecard:**
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Purchasable Fit |
|---|---|---|---|---|---|---|---|---|
| 9 | 8 | 8 | 6 | 5 | 8 | 6 | 4 | 6/10 |
**Weighted total:** 6.7/10

**Blocking a green:** Free SEO competition is too strong and revenue ceiling is uncertain. Build only if a cheap validation page proves conversion on “will this ruin my [dish]?” queries.

---

## GymPhoto Coach
**Verdict:** 🟡 WATCH / 🔁 ALREADY QUEUED-ADJACENT | Score: 6.9/10

**Value proposition test:** Helps gym beginners/travelers turn a photo of available equipment into a safe workout plan in under 2 minutes. Passes.

**Analysis:** This has the cleanest direct demand receipt from the scout: someone asked for an app that creates workouts from photos of gym equipment because personal trainers are expensive. Vision fit is strong and build feasibility is high. The issue is overlap: MC already has HomeGym FitCheck, a visual gym/home-gym planning product. Also, fitness apps are brutally crowded, and the product needs a narrower buyer moment: hotel/apartment gym intimidation, not “another workout tracker.”

**TrustMRR reality check:** Health/wellness utility comps exist directionally, but not enough to overcome crowded fitness-app economics. This is a feature/wedge, not necessarily a standalone company yet.

**Vision Fit:** Strong for equipment recognition and plan generation. Defensibility must come from equipment database, safety constraints, and transient-gym templates, not generic Claude workout advice. Estimated AI cost can stay below $0.10/report.

**Scorecard:**
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Purchasable Fit |
|---|---|---|---|---|---|---|---|---|
| 8 | 8 | 8 | 7 | 5 | 8 | 7 | 3 | 6/10 |
**Weighted total:** 6.9/10

**Blocking a green:** Duplicate focus with HomeGym FitCheck and weak standalone differentiation in a crowded fitness market. Fold into existing card as Phase 2: “photo of hotel/apartment gym → 3-day plan.”

---

## BeginnerAffiliate Brief
**Verdict:** 🔴 PASS | Score: 4.6/10

**Saturation filter:** Failed. Top results include Smart Passive Income, Udemy, generic beginner guides, and multiple Reddit passive-income/affiliate threads. This is exactly the guru/listicle zone the strategist should avoid.

**Value proposition test:** Helps beginner affiliate marketers choose a less saturated product niche each week. It passes on paper, but the buyer is low-trust and surrounded by scammy claims.

**Analysis:** JT could build the research/report system, but distribution and trust are harder than product. The phrase “affiliate marketing beginners” attracts low-intent, low-retention buyers and compliance risks around income claims. TrustMRR creator/social/content comps validate monetization tooling broadly, but also reveal crowdedness — this would need an established audience before a paid brief works.

**Scorecard:**
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Purchasable Fit |
|---|---|---|---|---|---|---|---|---|
| 6 | 7 | 8 | 4 | 5 | 6 | 2 | 2 | 7/10 |
**Weighted total:** 4.6/10

**Reason for PASS:** Saturated and trust-poor. Do not build now.

---

## RP Monetization Radar
**Verdict:** 🟡 WATCH | Score: 6.6/10

**Value proposition test:** Helps FiveM/GTA RP server owners see competitor Tebex pricing/package patterns and launch monetization opportunities in a weekly dashboard. Passes.

**GTA VI / FiveM opportunity check:** This is the right posture — shovel/intelligence, not running a server or selling fragile scripts. It avoids daily moderation and copyright asset risk if it only monitors public stores/guides and produces pricing/category intelligence. However, the FiveM/Tebex ecosystem is already crowded with monetization guides, script stores, and community-specific knowledge. Distribution into server-owner communities is the hard part.

**TrustMRR reality check:** Analytics/data/attribution and creator monetization comps validate paid data products, but FiveM is niche and possibly ToS/platform-sensitive. Treat this as directional only.

**Scorecard:**
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Purchasable Fit |
|---|---|---|---|---|---|---|---|---|
| 6 | 7 | 7 | 5 | 7 | 7 | 8 | 5 | 6/10 |
**Weighted total:** 6.6/10

**Blocking a green:** Need validation from actual server owners and a reliable, policy-safe data source before building. Next action: manually produce one free “Tebex pricing radar” PDF for 10 popular servers and post it where server owners gather; if 3+ owners ask for updates, promote.

---

## Mission Control Pushes
- Created/confirmed required active `[PI] Build:` cards for the two 🟢 ideas.
- Skipped GymPhoto Coach duplicate because HomeGym FitCheck already exists and is active.

## State Update
- Append BUILD ideas to `agents/passive-income-scout/state.json`: EarStack Studio, VendorChase Desk.
