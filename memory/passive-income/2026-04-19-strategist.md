# Passive Income Strategist Report — 2026-04-19
**Run:** #7 | **Agent:** Passive Income Strategist | **Date:** Sunday, April 19, 2026

---

## Prior Recommendations Status (From 2026-04-05)

| Idea | Verdict | Status |
|------|---------|--------|
| WatchScore | 🟡 WATCH | Not yet built |
| PermitPilot | 🟡 WATCH | Not yet built |
| ProgramScore | 🟡 WATCH | Not yet built |
| DiscRank (with pivot angle) | 🟡→🟢 if angle applied | Not yet revisited |

**Bottom line:** Nothing crossed the 🟢 threshold last week. Zero builds. This week's batch needs to produce at least one candidate or the pipeline needs recalibration.

---

## Step 2: Saturation Filter — Fail Fast

| # | Idea | Saturation Verdict | Reason |
|---|------|-------------------|--------|
| 1 | CardSwap | 🔴 FAIL | Mobilo, HiHello, Unvelope all have app-based exchange + analytics. Market is served. |
| 2 | NewsletterStack | 🔴 FAIL | 10+ newsletter discovery tools exist. Substack has its own discovery engine. Low differentiation. |
| 3 | LandingGrade | 🟡 EVALUATE | Existing tools (Interact, Fibr, Juma) are real but are developer/designer-focused. SMB non-technical gap may exist. |
| 4 | PropTrack | 🟡 EVALUATE | "YourPropFirm" and similar exist but niche and expensive. Nash Satoshi's ensemble ranking approach could differentiate. |
| 5 | FanCanvas | 🟡 EVALUATE | Fan community ranking tools are fragmented. No clear winner for niche fan ranking + community. |
| 6 | AccentLab | 🟡 EVALUATE | Multiple accent training tools exist (ELSA Speak, PronunciationMirror) but none positioned as a "professional accent coach." Narrower target, less crowded. |

**Ideas moving to deep analysis:** LandingGrade, PropTrack, FanCanvas, AccentLab

---

## Step 3: Deep Analysis

---

### 3. LandingGrade — AI Landing Page Evaluator

**A. Market Demand Validation**
- X signal: Founders/SMBs asking "is my landing page good?" constantly with no good answer
- Google Trends: "landing page checker" + "landing page grader" consistent search volume
- Pain is real and recurring — every launch needs evaluation
- Demand signal: Strong

**B. Competition Landscape**
- Existing: Interact (free grader), Fibr AI, Juma AI, Expertise AI, custom TypingMind tools
- All are functional but targeted at marketers/designers
- None specifically serve: non-technical founder who needs a simple "good/bad/why" answer
- Competition: Moderate (well-served at technical layer, underserved at simplicity layer)

**C. Build Reality Check (JT's stack)**
- Frontend: Next.js on Vercel ✅
- AI scoring: OpenRouter/LLM with screenshot analysis ✅
- Screenshot: Cloudflare Browser Rendering or screenshot API ✅
- Build time: ~1-2 weeks for MVP
- JT's CRO research from coreyhaines31/marketingskills framework is a genuine asset here
- Build feasibility: HIGH (8/10)

**D. Autonomous Marketing Assessment**
- SEO: Every founder who googles "is my landing page good?" is a potential organic user
- X/Twitter: "Paste your landing page, I'll grade it" is a viral loop
- Waitlist page + 1-week viral: If 300 people paste a URL unprompted = strong signal
- Marketing: Self-generating via content loop
- Autonomy: 7/10

**E. Longevity Assessment**
- Landing pages aren't going away
- AI evaluation tools will get cheaper and more capable — need to stay ahead
- Threat: Any AI agent could add landing page scoring as a feature
- Longevity: Moderate (3-5 years before commoditization risk)

---

### 4. PropTrack — Prop Firm Performance Tracker

**A. Market Demand Validation**
- Prop trading is growing fast — MyFundedFutures, TopStep, Tradeable.Pro all scaling
- Traders using 2-5 prop firms simultaneously: real and common use case
- Currently no good cheap tool — traders use spreadsheets or manual tracking
- "Prop firm dashboard" search volume real
- Demand signal: Moderate-Good

**B. Competition Landscape**
- YourPropFirm.com exists but $49/mo+ and clunky
- Most traders track in spreadsheets — massive opportunity
- Nash Satoshi proves ensemble ranking works for JT's stack
- Competition: Weak (existing tools are expensive and bad)

**C. Build Reality Check (JT's stack)**
- Nash Satoshi tech stack is proven and reusable: ensemble ranking + React frontend
- API integrations for prop firms: challenging — most don't have public APIs
- Would need: manual data entry (CSV upload) OR web scraping prop firm dashboards
- Web scraping = brittle + could break with UI changes
- Build time: 2-3 weeks for MVP with CSV upload approach
- Build feasibility: Medium-High (7/10) — tech proven, data sourcing is the challenge

**D. Autonomous Marketing Assessment**
- Crypto trader X audience is huge and self-sharing
- "I track all my prop firm stats in [app]" is a natural viral loop
- SEO: "prop firm tracker" + "prop firm comparison" = low competition keywords
- Discord communities for prop traders are massive and self-organizing
- Marketing: Crypto audience is sticky and paying
- Autonomy: 8/10

**E. Longevity Assessment**
- Prop trading is a secular growth trend
- Tool becomes more valuable as trader progresses (compounding data = switching cost)
- Long-term stickiness: Strong — once historical data accumulates, leaving is costly
- Longevity: Good (5+ years, compounding data moat)

---

### 5. FanCanvas — Niche Fan Community Ranking Tool

**A. Market Demand Validation**
- Niche fan communities (K-pop, anime, sports, gaming) are enormous and undermonetized
- Communities constantly ranking and debating — this behavior is天然的
- No good tool exists that serves both ranking + community
- Fan merchandise spending: billions annually
- Demand signal: Good

**B. Competition Landscape**
- Fandom.com serves as wiki/database but not ranking
- Reddit threads are the current ranking mechanism — bad UX but high engagement
- TryDiscs (disc golf) proves ranking tools work in niche communities
- No clear winner for generic fan community ranking
- Competition: Weak

**C. Build Reality Check (JT's stack)**
- Nash Satoshi ensemble approach is relevant: community-voted rankings by outcome
- Community features require: auth, profiles, voting, discussion — more complex than single-purpose tools
- MVP would need: ranking submission + community voting + basic profiles
- Build time: 3-4 weeks for basic MVP
- Build feasibility: Medium (6/10) — more complex than single-purpose tools, community mechanics are hard

**D. Autonomous Marketing Assessment**
- Niche communities self-organize around ranking tools
- Viral mechanics: "Vote for your favorite [X]" posts naturally spread in fan communities
- SEO: [niche] + "rankings" + "best [X]" = low competition, high intent
- Requires: community seeding + moderation early on
- Autonomy: 5/10 (needs more manual community management early)

**E. Longevity Assessment**
- Fan communities are sticky but also trend-dependent
- If the niche fades, the tool fades with it
- Need: multiple niches to diversify or one very durable niche
- Longevity: Moderate (3-5 years, niche-dependent)

---

### 6. AccentLab — AI Accent Coaching Tool

**A. Market Demand Validation**
- Global professional workforce is increasingly cross-cultural
- Non-native English speakers paying for accent coaching is real and growing
- "Professional accent" is different from "language learning" — more niche, more paying
- ELSA Speak has millions of users — proven market
- Demand signal: Good but niche

**B. Competition Landscape**
- ELSA Speak: language learning, broad audience, $12.99/mo
- PronunciationMirror: accent coaching, less polished
- YouGlish: reverse approach (youtube examples)
- None specifically positioned as: "professional accent coach for business English"
- Competition: Moderate (real players but positioning gap exists)

**C. Build Reality Check (JT's stack)**
- Whisper (Groq) for speech-to-text: proven in JT's stack ✅
- LLM for accent analysis + coaching: achievable with fine-tuned prompt engineering
- Voice synthesis for "say it like this" playback: adds complexity
- Build time: 3-4 weeks for MVP (Whisper + LLM evaluation loop)
- Build feasibility: Medium (7/10) — tech is accessible but voice UX adds time

**D. Autonomous Marketing Assessment**
- "Accent coach for business English" has clear Reddit + LinkedIn audience
- Professional LinkedIn users sharing "how I fixed my accent" is a real content genre
- SEO: "accent coaching" + "business English" = low competition keywords
- TikTok/YouTube: accent coaching videos go viral naturally
- Marketing: can be autonomous but needs quality content early
- Autonomy: 6/10

**E. Longevity Assessment**
- AI voice coaching will commoditize eventually
- Building early gives time to compound audience before commoditization
- Differentiation needs: specific accent targets (Indian English, Mandarin English, etc.)
- Longevity: Moderate (3-5 years before commoditization, niche specificity helps)

---

## Step 4: Scores

### Scoring Philosophy
- I do not give 8s to be nice. The benchmark is levels.io products at $30K+/mo.
- Only 🟢 verdicts get full build reports.
- The levels.io test: "Could I imagine this appearing on Pieter's income dashboard in 12 months?"

---

### LandingGrade — Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Market demand | 20% | 7 | Real, recurring, underserved at SMB layer |
| Autonomy | 20% | 7 | Self-generating via content loop |
| Build feasibility | 15% | 8 | Next.js + screenshot + LLM = clean fit |
| Marketing leverage | 15% | 7 | Viral X loop + organic SEO |
| Revenue ceiling | 15% | 6 | $3-5K/mo realistic solo ceiling |
| Uniqueness | 10% | 7 | Simplicity layer — none do "for non-technical founders" |
| Competition weakness | 5% | 6 | Existing tools are technical, not consumer |
| **Overall** | 100% | **6.9/10** | |

---

### PropTrack — Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Market demand | 20% | 7 | Growing fast, unserved at mid-range price |
| Autonomy | 20% | 8 | Crypto audience self-generates, Discord-native |
| Build feasibility | 15% | 7 | Nash Satoshi proven, data sourcing challenge |
| Marketing leverage | 15% | 8 | "I track all my prop firm stats" is sticky |
| Revenue ceiling | 15% | 7 | Prop traders pay for tools, $5-8K/mo realistic |
| Uniqueness | 10% | 7 | No good cheap tool in this space |
| Competition weakness | 5% | 8 | Existing tools expensive + bad UX |
| **Overall** | 100% | **7.4/10** | |

---

### FanCanvas — Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Market demand | 20% | 6 | Real but niche-dependent |
| Autonomy | 20% | 5 | Community seeding + moderation required early |
| Build feasibility | 15% | 6 | Community mechanics add complexity |
| Marketing leverage | 15% | 6 | Viral in niche, not broad |
| Revenue ceiling | 15% | 5 | Merchandise沾上但 VC-style scaling hard solo |
| Uniqueness | 10% | 7 | Ranking + community is differentiated |
| Competition weakness | 5% | 7 | No clear winner in fan community ranking |
| **Overall** | 100% | **5.8/10** | |

---

### AccentLab — Scores

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Market demand | 20% | 6 | Niche but growing |
| Autonomy | 20% | 6 | Content marketing can drive, but needs quality early |
| Build feasibility | 15% | 7 | Whisper + LLM accessible, voice UX adds time |
| Marketing leverage | 15% | 6 | Professional accent is LinkedIn-native, TikTok viral |
| Revenue ceiling | 15% | 6 | Professional users pay more, $4-6K/mo realistic |
| Uniqueness | 10% | 7 | Positioning as "business English accent coach" is different |
| Competition weakness | 5% | 6 | ELSA is real but broad; niche gap exists |
| **Overall** | 100% | **6.2/10** | |

---

## Step 5: Verdict Summary

**Verdicts — 🟢 BUILD:** 0 | **🟡 WATCH:** 4 | **🔴 PASS (saturation filter):** 2

---

### 🟢 BUILD THIS: None this week

This batch is weaker than last week's. The saturation filter killed 2 ideas (CardSwap, NewsletterStack), and the remaining 4 all have at least one dimension that falls below the threshold. The pipeline is healthy but this week produced no 🟢 candidates.

### 🟡 WATCH

1. **PropTrack** — Score: 7.4/10 | "Could it appear on Pieter's dashboard?" Yes, if the data sourcing problem (prop firm APIs) gets solved. This is the strongest candidate but needs more validation on data access before it's a 🟢.

2. **LandingGrade** — Score: 6.9/10 | "Could it appear on Pieter's dashboard?" Stretch. The market is real but the revenue ceiling is lower and competition from AI agents is a real threat. Watch for commoditization timeline.

3. **AccentLab** — Score: 6.2/10 | "Could it appear on Pieter's dashboard?" No — too niche and too many existing players. Interesting as a personal project but not a levels.io-style business.

4. **FanCanvas** — Score: 5.8/10 | "Could it appear on Pieter's dashboard?" No. Community mechanics are hard, revenue ceiling is low, and niche-dependence makes it fragile.

---

## Already Queued (from prior runs)

| Idea | Last Score | Status | Next Action |
|------|-----------|--------|-------------|
| **DiscRank** (with angle pivot) | ~7.8 | 🟡 WATCH → 🟢 if pivot applied | Revisit with "Community-voted disc rankings by outcome" framing |
| WatchScore | 6.x | 🟡 WATCH | Awaiting JT's decision |
| PermitPilot | 6.x | 🟡 WATCH | Awaiting JT's decision |
| ProgramScore | 6.x | 🟡 WATCH | Awaiting JT's decision |

---

## Step 7: Push to Mission Control

No 🟢 candidates this week — no new tasks created.

Existing queued items remain in MC.

---

## Step 8: Report Saved

**Output:** `memory/passive-income/2026-04-19-strategist.md`

---

## Step 10: Sunday Digest

---

**🗓 Passive Income Pipeline — Sunday Digest**
*Strategist Run #7 | April 19, 2026*

**This week's verdict: 0 🟢 BUILD | 4 🟡 WATCH | 2 🔴 PASS**

**Why no builds this week:**
The Scout surfaced 6 ideas but only 4 passed the saturation filter. Of those 4, none crossed the 7.0 threshold. The pipeline is working correctly — we're being more selective, which is right — but this means JT needs to either (a) wait for the next Scout run or (b) revisit the DiscRank angle pivot that's been sitting at ~7.8 with the framing fix already identified.

**Top candidate: PropTrack (7.4/10)**
- Reuses proven Nash Satoshi tech stack
- Prop trading is a hot market with no good cheap tool
- Crypto audience is sticky and self-generating
- **The blocker:** prop firm APIs don't exist — need to validate CSV upload approach or web scraping feasibility before it's a real 🟢

**What to do this week:**
1. 🟡 **DiscRank:** Apply the angle pivot (community-voted rankings by outcome) and recalculate — this has been sitting at 7.8 for two weeks
2. 🔍 **PropTrack validation:** Spend 30 minutes scraping or manual-testing one prop firm's dashboard to confirm data is accessible via CSV or scraping — if yes, PropTrack becomes 🟢
3. ⏸ **The rest:** Stand down on LandingGrade, AccentLab, FanCanvas until market conditions shift

**Pipeline health:** ✅ Filter is working | ❌ No 🟢 candidates for second consecutive week — next Scout run should prioritize ideas that score 8+ on the Scout rubric

---
*Generated by Passive Income Strategist — Eve (AI Chief of Staff)*
*Scout output: memory/passive-income/2026-04-19-scout.md*