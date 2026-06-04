# Viral Post Swipe File X Research — 2026-06-03

## Search Coverage

Ran all 6 core niche queries with `--sort likes --since 7d --min-likes 10 --limit 12 --json`.

Thin-query 14-day rerun was attempted for n8n, Agentforce, SMB buyers, agent tooling, and distribution, but the X recent-search endpoint rejected `--since 14d`: start time must be on or after 2026-05-27. Restored valid 7-day artifacts and used adjacent backfill.

Adjacent backfill ran all 3 queries with `--sort likes --since 7d --min-likes 10 --limit 12 --json`.

## Usable Posts

- @lukepierceops — 408 engagement / 6,347 impressions — AI consulting discovery-call proof. Relevant to AI Operations Diagnostic.
- @lukepierceops — 1,000 engagement / 109,408 impressions — AI consulting opportunity claim. Relevant but partly course-funnel oriented.
- @kawai_design — 446 engagement / 41,430 impressions — Claude Code folder/artifact stack. Relevant to OpenClaw memory and skill structure.
- @nursetools — 352 engagement / 24,025 impressions — shipped agent workflow debugger. Relevant to workflow failure visibility.
- @tom_doerr — 112 engagement / 3,290 impressions — Salesforce agent skills resource. Relevant to Agentforce assets.
- @fivosaresti — 88 engagement / 1,733 impressions — founder-led content operating layer. Relevant to Eve/content system.
- @fivosaresti — 68 engagement / 1,070 impressions — GTM tool stack including Claude Code and n8n. Relevant but less specific.
- @tax_zack — 22 engagement / 3,703 impressions — accounting firm AI consulting/back-office offer. Relevant to SMB buyer niche.

## Low Signal / Rejected

- SMB buyer core query returned zero posts after the 10-like gate.
- Distribution query included hashtag/connect engagement bait and generic skill lists; most rejected.
- MarketAvenues AI stock list rejected as off-niche market hype.
- X algorithm connect posts rejected as engagement bait.

## Signal Analysis

FORMAT Concrete stack/artifact breakdown met threshold again: 5 appearances / 2,115 total engagement across Claude Code folders, Salesforce skills, StackFl0w debugger, GTM stack, and founder-led content operating layer.

JT has angle: yes. Eve/OpenClaw is an actual stack with AGENTS.md, CLAUDE.md, skills, memory, crons, validators, and Drive/Notion routing.

Posted/logged recently: yes. Same pattern logged 2026-05-29 and already covered, so no format draft trigger fired.

TOPIC signals: no new topic crossed a clean threshold after spam filtering. AI consulting demand was strong through Luke Pierce, but it was dominated by one account and course-funnel mechanics, so no hot-topic fast lane.

MECHANIC signals: artifact-first posts continue working. Transferable pattern: show the operating surface first, then explain the judgment it enables.

## Swipe Pushes

Pushed 5 clean examples to Notion Viral Swipe:

- @lukepierceops discovery-call tactical breakdown.
- @kawai_design Claude Code folder checklist.
- @nursetools StackFl0w shipped artifact.
- @tom_doerr Salesforce agent skills resource.
- @fivosaresti founder-led content operating layer.

No `RECENT_SWIPE_GAP`: at least 3 recent examples were pushed.

## Notes

`memory/content/content-signals.md` was already above the 20K target before this run. Appended the covered 2026-06-03 entry because the signal passed, but this file needs an archive/trim pass outside the cron.
