# Passive Income Strategist Report — March 8, 2026

**Run time:** Sunday, March 8, 2026 — 7:31 AM ET  
**Scout report loaded:** memory/passive-income/2026-03-08-scout.md  
**Ideas evaluated:** 6  
**Passed saturation filter:** 6 (with caveats noted below)  
**Recommended (🟢 BUILD THIS):** 2  
**Watch (🟡):** 3  
**Pass (🔴):** 1  

---

## Saturation Filter Results

| Idea | Saturation Verdict | Notes |
|---|---|---|
| SUPPLEMENT SCORE | ✅ PASS | Not in passive income listicles. No free 3rd-party testing aggregator exists. ConsumerLabs is paywalled. Top10Supps is generic affiliate — not testing-focused. |
| QUOTE PILOT | ✅ PASS | Not in passive income listicles. ServiceM8 is a full-suite AU-focused tool, not a US $19/mo quoting-only play. |
| CAP TABLE SPLIT | ✅ PASS | Zero consumer awareness. Not in any passive income list. Genuinely unknown category. |
| ANCESTRYCANVAS | ⚠️ BORDERLINE | Family tree POD IS in passive income circles (customfamilytreeart.com, dearestforever.com, 60K+ Etsy listings). AI-narrative angle is new but the base product category is saturated in POD passive income content. Proceeding to analysis with uniqueness penalty applied. |
| SITEAUDIT.AI | ⚠️ BORDERLINE | Not in passive income listicles, but direct product competitors found: LinkBoss (builds silos, fixes orphans, auto-interlinks), LinkStorm, Junia AI. These already execute the core functionality. Proceeding with analysis with heavy uniqueness/competition penalty. |
| CRYPTO TAX NOMAD | ⚠️ WEAKENED | CryptoTaxMap.io found: 170 countries, crypto tax rates, lifestyle scores, relocation data. More competitive than Scout indicated. AI-personalized modeling (input your specific income → ranked countries) is still differentiated. Proceeding with adjusted competition scores. |

---

## 🟢 SUPPLEMENT SCORE

**Verdict:** 🟢 BUILD THIS | Score: **8.4/10**

### 1. The Opportunity
The supplement market ($52B, growing 7%/yr) has a massive trust problem: no free, permanent, searchable site aggregates third-party testing certifications (NSF, USP, Informed Sport) and presents them as clean brand scores. ConsumerLabs has a paywall. Reddit's r/Supplements (900K members) manually compiles meta-analyses that get 150 votes and 51 comments, then disappear. The gap is structural, not temporary — ConsumerLabs has kept its paywall for 20+ years and shows no sign of going free. JT already built the exact architecture (Glow Index), so this is a pattern replication into a market 5× larger. AI makes dynamic scoring possible: Claude reads COA language, categorizes certifications, and generates summary scores automatically as new products enter the database.

### 2. Positioning for Profit
- **Smartest niche**: Start with protein powders and pre-workout (highest purchase frequency, most Reddit debate). Expand to vitamins, fish oil, creatine on a rolling schedule. r/Supplements is the distribution channel.
- **Defensibility**: The data itself becomes the moat. Once n8n is scraping NSF/USP certification databases monthly and building the index, competitors need to replicate the same scraping infrastructure + manual review layer. First-mover SEO on "NSF certified protein powder" type queries compounds month over month. Community trust in r/Supplements accelerates inbound links.
- **What beginners get wrong**: Building a generic "best supplements" affiliate site (Top10Supps style). SupplementScore wins by being *certification-first*, not commission-first. Trust = conversion. The first thing on every product page is testing score, not an affiliate button.

### 3. Launch Plan
- **Fastest path to live in 7 days**: Coding agent builds a Next.js frontend with 50 manually curated top brands (protein, creatine, vitamin D). Claude generates the scoring rubric summaries for each. Deploy to Vercel. No scraping automation needed for launch — launch static, automate later.
- **Minimum viable version**: 50 brands × 3 categories, scoring only on NSF/USP/Informed Sport certifications (not full COA analysis). Amazon affiliate links on every product. Simple search. No account required.
- **Key tools**: Next.js (frontend, identical to Glow Index) + Claude API (scoring summaries) + n8n (NSF/USP database scraping, Amazon affiliate link generation) + Vercel (hosting) + Amazon Associates API (affiliate)

### 4. Monetization
- **How first dollar comes in**: Amazon affiliate click from a user who found the site searching "NSF certified creatine" on Day 1 with live users. No conversion path required — users are already in purchase mode.
- **Pricing model**: Primary: Amazon/iHerb affiliate (8-10% commission on supplements is material — a $50 protein tub = $4-5/sale). Secondary: $7/mo "SupplementScore Pro" — full brand history, full ingredient analysis, "stack score" for combined supplement regimens.
- **Path to $3K–$10K/month**: 500 affiliate clicks/day × 5% conversion × $4 average commission = $3,000/mo from affiliate alone. Pro tier at 500 subscribers × $7 = $3,500 added = $6,500 total. At 1,000 clicks/day (feasible with 100K monthly visitors), this hits $10K+/mo.

### 5. Automation Stack
- **What to automate first**: n8n workflow that hits NSF, USP, and Informed Sport certification APIs/pages monthly and updates brand certification status automatically. This is the core data moat — without it, the site stales.
- **AI's role**: Claude reads Certificate of Analysis (COA) PDFs when brands submit them, categorizes claims, flags discrepancies between label claims and test results, generates the 2-sentence brand summary shown on each product page.
- **How ongoing time approaches zero**: Month 1 = manual data curation + automation setup. Month 2 = n8n running nightly updates, Claude summarizing new entries. Month 3+ = zero-touch for existing categories; JT's only ongoing task is approving the weekly "new brands to add" queue (10 min/week).

### 6. 90-Day Execution Plan
- **Days 1–30 (Foundation)**: Coding agent builds Next.js site with 50 brand entries, affiliate links, search. Deploy. Post to r/Supplements introducing the site ("I built the free alternative to ConsumerLabs"). First affiliate revenue within 48 hours of posting. n8n scraping automation deployed by end of week 2.
- **Days 31–60 (Traction)**: Agent-driven posting on r/Supplements, r/PeterAttia, r/Fitness: answer "which brands are tested?" questions, reference the site. Add 200 more brands. Start ranking for "NSF certified [category]" queries. First Pro subscribers when "stack score" feature launches at end of this phase.
- **Days 61–90 (Scale)**: SEO flywheel compounds. Target 50K monthly visitors. Identify top 10 affiliate revenue drivers by category — double down on content for those. Consider niche email list ("Weekly Supplement Safety Report") as Pro upgrade hook. Target $1K–$3K/mo by Day 90.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 9 | 8 | 9 | 8 | 7 | 9 | 9 |

**Weighted overall: 8.4/10**

---

## 🟢 CRYPTO TAX NOMAD

**Verdict:** 🟢 BUILD THIS | Score: **7.8/10**

*Note: CryptoTaxMap.io exists (170 countries, static tax data + lifestyle scores). JT's differentiation is AI-personalized scenario modeling — input YOUR income, current country, lifestyle priorities → ranked recommendations with specific tax impact calculations. CryptoTaxMap shows you a map; CryptoTaxNomad tells you exactly what to do.*

### 1. The Opportunity
Crypto holders optimizing six-figure tax bills represent the highest-WTP audience in the nomad space, and there is no personalized AI decision tool for them. CryptoTaxMap.io has the data but no intelligence — it's a spreadsheet with a pretty interface. The real job-to-be-done is: "Tell me, given MY income and MY lifestyle preferences, where I should move and why." That requires AI modeling, not a map. JT holds a unique structural advantage: this is his personal life problem (crypto as primary income), so he understands the nuance that a generic builder won't. Tax law complexity is increasing globally (FATCA, CRS, expanding CBDC frameworks) — this problem will matter MORE in 3 years, not less.

### 2. Positioning for Profit
- **Smartest niche**: Start with US-based crypto holders looking to leave (largest addressable segment — the US exit tax situation is a huge pain point). Add EU holders, then global expansion. Focus early on the $100K-$1M crypto gain bracket — large enough to care, small enough that Big Four tax firms feel overkill.
- **Defensibility**: Two compounding moats. First: JT's own crypto credibility (@jts_14, @jt__crypto) drives authentic distribution into crypto Twitter — competitors without this audience can't replicate the launch. Second: As the subscriber base grows, user scenario data trains the AI model to generate better recommendations — each user makes the system smarter.
- **What beginners get wrong**: Building a generic "countries with no crypto tax" blog post in SaaS form. The value is personalization — the tool needs to ask specific questions (current country, citizenship, holding period, income level, desired lifestyle) and return a personalized ranked list, not a generic table. CryptoTaxMap made this mistake. JT avoids it by leading with the questionnaire flow.

### 3. Launch Plan
- **Fastest path to live in 7 days**: Coding agent builds the questionnaire flow (5 questions: current country, crypto income level, primary income type, lifestyle priorities, timeline) + Claude generates a personalized country report for top 5 recommendations. No account required for first report — email gate for the full PDF. Deploy to Vercel.
- **Minimum viable version**: 20-30 countries with AI-generated profiles. No n8n scraping automation at launch — seed the country data manually from public sources (IMI Daily, Coin Bureau). Automate the update layer in Week 2-3.
- **Key tools**: Next.js (questionnaire + report UI) + Claude API (personalized scenario modeling and country comparison) + n8n (monitors tax law changes from 5-10 government/crypto news sources, triggers country profile updates) + Stripe (subscription) + Resend (email delivery of reports)

### 4. Monetization
- **How first dollar comes in**: User completes the questionnaire, gets a preview of 2 countries free, hits a paywall for full 5-country report → Stripe $19/mo subscription. First paying user on Day 1 with live traffic.
- **Pricing model**: $19/mo Basic (country comparisons + quarterly updates), $99/mo "Relocation Plan" (personalized AI scenario modeling with income inputs + ongoing tax law alerts for your target country, downloadable PDF report).
- **Path to $3K–$10K/month**: 200 subscribers × $19 = $3,800/mo. 50 Relocation Plan subscribers × $99 = $4,950/mo. Combined at 250 total subscribers = $8,750/mo. This is a realistic 12-month target given the crypto Twitter distribution advantage.

### 5. Automation Stack
- **What to automate first**: The tax law update n8n workflow — monitor IMI Daily, government source feeds, and 3 crypto tax blogs for jurisdiction-level changes. Claude classifies the change (capital gains treatment, holding period, territorial tax, banking access) and queues it for country profile update. This is what keeps subscribers subscribed.
- **AI's role**: Claude is the core product engine — it takes the questionnaire inputs, loads the relevant country profiles from the database, runs the multi-factor comparison (tax impact + lifestyle fit + visa difficulty + banking access), and generates a personalized narrative recommendation with specific projections ("Based on your $180K/year crypto income, moving to Portugal saves you approximately $X compared to your current situation").
- **How ongoing time approaches zero**: Month 3+ = n8n handles the update monitoring, Claude handles all report generation. JT's only interaction is reviewing major tax law changes that trigger a full country profile rewrite (2-3 times/year, 1-2 hours each).

### 6. 90-Day Execution Plan
- **Days 1–30 (Foundation)**: Build questionnaire + report UI. Seed 25 countries. Post launch thread on crypto Twitter (@jts_14) — "I built the tool I wish existed when I started thinking about leaving the US for crypto tax reasons." Target 100 free users in week 1. First paid conversions by Day 7.
- **Days 31–60 (Traction)**: Post weekly crypto tax insights on X (automated from the country data). Engage r/ExpatFIRE and r/digitalnomad threads. Add 15 more countries. Launch Relocation Plan tier. Target $500–$1K MRR by end of month 2.
- **Days 61–90 (Scale)**: n8n monitoring live and updating country profiles. SEO on "crypto tax country comparison" queries. Target 100+ subscribers. Build "Tax Law Alert" email feature as Pro retention hook. Target $3K–$5K/mo by Day 90.

### Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 9 | 8 | 7 | 8 | 8 | 6 | 6 |

**Weighted overall: 7.8/10**

---

## 🟡 WATCH — ANCESTRYCANVAS

**Score: 6.9/10 | Blocking factor: Uniqueness**

**Value Prop:** "This helps gift-givers create personalized AI-generated family tree art that ships as a canvas print in 3 minutes." ✅

**Why 🟡 and not 🟢:**
- Uniqueness scores 5/10 — family tree POD art IS in passive income circles (60K+ Etsy listings, customfamilytreeart.com, dearestforever.com). The AI-narrative + AI-visual combination is new but the category is not hidden.
- Fails the uniqueness gating criterion (≥6 required for 🟢).
- Build complexity bump: image generation API integration (DALL-E 3 or Stable Diffusion) adds non-trivial complexity vs. JT's existing stack. JT hasn't shipped a POD product before.
- Revenue ceiling is capped without paid ads — seasonal gifting patterns mean lumpy income.

**What would make this 🟢:** If the AI-generated narrative layer becomes the moat (i.e., a beautiful 500-word written family history + AI art, positioned as a premium "Family Legacy" product at $149-199) rather than just a print. The *narrative* is the differentiator, not the print. Current positioning is still too close to existing POD.

**Scores:**
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 8 | 8 | 6 | 7 | 6 | 5 | 6 |

---

## 🟡 WATCH — QUOTE PILOT

**Score: 6.4/10 | Blocking factor: Autonomy**

**Value Prop:** "This helps solo HVAC/plumbing/electrical contractors create professional PDF quotes in 3 minutes instead of 30-60 minutes." ✅

**Why 🟡 and not 🟢:**
- Autonomy scores 5/10 — B2B SaaS for contractors is inherently support-heavy. Contractors will email when a quote is wrong. Regional pricing calibration requires ongoing maintenance. This is not passive income; it's a startup.
- Fails autonomy gating criterion (≥7 required for 🟢).
- ServiceM8 (AU) has AI quoting built in. While US market gap exists at $19/mo, the support burden makes this a customer-service business, not a vending machine.
- Marketing leverage is low — no viral loop; requires cold outreach to solo contractors.

**What would make this 🟢:** Partner with a trade association or contractor directory to get passive distribution. Build in a referral mechanism (contractors refer other contractors for discounts). Reduce support surface with tighter feature scope and guardrails.

**Scores:**
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 8 | 5 | 7 | 5 | 7 | 7 | 6 |

---

## 🟡 WATCH — CAP TABLE SPLIT

**Score: 6.3/10 | Blocking factor: Marketing Leverage**

**Value Prop:** "This helps startup ops teams and law firm paralegals split shareholder registers by investor jurisdiction in 10 minutes instead of 4-8 hours." ✅

**Why 🟡 and not 🟢:**
- Marketing leverage scores 3/10 — there is no way to market this passively. Startup ops people and law firm paralegals don't discover tools via SEO articles or social sharing. This requires cold LinkedIn DMs and direct sales. A fundamental incompatibility with passive income.
- Overall 6.3/10 passes the numerical bar but the marketing moat is fatal: without passive discovery, you're building a B2B sales job, not a passive income asset.
- Narrow total addressable market — genuine users are rare (cross-border cap table work is a niche of a niche).

**What would make this 🟢:** Distribution via legal tech marketplaces (LexisNexis, Clio app store), or a partnership with Carta/Pulley to offer this as an add-on. Without a built-in distribution channel, this sits on the shelf.

**Scores:**
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 8 | 5 | 7 | 3 | 6 | 9 | 8 |

---

## 🔴 PASS — SITEAUDIT.AI

**Score: 5.8/10**

**Why 🔴:**
- Direct competitors already executing: **LinkBoss** ("the only AI tool that builds silos, fixes orphans, and auto-interlinks in one click"), **LinkStorm**, **Junia AI** internal linking tool. These are funded, launched, and ranking.
- Uniqueness scores 4/10 — while the "AI content chaos" framing is clever, the underlying product (AI-powered internal linking + orphan page detection) is not novel.
- Fails uniqueness gating criterion (≥6 required) and overall score is below 🟡 territory.
- Even the specific positioning ("for sites that used AI to bulk-produce content") is addressable by telling existing users to position their marketing differently — not a real differentiation.
- levelsio test: No. This is a crowded B2B SEO SaaS with multiple competent competitors. Not a candidate for pieter's income dashboard.

---

## Portfolio Commentary

SUPPLEMENT SCORE is the strongest bet this week: it's a direct extension of the Glow Index pattern into a market 5× larger with a stronger community signal and clearer monetization path. Building it second (after Glow Index is activated with n8n) makes infrastructure sense — same architecture, same affiliate model, different dataset. 

CRYPTO TAX NOMAD is the higher-ceiling play with more build complexity: it requires country data curation, AI modeling calibration, and ongoing tax law monitoring. JT's crypto credibility is a genuine distribution advantage that no generic indie builder has. In a 12-month portfolio view: SupplementScore = steady affiliate compounding; CryptoTaxNomad = higher-WTP subscription with viral upside in crypto Twitter.

Together with Nash Satoshi (crypto rankings) and Glow Index (skincare rankings), a SupplementScore launch extends the "AI rankings + community trust + affiliate" flywheel into a third vertical — creating a defensible portfolio of niche data sites that reinforce each other's SEO authority over time.
