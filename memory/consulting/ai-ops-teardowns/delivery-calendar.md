# AI Ops Teardowns — Delivery Calendar

## Standing Cadence
- Sunday 7:15PM ET: `AI Ops Teardown Weekly Draft` cron (`f96cc24f`) scans/scores topics and writes one review-ready bundle or skips weak topics.
- Monday morning: surface the selected bundle for JT review/posting.
- Wednesday: publish/deepen if a real template or screenshot exists.
- Friday: tactical compressed follow-up if new angle exists.

## Current Bundle
### 2026-05-17 — Rent Delinquency Data Readiness Queue
Status: ready to review/post; not posted as of 2026-05-17 weekly run.
Recommended first platform: LinkedIn.
Local draft: `memory/content/bank/2026-05-17/ai-ops-teardown-rent-delinquency-readiness.md`
Supporting teardown: `memory/consulting/ai-ops-teardowns/2026-05-17-rent-delinquency-readiness.md`
Build tier: Tier 2 now; Tier 3 gated until the teardown is posted and produces operator reply/DM signal, or JT explicitly prioritizes a synthetic-data build.
JT action: review LinkedIn draft, edit if desired, post or explicitly defer, then send URL back if posted. Mission Control task: `j5758pva0bw51gtx17pjdaxcmn86we3s`.
Proof-safe framing: category/hypothetical language only; no private client names, no fake client claims, no ROI/hours-saved/collection-rate/client-acceptance claims.
Why this matters: shows buyer-safe implementation judgment for property/family-office teams by validating delinquency reports and approval boundaries before tenant-facing automation.
Posted URL capture: append exactly one JSONL record to `memory/content/posted-log.jsonl` only after a public URL exists. Required fields: `date`, `platform`, `title`, `source`, `url`, `posted: true`, `cta`, `reply_route`.
Reply/DM routing: route relevant property/family-office replies to `memory/consulting/family-office-ai-ops-diagnostic-one-pager.md`.
Defer capture: if JT defers, update this calendar with reason + next review date; do not mark posted.

## Prior Unposted Bundle
### 2026-05-10 — Property Insurance Expiration Exception Layer
Status: ready to review/post; not posted as of 2026-05-17 weekly run. Do not create duplicate review/post tasks; the active MC review/post task now points to the latest rent-delinquency draft while preserving this as an alternate if JT prefers the cleaner insurance-expiration angle.
Recommended first platform: LinkedIn.
Local draft: `memory/content/bank/2026-05-10/ai-ops-teardown-property-insurance-expiration.md`
Monday delivery bundle: `memory/consulting/ai-ops-teardowns/monday-delivery-bundle-2026-05-11.md`
Saturday prep pack: `memory/consulting/ai-ops-teardowns/saturday-prep-pack-2026-05-16.md`
Supporting teardown: `memory/consulting/ai-ops-teardowns/2026-05-10-property-insurance-expiration.md`
Build tier: Tier 3 candidate, gated.
Next build: reusable n8n template task is in Mission Control, but must wait for posted-teardown reply/DM signal or explicit JT priority.
Posted URL capture: append exactly one JSONL record to `memory/content/posted-log.jsonl` only after a public URL exists. Required fields: `date`, `platform`, `title`, `source`, `url`, `posted: true`, `cta`, `reply_route`.
Defer capture: if JT defers, update this calendar with reason + next review date; do not mark posted.

## Monday Morning Delivery Checklist
- Surface the current 2026-05-17 rent delinquency readiness draft to JT during the first active morning check-in.
- If JT posts it, capture the URL and append to `memory/content/posted-log.jsonl`.
- If JT defers it, update this calendar with defer reason + next review date and keep the MC task open or replace it with one concrete next action.
- Do not build any Tier 3 n8n template unless a posted teardown produces operator reply/DM signal or JT explicitly prioritizes the build.

## Next Planned Bundles
1. Construction Field Note → Owner Update — drafted 2026-05-10; use as X-first test.
2. Wholesale Order Status Exception Desk — Tier 2 mock workflow.
3. Family Office Cash Timing / Overdraft Risk Queue — approval-only content; use after property workflow posts have been tested.
