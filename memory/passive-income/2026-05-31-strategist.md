# Passive Income Strategist Report - 2026-05-31

Scout file evaluated: `memory/passive-income/2026-05-31-scout.md`

## Executive Decision
- Ideas evaluated: 6
- Passed saturation filter: 5
- Recommended BUILD: 1
- WATCH: 4
- PASS: 1
- TrustMRR status: stale soft evidence only. `weekly-trustmrr.json` was fetched 2026-05-23, so it was used as a pattern lens, not verdict proof.
- Existing Mission Control passive-income cards checked: VendorChase Desk, EarStack Studio, GymPhoto Coach, HomeGym FitCheck, LabelLaunder, WalkthroughProof, Spreadsheet-to-Agent Desk, RuleWatch NYC, CollectionProof, PDRN Decoder. None were near-identical to today's BUILD recommendation.

## Saturation Filter Results

| Idea | Saturation Result | Notes |
|---|---|---|
| ContractorProof Packet | Passed | Search showed official state license tools, construction risk software, and one Reddit mention of ContractorShield in Arizona. Not a generic passive-income listicle idea. Risk is execution complexity, not saturation. |
| ClaimRisk Cards for Beauty Sellers | Passed | Search showed enterprise cosmetics/compliance tools and TikTok Shop policy content, but not a small one-shot beauty claim-risk card product. Strongly differentiated if tied to Glow Index's evidence-first posture. |
| ChargeReady Rank | Passed with caution | EV charger passive-income content is saturated, but that is about owning chargers, not portable-charger compatibility reports. Comparison pages are crowded. |
| SwitchStack Escape Plan | Passed with caution | Generic "Notion alternatives" and SaaS migration content are saturated. The screenshot/export-to-migration-plan artifact is differentiated enough to evaluate. |
| GrantRoute Desk | Saturated/crowded | Search surfaced GrantStation, Granter, Granted AI, GrantPal, AI grant lists, and founder grant directories. The category is crowded and support-heavy. |
| BookClubFit Index | Passed with weak evidence | Book club apps and recommendation tools exist, but the host-fit scoring wedge is not saturated. Demand evidence is thin. |

## Verdict Summary

| Idea | Verdict | Score | Blocking Factor |
|---|---:|---:|---|
| ClaimRisk Cards for Beauty Sellers | 🟢 BUILD THIS | 7.5/10 | Must avoid medical claims and keep it evidence-card/compliance-assist, not legal advice. |
| ContractorProof Packet | 🟡 WATCH | 6.9/10 | Strong pain, but state-by-state license data, COI verification limits, and homeowner liability language make autonomy weaker. |
| ChargeReady Rank | 🟡 WATCH | 6.8/10 | Search demand is real, but comparison/listicle competition is heavy and recommendation accuracy creates support/refund risk. |
| SwitchStack Escape Plan | 🟡 WATCH | 6.6/10 | Great JT edge, but custom migrations drift into service work unless scoped to one export type and one buyer. |
| BookClubFit Index | 🟡 WATCH | 5.8/10 | Pleasant product, but weak urgency and low willingness to pay cap the opportunity. |
| GrantRoute Desk | 🔴 PASS | 4.8/10 | Crowded grant-finder market, high freshness burden, and support-heavy application expectations. |

## ClaimRisk Cards for Beauty Sellers
**Verdict:** 🟢 BUILD THIS | Score: 7.5/10

### 1. The Opportunity
ClaimRisk Cards is a micro-tool for small beauty sellers, TikTok Shop affiliates, and skincare microbrands that need to publish product copy without making unsupported cosmetic or medical claims. The user pastes a product page, label text, or affiliate script and gets a risk score, flagged claims, safer copy variants, and a buyer-facing evidence card. It works right now because TikTok Shop and AI-generated affiliate content are increasing claim volume faster than small sellers can review it. It should still work in 3-5 years because beauty commerce, platform enforcement, buyer skepticism, and safe-claim needs are durable.

### 2. Positioning for Profit
- **Smartest niche**: TikTok Shop skincare affiliates and microbrands selling trend-driven ingredients where hype creates claim risk: PDRN, centella, cica, barrier repair, glass skin, firming neck products, milky moisturizers.
- **Defensibility**: Start from Glow Index's evidence-first scoring stance, keep a claim taxonomy, save anonymized flagged-claim patterns, and build ingredient/category pages that explain what sellers can safely say. Over time, the dataset becomes a vertical claim-risk corpus instead of a generic AI copywriter.
- **What beginners get wrong**: They build an "AI copywriter for ecommerce" and promise compliance. JT's version should say: "This flags risk and suggests safer wording; it is not legal advice." The moat is conservative scoring, source-backed reasoning, and a buyer-facing evidence artifact.
- **TrustMRR reality check**: TrustMRR shows reported MRR in AI content/SEO/AEO, creator tools, CPG commerce enablement, and compliance/documentation-adjacent products. That validates the monetization pattern, but also warns that generic AI content tools are crowded. The vertical beauty-claim/evidence-card wedge is the reason this stays differentiated.
- **Niche-intel check**: Skincare/Glow guidance explicitly favors evidence-first, skeptical, buyer-protective products and rejects medical/diagnosis language. This idea matches the approved Glow lane if it avoids treatment promises and fake before/after claims.
- **Agent-native fit**: Strong. A content agent preparing TikTok Shop scripts could call the tool before publishing and receive JSON risk fields, safer copy, markdown evidence cards, cited claim notes, and an approval boundary for the human seller.
- **TikTok Shop/social commerce fit**: Strong. This is digital-first, no inventory, and tied to an owned JT asset. Revenue event is a report/card, not product fulfillment.
- **Behavioral demand**: Primary motive is fear of loss and buyer protection. Sellers care because platform penalties, chargebacks, and public embarrassment hurt. Shoppers care because the card says whether a claim is evidence-backed or just hype.

### 3. Step-by-Step Build Instructions
**Phase 1 - MVP (Days 1-7):**
1. Clone the Glow Index scoring posture into a new Next.js route/app named `claimrisk` and define the MVP around paste-in text or URL input only.
2. Create a claim taxonomy JSON: medical/treatment claim, unsupported percentage, before-after claim, ingredient-evidence gap, missing disclaimer, vague puffery, and safe cosmetic claim.
3. Build a Claude-powered analyzer that returns strict JSON: `risk_score`, `flagged_claims`, `reason`, `safer_copy`, `evidence_card_markdown`, `disclaimer`, `sources_needed`.
4. Add a simple report page with a printable/shareable evidence card and a Stripe checkout for a $15 one-off card.
5. Deploy on Replit or Vercel, run 10 seeded tests against trend products, and verify no output makes diagnosis/treatment promises.

**Phase 2 - Traction (Days 8-30):**
1. Create 30 public SEO pages for high-risk skincare claim patterns: "PDRN claim checker", "centella serum claim checker", "glass skin claim substantiation", "TikTok Shop skincare claims".
2. Add product-page screenshot OCR as an optional upload for sellers who work from TikTok/Amazon screenshots.
3. Create a weekly OpenClaw trend scrape from Exploding Topics/Glow inputs that queues new ingredient pages and claim examples.
4. Add $29/month for 20 cards and save a seller's previous cards.
5. Publish comparison content: "What beauty sellers can say vs. what gets risky."

**Phase 3 - Scale (Days 31-90):**
1. Add a lightweight API endpoint for content agents: `POST /api/claimrisk/analyze`.
2. Add team/microbrand plan at $99/month with weekly trend-risk brief.
3. Add affiliate-safe buyer-facing product cards that link back to Glow Index rankings where relevant.
4. Build an approval log so sellers can show what changed before publishing.
5. Expand from skincare to cosmetics only after the skincare taxonomy is stable.

- **Minimum viable version**: Paste text/page copy, risk score, flagged claims, safer rewrite, evidence card, Stripe one-off checkout. Defer screenshot OCR, saved accounts, API, and trend alerts.
- **Full tech stack**: Next.js + Stripe + Claude API + structured JSON schema + Glow Index evidence taxonomy + OpenClaw weekly trend cron + optional OCR/vision after MVP + Vercel/Replit deploy.
- **Operating cost at scale**: $30-80/month for hosting/domain/logging plus Claude usage. Expected per-card AI cost roughly $0.03-$0.20 depending on source text length and evidence depth, supporting $15 one-off pricing.
- **Realistic build timeline**: 7 days for a coding agent MVP; 14 days if Stripe, saved reports, and OCR ship together.

### 4. Monetization
- **How first dollar comes in**: A TikTok Shop seller pastes product copy, sees a preview risk score, then pays $15 via Stripe to unlock the full evidence card and safer copy variants.
- **Pricing model**: $15 one-off card; $29/month for 20 cards; $99/month microbrand plan with saved card history and weekly trend-risk brief.
- **Affiliate programs / revenue splits**: Optional later via Glow Index skincare affiliate links. Do not rely on affiliate revenue for MVP.
- **Path to $3K/month**: 100 sellers on $29/month = $2,900 plus 10 one-off cards = $150. This is reachable with SEO plus TikTok Shop affiliate communities if the output is immediately useful.
- **Path to $10K/month**: 70 microbrands at $99/month = $6,930 plus 110 sellers at $29/month = $3,190. Requires saved history, weekly brief, and agency/affiliate-manager distribution.

### 5. Marketing Strategy (Autonomous - runs without JT)
**Primary channel**: SEO + TikTok/Reddit education aimed at TikTok Shop beauty sellers and skincare affiliates.

**Week 1 launch post**:
- Platform: Reddit
- Community/subreddit: r/TikTokShopSellers or beauty seller/founder communities where allowed
- Post format: "I built a claim-risk checker for beauty product copy - paste a claim and it gives safer wording"
- Hook: "Most TikTok Shop beauty claims are not malicious. They are just one sentence away from being risky."

**Ongoing autonomous marketing stack**:
- SEO pages: Publish 3 ingredient/claim pages per week from the trend queue.
- X/LinkedIn: Post one teardown per week: risky claim, why it is risky, safer version.
- TikTok/Reels: Short text-video format: "TikTok made me buy it, but can the brand prove the claim?"

**SEO strategy**:
- Primary search terms: `cosmetic claim substantiation`, `TikTok Shop beauty claims`, `skincare product claims checker`, `beauty compliance copy`, `cosmetic claims examples`.
- Content pages to create: "PDRN claims checker", "Before and after skincare claims: safer wording", "TikTok Shop beauty claims checklist", "Cosmetic vs medical skincare claims", "Ingredient evidence card examples".
- Timeline to first organic traffic: 6-10 weeks if pages are indexed and internally linked from Glow Index.

**Viral / referral mechanism**:
- The output can be shared as a buyer-facing evidence card. Sellers have an incentive to show "we cleaned up this claim" and affiliates can share skeptical product teardowns.

**Paid acquisition**:
- Skip for MVP. Unit economics can support small retargeting only after conversion from organic/referral is proven.

**What to do in Month 1 manually (before automation)**:
- Review 25 real TikTok Shop beauty listings and save claim patterns.
- Publish 5 public teardown examples.
- Ask 3 microbrand/affiliate sellers for copy samples.
- Verify every output disclaimer is conservative.

### 6. Automation Stack
- **What to automate first**: Claim analysis and evidence-card generation.
- **Full automation sequence**: User submits copy -> Claude returns strict JSON -> app renders risk card -> Stripe unlocks report -> report saved -> OpenClaw weekly cron adds new trend ingredients and claim examples -> content cron drafts public teardown pages.
- **AI's role in the product**: Classify claims, explain risk, rewrite safely, generate evidence-card markdown, and identify missing proof.
- **AI's role in marketing**: Turn anonymized claim patterns into SEO pages and weekly teardown posts.
- **How ongoing time approaches zero**: After Month 3, new trend pages, example cards, and claim taxonomies update from a weekly review queue; JT only reviews edge-case safety rules monthly.
- **OpenClaw integration**: Yes. Add a weekly `claimrisk-trend-queue` cron only after MVP conversion signal; it pulls Glow/Exploding Topics skincare terms and drafts claim-page candidates.

### 7. Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Agent-Native Bonus | TikTok Bonus | TrustMRR Bonus |
|---|---|---|---|---|---|---|---|---|---|---|
| 8.0 | 7.2 | 8.2 | 8.0 | 7.0 | 8.3 | 7.4 | 6.0 | +0.3 | +0.3 | +0.2 |

**Core weighted total:** 6.7/10  
**Bonus-adjusted total:** 7.5/10  
**Verdict gate:** Passed value proposition, autonomy, build feasibility, uniqueness, and agent-native/human buyer demand gates.

## WATCH Ideas

### ContractorProof Packet
**Verdict:** 🟡 WATCH | Score: 6.9/10

**Value proposition test:** This helps a homeowner decide whether to hire a contractor before signing or wiring a deposit, usually within the same day. Specific and urgent.

**Demand validation:** Strong. Search surfaced state license verification tools, official contractor lookup pages, and Reddit discussion around contractor vetting and COI verification. The pain is real: public databases are fragmented and homeowners do not know what a clean packet should include.

**Competition landscape:** Official state sites solve pieces; construction risk software is aimed at contractors/enterprise, not homeowners. ContractorShield appears as an Arizona-specific example. Competition is medium but fragmented.

**TrustMRR reality check:** Adjacent validation/API and local-business software comps support paid verification artifacts. No direct comp. Revenue evidence is soft.

**Vision Fit:** Model task is OCR/document extraction from estimates, COIs, and text screenshots. Defensibility is the checklist, state links, risk taxonomy, and source-cited artifact. Risk is legal/liability framing and false confidence. Estimated per-analysis cost: $0.05-$0.40 depending on document length.

**Agent-native fit:** Strong for property-management/vendor-vetting agents, but human approval is mandatory.

**Behavioral demand:** Fear of loss is intense. A homeowner facing a $10K-$80K project has urgency this week.

**Build reality:** Buildable in 2-3 weeks if limited to one or two states plus document risk language. Not safe to market as universal contractor verification at launch.

**Why not BUILD:** The first version risks becoming a state-by-state compliance data product with support questions. COI authenticity cannot be fully verified unless the user obtains broker-issued proof. Score is close, but autonomy is not strong enough yet.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Bonus |
|---|---|---|---|---|---|---|---|---|
| 8.3 | 5.9 | 6.2 | 7.0 | 7.2 | 9.0 | 8.0 | 5.8 | +0.2 |

**Best next validation:** Build one free "NY contractor pre-hire checklist" page and see if it earns search or Reddit traction before building uploads/payments.

### ChargeReady Rank
**Verdict:** 🟡 WATCH | Score: 6.8/10

**Value proposition test:** This helps a new EV owner or renter choose a portable charger/adapter that actually works with their car and parking setup in 10 minutes. Specific and useful.

**Demand validation:** Good. Exploding Topics signal says portable EV charger has strong search momentum. Search showed active comparison pages and Reddit anxiety around charging. However, passive-income SERPs are polluted by EV charging station income, not the product idea.

**Competition landscape:** Wirecutter, Car and Driver, PlugShare, KBB, charger brands, and niche affiliate pages already cover broad EV charger recommendations. The wedge is renter-fit/compatibility scoring, not generic "best charger."

**TrustMRR reality check:** No direct comp. Affiliate/comparison monetization is plausible but not validated by TrustMRR records.

**Agent-native fit:** Medium. A car-buying or road-trip agent could request a ranked SKU list with adapter warnings, but humans still care most.

**TikTok/social commerce fit:** Good. Comparison demos and renter-safe kits are content-native. Still, inaccurate recommendations can create return/refund/support drag.

**Behavioral demand:** Control and fear of being stranded are strong. Urgency happens when someone buys an EV or plans a trip.

**Build reality:** Buildable in 2 weeks using a normalized SKU/spec database, affiliate links, and a questionnaire. Accuracy burden is non-trivial because charger standards and vehicle compatibility change.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Bonus |
|---|---|---|---|---|---|---|---|---|
| 8.1 | 7.0 | 7.0 | 7.4 | 6.4 | 7.8 | 6.3 | 4.5 | +0.3 |

**Best next validation:** Publish a single "portable EV charger fit checker for renters" page with 20 SKUs and measure search impressions before building payments.

### SwitchStack Escape Plan
**Verdict:** 🟡 WATCH | Score: 6.6/10

**Value proposition test:** This helps a small ops team decide whether and how to leave Notion/Airtable/ClickUp before a renewal or workflow break, in one afternoon. Specific and JT-relevant.

**Demand validation:** Tool-switching intent is real, but generic alternatives pages are saturated. Search showed endless Notion/ClickUp/Airtable comparison content and workflow migration tooling for enterprise products.

**Competition landscape:** Comparison content is strong. Exact screenshot/export-to-migration-plan products are weaker, which is the opportunity.

**TrustMRR reality check:** Analytics/data products and AI SEO/content products validate messy-data-to-decision monetization, but this can easily become consulting instead of passive software.

**Vision Fit:** Model task is screenshot/export understanding and workflow/data-model extraction. Defensibility is JT's ops handoff pattern library and migration risk taxonomy. Risk is customer-specific edge cases. Estimated per-analysis cost: $0.10-$0.60.

**Agent-native fit:** Strong. A business-ops agent reducing SaaS spend could buy a markdown plan, CSV field map, task checklist, and risk register.

**Behavioral demand:** Frustration and control are real, but urgency usually appears around renewals or broken workflows.

**Build reality:** Buildable in 2 weeks if scoped to one source stack and one output format. Broad multi-tool migration support turns into a support queue.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Bonus |
|---|---|---|---|---|---|---|---|---|
| 7.7 | 5.8 | 7.4 | 6.4 | 6.5 | 7.0 | 7.2 | 4.8 | +0.3 |

**Best next validation:** Make a one-off "Airtable-to-Notion escape plan" generator for one common workflow, not a universal migration app.

### BookClubFit Index
**Verdict:** 🟡 WATCH | Score: 5.8/10

**Value proposition test:** This helps a book club host pick a book the group will finish and discuss before the next monthly meeting. Specific, but not painful enough.

**Demand validation:** Weak to moderate. Book club apps, recommendation apps, and random pickers exist. Search did not show strong paid demand for a fit-scoring product.

**Competition landscape:** Goodreads, StoryGraph, Fable, Bookclubs, Book Movement, Readfeed, and random picker sites occupy much of the discovery/coordination space. The host-fit angle is narrower but may be too small.

**TrustMRR reality check:** No direct comp. Creator/community subscription comps are too indirect to support a BUILD verdict.

**Agent-native fit:** Medium. A planning agent could buy a shortlist, but there is little reason to pay repeatedly unless the output is excellent.

**TikTok/social commerce fit:** Medium. BookTok hooks are strong, but monetization through affiliate links and $5 shortlists is modest.

**Behavioral demand:** Belonging and taste identity exist, but urgency is low. This is shareable, not painful.

**Build reality:** Very buildable with Open Library, Google Books, NYT Books, and Claude classification. The issue is revenue, not engineering.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Bonus |
|---|---|---|---|---|---|---|---|---|
| 7.2 | 8.3 | 8.5 | 6.2 | 3.8 | 5.7 | 6.2 | 4.5 | +0.1 |

**Best next validation:** Build no app. Post 10 book-club-fit rankings as content and watch for saves/shares.

## PASS Idea

### GrantRoute Desk
**Verdict:** 🔴 PASS | Score: 4.8/10

**Value proposition test:** This helps a founder find fitting grants/accelerators and assemble an application packet before deadlines. Specific enough, but the market expectation quickly becomes "help me apply."

**Demand validation:** There is demand, but it is already served by grant directories and AI grant tools. Search surfaced GrantStation, Granter, Granted AI, GrantPal, AI Grant, and broad startup grant lists.

**Competition landscape:** Strong and crowded. Existing tools already promise continuous scanning, eligibility checks, and drafting.

**TrustMRR reality check:** Career/education and document-package comps exist, but they do not overcome category crowding.

**Agent-native fit:** Good on paper: eligibility JSON, deadline feed, checklist, answer bank. The problem is not agent readability; it is freshness, trust, and application support.

**Behavioral demand:** Hope/FOMO is real but can become manipulative if framed poorly. Founders act near deadlines, but churn is likely after one application cycle.

**Build reality:** Discovery freshness, eligibility edge cases, and application writing expectations make this support-heavy. It is not passive enough.

| Longevity | Autonomy | Build | Marketing | Revenue | Behavioral | Uniqueness | Competition | Bonus |
|---|---|---|---|---|---|---|---|---|
| 6.8 | 4.0 | 5.8 | 5.5 | 5.8 | 6.2 | 3.2 | 2.8 | +0.2 |

## Already Queued Ideas
None. Existing `[PI]` Mission Control cards are adjacent backlog, but no active card is identical or near-identical to ClaimRisk Cards.

## Portfolio Commentary
ClaimRisk Cards is the right kind of passive-income bet for JT because it extends an existing owned asset, Glow Index, instead of starting another disconnected app. It also fits the broader portfolio direction alongside Nash Satoshi and Glow Index: narrow ranking/trust artifacts that can serve humans now and agent-readable workflows later.

## Mission Control Action
Add one active card:
- `[PI] Build: ClaimRisk Cards — beauty claim-risk reports for TikTok Shop sellers`

