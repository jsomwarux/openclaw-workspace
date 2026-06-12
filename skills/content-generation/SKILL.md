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
1. **First-Person Proof Over Advice Voice:** The old "you/your must outnumber I/my 5:1" rule is retired for JT's core channels. Every serious post should contain at least one verifiable first-person specific: a number, artifact name, deployment detail, named tool decision, or failure.
2. **Compression is Confidence:** Cut every word that doesn't earn its place. No filler, no empty adverbs or generic intensifiers, no emojis unless absolutely necessary for structure. Keep practical qualifiers when they carry JT's judgment, like "probably," "largely," or "pretty" in a real caveat.
3. **Uncomfortable Truths:** State facts flatly. E.g., "AI builds aren't expensive — they're cheaper than the humans that would do the same work."
4. **No "Broetry":** Do not use cringe LinkedIn spacing (one sentence per line for 20 lines) unless mocking it.
5. **No Preamble:** Never start with "Here's a thought" or "I was thinking today." Start with the punchline.
6. **No Semantic Repeats:** For LinkedIn, check the last 45 days of posted/scheduled content before drafting. Repeating the same idea with new wording is a failed draft.
7. **No Internal Content Ops:** Do not publish about JT's content generation, publishing system, posted logs, swipe mechanics, state files, or content automation unless JT explicitly asks for that public topic.
8. **No Proof-Hygiene Standalone Posts:** Removing client names, cleaning public proof, hiding private details, fixing attribution, or saying "proof needs privacy" is internal discipline, not a post-worthy idea by itself. Use it only as support inside a real buyer problem, shipped outcome, or permission-safe case study.
9. **AI Ops Teardown Standard:** A teardown must examine a current company or trending operational problem in a JT-relevant niche, then show the optimal AI workflow JT would build for that company/problem. If there is no current signal, named problem, workflow map, approval boundary, and buyer outcome, it is not a teardown. Strong teardowns translate the news into a buyer-recognizable operating bottleneck, show the messy input scene, then explain what the workflow reads, extracts, checks, drafts, routes, and prevents before bad data or unclear ownership hits the system of record.
10. **Build Proof + Consultant POV Balance:** Generated content should balance things JT is building or uniquely incorporating during builds with consultant-perspective analysis of focused niches and buyer problems. The goal is to make JT attractive to potential clients/employers through proof of execution and proof of diagnostic judgment. Do not drift into pure build diary or generic consultant commentary.
11. **No Polished X Guru Compression:** For X, do not use staged trust hooks, dramatic one-word workflow noun stacks, "the useful question is uglier," "probably a margin leak," build-list flex CTAs, automation/chaos contrast lines, or "that's not automation, that's leverage." Keep X sharper and rawer: one concrete observation, build fact, or operational judgment.
12. **No Too-Casual LinkedIn:** For LinkedIn, remove anything that would not make a potential client or employer trust JT more. No "quick update," "small win," "built this weekend," "been playing with," "nothing crazy," "pretty cool," vibes/slang, tool fandom, app-growth chatter, or build diary unless rewritten into buyer problem, proof, outcome, deployment constraint, approval boundary, or career-relevant systems judgment.
13. **No Old Template Slogans:** Do not use reusable creator-framework lines like "The tools exist. The implementation doesn't," "Agents handle the work," "Build the process. Buy back the time," "Demo proves it's possible. Deploy proves it's real," or "Chatbots answer questions. Agents close tickets." Rewrite around the actual input, source, owner, approval, metric, deployment constraint, or buyer scene.
14. **Stop Slop Delta Guard:** Do not import generic anti-AI-writing rules wholesale. Use the local guard to catch the useful enforceable gaps: false agency where data/workflows/markets act like people, narrator-from-distance lecturer phrasing, vague declaratives, Wh-opener setups, pull-quote endings, and high-confidence passive voice. Rewrite by naming the actor, owner, input, queue, approval boundary, or concrete consequence.
15. **LinkedIn Proof Density:** Treat LinkedIn as a trust and pipeline surface, not an opinion surface. Serious LinkedIn posts should carry at least two proof assets: concrete workflow input, system of record, human approval boundary, deployment constraint, before/after metric, safe artifact/screenshot, client/operator scene, or an implementation decision a generic AI writer would not know. Reject virality-first funnel advice unless it strengthens qualified buyer trust.

## Platform Formatting Rules
### X (Twitter)
- **Standalone Posts:** Extreme compression. Roughly 6-25 words, with shorter preferred when the point still lands. Lowercase starting letter is allowed for raw/thinking-out-loud X posts.
- **Threads:** Maximum 5 tweets. First tweet is the hook + the payoff. No "A thread 🧵".

### LinkedIn
- **Format:** Professional, outcome-driven, but still compressed.
- **Case Studies:** Problem → AI Solution → Exact ROI (Time/Money saved).
- **Structure:** Bullet points for readability. First line must stop the scroll without being clickbait.

## Execution Steps
1. **Analyze Request:** Determine the platform (X or LinkedIn) and the content type (Hot Take, Case Study, Workflow Teardown). For AI Ops Teardowns, identify the current company/problem signal before drafting.
2. **Load Niche Map:** Read `~/.openclaw/workspace/memory/content/current-niche-map.md`. Pick the exact canonical niche lane before fetching references or drafting. Default LinkedIn lanes are `SMB AI Implementation`, `Property Management Operations`, `NYC SMB Operations`, `Wholesale Distribution Operations`, `Construction + Skilled Trades Operations`, `Insurance / Agentforce Operations`, `AI Operating Systems / Agent Orchestration`, `AI Enablement / Solutions Architecture Career`, and `Productized Services / Solo Operator Systems`.
3. **Load Voice Profile:** Read `~/.openclaw/workspace/memory/content/jt-voice-profile.md` and `~/.openclaw/workspace/memory/content/jt-voice-evidence-corpus.md`. Use them for taste-level decisions: buyer-scene hooks, actual JT cadence, rejected patterns, proof-safe ownership, specificity, and the pre-send voice gate.
4. **Drafting:** Write the post explicitly applying the Core Directives.
   - Choose the lane deliberately: `Build Proof`, `Buyer Problem POV`, or `Bridge`.
   - `Build Proof` posts need a real implementation detail and the buyer-facing lesson it proves.
   - `Buyer Problem POV` posts need a focused niche, buyer-recognizable scene, and solution shape JT would actually build.
   - `Bridge` posts are preferred when available: build detail -> niche implication -> workflow/approval/source-of-truth lesson.
   - LinkedIn posts must pass the client/employer trust test: a buyer, recruiter, or hiring manager should see proof of execution or proof of judgment, not just that JT was tinkering.
   - Recurring LinkedIn/X generators must use `memory/jt-corpus.md` as the primary voice source and inline five format-matched exemplars before drafting. Swipe references supply topic and hook mechanics only.
   - If the post is meant to drive pipeline, include the conversion layer it points to: lead magnet, checklist, diagnostic, reply path, Drive/Notion artifact, email capture, call-prep asset, or next-step offer. Do not chase comments/impressions without a buyer-readable asset behind the post. Current canonical asset path for the property-management checklist is `memory/content/assets/property-management-ai-workflow-readiness-checklist.md`.
5. **Compression Pass:** Read the draft. Delete 20% of the words. If the meaning changes, you cut the wrong words. If it hits harder, keep going.
6. **Teardown Fit Pass:** For AI Ops Teardowns, reject drafts that read like a news summary or generic AI advice. The post must include: current signal, buyer-recognizable bottleneck, concrete input examples, system-of-record need, workflow start point, extraction/check/routing steps, and a practical outcome that lets customers/operators keep normal behavior while the business gets cleaner handoffs.
7. **Originality + Worthiness Pass:** Compare against `memory/content/posted-log.jsonl` and reject repeated hooks, phrasing, or angles. Current blocked LinkedIn repeats include "best first AI project / least glamorous," "handoff everyone checks manually," "gets risky when...live in different places," "exception layer," "autonomous content system," "state file," "stop condition," internal content-system transparency, and public-proof/privacy cleanup as standalone content. Also reject drafts that are merely true but do not improve JT's buyer, recruiter, or builder positioning.
8. **Voice Guard:** For saved serious drafts, run `python3 scripts/jt_voice_guard.py [draft-file] --platform linkedin|x` and rewrite until the score is 80+ with no listed problems. The guard fails on any problem line; do not treat "soft" voice issues as optional unless JT explicitly asks for that phrasing.
9. **Output:** Return ONLY the post text. No "Here is your drafted post." Just the text.

## Data Flow & Integration Guidelines
- **Input Content:** For Monday/Thursday crons, always load `~/.openclaw/workspace/memory/content/weekly-intel-brief.md` for this week's niche signals before drafting any content.
- **@jts_14 X Reference Ledger:** Weekly @jts_14 X generation must write or update `~/.openclaw/workspace/memory/content/jts14-x-reference-ledger-[MONDAY].md`. Each saved source needs: source URL, canonical niche lane, why selected, analyzed mechanic, influence type (`Topic selection`, `Structure`, `Credibility/proof`, `Niche signal only`, `Rejected`, or `Constraint`), and which draft it touched. Run `python3 scripts/jts14_x_reference_ledger_guard.py memory/content/jts14-x-reference-ledger-[MONDAY].md` before calling the X content system healthy.
- **Output (Review):** All raw generated X or LinkedIn drafts should be appended to `~/.openclaw/workspace/memory/drafts/` with their dates, OR explicitly pushed to a `Google Drive` link for JT's review and scheduling.
- **Logging Rule:** If JT says "posted," an agent loaded with this skill must immediately update `~/.openclaw/workspace/memory/content/posted-log.jsonl` with `posted: true`.
- **Notion Integration:** Approved posts can be scheduled directly via `python3 ~/.openclaw/workspace/scripts/notion-calendar-push.py`.
