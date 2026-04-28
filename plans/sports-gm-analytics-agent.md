# Sports GM Analytics System — Build Plan

Date: 2026-04-27
Owner: Eve + JT
Status: awaiting JT approval before implementation

## Objective
Build a credible fantasy/dynasty football analytics system that turns JT's natural GM instincts into:
1. differentiated public content,
2. a receipts-backed decision model,
3. a paid roster-audit offer,
4. eventually a sports analytics agent/product if demand appears.

This should not become generic fantasy content. The lane is: **dynasty fantasy football through a GM/front-office lens: market pricing, roster lifecycle, asset liquidity, and decision process.**

## Strategic Constraint
Do not overbuild a SaaS/app before proof of demand. Existing future-signal says the fantasy sports agent/app is deferred until job/consulting runway improves or demand is validated. So Phase 1 is lightweight: manual/agent-assisted research, content, receipts, and paid audit beta.

## Trust Standard
No advice should be framed as certainty. Every claim gets a confidence tier and reference trail.

A recommendation is publishable only if it has:
- Market price reference
- Football/usage reference
- Context reference
- Thesis
- Confidence tier
- Risk case
- Receipt tracking row

## Core Data Sources

### Market Price Sources
Use these to estimate what dynasty managers currently believe:
- KeepTradeCut values and trend movement
- FantasyCalc trade database / trade calculator
- DynastyProcess trade calculator
- Dynasty Data Lab ADP / rookie ADP where available
- Sleeper ADP, roster/trade activity where available
- DLF / startup ADP where accessible
- X/Reddit sentiment as soft retail sentiment, not truth

### Player/Team Signal Sources
Use these to estimate probable future value:
- PlayerProfiler: athletic profile, dominator, breakout age, production profile
- PFF: grades, route data if accessible, receiving/rushing context
- FantasyPoints Data / FTN / Establish The Run style usage concepts where accessible
- Reception Perception for WR route/coverage-level skill where accessible
- NFL Next Gen Stats
- Pro Football Reference / Stathead
- Team depth charts, contracts, draft capital, coaching/offensive environment
- Vegas/team implied totals and player props as market-implied expectations

### Historical/Framework Sources
Use these to avoid fake precision:
- Age curves by position
- Draft capital hit rates
- Rookie pick hit rates by range
- Positional replacement value / WAR-style thinking
- Start-rate and lineup size effects
- Superflex vs 1QB and TE premium scarcity adjustments
- Historical ADP/value movement after injuries, depth-chart shifts, rookie hype, and playoff production

## Definition: Market Inefficiency
A dynasty market inefficiency is not just a take. It is a measurable gap between:

**Market price** = how the crowd values an asset now

and

**Probable future value** = what the asset is likely to be worth over the relevant dynasty window based on usage, talent profile, role, age, team context, liquidity, and historical comps.

Inefficiency types:
1. Recency overreaction — short-term production swings move price more than role/talent changed.
2. Narrative lag — role/usage improved before price caught up.
3. Liquidity discount — useful production is cheap because the asset is unfashionable.
4. Fragility premium — market overpays for profile with weak role security.
5. Format mispricing — player is priced generically, but league format changes value.
6. Window mismatch — player is good, but wrong for a specific team's lifecycle.
7. Pick arbitrage — market misprices pick packages, tier breaks, or timing.

## Confidence Framework

### Low Confidence
- One source suggests mispricing.
- Thesis is plausible but not triangulated.
- Publishable as a question or watchlist, not a buy/sell call.

### Medium Confidence
- 2-3 independent signals agree.
- Example: KTC price is low, trade data confirms, usage trend supports, and team context is stable.
- Publishable as a call with caveats.

### High Confidence
- Market price disagrees with history + usage + multiple market sources.
- Has clear catalyst/timing.
- Risk case is known and bounded.
- Publishable as a strong stance and eligible for paid-audit recommendation.

## GM Decision Model
Every player/asset receives seven scores, 1-10:

1. Price Score — is the market cheap, fair, or expensive?
2. Production Signal — current/future scoring ability.
3. Usage Quality — routes, targets, snaps, carries, high-value touches, QB/offense quality.
4. Role Security — contract, draft capital, team investment, depth chart, coaching stability.
5. Age/Window Fit — where the asset sits on the dynasty curve.
6. Liquidity — how easy the asset is to trade later.
7. Catalyst — what could cause value movement and when?

Output labels:
- Buy
- Hold
- Sell
- Avoid
- Contender Buy
- Rebuild Buy
- Liquidity Flip
- Watchlist

## Roster Construction Framework

### Team Lifecycle Classes
1. True Contender — top-tier weekly ceiling + depth; should consolidate for points.
2. Fragile Contender — good starters but weak depth/injury insulation; should buy depth/liquidity.
3. Productive Struggle — intentionally young, high-upside, low current points.
4. Rebuild — weak points, should maximize liquid future value.
5. Trapped Middle — too good for elite picks, too weak to win; needs direction.

### Roster Audit Dimensions
- Starting lineup strength vs league
- Bench insulation
- Age curve exposure
- Positional scarcity exposure
- Pick inventory
- Asset liquidity
- Window alignment
- Consolidation opportunities
- Fragility risks
- Trade market opportunities

### Advice Rule
No roster advice without league format:
- Superflex or 1QB
- PPR/scoring
- TE premium or not
- lineup size
- bench size
- number of teams
- contender/rebuild preference
- trade deadline/playoff structure

## Content System

### Account Positioning
`@dynastyjig`: Dynasty fantasy football for people who think like GMs, not box score chasers.

### Content Pillars
1. Market Inefficiency Reports
2. Roster Construction Economics
3. Draft Capital Arbitrage
4. Player Value Receipts
5. Trade/Roster Audit Teardowns
6. Builder Narrative: turning GM instincts into a decision system

### Post Formats
- One sharp standalone take
- Data-backed mini-thread
- Buy/sell thesis card
- Roster construction principle
- Public receipt update
- Trade teardown
- Player price vs role mismatch

### Voice
Analytical, compressed, clinical. No fanboying. No generic rankings. No fake certainty.

## Receipts System
Create `memory/sports-gm/receipts.csv` with columns:
- date
- sport
- format
- player_or_asset
- call_type
- market_price_source
- market_price_at_call
- thesis
- confidence
- risk_case
- time_horizon
- review_date_3m
- review_date_6m
- review_date_12m
- outcome_3m
- outcome_6m
- outcome_12m
- process_grade
- notes

## Paid Offer MVP
Start manually after 2-3 weeks of content proof.

Offer: **Dynasty GM Roster Audit**
- Beta price: $25-$49
- Deliverable: 1-page audit
- Sections:
  1. Team lifecycle classification
  2. Window diagnosis
  3. Asset liquidity map
  4. Three recommended moves
  5. Buy/sell/watchlist targets
  6. Risk warning

Trust builder: include sample audit using JT's own team or a synthetic roster.

## Agent Architecture — staged

### Phase 1: Manual/Light Agent Desk
- Weekly research file
- Manual data pulls from public sources
- Generated content with citations
- Receipts CSV
- No scraping gray-area or paid-source copying

### Phase 2: Sports GM Research Agent
Inputs:
- player list
- market value snapshots
- ADP/trade data
- usage metrics
- JT qualitative notes

Outputs:
- weekly inefficiency report
- content drafts
- roster audit draft
- receipts updates

### Phase 3: Product/App Candidate
Only if demand appears:
- Dynasty Window Calculator
- Trade Leverage Finder
- Roster Liquidity Map
- Market Inefficiency Tracker

## Implementation Tasks After Approval
1. Create `memory/sports-gm/receipts.csv`.
2. Create `memory/sports-gm/player-thesis-template.md`.
3. Create `memory/sports-gm/roster-audit-template.md`.
4. Create `memory/sports-gm/weekly-gm-report-template.md`.
5. Create first weekly GM report for 2026-04-27.
6. Generate first 10 `@dynastyjig` posts from the framework.
7. Create Mission Control project/tasks for the 30-day sprint.
8. Optional: build a lightweight `sports-gm` skill after the first report proves useful.

## Approval Gate
Before implementation, JT should approve:
- Primary sport: dynasty fantasy football first? presumed yes.
- Account: `@dynastyjig`? presumed yes.
- Initial scope: content + receipts + roster audit template, not full app? recommended yes.
