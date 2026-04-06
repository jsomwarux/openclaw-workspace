# Passive Income Strategist Report — 2026-04-05

**Run time:** Sunday, April 5, 2026 — 2:01 PM ET
**Ideas evaluated:** 6
**Already queued (skipped):** 3
**New ideas analyzed:** 3
**Verdicts — 🟢 BUILD:** 0 | **🟡 WATCH:** 3 | **🔴 PASS:** 0

---

## Already Queued — Skipped Deep Analysis

These three ideas surfaced this week but are already on the Mission Control board with `todo` status. Not re-evaluated — still unbuilt.

| Idea | MC Task Title | Status |
|---|---|---|
| WATCHSCORE | [PI] Build: WatchScore — AI investment scores for affordable watches | todo |
| PERMITPILOT | [PI] Build: PermitPilot — AI building permit navigator for US homeowners | todo |
| PROGRAMSCORE | [PI] Build: ProgramScore — AI evidence-based strength program rankings | todo |

**Note:** PermitPilot and ProgramScore are the most time-sensitive of the existing queue. PermitPilot's ImmigrantIQ validation makes it low-risk. ProgramScore's M6 trend signal is strongest now.

---

## Saturation Filter Results

| Idea | In Passive Income Lists? | Reddit Passive Income Thread? | Result |
|---|---|---|---|
| TARIFFSWITCH | No | No | ✅ PASSES |
| DISCRANK | No | No | ✅ PASSES |
| VINYLIQ | No | No | ✅ PASSES (but strong competition found) |

All three pass the saturation filter. However, competition research reveals significant issues for DiscRank and VinylIQ.

---

## Deep Analysis

---

## TARIFFSWITCH
**Verdict:** 🟡 WATCH | Score: 7.2/10

### 1. The Opportunity
TariffSwitch helps US small importers (Shopify sellers, Amazon FBA, wholesale) who source from China find verified alternative suppliers in Vietnam, Mexico, India, or Turkey, with a side-by-side landed cost comparison (tariff rate + shipping + MOQ + lead time). The April 2025 China tariff spike to 145%+ created a $39B problem for 100K+ active SMB importers with no SMB-tier solution. Enterprise tools (Suplari, Order.co, Flexport) all require sales calls and $500+/month contracts. The structural shift is real — US-China trade diversification is now a board-level mandate at every size, not a news cycle. The tool's urgency peaks in 2026, but its value continues as "supply chain resilience" intelligence even if tariffs ease.

### 2. Value Proposition Test
✅ **Passes:** "This helps US small importers who source from China achieve a verified non-China supplier match with landed cost comparison in under 10 minutes."

### 3. Competition Landscape
- **Enterprise tier:** Suplari (alternative supplier recommendations), Order.co (procurement AI), Flexport (freight), Avalara (compliance) — all enterprise-only, $500+/month, require sales demos
- **SMB tier:** Government trade.gov FTA tool (tariff lookup only, no supplier matching), Alibaba search (no tariff cost context), ThomasNet (US domestic only, no international alternative matching)
- **Gap:** Zero SMB tools combining supplier discovery + tariff cost comparison in one UI
- **Competition weakness:** Strong — enterprise tools are inaccessible at price/complexity level. SMB gap is confirmed by the "6 different tools" Reddit complaint.

### 4. Build Reality Check
**Why this is 🟡 and not 🟢 — The Autonomy Problem:**

The core data challenge: supplier quality is not static. A verified listing on IndiaMART or ThomasNet doesn't mean that supplier will respond to a US SMB's cold email. When users pay $39/month and the supplier doesn't respond, they blame the product, not the supplier. This creates a support burden that makes full autonomy unrealistic without a clear "discovery tool, not vetting service" positioning enforced by copy.

- **Frontend:** Next.js product search (category + current country of origin → results page)
- **Backend:** n8n workflows querying supplier directories (ThomasNet API, IndiaMART partner API or scrape, Alibaba international alternatives section)
- **Claude API:** HS code classification from plain-English product description → tariff rate lookup → landed cost calculation
- **Stripe:** $39/month subscription, 3 searches/day; $0 free tier (1 search/week)
- **Data freshness:** n8n cron refreshes supplier listings weekly — this IS automatable
- **Operating cost at scale:** $150–250/month (hosting + API calls + directory access)
- **Realistic build timeline:** 4 weeks (the data pipeline is the hard part — directory scraping has fragile rate limits)
- **First revenue event:** First subscriber who gets a valid supplier result and converts within the 7-day free trial

### 5. Monetization
- **Path to $3K/month:** 77 subscribers × $39/month
- **Path to $10K/month:** 256 subscribers — achievable if SMB importer community adoption picks up via r/smallbusiness + Shopify ecosystem
- **Ceiling concern:** Urgency is tariff-driven. If a comprehensive US-China trade deal happens, demand softens. Pivot positioning to "supply chain resilience tool" mitigates this.

### 6. Marketing Strategy (Autonomous — runs without JT)
- **Primary channel:** r/smallbusiness + r/ecommerce (tariff news hooks are infinite right now)
- **SEO:** "China tariff alternative supplier," "Vietnam supplier for [product category]," "find non-China supplier US importer"
- **Agent posting:** Agent monitors r/smallbusiness tariff threads → posts helpful context + tool mention 2x/week
- **Viral mechanism:** Tool output screenshot ("Found 3 Vietnam suppliers for my category at 31% lower landed cost") is r/smallbusiness gold — natural share moment

### 7. What's Blocking 🟢
**Autonomy bottleneck.** Supplier data quality creates a support surface that breaks "zero-touch" assumption. Two paths to green:
1. **Reframe the product positioning:** Explicitly market as a "discovery starting point" not a vetting service (set expectation in onboarding). Reduces support requests from "why didn't this work?" to "great first step."
2. **Build a quality confidence score:** Claude scores each supplier match on: recency of listing, response rate (if available), number of verified reviews in the directory. Higher confidence score = higher trust. This automates the vetting layer partially.

If either path is built into the MVP, this becomes a 🟢. Proceed when you're ready to build the quality confidence score into Phase 1.

### 8. Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 8 | 5 | 6 | 8 | 8 | 9 | 8 |
**Weighted total: 7.2/10**
*Verdict: 🟡 WATCH — autonomy score (5) blocks green. Fix with quality confidence scoring layer.*

---

## DISCRANK
**Verdict:** 🟡 WATCH | Score: 7.15/10

### 1. The Opportunity
DiscRank would AI-score every PDGA-approved disc on beginner-friendliness, stability, distance potential, and wind performance using the flight number database and community review sentiment. 11M+ US disc golfers, fastest-growing sport 2020–2025, gear-obsessed community. The "which disc is right for me?" question floods r/discgolf weekly.

### 2. Value Proposition Test
✅ **Passes (narrowly):** "This helps beginner-to-intermediate disc golfers achieve a personalized disc recommendation based on arm speed and playing style in 60 seconds."

### 3. Competition Landscape — Updated (Scout Was Wrong)
**TryDiscs.com exists and is strong:**
- 2,065+ disc database across 105+ brands
- **Already has a Recommendation Quiz**
- Flight Matrix (visual flight path visualization)
- Out-of-production checker
- Multi-retailer price comparison across 215+ stores
- Active Reddit community presence — r/discgolf members love it

**Infinite Discs:** Advanced search with flight number range filters

**UDisc:** Course tracking + brand surveys, 12M+ users

**The actual gap:** TryDiscs' quiz is filter-based (you input min/max flight numbers). Nobody does AI-native plain-English recommendation: "Given your 280ft arm speed, you're a beginner who needs a very forgiving understable disc for hyzer flips — skip the Innova Destroyer and start with a Latitude 64 Compass." That reasoning layer doesn't exist.

The gap exists, but it's smaller than Scout claimed. TryDiscs is a legitimate competitor.

### 4. Build Reality Check
- PDGA approved disc database: public, 12,000+ discs with flight numbers
- Claude API: generates plain-English flight profiles and beginner rationale (this is the AI differentiator over TryDiscs)
- n8n: refreshes new disc approvals weekly, scrapes r/discgolf sentiment
- Affiliate via Infinite Discs (8–12% commission on $12–25 discs), Dynamic Discs partner program
- **Timeline:** 2 weeks (data is cleaner than supplier directories)
- **Operating cost at scale:** $75–100/month

### 5. Competition Assessment
TryDiscs has the data AND a quiz. The defensible differentiation for DiscRank requires:
1. AI-generated plain English recommendation narratives (not filter sliders)
2. "Avoid this disc because…" reasoning (TryDiscs doesn't explain why)
3. Outcome-based scoring: "Most recommended beginner disc by r/discgolf in the last 12 months" — community signal, not just flight numbers

### 6. What's Blocking 🟢
**Uniqueness score (5/10) blocks green.** TryDiscs.com already has a recommendation quiz with 2,065+ discs and community love. The AI narrative layer is differentiated, but not differentiated enough to score uniqueness ≥6 when a direct competitor exists and is community-endorsed.

Path to green:
- **Angle pivot:** Don't compete head-on with TryDiscs. Instead: "DiscRank: Community-voted disc rankings by outcome" — aggregate r/discgolf recommendation threads into a ranking table. This is genuinely different from TryDiscs' database. The positioning: "We rank discs by how many times the community actually recommended them. TryDiscs tells you specs. We tell you what players chose."
- This pivot reframes uniqueness from 5 → 8 and avoids the direct TryDiscs clash.

With this angle pivot, DiscRank becomes a 🟢 at ~7.8/10. Recommend revisiting with this framing.

### 7. Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 8 | 9 | 7 | 7 | 6 | 5 | 5 |
**Weighted total: 7.15/10**
*Verdict: 🟡 WATCH — uniqueness score (5) blocks green. Pivot to community-vote ranking angle to differentiate from TryDiscs.*

---

## VINYLIQ
**Verdict:** 🟡 WATCH | Score: 6.55/10

### 1. The Opportunity
VinylIQ would use Discogs API data (sold listings, want/have ratios, pressing scarcity) to generate "investment scores" for vinyl records as assets — helping collectors understand which pressings are appreciating, cooling, or worth buying.

### 2. Value Proposition Test
✅ **Passes:** "This helps serious vinyl collectors with 100+ records achieve investment intelligence (buy/hold/sell signals with AI reasoning) in real-time."

### 3. Competition Landscape — Critical Finding
**The gap the Scout described does NOT exist as cleanly as claimed:**

- **VinylWorth.com:** "Tracks real-time market values from Discogs, provides price alerts, and helps you manage your records." Free for up to 10 records. This is VinylIQ's core product.
- **Vizcogs.com:** "Pulls real marketplace data from Discogs to show current values, price trends, and condition-based pricing for every record." This also exists.
- **VinylSnap:** Mobile app (Google Play + App Store) for scanning and valuing records.

The "no tool currently generates per-pressing investment scores using Discogs market data" assertion in the Scout report is incorrect. VinylWorth and Vizcogs are exactly this. They are active, have freemium models, and are the actual Discogs analytics tools collectors use.

### 4. What's Still Differentiated (If Anything)
Neither VinylWorth nor Vizcogs generates an AI "investment thesis" — narrative reasoning like "This pressing is appreciating because the artist is being reissued by a boutique label, demand is outpacing supply, and the want-to-have ratio has increased 40% in 12 months. Strong buy at current $45 median." That reasoning layer appears to be absent from both tools.

The differentiation: **AI narrative investment analysis** vs. **raw price data dashboards**. VinylWorth gives you numbers. VinylIQ would explain what the numbers mean and tell you what to do.

### 5. Revenue Model Problem
VinylWorth is free for 10 records. Charging $12/month when a free competitor exists with the same data source (Discogs API) is a hard sell unless the AI reasoning layer is demonstrably valuable to collectors. The question is: do vinyl collectors think of themselves as investors enough to pay $12/month for investment intelligence?

### 6. What's Blocking 🟢
Two issues:
1. **Strong active competition** (VinylWorth + Vizcogs) reduces uniqueness and competition weakness scores below green threshold
2. **Revenue ceiling concern** — freemium competitor with same data source caps willingness-to-pay

Path to a genuine 🟢: Build the AI narrative layer as the core product (not just a dashboard). The positioning: "VinylIQ isn't a price tracker. It's a collection advisor." Weekly digest: "Your 3 most at-risk records. Your 2 best sell opportunities right now. 1 pressing in the market worth adding." If the AI reasoning is that specific and actionable, $12/month vs. VinylWorth's numbers-only dashboard becomes defensible. This pivot requires stronger product thinking before building.

### 7. Scores
| Longevity | Autonomy | Build | Marketing | Revenue | Uniqueness | Competition |
|---|---|---|---|---|---|---|
| 7 | 8 | 8 | 6 | 5 | 5 | 4 |
**Weighted total: 6.55/10**
*Verdict: 🟡 WATCH — strong competition (VinylWorth + Vizcogs) + revenue ceiling concern. Differentiate via AI narrative advisory positioning before building.*

---

## Portfolio Commentary

This week's batch surfaces a pattern worth naming: the Scout's "gap is wide open" signals are running slightly ahead of reality. Two of three new ideas (DiscRank, VinylIQ) discovered active competitors after basic search that the Scout's Reddit-sourced research didn't surface. The Scout's methodology is strongest at identifying demand signals; competition landscape requires an explicit "search for existing tools" step, not just a passive income list check.

For JT's portfolio: the already-queued build list now stands at 17 items. No new 🟢 this week is not a failure — it's honest. The highest-urgency existing queue item is TariffSwitch if rebuilt with a quality confidence score layer (currently 🟡), and PermitPilot (already queued, validated by ImmigrantIQ's 7.1 score, bigger TAM).

The DiscRank community-vote-ranking pivot is the most actionable near-term opportunity: one angle change from "AI recommendations" to "community outcome rankings" separates it clearly from TryDiscs and could score 🟢 on a resubmission.

---

## Verdict Summary

| Idea | Status | Score | Verdict | Blocking Factor |
|---|---|---|---|---|
| TariffSwitch | New | 7.2 | 🟡 WATCH | Autonomy=5 (supplier quality support burden) |
| DiscRank | New | 7.15 | 🟡 WATCH | Uniqueness=5 (TryDiscs.com exists with quiz) |
| WatchScore | 🔁 Queued | — | ALREADY ON BOARD | — |
| PermitPilot | 🔁 Queued | — | ALREADY ON BOARD | — |
| ProgramScore | 🔁 Queued | — | ALREADY ON BOARD | — |
| VinylIQ | New | 6.55 | 🟡 WATCH | Competition (VinylWorth + Vizcogs exist) |
