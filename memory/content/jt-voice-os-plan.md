# JT Voice OS Plan

Date: 2026-06-02

Purpose: improve AI-generated content so it sounds like JT while still learning from what works on X and LinkedIn.

## Core Decision

Do not build a giant generic "voice profile" in isolation. Build a compact Voice OS with five layers:

1. **JT examples:** real posts, messages, rewrites, and corrections.
2. **Taste interview:** decision rules that explain why JT likes or rejects a draft.
3. **Existing rules:** banned phrases, usage rules, platform rules, and content constraints already in `memory/content-voice.md`, `memory/FEEDBACK-LOG.md`, `docs/agents/content-rules.md`, and `skills/content-generation/SKILL.md`.
4. **Good/bad pairs:** targeted examples only for rules that are subjective or repeatedly fail.
5. **Evaluation loop:** generate, compare, score, revise, and update the profile from JT's corrections.

The goal is not "AI writes like JT perfectly." The goal is fewer drafts that feel like generic AI, faster editing, and a reusable correction loop.

## Step 1: Example Collection

Optimal collection mix:

- **Tier 1: JT-written public posts.** Best source for published content voice. Use X posts, LinkedIn posts, and any captions JT wrote himself. Prioritize posts JT still likes.
- **Tier 2: JT-approved edits.** Best source for taste. Use "before Eve/AI draft" and "after JT rewrite" pairs whenever possible.
- **Tier 3: messages to Eve/OpenClaw.** Useful for natural cadence, bluntness, decision style, and phrase patterns. Use as voice reference, not as public-topic material.
- **Tier 4: private text messages.** Optional and only if JT explicitly provides them. Useful for rhythm and personality, but should be scrubbed for names/private context and never used as factual content.
- **Tier 5: external successful posts.** Use only for mechanics: hook shape, pacing, tension, specificity, proof, reply trigger. Never copy persona, wording, claims, or structure wholesale.

Collection target:

- 20 JT-written X posts.
- 10 JT-written LinkedIn posts.
- 10 JT-approved rewrites or rejected draft corrections.
- 20 short natural messages from JT to Eve or elsewhere that capture cadence.
- 10 outside examples from successful X/LinkedIn posts in the exact platform+niche lane.

JT can provide examples manually, or Eve can mine existing local corpora first. User-provided examples should be marked:

- `love this`
- `sounds like me`
- `almost right`
- `bad, but common failure`
- `never write like this`

## Step 2: Taste Interview

The interview should not ask vague questions like "what is your tone?" It should extract decisions.

Optimal questions:

1. What is a post you wrote that still sounds most like you, and why?
2. What is a generated post that annoyed you, and what exactly felt fake?
3. When should your content be blunt versus explanatory?
4. When is "I built this" the right opener, and when should the buyer's pain come first?
5. What topics make you sound credible because of your actual background?
6. What topics make you sound like a generic AI consultant?
7. What is the difference between a good contrarian take and AI slop contrarian framing?
8. What words or sentence shapes feel like you?
9. What words or sentence shapes make you cringe immediately?
10. What is too polished for X?
11. What is too casual for LinkedIn?
12. What should never be public even if it is interesting internally?
13. What should a reader feel after reading your best LinkedIn post?
14. What should a reader feel after reading your best X post?
15. What does "specific enough" mean in your voice?
16. What is one post from another creator you respect structurally but would never want to sound like?

Output should be decision rules, not a transcript.

## Step 3: Existing Rule Inventory

Yes, much of Step 3 already exists.

Already configured:

- platform split for X vs LinkedIn
- banned phrases
- no em dashes
- no hashtags
- no generic AI consultant hooks
- no "X is not Y, it is Z" reveal pattern
- no tricolon negation
- proof-first client quote tweet rules
- LinkedIn buyer-facing rules
- AI Ops Teardown spine
- originality checks
- platform/niche reference selection
- Notion swipe fetch/reference guard
- posted-log and recent-content checks

Gap:

The current system has many rules, but they are scattered. The Voice OS should not duplicate them. It should add a compact extraction layer:

- `what JT sounds like`
- `why JT rejects drafts`
- `how to choose between competing rules`
- `which examples prove the rule`
- `how to score a draft before JT sees it`

## Step 4: Good/Bad Pair Needs

Good/bad pairs are needed only where rules are subjective or where AI keeps failing.

Priority pairs JT should provide or approve:

1. **Generic AI consultant hook vs JT buyer-scene hook.**
2. **Fake contrarian reframe vs real uncomfortable truth.**
3. **Aphorism that sounds polished but empty vs compressed truth with proof.**
4. **"I built this" proof post done right vs self-centered build update.**
5. **LinkedIn post that is too X-like vs LinkedIn post with enough credibility depth.**
6. **X post that is too LinkedIn-like vs punchy X observation.**
7. **Overexplained implementation take vs tight operator take.**
8. **External successful post mechanic copied badly vs translated into JT voice.**
9. **Internal process reveal that weakens trust vs proof capture that strengthens trust.**
10. **Vague workflow language vs concrete inputs, system, owner, and outcome.**

No need to provide pairs for hard mechanical rules like em dashes, hashtags, forbidden words, or "no DM me" endings. Those are checklist guards.

## Step 5: Voice Evaluation Scorecard

Every serious draft should be scored before JT sees it.

Score out of 100:

- **JT voice fidelity: 25** — sounds like JT, not generic AI.
- **Specificity/proof: 20** — names concrete workflow, number, system, buyer pain, or build detail.
- **Platform fit: 15** — X is punchy; LinkedIn has buyer trust and enough depth.
- **Originality: 15** — not a 45-day semantic repeat or stale phrasing pattern.
- **Business usefulness: 10** — strengthens consulting, hiring, product, or community surface.
- **Mechanic quality: 10** — uses a proven hook/pacing/tension mechanic without copying.
- **Rule compliance: 5** — no banned phrases, em dashes, hashtags, forbidden structures.

Hard fail if:

- It sounds like a generic AI consultant.
- It repeats a recent angle with new words.
- It reveals internal content ops by default.
- It copies another creator's wording/persona.
- It uses a banned structure.
- It makes unverified proof claims.

## Step 6: Proven-Post Integration

Use successful X/LinkedIn posts as pattern evidence, not voice source.

Optimal blend:

1. Select references by platform first, niche second, format third.
2. Extract only the mechanic: hook type, conflict, pacing, proof density, rhythm, reply trigger.
3. Translate through JT's operator POV and proof base.
4. Rewrite into JT's language constraints.
5. Score against the Voice Evaluation Scorecard.
6. Compare against recent JT posts for repetition.

Example:

- External post teaches: start with a buyer-recognizable pain.
- JT translation: use property ops, construction, wholesale, Agentforce, or AI implementation scenes JT actually understands.
- Final draft must sound like JT's specific judgment, not a borrowed creator's cadence.

## Step 7: Feedback Loop

Whenever JT says "this does not sound like me," Eve should log it immediately in `memory/FEEDBACK-LOG.md` with:

- bad phrase or pattern
- why it failed
- preferred replacement
- whether it updates `memory/content-voice.md`
- whether a good/bad pair should be added

Weekly at first, distill repeated corrections into `memory/content-voice.md`. Monthly once stable.

## Step 8: Test Protocol

For one topic, generate:

1. draft without Voice OS
2. draft with current `content-voice.md`
3. draft with Voice OS examples
4. draft with Voice OS examples plus proven-post mechanic

JT picks the winner and explains why. The delta becomes the next rule or pair.

## Saved Next Action

Mission Control task: `j575h8ttyp38dn1z57wfrrpk6d87x6sr`

Next move: collect Tier 1 and Tier 2 examples first. Start with JT-written X/LinkedIn posts and JT-approved rewrites. Do not start by expanding rules. The system already has enough rules; it needs examples, taste decisions, and scoring.
