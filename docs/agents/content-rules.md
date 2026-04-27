# Content Generation Rules
> Source: AGENTS.md §Content Generation Rule
> Governs all X posts, threads, and LinkedIn content for JT.

## Pre-Draft Checklist (mandatory)
Before drafting ANY post or content for JT:
1. Read `memory/content-voice.md` in full
2. Fetch current swipe-file references with `python3 scripts/notion-swipe-fetch.py --limit 12 --min-engagement 500` unless Notion/API is unavailable; if unavailable, explicitly say swipe references were unavailable and use the latest local weekly content's hook mappings instead.
3. Select 2-4 reference patterns that match the platform + niche + format, then write a `Hook mappings from swipe file` section in the draft file before the posts.
4. Run the audit checklist at the bottom of `memory/content-voice.md` on every draft before delivering

## Swipe File Requirement
The Notion Viral Posts Swipe database is not just an archive. It must influence output.
- Weekly content packs: include a `Hook mappings from swipe file` section with the actual patterns used.
- One-off X/LinkedIn drafts: mention the pattern internally in the saved draft when a file is created.
- Priority niches to keep represented: AI Consulting, NYC SMB, Construction, Property Management, Wholesale Distribution, Skilled Trades, AI Agents/OpenClaw, Job Market, Nash Satoshi/x402, Personal Brand.
- If a niche has fewer than 3 usable recent examples, create a Mission Control task to collect more examples instead of pretending the swipe file is sufficient.

## Core Voice Rules
- Start with the point, never with setup or preamble
- "you/your" must outnumber "I/my" 5:1 or better
- Standalone posts: target 6–15 words
- No forbidden words (full list in content-voice.md)
- No em dashes, no exclamation points, no "Here's the thing:" openers
- Threads: max 5 tweets; most should be 3

## Wednesday LinkedIn
Most important post of the week. Wednesday LinkedIn is a case study post — real build, honest framing, specific outcome. Always load `skills/wednesday-linkedin/SKILL.md` before drafting.

## Platform Calibration
- **X**: compression + hot takes, standalone 6–15 words
- **LinkedIn**: case studies + expertise positioning, longer form OK
- **Reddit**: authentic discussion tone, value-first comment

## Autonomous Post Detection
When notable work completes: evaluate against `memory/content/post-detection-rubric.md`.
Pass → generate X + LinkedIn post, write to `memory/content/bank/[MONDAY-DATE]/auto-[slug].md`, upload both to Drive, push both to Notion calendar. Full procedure: `docs/agents/post-detection-rules.md`

## Proof Points Auto-Update
Anything shipped/done/live → update `memory/content-voice.md` Proof Points immediately (same turn). Add to Builds table. Also add to Content-Ready Angles if post hook exists. Skip internal-only builds.

## Recent Builds → Content
Append to `memory/content/recent-builds.md` in the same turn. Required fields: Build Name + date | What | For | Outcome | Demonstrates | Content angle | Status: complete.

## Technical Angles Bank
`memory/content/technical-angles.md` = source bank for technical X posts.
Append when: non-obvious problem solved, new agent/cron pattern established, "learned this the hard way" moment, or system design decision that practitioners would find useful.
Format: `- **[Pattern name]:** [2–3 sentences, specific enough to apply immediately.]`

## Posted Reply Logging
When JT replies "posted" or "posted both":
1. Identify which post(s) from the most recent content-reminder or content-sunday send
2. Update `memory/content/posted-log.jsonl` — set `"posted": true` + `"posted_date": "YYYY-MM-DD"`
3. If JT specifies platform, mark only that entry
4. Confirm: "Logged ✅ — [post description] marked posted."
