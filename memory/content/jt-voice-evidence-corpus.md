# JT Voice Evidence Corpus

Date: 2026-06-07
Status: v1.2 local evidence corpus for `memory/content-voice.md` and `memory/content/jt-voice-profile.md`.

Purpose: convert the unfinished voice-calibration questions into durable evidence so generated posts sound like JT: direct, practical, specific, and operator-led instead of generic AI consultant copy.

## Evidence Boundary

Public post inventory is thin from the live X API right now. `skills/x-research profile jts_14 --count 40 --json` returned one recent post:

> Lead capturing from NYC ballet family contributors page

That is useful for cadence but not enough for a full public voice clone. So this corpus uses the strongest available local evidence:

- JT's direct corrections in `memory/FEEDBACK-LOG.md`.
- JT's Canals AI Ops Teardown rewrite from the June 1 content correction.
- JT's direct-message/request cadence from recent OpenClaw conversations.
- Verified proof-post preferences, especially the Yair COI quote-tweet correction.
- Existing content rules that have passed JT corrections.

This is now enough to improve generated drafts materially. Future public examples can enrich the corpus, but lack of 20 public X posts should no longer block better generation.

2026-06-07 update: JT answered Voice OS Question 1 with four posts he believes sound most like him. Treat these as Tier 1 voice evidence because they are JT-selected examples, even where the original publishing surface varies.

## Actual JT Cadence Signals

JT's natural written instructions tend to:

- Start with the ask, not politeness.
- Use direct correction language: "This is an issue", "Why nothing for my account?", "Check your work", "ensure everything is optimal".
- Name the standard he expects: "actual voice, phrasing, rhythm, and specificity".
- Push for root cause and system repair, not explanation-only answers.
- Prefer dense operational words over polished creator words: scraped, stored, analyzed, reference, generated, optimal, task, file, account.
- Use short commands with high standards: "Figure it out", "Check your work", "Complete the unfinished questions/tasks".

Translation for content:

- The post should move like a decision, not a performance.
- The first line should make a concrete claim or name a concrete work scene.
- Rhythm should be short but not sloganized.
- Specificity should come from objects, systems, owners, numbers, inputs, and constraints.

## Best Evidence Pair: Canals Rewrite

JT's stronger Canals teardown pattern:

> Canals just raised $35M for a wholesale problem every distributor recognizes: orders arrive messy.
>
> One buyer emails a PDF. Another sends a spreadsheet. A rep forwards a voice note. A handwritten line item shows up with the wrong unit count.
>
> The ERP still needs a clean order, price check, inventory check, exception owner, and confirmation back to the customer.
>
> The workflow I would build starts with a shared order-intake desk.
>
> It reads emails, PDFs, spreadsheets, and notes. It extracts customer, SKU, quantity, unit, requested date, and attachments. It checks the catalog, customer-specific pricing, inventory, and margin rules.
>
> When the order is clean, it drafts the ERP-ready entry. When something is off, it routes the exception to the right owner with the source attached.
>
> Customers keep sending orders their way. The distributor gets a cleaner intake layer before bad data hits the ERP.

Durable rules:

- Current signal first, but translated into operator pain.
- Concrete messy input scene before AI/workflow explanation.
- Name the system of record.
- Name clean path and exception path.
- Preserve normal customer/operator behavior.
- End with cleaner operating outcome before damage hits the system.

## JT-Written / JT-Preferred Shapes

### Tier 1: JT-Selected Posts That Sound Like Him

These are the first explicit answers to Voice OS Question 1: "What is one post you wrote that still sounds most like you?"

#### 1. Client Proof + Vertical Thesis

> Built this AI workflow for Yair and his real estate firm.
>
> A dedicated mini PC in their office, connected to their existing systems, running automated workflows 24/7.
>
> 11% to 78% compliance jump. $85K saved annually.
>
> Real estate operations is one of the best verticals for this kind of AI automation. @YairsQuest and I are just getting started.

What this proves:

- JT is comfortable leading with "Built this" when the proof is real.
- The post earns confidence through deployment detail before thesis.
- The strongest rhythm is: build owner -> architecture -> metric -> vertical thesis -> momentum.
- Numbers can be blunt fragments; they do not need explanatory cushioning.
- A public collaborator/client tag is natural only when permission/relationship context is real.

Generation rule:

When verified proof exists, do not hide behind buyer-scene abstraction. Lead with the build, name the deployment surface, give the metric, then generalize the vertical.

#### 2. Product Retrospective + Timing Judgment

#### 2. Local Deployment Story + Safety Rationale

> Yesterday I installed a dedicated automation PC for a NYC real estate family office.
>
> They decided to name it Jarvis 😂
>
> The machine will host 6 automated workflows I built for them, covering insurance expiration tracking, QuickBooks data entry, validation checks, and other back-office tasks that used to require manual follow-up.
>
> The dedicated PC lets the workflows run locally without touching their existing servers, changing their current setup, or introducing unnecessary risk into systems they already depend on.
>
> That is a big part of real AI implementation for established businesses.
>
> The work is not just building the workflow. It is giving the business a safe operating environment where the workflow can run every week without creating a new security headache.
>
> The system handles the repetitive work, and the team only gets notified when something actually needs human attention.
>
> Projected time saved: 10-20 hours per week.

What this proves:

- JT's LinkedIn proof voice can open with a plain deployment story, not a hook.
- A small human detail is allowed when it is attached to real implementation context.
- Workflow scope should be concrete: count, examples, and prior manual burden.
- The safety rationale matters as much as the automation: local machine, no server disruption, no unnecessary risk.
- "Real AI implementation" should be defined through operating conditions, not hype.
- The post ends with the human-attention boundary and projected time saved.

Generation rule:

For established-business implementation posts, use story -> workflow scope -> safety rationale -> operating environment -> human exception boundary -> projected outcome. Do not reduce local deployment to "we automated back office tasks."

#### 3. Product Retrospective + Timing Judgment

> This is essentially what I attempted to build with http://adversightai.com almost a year ago.
>
> But models weren't good enough at that time to cost-effectively automate the whole process end-to-end like you can now, and user acquisition was super tough and time consuming where it wasn't worth continuing to focus on at that point in my life.
>
> But small internal boost of confidence knowing the idea was right.

What this proves:

- JT's natural retrospective voice is candid and context-heavy, not polished into a founder aphorism.
- He explains the practical constraints: model quality, cost, end-to-end automation, user acquisition, life timing.
- He can use "But" twice when that is the honest rhythm; do not over-edit into tidy symmetry.
- The conclusion is modest and specific: "small internal boost of confidence," not a grand lesson.

Generation rule:

For product/build reflections, preserve the practical timeline and constraint stack. Do not turn it into "timing beats ideas" unless JT writes that himself.

#### 4. Model Stack + Risk/Return Conviction

> Context on how this works: GPT-5.2, Gemini 3 Pro, Opus 4.5, and Grok 4 work together and cross-check other to provide optimal analysis with a focus on game theory positioning.
>
> So pretty much the smartest AI models in the world think this is best risk/return coin right now from a game theory perspective.
>
> Send it.

What this proves:

- JT can start with "Context on how this works" when explaining a system behind a claim.
- Specific named tools/models create credibility when they explain method, not tool fandom.
- The logic is stack -> cross-checking -> analytic focus -> risk/return conclusion.
- Casual conviction is allowed on X/crypto contexts: "Send it." works because the setup carried the proof.

Generation rule:

For technical or crypto posts, explain the analysis system plainly, then state the conviction. Keep the final line short if the setup is specific enough.

### Direct Operator Proof

Use when JT built the thing or owns the proof.

Shape:

`Built this workflow for [client/person]. [Deployment detail]. [Metric]. [Vertical thesis].`

Longer LinkedIn proof variant:

`Installed/deployed [local operating surface]. [Human detail if real]. [Workflow count + examples]. [Why deployment is safe]. [What real implementation means]. [Human exception boundary]. [Projected/verified outcome].`

Why it sounds like JT:

- Ownership first.
- Architecture second.
- Number third.
- Thesis last.
- Safety rationale when implementation affects established systems.

Avoid:

- "AI businesses pay for outcomes."
- "Chatbots vs agents."
- Generic category commentary when real proof exists.

### Buyer-Scene Consulting Post

Use when selling implementation judgment.

Shape:

`[Concrete workday scene] should not become [fragmented operational mess].`

Then:

- Inputs.
- System of record.
- Owner / approval boundary.
- Workflow action.
- Business outcome.

Avoid:

- "Most businesses do not need an AI chatbot."
- "Your team does not have an AI problem."
- "The blocker is not X."

### X Build/Observation Post

Use when writing for @jts_14.

Shape:

Short direct claim.

Then one concrete proof detail or contrast.

Example from live profile:

> Lead capturing from NYC ballet family contributors page

Lesson:

- JT's native X can be extremely plain.
- It does not need a guru hook if the object is specific.
- The noun does the work: lead capture, NYC ballet, family contributors page.

## Answered Taste Questions

### Question 2: Generated Posts That Annoy JT

JT named three drafts that annoyed him because they used AI-slop hook patterns even though the operational content was plausible.

Rejected patterns:

- "The best first AI project is usually..."
- "[Niche] AI gets useful at..."
- "Most AI projects do not fail because X. They fail because Y."
- "Most SMBs do not need X. They need Y."
- Colon followed by a comma-list of instructions, especially: "Before you automate the task, answer four questions: what..., what..., who..., where..."

What this proves:

- Operational nouns are not enough if the hook sounds generated.
- JT dislikes packaged consultant cadence where the first line announces a framework.
- The stale reveal pattern is broader than literal "not X, Y"; "do not fail because X / fail because Y" and "do not need X / need Y" are the same failure.
- Lists can sound robotic when they are compressed into a colon sentence instead of written like natural judgment.
- "Gets useful at" feels like generic AI-thread language, even when the exception-layer idea is sound.

Generation rule:

Do not open with a category/framework thesis about AI projects. Open with the actual deployment, buyer scene, constraint, or result. If a draft contains a colon followed by multiple comma-separated "what/who/where" instructions, rewrite it into normal sentences or a concrete work scene.

### Question 3: Outside Creator Structure To Respect, Persona To Reject

JT named @AlexFinn on X as a creator whose structure can be useful but whose voice/persona should not be copied.

Useful mechanics to borrow:

- Urgency around a current opportunity.
- Concrete tool stack and setup path.
- Clear sequence from signal discovery to prototype/build.
- Business-idea generation from real market pain.
- Direct "go do the thing" energy when the reader can actually act.

Persona and patterns to reject:

- Insult hooks like "you're a moron."
- Hype phrases like "INSANE opportunity" and "unreal opportunity."
- Manic self-sacrifice as aspiration: no sleep, missed meals, no walks, barely working out.
- All-caps command energy: "DO NOT," "EVERYTHING," "PISSED."
- Generic creator cliches: "what most people miss," "here's the system:", "the results?"
- Related setup cliche: "here's what you need to do."
- Numbered lists with no personality.
- "Now take action before someone else does" style urgency.

What this proves:

- JT is open to borrowing structure, but not persona.
- A numbered list is not automatically bad; it fails when it reads like a generic creator playbook instead of JT's operating judgment.
- Urgency should come from a real market window, verified build, or workflow consequence, not motivational intensity.
- JT's version of "take action" should be grounded in a concrete first move, not hype.

Generation rule:

When using outside creator posts as references, label the borrowed mechanic separately from the rejected persona. Translate Alex Finn-style opportunity posts into JT voice by keeping the concrete setup path and market-pain scan, but removing insults, manic dedication, hype caps, generic setup cliches, and generic motivational CTAs.

### Question 4: Natural Sentence Shapes Inferred From JT Examples

JT said he is not sure he can name exact words/sentence shapes, then supplied natural communication examples to infer from.

Examples supplied:

> Facts. But distribution is the new moat. Anyone can create anything now, but need to be able to get it attention and in front of people

> I like that Mamdani is charismatic and well spoken. Refreshing in this day and age of politics. Very unconvinced his policies will work though. The government has proven to be largely incompetent. Government-run anything will probably end poorly. They just don’t have the talent pool private companies do. If you want shit done effectively and innovatively it has to be for profit which is why capitalism is the only system that makes sense long term imo. I’m also pretty worried about increase in crime and homelessness with his radical history of views regarding law enforcement

> Thanks for these detailed answers. If all information could live in a single source spreadsheet, this should be pretty straightforward. I've attached a proposal for this workflow. Please review and let me know if all looks good, and if so, I can get started on this one as soon as I finish the Rent Delinquency workflow.

Inferred sentence shapes that feel like JT:

- **Short agreement, then sharper caveat:** "Facts. But..." The first sentence can be one word when it is a real conversational response, but the next line needs the actual point.
- **Plain thesis with causal follow-up:** "Distribution is the new moat" works because the next sentence explains the practical reason: creation is cheap, attention is scarce.
- **Approve one part, reject another:** "I like that X. Refreshing. Very unconvinced Y though." JT often separates personal reaction from practical judgment instead of forcing one clean ideological line.
- **Blunt confidence with practical qualifier:** "will probably end poorly," "has proven to be," "they just don't have..." The rhythm is not hedged, but it is grounded in a reason.
- **Conversational intensifiers are allowed when native:** "largely," "probably," "pretty worried," "long term imo." These make the claim sound like JT thinking in real time, not a polished manifesto.
- **Direct client email spine:** appreciation -> condition -> simplicity assessment -> attached proposal -> review request -> start timing. This is clean, useful, and specific without sounding corporate.
- **Condition-first operational clarity:** "If all information could live in a single source spreadsheet, this should be pretty straightforward." This is a strong JT implementation sentence: one prerequisite, one complexity judgment.
- **Concrete next step with dependency:** "I can get started on this one as soon as I finish the Rent Delinquency workflow." JT's natural client voice names the dependency instead of pretending unlimited capacity.

Generation rule:

Do not over-polish JT into symmetrical founder aphorisms. Keep the useful rough edges: short verdict fragments, "but" pivots, practical skepticism, condition-first implementation sentences, and direct next-step language. When drafting client/proof content, prefer "If [source/condition] can live in [one place], this should be [simple/straightforward]" over abstract "we can streamline this workflow" language.

### Question 5: Cringe Sentence Shapes JT Rejected

JT supplied additional negative examples that should be treated as structural rejects:

- `"hit a wall where every coordination problem gets solved with a hire"` — JT specifically does not like "gets solved with a hire."
- `"X don't Y, they Z"` — reject this as a stale contrast template.
- `"The question that changes every build: what are you trying to prevent?"` — JT does not like statement-followed-by-colon hook phrasing.
- `"The workflow design changed when that distinction was clear."` — JT does not like closing posts with the "X happened when Y" pattern.

What this proves:

- JT dislikes generated copy that sounds like a tidy framework sentence, even when the idea is plausible.
- The banned reveal family is larger than "not X, Y." It also includes "X don't Y, they Z."
- Colons should not be used as hook machinery. They make the line feel packaged.
- Closing lines should end on a concrete outcome, next action, number, constraint, or practical implication, not a retrospective "X changed when Y" wrap-up.

Generation rule:

Avoid polished template closures and colon-hook statements. Replace "The question that changes every build: what are you trying to prevent?" with a direct sentence like "Every build needs to know what it is trying to prevent." Replace "The workflow design changed when that distinction was clear" with the actual operational change or result.

### Question 6: Optimal Balance Between Build Proof And Consultant POV

JT clarified that generated content should balance two modes:

1. **Operator explaining a build:** content about what JT is building, unique implementation choices, safe deployment details, architecture decisions, workflow constraints, and proof points that make him look more credible as a consultant.
2. **Consultant naming a buyer problem:** content about what JT is seeing across his focused niches, the operational problems buyers recognize, and unique solution ideas that make him attractive to potential clients and employers.

Key instruction from JT:

> Content generated for me should be optimal balance of the 2. There should be content about things Im building, unique things I'm doing or incorporating during these builds that would be beneficial to share/make me look better as a consultant if shared, as well as content about things I'm seeing from a consultant perspective on the niches I am currently focused on and sharing unique value on solutions to buyer problems within these niches that makes me attractive to potential clients/employers that come across my profile.

What this proves:

- Build posts are valuable when the build demonstrates reusable consulting judgment, not just activity.
- Consultant POV posts are valuable when tied to current niche focus and buyer-recognizable problems, not generic AI implementation advice.
- The content system should not ask JT to choose one mode. It should balance both across the week and often combine them inside a single post.
- The shared standard is external credibility: a buyer, recruiter, or peer should see either proof of execution or proof of diagnostic judgment.

Generation rule:

Use a two-lane balance:

- **Build Proof Lane:** lead with a real build, deployment detail, architecture choice, constraint, metric, or workflow edge case. Then explain why that choice matters for the buyer vertical.
- **Buyer Problem Lane:** lead with a niche-specific operational problem, buyer scene, current market signal, or repeated workflow failure. Then describe the solution shape JT would build or the implementation judgment a buyer should care about.

Best posts often bridge both: "I built/observed X" -> "the useful lesson for [property managers/distributors/real estate operators/etc.] is Y" -> "the workflow needs [source, owner, approval rule, exception route, metric]."

Weekly balance guidance:

- Do not let the week become only build-in-public.
- Do not let the week become only consultant commentary.
- For a normal 3-4 post week, include at least one real-build/proof post and at least one niche/buyer-problem POV post.
- If there is a strong current build, use it as proof and extract one buyer-facing lesson from it.
- If there is no strong current build, use niche observation/AI Ops teardown style and make the solution specific enough that it still demonstrates build judgment.

### Question 7: What Feels Too Polished For X

JT supplied examples of X content that feel too polished:

- `"Would you trust an AI agent with a cash timing decision? ... I would trust it with the review queue."`
- `"Your maintenance inbox is probably a margin leak."`
- Short dramatic noun stacks like `"Urgency. Unit history. Vendor route. Tenant update. Owner approval."`
- `"The useful question is uglier:"`
- Build-list flex posts ending with `"What did you build in March?"`
- `"one patch. but the difference between an agent that routes correctly and one that fires the wrong workflow is the difference between automation and chaos"`
- `"that's not automation. that's leverage."`

What this proves:

- JT does not want X posts that read like compressed LinkedIn broetry.
- Workflow nouns are not enough if the rhythm is staged.
- Rhetorical trust hooks, dramatic list fragments, and creator-flex CTAs make real build proof feel less like JT.
- "Useful question is uglier" and "that's not automation, that's leverage" are too neat. They sound like a creator trying to coin a line.
- X should feel sharper and rawer: one concrete observation, one practical judgment, or one build fact with less stage lighting.

Generation rule:

For X, avoid polished guru compression. Prefer direct operational statements:

- Bad: `"Would you trust an AI agent with a cash timing decision?"`
- Better: `"I would not let an agent approve cash movement. I would let it find the risk and queue the approval."`
- Bad: `"Your maintenance inbox is probably a margin leak."`
- Better: `"The maintenance request is easy. The leak is the handoff nobody owns."`
- Bad: `"That's not automation. That's leverage."`
- Better: `"A loop is useful when the next run changes the next decision. Otherwise it is just another automation."`

1. **When should JT be blunt?**
   When the reader is facing a bad implementation pattern, repeated manual work, stale content angle, or overhyped AI claim. Bluntness should name the consequence, not insult the reader.

2. **When should JT be explanatory?**
   When credibility depends on workflow architecture: inputs, system checks, exception routing, approval boundaries, metrics, and deployment constraints.

3. **When is "I built this" right?**
   When ownership is verified proof: client workflow, app, automation, service page, pipeline, dashboard, or public build. It is wrong when the post is meant to teach a buyer pain before JT's role matters.

4. **What topics make JT credible?**
   Messy operations, workflow implementation, Spectrum-style systems coordination, property management, wholesale/distribution, construction handoffs, local-first client workflows, Agentforce/Salesforce activation, proof-safe AI operating systems.

5. **What topics make JT generic?**
   AI will change everything, chatbots vs agents, generic automation saves time, vague AI adoption, public proof hygiene as a standalone thought, content system transparency, and tool fandom without workflow consequence.

6. **What is a real uncomfortable truth?**
   A direct operational claim with a consequence: "If your team still checks the same spreadsheet every morning, the system is not finished."

7. **What is AI slop contrarian framing?**
   Any reveal structure where the sentence depends on "not X, Y" instead of a concrete failure, number, system, owner, or workflow.

8. **What words feel like JT?**
   Workflow, handoff, owner, approval, source, queue, system, exception, intake, record, check, proof, deployment, local, messy, concrete, route, logs.

9. **What words do not feel like JT?**
   Transformative, streamline, unlock, innovative, ecosystem, AI-powered future, leverage as a buzzword, thought leader, best-in-class, holistic.

10. **What is too polished for X?**
    Rhetorical trust hooks, dramatic one-word noun stacks, "useful question is uglier" pivots, abstract leverage endings, build-list flex CTAs, symmetrical LinkedIn phrasing, abstract lessons, multi-line aphorisms with no object, guru-style "truth" posts, and compressed lines that could be sold by any AI creator.

11. **What is too casual for LinkedIn?**
    JT delegated this to Eve's platform judgment: leave out anything that would not be attractive to a potential client or employer. Too casual means one-line tweets, lowercase hot takes, "quick update" posts, "small win" framing, vibes/slang, weekend-project chatter, "been playing with..." tool notes, product-builder updates with no buyer/recruiter relevance, and app-growth observations that do not prove implementation judgment.

    Generation rule: LinkedIn can keep JT's plain language, but the purpose cannot be casual. Every LinkedIn post needs at least one of: buyer-recognizable operating problem, verified build ownership, measurable outcome, safe deployment detail, workflow/approval boundary, niche-specific implementation lesson, or career-relevant systems judgment. If the post only says "I built something," "this is cool," or "here is a tool I tested," rewrite it or skip it.

12. **What should never be public by default?**
    Outreach mechanics, private client names/details, internal content machinery, scraped reference workflows, proof-hygiene cleanup, stale system corrections, and anything that makes JT look like he is repairing credibility instead of demonstrating it.

13. **What should a reader feel after LinkedIn?**
    "He understands the operational mess before he automates it."

14. **What should a reader feel after X?**
    "That is a sharper way to think about this."

15. **What does specific enough mean?**
    The post names at least one concrete input, system of record, owner, approval boundary, metric, deployment fact, or failure mode.

16. **What inherited framework language should be retired?**
    Old compression-template slogans: "The tools exist. The implementation doesn't," "Agents handle the work," "Build the process. Buy back the time," "Consultants charge for advice," "Demo proves it's possible. Deploy proves it's real," "Specs live in decks," "Chatbots answer questions. Agents close tickets," and "the implementation is always the bottleneck." These can be mechanically clean and still wrong for JT because they prove no buyer scene, workflow object, or implementation judgment.

    Replacement rule: if the line could be printed on an AI consultant carousel, it needs a concrete object before it reaches JT.

## V1 Voice Scoring Rules

A serious draft should score 80+ before JT sees it.

- JT voice fidelity: 25
- Specificity/proof: 20
- Platform fit: 15
- Originality: 15
- Business usefulness: 10
- Reference mechanic translation: 10
- Rule compliance: 5

Hard fail:

- Sounds like any AI consultant could have written it.
- Starts with an AI category when it should start with a buyer scene.
- Uses reveal framing as the main engine.
- Has no concrete input/system/owner/metric.
- Foregrounds internal cleanup or content machinery.
- Makes unverified proof claims.
