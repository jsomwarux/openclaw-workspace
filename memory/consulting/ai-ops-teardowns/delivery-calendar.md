# AI Ops Teardowns — Delivery Calendar

## Standing Cadence
- Sunday 7:15PM ET: `AI Ops Teardown Weekly Draft` cron (`f96cc24f`) scans/scores topics and writes one review-ready bundle or skips weak topics.
- Monday morning: surface the selected bundle for JT review/posting.
- Wednesday: publish/deepen if a real template or screenshot exists.
- Friday: tactical compressed follow-up if new angle exists.

## Current Bundle
### 2026-05-10 — Property Insurance Expiration Exception Layer
Status: ready to review/post; not posted as of 2026-05-13 hardening check.
Recommended first platform: LinkedIn.
Local draft: `memory/content/bank/2026-05-10/ai-ops-teardown-property-insurance-expiration.md`
Monday delivery bundle: `memory/consulting/ai-ops-teardowns/monday-delivery-bundle-2026-05-11.md`
Supporting teardown: `memory/consulting/ai-ops-teardowns/2026-05-10-property-insurance-expiration.md`
Build tier: Tier 3 candidate, gated.
Next build: reusable n8n template task is in Mission Control, but should wait for posted-teardown reply/DM signal or explicit JT priority.
JT action: review LinkedIn draft, edit if desired, post or explicitly defer, then send URL back if posted. Mission Control task: j57e5q8chn2q3ygrd1at9s079986ek6q.
Posted URL capture: append exactly one JSONL record to `memory/content/posted-log.jsonl` only after a public URL exists. Required fields: `date`, `platform`, `title`, `source`, `url`, `posted: true`, `cta`, `reply_route`.
Defer capture: if JT defers, update this calendar with reason + next review date; do not mark posted.

## Monday Morning Delivery Checklist
- Surface the `monday-delivery-bundle-2026-05-11.md` to JT during the first active morning check-in, not buried in overnight notes.
- If JT posts it, capture the URL and append to `memory/content/posted-log.jsonl`.
- If there is no engagement or no operator reply, do not build the Tier 3 n8n template yet; use rent delinquency readiness as the next lighter draft instead.

## Next Planned Bundles
1. Rent Delinquency Data Readiness + Outreach Queue — drafted 2026-05-10; ready after insurance-expiration post.
2. Construction Field Note → Owner Update — drafted 2026-05-10; use as X-first test.
3. Wholesale Order Status Exception Desk — Tier 2 mock workflow.
