# Content Voice — JT Somwaru
*JT operator voice first. Compression is useful only when it preserves proof, specificity, and natural cadence.*
*Load this file before drafting any X post, thread, or LinkedIn content.*
*Also load `memory/content/current-niche-map.md` before choosing the niche or swipe references.*
*For taste-level voice decisions, load `memory/content/jt-voice-profile.md`; this file owns mechanical/platform rules.*
*For evidence-backed voice calibration, load `memory/content/jt-voice-evidence-corpus.md`; run `python3 scripts/jt_voice_guard.py [draft] --platform linkedin|x` before serious drafts reach JT.*

---

## The Core Rule
Compression is confidence — but compression is a **language tool**, not a length requirement for every post.
A 300-word LinkedIn case study written tight is better than a 12-word aphorism that proves nothing.
Use compression to cut waste. Use depth when the goal is credibility, not virality.

## Actual Voice Evidence Layer

Generated posts should now be judged against `memory/content/jt-voice-evidence-corpus.md`, not just generic style rules.

JT's voice is not "short AI consultant copy." It is:

- Direct request/decision cadence.
- Short verdict fragments when conversationally earned.
- "But" pivots that sharpen the real point.
- Concrete nouns before abstract claims.
- Workflow objects before AI categories.
- Ownership when proof exists.
- Buyer scene when selling implementation judgment.
- System, owner, approval, input, queue, record, metric, or exception before conclusion.
- Practical constraint stacks when reflecting on old builds.
- Condition-first implementation clarity: "If [source/condition] can live in [one place], this should be straightforward."
- Direct next-step/dependency language in client-facing copy.
- Safe operating environment when selling implementation into established businesses.
- Short casual conviction only after the proof/method has done the work.

If a draft cannot name the operating object it is about, it is not specific enough.

If verified proof exists, the most JT-native structure is often: built this -> deployment detail -> metric -> vertical thesis. Do not dilute that into generic "AI automation saves time" copy.

For longer LinkedIn proof posts, the most JT-native structure can be: deployment story -> workflow count/examples -> why the setup is safe -> what real implementation means -> human exception boundary -> projected or verified outcome.

Before delivering a serious LinkedIn/X draft:

1. Load `memory/content/jt-voice-profile.md`.
2. Load `memory/content/jt-voice-evidence-corpus.md`.
3. Run `python3 scripts/jt_voice_guard.py [draft-file] --platform linkedin|x`.
4. Rewrite until score is 80+ and no listed problems remain. The guard fails on any problem line.

Hard-banned AI-slop hooks from JT's Question 2 answer:

- "The best first AI project is..."
- "[Niche] AI gets useful at..."
- "Most AI projects do not fail because X. They fail because Y."
- "Most SMBs do not need X. They need Y."
- Colon plus comma-list instructions like "answer four questions: what..., what..., who..., where..."

These can contain good operational ideas and still sound fake. Rewrite around the actual deployment, buyer scene, constraint, or result.

Hard-banned borrowed-creator patterns from JT's Question 3 answer:

- "what most people miss"
- "here's the system:"
- "here's what you need to do"
- "the results?"
- Insult hooks like "you're a moron"
- Hype caps/manic urgency: "INSANE opportunity," "DO NOT," "EVERYTHING," "PISSED"
- Numbered lists with no JT-specific personality
- Motivational CTAs like "take action before someone else does"

If using @AlexFinn-style references, borrow only the structure: urgent opportunity, concrete tool stack, setup path, market-pain scan, prototype loop. Rewrite the persona into JT's calmer operator voice.

Hard-banned sentence shapes from JT's Question 5 answer:

- "gets solved with a hire"
- "X don't Y, they Z"
- Statement followed by colon as hook machinery, e.g. "The question that changes every build: what are you trying to prevent?"
- Closing posts with "X happened/changed/worked when Y"

Rewrite those into direct sentences with the real operational consequence, owner, rule, or result.

Hard-banned too-polished X patterns from JT's Question 7 answer:

- "Would you trust an AI agent with..." staged trust hooks.
- "I would trust it with..." reveal lines.
- One-word or two-word operational noun stacks as dramatic line breaks: "Urgency. Unit history. Vendor route."
- "Your [inbox/workflow/etc.] is probably a margin leak."
- "The useful question is uglier:"
- "Make stuck work visible before you make replies faster."
- Big build-list flex posts ending with "What did you build in [month]?"
- "The difference between [X] and [Y] is the difference between automation and chaos."
- "That's not automation. That's leverage."

The issue is not that these are short. The issue is that they sound staged: guru compression, dramatic list rhythm, abstract moral lines, or creator flex CTAs. For X, prefer a rawer single observation, a concrete build fact, or a direct operational judgment that still sounds like JT texting the point.

Positive sentence shapes inferred from JT's Question 4 answer:

- "Facts. But [actual point]."
- "I like that [specific positive]. [Short reaction]. Very unconvinced [practical concern] though."
- "[Actor/system] has proven to be [practical judgment]."
- "They just don't have [constraint]."
- "If [all information/source data] could live in [single source], this should be pretty straightforward."
- "Please review and let me know if all looks good, and if so, I can get started [real timing/dependency]."

Use these as cadence references, not templates to spam. The rule is: keep JT's practical qualifier, source-of-truth thinking, and direct dependency language. Do not smooth it into "in today's landscape," "broader implications," "centralized source of truth," or "streamline execution."

---

## Content Balance Rule

Generated content should balance two credibility modes:

1. **Operator explaining a build:** real workflows, dashboards, deployment details, local machines, approval routes, source-of-truth decisions, automation constraints, metrics, and implementation edge cases.
2. **Consultant naming a buyer problem:** niche-specific operating problems, buyer scenes, messy handoffs, current market signals, and solution shapes for property management, real estate operations, wholesale/distribution, construction/trades, insurance/Agentforce, and AI operating systems.

Use JT's expertise to choose the right mix. Do not ask JT to pick the lane unless the request is genuinely ambiguous.

For a normal weekly queue:

- Include at least one build/proof post when a real build or verified implementation detail exists.
- Include at least one consultant POV post about a focused niche buyer problem.
- Prefer bridge posts when possible: build detail -> why it matters in the niche -> solution shape or buyer implication.
- Skip build updates that are only activity with no transferable consulting judgment.
- Skip buyer-problem posts that could be written by any AI consultant.

Strong content should make a potential client/employer think one of two things:

- "He has actually built this kind of workflow."
- "He understands this operational problem well enough to build the right workflow."

If a batch does not create at least one of those impressions, it is not balanced enough.

---

## Platform Distinction (non-negotiable)

### LinkedIn — Consulting + Career Surface
- **Audience:** NYC SMB owners, hiring managers, recruiters, peers
- **Goal:** Demonstrate expertise, prove you can actually build, generate consulting leads and job interest
- **Tone:** Professional but direct. No corporate jargon. Confident, specific, no filler.
- **What works:** Case studies with real outcomes, tactical insights, proof of work, substantive opinions
- **What doesn't:** One-line aphorisms (weak signal), vague claims, anything that sounds like a tweet
- **Too casual:** builder diary updates, lowercase hot takes, "quick update" posts, vibes/slang, weekend-project chatter, tool fandom, app-growth notes with no consulting lesson, or anything that would not make a potential client or employer trust JT more
- **Never reference @jts_14, X, or Twitter** in LinkedIn content

**Trust-era proof rule:** A serious LinkedIn post should feel like it could only be written by someone close to the work. Include at least two proof assets when available: workflow input, system of record, owner/approval boundary, deployment constraint, before/after metric, safe artifact/screenshot, client/operator scene, or a specific implementation decision. Do not let generic AI commentary, trend reactions, or funnel tactics replace proof.

**Pipeline infrastructure rule:** If a LinkedIn post is designed to generate inbound, name the asset or path behind it: checklist, diagnostic, lead magnet, reply prompt, consultation offer, email capture, or call-prep artifact. Qualified trust beats raw comments. Skip engagement-network and virality-first advice unless it creates trust with the right buyer. Current property-management asset path: `memory/content/assets/property-management-ai-workflow-readiness-checklist.md`.

### X / Twitter — Brand + Community Surface
- **Audience:** Tech builders, founders, AI community, crypto crowd
- **Goal:** Build reach, establish POV, start conversations, attract inbound
- **Tone:** Punchy, a little edgy, direct. Compression works only when it still sounds like JT, not a creator template.
- **What works:** Hot takes, short observations, compressed truths, build-in-public moments
- **What doesn't:** Long explanations, LinkedIn-style case study posts
- **Can reference LinkedIn posts, builds, or consulting work** with a link when relevant

---

## Content Calendar — Format by Day

### LinkedIn Schedule

| Day | Format | Depth | Goal |
|-----|--------|-------|------|
| **Monday** | Short punchy take or compressed truth | 1–3 sentences | Reach, establish voice |
| **Wednesday** | Case study or proof of work | 3–5 paragraphs | Consulting credibility, prospect attention |
| **Friday** | Tactical insight or "how I approach X" | 2–4 paragraphs | Expertise signal for recruiter/prospect |
| **Sunday** | Behind the build | 2–4 paragraphs | Trust-building, process transparency |

**Wednesday is the most important post of the week.** This is the post that makes a property manager or wholesale distributor DM you. It must have:
- A specific client, problem, and outcome (Aya preferred, or a real build)
- A concrete number ("replaced 18 hrs/week", "pulls every 14 days", "$1,000 project")
- A lesson that generalizes to the reader's situation

**Friday must have an actual opinion.** Not a hot take for its own sake — a real perspective on implementation, AI in unglamorous verticals, or consulting reality. 3+ sentences of reasoning minimum.

### X Schedule

| Day | Format |
|-----|--------|
| Monday | Short punchy take (1–2 tweets) |
| Tuesday | Observation or pattern (1–3 tweets) |
| Wednesday | Mini case study or specific result (2–4 tweets) |
| Thursday | Hot take or contrarian opinion (1–2 tweets) |
| Friday | Tactical insight — shorter than LinkedIn version (2–3 tweets) |
| Saturday | Build-in-public or tool/stack note (1–3 tweets) |
| Sunday | Behind the build — compressed version (2–3 tweets) |

---

## Who You're Writing For
Two audiences, same content calendar:
- **NYC business owners** evaluating whether to hire an AI consultant
- **Hiring managers / peers** evaluating whether JT is the real deal

For LinkedIn: neither wants explanation — both want proof you've thought harder than them AND that you've built real things.
For X: neither wants a pitch — both want an insight or observation they haven't heard before.

---

## The 6 Language Techniques (apply to all posts regardless of length)

### 1. Sound-Based Contrast — Use Only After Specificity
Sound-based contrast is allowed only when the sentence is already grounded in a concrete object, metric, owner, system, approval rule, or deployment fact.

Do not use slogan pairs as standalone content. Lines like "Agents handle the work. You keep the margin," "Build the process. Buy back the time," "Consultants charge for advice. I charge for the thing that works," "Demo proves it's possible. Deploy proves it's real," and "Specs live in decks. Systems live in production" are too polished unless they follow real proof.

Better shape:
- "The scraper was easy. The approval queue was the part that made it usable."
- "The demo worked in a clean file. The deployment had to survive the spreadsheet the client already checks."
- "The local machine mattered because the workflow could run near the files without creating a new IT problem."

---

### 2. First-Person Proof > Generic Advice
The old "you/your must outnumber I/my 5:1" rule is retired for JT's core channels. It pushed too many drafts into generic advice voice.

❌ "I built an AI workflow for a construction client that saves 3 hours a day."
✅ "Your ops team is spending 3 hours a day on a problem a workflow could solve in 3 seconds."

The better rule: every serious post needs at least one verifiable specific. Use first person when it proves execution: a number, artifact, deployment environment, named tool decision, failure, client/operator scene, or before/after result.
For case studies, client proof, launches, and build-in-public posts, lead with ownership when credibility is the point. Then prove it with architecture, metric, and vertical thesis.

---

### 3. Compression — Cut Every Word That Doesn't Earn Its Place
Each line should survive this test: read it aloud. If a word can be removed without losing meaning, remove it.

**Rewrite drill:**
❌ "Most businesses are still running on spreadsheets and manual workflows even though the AI tools to fix this have already been built."
❌ "The tools exist. The implementation doesn't."
✅ "The StreetEasy scraper only mattered because the output landed in the sheet the client already used every 14 days."

This applies to every post regardless of length — a 300-word post should feel tight, not padded.

---

### 4. Two-Part Parallel — Not A Default Template
Two sentences can work when they describe a real functional distinction. They fail when they become generic category contrast.

Bad:
- "Chatbots answer questions. Agents close tickets."
- "The tech is ready. The operations aren't."
- "Every business has the data. Almost none has the workflow."

Better:
- "The tenant email is only the start. The owner approval rule decides whether the workflow is usable."
- "The PDF has the answer. The workflow still needs to know who owns the exception."
- "The system can draft the follow-up. A manager still needs the flagged rows in review."

---

### 5. Uncomfortable Truths — Stated Flat
Say the thing people avoid saying. No softening. No hedge.

- "If your team still checks the same spreadsheet every morning, the system is not finished."
- "A workflow with no exception owner just creates cleaner follow-up work."
- "The scraper is not the hard part. The hard part is where the output lands and who reviews the edge case."
- "If the approval rule lives in someone's head, the automation is not ready."

**Rule:** One sentence. No follow-up explanation needed. Trust the reader.
*Use on Mondays (LinkedIn) and Thursdays (X). Not every post.*

---

### 6. Lowercase for "Thinking Out Loud" Posts
Lowercase signals observation, not announcement. Counterintuitively gives more authority.
Use for hot takes and compressed insights — NOT for announcements, launches, or threads.

✅ "automating a broken process just breaks it faster"
❌ "the implementation is always the bottleneck"
✅ "the approval rule is usually where the build gets real"

❌ lowercase on: launch announcements, project milestones, demo drops, case studies

---

## JT's Theme Library

| Theme | What JT Actually Knows |
|-------|------------------------|
| **Agents > chatbots** | Built triage, inventory, construction workflows from scratch |
| **Implementation gap** | 6 years watching $500K systems fail due to no change management |
| **Build in public** | Consulting clients, Vista, Nash Satoshi — shipped, not theorized |
| **AI for unglamorous verticals** | Construction, wholesale, property mgmt — where the real ROI is |
| **Real estate operations automation** | COI tracking, rent delinquency, lease renewals, compliance workflows, local systems, recurring exception handling |
| **Manual → automated** | Concrete before/after from Aya client ($1,500 dashboard, $1,000 scraper) |
| **x402 / agentic payments** | Early builder, forward bet on infrastructure layer |
| **Consulting without the corpo** | No buzzwords, no decks that gather dust |

---

## Current Niche Hierarchy

Canonical map: `memory/content/current-niche-map.md`.

Default LinkedIn lanes:
1. SMB AI implementation.
2. Property management operations.
3. NYC SMB operations.
4. Wholesale distribution operations.
5. Construction + skilled trades operations.
6. Insurance / Agentforce operations.
7. AI operating systems / agent orchestration.
8. AI enablement / solutions architecture career.
9. Productized services / solo operator systems.

Product lanes like Vista, Nash Satoshi, Glow Index, and App Marketing are active but secondary. Use them when the post is explicitly about product growth, app proof, passive-income experiments, or builder credibility. Do not let them become the default niche set for LinkedIn consulting content.

Claude Code is a tool/proof ingredient, not a primary niche.

## AI Ops Teardown Standard

AI Ops Teardown posts are not generic workflow advice. They should examine a current company, funding event, product launch, market shift, regulation, or visible buyer problem in a niche relevant to JT, then show the optimal AI workflow JT would build for that exact company/problem.

Minimum bar:
- Current signal, preferably last 30 days.
- JT-relevant niche: property ops, construction/trades, wholesale distribution, insurance/Agentforce, SMB operations, or AI operating systems when tied to business adoption.
- Specific workflow map: inputs, extraction/classification, system-of-record check, exception handling, human approval, output, audit trail.
- Distinct angle from the last 45 days of scheduled/posted content.
- Buyer learns what should be built, not just that "AI needs workflow."
- Concrete operating scene before abstract diagnosis: name the input formats, wrong/missing details, system-of-record need, and owner handoff.
- Customer/operator behavior stays realistic: the best teardown often adds a cleaner intake layer without asking customers to change how they already send work.

Strong shape:
`[Company/event] just showed a problem [buyer] already recognizes: [plain bottleneck]. [Concrete input scene]. [System] still needs [clean output/check/owner/confirmation]. The workflow I would build starts with [desk/router/queue]. It reads [inputs], extracts [fields], checks [systems/rules], drafts [output], routes exceptions, and preserves the source. [Customers/operators] keep working normally. [Buyer] gets [cleaner handoff] before [bad data/missed work] hits [system of record].`

---

## LinkedIn Post Format Rules

- **Length:** 3–6 short paragraphs (Monday: can be 1–3 sentences). Each paragraph = 1–2 lines max.
- **Line breaks:** blank line between every paragraph
- **Hook line:** first line must grab attention by naming a buyer-recognizable workday pain, not a generic AI category debate.
- **Default consulting structure:** concrete operational scene → specific examples → plain diagnosis → where AI fits → clean outcome. Buyer pain first, AI second, JT POV last.
- **Friday buyer-facing rule:** Prefer hooks like “Weekly status meetings might be the most expensive meeting on your calendar” over abstract hooks like “Most businesses do not need an AI chatbot.” Start with meetings, handoffs, approvals, stale reports, duplicate entry, ownerless requests, inbox/spreadsheet/portal sprawl.
- **No outreach-meta by default:** Do not discuss JT's prospect research, lead enrichment, buyer-channel validation, or outreach strategy on LinkedIn unless writing explicitly for a sales-ops audience.
- **No content-ops reveal by default:** Do not discuss JT's internal content generation, publishing system, swipe mechanics, posted logs, state files, or content automation on LinkedIn. That may be useful for internal build discipline, but it weakens the public trust surface.
- **No proof-hygiene standalone posts:** Removing client names, cleaning public proof, hiding private details, or fixing attribution is internal trust discipline, not a post-worthy idea by itself. Use it only as a support line inside a real buyer problem, shipped client outcome, or permission-safe case study. Never deliver "public proof/privacy cleanup" as the main LinkedIn/X recommendation.
- **No too-casual LinkedIn:** do not post "quick update," "small win," "built this weekend," "been playing with," "not gonna lie," "nothing crazy," "pretty cool," "vibes," "ship it and see," or app/build diary updates unless they are converted into client/employer-facing proof. LinkedIn should still sound like JT, but the reader should leave with trust, not just awareness that JT was building.
- **Avoid AI-generated thought-leadership smell:** no “AI chatbot” contrast hooks, no “exception layer” phrasing, no vague “messy work” language, no stacked rhetorical lists unless grounded in a concrete workflow.
- **Originality over acceptable:** every weekly slot must clear a 45-day semantic repeat check. Rewording a familiar angle is still a failure. Current hard-block phrases/angles: “best first AI project / least glamorous,” “handoff everyone checks manually,” “gets risky when...live in different places,” “exception layer,” “autonomous content system,” “state file,” “stop condition,” content-system/process transparency, and public-proof/privacy cleanup as standalone content.
- **Contrarian setup ban for all JT content:** do not use “the blocker is not X, it is Y,” “not look what this tool can do, more like…,” “not X, but Y,” the two-sentence “X is not just Y. It is Z.” variant, or repeated-noun reveals like “The risk is not X. The risk is Y.” This is banned across LinkedIn, X, reminders, client-proof posts, product-builder posts, and methodology/trust posts. Start with the positive claim, concrete scene, machine, workflow, owner, number, or business constraint.
- **Question 5 sentence-shape ban:** do not use "gets solved with a hire," "X don't Y, they Z," statement-colon hook lines, or "X happened/changed/worked when Y" as a closing pattern. These sound like generated reflection, not JT's natural voice.
- **Generic importance phrase ban:** never write “matters more than people think,” “people underestimate,” or “that part matters” unless replaced with the specific business reason.
- **No hashtags.** They suppress reach.
- **No emojis** unless they serve a specific purpose (rarely)
- **End:** clean insight OR a direct question. Never "DM me" or "link in bio"
- **Specificity rule:** Replace every vague claim with a number or proper noun. "Saved time" → "Replaced 18 hrs/week of manual StreetEasy searches."

---

## X Post Format Rules

- **Lead tweet:** ≤ 240 chars. The hook IS the post.
- **Thread format:** `1/`, `2/`, `3/` Max 5 tweets.
- **Single tweet:** 6–15 words ideal for observations. Client-proof quote tweets can be longer when they include ownership, deployment detail, metrics, and market thesis.
- **Client-proof quote tweet shape:** ownership first → operational architecture → hard metric → vertical thesis → partner/client tag only when relevant.
- **Proof beats aphorism:** when someone else posts a concrete result JT built, do not answer with generic "AI businesses pay for" framing, "chatbots vs agents," or abstract category commentary. Say JT built it, name the real-world setup, cite the numbers, and connect it to the buyer vertical.
- **Architecture detail is a feature:** include concrete deployment facts when they make the result feel real: mini PC, client office, existing systems, inbox, tracker, PDF workflow, daily summary, approval loop, 24/7 workflow. Specific machinery beats slogan language.
- **Good client-proof X pattern:** "Built this AI workflow for [person/company]." Then 1-2 concrete deployment lines, 1 line of measured outcome, 1 line of vertical POV.
- **No hashtags.** No "🧵 Thread below."
- **Tone:** slightly more casual than LinkedIn, punchier, more direct
- **End of thread:** clean conclusion line, no "follow me for more"

---

## Forbidden Words (zero exceptions across all platforms)
**Jargon:** utilize, synergy, ecosystem, scalable, streamline, actionable, bandwidth, holistic, innovative, robust, cutting-edge, best-in-class, thought leader, value-add, paradigm, granular, deliverable, upskill, touchpoint, disruptive

**AI consulting specific:**
implementation excellence, transformative, leverage (as buzzword), solution, optimize, strategize, proactive, learnings, unpack, unlock (as buzzword)

**Filler:** at the end of the day, in terms of, it is important to note, that being said, in order to, here's the thing

**Never use:** em dashes (—), excessive question marks, exclamation points, "No X. No Y. Just Z." tricolon negation

**Never use sentence shapes:** "X don't Y, they Z"; "The question that changes every build: ..."; "X happened/changed/worked when Y" as the closing line; "gets solved with a hire"

**Stop Slop delta adopted 2026-06-07:** Use `scripts/jt_voice_guard.py` to catch the parts of `hardikpandya/stop-slop` that improve JT content without flattening his voice:
- false agency: data, markets, workflows, decisions, complaints, bets, or culture acting like people
- narrator-from-distance phrasing: "people tend to," "nobody designed this," "this happens because," "this is why"
- vague declaratives: "the stakes are high," "the implications are significant," "the reasons are structural," "the consequences are real"
- Wh-opener setups: "What makes this hard is...," "Why this matters...," "How teams should think..."
- pull-quote endings: "That's the lesson," "That's the tradeoff," "X is the new Y"
- high-confidence passive voice: "was created/generated/decided/reached" or "mistakes were made"

Do not adopt the repo's blanket bans on all adverbs, all passive voice, two-item lists, or ultra-short aphoristic rewrites. JT uses practical qualifiers and constraint stacks when they carry real judgment.

---

## What JT Never Does
- Preamble before the point ("Here's what I've been thinking about lately...")
- Summary at the end restating the post
- Hedging ("I think maybe," "from my perspective")
- Humblebragging ("Grateful to share that we...")
- Long explanations of things the reader can infer
- "We" or "our team" — JT is a solo operator
- Contrast pairs as standalone structural framing ("X isn't Y, they're Z") — banned across JT content unless JT explicitly asks for a contrarian take; the Two-Part Parallel is fine only when it states a functional distinction without reveal-language
- “The blocker is not whether X, it is whether Y,” “Not ‘look what this tool can do,’ more like…,” “X is not just Y. It is Z.,” and “The risk is not X. The risk is Y.” patterns — stale AI-copy smell; replace with direct proof, operational architecture, or the concrete failure moment
- Generic importance phrases like “matters more than people think,” “people underestimate,” and “that part matters”
- @jts_14 or Twitter references in LinkedIn content

---

## X Algorithm Rules (source: docs/x-algorithm.md — apply to every X post)

The Phoenix algorithm ranks posts by weighted action probabilities. Replies > Reposts > Quotes > Likes > Bookmarks.

### Must-do for every X post:
1. **Reply hook first line** — the opening must make someone want to respond, agree, disagree, or add to. This is the #1 ranking signal. If the first line doesn't invite a response, rewrite it.
2. **No links in post body** — links suppress reach (user leaves X = negative signal). Move all URLs to a reply under the post, including jtsomwaru.com.
3. **Single sentence per line** — forces dwell time, which is a ranking signal. No paragraph walls.
4. **One repost-worthy line per thread** — something sharp, quotable, or counterintuitive that someone would want to put their name on.
5. **Lead tweet stands alone** — if the thread doesn't take off, tweet 1 still delivers value under 280 chars.
6. **No hashtags** — penalized in algorithm.
7. **Specificity over generality** — "AI saved a contractor 15 hrs/week" beats "AI saves businesses time."
8. **Never beg for engagement** — "like and repost if you agree" signals low-quality audience. Let the content earn it.
9. **Post at 8–10AM or 6–9PM EST** — first 30 minutes of velocity determines amplification.
10. **Reply to your own post immediately** after posting — adds content, signals active engagement, boosts the original.

### Timing (when scheduling matters):
- Morning window: 8–10AM EST
- Evening window: 6–9PM EST

---

## Audit Checklist (run on every draft)

### All content:
- [ ] Is this the right format for this day/platform?
- [ ] Strategic-fit gate: does this make JT look more credible to buyers/hiring managers? Block drafts that foreground a mistake, inflated claim, correction, apology, weak metric, or credibility repair unless JT explicitly asks for that postmortem angle.
- [ ] Did you check recent/proven references for this exact platform + niche + format before drafting?
- [ ] Did you avoid cross-platform/niche leakage unless explicitly labeled as adjacent inspiration?
- [ ] Did you extract the mechanic instead of copying the wording/persona?
- [ ] Did you translate the reference through JT's operator voice before writing, instead of copying the creator's posture?
- [ ] Did you replace generic outcomes with concrete operational detail, numbers, queues, systems, roles, or failure modes wherever possible?
- [ ] Does the draft breathe: short opening, clean paragraph breaks, one idea per paragraph, and a final line that lands without engagement bait?
- [ ] Does this sound like JT, not the source account or a generic creator?
- [ ] Does it start with the point, not the setup?
- [ ] Does it include at least one verifiable first-person specific when credibility is the point: a number, artifact, deployment environment, named tool decision, failure, client/operator scene, or before/after result?
- [ ] Does it use any forbidden words?
- [ ] Is there any preamble that can be cut?
- [ ] Does it make a claim the reader has to think about?
- [ ] For LinkedIn Wed/Fri: is there a specific number or proper noun?
- [ ] Platform check: does the content belong on THIS platform?
- [ ] LinkedIn consulting check: does the hook start with a concrete buyer pain a nontechnical SMB operator recognizes from their workday?
- [ ] LinkedIn consulting check: is AI introduced only after the operational problem is clear?
- [ ] LinkedIn consulting check: did you avoid outreach-meta and generic “AI chatbot” contrast framing?
- [ ] Contrast/reveal ban: did you avoid “not X, it’s Y,” “not X but Y,” and “X is not just Y. It is Z.” framing across the entire draft?

### X only (algorithm compliance):
- [ ] First line invites a reply?
- [ ] No links in post body?
- [ ] Single sentence per line?
- [ ] One repost-worthy line?
- [ ] Lead tweet ≤ 280 chars and stands alone?
- [ ] No hashtags?
- [ ] If quote tweeting a client result JT built, did it lead with ownership, include deployment detail, cite the metric, and end with a vertical thesis instead of a generic AI aphorism?
- [ ] Volume gate: is this the one strongest post for this audience/window? If not, bank it instead of posting.
- [ ] Originality gate: does this contain JT-specific proof, data, build experience, or a verified source? If it is just a copied swipe pattern with new nouns, block it as slop.
- [ ] Safety gate: no ragebait, conspiracy framing, NSFW/gore/violence bait, or advertiser-hostile angle.

---

*Last updated: 2026-06-07 (JT voice evidence corpus + voice guard added) | Framework: JT correction-derived voice evidence + platform-specific depth model + X Phoenix algorithm*
- **jtsomwaru.com AI Operations Diagnostic Reposition (2026-05-05):** Updated JT's personal site from generic AI Implementation Specialist framing to AI Operations Diagnostic / ops-heavy business workflow implementation. Added who-I-help, diagnostic front door, outcome-led services, and AI-search metadata. Build + lint passed; commit `2d0bb2a` pushed; production verified with updated hero/metadata.
- **Nash Satoshi Methodology Page (2026-05-07):** Added and shipped `/methodology` explaining the 4-model crypto game-theory ranking system, with sitemap/robots/llms.txt exposure. GitHub synced at `5473082`; build/typecheck passed; production confirmed live. Content angle: trust pages are distribution assets for AI-search, not just documentation.

## Proof Points

| Date | Proof Point | Verified Detail | Demonstrates | Status |
|---|---|---|---|---|
| 2026-06-06 | Plan Review Pack Skill + Human Signal Workflow | Added validated `plan-review-pack` skill, Client OS review-pack template, AI Context OS/consulting/workflow/proof/product/video wiring, portable `jt-operating-system` plugin update, autoresearch enrollment, and Mission Control next-use task for Altmark rent delinquency gate. | Agent operating-system design, client proof workflow packaging, human-as-signal delivery loops | Complete |
| 2026-06-03 | Crypto Full Analysis Atomic Pipeline | Added `scripts/run-full-analysis-pipeline.py`, moved X freshness preflight into `generate-full-analysis.py`, refreshed X research, regenerated June 3 artifacts, patched the 6AM cron to call the pipeline, and verified X guard plus full validator passed with `CRYPTO_FULL_ANALYSIS_OK`. | Atomic cron design, stale-evidence prevention, validator-gated delivery | Complete |
| 2026-06-03 | Crypto Full Analysis Deterministic Writer | Added `scripts/generate-full-analysis.py`, generated dated June 3 analysis/history/Telegram/allocation artifacts, patched the 6AM cron to call it, and verified X guard plus full-analysis validator passed for 24 coins, 6 held positions, and 25 X entries. | Cron reliability hardening, validator-gated artifact generation, financial-safety boundaries | Complete |
| 2026-05-27 | Altmark Rent Delinquency Testing Pack | Created Altmark rent delinquency acceptance checklist and runbook for sample-report testing, exception routing, human approval, rollback, and production cutover; Mission Control top task now points to the checklist. | Paid-client delivery control, property-ops workflow acceptance design, privacy-safe reusable IP capture | Complete |
| 2026-05-31 | jtsomwaru.com AI Context OS Sprint Service Page | Added `/services/ai-context-os`, homepage service routing, sitemap/llms/JSON-LD exposure, and an `ai-context-os` delivery skill with reusable sprint template; build/lint passed, pushed commit `9fc24fd`, and production returned HTTP 200. | AI context engineering offer packaging, GEO service-page build, reusable consulting IP system | Complete |
| 2026-06-01 | jtsomwaru.com Vista 1-100 Movie Rating Landing Page | Built `/1-100-movie-rating-app` with direct-answer copy, App Store CTA, screenshots, FAQ schema, SoftwareApplication schema, BreadcrumbList schema, sitemap exposure, and llms.txt coverage; build/lint/local route checks passed; commit `f09e09f` pushed and production returned HTTP 200. | Durable product-distribution page, AI-search/GEO app marketing, Vista growth infrastructure | Complete |
| 2026-06-01 | jtsomwaru.com Vista Movie Taste Profile Landing Page | Built `/movie-taste-profile-app` with direct-answer copy, App Store CTA, Vista screenshot, FAQ schema, SoftwareApplication schema, BreadcrumbList schema, sitemap exposure, llms.txt coverage, and cross-linking from `/1-100-movie-rating-app`; build/lint/local route checks passed; commit `eb983d3` pushed and production returned HTTP 200. | Product SEO clustering, AI-search/GEO app marketing, internal-link compounding | Complete |
| 2026-06-01 | jtsomwaru.com Vista Letterboxd Precise Ratings Landing Page | Built `/letterboxd-alternative-precise-ratings` with careful Letterboxd-adjacent positioning, direct-answer copy, App Store CTA, Vista screenshot, FAQ schema, SoftwareApplication schema, BreadcrumbList schema, sitemap exposure, llms.txt coverage, and cross-links from both existing Vista SEO pages; build/lint/local route checks passed; commits `61ba431` and `6640cbf` pushed and production returned HTTP 200. | Guardrailed comparison SEO, AI-search/GEO product-page clustering, product positioning discipline | Complete |
| 2026-06-01 | jtsomwaru.com Vista Private Movie Rating Landing Page | Built `/private-movie-rating-app` with private personal tracking positioning, direct-answer copy, App Store CTA, Vista screenshot, FAQ schema, SoftwareApplication schema, BreadcrumbList schema, sitemap exposure, llms.txt coverage, and reciprocal links from the existing Vista SEO pages; lint/build/local rendered checks passed; commit `f8f8149` pushed and production returned HTTP 200. | Privacy-positioned product SEO, AI-search/GEO page clustering, unsupported-claim avoidance | Complete |
| 2026-06-01 | jtsomwaru.com Vista Rate Movies Out Of 100 Landing Page | Built `/rate-movies-out-of-100` with 100-point rating-method copy, App Store CTA, Vista screenshot, FAQ schema, SoftwareApplication schema, HowTo schema, BreadcrumbList schema, sitemap exposure, llms.txt coverage, and reciprocal Vista cluster links; final source verifier, lint, build, and production checks passed after commits `6ff6610`, `5111a61`, and `a24616f`. | Educational product SEO, AI-search/GEO page clustering, verification hardening | Complete |
| 2026-05-19 | App Marketing Share Artifacts Batch 5 | Built Nash `/receipts/weekly` PNG receipt generator and Glow Product Verdict Card MVP; Nash `npm run check` + `npm run build` passed, Glow `npm run build` + `npm run lint` passed. | Product-led app distribution assets, repo-aware AI coding-agent orchestration | Complete |
| 2026-05-27 | jtsomwaru.com n8n Automation Service Page | Built `/services/n8n-automation` with FAQ schema, Service JSON-LD, sitemap exposure, homepage links, llms.txt coverage, and an updated Drive roundup packet; verifier/build/lint and production live checks passed. | AI-search/GEO service-page build, proof-safe consulting positioning, citation-ready outreach infrastructure | Complete |
| 2026-05-14 | jtsomwaru.com Public Proof Privacy Pass | Anonymized client names and removed exact proposal amounts from site proof copy; production verified clean for Aya/Altmark/Lady D/exact amount hits. | Public proof hygiene, privacy-safe case-study packaging | Complete |
| 2026-05-14 | jtsomwaru.com Client Outcome Attribution Fix | Corrected Aya vs Altmark site attribution, added Altmark local-first automation detail page, restored Adversight AI to Apps; build/lint passed and commit `25b9563` pushed. | Proof attribution discipline, client-work packaging, portfolio inventory preservation | Complete |
| 2026-05-14 | jtsomwaru.com Positioning + Roles Update | Shipped balanced Work buckets, updated niches/About/tools, new `/roles` page, footer links, and AI-search metadata; build/lint passed; pushed commit `fce1480`; production `/` and `/roles` returned HTTP 200. | Consulting positioning, proof-tier hygiene, recruiter/buyer path separation | Complete |
| 2026-05-10 | jtsomwaru.com AI Operations Systems Overview | Added homepage capability matrix + AI Ops Teardowns section to make consulting range legible fast; pushed commit `5c163af`. | Buyer-facing site positioning, AI ops proof packaging | Complete |
| 2026-05-10 | jtsomwaru.com StreetEasy Metric Correction | Tightened homepage claim from “10+ hrs/week” to “4 hrs / 2 weeks” to match project detail data; build/lint passed and pushed commit `a164e4b`. | Proof discipline, conservative client-outcome claims | Complete |
| 2026-05-07 | Nash Satoshi Methodology SEO Page | Shipped public `/methodology` page with sitemap/robots/llms.txt exposure; GitHub synced at `5473082`; `npm run check` and `npm run build` passed. | AI-search/GEO product trust page | Complete |
| 2026-05-07 | jtsomwaru.com Vista 1–100 Movie Rating SEO Page | Added SEO page for `1–100 movie rating app`; `npm run build` and `npm run lint` passed; commit `cd7ab18` pushed; production verified in daily note. | Durable app-distribution asset from social insight | Complete |
| 2026-05-05 | jtsomwaru.com AI Operations Diagnostic Reposition | Production site updated around AI Operations Diagnostic, workflow segments, diagnostic offer, and AI-search metadata; build/lint passed and commit `2d0bb2a` pushed. | Consulting positioning, buyer-facing AI ops offer | Complete |
| 2026-05-05 | jtsomwaru.com AI Operations Blog Library | Added 6 buyer-intent / AI-search blog routes; build/lint passed and commit `143d839` pushed. | GEO strategy, buyer-intent content architecture | Complete |
