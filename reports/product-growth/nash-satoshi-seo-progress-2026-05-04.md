# Nash Satoshi SEO / AI Crawler Progress — 2026-05-04

## Shipped
- Extended `server/static.ts` production sitemap route to pull the current top 10 leaderboard symbols from `/api/leaderboard?limit=10&sortBy=latestScore&order=desc`.
- Added dynamic `/token/{SYMBOL}` entries to `/sitemap.xml` with daily recrawl priority.
- Added explicit `Allow: /token/` to `/robots.txt`.

## Why it matters
The first crawl endpoints were static. This update turns the sitemap into a live acquisition surface for the highest-scoring token pages, which is the next gate in the Nash Satoshi AI-search/SEO task.

## Verification
- Ran `npm run check`.
- Result: still blocked by pre-existing `server/routes.ts(1087,9): Type 'number' is not assignable to type 'string'`.
- The TypeScript error predates this SEO work and is outside `server/static.ts`.

## Next gate
Fix the pre-existing TS error, then run a production build and hit:
- `/robots.txt`
- `/sitemap.xml`
- `/llms.txt`
- `/token/{top-symbol}`
