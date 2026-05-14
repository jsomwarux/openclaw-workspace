# Viral Post Swipe File — X Research Report — 2026-05-13

## Searches run
Core 6 searches were run with `--sort likes --since 7d --limit 12 --json` and `-is:retweet -is:reply` in query text. Backfill was attempted. X API rejected `--since 14d` because the current endpoint only allows 7-day recent search.

## Query quality
- AI implementation / consulting / audit: LOW_SIGNAL. Mostly 0-like, <100 impression posts. No usable signal.
- n8n / workflow automation: usable post from @The_CoDEFi; remainder mostly low engagement or spammy product/news links.
- Agentforce / Salesforce agent: LOW_SIGNAL. Mostly low-impression event/course posts. No usable signal.
- SMB buyer niches: one relevant Propmodo property-management post, but low engagement. Useful reply target, not signal.
- Claude Code / Claude Skills / AI agents: usable @seelffff Claude Skills artifact post. Repeated Claude Skills/resource mechanic but already logged 2026-05-08.
- App/product distribution: LOW_SIGNAL due to algorithm/connect bait; one useful near-miss reply target from @TheAIAgentRev.
- Adjacent backfill: one usable @brandon operational case-study post; other backfill searches returned 0 after filters.

## Usable posts captured

1. @The_CoDEFi — 4,409 followers
- Engagement: 197 (111 likes + 1 repost + 70 replies + 0 quotes + 14 bookmarks)
- Impressions: 1,471
- Timestamp: 2026-05-10T06:58:20Z
- URL: https://x.com/The_CoDEFi/status/2053369028442202460
- Query: n8n/workflow builders
- Text: Top 12 popular open source AI projects on GitHub. OpenClaw, n8n, Ollama, Langflow, Dify, LangChain...
- Relevance: relevant to JT through OpenClaw + n8n + practical stack framing. Transferable mechanic: bookmarkable resource list with categories.

2. @seelffff — 5,678 followers
- Engagement: 87 (44 likes + 0 reposts + 3 replies + 0 quotes + 40 bookmarks)
- Impressions: 3,161
- Timestamp: 2026-05-07T20:18:46Z
- URL: https://x.com/seelffff/status/2052483300053467606
- Query: Claude Code / Claude Skills / AI agents
- Text: a principal consultant published claude-skills, 66 specialized skills for full-stack development, one command to install...
- Relevance: relevant to JT's skill/freshness-gated agent workflow. Transferable mechanic: specific artifact + count + install command.

3. @brandon — 27,350 followers
- Engagement: 37 (24 likes + 2 reposts + 6 replies + 1 quote + 4 bookmarks)
- Impressions: 2,809
- Timestamp: 2026-05-06T13:46:39Z
- URL: https://x.com/brandon/status/2052022232952500528
- Query: adjacent hours-saved backfill
- Text: Zoot raised $6M; CEO shares why they consolidated treasury and crypto operations onto Meow and how it saves hours per week.
- Relevance: relevant as operational consolidation case study. Transferable mechanic: customer milestone plus hours-saved proof.

4. @propmodo — 10,659 followers
- Engagement: 1 (bookmark only)
- Impressions: 63
- Timestamp: 2026-05-13T00:29:01Z
- URL: https://x.com/propmodo/status/2054358217187025349
- Query: SMB/property management profile follow-up
- Text: Property management is undergoing digital transformation, embracing AI/data tools while struggling to bridge insight and action.
- Relevance: strong topical fit for JT's property/family-office lane, but low engagement. Use for replies, not content signal.

5. @TheAIAgentRev — 514 followers
- Engagement: 7 (4 likes + 3 replies)
- Impressions: 72
- Timestamp: 2026-05-13T06:55:14Z
- URL: https://x.com/TheAIAgentRev/status/2054455409629413794
- Query: app/product distribution
- Text: thinking about first 100 users for SaaS; cold DMs not working, building in public slow, SEO takes forever; asks what worked.
- Relevance: useful to JT's app/product distribution lane. Near-miss on follower threshold; included as reply target only.

## Signal analysis

FORMAT signals:
- Resource/artifact roundup appeared again via @The_CoDEFi and @seelffff, but this was already logged on 2026-05-08 as Resource roundup / Claude Skills resource packs. Not a first-time signal. No new content-signals.md append.

TOPIC signals:
- Claude Skills/resource packs: active but already covered recently.
- n8n/open-source automation stacks: one strong post, not enough independent posts above threshold.
- Property-management AI: relevant, but no engagement threshold.
- Agentforce: LOW_SIGNAL this run.

MECHANIC signals:
- Bookmarkable concrete artifacts remain useful: list of tools, count, install command, specific customer outcome. Transferable to JT, but not new enough to log again.

NO_STRONG_SIGNAL

## Swipe update
RECENT_SWIPE_GAP: Notion push attempted for 3 qualifying examples (@The_CoDEFi, @seelffff, @brandon), but blocked because NOTION_TOKEN / NOTION_API_KEY is not available in the runtime environment. Niche gaps with few recent examples: Agentforce, NYC SMB/property management, construction, wholesale distribution.

## Format draft trigger
Skipped. No new first-time FORMAT signal was logged this run.
