# Content Generation Rules
> Source: AGENTS.md §Content Generation Rule
> Governs all X posts, threads, and LinkedIn content for JT.

## Pre-Draft Checklist (mandatory)
Before drafting ANY post or content for JT:
1. Read `memory/content-voice.md` in full.
2. Identify the exact platform, niche, and format before fetching references. Platform/niche fit matters more than raw engagement.
3. Fetch current swipe-file references using the narrowest relevant filters available: platform first, then niche, then format. Example: `python3 scripts/notion-swipe-fetch.py --platform X --niche "Dynasty Fantasy" --niche "Sports Betting" --limit 12 --min-engagement 0` or `python3 scripts/notion-swipe-fetch.py --platform LinkedIn --niche "AI Consulting" --format "Case Study" --limit 8`.
4. Never use cross-platform or cross-niche references by default. LinkedIn consulting content must not use dynasty X hooks/context. Dynasty X content must not use LinkedIn consulting patterns. Adjacent references are allowed only when same platform+niche examples are insufficient, and the draft must explicitly label them as adjacent inspiration.
5. Select 2-4 reference patterns that match the platform + niche + format. Extract the mechanic: hook shape, emotional tension, context, rhythm, reply trigger, proof style, and why it worked.
6. Write a `Pattern inputs / Hook mappings from swipe file` section in the draft file before the posts.
7. Translate the mechanics through JT's voice. Do not copy wording, claims, account persona, or structure wholesale.
8. Run the audit checklist at the bottom of `memory/content-voice.md` on every draft before delivering.

## Self-Improving Content Loop
All content Eve generates for JT must use a feedback loop calibrated to the niche and platform.

Loop:
1. **Observe:** Pull proven examples from Notion swipe file and, when needed, fresh X research or platform-native examples.
2. **Extract:** Identify what is working: hook type, context, tone, tension, specificity, proof, pacing, CTA/reply trigger, and platform behavior.
3. **Translate:** Adapt the mechanic into JT's compressed, practical, lightly contrarian voice.
4. **Differentiate:** Add JT's specific proof, operator POV, product context, or decision framework so the content is not imitation.
5. **Log:** Save usable winners or new patterns back into the swipe file/content bank when they reveal a repeatable mechanic.

This applies to X, LinkedIn, Reddit, newsletters, scripts, launch posts, consulting content, sports content, crypto content, job-market/career content, and product content.

## Swipe File Requirement
The Notion Viral Posts Swipe database is not just an archive. It must influence output.
- Weekly content packs: include a `Pattern inputs / Hook mappings from swipe file` section with the actual mechanics used.
- One-off X/LinkedIn/Reddit drafts: mention the pattern internally in the saved draft when a file is created.
- Priority niches to keep represented: AI Consulting, NYC SMB, Construction, Property Management, Wholesale Distribution, Skilled Trades, AI Agents/OpenClaw, Job Market, Nash Satoshi/x402, Crypto, Personal Brand, Dynasty Fantasy, Sports Betting.
- If a niche/platform has fewer than 3 usable recent examples, create a Mission Control task to collect more examples instead of pretending the swipe file is sufficient. Until then, use adjacent references only as labeled inspiration, not as the primary pattern source.
- Never let the swipe file flatten JT's voice. It supplies evidence of what works; JT's taste supplies the final shape.

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
