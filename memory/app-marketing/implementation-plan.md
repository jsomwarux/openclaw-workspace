# App Marketing OS — Implementation Plan

## Decision
App marketing is now a first-class North Star system. The goal is to create reusable distribution infrastructure for current and future apps while preserving the existing systems that already work. JT's laptop owns ReelFarm slideshow execution; Eve owns strategy, tracking, assets, and adjacent distribution systems.

## Phase 1 — Foundation (done / in progress)
Status: started 2026-05-06

Completed:
- Audited current systems.
- Created OS spec.
- Created app registry.
- Created weekly scoreboard template.
- Created directory/backlink backlog.
- Created SEO backlog.
- Created ASO checklist.
- Created future-app onboarding template.
- Created metrics inbox + parser: `memory/app-marketing/metrics-inbox.jsonl` and `scripts/app_marketing_metrics.py`.
- Created post registry + automated collector skeleton: `memory/app-marketing/post-registry.jsonl`, `scripts/app_marketing_collect_metrics.py`, and `scripts/app_marketing_connectors/`.
- Created first public connector: Reddit public score/comments/removal-status fetcher.
- Created asset map: `memory/app-marketing/asset-map.md`.

Files:
- `memory/app-marketing/audit-2026-05-06.md`
- `memory/app-marketing/os-spec.md`
- `memory/app-marketing/app-registry.md`
- `memory/app-marketing/weekly-scoreboard.md`
- `memory/app-marketing/directory-submissions.md`
- `memory/app-marketing/seo-backlog.md`
- `memory/app-marketing/aso-checklist.md`
- `memory/app-marketing/future-app-template.md`

## Phase 2 — Measurement First
Priority: highest

Why:
- Current Vibe Marketing performance log has only 6 entries and all metrics are pending/zero.
- Queue has 119 valid entries but weak feedback.
- The system cannot optimize without true performance data.

Tasks:
1. Do not duplicate JT's laptop ReelFarm slideshow automation.
2. API-first measurement: use `memory/app-marketing/post-registry.jsonl` as canonical list of posted items and `scripts/app_marketing_collect_metrics.py` to collect available platform metrics.
3. Use connector priority: Reddit public metrics first; X API if credentials/tier allow; ReelFarm/TikTok analytics if endpoint/export exists; App Store Connect for Vista after secure API setup; web analytics after provider is identified.
4. Manual metrics inbox remains fallback only: append rows to `memory/app-marketing/metrics-inbox.jsonl`, then run `python3 scripts/app_marketing_metrics.py`.
5. Add one weekly App Marketing Scoreboard cron only after at least one connector produces real Vista/Nash data.

Current done state:
- Metrics inbox exists.
- Parser exists and py_compile passes.
- Empty inbox writes a clear “No metrics entries yet” block to the scoreboard.

Remaining done state:
- Weekly scoreboard shows real Vista and Nash metrics from JT laptop/ReelFarm/X/Reddit outputs.
- Performance log rows move from `pending` to actual score labels once metrics are available.

## Phase 3 — Asset Fixes
Priority: high

Tasks:
1. Confirm whether JT's laptop ReelFarm setup already has the needed Vista/Nash/Glow screenshots.
2. If yes, do not recreate Drive screenshot automation. Instead document screenshot asset locations and naming conventions in `memory/app-marketing/asset-map.md`.
3. If Mac mini systems still generate review docs, keep Drive screenshot folders as optional support assets, not blockers.

Done state:
- Eve knows where canonical screenshots live and can reference them in prompts/strategy.
- No duplicate screenshot pipeline is created unless needed.

## Phase 4 — Durable Discovery
Priority: high

Tasks:
1. Create Vista directory submission pack.
2. Create Nash Satoshi directory submission pack.
3. Draft first SEO page outline for Vista: `1–100 movie rating app` or `Letterboxd alternative for precise movie ratings`.
4. Draft first SEO page outline for Nash: `Game theory crypto analysis` or `Nash Satoshi methodology`.
5. Decide where pages live: app site, jtsomwaru.com, or separate landing pages.

Done state:
- At least one directory submission pack per active app.
- At least one SEO page outline per active app.

## Phase 5 — Product Registry Expansion
Priority: medium-high

Tasks:
1. Add Action Arena to the relevant marketing registry only after there is a landing/waitlist page or beta target.
2. Keep Action Arena primarily in Sports GM/@dynastyjig until launch assets exist.
3. Add Dynasty Fantasy Football Simulator separately if/when it needs marketing automation.
4. Update Glow Index from pending to active only after deployment/engine/screenshot/account gates clear.

Done state:
- No product conflation.
- No generic product-promo content for sports apps.

## Phase 6 — Patch Existing Generators Carefully
Priority: after Phases 2–5

Potential Vibe Marketing patches:
- Tighten Reddit rule: default to no product mention unless subreddit-safe; skip if no compliant community-native angle.
- Add App Marketing OS registry read step.
- Add weekly scoreboard write/read step.
- Add directory/SEO/ASO action recommendation in Telegram summary.

Potential Sports GM patches:
- Add Action Arena prelaunch waitlist metric once page exists.
- Keep product references banned by default.

Do not patch until there is a clear owner surface and regression check.

## Immediate Next Best Action
Build/verify the measurement handoff, not ReelFarm automation. Metrics are still the bottleneck, but execution lives on JT's laptop.

Recommended next task:
- Define a lightweight weekly metrics input format for JT's laptop/ReelFarm output, then have Eve update the App Marketing scoreboard from that input.
