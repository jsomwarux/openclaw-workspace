# App Marketing OS — Weekly Scoreboard

## Purpose
One weekly view of whether each app's marketing is producing attention, learning, and users.

## 2026-06-18 Portfolio Decision Model
Opus strategy reset overrides the older Vista-first allocation below until a new decision memo changes it.

Portfolio posture:
- **Consulting first:** app work cannot outrank Yair/Altmark, Petri/HPM/Superior follow-ups, or proof assets.
- **Action Arena:** gate sprint only. Diagnose and clear App Store submission by 2026-07-15, build the 20-commissioner list, then park until football season.
- **Glow Index:** only ongoing app bet. SEO/GEO money pages, methodology trust anchor, indexing/impression trend, affiliate/email conversion.
- **Nash Satoshi:** capped. One human-reviewed research receipt/week, measured by methodology-page clicks and waitlist signups.
- **Vista:** paused. Monitor existing SEO/App Store data only; no ReelFarm scaling, taste-card build sprint, or directory push until an explicit un-pause trigger.
- **Paid UGC creators:** paused for all apps except a future capped Action Arena kickoff test. The Action Arena test requires app live, attribution ready, loop instrumented, fixed small budget, and 2-3 creators before any scale.

Weekly output requirement for the reset:
- `GATE_ACTION_ARENA`: EAS/TestFlight/App Store state and next submission action are known, or the app is submitted.
- `PUSH_GLOW_SEO`: next Glow money pages are chosen from intent/winnability/affiliate fit and tracked for indexing.
- `CAP_NASH`: one receipt max, research-only, with click/signup measurement.
- `HOLD_VISTA`: no new work unless share-to-install proof or $10K/month consulting trigger exists.

Do not recommend Product Hunt, broad directory pushes, daily Nash drafts, Vista taste-card implementation, TikTok/ReelFarm scaling, or new app features until the scoreboard shows a measured loop.

Do not recommend paid creators for Nash under any condition. Do not recommend Glow creators until compliance scripts, analytics, and crawler/indexing are healthy.


## Measurement Spine Gate — added 2026-05-24
Before recommending more content volume or marking an experiment as ready, confirm the related `post-registry.jsonl` row includes:
- experiment_name
- source_tag or UTM
- creative_type
- target_audience
- CTA
- 24h / 72h / 7d metric fields, even if still null
- downstream_metric
- attribution_confidence
- decision

Weekly review rule: if a promoted post lacks these fields, classify the next action as **fix tracking first**, not **ship more content**.

## Weekly Review Template

```md
# App Marketing Scoreboard — Week of YYYY-MM-DD

## Executive Read
- Best-performing app/channel:
- Weakest app/channel:
- One thing to double down on:
- One thing to stop/reduce:
- One durable discovery action completed:
- One blocker needing JT:

## Vista
Stage: active
Primary goal this week:

### Output
- TikTok/ReelFarm posts:
- X posts queued/posted:
- Reddit drafts/posted:
- SEO/directory/ASO actions:

### Metrics
- TikTok views:
- TikTok saves:
- TikTok comments:
- App Store downloads:
- App Store rating/reviews:
- Site/landing visits:

### Learning
- Winning hook/format:
- Losing hook/format:
- Next test:

## Nash Satoshi
[repeat same structure]

## Glow Index
[repeat when active]

## Action Arena
Stage: prelaunch
Primary goal this week:

### Output
- @dynastyjig posts:
- Reply targets/replies:
- Waitlist/page actions:
- SEO/directory actions:
- UGC test status: locked until app live + attribution ready + kickoff timing

### Metrics
- @dynastyjig impressions/engagement:
- Replies/comments:
- Waitlist signups:
- Beta interest:
- Per-creator attributable installs, if unlocked:
- Creator-to-league creation rate, if unlocked:

### Learning
- Winning sports/betting angle:
- Losing angle:
- Next test:

## Dynasty Fantasy Football Simulator
[repeat when active/prelaunch]
```

## Data Requirements
Minimum viable scoreboard can start with manual metrics. Automation comes second.

Required weekly inputs:
- ReelFarm/TikTok: views, likes, comments, saves from JT's laptop/ReelFarm output if available.
- X: impressions, likes, reposts, replies, profile clicks if available.
- Reddit: subreddit, upvotes, comments, removal status, promo risk notes.
- Web/App: visits, signups, downloads, App Store metrics where available.

## Decision Rules
- Double down when a hook/format materially beats the app's baseline.
- Retire when a format underperforms 3 times or gets removed/flagged by community norms.
- Do not increase posting volume until metrics are captured reliably.
- If data is missing for 2 consecutive weeks, fix the metrics handoff before recommending more content volume.

## Weekly App Signal Review — updated 2026-06-18

Purpose: choose a small weekly app-marketing queue from measured signals, not equal-volume content across every app.

### Portfolio Allocation Rule
- Consulting work outranks app marketing.
- Action Arena: gate sprint only until Apple Developer Organization transfer, EAS secrets, and App Store/TestFlight path are clear.
- Glow Index: only ongoing compounding app bet, but current action is measurement and GA4 source-tag setup, not another Replit rebuild.
- Nash Satoshi: one human-reviewed receipt/week max.
- Vista: paused; monitor only unless a later written decision memo unpauses it.
- Dynasty Simulator: validation-first only; no launch/content expansion unless a concrete validation plan exists.
- Paid creators: locked except a future capped Action Arena kickoff test after app-live + attribution gates.

### Required Review Inputs
Each weekly review must check:
- winning format from the prior week;
- losing format from the prior week;
- source tag / UTM coverage;
- 24h, 72h, and 7d metric windows;
- downstream metric: App Store click/download, site visit, signup, reply, save, export, or qualified comment;
- attribution confidence: high / medium / low;
- scale / iterate / kill decision.

### Queue Selection Template

```md
## Next App Marketing Queue

| Slot | App | Work type | Source tag / tracking | Owner | CTA / done state | Metric window | Decision rule |
|---:|---|---|---|---|---|---|---|
| 1 | Glow | Measurement setup | source_tag custom dimension | Eve/JT | GA4 source_tag queryable | 24h / 72h / 7d | fix / measure / defer build |
| 2 | Glow | SEO/GEO measurement | glow_seo_product_analysis_20260618 + glow_seo_rankings_index_20260618 | Eve | baseline + 72h/7d checks | 72h / 7d | build next batch only if signal appears |
| 3 | Action Arena | Submission gate | App Store/TestFlight state | JT/Eve | org transfer then EAS/App Store path clear | weekly until 2026-07-15 | submit / fix / pause |
| 4 | Nash | Weekly receipt | nash_newsletter_receipt_[name]_YYYYMMDD | Eve/JT | one reviewed receipt only | 7d / 30d | keep weekly / cap monthly |
| 5 | Vista | Monitor only | App Store/web baseline | Eve | no new build/content unless trigger | weekly | hold / unpause by written memo only |
```

### Kill / Hold Rules
- If a post idea has no source tag, hold it.
- If the matching app has no metric path, hold it.
- If Glow's crawler access is blocked, source-tag reporting is broken, or claim-safety is unclear, replace page building with measurement/setup.
- If Vista assets are missing, do nothing; Vista is paused unless an explicit un-pause trigger exists.
- If Nash language implies returns, price prediction, or financial advice, kill the slot.

### Weekly Output Requirement
Every weekly review ends with exactly one of these:
- `SHIP_QUEUE`: 5-7 posts have owner, source tag, CTA, and metric windows.
- `FIX_TRACKING_FIRST`: tracking is too weak to justify more posts.
- `BUILD_ASSET_FIRST`: the best post needs a visual/card/page before distribution.
- `SEO_FIRST`: app should get page work instead of social volume this week.
- `MEASURE_FIRST`: live work shipped and the next move is source-tag/reporting/indexing measurement before more build or content volume.

<!-- METRICS_SUMMARY_START -->
## Metrics Summary — Week of 2026-06-16

### vista / tiktok
- Posts/results logged: 1
- Views/impressions: 145
- Best item: Rating every film I watched this year on VISTA (145 views/impressions)

**Best overall:** vista / tiktok — Rating every film I watched this year on VISTA (145 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-15

### glow-index / tiktok
- Posts/results logged: 1
- Views/impressions: 262
- Engagement: likes 2, comments 0, saves 0, reposts 0
- Best item: The Ordinary, ranked best to worst by 4 AIs. Some picks will surprise you. (262 views/impressions)

**Best overall:** glow-index / tiktok — The Ordinary, ranked best to worst by 4 AIs. Some picks will surprise you. (262 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-13

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-06-13 to 2026-06-19 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 2
- Web depth: active users 2, pageviews 15, events 24
- Best item: glow-index GA4 web traffic 2026-06-13 to 2026-06-19 (2 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-13 to 2026-06-19 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 42
- Web depth: active users 10, pageviews 122, events 369
- Best item: nash-satoshi GA4 web traffic 2026-06-13 to 2026-06-19 (42 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-13 to 2026-06-19 (42 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-12

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-06-12 to 2026-06-18 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 2
- Web depth: active users 2, pageviews 8, events 12
- Best item: glow-index GA4 web traffic 2026-06-12 to 2026-06-18 (2 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-12 to 2026-06-18 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 47
- Web depth: active users 12, pageviews 124, events 385
- Best item: nash-satoshi GA4 web traffic 2026-06-12 to 2026-06-18 (47 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-12 to 2026-06-18 (47 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-11

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-06-11 to 2026-06-17 (1 views/impressions)

### glow-index / tiktok
- Posts/results logged: 1
- Views/impressions: 492
- Engagement: likes 3, comments 0, saves 0, reposts 0
- Best item: 4 AIs flagged the ingredient in your clean skincare that's actually irritating (492 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-06-11 to 2026-06-17 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-11 to 2026-06-17 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 37
- Web depth: active users 11, pageviews 118, events 381
- Best item: nash-satoshi GA4 web traffic 2026-06-11 to 2026-06-17 (37 views/impressions)

**Best overall:** glow-index / tiktok — 4 AIs flagged the ingredient in your clean skincare that's actually irritating (492 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-10

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 40
- Best item: Mastercard using crypto to securely verify AI identity on the front end and to settle transactions on the back end through stablecoins. 

The intersection of AI and crypto is going (40 views/impressions)

**Best overall:** nash-satoshi / x — Mastercard using crypto to securely verify AI identity on the front end and to settle transactions on the back end through stablecoins. 

The intersection of AI and crypto is going (40 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-09

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-06-09 to 2026-06-15 (1 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 1
- Web depth: active users 0, pageviews 1, events 2
- Best item: glow-index GA4 web traffic 2026-06-09 to 2026-06-15 (1 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-09 to 2026-06-15 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 37
- Web depth: active users 9, pageviews 121, events 384
- Best item: nash-satoshi GA4 web traffic 2026-06-09 to 2026-06-15 (37 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-09 to 2026-06-15 (37 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-08

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-06-08 to 2026-06-14 (1 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 1
- Web depth: active users 0, pageviews 1, events 2
- Best item: glow-index GA4 web traffic 2026-06-08 to 2026-06-14 (1 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-08 to 2026-06-14 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 46
- Web depth: active users 10, pageviews 195, events 515
- Best item: nash-satoshi GA4 web traffic 2026-06-08 to 2026-06-14 (46 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-08 to 2026-06-14 (46 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-07

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-06-07 to 2026-06-13 (1 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 1
- Web depth: active users 0, pageviews 1, events 2
- Best item: glow-index GA4 web traffic 2026-06-07 to 2026-06-13 (1 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-07 to 2026-06-13 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 46
- Web depth: active users 10, pageviews 195, events 516
- Best item: nash-satoshi GA4 web traffic 2026-06-07 to 2026-06-13 (46 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-07 to 2026-06-13 (46 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-06

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-06-06 to 2026-06-12 (1 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 1
- Web depth: active users 0, pageviews 1, events 2
- Best item: glow-index GA4 web traffic 2026-06-06 to 2026-06-12 (1 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-06 to 2026-06-12 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 43
- Web depth: active users 9, pageviews 192, events 506
- Best item: nash-satoshi GA4 web traffic 2026-06-06 to 2026-06-12 (43 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-06 to 2026-06-12 (43 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-05

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-06-05 to 2026-06-11 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 1
- Web depth: active users 0, pageviews 1, events 2
- Best item: glow-index GA4 web traffic 2026-06-05 to 2026-06-11 (1 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-05 to 2026-06-11 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 38
- Web depth: active users 9, pageviews 179, events 464
- Best item: nash-satoshi GA4 web traffic 2026-06-05 to 2026-06-11 (38 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-05 to 2026-06-11 (38 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-04

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-06-04 to 2026-06-10 (1 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 1
- Web depth: active users 0, pageviews 1, events 2
- Best item: glow-index GA4 web traffic 2026-06-04 to 2026-06-10 (1 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-04 to 2026-06-10 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 37
- Web depth: active users 10, pageviews 164, events 401
- Best item: nash-satoshi GA4 web traffic 2026-06-04 to 2026-06-10 (37 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-04 to 2026-06-10 (37 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-06-01

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 3
- Best item: glow-index Search Console queries 2026-06-01 to 2026-06-07 (3 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-06-01 to 2026-06-07 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-06-01 to 2026-06-07 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 11
- Web depth: active users 7, pageviews 15, events 60
- Best item: nash-satoshi GA4 web traffic 2026-06-01 to 2026-06-07 (11 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-06-01 to 2026-06-07 (11 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-31

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-31 to 2026-06-06 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-05-31 to 2026-06-06 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-31 to 2026-06-06 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 11
- Web depth: active users 8, pageviews 18, events 78
- Best item: nash-satoshi GA4 web traffic 2026-05-31 to 2026-06-06 (11 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-31 to 2026-06-06 (11 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-30

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-30 to 2026-06-05 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-05-30 to 2026-06-05 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-30 to 2026-06-05 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 14
- Web depth: active users 9, pageviews 23, events 92
- Best item: nash-satoshi GA4 web traffic 2026-05-30 to 2026-06-05 (14 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-30 to 2026-06-05 (14 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-29

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-29 to 2026-06-04 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-05-29 to 2026-06-04 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-29 to 2026-06-04 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 15
- Web depth: active users 9, pageviews 22, events 86
- Best item: nash-satoshi GA4 web traffic 2026-05-29 to 2026-06-04 (15 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-29 to 2026-06-04 (15 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-28

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-28 to 2026-06-03 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-05-28 to 2026-06-03 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-28 to 2026-06-03 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 18
- Web depth: active users 8, pageviews 26, events 101
- Best item: nash-satoshi GA4 web traffic 2026-05-28 to 2026-06-03 (18 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-28 to 2026-06-03 (18 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-27

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-27 to 2026-06-02 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 2
- Web depth: active users 2, pageviews 5, events 9
- Best item: glow-index GA4 web traffic 2026-05-27 to 2026-06-02 (2 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-27 to 2026-06-02 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 24
- Web depth: active users 7, pageviews 39, events 131
- Best item: nash-satoshi GA4 web traffic 2026-05-27 to 2026-06-02 (24 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-27 to 2026-06-02 (24 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-26

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-26 to 2026-06-01 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 2
- Web depth: active users 2, pageviews 5, events 9
- Best item: glow-index GA4 web traffic 2026-05-26 to 2026-06-01 (2 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-26 to 2026-06-01 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 29
- Web depth: active users 6, pageviews 58, events 162
- Best item: nash-satoshi GA4 web traffic 2026-05-26 to 2026-06-01 (29 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-26 to 2026-06-01 (29 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-25

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-25 to 2026-05-31 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 4
- Web depth: active users 4, pageviews 7, events 15
- Best item: glow-index GA4 web traffic 2026-05-25 to 2026-05-31 (4 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-25 to 2026-05-31 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 34
- Web depth: active users 7, pageviews 62, events 170
- Best item: nash-satoshi GA4 web traffic 2026-05-25 to 2026-05-31 (34 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-25 to 2026-05-31 (34 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-24

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-24 to 2026-05-30 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 5
- Web depth: active users 5, pageviews 8, events 18
- Best item: glow-index GA4 web traffic 2026-05-24 to 2026-05-30 (5 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-24 to 2026-05-30 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 44
- Web depth: active users 5, pageviews 83, events 229
- Best item: nash-satoshi GA4 web traffic 2026-05-24 to 2026-05-30 (44 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-24 to 2026-05-30 (44 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-23

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-23 to 2026-05-29 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 5
- Web depth: active users 5, pageviews 8, events 18
- Best item: glow-index GA4 web traffic 2026-05-23 to 2026-05-29 (5 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-23 to 2026-05-29 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 47
- Web depth: active users 5, pageviews 87, events 256
- Best item: nash-satoshi GA4 web traffic 2026-05-23 to 2026-05-29 (47 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-23 to 2026-05-29 (47 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-22

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-05-22 to 2026-05-28 (1 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 5
- Web depth: active users 5, pageviews 8, events 18
- Best item: glow-index GA4 web traffic 2026-05-22 to 2026-05-28 (5 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-22 to 2026-05-28 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 55
- Web depth: active users 11, pageviews 109, events 343
- Best item: nash-satoshi GA4 web traffic 2026-05-22 to 2026-05-28 (55 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-22 to 2026-05-28 (55 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-21

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-05-21 to 2026-05-27 (1 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 5
- Web depth: active users 5, pageviews 8, events 18
- Best item: glow-index GA4 web traffic 2026-05-21 to 2026-05-27 (5 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-21 to 2026-05-27 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 56
- Web depth: active users 13, pageviews 134, events 399
- Best item: nash-satoshi GA4 web traffic 2026-05-21 to 2026-05-27 (56 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-21 to 2026-05-27 (56 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-20

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-05-20 to 2026-05-26 (1 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 3
- Web depth: active users 3, pageviews 3, events 9
- Best item: glow-index GA4 web traffic 2026-05-20 to 2026-05-26 (3 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-20 to 2026-05-26 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 56
- Web depth: active users 16, pageviews 137, events 416
- Best item: nash-satoshi GA4 web traffic 2026-05-20 to 2026-05-26 (56 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-20 to 2026-05-26 (56 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-19

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-19 to 2026-05-25 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 3
- Web depth: active users 3, pageviews 3, events 9
- Best item: glow-index GA4 web traffic 2026-05-19 to 2026-05-25 (3 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-19 to 2026-05-25 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 56
- Web depth: active users 18, pageviews 135, events 434
- Best item: nash-satoshi GA4 web traffic 2026-05-19 to 2026-05-25 (56 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-19 to 2026-05-25 (56 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-18

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 3
- Best item: glow-index Search Console queries 2026-05-18 to 2026-05-24 (3 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 1
- Web depth: active users 1, pageviews 1, events 3
- Best item: glow-index GA4 web traffic 2026-05-18 to 2026-05-24 (1 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-18 to 2026-05-24 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 71
- Web depth: active users 22, pageviews 174, events 552
- Best item: nash-satoshi GA4 web traffic 2026-05-18 to 2026-05-24 (71 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-18 to 2026-05-24 (71 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-17

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 3
- Best item: glow-index Search Console queries 2026-05-17 to 2026-05-23 (3 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-05-17 to 2026-05-23 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-17 to 2026-05-23 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 58
- Web depth: active users 19, pageviews 171, events 539
- Best item: nash-satoshi GA4 web traffic 2026-05-17 to 2026-05-23 (58 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-17 to 2026-05-23 (58 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-16

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-16 to 2026-05-22 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-05-16 to 2026-05-22 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-16 to 2026-05-22 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 57
- Web depth: active users 18, pageviews 170, events 525
- Best item: nash-satoshi GA4 web traffic 2026-05-16 to 2026-05-22 (57 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-16 to 2026-05-22 (57 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-15

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-15 to 2026-05-21 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 1
- Web depth: active users 1, pageviews 1, events 5
- Best item: glow-index GA4 web traffic 2026-05-15 to 2026-05-21 (1 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-15 to 2026-05-21 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 49
- Web depth: active users 13, pageviews 167, events 468
- Best item: nash-satoshi GA4 web traffic 2026-05-15 to 2026-05-21 (49 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-15 to 2026-05-21 (49 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-14

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 2
- Best item: glow-index Search Console queries 2026-05-14 to 2026-05-20 (2 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 3
- Web depth: active users 3, pageviews 12, events 26
- Best item: glow-index GA4 web traffic 2026-05-14 to 2026-05-20 (3 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-14 to 2026-05-20 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 47
- Web depth: active users 13, pageviews 147, events 434
- Best item: nash-satoshi GA4 web traffic 2026-05-14 to 2026-05-20 (47 views/impressions)

### nash-satoshi / x
- Posts/results logged: 2
- Views/impressions: 64
- Best item: $BOTCOIN jumped +18.08 points in our latest game theory rankings.

"BOTCOIN implements an epoch-based proof-of-inference mining protocol where AI agents earn tokens by completing i (58 views/impressions)

**Best overall:** nash-satoshi / x — $BOTCOIN jumped +18.08 points in our latest game theory rankings.

"BOTCOIN implements an epoch-based proof-of-inference mining protocol where AI agents earn tokens by completing i (58 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-13

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 1
- Best item: glow-index Search Console queries 2026-05-13 to 2026-05-19 (1 views/impressions)

### glow-index / web
- Posts/results logged: 3
- Views/impressions: 3
- Web depth: active users 3, pageviews 12, events 26
- Best item: glow-index GA4 web traffic 2026-05-13 to 2026-05-19 (3 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-13 to 2026-05-19 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 3
- Views/impressions: 40
- Web depth: active users 10, pageviews 130, events 382
- Best item: nash-satoshi GA4 web traffic 2026-05-13 to 2026-05-19 (40 views/impressions)

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 20
- Best item: Nash Satoshi has AI Agents averaging 77.8 across 218 tokens.

While AI Infrastructure is scoring 81.0 across only 18.

Does this suggest the crowded trade is agents?

Is the sharpe (20 views/impressions)

### vista / app_store
- Posts/results logged: 36
- Views/impressions: 0
- Best item: Vista App Store reporting readiness (None views/impressions)

### vista / web
- Posts/results logged: 36
- Views/impressions: 0
- Best item: Vista web analytics readiness (None views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-13 to 2026-05-19 (40 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-12

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-12 to 2026-05-18 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 3
- Web depth: active users 3, pageviews 12, events 26
- Best item: glow-index GA4 web traffic 2026-05-12 to 2026-05-18 (3 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-12 to 2026-05-18 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 38
- Web depth: active users 11, pageviews 113, events 342
- Best item: nash-satoshi GA4 web traffic 2026-05-12 to 2026-05-18 (38 views/impressions)

### nash-satoshi / x
- Posts/results logged: 2
- Views/impressions: 307
- Engagement: likes 5, comments 0, saves 0, reposts 1
- Best item: $GITLAWB is the now the number 3 overall ranked game theory token.

"GITLAWB is building a decentralized git network that gives AI agents first-class workflow primitives and crypto (230 views/impressions)

**Best overall:** nash-satoshi / x — $GITLAWB is the now the number 3 overall ranked game theory token.

"GITLAWB is building a decentralized git network that gives AI agents first-class workflow primitives and crypto (230 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-11

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-11 to 2026-05-17 (0 views/impressions)

### glow-index / tiktok
- Posts/results logged: 1
- Views/impressions: 310
- Engagement: likes 1, comments 0, saves 0, reposts 0
- Best item: 5 ingredients dermatologists actually avoid (310 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 3
- Web depth: active users 3, pageviews 12, events 26
- Best item: glow-index GA4 web traffic 2026-05-11 to 2026-05-17 (3 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-11 to 2026-05-17 (0 views/impressions)

### nash-satoshi / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: The Difference Between Buying Strength And Holding Someone Else's Bags Is 4 AIs (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 27
- Web depth: active users 12, pageviews 64, events 186
- Best item: nash-satoshi GA4 web traffic 2026-05-11 to 2026-05-17 (27 views/impressions)

### nash-satoshi / x
- Posts/results logged: 7
- Views/impressions: 1524
- Engagement: likes 28, comments 3, saves 0, reposts 6
- Best item: GPT 5.5, Opus 4.7, Gemini 3.1 Pro, and Grok 4 worked together and cross checked each other to produce optimal crypto token analyses with a focus on game theory positioning.

Here i (437 views/impressions)

**Best overall:** nash-satoshi / x — GPT 5.5, Opus 4.7, Gemini 3.1 Pro, and Grok 4 worked together and cross checked each other to produce optimal crypto token analyses with a focus on game theory positioning.

Here i (437 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-10

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-10 to 2026-05-16 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 3
- Web depth: active users 3, pageviews 12, events 26
- Best item: glow-index GA4 web traffic 2026-05-10 to 2026-05-16 (3 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-10 to 2026-05-16 (0 views/impressions)

### nash-satoshi / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: Every Pump Has 5 Phases. Most Traders Learn About Mania One Phase Too Late. (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 14
- Web depth: active users 7, pageviews 39, events 114
- Best item: nash-satoshi GA4 web traffic 2026-05-10 to 2026-05-16 (14 views/impressions)

### vista / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item:  (0 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-10 to 2026-05-16 (14 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-09

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-09 to 2026-05-15 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 3
- Web depth: active users 3, pageviews 12, events 26
- Best item: glow-index GA4 web traffic 2026-05-09 to 2026-05-15 (3 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-09 to 2026-05-15 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 9
- Web depth: active users 6, pageviews 31, events 87
- Best item: nash-satoshi GA4 web traffic 2026-05-09 to 2026-05-15 (9 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-09 to 2026-05-15 (9 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-08

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-08 to 2026-05-14 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 2
- Web depth: active users 2, pageviews 11, events 21
- Best item: glow-index GA4 web traffic 2026-05-08 to 2026-05-14 (2 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-08 to 2026-05-14 (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 7
- Web depth: active users 5, pageviews 10, events 50
- Best item: nash-satoshi GA4 web traffic 2026-05-08 to 2026-05-14 (7 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-08 to 2026-05-14 (7 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-07

### glow-index / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index Search Console queries 2026-05-07 to 2026-05-13 (0 views/impressions)

### glow-index / web
- Posts/results logged: 1
- Views/impressions: 0
- Best item: glow-index GA4 web traffic 2026-05-07 to 2026-05-13 (0 views/impressions)

### nash-satoshi / search_console
- Posts/results logged: 1
- Views/impressions: 0
- Best item: nash-satoshi Search Console queries 2026-05-07 to 2026-05-13 (0 views/impressions)

### nash-satoshi / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: What Nash Satoshi actually measures, in 5 slides (0 views/impressions)

### nash-satoshi / web
- Posts/results logged: 1
- Views/impressions: 4
- Web depth: active users 2, pageviews 0, events 10
- Best item: nash-satoshi GA4 web traffic 2026-05-07 to 2026-05-13 (4 views/impressions)

### vista / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: My VISTA profile after rating 400 films (0 views/impressions)

**Best overall:** nash-satoshi / web — nash-satoshi GA4 web traffic 2026-05-07 to 2026-05-13 (4 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-06

### nash-satoshi / tiktok
- Posts/results logged: 1
- Views/impressions: 200
- Engagement: likes 3, comments 0, saves 0, reposts 0
- Best item: Crypto Isn't A Guessing Game. It's A Math Problem Most Traders Refuse To Solve. (200 views/impressions)

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 18
- Best item: single-model crypto analysis is how you inherit one model’s blind spots.

the edge is disagreement.

Claude, GPT, Gemini, and Grok each scor (18 views/impressions)

**Best overall:** nash-satoshi / tiktok — Crypto Isn't A Guessing Game. It's A Math Problem Most Traders Refuse To Solve. (200 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-05

### nash-satoshi / tiktok
- Posts/results logged: 1
- Views/impressions: 182
- Engagement: likes 4, comments 0, saves 0, reposts 0
- Best item: 4 AIs Agreeing On A Token Is Rarer Than You Think. It Matters When They Do. (182 views/impressions)

### vista / tiktok
- Posts/results logged: 2
- Views/impressions: 193
- Engagement: likes 5, comments 0, saves 0, reposts 0
- Best item: Me and my boyfriend are 34% compatible on Vista. We're doing couples counseling now. (193 views/impressions)

**Best overall:** vista / tiktok — Me and my boyfriend are 34% compatible on Vista. We're doing couples counseling now. (193 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-05-04

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 449
- Engagement: likes 8, comments 0, saves 0, reposts 4
- Best item: We've upgraded the analysis workflow to use GPT-5.5 and Claude Opus 4.7.

Updated top 10 ranked game theory tokens:

1. $CRED 
2. $CLAWD
3.  (449 views/impressions)

**Best overall:** nash-satoshi / x — We've upgraded the analysis workflow to use GPT-5.5 and Claude Opus 4.7.

Updated top 10 ranked game theory tokens:

1. $CRED 
2. $CLAWD
3.  (449 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-29

### vista / tiktok
- Posts/results logged: 2
- Views/impressions: 0
- Best item:  (0 views/impressions)

**Best overall:** vista / tiktok —  (0 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-21

### nash-satoshi / tiktok
- Posts/results logged: 2
- Views/impressions: 0
- Best item: watch this (0 views/impressions)

### vista / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: watch this (0 views/impressions)

**Best overall:** nash-satoshi / tiktok — watch this (0 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-19

### vista / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: IMDb gave Midsommar a 7.1. that's the wrong number. (0 views/impressions)

**Best overall:** vista / tiktok — IMDb gave Midsommar a 7.1. that's the wrong number. (0 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-17

### vista / tiktok
- Posts/results logged: 1
- Views/impressions: 1114
- Engagement: likes 9, comments 1, saves 1, reposts 0
- Best item: IMDb gave Midsommar a 7.1. that's the wrong number. (1114 views/impressions)

**Best overall:** vista / tiktok — IMDb gave Midsommar a 7.1. that's the wrong number. (1114 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-16

### nash-satoshi / tiktok
- Posts/results logged: 2
- Views/impressions: 0
- Best item: watch this (0 views/impressions)

**Best overall:** nash-satoshi / tiktok — watch this (0 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-12

### vista / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: i can't believe i've been using half-stars this whole time (0 views/impressions)

**Best overall:** vista / tiktok — i can't believe i've been using half-stars this whole time (0 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-10

### vista / tiktok
- Posts/results logged: 1
- Views/impressions: 453
- Engagement: likes 2, comments 1, saves 0, reposts 0
- Best item: i can't believe i've been using half-stars this whole time (453 views/impressions)

**Best overall:** vista / tiktok — i can't believe i've been using half-stars this whole time (453 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-09

### nash-satoshi / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: watch this (0 views/impressions)

**Best overall:** nash-satoshi / tiktok — watch this (0 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-07

### nash-satoshi / tiktok
- Posts/results logged: 1
- Views/impressions: 0
- Best item: watch this (0 views/impressions)

**Best overall:** nash-satoshi / tiktok — watch this (0 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-04-01

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 56
- Engagement: likes 1, comments 0, saves 0, reposts 2
- Best item: Outperformance? 🤔 https://t.co/ttkMvyHI7C (56 views/impressions)

**Best overall:** nash-satoshi / x — Outperformance? 🤔 https://t.co/ttkMvyHI7C (56 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-03-24

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 1177
- Engagement: likes 18, comments 7, saves 1, reposts 6
- Best item: We upgraded to GPT-5.4, Gemini 3.1 Pro, and Opus 4.6 for this week's updated analyses.

And it produced quite different results. Only 8 S+ t (1177 views/impressions)

**Best overall:** nash-satoshi / x — We upgraded to GPT-5.4, Gemini 3.1 Pro, and Opus 4.6 for this week's updated analyses.

And it produced quite different results. Only 8 S+ t (1177 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-03-22

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 168
- Engagement: likes 3, comments 1, saves 1, reposts 1
- Best item: $BOTCOIN is the number 1 ranked game theory token.

"A native currency for autonomous AI agents through a proof-of-inference mining mechanis (168 views/impressions)

**Best overall:** nash-satoshi / x — $BOTCOIN is the number 1 ranked game theory token.

"A native currency for autonomous AI agents through a proof-of-inference mining mechanis (168 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-03-21

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 329
- Engagement: likes 3, comments 0, saves 1, reposts 2
- Best item: We are back up and running.

Updated top 10:
1. $BOTCOIN
2. $CLAWD
3. $CLAWNCH
4. $TRIDENT
5. $A0T
6. $DIEM
7. $TAKEOVER
8. $XONA
9. $MLTL
1 (329 views/impressions)

**Best overall:** nash-satoshi / x — We are back up and running.

Updated top 10:
1. $BOTCOIN
2. $CLAWD
3. $CLAWNCH
4. $TRIDENT
5. $A0T
6. $DIEM
7. $TAKEOVER
8. $XONA
9. $MLTL
1 (329 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-03-17

### nash-satoshi / x
- Posts/results logged: 1
- Views/impressions: 18
- Best item: Experiencing some technical difficulties with this week's updated analyses.

We should have a fix in place by EOD. Apologies for the inconve (18 views/impressions)

**Best overall:** nash-satoshi / x — Experiencing some technical difficulties with this week's updated analyses.

We should have a fix in place by EOD. Apologies for the inconve (18 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

## Metrics Summary — Week of 2026-02-27

### nash-satoshi / x
- Posts/results logged: 3
- Views/impressions: 46
- Engagement: likes 1, comments 3, saves 0, reposts 0
- Best item: Output per token:

-Consensus recommendation across all 4 models
-Where they disagreed and why
-Nash equilibrium optimal position

A scoreca (27 views/impressions)

**Best overall:** nash-satoshi / x — Output per token:

-Consensus recommendation across all 4 models
-Where they disagreed and why
-Nash equilibrium optimal position

A scoreca (27 views/impressions)

**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.

_Last updated: 2026-06-20_

<!-- METRICS_SUMMARY_END -->

## Run Note — Week of 2026-05-11 — 2026-05-11
- Generated counts: X 0; Reddit 0; TikTok/ReelFarm support 2; LinkedIn 0.
- Queue append: +2 approved entries; queue count 120 → 122.
- Skips: Nash X skipped because live ranking/model-disagreement details were not verified; Reddit skipped for compliance risk; LinkedIn skipped because May monthly post already exists and no new milestone/proof was available.
- Measurement blocker: metrics remain thin; App Store Connect parked and ReelFarm/TikTok live IDs need handoff before increasing volume.
- Next durable discovery action: reconcile planned rows in `memory/app-marketing/post-registry.jsonl` to exact live ReelFarm/TikTok post IDs after JT posts from laptop.



## Run Note — Week of 2026-05-18
- Generated: X 1, Reddit 0, TikTok/ReelFarm support 2 hook/slide concepts only, LinkedIn 0.
- Approved queue entries: 3 (`nash-satoshi-x-2026-05-18-ranking-update-1`, `vista-tiktok-2026-05-18-rating-precision-1`, `nash-satoshi-tiktok-2026-05-18-model-consensus-1`).
- Skips: Reddit skipped because no clearly compliant community-native angle was needed this week; LinkedIn skipped because May monthly cadence already used and no new product milestone/proof.
- Measurement blocker: metrics remain thin; volume should not increase until ReelFarm/TikTok live IDs, X post IDs, and App Store/web metrics are reconciled.
- Next durable discovery action: reconcile planned queue entries to live post IDs in `memory/app-marketing/post-registry.jsonl`, then rerun metrics collection/analysis before scaling output.
- Behavioral demand lens: Vista draft uses precision/taste identity and challenges coarse 5-star ratings; Nash drafts use uncertainty reduction, model-disagreement curiosity, and ranking-dispersion as the research trigger.


## Run Note — 2026-05-25
- Generated counts: X 0; Reddit 0; TikTok/ReelFarm support 1; LinkedIn 0.
- Approved: 1 Vista rating-precision ReelFarm concept mapped to `Vista rating precision retest` with source tag `vista_tiktok_rating_precision_20260525`.
- Skips: Nash X/TikTok skipped because live rankings are stale (~161h old); Reddit skipped for compliance risk; LinkedIn skipped because May monthly post already exists and no new milestone/proof.
- Measurement blocker: Vista/ReelFarm live post IDs + App Store metrics still need reconciliation; Nash leaderboard freshness must be restored before ranking copy.
- Next durable discovery action: fix/refresh Nash ranking generation or leaderboard freshness, then produce one ranking/model-disagreement X draft from live data only.

## Run Note — 2026-06-01 Product Content
- Generated counts: X 1, Reddit 0, TikTok/ReelFarm support 1 hook/slide concept only, LinkedIn 0.
- Approved queue entries: `vista-x-2026-06-01-rating-precision-1`, `vista-tiktok-2026-06-01-rating-precision-1`.
- Skips: Nash X/TikTok skipped because `scripts/nash_rankings_probe.py --json --limit 10` returned stale rankings (~329h old); Reddit skipped fail-closed; LinkedIn skipped because no new product milestone/proof.
- Measurement blocker: Vista/ReelFarm live post IDs and App Store/App metrics still need reconciliation before volume increases.
- Next durable discovery action: reconcile Vista live post IDs into `memory/app-marketing/post-registry.jsonl`, then compare 24h/72h/7d metrics before reusing rating-precision again.
- Review doc: `https://docs.google.com/document/d/1CPONywqHxRlmcvf_kbXFvgVpadUMeGYBCGd5kKBiDq8/edit` (local: `/Users/jtsomwaru/.openclaw/workspace/memory/drafts/app-marketing-review-2026-06-01.md`).
