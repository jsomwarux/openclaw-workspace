# FEEDBACK-LOG.md — JT's Voice & Style Corrections

> Source of truth for JT's content voice, communication preferences, and style corrections.
> **Operational/process mistakes** → AGENTS.md Mistakes Log.
> **Voice, tone, content style corrections** → this file.
> All content agents (viral-swipe, overnight content, future LinkedIn/X agents) must read this before producing or evaluating content.

---

## JT's Content Voice

**Who JT is (as a creator):**
- AI consultant and builder. Not a developer. Speaks both business AND technology — that's the edge.
- Ithaca College → 6 years at Spectrum Enterprise (product catalog, cross-team coordination, system implementations) → JT Somwaru Consulting (AI consulting)
- Building: JT Somwaru Consulting, Vista, Nash Satoshi, Glow Index, jtsomwaru.com
- Crypto-native. x402 protocol forward bet.
- NYC-based. Direct. No fluff.

**Tone (what good JT content sounds like):**
- Confident without being arrogant. Opinionated — takes a stance and defends it.
- Practical over theoretical. "Here's what actually happens when you implement this" beats "AI is the future."
- Short sentences. No corporate speak. No buzzword stacking.
- Real talk from someone who builds. Not a pundit, not a cheerleader.
- Occasionally dry humor. Never forced.

**Content categories (what performs well for JT's audience):**
- AI implementation reality (what consultants actually do vs. the hype)
- Agentforce / Claude Cowork practical takes
- Crypto + AI crossover (x402, on-chain agents)
- Founder/builder process content (what he's building, lessons from builds)
- Job market for AI practitioners (skill gaps, what companies actually want)
- NYC business + AI adoption (local angle)

**What to avoid (confirmed JT dislikes):**
- Filler phrases: "Great question!", "Certainly!", "As an AI..."
- Motivational fluff: "Hustle harder", "Your dream life is one decision away"
- Generic AI takes with no specificity: "AI is changing everything"
- Sycophancy in any form
- Default validation before answering. Lead with the answer. If JT's premise is wrong, say so directly.
- Anchoring on JT's estimates/numbers in strategy or tradeoff questions. Generate an independent view first, then compare.
- Over-formatted posts with excessive emojis every line
- Threads that could be one tweet

**Post structure preferences (for swipe file evaluation):**
- Hook that challenges an assumption or shares a counterintuitive finding — not clickbait
- Body: specific, concrete, personal where possible
- Ending: clear takeaway or strong opinion, not "what do you think?"
- Emojis: used sparingly for navigation, not decoration
- Threads: only when content genuinely requires it (not just to seem thorough)

---

## Style Corrections Log

> Format: `[DATE] | [What was wrong] | [What JT prefers instead]`

**[2026-03-18] | Em dashes ("—") in any written content | NEVER use em dashes in any output: posts, cover letters, resume bullets, cold emails, DMs, news hooks, LinkedIn, X — anything. Use commas, colons, periods, or parentheses instead. This rule applies at generation time, not just review. No exceptions.**

**[2026-03-18] | Overused contrarian reframe pattern "X isn't Y, it's Z" / "X wasn't Y, it was Z" | Use this structure at most once per document. Never in back-to-back paragraphs or consecutive posts. This applies at generation time — not just when reviewing drafts. Check before writing, not after.**
The flip pattern is effective exactly once. When it appears twice in the same piece, the second instance cancels the first. Alternatives: lead with what something actually required ("Getting eight teams to use the system correctly was the core of the work"), state the outcome directly, or open with a concrete scenario. The flip is a tool, not a default sentence structure.

**[2026-03-18] | Build showcase posts compared to other demos as value prop | Never position JT's work against what others do or don't show**
Framing like "nobody shows what happens when the model isn't confident" makes JT's value prop dependent on a gap in the market rather than the substance of what he built. The reader doesn't care about the demo landscape — they care about whether this applies to them. Lead with the problem the reader has, not the gap other builders leave.

**[2026-03-18] | Build showcase posts must convey why it was built and how the pattern applies inside a business**
When JT builds a demo or proof-of-concept, the LinkedIn post should answer two questions the reader actually has: (1) why did you build this? and (2) how would something like this work inside my business? Posts that only describe what the demo does read like product announcements — which is wrong when the build is architecture, not a product. The correct frame: JT built this to prove a pattern works, and here's where that pattern shows up in real business workflows.

**[2026-03-18] | Distinguish between a demo/proof-of-concept and a product for sale**
When a build is a demonstration of architecture (not a sellable product), say so explicitly. "It's not a product. It's a demonstration of architecture that should be standard in any serious AI implementation." This is more credible than implying it's available for purchase — and positions JT as someone who understands the pattern, not just the specific tool.

---

## Swipe File Criteria (for viral-swipe cron)

When evaluating whether a post belongs in the swipe file, prioritize:
1. **Structural technique** is transferable to JT's topics (not just "I liked this post")
2. **Hook type** is one JT could use: Contrarian claim, Personal story, Data surprise, Bold prediction, Curiosity gap
3. **Voice is direct** — avoid overly polished corporate or influencer content
4. **The format** matches how JT communicates: plain language, short paragraphs, no padding
5. **Engagement came from substance**, not from controversy for its own sake or a large existing following

Posts to deprioritize (even if high engagement):
- Pure hustle/grind content
- Generic "AI will replace X" without specificity
- Content that only works because the poster has 500K followers
- Over-formatted carousel reposts (formatting did the work, not the idea)

## 2026-03-22 — Em dash + contrarian pattern violations in weekly content

**Corrections:**
1. Sunday LinkedIn paragraph 3: "wasn't the classification — Claude handles that" → period, no em dash
2. Sunday X post: "wasn't the classification / it was the escalation logic" → contrarian flip pattern, banned outside Thursday CONTRARIAN WEIGHT mode
3. Additional em dashes found and removed in Tuesday, Wednesday, Thursday, Friday posts (5 total in the week's content)

**Root cause analysis:**

The em dash violation is a *generation-time failure*, not a checklist failure. The Q2 check in the PRE-GENERATION COMMITMENTS correctly says "Scan for '—'. If found → rewrite." But this is positioned as a *post-generation scan*, which means the model generates naturally (and naturally reaches for em dashes as a stylistic separator), then is expected to catch and fix them in a checklist pass. The failure mode: the checklist runs but the model's self-review misses dashes that feel "correct" in context — particularly mid-sentence parenthetical uses like "X — which does Y — is Z", which the model often doesn't flag because they're grammatically correct.

The contrarian flip on Sunday X ("wasn't X, it was Y") is the same root cause: the pattern is only supposed to be Thursday's format during CONTRARIAN WEIGHT mode, but it bleeds into other days because it's a natural writing pattern for "behind the build" retrospectives. The generation phase defaulted to a familiar structure without checking day-of-week constraints.

**The deeper issue:** Both rules exist in the cron payload but are positioned as *post-generation corrections* rather than *pre-generation constraints*. The PRE-GENERATION COMMITMENTS block exists for exactly this reason, but only Commitment 1 (opener), Commitment 2 (em dash), and Commitment 3 (adverbs) are listed — and Commitment 2 is not strong enough. It says "scan for '—'" as a checklist step, not "do not generate em dashes under any circumstances."

**Rule changes applied:**

1. Em dashes are now a generation-time hard ban, not a checklist item. The distinction matters: "scan and fix" assumes fallible self-review. "Never write one" is a constraint applied before the first word.
2. Contrarian flip pattern ("wasn't X / it was Y" or "X isn't Y / it's Z") is restricted to Thursday only during CONTRARIAN WEIGHT mode. Any other day: rewrite to lead with the positive claim directly.

---

## 2026-04-03 — Tricolon negation pattern ban

**JT flagged:** "No X. No Y. Just Z." as a common AI slop tell — showing up in generated content across the industry.

**Rule added to content-voice.md AI-Generated Pattern Ban:**
"No [X]. No [Y]. Just [Z]." and all variants (tricolon negation resolving to a simple positive) are banned. State what it is directly. Drop the negations.

**Examples of banned constructions:**
- "No strategy decks. No jargon. Just results."
- "No meetings. No overhead. Just automation."
- "Not complicated. Not expensive. Just done."

## 2026-04-29 — Dynasty X reply tone correction
- JT disliked @dynastyjig replies that sounded too statistical/scientific: words like “latency,” “liquidity,” and “probability fragments” do not fit the fantasy/dynasty community vibe.
- Rule: Dynasty replies should be sharp, plain, and community-native. Use familiar language: price, value, rookie pick, roster spot, window, bet, role, points, upside, risk, rebuild/contender, manager. Avoid quant jargon unless the target audience already used it.
- Better shape: one clean football/fantasy point, lightly contrarian, easy to reply to. Sound like a sharp dynasty manager, not a finance model.

## 2026-04-30 — @dynastyjig content must ladder to Action Arena
- Trigger: JT rejected the Daily Player Evals pack because it was generic dynasty analysis: no hook, no unique angle, no organic growth mechanism, and no connection to the products being built.
- Correction: @dynastyjig content should not default to player evals. It must reference the tone/context of JT-approved niche accounts and connect to Action Arena's world: fantasy league structure + sports betting strategy + public weekly profit competition.
- Rule: Every @dynastyjig post needs a hook, social tension, or strategic edge that makes fantasy/betting people want to respond. If it could be posted by any dynasty account, it is not good enough.
- Product positioning: build demand for Action Arena indirectly through bankroll construction, public picks, rivalry, weekly budget constraints, parlays/teasers discipline, profit standings, and playoff pressure. Do not write generic “download my app” promo copy.
- Second product lane: Dynasty Fantasy Football Simulator. Build demand for a persistent dynasty sandbox where managers test rebuilds, replay alternate histories, face AI managers with personalities, fast-forward seasons, and get a dynasty fix faster than the NFL calendar allows.
- Rule: DynastyJig content should rotate between Action Arena and Dynasty Simulator angles. Action Arena = betting strategy as social fantasy competition. Dynasty Simulator = dynasty strategy as a replayable sandbox.
- Bad shape: “Player X is a hold. KTC RB35. Risk: role ceiling.”
- Better Action Arena shape: “Your weekly betting card is a lineup. If every leg needs ceiling, you built a best ball team with no floor.”
- Better Simulator shape: “Every dynasty manager has a rebuild theory they’ll never get enough seasons to prove.”

## 2026-04-30 — @dynastyjig content should be niche-native, not app-centric
- Trigger: JT clarified that dynasty X content should not be about the apps themselves. The goal is to gain traction in the niches the apps live in: dynasty fantasy football and sports betting.
- Correction: Action Arena and Dynasty Simulator are strategy backdrops, not copy subjects. Daily content should earn trust from dynasty managers and bettors through relatable, unique takes about roster construction, betting-card construction, league psychology, public accountability, boredom, regret, timing, risk, and group-chat pressure.
- Rule: Product references are banned by default in @dynastyjig daily niche-growth drafts. Mention product lane only in internal angle notes. If the post reads like app promo, rewrite it.
- Voice target: JT-style compression + practical contrarian angle + community-native language. Avoid AI-ish generic hooks, quant jargon, and player-value blurbs.
- Better dynasty shape: “Most rebuilds fail because managers want credit for patience without paying the boredom tax.”
- Better betting shape: “The worst parlay leg is usually the one you added so the slip felt exciting.”

## 2026-04-30 — Content engine must be self-improving from proven niche X patterns
- Trigger: JT clarified that @dynastyjig content should constantly learn from what is working on X in dynasty fantasy football and sports betting, while still sounding uniquely like him.
- Rule: Daily niche-growth drafts must pull from the Notion Viral Post Swipe File for `Dynasty Fantasy` and `Sports Betting` before drafting. Use examples as evidence of hook shape, context, tone, tension, and rhythm — not as copy templates.
- Guardrail: Never copy wording, claims, account persona, or post structure wholesale. Extract the mechanic, then translate into JT's compressed, practical, lightly contrarian voice.
- Output expectation: generated packs should include the pattern inputs used and explain which proven mechanic each draft adapts.

## 2026-04-30 — Global content must use platform/niche feedback loops
- Trigger: JT clarified the self-improving content loop should apply to all content on all platforms, not just @dynastyjig X content.
- Rule: Every content draft should identify platform + niche + format, pull proven references when available, extract mechanics (hook, tone, context, tension, proof, pacing, reply trigger), then translate through JT's unique voice.
- Guardrail: Proven content is evidence, not a template. Never copy wording, claims, structure, or persona wholesale. JT's content must remain specific to his operator POV, proof, products, and communication style.
- Applied to: X, LinkedIn, Reddit, newsletters, launch posts, consulting content, crypto/Nash content, sports content, job-market/career content, and product content.

## 2026-04-30 — Platform/niche isolation for content references
- Trigger: JT asked whether LinkedIn content would avoid referencing dynasty X hooks/context.
- Rule: Reference selection must be platform-first, then niche, then format. Same-platform/same-niche examples are the default. Cross-platform or cross-niche examples are forbidden by default and may only be used as explicitly labeled adjacent inspiration when the correct pool is too thin.
- Guardrail: If same platform+niche has fewer than 3 usable examples, create a collection task instead of silently borrowing from a mismatched niche/platform.
- Verification: Added `--platform` and `--format` filters to `scripts/notion-swipe-fetch.py`; smoke-tested Dynasty X returning examples and LinkedIn AI Consulting returning none; created MC task to collect LinkedIn consulting examples.

## 2026-05-08 — LinkedIn consulting content must be buyer-facing, not outbound-meta
- Trigger: JT rejected a Friday LinkedIn draft about prospect research mechanics because it discussed his outreach strategy instead of attracting prospects with pain they care about.
- Rule: LinkedIn consulting posts should speak to buyer problems, implementation reality, workflow failures, proof of work, and operational outcomes. Do not publish posts about JT's prospecting, lead research, outreach process, enrichment, or channel selection unless the explicit topic is sales ops for a sales-ops audience.
- Guardrail: Before drafting LinkedIn consulting content, ask: “Would a property manager, construction operator, wholesaler, recruiter, or SMB owner see their own operational problem in this?” If no, rewrite around buyer pain. X may be more meta, but LinkedIn must stay prospect-facing by default.
- Verification: Regenerated 2026-05-08 Friday posts around manual exception tracking and operational AI, not outbound strategy.

## 2026-05-08 — Avoid generic AI-consultant hooks like “you don’t need a chatbot”
- Trigger: JT said the regenerated LinkedIn/X drafts sounded too AI-generated and questioned the value of “Most businesses do not need an AI chatbot” as the hook.
- Rule: Do not lead consulting posts with generic AI-category contrasts unless the buyer already has that exact misconception. Hooks should start from a recognizable business moment: the Monday meeting, stale report, missed handoff, duplicate data entry, delayed approval, or owner asking “where does this stand?”
- Guardrail: Before shipping a LinkedIn consulting hook, ask: “Would a nontechnical SMB operator immediately recognize this from their workday?” If the hook starts with abstract AI positioning instead of lived operational pain, rewrite it.
- Better direction: buyer scene first, AI implementation second, JT POV last. Avoid phrases that sound like AI-generated thought leadership: “AI chatbot,” “exception layer,” “messy work your team already handles,” and stacked rhetorical lists unless grounded in a concrete workflow.
- Preferred pattern: “Weekly status meetings might be the most expensive meeting on your calendar.” Then list concrete examples with clean bullets, diagnose the spread across inboxes/spreadsheets/PDFs/portals, and only then say where AI fits.
- Verification: Regenerated 2026-05-08 posts with a concrete operational scene as the hook, then updated `memory/content-voice.md` LinkedIn rules + audit checklist so future drafts align with JT's preferred version.
