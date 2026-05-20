# Nash Satoshi — Weekly Ranking Receipt Card Spec
Date: 2026-05-19
App: Nash Satoshi
Positioning: crypto ranking thesis + receipts / game theory / narrative + incentive analysis
Guardrail: no financial advice, no return claims, no price predictions

## Verdict
Build the **Weekly Ranking Receipt Card** before more generic Nash promotion. Crypto audiences already understand market-cap lists and data dashboards; the acquisition wedge is a recurring artifact that lets them argue, compare, and share a ranking thesis without framing Nash as “buy this token.”

The card should feel closer to a Messari/CoinDesk-style research receipt plus a Kaito-style mindshare/ranking artifact than a generic portfolio dashboard.

## Source Signals Used
- CoinGecko category API returned 710 categories, including major narrative/category groupings such as Smart Contract Platform, Layer 1, RWA, DeFi, Meme, Privacy. Source: `https://api.coingecko.com/api/v3/coins/categories?order=market_cap_desc`; public category page: https://www.coingecko.com/en/categories/artificial-intelligence was bot-walled during direct fetch, so API evidence is stronger than page scrape.
- DeFiLlama public API returned 7,525 protocols; top category counts included Dexs, Yield, Lending, Derivatives, Liquid Staking, RWA, Prediction Market, Gaming. Source: `https://api.llama.fi/protocols`; categories page https://defillama.com/categories was bot-walled, so page evidence is weak.
- Token Terminal positions around crypto fundamentals and onchain market coverage. Source: https://tokenterminal.com/
- Messari search result positioning: “Research, evaluate, and monitor crypto assets with analyst-verified intelligence across 40K+ assets” and “AI-powered research built on proprietary crypto data.” Source: https://messari.io/ and search result for Messari crypto research.
- CoinMarketCap Academy “Week in AI” uses weekly sector movement, standout tokens, narrative/news roundup, and category context. Source: https://coinmarketcap.com/academy/article/week-in-ai-bittensor-secures-rank-2-ai-sector-leads-market-recovery
- CoinDesk Data “Chart of the Week” emphasizes topical digital-asset developments with commentary and analysis. Source: https://data.coindesk.com/chart-of-the-week
- Bankless “Top X Accounts for Crypto AI Agent Alpha” validates AI-agent crypto discovery as an X-native behavior and points to Kaito/mindshare as a ranking primitive. Source: https://www.bankless.com/read/top-x-accounts-to-follow-for-ai-agent-updates
- Kaito search result: pre-TGE token mindshare rankings and attention leaderboard. Source: https://kaito.ai/
- Product Hunt crypto topic exists, but this is launch/backlink surface, not proof of durable crypto users. Source: https://www.producthunt.com/topics/crypto

## Card Job-To-Be-Done
Make the viewer think:
> “This is a clean receipt of how the crypto narrative shifted this week — I either agree, disagree, or want to check the methodology.”

It should create debate and curiosity, not tell people what to buy.

## Primary Audience
- Crypto X users who follow AI/token narrative accounts.
- Newsletter readers who like weekly market breakdowns.
- Analysts/builders who care about incentives, narratives, and relative positioning.
- Early users who want a shareable “why this moved” artifact.

## Core Card Format
Use a square/X-native image first, then optionally produce a 9:16 slideshow cover.

### X-Native Image
- Size: 1600×1200 or 1200×1200.
- Export: PNG.
- Visual hierarchy:
  1. Week label + category/narrative.
  2. Top movement table.
  3. Model disagreement strip.
  4. Thesis receipt notes.
  5. Methodology + disclaimer footer.

### 9:16 Slideshow Cover
- Size: 1080×1920.
- Use for TikTok/Reels/Shorts carousel, X vertical image, and Reddit image post.
- Cover hook should be one sentence, e.g. “The models disagreed hard on AI agents this week.”

## Required Data Blocks

### 1. Weekly Rank Delta
Show 5–7 tokens/projects with:
- Current Nash rank.
- Prior Nash rank.
- Delta: ↑/↓/new/flat.
- Narrative/category tag.
- One short reason.

Example row format:
`#4 → #2 | [TOKEN] | +2 | AI agents | narrative strength rose, fundamentals lagged`

### 2. Model Disagreement
Show where the multi-model system disagreed most.

Fields:
- Token/project.
- Bullish model count vs skeptical model count.
- Disagreement label: consensus / split / contested.
- Why it matters: one phrase.

Example:
`[TOKEN] — 2 bullish / 2 skeptical — contested: mindshare strong, incentive quality unclear`

### 3. Overhyped / Undervalued-by-Thesis Leaderboard
Use language carefully. Avoid “undervalued” as price prediction unless explicitly framed as “ranking thesis mismatch.” Prefer:
- “Narrative ahead of substance.”
- “Substance ahead of attention.”
- “High disagreement.”
- “Incentives unclear.”
- “Attention not yet matched by fundamentals.”

### 4. Receipt Notes
3 bullets max. Must be evidence-oriented:
- What changed.
- Which model/narrative component moved.
- What would invalidate the ranking.

### 5. Methodology Footer
Suggested copy:
> Nash Satoshi ranks crypto projects by game-theory, narrative, incentive, and model-disagreement signals. Not financial advice. No price prediction.

## Copy System

### Hook Options
Use one per card/post:
1. “The models disagreed hard on AI agents this week.”
2. “Narrative strength moved faster than fundamentals this week.”
3. “This week’s crypto ranking receipt: who moved, why, and where the models split.”
4. “The biggest Nash Satoshi ranking change was not the obvious one.”
5. “A weekly receipt for crypto thesis drift — not a price call.”

### CTA Options
- “Check the full ranking thesis.”
- “See the model disagreement behind the ranking.”
- “Argue with the ranking.”
- “Which token is the model overrating?”

Best CTA: **“Argue with the ranking.”** It fits crypto X behavior better than “try my app.”

## Design Direction
- Dark mode by default.
- Use high-contrast category tags: AI, DeFi, RWA, Gaming, Infra, Meme, Privacy.
- Avoid candlestick/trader aesthetic. It makes the product look like a trading terminal.
- Use “receipt” styling: timestamp, rank delta, evidence snippets, methodology chip.
- Include small Nash Satoshi watermark and URL/handle.

## Data/Generation Requirements
Minimum fields needed from app or pipeline:
```json
{
  "week_start": "YYYY-MM-DD",
  "week_end": "YYYY-MM-DD",
  "category": "AI Agents",
  "tokens": [
    {
      "symbol": "TOKEN",
      "name": "Project",
      "current_rank": 2,
      "prior_rank": 4,
      "rank_delta": 2,
      "category": "AI agents",
      "model_votes": {"bullish": 2, "skeptical": 2, "neutral": 0},
      "thesis_summary": "Mindshare strong, incentive durability unclear.",
      "movement_reason": "Narrative strength rose while fundamentals stayed mixed.",
      "invalidation": "Drops if developer/activity and incentive quality fail to improve."
    }
  ]
}
```

## Template Layout

### Header
`NASH SATOSHI WEEKLY RECEIPT`
`Week of [DATE] · [Narrative/category]`

### Hero Line
`Biggest disagreement: [TOKEN]`
`[bullish] bullish / [skeptical] skeptical models`

### Table
Columns:
- Rank
- Project
- Δ
- Thesis note

### Side Rail
- “Narrative leader”
- “Model split”
- “Substance ahead of attention”

### Footer
`Game theory + narrative + incentives + model disagreement`
`Not financial advice. No price predictions.`

## Distribution Package
For each weekly card, create:
1. X single post with image.
2. X thread of 3 posts: card → biggest disagreement → methodology note.
3. Reddit value-first post, no hard app pitch.
4. Newsletter/creator pitch asset: “free weekly receipt graphic you can embed/use.”
5. 9:16 carousel: cover + 3 explanation slides.

## Tracking Spine
Every post/pitch needs:
- UTM source: `x`, `reddit`, `newsletter`, `creator`, `producthunt`, `directory`.
- UTM campaign: `nash_weekly_receipt_[YYYYMMDD]`.
- Creative tag: `ranking_receipt_card`.
- Category tag: `ai_agents`, `defi`, `rwa`, etc.
- Result windows: 24h, 72h, 7d.

Example:
`https://[nash-url]/?utm_source=x&utm_medium=social&utm_campaign=nash_weekly_receipt_20260519&utm_content=ranking_receipt_card_ai_agents`

## Quality Bar
Ship only if:
- At least 5 projects/tokens included.
- Every movement has a reason.
- At least one model-disagreement insight is visible.
- No price targets, return claims, or “buy/sell” language.
- Methodology disclaimer is present.
- The card can stand alone without app context.

## First Build Recommendation
Build a static card generator first from JSON, not a full in-app export flow.

Why:
- Faster to test weekly acquisition loop.
- Lets JT/Eve iterate copy and layout before productizing.
- Can later become in-app share/export once format proves traction.

## Promoted Experiments

## Experiment: Weekly Ranking Receipt Drop

App: Nash Satoshi
Date created: 2026-05-19
Owner: Eve/JT
Decision state: planned

### Source Pattern
Source URL(s):
- https://coinmarketcap.com/academy/article/week-in-ai-bittensor-secures-rank-2-ai-sector-leads-market-recovery
- https://data.coindesk.com/chart-of-the-week
- https://tokenterminal.com/
- https://messari.io/
Observed pattern: Weekly market/sector updates package movement + context + analysis into a repeatable asset.
Proof of traction: CoinMarketCap Academy runs recurring “Week in AI”; CoinDesk has Chart of the Week; large research brands package recurring analysis because it is legible and repeatable.
Audience: Crypto X, AI-token watchers, newsletter readers.
Competitor/incumbent gap: Incumbents show market cap, price movement, or analyst prose; fewer show “model disagreement + game-theory thesis” as a shareable receipt.

### Hypothesis
If we post one weekly Nash ranking receipt card for a hot crypto narrative on X, then crypto users will click/argue/share because the card gives them a concise thesis receipt without pretending to be a price signal.

### Asset Needed
- Creative/share artifact: Weekly Ranking Receipt Card PNG.
- Copy/hook: “The models disagreed hard on [category] this week.”
- Landing/app destination: Nash ranking page or public waitlist/landing page.
- Tracking link/source tag: `utm_source=x&utm_campaign=nash_weekly_receipt_[date]&utm_content=ranking_receipt_card`.

### Distribution
Channel: X first, Reddit second, borrowed-newsletter pitches third.
Borrowed audience target, if any: 0xJeff, Bankless AI coverage, Milk Road, Coin Bureau newsletter, The Defiant.
CTA: “Argue with the ranking.”
Run date: next available Friday after card generator exists.

### Measurement
Primary metric: qualified clicks to Nash ranking page.
Secondary metric: replies/bookmarks/reposts; email/waitlist signups if available.
24h result:
72h result:
7d result:

### Decision
Scale / iterate / kill:
Reason:
Next action: Build static JSON-to-PNG generator and run first AI Agents receipt.

Score: 31/35
- Audience fit: 5
- Repeatability: 5
- Proof: 4
- Cost: 5
- Conversion intent: 4
- Shareability: 5
- Competition gap: 3

## Experiment: Model Disagreement Mini-Card

App: Nash Satoshi
Date created: 2026-05-19
Owner: Eve/JT
Decision state: planned

### Source Pattern
Source URL(s):
- https://www.bankless.com/read/top-x-accounts-to-follow-for-ai-agent-updates
- https://kaito.ai/
- https://www.bankless.com/ai-agents
Observed pattern: Crypto AI-agent discovery is X-native; ranking/mindshare artifacts are accepted primitives.
Proof of traction: Bankless explicitly frames AI-agent crypto as Twitter/X-native and highlights Kaito mindshare/ranking as signal infrastructure.
Audience: Crypto AI/token narrative watchers.
Competitor/incumbent gap: Mindshare tools show attention; Nash can show disagreement between reasoning models and incentive/narrative analysis.

### Hypothesis
If we publish a small “4 models disagreed most on…” card, then users will engage because disagreement is more debateable than a plain ranking.

### Asset Needed
- Creative/share artifact: single-token disagreement card.
- Copy/hook: “Four models split on [TOKEN]. Here’s why.”
- Landing/app destination: token detail receipt page.
- Tracking link/source tag: `utm_content=model_disagreement_card`.

### Distribution
Channel: X replies + quote posts under relevant narrative discussions.
Borrowed audience target, if any: X accounts/newsletters covering AI agents or DeFi narratives.
CTA: “See the full disagreement receipt.”
Run date: weekly, 1–2 days after main receipt card.

### Measurement
Primary metric: profile/app clicks from X.
Secondary metric: replies from analysts/builders; saves/bookmarks.
24h result:
72h result:
7d result:

### Decision
Scale / iterate / kill:
Reason:
Next action: Add model-vote field to card data schema.

Score: 30/35
- Audience fit: 5
- Repeatability: 5
- Proof: 4
- Cost: 5
- Conversion intent: 4
- Shareability: 5
- Competition gap: 2

## Experiment: Newsletter-Embeddable Receipt Graphic

App: Nash Satoshi
Date created: 2026-05-19
Owner: Eve/JT
Decision state: planned

### Source Pattern
Source URL(s):
- https://milkroad.com/
- https://coinbureau.com/
- https://blockworks.com/podcasts
- https://www.thedefiant.io/
Observed pattern: Crypto media/newsletters need recurring charts, snippets, and talking points.
Proof of traction: Milk Road, Coin Bureau, Blockworks, The Defiant all publish recurring crypto analysis/news products; Blockworks specifically has research/thesis podcasts like 0xResearch and Bell Curve.
Audience: newsletter writers, crypto media editors, podcast researchers.
Competitor/incumbent gap: Most tools pitch dashboards; Nash can offer a free weekly “ranking receipt” image with methodology and no price call.

### Hypothesis
If JT offers a free embeddable weekly ranking receipt graphic to 10 niche crypto newsletter/podcast researchers, then at least one will reply or use it because it saves them research/visual packaging work.

### Asset Needed
- Creative/share artifact: clean PNG + short methodology blurb.
- Copy/hook: “I made a weekly model-disagreement receipt for AI-agent tokens — useful as a chart/snippet?”
- Landing/app destination: public receipt archive.
- Tracking link/source tag: `utm_source=newsletter&utm_campaign=nash_receipt_embed_[date]`.

### Distribution
Channel: JT-sent email/DM outreach only; Eve drafts, JT sends.
Borrowed audience target, if any: Milk Road, Coin Bureau, The Defiant, Bankless AI Rollup, Blockworks research shows.
CTA: “Want me to send this weekly?”
Run date: after 2 public receipt examples exist.

### Measurement
Primary metric: replies/acceptances.
Secondary metric: mentions, backlinks, referral clicks.
24h result:
72h result:
7d result:

### Decision
Scale / iterate / kill:
Reason:
Next action: Create public archive page with two sample receipts before outreach.

Score: 28/35
- Audience fit: 4
- Repeatability: 4
- Proof: 4
- Cost: 5
- Conversion intent: 4
- Shareability: 4
- Competition gap: 3
