# Content Generation Rules
> Source: AGENTS.md §Content Generation Rule
> Governs all X posts, threads, and LinkedIn content for JT.

## Pre-Draft Checklist (mandatory)
Before drafting ANY post or content for JT:
1. Read `memory/content-voice.md` in full.
2. Read `memory/content/jt-voice-profile.md` and `memory/content/jt-voice-evidence-corpus.md` for actual JT cadence, phrasing, rhythm, specificity, proof rules, and hard-fail patterns.
3. Read `memory/content/current-niche-map.md`. Choose the exact platform, niche, and format from that priority map before fetching references. Platform/niche fit matters more than raw engagement.
4. Fetch current swipe-file references using the narrowest relevant filters available: platform first, then niche, then format. Example: `python3 scripts/notion-swipe-fetch.py --platform X --niche "Dynasty Fantasy / Sports GM" --limit 12 --min-engagement 0` or `python3 scripts/notion-swipe-fetch.py --platform LinkedIn --niche "SMB AI Implementation" --format "Case Study" --limit 8`.
5. Never use cross-platform or cross-niche references by default. LinkedIn consulting content must not use dynasty X hooks/context. Dynasty X content must not use LinkedIn consulting patterns. Adjacent references are allowed only when same platform+niche examples are insufficient, and the draft must explicitly label them as adjacent inspiration.
6. Select 2-4 reference patterns that match the platform + niche + format. Extract the mechanic: hook shape, opening-line move, emotional tension, context, rhythm, reply trigger, proof mechanism, specificity level, CTA type, and why it worked.
7. Write a `Pattern inputs / Hook mappings from swipe file` section in the draft file before the posts.
8. Translate the mechanics through JT's voice. Do not copy wording, claims, account persona, or structure wholesale.
9. Run the audit checklist at the bottom of `memory/content-voice.md` on every draft before delivering, except where the retired 5:1 ratio conflicts with the first-person-proof rule below.
10. For every serious saved draft, run `python3 scripts/jt_voice_guard.py [draft-file] --platform linkedin|x`. Rewrite until score is 80+ and no hard-fail problems remain.
11. For every LinkedIn draft, run the executable stale-pattern guard before delivery: `python3 scripts/content_distribution_guard.py --linkedin-draft [draft-file]`. If it fails, rewrite before showing JT.
12. AI Ops Teardown Drive hygiene: top-level `Eve — Drafts / Content / LinkedIn / AI Ops Teardowns` must contain one canonical doc per teardown plus `Archive/`. Prep packs, delivery bundles, superseded drafts, and weekly batches must not sit beside canonical teardowns. If local copy changes after upload, update the existing Google Doc body or create a new canonical doc and archive stale copies.
13. AI Ops Teardown purpose: each teardown must start from a current company, funding, product, market, regulation, or buyer-problem signal in a JT-relevant niche, then show the optimal AI workflow JT would build for that company/problem. Generic "AI ops" advice, repeated approval-queue content, or evergreen workflow tips are not valid teardowns unless tied to a new current signal and distinct workflow. The preferred shape is current signal → buyer-recognizable bottleneck → concrete messy input scene → system-of-record need → workflow JT would build → clean operating outcome. Name the company/signal when public and relevant, but frame carefully: no client implication, no internal-access claim, no fake metric. Previous AI Ops Teardown companies are exclusion-only context and must never be mentioned in the new teardown post. Public value should be a partial blueprint with workflow shape, business logic, approval boundary, and outcome; paid value stays protected by withholding node stack, prompts, schemas, thresholds, vendor choices, and proprietary routing logic.

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
- Priority niches are defined in `memory/content/current-niche-map.md`. Do not replace that map with a narrow product/tool list. Default LinkedIn content should bias toward Tier 1 consulting/proof niches and Tier 2 authority/career niches before product lanes.
- If a niche/platform has fewer than 3 usable recent examples, create a Mission Control task to collect more examples instead of pretending the swipe file is sufficient. For LinkedIn consulting generation, do not call the system optimized until the corpus has at least 5 niche-relevant creator/account sources and 30 recent or evergreen high-performing posts scored for mechanics. Until then, use adjacent references only as labeled inspiration, not as the primary pattern source.
- Never let the swipe file flatten JT's voice. It supplies evidence of what works; JT's taste supplies the final shape.

## Reference Mechanics Contract
Any recurring content generator that claims it used swipe/native references must save a platform-specific reference section in the artifact before delivery.

For @jts_14 X content, the weekly artifact must also have a dedicated source-to-draft ledger, or a linked ledger file, that separates:
- `Topic selection`: source directly influenced what the post was about.
- `Structure`: source influenced hook shape, pacing, format, or compression.
- `Credibility/proof`: source validated artifact-first proof, visible systems, or stack detail.
- `Niche signal only`: source showed market/buyer language but was not strong enough to anchor a post.
- `Rejected`: source was reviewed and intentionally not used.

Minimum row contract: `scraped source -> lane -> why selected -> analyzed mechanic -> influence type -> draft touched -> rejection/constraint if not used`. Run `python3 scripts/jts14_x_reference_ledger_guard.py memory/content/jts14-x-reference-ledger-[MONDAY].md` before claiming @jts_14 X research is optimal.

Required section headings:
- `## LinkedIn Reference Mechanics`
- `## X Reference Mechanics`
- `## Reddit Reference Mechanics`
- `## TikTok Reference Mechanics`

Each section must include at least 2 source rows unless it explicitly marks `RECENT_SWIPE_GAP` or `ADJACENT_REFERENCE_ONLY`. Each row must include:
- `Source URL`
- `Platform`
- `Niche`
- `Format`
- `Hook mechanic`
- `Opening line mechanic`
- `Proof mechanism`
- `Emotional driver`
- `Specificity level`
- `CTA type`
- `Why it worked`
- `JT translation`

Use the narrowest available fetch first:
`python3 scripts/notion-swipe-fetch.py --platform [PLATFORM] --niche "[NICHE]" --format "[FORMAT]" --limit 8 --since-days 30`

If fewer than 3 usable current references exist, label the gap and either use adjacent references explicitly or skip the slot. Do not silently fall back to old all-platform mega posts.
For LinkedIn consulting drafts, raw viral structures must pass through a voice translation layer before generation: convert the winning mechanic into JT's operator voice, add real proof/specificity, remove guru/engagement-bait posture, and prefer concrete workflow detail over generic business outcomes.
The reference section's `Niche` value must exactly match a lane in `memory/content/current-niche-map.md` or explicitly state `ADJACENT_REFERENCE_ONLY` / `RECENT_SWIPE_GAP`. Do not use legacy shorthand like `AI Consulting`, `NYC SMB`, `Claude Code`, `Vista`, `Glow Index`, `Nash Satoshi`, or `App Marketing` as the saved niche value unless the canonical map lane itself uses that exact name.

New weekly LinkedIn/X queues must pass the platform guard, preferably through:
`/Users/jtsomwaru/.openclaw/workspace/scripts/run_content_guard.sh [linkedin|x] [MONDAY]`



## Relevance Ladder + Current Trend Rule
Current efforts are a relevance input, not a cage. Content should choose the strongest available source in this order:
1. Fresh niche/platform trend from the last 7-14 days + JT has an earned angle.
2. Current effort + useful, specific lesson.
3. Fresh proof point/build.
4. Older proof tied to current motion.
5. Evergreen operator truth, sparingly, only if sharp and non-repetitive.

Do not force every post to mention current efforts. Do not use old swipe examples as if they are current. If current swipe references are thin, label older examples as archive patterns and use fresh topic/proof from another source.

## Viral Swipe Quality Rule
Viral Swipe must search live X with explicit recency and performance filters: `--since 7d`, fallback `--since 14d`, `--sort likes`, and minimum engagement thresholds. Broad queries returning spam/hashtag trains/low-impression posts are `LOW_SIGNAL` and must not be logged. Strong outputs capture not only topic/format but mechanic: hook shape, proof style, reply trigger, rhythm, novelty, and audience identity. The swipe file should be refilled with recent qualifying posts; if fewer than 3 recent examples exist in a niche, report `RECENT_SWIPE_GAP` rather than pretending the archive is current.

## Source Freshness Gate for News/Intel Claims
- Any draft that says "this week," "today," "new," "fresh," or implies current market intel must have a source published within the last 14 days, unless the draft explicitly labels it as older background context with the date.
- Before using any stat from `memory/content/weekly-intel-brief.md`, verify the source date via live web or saved citation. If the source date is older than 14 days, remove the freshness framing or cut the stat.
- Weekly intel briefs must include source name + source date for every factual market/stat claim. No anonymous phrases like "one report this week" without a dated source.
- If a source cannot be verified quickly, the draft must use a non-stat, operator-observation angle instead of inventing or laundering the claim.

## Core Voice Rules
- Start with the point, never with setup or preamble
- The old "you/your must outnumber I/my 5:1" rule is retired for JT's core channels. First-person proof is encouraged when it carries a verifiable specific: number, artifact, deployment detail, tool decision, or failure.
- Standalone posts: target 6–15 words
- No forbidden words (full list in content-voice.md)
- No em dashes, no exclamation points, no "Here's the thing:" openers
- All JT content must not use stale contrarian/reveal patterns: no “the blocker is not whether X, it is whether Y,” no “not look what this tool can do, more like…,” no “not X, but Y,” no two-sentence “X is not just Y. It is Z.” framing, and no “matters more than people think” generic importance phrases.
- LinkedIn originality gate: before delivery, compare every slot against the last 45 days of `memory/content/posted-log.jsonl` and the prior week's published/scheduled posts. Block drafts that reuse the same semantic angle, not just the same words. Current hard blocks: “best first AI project / least glamorous,” “handoff everyone checks manually,” “gets risky when...live in different places,” “exception layer,” “autonomous content system,” “state file,” “stop condition,” any public discussion of internal content-generation or publishing machinery, and standalone public-proof/privacy-cleanup posts.
- Worthiness gate: a draft must improve JT's position with a buyer, recruiter, or builder. Internal hygiene work like removing client names, cleaning site proof, hiding private details, attribution cleanup, or "proof needs privacy" is not post-worthy unless attached to a real buyer problem, shipped client outcome, or permission-safe case study.
- LinkedIn strategic-fit gate: posts must make JT look like the operator a buyer or hiring manager would trust with implementation. Default to buyer-recognizable workflows, real proof, service-delivery judgment, and business constraints. Do not publish posts about how JT generates, schedules, guards, or automates his own content unless JT explicitly asks for that topic.
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
Anything shipped/done/live → update `memory/content-voice.md` Proof Points immediately (same turn). Add to the `## Proof Points` table using: `Date | Proof Point | Verified Detail | Demonstrates | Status`. Use only verified evidence from recent-builds, proof logs, commits, live checks, or daily notes. No fabricated metrics. Also add to Content-Ready Angles if post hook exists. Skip internal-only builds.

## Recent Builds → Content
Append to `memory/content/recent-builds.md` in the same turn. Required fields: Build Name + date | What | For | Outcome | Demonstrates | Content angle | Status: complete.

## Recap/Proof Regression Gate
After substantive deliverables, site/app ships, client work, cron/agent builds, or proof-point updates, run:
`python3 scripts/log-proof.py --type TYPE --title "..." --description "..." --outcome success|partial --files PATH...` and then `python3 scripts/memory_recap_proof_guard.py --date $(date +%F) --json`.
The guard must pass before marking the work done. If it flags recent-builds entries missing from `content-voice.md` Proof Points, backfill from verified evidence only.

## Technical Angles Bank
`memory/content/technical-angles.md` = source bank for technical X posts.
Append when: non-obvious problem solved, new agent/cron pattern established, "learned this the hard way" moment, or system design decision that practitioners would find useful.
Format: `- **[Pattern name]:** [2–3 sentences, specific enough to apply immediately.]`


## Content Calendar Follow-through Audit
Run after weekly content generation, after any content cron patch, or when Notion/posted-log drift is suspected:
`python3 scripts/content_calendar_audit.py --week YYYY-MM-DD`

Run before delivering any one-off LinkedIn draft:
`python3 scripts/content_distribution_guard.py --linkedin-draft [draft-file]`

Use `--with-notion` only when Notion token is available and external read checks are appropriate.
The audit must pass locally before calling the weekly content system healthy. It checks: weekly file guard, posted-log duplicate slots, content cron guard prompts, posted-reply handler + pending-state writer presence, and optional Notion duplicate/missing Drive links.

Semantic repeat guard: content delivery must also pass the topic-cooldown check in `scripts/content_distribution_guard.py`. It blocks active/future LinkedIn slots that reuse recent semantic clusters from `memory/content/posted-log.jsonl` within 45 days, even when older manual rows are still marked `posted=false`. If it fails, replace/regenerate the slot instead of delivering.

## Posted Reply Logging
When JT replies `posted`, `posted both`, `posted LinkedIn`, `posted X`, or `posted: [url]`, use the deterministic local handler instead of manual/context-only edits:

```bash
cd /Users/jtsomwaru/.openclaw/workspace
python3 scripts/content_posted_reply_handler.py --reply "<JT reply>"
```

Rules:
1. Never mark content posted without JT's explicit `posted` reply or a verified post URL.
2. Use `--dry-run` first if the reply is ambiguous.
3. Platform-specific replies mark only that platform.
4. Content reminder/Sunday delivery flows should write `memory/content/pending-posted-reply.json` after sending posts using `python3 scripts/content_pending_reply_state.py --date YYYY-MM-DD --platform linkedin --platform x --source content-reminder` or exact `--entries-json`.
5. The handler updates `memory/content/posted-log.jsonl`, consumes `memory/content/pending-posted-reply.json` when present, idempotently refuses duplicate mutation, and updates Notion Status to Posted only when exactly one date/platform row matches.
6. Send the handler's confirmation back to JT.
7. When JT replies posted: ask once, "any edits? paste final text if changed." If he pastes final text, diff it against the draft and append `{date, platform, draft_excerpt, final_excerpt, delta_summary}` to `memory/content/edit-deltas.jsonl`. If no edits, log `delta_summary: none`. Never fetch from the X API for this.
8. Full docs: `docs/agents/content-posted-reply-handler.md`.
