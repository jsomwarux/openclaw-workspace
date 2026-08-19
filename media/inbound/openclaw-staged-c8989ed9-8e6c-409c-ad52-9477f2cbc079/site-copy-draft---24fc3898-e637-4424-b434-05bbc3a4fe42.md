# jtsomwaru.com homepage copy: replacement draft

Drafted 2026-08-18. Positioning: NYC and NJ property management and real estate as the
named primary market. Through-line: method and verification. Nothing here claims a
proprietary, reusable, or productized system.

## Corpus load report

| Input | Status |
|---|---|
| `~/Desktop/proof-engine/corrections.jsonl` | Present. **One** correction record (2026-08-11 SiteCompli teardown) plus a header comment. This is a much thinner correction set than the brief assumes. I did not invent additional records. |
| `~/Desktop/proof-engine/lessons.jsonl` | Present. 65 records, `L-001` to `L-065`. |
| `~/Desktop/proof-engine/proof-ledger.jsonl` | Present. `PP-000` template plus `PP-001` to `PP-005`. |
| `~/Desktop/proof-engine/outcomes.csv` | Present but **empty of data**: header row only, zero rows. Nothing citable. |
| `jt-voice` skill | Read from `~/Desktop/jt-toolkit/methodology/skills/jt-voice/SKILL.md`. Its own `## Corrections` section carries six rules derived from the same 2026-08-11 diff, so it is effectively a second view of `corrections.jsonl`. Cited as `[jt-voice corr 2026-08-16]`. |
| `design-system` / `b2b-trust.md` | Read. Used for register only. |
| Current live homepage | Read from the repo, read-only. No repo file was modified. |

**Publishable proof available.** Only three ledger records are `publish-ready`:
`PP-001` (a New York City property management firm, COI expirations, shipped 2026-06-05),
`PP-003` (a construction firm, progress dashboard, shipped 2026-07-09),
`PP-004` (a solo recovery coaching practice, website, shipped 2026-07-03).
`PP-002` and `PP-005` are `blocked`. Every claim below is sourced to a `publish-ready`
record, to a lesson, or to nothing at all.

**No numbers appear in this draft.** All five ledger records carry `metric: null` and
`metric_permissioned: false`, so under README Rule 2 there is no figure I am allowed to
publish. Sections are written as workflow states instead, which `b2b-trust.md` §5.2
explicitly sanctions: "If no number exists, present workflow states. Structure is proof
even when numbers are absent."

---

# 1. Hero

### Current live copy

> **Headline:** Recurring manual work is eating your team's week. I replace it.
>
> **Subhead:** For teams with work stuck across inboxes, spreadsheets, documents, CRMs,
> websites, and disconnected tools. I map the workflow, find the bottleneck, and ship the
> dashboard, automation, or AI-assisted system that makes the work visible and easier to run.
>
> **Eyebrow row:** $1,500 Workflow Audit · Dashboards + automation · Property, construction, and ops proof

---

### Variant A. The week gets smaller

**Angle bet:** the reader is tired. What they want to know is whether the recurring work
comes off their plate. Proof and safety are reassurance, not the lead.

> **Headline**
> I build the system that runs the work your team repeats every week.
>
> **Subhead**
> For NYC and NJ property managers, owners, and ops-heavy teams with work moving by hand
> between inboxes, spreadsheets, and property software. The build runs in production, shows
> what is stuck, and stops for a human before anything touches a tenant, a vendor, or money.
>
> **Eyebrow row**
> $1,500 Workflow Audit · Running in production for a NYC property management firm · Sensitive rows stay human-approved

**Citations**

- Ownership opening "I build" rather than a problem statement: `[jt-voice §2]` allows
  "Built this / installed this / deployed this, only when proof exists," and `[jt-voice §5]`
  "Lead with ownership only when proof exists." Proof exists: `[PP-001]`, `[PP-003]`, `[PP-004]`.
- "stops for a human" not "stops for a person": `[jt-voice corr 2026-08-16]` "The approval
  actor is a human, not a person." Published line: "The owner update is the step a human
  approves before it sends."
- The closing triad "a tenant, a vendor, or money" copies the shape of the only line
  confirmed as actually posted, `[post 2026-08-11 opening]`: "A delinquency balance, a lease
  date, and a deposit chase should not move through the same AI workflow without a decision
  trail." `[jt-voice §8 gaps]` notes this is the single confirmed-posted line, so its shape
  is the highest-grade evidence in the file.
- "Running in production for a NYC property management firm" is the exact `anon_descriptor`
  from `[PP-001]`, which is `publish-ready` with `client_named_ok: false`. Every fact in it
  is literally true, per README's descriptor rule.
- "Sensitive rows stay human-approved" restates `[PP-001] human_approval_point`: "Exceptions
  are human-approved; routine outreach is automated." It does not claim every message is
  human-approved, which would fail the `human_approval_framing_accurate` gate.
- The eyebrow answers three of the four `[b2b-trust §2]` ten-second questions: is it real,
  is it safe, what do I do next.
- Vocabulary check against `[jt-voice §3]`: workflow, system, exception, approval, production
  are all on the Use list. No banned word appears.

**Self-grade: 4 of 5.** The headline and the closing triad read like him. The subhead is a
touch longer than his 7 to 18 word default `[jt-voice §1]`, but it carries a constraint
stack, which §1 permits up to 35 words.

**Weakest line:** "shows what is stuck." It is the vaguest clause in the block and it is
doing real work. "Stuck" is a feeling, not a workflow object. `[jt-voice §7]` demands "a
concrete object, owner, metric, approval rule, or buyer scene." A stronger version names
the object: "surfaces the expired and the overdue." I left "stuck" because it generalizes
across all three cards below it, but it is the seam.

---

### Variant B. You will find out when it stops being right

**Angle bet:** this reader is not tired, they are suspicious. They have been sold automation
before. `[b2b-trust §1]` describes them as "specifically wary of unsupervised AI touching
sensitive data." The thing worth promising is not that it runs, but that they will know
when it stops working.

> **Headline**
> I build the automation your property team runs on, and the check that catches it when it drifts.
>
> **Subhead**
> For NYC and NJ property and real-estate operators. I map how the work actually runs, build
> the workflow that carries it, and measure it against records the workflow did not write.
> Routine sends go out on schedule. Every exception goes to a human.
>
> **Eyebrow row**
> $1,500 Workflow Audit · Built for NYC and NJ property operations · Checked against records the system did not write

**Citations**

- "measure it against records the workflow did not write" is `[L-044]` verbatim in substance:
  "Anchor at least one number in a fact from outside the system being measured. A system
  grading itself with its own data will always agree with itself, right up until reality
  disagrees." Supported by `[L-045]` (re-derive a reported figure by hand from the raw source).
- "the check that catches it when it drifts" is `[L-065]`: "A wrong number that looks
  reasonable costs more than a visible gap, because nobody knows to question it." Also
  `[L-011]`: "A check that has never once failed offers no evidence that it would catch the
  problem coming back."
- "Routine sends go out on schedule. Every exception goes to a human." is the two-sentence
  form of `[PP-001] human_approval_point` and satisfies the ledger's
  `human_approval_framing_accurate` gate, which requires stating the split plainly rather
  than implying total human approval.
- Short verdict sentences after a longer clause: `[jt-voice §1]` "Use short sentences for
  verdicts, transitions, and proof points," with verbatim models "Some rows are routine."
- No competitor or category claim appears anywhere, per `[corrections.jsonl 2026-08-11]`,
  whose note records cutting "the unsourceable claim about SiteCompli's pricing and target
  market" and narrowing the category verdict to the product itself.

**Self-grade: 3 of 5.** The method is his and the evidence is the strongest in the corpus,
but the headline asks a buyer to care about verification before they have agreed they have
a problem. This is the copy he would write on a Tuesday, not the copy that converts a warm
intro in ten seconds.

**Weakest line:** "and the check that catches it when it drifts." "Drifts" is doing a lot of
unearned work and is closer to vendor vocabulary than operator vocabulary.
`[corrections.jsonl 2026-08-11]` records exactly this correction in the other direction:
"cure window" became "correction deadline" because "legal shorthand and vague nouns both
hide the thing actually being tracked." "Drifts" hides the thing being tracked.

---

**Which one an 800-unit property manager repeats back to a colleague after one read:
Variant A.** They repeat "he builds the system that runs the work you repeat every week."
It maps onto a sentence they already say to themselves. Variant B's promise requires them
to first accept that their current automation might be silently wrong, which is a second
conversation, not a first one. `[b2b-trust §2]` is explicit that the entire job above the
fold is that a warm intro "must believe him in ten seconds," and B spends those ten seconds
introducing a problem the reader did not arrive with.

**Ship: Variant A**, with Variant B's "Every exception goes to a human" swapped in for A's
"stops for a human before anything touches a tenant, a vendor, or money" if the line tests
long.

---

# 2. Who this is for

### Current live copy

> **Headline:** Teams with important work stuck between people, tools, and spreadsheets.
>
> **Subhead:** The strongest first project usually starts with one named workflow, dashboard,
> or digital handoff that keeps aging, changing quietly, or waiting for one person to move it forward.
>
> **Card 1 (Ops-heavy teams with messy internal workflows):** Dashboards, automations, and
> AI-assisted workflows for recurring work trapped between spreadsheets, inboxes, documents, and approvals.
>
> **Card 2 (Construction & real-estate operators):** Field updates, market research, owner
> reporting, vendor follow-up, and project visibility systems built around how the team already works.
>
> **Card 3 (Property & family-office operations):** Focused audit and automation paths for COIs,
> rent readiness, lease renewals, vendor coordination, and sensitive back-office workflows.

---

### Variant A. Named by the workflow object

**Angle bet:** the reader recognizes themselves by the specific thing they chase. Vertical
vocabulary is the trust signal, so each card leads with the object and then says what gets
built for it.

> **Headline**
> Who this is for, and what gets built
>
> **Subhead**
> The first build is usually one workflow that runs every week and depends on one person
> being available. A few weeks later it runs on a schedule, and that person approves instead
> of doing.
>
> **Card 1. Ops-heavy teams with messy internal workflows**
> Recurring work moving by hand between a spreadsheet, an inbox, and whoever signs off. I
> build the dashboard or the workflow that carries it, and route every exception to the
> human who owns it.
>
> **Card 2. Construction and real-estate operators**
> Field updates, owner reporting, listings research, vendor follow-up. I build the job
> dashboard that reads the tracking sheet your team already keeps, and computes the headline
> completion figure from the detail underneath instead of from a summary cell someone set by hand.
>
> **Card 3. Property and family-office operations**
> COI expirations, rent readiness, lease renewals, and back-office work where the records are
> sensitive. I build it to run inside your own environment, with routine reminders going out
> on schedule and every expired or past-due row routed to a human.

**Citations**

- Every card names situation then build, per the brief's constraint. The verbs are all
  "I build," which `[jt-voice §5]` sanctions only where proof exists. Card 2 is `[PP-003]`,
  card 3 is `[PP-001]`, both `publish-ready`.
- Card 2's second clause is `[PP-003] human_approval_point` almost verbatim: "the headline
  completion figure is recomputed from the detail cells rather than showing the hand-set
  summary value, because that value went stale in practice." This is the single most
  specific publishable detail in the entire ledger and it is currently unused on the site.
- Card 3's split is `[PP-001] human_approval_point`: "The daily summary routes every skipped
  row and every expired or past-due certificate to the operators. The routine tenant
  reminders send on schedule without per-message human approval."
- "inside your own environment" rather than "local-first" or "self-hosted":
  `[corrections.jsonl 2026-08-11]` note, "Name the operational object in the operator's own
  words." A property manager does not say self-hosted.
- Vertical vocabulary as a deliberate trust device: `[b2b-trust §3]` section order item 1,
  "Vertical vocabulary is itself a trust signal: it proves insider understanding."
- Subhead avoids the word "quietly", which `[jt-voice §7 AVOID]` flags by name as a softener
  adverb ("The queue quietly stops moving"). The current live subhead uses it.

**Self-grade: 4 of 5.** Card 2 is the best writing in this document because it is the only
place a real, permissioned, weirdly specific operating decision reaches the page.

**Weakest line:** card 1's "and whoever signs off." It is the one card with no ledger record
behind it and it shows. It stays abstract because it has to cover everything the other two
cards do not, which is exactly the structural problem I flag at the end of this file.

---

### Variant B. Named by the failure shape

**Angle bet:** the reader does not identify by vertical, they identify by the way their
operation fails. Each card opens on a recognizable failure and then names the build that
answers it.

> **Headline**
> Where the first build usually lands
>
> **Subhead**
> Three shapes come up again and again. In all three the work is already happening, and it
> is happening in someone's head or someone's inbox.
>
> **Card 1. Ops-heavy teams with messy internal workflows**
> One person holds the workflow, and it moves when they get to it. I build the system that
> runs it on a schedule and puts what is waiting in front of the human who owns it, so the
> work stops depending on one person being at their desk.
>
> **Card 2. Construction and real-estate operators**
> The completion figure people quote in the meeting came from a cell somebody set by hand,
> and it went stale the moment the detail underneath it changed. I build the dashboard that
> computes it from the detail, which means it can disagree with what was typed, by design.
>
> **Card 3. Property and family-office operations**
> Nothing has complained, so everyone assumes the COI chase is still working. I build the
> renewal and expiration workflow, and I check it against records the workflow did not write.

**Citations**

- Card 2 is `[PP-003] problem` plus `[PP-003] human_approval_point`, compressed. The
  ledger's own words: "The completion figures people quoted came from a summary value
  somebody set by hand, and it drifted out of date the moment the detail underneath it
  changed." "by design" is the ledger's word, not mine.
- Card 3's opening is `[L-016]` inverted: "A status report with nothing behind it is
  indistinguishable from a false one until the customer finds the gap." The check is
  `[L-044]`, and `[L-045]` is the cadence behind it.
- Card 3 deliberately makes no claim about a specific client's monitoring engagement. The
  method is stated as JT's operating rule, not as a delivered outcome, because the only
  detailed write-up of that work in the corpus carries a hard publication gate at the top of
  the file and no permission has landed.
- Card 1 avoids the "not X, Y" reveal engine that `[jt-voice §7]` bans, by stating the
  failure and the build as two plain clauses rather than as a contrast.
- Opening on the operational failure rather than an explanation: `[jt-voice corr 2026-08-10]`,
  "Open with the operational failure, never with explanation," a rule added after three
  drafts were rejected for the same opening.

**Self-grade: 4 of 5.** Riskier and more his. Card 3's "Nothing has complained, so everyone
assumes" is the most JT sentence in this file.

**Weakest line:** the subhead. "Three shapes come up again and again" is a framework
announcement with nothing concrete in it, which is the exact tell `[jt-voice §7]` describes
as "Hooks that announce a framework instead of showing a scene."

**Ship: Variant A** for the cards, **Variant B's card 3 opening line** grafted in. A is the
safer register for a page a referrer forwards; B card 3 earns its place because it names a
failure mode the buyer has actually lived through.

---

# 3. Proof section headline and subhead

### Current live copy

> **Eyebrow:** Client Work
>
> **Headline:** Proof from real operating work.
>
> **Subhead:** The site does not need to claim magic. It needs to show that workflows have
> already moved from messy inputs into dashboards, recurring pipelines, local-first
> automation, audit logs, and approval paths.

The current subhead talks to the reader about the site. `[jt-voice §7]` cuts "internal
content-system transparency" and "public-proof hygiene" from public writing. Both variants
below remove it.

---

### Variant A. These are states, not stories

**Angle bet:** the reader wants to know what changed. Say what the cards are before they
read them, and disclose the absence of numbers rather than hoping nobody notices.

> **Eyebrow:** Client work
>
> **Headline**
> What was manual, what runs now, and who approves it.
>
> **Subhead**
> Three engagements, described as workflow states. Where a figure is missing it is because
> it was not measured in a way I can hand you.

**Citations**

- "described as workflow states" is `[b2b-trust §5.2]` verbatim policy: "If no number
  exists, present workflow states: what was manual, what runs automatically now, where the
  human approves. Structure is proof even when numbers are absent."
- The disclosure sentence is `[L-019]`: "State not yet verified rather than presenting an
  unverified claim as fact. An unmarked guess mixed in with confirmed facts destroys the
  value of the confirmed ones, because now none of them can be trusted on sight." Also
  `[L-016]`, "Never mark work complete without pointing to the evidence that it works."
- The absence is real, not rhetorical: all of `[PP-001]`, `[PP-003]`, `[PP-004]` carry
  `metric: null` and `metric_permissioned: false`.
- The headline is three plain noun clauses with no contrast engine, avoiding the
  `[jt-voice §7]` ban on "X is not just Y. It is Z."

**Self-grade: 4 of 5.** The disclosure line is the kind of thing he actually says. Sample
line 7 in `[jt-voice §8]`: "I am not sure that claim is strong enough to publish without a
cleaner proof path."

**Weakest line:** "Three engagements." It is a count, and it dates the section the moment a
fourth card ships. A durable version drops the number.

---

### Variant B. Somebody other than me signed off

**Angle bet:** the differentiator is not the work, it is who verified it. This is the
through-line stated at the top of the section rather than left for the cards to imply.

> **Eyebrow:** Client work
>
> **Headline**
> Built, handed over, and checked by someone who did not build it.
>
> **Subhead**
> These are described by what they do on an ordinary week, and by who catches them when they
> get something wrong.

**Citations**

- The headline is `[L-047]` compressed: "The party that builds the work never decides whether
  it is done. One party builds and a different one with no build history reviews and attacks;
  the completion signal is the reviewer verdict." Reinforced by `[L-051]`, "Whoever checks
  the work must not be able to change the work," and `[L-018]`, "Instruct a reviewer to break
  the work, never to confirm it."
- "who catches them when they get something wrong" points at the human approval point every
  ledger record is required to carry. README: "`human_approval_point` is required and is
  never null. If nothing in the system is human-approved, the record is not publishable at
  all."
- The subhead deliberately does **not** say "the interesting part is not the demo, it is what
  it does on an ordinary week." That shape is banned twice over: `[jt-voice §7]` contrarian
  reveal engines ("The risk is not X. The risk is Y") and `[jt-voice §7 AVOID]` "the useful
  question is uglier." The substrate draft contains this exact construction and I cut it.

**Self-grade: 3 of 5.** The angle is right and it is the brief's stated through-line, but
"checked by someone who did not build it" is at risk of over-reaching: it is precisely true
of one engagement, and that engagement's ledger record is `blocked`. See the flag at the end
of this file.

**Weakest line:** the headline. It is a general claim about how JT works, sitting directly
above three cards, only one of which demonstrates it. `[L-019]` is the rule it strains.

**Ship: Variant A.** It is the one whose every word is backed by a `publish-ready` record.
B's headline is a claim I cannot fully evidence today, and the brief is explicit that a
number or claim without an artifact behind it gets dropped.

---

# 4. Workflow Audit subhead and four card bodies

Headline is fixed and not redrafted: **Five business days. One named workflow. A clear build decision.**

### Current live copy

> **Subhead:** For property operators and other ops-heavy teams with one workflow that keeps
> aging, breaking, or waiting on manual follow-up. I map the real process, inventory the
> exceptions, and tell you exactly what should be built first.
>
> **Workflow map:** What actually happens today, which source reports are trusted, who owns
> each handoff, and where work stalls before the next follow-up.
>
> **Exception inventory:** A scored list of expired, aged, missing, changed, blocked, and
> approval-needed work that automation should surface first.
>
> **Build-or-do-not verdict:** A clear call on whether this workflow is ready to automate now,
> needs a readiness queue first, or should stay manual until the inputs improve.
>
> **Fixed-price build scope:** If the workflow is ready, you get the safest first build scoped
> with human approval design, logging, dependencies, timeline, and acceptance criteria.

---

### Variant A. You are buying a decision

**Angle bet:** the reader is deciding whether to spend $1,500. What de-risks that is knowing
the output is a decision they can act on, including the decision not to build.

> **Subhead**
> Pick the workflow that costs you the most hours. I spend five days mapping how it actually
> runs, not how it is supposed to run. At the end you get a decision: build this now, fix the
> inputs first, or leave it manual.
>
> **Workflow map**
> The real path. Which report anyone actually trusts, who owns each handoff, and where work
> sits waiting.
>
> **Exception inventory**
> Everything expired, missing, stale, or waiting on an approval, ranked so you can see what
> the build should surface first.
>
> **Build-or-do-not verdict**
> Sometimes the answer is do not build yet. If the inputs are dirty, automation will move the
> mess faster. I will tell you that instead of selling you a build.
>
> **Fixed-price build scope**
> If it is ready, you get the first build scoped with the approval design, the logging, the
> timeline, and the acceptance criteria written before I start.

**Citations**

- "acceptance criteria written before I start" is `[L-048]`: "Define done as evidence pasted
  into the record, not as a claim that everything passed. The completion condition names the
  specific checks that must appear in the pasted output." Also `[L-039]`, "Agree which
  capabilities are worth measuring before generating any test suite. A measurement nobody
  agreed to in advance gets argued with the moment it produces an inconvenient number."
- "I will tell you that instead of selling you a build" is `[jt-voice §8 sample line 7]` in
  spirit: "I am not sure that claim is strong enough to publish without a cleaner proof path."
  The willingness to talk himself out of revenue is the strongest trust move available and it
  is already in his voice.
- "how it actually runs, not how it is supposed to run" is the audit form of `[L-013]`:
  "Prove a behavior claim with different outputs, not with different instructions. Writing
  different instructions is not the same as getting different behavior."
- "ranked" replaces the live copy's "scored": a score implies a scoring model the reader
  cannot inspect, and `[L-042]` warns that a grader nobody can audit "converts a broken
  system into a confident green number."

**Self-grade: 5 of 5.** This is the closest section to publishable as written. The verdict
card in particular reads exactly like him.

**Weakest line:** "Pick the workflow that costs you the most hours." The brief bans
hours-saved figures. This is a selection instruction rather than a claim, so it is inside
the rule, but it is the one place in the document where the word "hours" appears and it
invites the reader to expect an hours number later that never arrives.

---

### Variant B. Five days, described as five days

**Angle bet:** the reader has been burned by a discovery phase that produced a slide deck.
What they want is a literal account of what happens, so the deliverables read as artifacts
rather than as phases.

> **Subhead**
> Name one workflow. I follow it for five days: the files it touches, the inbox it lands in,
> the person who approves it, and what happens on the week it goes wrong. You get four
> artifacts and a recommendation you can act on without me.
>
> **Workflow map**
> The real path, drawn from the work rather than from the process document. Which report
> anyone actually trusts, who owns each handoff, and where work sits waiting.
>
> **Exception inventory**
> Every expired, missing, stale, and waiting-on-approval item, listed with the rule it broke
> and the human who owns it.
>
> **Build-or-do-not verdict**
> Sometimes the answer is do not build yet. If the inputs are dirty, automation will move the
> mess faster. I will tell you that instead of selling you a build.
>
> **Fixed-price build scope**
> One build, fixed price, with the approval boundary, the logging, and the acceptance
> criteria written down before anyone starts, so we both know what done means.

**Citations**

- "the rule it broke and the human who owns it" is `[b2b-trust §6]` exception-notification
  spec verbatim: "Four elements, always: the exception, the rule it broke, the single next
  action, the owner."
- "a recommendation you can act on without me" is the positive form of
  `[corrections.jsonl 2026-08-11]`, whose published close was "Pull your open violations and
  find the oldest one nobody has touched," replacing a conditional that restated the post.
  The correction's own words: end with "an audit the reader can run against their own
  violations."
- "what happens on the week it goes wrong" is `[L-015]`: "Test that the system correctly
  returns nothing, not only that it returns the right something. Positive tests only prove
  the system can say yes."
- "so we both know what done means" is `[L-047]` and `[L-048]` in plain buyer language.
- "approval boundary" is on the `[jt-voice §3]` Use list.

**Self-grade: 4 of 5.** More concrete than A and the exception card is better. The subhead
is one clause too long.

**Weakest line:** "You get four artifacts and a recommendation you can act on without me."
Counting the deliverables turns the section into a package list, and `[jt-voice §7]` flags
"listicle announcements and school-essay structure" by name, quoting "I would build it as
four steps."

**Ship: Variant A subhead and verdict card, Variant B exception and scope cards.** A's
subhead converts, B's exception card is the one with a design-system spec behind it.

---

# 5. How I work

### Current live copy

> **Headline:** How I work
>
> **Subhead:** The first job is judgment: figure out what should be automated before anyone
> starts buying tools or building demos.
>
> **01 Map the real workflow:** I start with how the work actually moves: files, inboxes,
> approvals, spreadsheets, people, edge cases, and the places ownership gets fuzzy.
>
> **02 Rank the bottlenecks:** Not every workflow deserves AI. I score opportunities by time
> saved, visibility, risk, implementation complexity, and how painful the failure mode is.
>
> **03 Scope the first system:** You get a clear build recommendation: what to automate first,
> what data it needs, what success looks like, and what should stay human-owned.
>
> **04 Build it into production:** If the scope makes sense, I build the workflow, document it,
> test the edge cases, and leave your team with a system that actually runs.

---

### Variant A. The decision is the hard part

**Angle bet:** the reader's real risk is building the wrong thing. The differentiator is
where the time goes, so the section explains why the first days are spent not building.

> **Headline**
> How I work
>
> **Subhead**
> Most automation fails at the decision, not the build. I spend the first days on the
> decision so the build is the straightforward part.
>
> **01. Map the real workflow**
> I follow the work: which file, which inbox, who approves, and what happens when the data is
> wrong. The documented process and the real one are rarely the same.
>
> **02. Rank the bottlenecks**
> What it costs to run by hand, what breaks if it fails, and how dirty the inputs are. Some
> of these will not be worth automating and I will say so.
>
> **03. Scope the first system**
> One build, fixed price, acceptance criteria written before I start, so we both know what
> done means.
>
> **04. Build it into production**
> Dry runs, logs, alerts, and a human approval point anywhere money, tenants, or vendors are
> involved.

**Citations**

- Step 04's four objects are all `[jt-voice §3]` Use words, and the approval clause matches
  `[PP-001]` and `[PP-002]` human approval points. "a human approval point" already uses the
  corrected actor noun from `[jt-voice corr 2026-08-16]`.
- Step 02's "Some of these will not be worth automating and I will say so" is `[L-019]` in
  sales register, and it is the same trust move as the audit verdict card.
- Step 01's "what happens when the data is wrong" is `[L-015]` and `[L-065]`: a display that
  cannot answer its question should refuse and name what is missing rather than render an
  approximation.
- "What it costs to run by hand" replaces the live copy's "time saved" to stay inside the
  brief's ban on time-saved framing while keeping the ranking criterion honest.
- Subhead avoids a colon hook. `[jt-voice §4]`: "No colon hook machinery. A colon that
  announces a framework is not" acceptable. The live subhead has one.

**Self-grade: 5 of 5.** Steps 02 through 04 are, to my ear, indistinguishable from him.

**Weakest line:** the subhead's "Most automation fails at the decision, not the build." That
is the "not X, Y" contrarian reveal engine `[jt-voice §7]` bans, and I could not find a
version that kept the meaning without it. It should probably be cut to just the second
sentence.

---

### Variant B. Every step ends in something you can check

**Angle bet:** the reader has hired people who reported green and delivered broken. What
differentiates JT is that each stage produces evidence rather than a status.

> **Headline**
> How I work
>
> **Subhead**
> Each step ends in something you can look at: a map, a ranked list, a scope, and a running
> system with its logs open.
>
> **01. Map the real workflow**
> I follow the work: which file, which inbox, who approves, and what happens when the data is
> wrong. The documented process and the real one are rarely the same.
>
> **02. Rank the bottlenecks**
> What it costs to run by hand, what breaks if it fails, and how dirty the inputs are. Some
> of these will not be worth automating and I will say so.
>
> **03. Scope the first system**
> One build, fixed price, acceptance criteria written before I start, so we both know what
> done means.
>
> **04. Build it into production**
> Dry runs, logs, and alerts, with a human approval point anywhere money, tenants, or vendors
> are involved. Then a check that reads from outside the system, so a green status has to
> mean something.

**Citations**

- "so a green status has to mean something" is `[L-011]` ("A check that has never once failed
  offers no evidence that it would catch the problem coming back") plus `[L-044]` (anchor
  outside the system being measured).
- "with its logs open" is `[b2b-trust §6]` on reports and logs as the surfaces that "carry
  more trust load than any landing page."
- The four artifacts named in the subhead map one-to-one onto the four audit deliverables
  above, which is intentional: `[b2b-trust §3]` asks for the engagement to read as a
  three-step process with "process transparency" as the confidence signal.
- Steps 01 to 03 are unchanged from Variant A. See the kept-lines list below.

**Self-grade: 4 of 5.** Step 04's second sentence is the best expression of the brief's
through-line anywhere in this document.

**Weakest line:** the subhead. Listing four artifacts is the same listicle tell I flagged in
section 4 Variant B, and here it also duplicates the audit section directly above it.

**Ship: Variant A steps with Variant B's step 04 second sentence appended.** Cut Variant A's
subhead first sentence and open on "I spend the first days on the decision so the build is
the straightforward part."

---

# 6. About, two paragraphs replacing three

### Current live copy

> **P1:** I spent six years as a Business Systems Analyst at Spectrum Enterprise, working
> across systems, teams, process gaps, and rollouts where the hardest part was rarely the
> software itself. It was getting the workflow, ownership, exceptions, and handoffs right.
>
> **P2:** That is the lens I bring to AI implementation. I map how work actually moves,
> identify the highest-leverage bottleneck, then build controlled automation around the real
> operating pattern instead of forcing teams into a generic tool.
>
> **P3:** My work now spans client dashboards, recurring research pipelines, Salesforce
> Agentforce agents, n8n workflows, and local-first operations systems. The common thread is
> practical implementation: visible exceptions, human approval where it matters, and systems
> that operators can actually use.

---

### Variant A. Biography as risk reduction

**Angle bet:** the reader is deciding whether one person can be trusted with their
operation. The six years explain why he builds the right thing, which is the specific fear
being answered.

> **P1**
> I spent six years as a Business Systems Analyst at Spectrum Enterprise. The hard part was
> almost never the software. It was working out who owned what, where the handoffs dropped,
> and which exceptions everyone had agreed to handle by hand.
>
> **P2**
> That is the same job now, with AI in it. I map how the work actually moves, find the
> bottleneck worth fixing, and build a controlled system around it. The systems log what they
> do and stop for a human when the stakes are real.

**Citations**

- The whole structure is `[b2b-trust §3]` section order item 4, quoted: "Six years reading
  workflows as a Business Systems Analyst before building automations explains why he builds
  the right thing. This is biography as risk-reduction, not a resume."
- "everyone had agreed to handle by hand" drops the substrate's "quietly," which
  `[jt-voice §7 AVOID]` names as a softener adverb with the verbatim example "The queue
  quietly stops moving."
- "stop for a human" uses the corrected actor noun, `[jt-voice corr 2026-08-16]`.
- The tool list from the current P3 is deliberately dropped. `[b2b-trust §3]` puts the stack
  "last and translated" and says "Never lead with tool names, agent vocabulary, or model
  names." `[b2b-trust §1]`: the buyer "cannot verify a tech stack and may fear one."
- The substrate's "can be handed to an operator without a training program" is cut. No ledger
  record supports it and the brief bars claims without an artifact behind them.

**Self-grade: 5 of 5.** P1 is the strongest paragraph in the substrate and survives almost
intact.

**Weakest line:** "That is the same job now, with AI in it." It is a good sentence, but "with
AI in it" is the only slightly cute construction in the block and it sits at a paragraph
opening where he would normally be plainest.

---

### Variant B. The operator who checks his own work

**Angle bet:** the reader has met consultants who are confident. The differentiator is a
person whose stated habit is assuming his own build is wrong until something outside it
agrees.

> **P1**
> I spent six years as a Business Systems Analyst at Spectrum Enterprise. The hard part was
> almost never the software. It was working out who owned what, where the handoffs dropped,
> and which exceptions everyone had agreed to handle by hand.
>
> **P2**
> I build the same way I read those workflows. The system logs what it does, stops for a
> human where money, tenants, or vendors are involved, and gets measured against records it
> did not write. A build I have checked myself is not finished. Somebody else has to be able
> to check it.

**Citations**

- "A build I have checked myself is not finished" is `[L-047]` stated in the first person:
  "The party that builds the work never decides whether it is done. The person who built it
  cannot see the assumption they built it on, which is precisely where the expensive defects
  hide."
- "gets measured against records it did not write" is `[L-044]`.
- "Somebody else has to be able to check it" is `[L-051]`: "Whoever checks the work must not
  be able to change the work."
- P1 is unchanged from Variant A.

**Self-grade: 4 of 5.** This is the brief's through-line stated as character rather than as
a claim about a project, which is the safest way to say it given the ledger state.

**Weakest line:** "I build the same way I read those workflows." The bridge is doing
connective work rather than carrying content, and `[jt-voice §7]` cuts "audience bridges"
with the verbatim example "The same shape shows up well outside software."

**Ship: Variant B.** It carries the brief's through-line without needing a client record to
back it, and P2's last two sentences are the only place in the document where the
verification method is stated as something JT does to himself rather than something a client
did for him.

---

# Lines kept unchanged from the substrate, and why

These went in untouched because I could not improve them and each has corpus backing:

1. **"The documented process and the real one are rarely the same."** (How I Work 01) Plain
   claim, second clause earns its place, 11 words. `[jt-voice §1]`.
2. **"Some of these will not be worth automating and I will say so."** (How I Work 02) The
   trust move of declining revenue, matching `[L-019]` and `[jt-voice §8 line 7]`.
3. **"One build, fixed price, acceptance criteria written before I start, so we both know
   what done means."** (How I Work 03) `[L-048]` in buyer language.
4. **"Dry runs, logs, alerts, and a human approval point anywhere money, tenants, or vendors
   are involved."** (How I Work 04) Every noun is on the `[jt-voice §3]` Use list, and the
   approval actor is already "human" per `[jt-voice corr 2026-08-16]`.
5. **"The real path. Which report anyone actually trusts, who owns each handoff, and where
   work sits waiting."** (Audit card 1) Fragment then constraint stack, exactly `[jt-voice §1]`.
6. **"Sometimes the answer is do not build yet. If your inputs are dirty, automation will
   move the mess faster. I will tell you that instead of selling you a build."** (Audit card 3)
   Condition-first sentence per `[jt-voice §1]`, and the strongest line in the substrate.
7. **Substrate About P1, minus one word.** "quietly" cut per `[jt-voice §7 AVOID]`. Everything
   else stands.

---

# jt-voice rules I deliberately ignored, and why

The skill declares itself for LinkedIn and short social writing and explicitly not for other
registers. I took diction, rhythm, refusals, and sentence shape. I discarded the following.

| Rule ignored | Where it lives | Why |
|---|---|---|
| All five post structures (verified build proof, buyer-scene, teardown, critique-reconstructed, learned-from-failure) | §6 | These are post shapes with ordered beats. A homepage is a set of parallel sections a reader scans in any order, and `[b2b-trust §3]` supplies the competing section order that actually governs this page. |
| "LinkedIn posts run 3 to 6 short paragraphs" and "blank line between every paragraph" | §4 | Page furniture, not voice. Card bodies are two to three sentences by layout constraint. |
| "Exactly three hashtags at the end of the body" | §4 | Hashtags do not exist on a website. |
| Banned and allowed **opening** patterns, including "Built this / installed this" as an opening requirement | §2 | These govern the first line of a post competing in a feed. A hero headline is not competing for a scroll stop; `[b2b-trust §2]` says its job is to answer four questions in ten seconds. I kept the underlying refusal (no throat-clearing, no framework announcement) and dropped the prescribed openers. |
| "Never end with engagement bait: DM me, link in bio" and "A reader question is optional" | §5 | A homepage exists to produce a booked call. The CTA "Book a 20-minute workflow call" is engagement bait by post standards and is correct here. `[b2b-trust §2]` requires exactly one CTA above the fold. |
| "Use a fragment only when conversationally earned" | §1 | The eyebrow row is three fragments separated by dots. That is a layout element, not a sentence. |
| "Keep most public lines between 7 and 18 words" | §1 | Kept as a default, ignored for card titles, the eyebrow row, and hero headlines, which run shorter by design. |
| "Lowercase allowed only for X thinking-out-loud posts" | §4 | Irrelevant; everything here is sentence case. |
| The "Corrections" note that a teardown body may run past six paragraphs | §Corrections | Lane-specific to teardowns. |

**I also ignored a corpus file on purpose:** `banned-nouns.txt`. It bans "tenant," "vendor,"
"client," "owner," "lease," "certificate," and "property management," among others. Its own
header says it lists "words that name a business object rather than a software object,"
seeded from adversary reports, and `lint.py` sits next to it. It is a linter for system
specifications. Applied to marketing copy it would delete precisely the vertical vocabulary
that `[b2b-trust §3]` calls a trust signal, and it would forbid the language of the only
confirmed-posted line in the corpus. I did not apply it. If it was meant to govern public
copy as well, this draft fails it comprehensively and should be rewritten.

---

# The three patterns from corrections.jsonl that most changed my drafting

`corrections.jsonl` contains **one** correction record, not a set. I extracted three
patterns from it and from the six correction entries in the jt-voice skill that were derived
from the same 2026-08-11 published-versus-draft diff.

**1. Cut any claim about a party you have no access to.** The diff removed "it is priced and
built for large portfolios" outright, and narrowed "Monitoring is where the category stops"
to "but stops at monitoring." The stated reason: "pricing and target market are claims about
a company you have no access to, and one product does not support a verdict about a
category." *Effect on this draft:* there is no comparison anywhere. No line says what
in-house teams do, what other consultants charge, what generic automation gets wrong, or
what a category fails to do. Every competitive claim I drafted came back out. This also
killed an early hero variant built on "most automation gets sold before anyone maps the
workflow," which is a verdict about a market I cannot evidence.

**2. The opening states the scene and the gap, and nothing more.** Draft: "A violation notice
lands in a shared inbox, **and the alert that produced it has already done its whole job.**
Nobody has been handed the correction, the vendor, or the filing." Published: "A violation
notice lands in a shared inbox, **but** nobody has been handed the correction, the vendor, or
the filing." The interpretive clause was cut. *Effect on this draft:* every section subhead
lost its explaining sentence. The proof subhead does not tell you why proof matters. The
"Who this is for" subhead does not tell you what the pattern means. This is also why I cut
the current live proof subhead entirely: "The site does not need to claim magic" is a whole
sentence of interpretation before the reader has seen anything.

**3. Name the operational object in the operator's own words.** "cure window" became
"correction deadline." "with the confirmation" became "with its acceptance." "The returned
document files against the building record" became "When the vendor sends proof back it
attaches to that item." *Effect on this draft:* "self-hosted" became "inside your own
environment." "Local-first" does not appear. "Ledger hygiene," "exception layer," and
"observability" were all drafted and all removed. It is also why I flagged "drifts" in hero
Variant B as that variant's weakest word: it is a vague noun hiding the thing being tracked,
which is the exact failure this correction names.

A fourth, worth recording because it changed the shape of two sections: **the approval actor
is a human, not a person.** Published: "The owner update is the step a human approves before
it sends." Every approval sentence in this draft says "human."

---

# What I think is strategically wrong with the substrate draft

Not wording. These are structural.

**1. The hero alternate fails the brief's own constraint.** "Your team repeats the same work
every week. I build the system that does it." opens on the reader's situation, not on what
JT builds. The brief states the hero "must lead with what JT BUILDS." The alternate is a
better sentence than the primary in rhythm, and it is disqualified. If it is kept, the
constraint should be relaxed deliberately rather than by accident.

**2. Two substrate lines use a construction the voice profile bans by name.** "Running in
production, not piloted" and "The interesting part of an automation is not the demo. It is
what it does on an ordinary week." Both are the "not X, it is Y" contrarian reveal engine
that `[jt-voice §7]` lists, and the second is close to "the useful question is uglier,"
quoted in the AVOID list. These are not stylistic near-misses. They are the specific shape
the corpus records him removing.

**3. "Ops-heavy teams with messy internal workflows" re-broadens the positioning the brief
says not to broaden.** The brief names NYC and NJ property management and real estate as the
primary market. Card 1 is a general-purpose card that lets any reader self-select, which is
exactly the generic AI implementation posture the brief rules out. Cards 2 and 3 are the
positioning. Card 1 argues with them. My recommendation is to retitle card 1 to a property
or real-estate-adjacent operation, or cut it and run two cards. I did not do it because
retitling was not in scope, and two cards would leave an orphan row in the three-column grid.

**4. The audit is still the loudest thing in the eyebrow row.** The brief says the audit is
the entry point, not the value proposition, and then the eyebrow leads with "$1,500 Workflow
Audit." The headline carries the build, so the page is not strictly in breach, but the price
is the first thing the eye lands on after the headline. Moving the price to third position
costs nothing and keeps proof and safety ahead of the offer.

**5. About P2 contains an unevidenced product claim.** "can be handed to an operator without
a training program" is a support and adoption claim. No ledger record covers handover,
training, or operator self-sufficiency. Under the brief's own rule, it should be dropped or
attached to an artifact. I dropped it.

**6. The substrate has no answer to "is it real" above the fold.** `[b2b-trust §2]` requires
a production-proof line without scrolling, and the substrate's eyebrow offers "Running in
production, not piloted," which is a category statement with no referent. `[PP-001]` is
`publish-ready` and gives a true, anonymized, specific alternative at no risk. Both my hero
variants use it.

---

# One governance flag, outside the copy

The marketing analytics card is treated as final and untouchable by the brief, and I have
not touched it, paraphrased it, or written around it. It is worth saying once that its
ledger record disagrees with its status on the site.

`[PP-005]` has `gate_status: blocked` and `missing_gates: ["date_shipped"]`. The proof-engine
README is unambiguous: "If `gate_status` is anything other than `publish-ready`, the record
does not exist as far as the outside world is concerned. There is no close enough, no I'll
just describe it vaguely." The card is live on the homepage today. Separately, the card
contains a count of defects found, while `PP-005` carries `metric: null` and
`metric_permissioned: false`, and README Rule 2 states that no number appears in public
material unless `metric_permissioned` is true.

Two readings. Either the client approval the brief refers to is exactly the written
permission the ledger wants, in which case `PP-005` should be updated with `date_shipped`,
`metric`, `metric_permissioned: true`, and an `evidence_path`, and moved to `publish-ready`.
Or the record is accurate and the card is ahead of its gate. I cannot tell which from the
corpus, and it is not a copy decision, so I have changed nothing and raised it here.
