# Nash Satoshi — Weekly Ranking Receipt Card Generator Implementation Plan
Date: 2026-05-19
Repo: `/Users/jtsomwaru/projects/nash-satoshi-2`
Status: build-ready coding task

## Repo Evidence
- React/Vite frontend with TypeScript.
- Existing share-card flow exists:
  - `client/src/components/scorecard/ShareModal.tsx`
  - `client/src/components/scorecard/ShareCard.tsx`
  - uses `html-to-image`
  - `/api/image-proxy` exists in `server/routes.ts`
- Leaderboard data is already fetched by:
  - `client/src/hooks/useLeaderboard.ts`
  - `client/src/pages/Leaderboard.tsx`
- Project rules require reading `PROJECT_CONTEXT.md` and `CHANGELOG.md` before coding, then updating `CHANGELOG.md` after changes.

## Verdict
Implement this as a **static frontend generator first**, reusing the existing `html-to-image` share-card pattern. Do not build a full backend archive or database table in the first pass.

## Product Goal
Generate a weekly public card that makes Nash feel like a ranking thesis engine with receipts:

`ranked data → weekly AI Agents receipt card → public post/archive → analyst/newsletter outreach`

## MVP Scope
### Route
Add a new internal/public route:
- `/receipts/weekly`

Alternative if router conventions prefer:
- `/weekly-receipt`

### Components
Create:
- `client/src/components/receipts/WeeklyReceiptCard.tsx`
- `client/src/components/receipts/WeeklyReceiptGenerator.tsx`
- optional `client/src/pages/WeeklyReceipt.tsx`

### Data Source MVP
Use live leaderboard data already exposed to frontend.

Default category for first card:
- `AI Agents`

If exact category filtering is unavailable, use available fields in this order:
1. `primaryNarrative === "AI Agents"`
2. `subNarrative` contains AI/agent/x402
3. fallback manual curated list from top leaderboard rows with AI-agent narrative labels

## Card Fields
Required:
- week label
- category: AI Agents
- 5-7 projects/tokens
- current rank
- rank delta if available, otherwise `new` / `tracked`
- short thesis note
- model disagreement line if model data exists
- methodology footer

Safe footer:
`Game theory + narrative + incentives + model disagreement. Not financial advice. No future-price forecast.`

## Design
Use existing Nash cyber/dark style:
- dark background
- neon/cyan accent
- monospace labels
- receipt/timestamp feel
- avoid candlestick/trading terminal styling

Recommended dimensions:
- 1200x1200 for X image
- later: 1080x1920 variant

## Export Flow
Reuse `ShareModal.tsx` mechanics:
- `toPng`
- fixed offscreen render node
- download PNG
- copy caption
- optional X share URL

Do **not** upload to server in MVP unless existing share-image endpoint supports it cleanly.

## Caption Template
```text
This week's Nash Satoshi AI Agents receipt:

[biggest movement/disagreement line]

Not a price call. Just the ranking thesis and where the models split.
```

## Tracking
Add source tags manually in generated copy:
- `nash_aiagents_receipt_x_20260519`
- `nash_weekly_receipt_ai_agents`

## Acceptance Criteria
- Route renders without auth errors in beta mode.
- Card renders 5+ token rows from real/current app data or a clearly labeled curated fallback.
- Download produces PNG.
- Copy caption contains no price target, buy/sell, or return language.
- TypeScript passes: `npm run check`.
- Build passes if feasible: `npm run build`.
- `CHANGELOG.md` updated.

## Out of Scope for MVP
- Automated weekly cron.
- Database receipt archive.
- Dynamic historical rank deltas if prior-week storage does not already exist.
- Public outreach before two polished receipts exist.

## References
- `memory/app-marketing/share-artifacts/nash-weekly-ranking-receipt-card-spec-2026-05-19.md`
- `memory/app-marketing/outreach-packs/nash-borrowed-audience-pack-2026-05-19.md`
- `memory/app-marketing/experiment-queue-2026-05-19.jsonl`
