EVE. SYSTEM REVIEW TASK. Not a post request. One deliverable.

I want constructive criticism of my LinkedIn content system. Be direct. Lead
with what is wrong. Do not open with what works.

WHAT YOU CAN AND CANNOT ASSESS
You have no file access and cannot see rendered images. Everything you need
is pasted below. If a question requires information I have not given you, say
"I cannot assess this without X" and move on. Do not infer, do not estimate,
and do not invent an example to illustrate a point. A named gap is more
useful to me than a guess.

I am three posts in with almost no performance data. Do not tell me which
lane performs best, what the algorithm rewards, or what my engagement rate
should be. You cannot know and neither can I yet. Review the design of the
system, not its results.

THE GOAL
Build a reputation with two audiences: operators and owners at NYC and NJ
property management, real estate, and construction firms who might hire me,
and employers who might hire me for an AI implementation role. The claim I am
making is that I understand their operations, not just my tools.

The primary reader is a non-technical operations manager at a property
management firm. Busy, skeptical of vendors, specifically wary of software
touching payments, legal notices, and tenant records.

WHAT TO REVIEW, in this order

1. NICHE WIDTH. This is the question I most want a real answer on, so argue
   it rather than reassuring me.

   Right now the content is almost entirely NYC and NJ property management
   and real estate operations, while my profile stays broader. The theory is
   that content builds topic authority in one subject while the profile keeps
   me open across verticals.

   What makes this live: my most recently completed engagement was with a
   marketing analytics firm, four weeks, fixed scope, and it went well enough
   that their technical lead said they would work with me again. That work
   has nothing to do with property. Separately, I am in an open negotiation
   for a property-focused venture whose terms are not settled. If it closes,
   narrow is obviously right. If it does not, I will have spent ninety days
   making myself look like a property specialist to every other buyer and
   employer.

   Give me both cases, honestly, at similar length:
   (a) The case that I am too narrow, including specifically what narrowing
       costs me with employers and with non-property buyers, and what a
       stranger reading only my posts would wrongly conclude I cannot do.
   (b) The case that I am not narrow enough, including what specifically gets
       lost when someone posts across four verticals, and why a property
       operator would or would not care that I also do marketing analytics.

   Then commit. Pick one and say which, and name the single strongest
   argument against your own pick. Do not answer "it depends" or "balance
   both." I need a position I can act on.

   If you recommend widening: which lane carries the second vertical, at what
   frequency, and what is the smallest change that achieves it. If you
   recommend staying narrow: what do I do with the non-property proof I
   already have, and where does it live if not in the feed.

2. LANE DESIGN. Four lanes plus an occasional recap lane, definitions pasted
   below. Does this set cover what those two audiences need to see? Is any
   lane redundant, missing, or pointed at the wrong reader? Is the weekly mix
   right?

3. SOURCE STRATEGY. Each lane draws from a fixed source, described in the
   lane definitions. Which lane is most likely to run dry, produce repetitive
   posts, or degrade in quality first, and why?

4. VOICE RULES. My voice skill is pasted below. Which rules are doing real
   work, which are cosmetic, and which are actively producing worse writing?
   Name any rule you would delete.

5. THE PUBLISHED POSTS. Read them as a stranger who found my profile. What do
   they collectively say about me? What would this person conclude I am good
   at? Is that what I want them to conclude?

6. CARD CONTENT MODEL. The five card frames are described below in words. Do
   not comment on visual design, colors, or typography, which you cannot see.
   Assess only whether the five frames carry the right argument in the right
   order, and whether the content rules for each frame produce good copy.

7. HASHTAGS AND TITLES. Strategy pasted below. Assess the logic, not the
   performance.

8. WHAT IS MISSING. What would you add to this system that is not in it? What
   am I not doing that someone building this reputation should be?

FORMAT
For each of the eight, give me: the single biggest problem, why it is a
problem, and the specific change. No more than three points per section. If a
section is genuinely fine, say so in one line and move on rather than
manufacturing criticism.

End with: the three changes you would make first, ranked, with the reason
each is ahead of the others.

--- LANE DEFINITIONS AND HARD RULES ---
## Premise

Never build a post on a premise a competent operator would reject about themselves. Do not
imply the reader is disorganized, has lost documents, does not know their own deadlines, or is
bad at their job. Why: they reject the premise and JT with it.

Premise instead on structural risk, which is true of well-run offices too: what depends on one
person remembering, what fails without announcing itself, what breaks when someone is out, what
stops scaling at portfolio size. These are provable against the reader's own last month.

**Banned as a value proposition:** "saves time on manual work," in any wording. Why: every
vendor says it, it does not differentiate, and it loses to "my person handles it fine."

## The four lanes

### TUESDAY — TEARDOWN — carousel

**Source.** A real, current company, product, funding round, regulation, or market signal,
plus the unpacked `nyc-real-estate-domain` skill at
`~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/`
for accuracy on any industry claim.

**Shape.** Open on the operational failure the signal creates or reveals, in operator language.
Then the signal itself, as support. Then the workflow in 3 to 5 steps, with exactly one step
marked human-approved. Then what stays human. Then one CTA line. Never announce the structure.
Never write "I would build it as N steps."

**Never.** Never claim access to that company. Never invent a metric about them. Never reuse a
company already used in a previous teardown — check `corrections.jsonl` and any prior drafts in
this session before choosing.

**Output.** The card blocks specified under "Card blocks" below, plus a post body.

### WEDNESDAY — OPERATOR LESSON — text only

**Source.** `~/Desktop/proof-engine/lessons.jsonl`, one unused record.

**Shape.** Open on a concrete property or construction operations scenario that illustrates the
rule. Then the rule. Then what JT does now. Then why it matters to someone running an ops team.
Why: the lessons corpus is deliberately stripped of concrete detail, so a lesson stated in its
own terms reads as abstraction.

**The scenario is invented, and has to read that way.**

- Write it as a plainly hypothetical example: "Say a super closes out a work order and the
  system has already moved the unit." Never in the past tense as something that happened, and
  never as a client reference. Why: an invented scene written as history is a fabricated proof
  claim, which is the one thing this skill exists to prevent.
- It must not resemble any client's actual setup, portfolio, or system. Why: a scenario close
  enough to recognize is a client disclosure whether or not it is labeled hypothetical.
- No metrics, no cadences, no headcounts. Why: a number inside an invented scene is
  indistinguishable from a real one, and the reader will assume it is real.
- The scenario illustrates the rule and nothing else. It adds no second lesson, and no detail
  in it may contradict the record.
- The Premise section above governs the scenario: the failure is structural, never the operator
  being careless.

**Selection rules.**
- For the first ten Wednesday posts, use only records where `evidence_tier` is 1.
- Never draw two consecutive Wednesdays from the same `source_skill`.
- Across any rolling five Wednesdays, no more than one may come from `build-verify-attack`.
  Why: it is the largest bucket in the file and will dominate the lane if left unchecked.

**Output.** A post body. Report the record `id` and `source_skill` used.

### THURSDAY — DOMAIN BRIEFING — text, or text plus one card

**Source.** The unpacked `nyc-real-estate-domain` skill, one reference file per post. Rotate
across these eight, in no fixed order. No file may be used twice before all eight have been
used once:

- `~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/references/compliance-calendar.md`
- `~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/references/rent-regulation.md`
- `~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/references/operations-vocabulary.md`
- `~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/references/subsidy-programs.md`
- `~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/references/insurance-coi.md`
- `~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/references/pms-platforms.md`
- `~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/references/market-landscape.md`
- `~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain/references/nj-differences.md`

The unpacked directory is the source of truth. Never read
`~/Desktop/jt-toolkit/consulting-toolkit/skills/nyc-real-estate-domain.skill` — that zip is a build artifact and can be stale.

**Shape.** Open on what goes wrong for the operator who gets this wrong, concretely. Then the
rule, deadline, threshold, or mechanic that governs it, sourced from the domain skill. Then what
to actually do. Facts are load-bearing and must all appear, but never in the first two
sentences. Never open with regulation summary. Never use "The first is X / The second is Y"
headings. Write it to be useful whether or not the reader ever hires JT.

**Selling.** Automation may be mentioned at the end in one sentence, or not at all. This lane's
job is demonstrating domain command, not selling.

**Accuracy.** Every date, deadline, threshold, and program name must come from the reference
file you opened. If the file does not state it, do not state it. If the file is missing or
unreadable, output NO COMPLIANT DRAFT rather than writing the briefing from memory.

**Output.** A post body. Report the reference file used.

### MONTHLY — BUILD NOTE — carousel, replaces a Tuesday

**Source.** `~/Desktop/proof-engine/proof-ledger.jsonl`, one unused record whose `gate_status`
is exactly `publish-ready`. Records with any other `gate_status` are not eligible, whatever
their `missing_gates` field says.

**Shape.** Open on what was breaking before, not on what JT built. What was manual. What runs
now. Where the human approves.

**Descriptor.** Use the `anon_descriptor` field exactly as written, character for character. Do
not re-word it, expand it, or make it more specific.

**Numbers.** Use a number only if `metric_permissioned` is true on that record. Otherwise
describe workflow states, using `states_before` and `states_after`.

**Output.** The same card blocks specified under "Card blocks" below, plus a post body. Report
the record `id`.

## Formatting

**Length.** 1,500 characters is a ceiling, on every lane. There is no minimum. Never add a
sentence, an example, or a paragraph to reach a length. A post that says what it needs in 900
characters is finished at 900.

**Paragraphs.** No paragraph runs longer than three sentences. A blank line between every
paragraph. Most posts carry at least one single-sentence paragraph doing the turn.

**No lists.** Never use bullets, dashes, numbered lists, or unicode list characters in a post
body. The voice is plain declarative sentences. Why: list formatting reads as machine output and
renders inconsistently across devices.

**The list rule is about register, not punctuation.** Break a dense paragraph into several short
paragraphs, one idea each, blank line between. Do not convert it to a list. Stripping the bullet
characters off a list does not fix it.

**Every line is a complete sentence, or it is merged into the line before it.** No fragments with
the subject dropped, and no mixing fragments with full sentences. Why: that mix reads as a
product feature list, which is the vendor register this whole skill is avoiding.

**Body vs. deck, on any lane that produces cards.** The body must not restate the workflow steps
that appear on Master B. The body's job is the problem and the stakes; the deck's job is the
mechanism. Why: if a reader can get the workflow without swiping, the deck is wasted.

The body may reference one or two specifics from the workflow that make the deck worth opening.
It may not walk all four steps.

## Hard rules — every lane

1. Never state a fact, descriptor, or number that is not in a source file or a source you can
   name. No estimates. No "significantly" standing in for a number you do not have. The single
   exception is the Wednesday illustrative scenario, which is invented under the constraints in
   that lane, marked hypothetical in the copy, and carries no numbers. It is not a fact claim.
2. Never name a client. Never name the partnership, any partner, any revenue or pricing figure,
   any infrastructure detail, or any legal or attorney material.
3. Every workflow shown includes its human-approval point. Not optional.
4. The first 210 characters must stand alone before the fold, and must not be a rhetorical
   question or a hook cliche. Cross-check them against the banned openings in jt-voice.
5. Zero to three hashtags, at the end only. No links in the body. Note the link separately for
   the first comment.
6. If a compliant draft is not possible for a slot, output `NO COMPLIANT DRAFT` and the reason.
   An empty slot is fine. A fabricated one is not.
7. Read the AVOID list in jt-voice before drafting, and check the finished draft against it
   before returning it.

## Output format

For each draft, in this order:

```
LANE:        Tuesday teardown | Wednesday operator lesson | Thursday domain briefing | Monthly build note
SOURCE:      record id, or reference file name, or the named public signal
CHARACTERS:  <count of the post body>
PROOF-SAFE:  PASS | the missing gate
```

Then the post body. Then the card blocks, if the lane uses them.

Count characters mechanically rather than estimating — write the body to a file and count it,
or pipe it through `wc -m`. Why: character estimates are consistently wrong, and 1,500 is a hard
ceiling.

The reported count is information, not a target to hit. A count well under the ceiling is a
finished post, not a short one.

`PROOF-SAFE: PASS` means you checked all seven hard rules against the finished draft. If any rule
fails, name the one that failed instead of writing PASS. Do not write PASS and then note a
caveat underneath.

Not part of JT's spec, but available: `~/Desktop/proof-engine/lint.py` and `banned-nouns.txt`
sit alongside the source files and can be run as a mechanical pre-check. The PROOF-SAFE verdict
is still yours.

[NO RECAP LANE SECTION EXISTS IN linkedin-content SKILL.md. The skill defines four lanes and nothing else. Nothing has been written to stand in for it.]

--- VOICE SKILL ---
---
name: jt-voice
description: Write in JT's voice for public publication: LinkedIn posts, social copy, X posts, captions, launch and proof posts, and any short public writing that goes out under his name. Use this skill whenever the task is to draft, rewrite, tighten, or edit a post JT will publish, or to check whether a draft sounds like him. Always use it before producing any LinkedIn draft, even a one-line one. Do NOT use it for client deliverables, proposals, playbooks, resumes, documentation, or code. Those have their own skills and their own register.
---

# JT Voice

Operating rules for writing publishable copy in JT's voice. Every rule below is checkable
against a draft. Verbatim examples are evidence and outrank any rule here. When a rule and
an example conflict, follow the example.

## 1. Sentence mechanics

- Keep most public lines between 7 and 18 words.
- Allow 18–35 words only when the sentence carries a constraint stack: source data, system
  of record, approval owner, exception path, metric, or deployment detail.
- Use short sentences for verdicts, transitions, and proof points. Verbatim:
  - "Some rows are routine."
  - "Some rows touch money, tenant communication, owner judgment, or legal timing."
  - "The workflow needs to know the difference before it drafts anything."
  - "Facts. But distribution is the new moat."
  - "Send it."
- Use a fragment only when it is conversationally earned or when a metric/proof point is
  stronger without explanation. One- and two-word fragments are rare on LinkedIn, more
  natural on X and in replies. Never stack fragments for drama.
- Write second clauses. The pattern is plain first claim + practical reason, caveat,
  dependency, or consequence. Connectors: "but," "because," "before," "when," "if," "so,"
  "without."
- The second clause must add operational clarity, not polish. If it only adds rhythm, cut it.
- Use condition-first sentences. Verbatim:
  - "If all information could live in a single source spreadsheet, this should be pretty straightforward."
  - "If the blocked case has no owner, the workflow is not ready."
- Keep rough practical qualifiers when they carry real judgment: "probably," "pretty,"
  "largely," "imo," "at that point in my life." Do not use them inside a professional proof
  claim. Why: a hedge on a verified number reads as an unverified number.
- Do not smooth the cadence into even, uniform sentences.
- Length alternation is mechanical, not a feel: after any sentence over roughly 25 words, the
  next sentence must be under 10. Never place two consecutive sentences of similar length in a
  closing. Why: back-to-back polished long sentences are the flattest AI tell in a draft.

## 2. Openings

Open with the ask, the work, the scene, or the concrete signal. Never with throat-clearing.

Real opening lines, verbatim:

1. "Built this AI workflow for Yair and his real estate firm."
2. "Yesterday I installed a dedicated automation PC for a NYC real estate family office."
3. "This is essentially what I attempted to build with http://adversightai.com almost a year ago."
4. "Context on how this works: GPT-5.2, Gemini 3 Pro, Opus 4.5, and Grok 4 work together and cross-check other to provide optimal analysis with a focus on game theory positioning."
5. "Lead capturing from NYC ballet family contributors page"

Confirmed posted LinkedIn opening, verbatim:

- "A delinquency balance, a lease date, and a deposit chase should not move through the same AI workflow without a decision trail."

Allowed opening patterns:

- Built this / installed this / deployed this, only when proof exists.
- A concrete buyer scene stated before any AI category.
- A current company or market signal translated into an operator problem.
- A workflow object plus its operational consequence.
- "Context on how this works:" when explaining the technical system behind a claim.

Banned openings. Reject a draft that starts with any of these, verbatim or in shape:

- "Great question" or any preamble.
- "Here's what I've been thinking about lately..."
- "The best first AI project is..."
- "Most AI projects do not fail because X. They fail because Y."
- "Most SMBs do not need X. They need Y."
- "The blocker is not X, it is Y."
- "The question that changes every build: ..."
- "What most people miss..."
- "Here's the system:"
- "Here's what you need to do:"
- "The results?"
- Insult or hype hooks: "you're a moron," "INSANE opportunity," "DO NOT," "EVERYTHING," "PISSED."

## 3. Vocabulary

**Use.** Repeated natural words: workflow, handoff, owner, approval, source, queue, system,
exception, intake, record, check, proof, deployment, local, messy, concrete, route, logs,
source record, system of record, approval boundary, review queue, final outcome, decision
trail, operating path, existing systems, sensitive rows, safe operating environment.

Domain terms, used as operating objects and never as buzzwords:

- Property operations: delinquency balance, lease date, deposit chase, tenant communication, owner judgment, legal timing, AppFolio, COI, rent delinquency, lease renewal.
- Workflow implementation: source report, approval owner, exception path, audit trail, human review, confidence threshold, final record.
- SMB AI: AI workflow, AI implementation, automated workflows, local deployment, dedicated mini PC, existing files, review item, source attached.
- Salesforce/enterprise-adjacent: Agentforce, Data Cloud, records, owners, approval workflows.
- Crypto/technical: model stack, cross-check, risk/return, game theory positioning. Casual conviction is allowed only after the method has been stated specifically.

**Avoid completely in public content.** Search the draft for each: utilize, synergy,
ecosystem, scalable, streamline, actionable, bandwidth, holistic, innovative, robust,
cutting-edge, best-in-class, thought leader, value-add, paradigm, granular, deliverable,
upskill, touchpoint, disruptive, transformative, implementation excellence, unlock, unpack,
proactive, learnings.

**Phrases already rejected. Delete on sight, verbatim or reworded:**

- "AI is changing everything"
- "The tools exist. The implementation doesn't."
- "Agents handle the work. You keep the margin."
- "Build the process. Buy back the time."
- "Demo proves it's possible. Deploy proves it's real."
- "Specs live in decks. Systems live in production."
- "Chatbots answer questions. Agents close tickets."
- "The implementation is always the bottleneck."
- "matters more than people think"
- "people underestimate"
- "that part matters"
- "exception layer" as a repeated or generic hook
- "AI chatbot" contrast framing

## 4. Punctuation and formatting

- No em dashes. Use a comma, colon, period, or parentheses.
- No exclamation points in normal posts.
- No hashtags by default. If JT explicitly asks, use exactly three tight relevant LinkedIn hashtags at the end. Never a hashtag block.
- No emoji by default. The one known natural exception is a real human detail: "They decided to name it Jarvis 😂." Never use emoji as decoration.
- LinkedIn posts run 3–6 short paragraphs. A Monday post can be 1–3 sentences.
- Blank line between every paragraph. One idea per paragraph.
- Use a list only to name concrete workflow components. No numbered creator lists unless the structure carries JT-specific operating judgment.
- Bullets are plain and functional. No decorative bullets.
- Normal sentence case. Lowercase is allowed only for X thinking-out-loud posts, never for LinkedIn case studies, launches, proof posts, or milestones.
- No colon hook machinery. A colon inside a technical explanation is fine; a colon that announces a framework is not.
- No "No X. No Y. Just Z." tricolon negation.

## 5. Stance and claims

- Remove, narrow, or mark as projected any claim you cannot support. Never inflate proof.
- State verified numbers bluntly. Label a projected number "projected."
- Keep proof internal or abstract the client unless the work is accepted, paid, permissioned, or anonymized.
- Never imply a company is a client unless it is.
- Do not hedge with "I think maybe" or "from my perspective." Hedge with "probably," "pretty," "I am unsure," "if," "should," "would."
- Use "I would build" for a teardown or hypothetical implementation.
- Lead with ownership only when proof exists: "Built this," "Installed," "I put together," "I would start with." Follow it with architecture, constraint, or metric. No humblebrag.
- Make predictions rarely, and only tied to an operating reason. Prefer naming what a workflow needs over a broad future claim.
- When writing about someone else's work, translate the public signal into an operational problem. Never dunk. Never make JT's value depend on saying others are bad.
- A reader question is optional. End with a clean insight or a direct question.
- Never end with engagement bait: "what do you think," "DM me," "link in bio," "follow me for more."

## 6. Post structures

**Template 1: verified build proof.** Requires real shipped work.

1. Ownership line. 2. Deployment surface or operating detail. 3. Workflow scope or examples.
4. Safety or approval rationale. 5. Human exception boundary. 6. Metric or projected outcome.
7. Vertical thesis or practical implication.

Shape: Built this for X. Dedicated machine / existing files / local setup. It handles A, B, C.
Sensitive rows stay in review. Metric. This is what real implementation means for established
businesses.

**Template 2: buyer-scene consulting post.**

1. Concrete workday scene. 2. Specific examples of inputs or handoffs. 3. Plain diagnosis.
4. Where AI fits. 5. Owner / approval / exception path. 6. Cleaner operating outcome.

Shape: A tenant email, vendor note, lease date, and owner rule should not become separate
follow-up systems. The workflow reads the source, checks the record, drafts the clean path,
and holds the sensitive case for the owner.

**Template 3: AI Ops teardown.**

1. Current public signal. 2. Buyer-recognizable bottleneck. 3. Messy input scene.
4. System-of-record need. 5. Workflow JT would build. 6. Clean path and exception path.
7. Outcome before bad data or missed work hits the downstream system.

**Template 4: buyer-scene consulting post, critique-reconstructed.** Reconstructed from
critique of rejected drafts, not from a published example. Treat the beats as corrections to
a generic explainer, not as an exemplar. This is the shape the critiques said should have
replaced a numbered compliance or "two things to watch" explainer.

1. The operational pressure, stated as the thing the workflow has to survive. Not a regulation
   summary, not a definition.
2. The messy handoff: the portfolio, the document, the entity that actually signed, the twelve
   months of data. Facts land here, supporting the problem.
3. The exact check, named. What the workflow verifies, and what it will not catch.
4. Where the workflow should stop, and the risk boundary that decides it.
5. Who owns the flagged row. The human approval point, named as a person's decision.
6. What proof has to be stored, and whether it can be produced later.

Shape, from the critique's own re-cut: "Local Law 97 is not just a penalty calculation. For a
portfolio, the work is twelve months of utility data, the right lot, the right owner, and a
filing confirmation you can produce later." Closing shape: "Automate verification, but keep
human sign-off on anything that would block a vendor from working."

**Template 5: verified build, learned-from-failure.** Reconstructed from critique of a
rejected draft, not from a published example. Requires a real failure that happened.

1. The failure, concrete and already on the page.
2. The check that missed it, and what it confirmed instead.
3. The corrected rule, stated plainly with no setup sentence in front of it.
4. The safer behavior now in place.
5. The consequence, kept inside the failure-and-guardrail lane.

Do not translate the failure into a generic "why this matters" audience lesson. The sequence
is failure, missed check, corrected check, consequence.

Shape, from the critique's own re-cut: "A health check kept reporting green after the access
key behind it had been revoked. The integration was failing authentication. Nothing surfaced."
Closing shape: "If a check cannot fail, it is not telling you anything."

## 7. What I edit out

Cut each of these from any draft before it ships:

- Generic AI consultant posture, even when the idea is true.
- Hooks that announce a framework instead of showing a scene.
- Contrarian reveal engines: "not X, Y," "X should be Y, not Z," "X needs Y, not Z," "X is not just Y. It is Z," "The risk is not X. The risk is Y," "X don't Y, they Z."
- "gets solved with a hire."
- Statement-colon hooks like "The question that changes every build: ..."
- Closers shaped like "X happened/changed/worked when Y."
- "matters more than people think". Replace it with the exact business reason.
- Outreach-meta on LinkedIn unless the topic is explicitly sales ops. Prospect research, lead enrichment, channel selection, and outbound process do not belong in default consulting posts.
- Internal content-system transparency on LinkedIn: state files, content automation, swipe mechanics, proof cleanup, public-proof hygiene. Keep internal unless attached to a real buyer problem or shipped outcome.
- Casual builder diary language on LinkedIn: "quick update," "small win," "built this weekend," "been playing with," "nothing crazy," "pretty cool," "vibes," tool fandom, app-growth chatter with no buyer or employer trust value.
- Fake proof and overclaiming: client names, metrics, payments, or acceptance claims that are not verified and safe to publish.
- Over-polished aphorisms. If a line could be printed on an AI consultant carousel, it needs a concrete object, owner, metric, approval rule, or buyer scene.
- Excessive compression on X: trust-question hooks, dramatic one-word noun stacks, "the useful question is uglier," "probably a margin leak," "that's not automation, that's leverage," build-list flex CTAs.
- Corporate smoothing: "in today's landscape," "broader implications," "centralized source of truth," "streamline execution."

### Rewrite patterns (verbatim, from draft-versus-critique diffs)

These are evidence, not description. Both sides are quoted as written. Match the shape, not
just the sentence.

- Instead of "Local Law 97 penalties run $268 per metric ton of CO2 equivalent over a building's limit", write "The penalty number is not the hard part. The filing trail is."
- Instead of "Knowing the number is the easy part.", write "For a portfolio, the number is only one row."
- Instead of "That step stays human, because the number drives penalty exposure and capital work.", write "That step stays human. The number drives penalty exposure and capital work."
- Instead of "Step five is the one that gets skipped.", write "The filing confirmation is where this usually gets weak."
- Instead of "An accepted submission and a submission you can produce on demand are different things", write "Accepted is not the same as retrievable."
- Instead of "that is the audit I would run first", write "I would check whether the confirmation is stored against the building record."
- Instead of "Every real request going through that integration was failing authentication, and nothing surfaced.", write "The integration was failing authentication. Nothing surfaced."
- Instead of "It never confirmed the service could still do the thing it existed to do.", write "It never confirmed the authenticated request worked."
- Instead of "Now the health check makes one real, cheap authenticated call against the live dependency at startup.", write "Now startup makes one cheap authenticated call against the live dependency."
- Instead of "This matters if you run an ops team, because", write "For an ops team, this is the bad version."
- Instead of "a green dashboard sitting on top of a dead integration", write "the dashboard is green and the integration is dead."
- Instead of "The status page says fine. The queue quietly stops moving.", write "The status page says fine. The queue stops moving."
- Instead of "The same shape shows up well outside software.", write "This is not only a software problem."
- Instead of "Two defects show up on vendor certificates of insurance that checking dates and limits will never catch.", write "Checking dates and limits will not catch the two defects that matter on vendor certificates of insurance."
- Instead of "A certificate is evidence of coverage, and the endorsement is the policy amendment that makes the coverage real.", write "The certificate is evidence. The endorsement is the amendment."
- Instead of "you are collecting evidence of something nobody has confirmed", write "you still have not confirmed the endorsement."
- Instead of "Both defects surface at the worst possible time", write "Both defects usually matter after a loss."
- Instead of "What to do about it is not complicated.", cut the sentence. The next sentence already says what to do.
- Instead of "Verification is the step worth automating", write "Automate verification."

### AVOID (flagged tells, quoted exactly)

**Lesson-announcement openers.** They announce the lesson before saying it. Say the rule.

- "The rule I broke is a plain one."
- "Step five is the one that gets skipped."
- "Knowing the number is the easy part."

**Audience bridges.** LinkedIn-translation voice.

- "This matters if you run an ops team, because"
- "The same shape shows up well outside software."

**Empty connectives.** Cut, do not rewrite.

- "What to do about it is not complicated."

**Softener adverbs.** Common AI softeners inside an otherwise blunt line.

- "quietly", as in "The queue quietly stops moving."

**Listicle announcements and school-essay structure.**

- "I would build it as five steps."
- "The first is the named insured." / "The second is additional insured status."

**Glossary-definition sentence shape.** Written for correctness instead of cadence.

- "A certificate is evidence of coverage, and the endorsement is the policy amendment that makes the coverage real."

**Mirrored parallel sentence pair.** Too neat. One of the two must be shorter or blunter.

- "A vendor portal that accepts a document has not told you the document was valid. A sync that ran on schedule has not told you the records landed on the other side."

**Also flagged.**

- Fact-dump opener: "Local Law 97 penalties run $268 per metric ton of CO2 equivalent over a building's limit"
- Policy-summary voice in paragraph two: "Coverage is buildings over 25,000 square feet, plus tax lots and condo boards that clear 50,000 square feet together."
- Engineered curiosity hook: "Two defects show up on vendor certificates of insurance that checking dates and limits will never catch."
- Model-written plainness: "the thing it existed to do"
- Vague outage scale: "Every real request going through that integration was failing authentication, and nothing surfaced."
- Creator-copy shine: "a green dashboard sitting on top of a dead integration"
- Aphorism shape: "An accepted submission and a submission you can produce on demand are different things"
- Polished aphorism: "you are collecting evidence of something nobody has confirmed"
- Generic risk phrase: "at the worst possible time"
- Slogan shape: "Verification is the step worth automating"
- Soft CTA ending that restates the post instead of landing the risk: "that is the audit I would run first"
- A strong claim with no proof on the page: "This is the most common real defect, and the hardest to catch by eye." If the claim cannot be supported inside the post, put a real detail there instead.

## 8. Sample lines (verbatim)

1. The source report has to be trusted before the workflow drafts anything sensitive.
2. I would not let an agent approve cash movement. I would let it find the risk and queue the approval.
3. Some rows can move automatically. The expensive ones need an owner.
4. If all the source data can live in one sheet, this should be straightforward.
5. The workflow is not ready until the blocked case has somewhere to go.
6. Built the approval step first because that is where the business risk sits.
7. I am not sure that claim is strong enough to publish without a cleaner proof path.
8. The demo worked in a clean file. The deployment had to survive the spreadsheet the client already checks.
9. A property manager does not need another place to check. They need the request, record, owner rule, and final outcome in one path.
10. Normal work can move faster when the sensitive rows still have a named owner.

## Gaps in the source profile

Stated plainly so no one fills them by guessing:

- **X/Twitter voice is defined only negatively.** The profile says what to cut on X and that
  lowercase and short fragments are more natural there, but supplies no X exemplar. Draft X
  posts from the LinkedIn rules minus the LinkedIn formatting rules, and flag them as unproven.
- **No full post is preserved anywhere.** Only openings, sample lines, and beat shapes. The
  templates are structures, not exemplars.
- **Emoji has one datapoint** ("Jarvis 😂"). Treat it as the only sanctioned case, not a pattern.
- **Cadence is thin.** "Monday can be 1-3 sentences" is the only posting-rhythm signal; the
  profile says nothing about frequency or the rest of the week.
- **Predictions have no example.** The rule (rare, tied to an operating reason) is supported;
  no verbatim prediction line exists to imitate.
- **Only one line is confirmed as actually posted:** the delinquency-balance opening. Everything
  else is local evidence or drafting rule.

## Corrections

Rules added from published-versus-draft diffs go here. Newest first.

**2026-08-16 — Close on an audit the reader can run against their own records.** End with
something the reader can go do, not a conditional that restates the post. Published: "Pull your
open violations and find the oldest one nobody has touched. Then ask who was supposed to be
chasing it." Cut: "If your compliance tool stops at the alert, the chase is the part still being
done by hand." This is the positive form of the soft-CTA tell already in the AVOID list. Source:
SiteCompli InCheck teardown, published 2026-08-11.

**2026-08-16 — Never characterize a competitor's pricing, target market, or category position.**
Credit the product for what it actually does, then name only the limit visible in the product
itself. Cut outright: "it is priced and built for large portfolios." Narrowed: "Monitoring is
where the category stops" became "but stops at monitoring." Softened: "That is a real
capability" became "That is a real and useful capability." Why: pricing and target market are
claims about a company you have no access to, and one product does not support a verdict about a
category. Source: same post.

**2026-08-16 — The opening states the scene and the gap, and nothing more.** Cut any clause that
tells the reader what the scene means before they have read it. Draft: "A violation notice lands
in a shared inbox, and the alert that produced it has already done its whole job. Nobody has been
handed the correction, the vendor, or the filing." Published: "A violation notice lands in a
shared inbox, but nobody has been handed the correction, the vendor, or the filing." Source: same
post.

**2026-08-16 — Name the operational object in the operator's own words.** "cure window" became
"correction deadline." "with the confirmation" became "with its acceptance." "The returned
document files against the building record" became "When the vendor sends proof back it attaches
to that item." Why: legal shorthand and vague nouns both hide the thing actually being tracked.
Source: same post.

**2026-08-16 — A teardown body may run past six paragraphs when each carries a single beat.** The
published post ran nine, most of them one sentence. This supersedes the "3–6 short paragraphs"
range in section 4 for this lane. Source: same post.

**2026-08-16 — The approval actor is a human, not a person.** Published: "The owner update is the
step a human approves before it sends." Source: same post.

**2026-08-10 — Open with the operational failure, never with explanation.** A post opens with
the operational failure or risk the workflow has to survive, and lets the facts support that
problem afterward. Never open with a regulation summary, a policy or coverage explainer, a
fact dump, a numbered-explainer frame, or a generic audience lesson translated out of a real
failure. Where the post already contains a real failure, keep the sequence as failure, missed
check, corrected check, consequence. Source: three drafts rejected for this same opening
(Local Law 97, health check, certificates of insurance).

--- PUBLISHED POSTS ---
LANE: Tuesday teardown
DATE: 2026-08-11

A violation notice lands in a shared inbox, but nobody has been handed the correction, the vendor, or the filing.

SiteCompli is the mature incumbent in NYC compliance monitoring. Its InCheck product scans DOB, FDNY, HPD, DEP and DOT for new violations and tells the manager one was issued.

That is a real and useful capability, but stops at monitoring. Manual labor remains after the alert.

The workflow I would build starts where the alert ends.

One item per violation, with the due date set from the correction deadline for that class rather than from when someone gets to it.

When the vendor sends proof back it attaches to that item, and the certificate of correction goes in the same place with its acceptance.

The owner update is the step a human approves before it sends.

Class C conditions are immediately hazardous, so that escalation path gets a named owner before the workflow runs, not after it misses one. Anything touching money or legal timing stays in the review queue.

Pull your open violations and find the oldest one nobody has touched. Then ask who was supposed to be chasing it.

#PropertyManagement #BuildingCompliance #PropTech

>>> PASTE THE OTHER TWO PUBLISHED POSTS HERE, WITH LANE AND DATE <<<

--- CARD FRAMES ---
Five frames, 1080x1350 portrait, published as a PDF carousel on Tuesdays and
for monthly build notes. Wednesday and Thursday are text only.

Frame A, the title frame. One sentence naming the operational failure. Hard cap of 12 words. No second sentence.

Frame B, the workflow frame. Exactly four steps, labeled B1 through B4. Maximum 18 words each. B4 is always the human-approved step, and it is written in second person, addressed to the reader, in the shape "You review X and release it. Nothing Y before you do." Never five steps, because the card template places the approval marker on the fourth step, so a fifth step would render that marker in the wrong position.

Frame C, the states frame. Six lines, labeled C-before-1, C-before-2, C-before-3 and C-now-1, C-now-2, C-now-3. Maximum 12 words each. They pair up in order. Keep them situational: where the work lives, who has to remember, what breaks when someone is out. No numbers and no percentages.

Frame D, what stays human. Four lines. The first three are fixed and never change: "Anything that moves money." / "Anything with a legal deadline." / "Anything a lawyer would want a signature on." The fourth line is specific to that post's workflow. Maximum 12 words.

Frame E, the closing frame. Not generated per post. It is fixed in the design system and carries no per-post copy.

Rules that apply across the five frames. The labels and counts are fixed, so no block is added, dropped, or renumbered. Every block is checked against the AVOID list in the voice skill before output, the same as post body copy. The post body must not restate the workflow steps that appear on frame B: the body's job is the problem and the stakes, the deck's job is the mechanism. The body may reference one or two specifics from the workflow that make the deck worth opening, but it may not walk all four steps.

--- HASHTAGS AND DOCUMENT TITLES ---
## Hashtags

Every draft returns exactly three hashtags, placed at the end of the post body on their own
line. Report the three tags separately from the post body so they can be seen at a glance.

**Slot 1 is always `#PropertyManagement`.** It never changes. Why: it is the anchor that
accumulates topic authority.

**Slots 2 and 3 are specific to the post**, chosen from vocabulary an operator would actually
search. Draw from: `#NYCRealEstate`, `#RealEstateOperations`, `#PropTech`,
`#BuildingCompliance`, `#Multifamily`, `#NJRealEstate`, `#OperationsManagement`,
`#FacilitiesManagement`, plus the specific law or program when the post is about one — for
example `#LocalLaw97`.

**Never, under any circumstance:** `#AI`, `#ArtificialIntelligence`, `#Automation`,
`#Innovation`, `#Leadership`, `#FutureOfWork`, `#Productivity`, `#DigitalTransformation`,
`#Tech`, `#Entrepreneurship`, or any tag with more than roughly 500k followers. Why: they
classify JT into a category his buyers are not searching, against everyone else in it.

Never more than three. Never a hashtag inside the body text.

## Document title

Every draft in a lane that produces cards also returns a DOCUMENT TITLE for the PDF upload.

- Plain and descriptive. It names what the document contains.
- Under 60 characters.
- Contains the terms an operator would search: the process name, the law, or the system. Why:
  this field is indexed.
- Never a hook, never a question, never a colon followed by a promise, never a number-led
  listicle title, no emoji, no title case affectation.
- It should read like the name of a file someone would keep.

Good: `NYC violation response: the workflow after the alert`
Good: `COI expiration tracking for a NYC portfolio`
Good: `Local Law 97 filing trail: what to store and where`
Bad: `The ONE thing property managers get wrong`
Bad: `5 steps to automate compliance`
Bad: `Why your compliance tool is failing you`

--- CADENCE ---
### TUESDAY — TEARDOWN — carousel
### WEDNESDAY — OPERATOR LESSON — text only
### THURSDAY — DOMAIN BRIEFING — text, or text plus one card
### MONTHLY — BUILD NOTE — carousel, replaces a Tuesday
