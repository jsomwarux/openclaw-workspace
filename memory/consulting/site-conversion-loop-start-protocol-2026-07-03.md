# Site Conversion Kill Loop Start Protocol - 2026-07-03

Status: registered, not started. No timers run until JT confirms the relevant site asset shipped.

## Start command

When JT confirms `/property` or the homepage conversion pass is live:

1. Open `memory/consulting/site-conversion-kill-loops-2026-07-03.jsonl`.
2. Set the relevant loop `status` to `active`.
3. Set `timer_start` to the confirmation date.
4. Set `review_due`:
   - `/property`: 21 days after confirmation, with a minimum of 5 connector sends.
   - homepage hero/audit/CTA: 30 days after confirmation, or earlier after 10 buyer conversations.
5. Create or update one Mission Control review task with the review due date in the description.

## Signals to track

Track only:

1. sends and replies
2. calls booked
3. audits paid

Ignore traffic noise, visual polish, teardown output, SEO/blog activity, and Salesforce content during this loop.

## Current state

- `/property` loop: waiting for JT ship confirmation.
- homepage hero/audit loop: waiting for JT ship confirmation.
- CTA signal loop: waiting for JT ship confirmation.

