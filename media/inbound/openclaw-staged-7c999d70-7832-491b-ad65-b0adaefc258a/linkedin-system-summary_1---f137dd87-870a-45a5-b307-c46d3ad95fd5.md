# LINKEDIN CONTENT SYSTEM: SUMMARY FOR REVIEW
**Current as of 2026-08-25. Replaces an earlier version describing a three-lane, three-post-per-week system.**

This describes a LinkedIn content system as it exists today, written to be handed to a reviewer for critique. Everything the reviewer needs is in this document.

---

## 1. Who this is for, and the situation that shapes every decision

The author is an independent AI implementation consultant in Brooklyn, NY, operating under his own name. He installs AI systems that catch errors a team cannot see, and is moving to a model where he is paid monthly to prove those systems are still catching them.

**The financial reality, because it explains the whole design:**

- Collected roughly $19,400 across seven payments in the first 7.7 months of 2026.
- Two counterparties account for most of that. One month is nearly half of Q3. August was zero.
- Zero subscribers on any recurring tier. That is the core diagnosis.
- The practice has not covered its own burn in any month but one.
- Revenue slope is up: max ticket went $1,500, then $6,250, then $10,800.

**Two tracks are running simultaneously.** A live job search for AI implementation roles at $150,000-plus, and a test of whether the practice can convert existing clients to retainers. Three dated gates decide between them, the last on 2026-10-15.

**The metric that governs everything:** two priced conversations per week, where a real buyer received a real number that included a recurring line. Not proposals sent, not calls taken.

**A named failure pattern.** Three independent reviews reached the same conclusion: the author substitutes high-quality preparation for the ask. Evidence includes a finished compliance product with no named buyer, an accuracy harness with zero subscribers, an outbound system never sent at volume, and three paid clients with nothing priced in front of them. The content system was itself an instance of this pattern, which is why it was cut down rather than expanded.

**Current LinkedIn scale:** roughly 350 followers, three published posts, no meaningful performance data.

---

## 2. What LinkedIn is for, and what it is explicitly not for

**LinkedIn is a due-diligence surface, not a lead engine.** At 350 followers, organic reach is a few dozen relevant impressions per post. Lead generation from LinkedIn requires an audience the author cannot build before his October gate, and every hour spent building it is an hour not spent on priced conversations.

**The profile is the artifact. The feed is a supporting signal** proving the person is real and active.

**Three named readers, in priority order through 2026-10-15:**

1. A recruiter or hiring manager. The job process is live, so this is guaranteed and dated.
2. A buyer who already received a quote and is checking the author before deciding.
3. A referral target's network, when an existing client mentions his name.

All three are due diligence. None are audience.

**Audience growth is not a goal in this window.** It is deferred, not rejected. If the practice clears $100,000 or a role lands, 2027 is the year to build one.

**Property lead generation moved off the feed entirely.** Bylined articles in property trade association newsletters reach thousands of exactly the right readers. Domain material that would have gone to 350 people in the feed becomes raw material for those instead.

---

## 3. Positioning

The feed carries the strongest available proof regardless of vertical, through 2026-10-15.

This suspends an earlier property-only rule. The reason: the strongest completed engagement is non-property, a fixed-scope build for a marketing analytics firm whose technical lead independently re-verified all deliverables on their own systems before accepting and put written acceptance in front of their executive team. A property-only feed hides that from the reader most likely to look in the next four weeks.

Property remains the general public lean. Exclusivity is suspended. Revisit 2026-10-15.

The profile stays broad across verticals. These were decided separately.

---

## 4. Architecture

Nothing is auto-posted. A human writes, edits, and publishes every post.

**Two skill files**, markdown instruction files read by a coding agent at generation time.

- `linkedin-content/SKILL.md`, roughly 300 lines after a 21 percent reduction: purpose, the single lane, hard rules, formatting, card spec, hashtags, document titles, cadence, time cap, priority gate, positioning, output format, post-publication loop, monthly review, and a frozen-changes section.
- `jt-voice/SKILL.md`, roughly 375 lines: sentence mechanics, openings, vocabulary, punctuation, stance, post structures, an AVOID list of specific machine-writing tells paired with rewrites, verbatim sample lines, and a Corrections section that grows from published-versus-draft diffs.

**Data files**, in a folder deliberately outside any public git repo because they contain anonymized client material.

- `proof-ledger.jsonl`: one record per delivered engagement. Six records, of which four are publish-ready. Each carries an anonymized descriptor, the problem, the system built, the human-approval point, before and after states, an optional metric, gate flags, and a `same_client_as` cross-reference.
- `lessons.jsonl`: 64 operating rules extracted from the author's own engineering practice files, each with a rule, what broke, what he does now, why it matters, and an evidence tier.
- `corrections.jsonl`: one entry per published post holding the draft, the published version, and what changed.
- `outcomes.csv`: per-post metrics, hand-logged.
- `lint.py` plus a banned-noun list: catches exact counts, monetary and temporal quantities, business nouns, and proper nouns in any record.

**One design system** in a visual design tool, saved and reused. Five card masters at 1080x1350, exported to PDF for LinkedIn document posts.

**A print pipeline** documented in a separate runbook rather than in the skill file, including invariants enforced at conversion time because the design tool silently dropped the contact line and type sizes twice.

---

## 5. The lane

There is one lane: **verified install proof.** At most one post per week, and often none.

**Two allowed sources.**

**Source 1: a publish-ready ledger record.** What was breaking, what runs now, where the human approves, and how correctness is proven over time. Carousel only if a card set can be produced inside the time cap. Uses the record's anonymized descriptor exactly as written. Uses a number only if that record's metric is marked permissioned.

**Source 2: a delivery discipline rule** from the lessons corpus, stated in the domain where it actually happened. Never recast as an invented scenario in another vertical. Text only. For the first ten posts drawn from this source, only records citing a concrete failure event are eligible, not records describing a generic failure mode.

Selection rules carried over: no two consecutive posts from the same source file, and a cap on how often the largest source file can be drawn from in any rolling five.

**Deleted in the last revision:** a weekly company teardown lane, a weekly domain briefing lane rotating through eight reference files, a recap lane, and a three-post-per-week cadence. All four existed to fill a schedule the proof supply could not support.

---

## 6. Hard rules

1. Never state a fact, descriptor, or number that is not in a source file or a nameable source. No estimates.
2. Never name a client, a partner, a revenue or pricing figure, an infrastructure detail, or any legal material.
3. Every workflow shown includes its human-approval point. Not optional.
4. The first 210 characters must stand alone before the fold and must not be a rhetorical question or a hook cliche.
5. Exactly three hashtags, at the end only. Slot one is the domain the work actually happened in. No links in the body; links go in the author's own first comment.
6. If a compliant draft is not possible, the agent outputs NO COMPLIANT DRAFT and the reason. An empty slot is acceptable. A fabricated one is not.
7. Never build a post on a premise a competent operator would reject about themselves. Premise instead on structural risk, which is true of well-run offices too: what depends on one person remembering, what fails without announcing itself, what breaks when someone is out.
8. "Saves time on manual work" is banned as a value proposition. Every vendor says it and it loses to "my person handles it fine."

**Formatting.** No paragraph longer than three sentences. A list of up to three lines is allowed, every line a complete sentence, never a fragment, one list maximum per post. No em dashes, exclamation points, or emoji. Ceiling of 1,500 characters with no minimum and an explicit instruction never to add content to reach a length.

**Body versus deck.** On carousel posts the body must not restate the workflow steps on the cards, but must contain at least one concrete mechanism detail naming what lands where or what gets stored. Abstraction like "routes to the right owner" is what separates someone who built one of these from someone describing one.

**Closings.** The last line may never restate the premise. A check the reader can run on their own operation in five minutes is preferred but not required.

---

## 7. The visuals

**Design intent:** the buyer reads restraint as competence and flourish as vendor risk. The system is deliberately the least expressive thing the author could build. Every decision was a subtraction.

**Format:** five masters, 1080x1350 portrait, exported to a single PDF and uploaded as a LinkedIn document post rather than images.

- **A. Title frame.** One sentence naming the operational failure. Hard cap of 12 words.
- **B. Workflow frame.** Exactly four numbered steps, maximum 18 words each. Step four always carries the human-approval marker, written in second person to the reader. The marker's position is hardcoded in the template, which is why the step count is fixed.
- **C. States frame.** Two columns, Before and Now, three lines each, maximum 12 words. Situational rather than numeric.
- **D. What stays human.** Four lines. The first three are fixed and identical on every card ever published: anything that moves money, anything with a legal deadline, anything a lawyer would want a signature on. The fourth is post-specific.
- **E. Closing frame.** The one-line positioning and contact details. A standing call to action was removed, on the grounds that a checkout button on every artifact reads as vendor behavior to both a wary operator and a hiring manager.

**Visual rules:** cream background, one accent color appearing in exactly two places across the set, the approval marker on frame B and the closing on frame E. Geist display, Inter body. WCAG AA. No icons, imagery, screenshots, gradients, charts, badges, additional colors, or motion.

**Screenshots are never used.** Any artifact shown is rebuilt from scratch with invented dummy data, because blurring is not sanitization.

---

## 8. The weekly operation

One prompt, run once a week, roughly 30 minutes total including replies.

1. **Priority gate first.** The agent asks whether a priced follow-up to a past client is unsent, and whether this week's two priced conversations have happened. If a quote is unsent, it outputs NO POST and stops. Content does not run ahead of quotes.
2. **If the gate clears,** it reports what sources are actually available and recommends one of three outcomes: no post this week with a reason, one draft from a ledger record, or one draft from a discipline rule.
3. **At most one draft is produced.** It is checked line by line against the AVOID list, and returns the source id, character count, a proof-safe verdict, three hashtags, and a document title if cards are needed.
4. **After publishing,** the published text is pasted back. The agent diffs it against the draft, logs the difference, and when the same kind of edit appears three times it becomes a rule in the voice skill.

**Time cap:** 30 minutes per week, plus one additional hour on a week where a build note ships with cards. If cards cannot be finished inside that, text ships or the week is skipped.

**Cadence:** no fixed day. Skip weeks are normal and expected. Never post on a day a client deliverable is due. One 30-minute reply window on a day a post goes out.

**Monthly coverage review,** separate from performance. It reads the month's posts and asks what a stranger would conclude the author is good at, what they would wrongly conclude he cannot do, which reader was better served, what claimed capability was never demonstrated, and whether anything repeated.

**Frozen:** no new lanes, no new rules, and no structural changes before 2026-10-15.

---

## 9. Anonymization

Client material passed two adversary review rounds with a deliberate round cap.

In the first, an agent reading only the sanitized lessons corpus reconstructed a system profile and narrowed the client to four candidate verticals using structural vocabulary alone, with no proper nouns present. In the second, reading all records at once, it assembled cross-file profiles and identified which individually harmless records were load-bearing in each.

Both rounds were applied as rewordings rather than deletions. A lint script was written to catch the same classes going forward. The same standard was later applied to the author's website, which turned out to be less sanitized than the ledger.

One ledger record is blocked with a gate named `not_activated_in_production`, which clears only when the system is actually running, never by supplying a date. That naming was deliberate: the original gate name looked like paperwork and invited a future session to fill in a date and publish a claim that something runs when it does not.

---

## 10. State of things

- Three posts published. One correction entry logged. The learning loop has fired once.
- Four publish-ready ledger records. At one post per week and often none, that is roughly four to six posts total through 2026-10-15.
- The next planned post is the marketing analytics engagement, now publishable in the feed since vertical exclusivity is suspended.
- Deliberately deferred: per-lane source-health tracking, any second vertical lane, and any further automation before post 20.

---

## 11. What would be most useful to critique

Honest criticism, not reassurance. Lead with what is wrong.

- Whether one lane at one post per week is the right answer given a live job search where recruiters will open the profile in the next four weeks, or whether it is now too quiet.
- Whether the profile-is-the-artifact framing is correct, and what specifically should be on the profile that this document does not mention.
- Whether the priority gate is a real safeguard or a way of guaranteeing the system never runs.
- Which voice and formatting rules are doing real work, which are cosmetic, and which are producing worse writing. The system accumulated many prohibitions across several sessions and may be over-constrained.
- Whether the five card frames still carry the right argument now that the only carousel source is a shipped build.
- Whether moving property lead generation to trade newsletters is right, or whether it trades a channel the author controls for one he does not.
- Whether anything in this system is still an instance of the substitution pattern in section 1.

**Not useful:** predictions about engagement rates, algorithm behavior, or which content will perform. There is no data to ground those, and the system is not optimizing for reach.
