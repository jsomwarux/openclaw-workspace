---
name: sports-gm
description: Build and run JT's dynasty fantasy football GM-style analytics desk: market price snapshots, inefficiency candidates, roster audit frameworks, receipts tracking, @dynastyjig content, and eventual monetization experiments. Use when JT mentions sports, fantasy sports, dynasty fantasy football, dynasty GM, roster audits, market inefficiencies, @dynastyjig, KeepTradeCut, FantasyCalc, DynastyProcess, player values, or making money through sports analytics.
---

# Sports GM Skill

## Mission
Turn JT's sports instincts into a credible, monetizable dynasty fantasy football analytics system.

Primary lane: **dynasty fantasy football through a GM/front-office lens**.

Do not produce generic rankings, waiver slop, betting picks, or unsupported player takes.

## Core Rule
No public player recommendation without:
1. market price reference,
2. football/usage reference,
3. role/context reference,
4. thesis,
5. confidence tier,
6. risk case,
7. receipt row.

If exact market prices are missing, fetch them yourself. Do not ask JT to manually pull KTC/FantasyCalc/DynastyProcess unless a source is blocked.

## Source Stack
### Market / rankings
- `python3 scripts/sports_gm_fetch_prices.py`
- Primary: KeepTradeCut embedded rankings data
- Primary: FantasyCalc public API
- Primary: FantasyPros consensus dynasty rankings
- Secondary sanity check: DynastyProcess open data CSV

Critical methodology: never compare raw trade values across sources. KTC, FantasyCalc, FantasyPros, and DynastyProcess do not share a value scale. Compare overall rank, position rank, rank delta, percentile/source direction, trend, and role context. Raw values are source-local metadata only.

### Candidate detection
- `python3 scripts/sports_gm_generate_report.py`
- Candidate output: `memory/sports-gm/candidates/YYYY-MM-DD.csv`
- Report output: `memory/sports-gm/reports/weekly-gm-report-YYYY-MM-DD.md`
- Post output: `memory/content/bank/YYYY-MM-DD/dynasty-gm-automated-market-posts.md`
- Player eval output: `memory/content/bank/YYYY-MM-DD/dynasty-gm-player-evals.md`

### Framework files
- `memory/sports-gm/gm-decision-model.md`
- `memory/sports-gm/sources.md`
- `memory/sports-gm/player-thesis-template.md`
- `memory/sports-gm/roster-audit-template.md`
- `memory/sports-gm/receipts.csv`

## Workflow: Weekly Market Report
1. Run `python3 scripts/sports_gm_fetch_prices.py`.
2. Run `python3 scripts/sports_gm_generate_report.py`.
3. Read the generated report.
4. Select 3-5 research candidates, not final calls.
5. For any player-specific take, complete `player-thesis-template.md` first.
6. Add any public call to `receipts.csv`.
7. Draft @dynastyjig posts in JT's content voice.

## Workflow: Dynasty X Replies
1. Read `memory/sports-gm/dynasty-x-targets.md` before generating reply targets.
2. Use JT-approved accounts as the main universe, but sample recent content before replying. Do not rely on handle reputation alone.
3. Build a candidate pool from multiple topical searches plus the target list. Do not use only one narrow `from:` query.
4. Final reply pack must use 3 different accounts. At least 2 of 3 should be from JT's approved list.
5. Cap repeat-heavy accounts (`@DynastyDwarf`, `@DFF_Dynasty`, or any account used yesterday) to at most one combined target per day.
6. Reply only when @dynastyjig can add a sharp fantasy point: dynasty value gaps, rookie uncertainty, draft capital vs. landing spot, roster window, role, upside, risk, manager behavior, or trade process.
7. Sound like a sharp dynasty manager, not a finance model. Avoid over-scientific words like latency, liquidity, probability fragments, arbitrage, or mathematical counterpoint unless the original post uses that frame.
8. Use community-native language: price, value, rookie pick, roster spot, window, bet, role, points, upside, risk, rebuild, contender, manager.
9. Avoid pure memes, giveaways, app promos, betting slips, and generic news unless the reply adds a plain dynasty/fantasy angle.
10. Include an `Account diversity: 3/3 unique accounts` line in the final output.

## Workflow: Roster Audit
1. Ask for league format only if unavailable: 1QB/SF, scoring, teams, starters, bench, TE premium, roster, picks, manager goal.
2. Classify lifecycle: True Contender, Fragile Contender, Productive Struggle, Rebuild, Trapped Middle.
3. Map liquidity, window alignment, and positional risk.
4. Recommend exactly 3 moves.
5. State risk case.

## Voice
Sharp, plain, community-native.
Smart but not academic.
No fake certainty.
No fanboying.
No em dashes.
No generic rankings.
Avoid finance/quant jargon in replies unless the original post already uses that language.

## Monetization Ladder
1. Content + receipts.
2. Sample roster audit.
3. Beta paid roster audits.
4. Newsletter/Discord only after demand.
5. App/agent only after demand signal: 10+ engaged replies/DMs, 3+ roster audit requests, or consistent traction.

## Guardrails
- Market disagreement is a research alarm, not a buy/sell call.
- KTC/FantasyCalc/DynastyProcess values are not truth; they are price signals.
- Never publish copied paid-source analysis.
- Do not scrape behind logins or bypass access controls.
- Never post externally; JT presses send.
