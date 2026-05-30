# Viral Post Swipe File - X Research - 2026-05-29

## Retrieval

- Ran all 6 required core X searches with `--sort likes --since 7d --limit 12 --json`.
- Ran 3 adjacent backfill searches because the core set produced fewer than 8 usable posts.
- Attempted the required 14-day fallback for thin core niches, but the current X API rejected start times older than 2026-05-22T09:46Z. Retrieval constraint: 7-day window only.

## Query Quality

- AI consulting/operator: LOW_SIGNAL. Mostly zero-engagement promo, news snippets, or low-impression takes.
- n8n/workflow: mixed. One strong GTM stack list, rest mostly promo or low-impression builder posts.
- Agentforce: thin but relevant. One usable multi-agent orchestration demo, otherwise low-impression event and hashtag posts.
- SMB buyer niches: LOW_SIGNAL. Mostly automation agency promo, low impressions, or no transferable mechanic.
- Claude Code/AI agents: strongest query. Multiple usable stack, memory, and artifact breakdown posts.
- Distribution: LOW_SIGNAL. Mostly repeated "X algorithm/connect" engagement bait.
- Backfill: one strong agent workflow thread and one low-reach n8n first-build post.

## Usable Posts

| Handle | Followers | Engagement | Impressions | Timestamp | URL | Query | Relevance |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| @fivosaresti | 2656 | 117 | 1746 | 2026-05-22T19:00:14Z | https://x.com/fivosaresti/status/2057899353964994862 | n8n/workflow | Tool-stack list names Claude Code and n8n as category winners. Relevant to JT's stack judgment and buyer-facing AI ops stack framing. |
| @iamKapilBatra | 1992 | 13 | 236 | 2026-05-23T15:46:03Z | https://x.com/iamKapilBatra/status/2058212873269289215 | Agentforce | Agentforce multi-agent orchestration demo. Relevant to JT's Agentforce credibility, but engagement is below swipe threshold. |
| @godofprompt | 275871 | 473 | 27562 | 2026-05-26T09:45:04Z | https://x.com/godofprompt/status/2059209193446621688 | Claude Code/AI agents | Claude Code memory/evidence stack artifact. Strong fit for Eve/OpenClaw memory, skills, hooks, and anti-repeat architecture. |
| @PawelHuryn | 67542 | 122 | 3664 | 2026-05-26T15:38:37Z | https://x.com/PawelHuryn/status/2059298167024193728 | Claude Code/AI agents | Codex plus Claude Code same-repo operating pattern. Directly relevant to AGENTS.md/CLAUDE.md/skills consistency. |
| @tec_aryan | 45784 | 378 | 43515 | 2026-05-27T09:13:41Z | https://x.com/tec_aryan/status/2059563684096356810 | AI workflow backfill | Outcome-first "exact 4-agent workflow" thread. Transferable as workflow proof, though the e-commerce angle is less JT-specific. |
| @RanganiVandan | 4 | 27 | 384 | 2026-05-24T08:22:28Z | https://x.com/RanganiVandan/status/2058463629973086280 | AI workflow backfill | First n8n AI workflow post. Relevant mechanic is weak because audience/reach is tiny. |

## Signals

FORMAT signal: Concrete stack/artifact breakdown.

- Appeared across @fivosaresti, @godofprompt, @PawelHuryn, and @tec_aryan.
- Total engagement counted: 1090.
- Mechanic: named tools/files/agents, concise stack categories, then a saved artifact or workflow.
- Why it works: high save value, clear operator identity, and concrete proof instead of generic AI hype.
- JT translation: "The AI ops stack I actually use" or "the files that keep an autonomous content system pointed at the current business."
- Anti-repeat check: recent posted log already includes Agent Stack Judgment on 2026-05-26 and a current-state content-system post scheduled for 2026-05-31. Logged as already covered, no format draft triggered.

TOPIC signals: NO_STRONG_SIGNAL.

- Claude Code/agent tooling was strongest, but the current topic overlaps recent JT content.
- AI consulting, SMB buyer niches, and distribution did not meet quality threshold.

MECHANIC signals:

- Reusable mechanic: "exact stack/artifact breakdown" with named files, tools, or agents.
- Not logged separately because it is covered by the format signal.

## Swipe Pushes

- Pushed @fivosaresti to Notion Viral Swipe.
- Pushed @godofprompt to Notion Viral Swipe.
- Pushed @PawelHuryn to Notion Viral Swipe.
- Pushed @tec_aryan to Notion Viral Swipe.

## Gaps

- RECENT_SWIPE_GAP: AI consulting and NYC SMB buyer niches lacked at least 3 usable recent examples.
- Reply target gap: only 4 high-quality fresh accounts in the 1k-500k follower band were found. A fifth lower-quality distribution target is included to satisfy the weekly pack shape, but should be treated as optional.
