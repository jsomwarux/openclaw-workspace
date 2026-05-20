# App Marketing OS — Self-Improvement Rules

Created: 2026-05-13
Owner: Eve

## Purpose
Prevent App Marketing OS from becoming a stale task/content generator. The system should autonomously decide what to continue, kill, rework, or measure before creating more work.

## Weekly Review Inputs
Every weekly App Marketing review must read, in this order:
1. `memory/app-marketing/app-registry.md`
2. `memory/app-marketing/weekly-scoreboard.md`
3. `memory/app-marketing/experiment-calendar.md`
4. `memory/app-marketing/generated-mission-control-tasks.json`
5. `memory/app-marketing/winning-pattern-research-protocol.md`
6. `memory/app-marketing/share-artifact-roadmap.md`
7. `memory/app-marketing/borrowed-audience-playbook.md`
8. `memory/app-marketing/competitor-mining-protocol.md`
9. `memory/app-marketing/measurement-spine.md`
10. `memory/app-marketing/durable-discovery-plan.md`
6. `memory/app-marketing/directory-submissions.md`
7. `memory/app-marketing/seo-backlog.md`
8. `memory/app-marketing/aso-checklist.md`
9. relevant ReelFarm/current app status files under `memory/reelfarm/`
10. relevant app-specific metrics sources once configured

## Decision States
For every app/channel/experiment, output exactly one:
- `CONTINUE` — evidence supports another test.
- `DOUBLE_DOWN` — evidence materially beat baseline and tracking is reliable.
- `REWORK` — signal exists but hook/asset/target was weak.
- `MEASURE_FIRST` — output exists but metrics are missing or unreliable.
- `PAUSE` — channel lacks current asset, metric source, or strategic fit.
- `KILL` — repeated underperformance, unsafe positioning, or no path to measurement.

## Continue / Double-Down Rules
Only mark `DOUBLE_DOWN` when all are true:
1. Metric source is reliable enough for that channel.
2. Result beats baseline by at least 1.5x, OR crosses the experiment threshold in `experiment-calendar.md`.
3. The hook/format is safe for the app's positioning.
4. The next action is concrete and not just “post more.”

`CONTINUE` is allowed when the first test was clean but not conclusive.

## Rework Rules
Use `REWORK` when:
- Hook was directionally right but too vague.
- Asset quality limited the result.
- Channel fit was right but CTA/format was wrong.
- Reddit/community risk was high but topic was useful.

Rework output must name the exact change: hook, asset, platform, CTA, audience, timing, or proof source.

## Measure-First Rules
Use `MEASURE_FIRST` when:
- Metrics are missing for 2 consecutive weeks.
- Planned posts have not reconciled to live post IDs.
- App Store/web/ReelFarm metrics are not available.
- The system cannot distinguish “bad content” from “no distribution/measurement.”

Hard rule: do not increase posting volume while in `MEASURE_FIRST`.

## Pause / Kill Rules
Use `PAUSE` when:
- The app lacks a landing page/waitlist but marketing would need one.
- The channel is blocked by missing screenshots/assets/account setup.
- The app has strategic priority but no measurement path yet.

Use `KILL` when:
- A format underperforms 3 clean tests.
- A channel creates safety/reputation risk.
- An experiment cannot be measured and does not create durable discovery.
- A task would serve vanity activity rather than users/traffic/signups.

## App-Specific Guardrails

### Vista
- Primary evidence: App Store downloads, rating/reviews, TikTok/ReelFarm views/saves/comments, directory/backlink status.
- Good experiments: rating precision, movie taste identity, private/personal tracking, App Store/ASO improvements.
- Avoid: generic “Letterboxd killer,” relationship-compatibility hooks unless real proof supports them.

### Nash Satoshi
- Primary evidence: ranking-page visits, X engagement, TikTok/ReelFarm engagement, methodology-page visits.
- Good experiments: live rankings, model disagreement, methodology proof, token-specific game-theory analysis.
- Avoid: return claims, price predictions, generic crypto engagement bait, vague “watch this.”

### Glow Index
- Primary evidence: crawlability, site visits, search impressions/clicks, product/category page health, safe directory status.
- Good experiments: product/category GEO, safe ingredient/value education, comparison pages only when data supports uniqueness.
- Avoid: medical/dermatology claims, diagnosis/treatment language, fake testimonials, fake before/after, acne/eczema/rosacea claims unless safely framed and data-supported.

### Action Arena
- Primary evidence: @dynastyjig engagement/replies, beta interest, waitlist signups once live.
- Good experiments: fake-money league strategy, bankroll/card construction, fantasy + sports betting competition mechanics.
- Avoid: real-money wagering claims, gambling promises, conflation with Dynasty Fantasy Football Simulator.

## Mission Control Task Rules
When generating tasks:
1. De-dupe against active MC title and slug.
2. Every task must include: first action, why it matters, done state, references, owner, priority, guardrail.
3. JT-owned tasks only when a human account/UI approval/manual submission is required.
4. Eve-owned tasks when file work, research, analysis, or scripting can proceed autonomously.
5. Do not create external-send/submission tasks as Eve-owned unless JT has explicitly approved that external action.
6. If an app/channel is `MEASURE_FIRST`, generated tasks must fix measurement, not generate more content volume.

## Weekly Output Contract
Each weekly App Marketing review must include:
1. One-line executive read.
2. App-by-app decision state.
3. Tasks created/updated/skipped by generator.
4. What changed from last week.
5. What Eve can do without JT.
6. What JT must provide or approve.
7. Kill/pause decisions with reasoning.

## Required Command
After weekly metrics/experiment refresh, run:

```bash
python3 scripts/app_marketing_task_generator.py --execute
```

Then inspect:

```bash
cat memory/app-marketing/generated-mission-control-tasks.json
```

If errors occur, fix the generator or Mission Control API before claiming the weekly review is complete.


## Experiment Promotion Rules
A marketing insight cannot become a Mission Control task unless it has an experiment card or is a clear infrastructure fix. Pattern score must be 24+/35 using `winning-pattern-research-protocol.md`, unless the task fixes measurement, crawlability, or product-share infrastructure.

## Share Artifact Rule
Before scaling rented-channel posting for any consumer app, confirm whether that app has a product-led share artifact. If missing, create a product/spec task before creating more content-volume tasks.

## Borrowed Audience Rule
Each active app must maintain at least 20 researched borrowed-audience targets before declaring its distribution strategy mature. External outreach remains JT-owned; Eve drafts and tracks only.
