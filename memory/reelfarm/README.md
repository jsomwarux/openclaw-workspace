# ReelFarm Intel OS

Purpose: daily/weekly strategy intelligence layer for JT's TikTok native slideshow campaigns.

## Daily input
Drop or forward Social Growth Engineers newsletter content into:
`memory/reelfarm/newsletters/inbox/`

Preferred filename:
`YYYY-MM-DD-social-growth-engineers.md`

Plain text or markdown is fine. Include the full newsletter body when possible.

## Daily output
Daily cron reads new inbox files, filters for slideshow-transferable patterns only, saves report to:
`memory/reelfarm/reports/daily/YYYY-MM-DD.md`

It sends Telegram only when there are strong recommendations. No weak padding.

## Weekly output
Weekly cron synthesizes the last 7 days of newsletters, daily recommendations, and analytics data, then saves:
`memory/reelfarm/reports/weekly/YYYY-MM-DD.md`

## Analytics feedback
When available, export TikTok/ReelFarm performance into:
`memory/reelfarm/analytics/post-performance.csv`

Columns:
date,app,automation,hook,views,avg_watch_time,completion_rate,swipe_rate,profile_visits,link_clicks,notes

## Add/remove apps
Edit `memory/reelfarm/config/apps.json`:
- Add new app object with product, audience, positioning, voice, strong_devices, banned.
- Set `status` to `paused` or `sunset` to remove from daily review without deleting history.
## Gmail unread behavior
The Social Growth Engineers Gmail ingest uses read-only Gmail access and does not mark messages as read, archive them, label them, or otherwise modify Gmail. Unread emails in `openclawagenteve14@gmail.com` can still have been scraped and analyzed. The source of truth is `memory/reelfarm/gmail-state.json` plus files moved into `memory/reelfarm/newsletters/processed/`.
