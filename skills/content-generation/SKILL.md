---
name: content-generation
description: "Use when drafting, reviewing, scheduling, or generating JT's X, LinkedIn, Reddit, TikTok, or social content, especially when selecting niches, swipe references, hooks, voice, or platform-specific content strategy."
---

# Content Generation Skill
> Unified framework for writing all of JT Somwaru's content (X, LinkedIn).

## Description
Generates zero-fluff, highly compressed, high-leverage content for JT's social channels. Enforces brand voice, platform constraints, and Mamba-level execution against his current niche map (`memory/content/current-niche-map.md`) plus the taste profile (`memory/content/jt-voice-profile.md`), with consulting/proof lanes prioritized above product/app lanes unless the request explicitly asks for app marketing.

## Usage
`openclaw sessions_spawn --agentId [id] --task "Create a LinkedIn case study using the content-generation skill on [Topic]"`
For agents/CRONs: Load this skill before drafting any post.

## Core Directives (Non-Negotiable)
1. **You > I Ratio (5:1):** Talk about the reader's problem, not JT's feelings. Limit "I/My/Me".
2. **Compression is Confidence:** Cut every word that doesn't earn its place. No filler, no adverbs, no emojis unless absolutely necessary for structure.
3. **Uncomfortable Truths:** State facts flatly. E.g., "AI builds aren't expensive — they're cheaper than the humans that would do the same work."
4. **No "Broetry":** Do not use cringe LinkedIn spacing (one sentence per line for 20 lines) unless mocking it.
5. **No Preamble:** Never start with "Here's a thought" or "I was thinking today." Start with the punchline.
6. **No Semantic Repeats:** For LinkedIn, check the last 45 days of posted/scheduled content before drafting. Repeating the same idea with new wording is a failed draft.
7. **No Internal Content Ops:** Do not publish about JT's content generation, publishing system, posted logs, swipe mechanics, state files, or content automation unless JT explicitly asks for that public topic.
8. **AI Ops Teardown Standard:** A teardown must examine a current company or trending operational problem in a JT-relevant niche, then show the optimal AI workflow JT would build for that company/problem. If there is no current signal, named problem, workflow map, approval boundary, and buyer outcome, it is not a teardown. Strong teardowns translate the news into a buyer-recognizable operating bottleneck, show the messy input scene, then explain what the workflow reads, extracts, checks, drafts, routes, and prevents before bad data or unclear ownership hits the system of record.

## Platform Formatting Rules
### X (Twitter)
- **Standalone Posts:** Extreme compression. 6-15 words. Lowercase starting letter for raw/thinking-out-loud vibe.
- **Threads:** Maximum 5 tweets. First tweet is the hook + the payoff. No "A thread 🧵".

### LinkedIn
- **Format:** Professional, outcome-driven, but still compressed.
- **Case Studies:** Problem → AI Solution → Exact ROI (Time/Money saved).
- **Structure:** Bullet points for readability. First line must stop the scroll without being clickbait.

## Execution Steps
1. **Analyze Request:** Determine the platform (X or LinkedIn) and the content type (Hot Take, Case Study, Workflow Teardown). For AI Ops Teardowns, identify the current company/problem signal before drafting.
2. **Load Niche Map:** Read `~/.openclaw/workspace/memory/content/current-niche-map.md`. Pick the exact canonical niche lane before fetching references or drafting. Default LinkedIn lanes are `SMB AI Implementation`, `Property Management Operations`, `NYC SMB Operations`, `Wholesale Distribution Operations`, `Construction + Skilled Trades Operations`, `Insurance / Agentforce Operations`, `AI Operating Systems / Agent Orchestration`, `AI Enablement / Solutions Architecture Career`, and `Productized Services / Solo Operator Systems`.
3. **Load Voice Profile:** Read `~/.openclaw/workspace/memory/content/jt-voice-profile.md`. Use it for taste-level decisions: buyer-scene hooks, rejected patterns, proof-safe ownership, and the pre-send voice gate.
4. **Drafting:** Write the post explicitly applying the Core Directives.
5. **Compression Pass:** Read the draft. Delete 20% of the words. If the meaning changes, you cut the wrong words. If it hits harder, keep going.
6. **Teardown Fit Pass:** For AI Ops Teardowns, reject drafts that read like a news summary or generic AI advice. The post must include: current signal, buyer-recognizable bottleneck, concrete input examples, system-of-record need, workflow start point, extraction/check/routing steps, and a practical outcome that lets customers/operators keep normal behavior while the business gets cleaner handoffs.
7. **Originality Pass:** Compare against `memory/content/posted-log.jsonl` and reject repeated hooks, phrasing, or angles. Current blocked LinkedIn repeats include "best first AI project / least glamorous," "handoff everyone checks manually," "gets risky when...live in different places," "exception layer," "autonomous content system," "state file," "stop condition," and internal content-system transparency.
8. **Output:** Return ONLY the post text. No "Here is your drafted post." Just the text. 

## Data Flow & Integration Guidelines
- **Input Content:** For Monday/Thursday crons, always load `~/.openclaw/workspace/memory/content/weekly-intel-brief.md` for this week's niche signals before drafting any content.
- **Output (Review):** All raw generated X or LinkedIn drafts should be appended to `~/.openclaw/workspace/memory/drafts/` with their dates, OR explicitly pushed to a `Google Drive` link for JT's review and scheduling.
- **Logging Rule:** If JT says "posted," an agent loaded with this skill must immediately update `~/.openclaw/workspace/memory/content/posted-log.jsonl` with `posted: true`.
- **Notion Integration:** Approved posts can be scheduled directly via `python3 ~/.openclaw/workspace/scripts/notion-calendar-push.py`.
