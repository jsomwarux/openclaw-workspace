# Viral Post Swipe File — X Research — 2026-06-01

## Search Coverage
- Ran all 6 required core queries with `--sort likes --since 7d --limit 12 --json`.
- Added `--min-likes 10` for broad AI/creator-style searches.
- Attempted the prescribed 14-day fallback with `--since 14d --min-likes 5`, but the X API rejected start times older than 7 days.
- Ran all 3 adjacent backfill queries because core usable posts were thin.

## Usable Posts
- @lukepierceops — 846 engagement / 74,945 impressions — AI consulting category conviction. Relevant to JT, but needs sharper operator framing.
- @tax_zack — 22 engagement / 2,778 impressions — CFO to back-office workflow to AI consulting wedge. Highly relevant to JT's property/family-office wedge.
- @godofprompt — 472 engagement / 27,916 impressions — Claude Code evidence stack. Relevant to Eve/OpenClaw proof and agent operating system content.
- @raunak_yadush — 155 engagement / 3,415 impressions — Claude guide/resource-pack mechanic. Relevant as a format mechanic, less as a source voice.
- @fivosaresti — 67 engagement / 972 impressions — GTM tool stack including Claude Code and n8n. Useful but below swipe threshold.
- @tec_aryan — 369 engagement / 43,682 impressions — exact 4-agent workflow thread. Transferable mechanic, but Notion script skipped as duplicate.

## Low Signal
- Agentforce search: LOW_SIGNAL. Mostly vendor promo, stock ticker snippets, and hashtag posts with sub-100 impressions.
- SMB/property/construction search: LOW_SIGNAL. Mostly generic vendor promotion and sub-100-impression posts.
- Distribution search: LOW_SIGNAL. Mostly engagement bait and X algorithm connect posts.

## Signal Analysis
- FORMAT: Concrete stack/artifact breakdown appeared again across Claude Code evidence stack, resource packs, tool stacks, and exact workflow thread. Threshold would pass, but it was already logged on 2026-05-29 and marked already covered.
- TOPIC: AI consulting as business opportunity had high impressions from @lukepierceops but did not clear the 1,000-engagement or 3-independent-post threshold.
- MECHANIC: Wedge sequence from trusted back-office work into AI is promising for JT, but only one strong post this run.

NO_STRONG_SIGNAL

## Swipe Pushes
- Pushed: @lukepierceops, @tax_zack, @godofprompt, @raunak_yadush.
- Skipped duplicate: @tec_aryan.
- RECENT_SWIPE_GAP: Agentforce, NYC SMB, property management, construction, and distribution lacked enough recent high-quality examples.

## Reply Targets
- Local file: `memory/content/reply-targets-2026-06-01.md`
- Drive: https://docs.google.com/document/d/1pJG_MeBxI8uhoYBsdGW-dVxZcvMrsDjRo-U0kBcx4vI/edit
- Validator: passed `x_reply_targets_latest`; warning only referenced older historical files missing links.
