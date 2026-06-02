# TikTok / ReelFarm Re-entry Plan — 2026-06-01

Drive: https://docs.google.com/document/d/1y_3WwqVjMJ85bohCapJYsUEJNyXR7wklgLuQqjRCZvc/edit

## Status
JT is still warming up the TikTok accounts for Vista, Nash Satoshi, and Glow Index after recent 0-view / likely throttling behavior.

No TikTok slideshow volume should be treated as overdue while the accounts are warming. The next useful move is controlled re-entry: one manual post per account, source-tagged before posting, then 24h / 72h / 7d metric capture.

Earliest practical re-entry window: after a couple more days of warm-up this week, only when JT has done normal account activity inside TikTok and is ready to post manually.

## Operating Rule
Do not resume blind ReelFarm auto-posting.

Preferred flow:
1. ReelFarm can generate the slideshow or draft.
2. JT reviews and posts manually from TikTok.
3. Eve reconciles the live post URL / ID afterward.
4. Eve logs 24h / 72h / 7d metrics before any scale decision.

Until each account has normal distribution again, all TikTok recommendations stay capped at `Medium - hypothesis`.

## First Re-entry Tests

### Vista
- Account: existing Vista / movie TikTok account
- Experiment: Vista rating precision retest
- Source tag: `vista_tiktok_rating_precision_reentry_20260603`
- Creative type: manual TikTok / ReelFarm slideshow
- Hook direction: specific movie + exact rating-number tension
- Slide 2 proof requirement: show the 1-100 rating distinction, not just a generic app claim
- CTA: rate movies with the number you mean
- Gate: post only after warm-up; one test first, then wait for 24h / 72h metrics
- Kill/rework rule: if the post gets 0 views again, stop TikTok volume and treat account trust/posting mode as the problem before touching creative

### Nash Satoshi
- Account: `@nashsatoshi`
- Experiment: Nash model-consensus slideshow
- Source tag: `nash_tiktok_model_consensus_reentry_20260603`
- Creative type: manual TikTok / ReelFarm slideshow
- Hook direction: contradiction, model disagreement, or rare model consensus
- Slide 2 proof requirement: visible model/ranking disagreement or live ranking logic
- CTA: check the latest game-theory rankings
- Gate: only use current ranking/model data; skip if there is no live proof
- Kill/rework rule: no vague methodology explainer, no `watch this`, no token/return claims unless sourced and current

### Glow Index
- Account: Glow Index skincare/product TikTok account
- Experiment: Glow product verdict exploration
- Source tag: `glow_tiktok_product_verdict_reentry_20260603`
- Creative type: manual TikTok / ReelFarm slideshow
- Hook direction: price/value or claim-versus-formula reveal
- Slide 2 proof requirement: product/formula/value evidence, not fear or treatment claims
- CTA: compare product verdicts safely
- Gate: one conservative test only after warm-up; do not scale Glow social while crawler access and claim-safety gates remain unresolved
- Kill/rework rule: no before/after, medical, treatment, fake dermatologist, dupe, or fear framing

## Metric Capture
For each resumed post, log:
- app
- account
- posting mode
- source tag
- live post URL / ID
- hook
- proof object on slide 2
- CTA
- 24h views, likes, comments, saves, profile visits
- 72h views, likes, comments, saves, profile visits
- 7d views, likes, comments, saves, profile visits
- downstream action if visible
- decision: blocked / running / iterate / scale / kill

## Decision Rule
- 0 views again: stop. This is still an account trust or posting-mode issue.
- Low but nonzero distribution: keep frequency low and improve proof by slide 2.
- Normal distribution on 2+ accounts: resume one controlled test per account per week.
- Normal distribution across 20+ posts per account: confidence can rise above `Medium - hypothesis`.
