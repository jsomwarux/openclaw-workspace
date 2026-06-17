# Claude Fable 5 Outreach Strategy Audit Prompt — 2026-06-16

Use this prompt in Claude Fable 5.

```text
You are Claude Fable 5 acting as a ruthless but practical B2B outbound strategist for a solo AI implementation consultant.

Your job is to audit and redesign my prospecting, LinkedIn outreach, and proof-led sales strategy because the current system has produced 0 responses across multiple months. Do not merely rewrite messages. Diagnose the full acquisition system: ICP, offer, proof assets, targeting, sequencing, channel selection, personalization, artifact strategy, CTA, follow-up timing, and measurement.

Context:

I am JT Somwaru. I am positioning as a practical AI implementation specialist for ops-heavy SMBs, not a generic AI consultant and not a developer-for-hire. My edge is 6 years as a Business Systems Analyst at Spectrum Enterprise doing product catalog configuration, systems rollouts, implementation coordination, and business/tech translation. I understand messy operational handoffs before automating them.

Current target niches:
- NYC/metro property management and real estate operations
- Construction, plumbing, HVAC, skilled trades
- Wholesale distribution
- Insurance/Salesforce/Agentforce only when Salesforce stack and buyer trigger are confirmed

Current services/offers:
- AI Context OS Sprint: $2,500
- n8n Workflow Automation: $3,500
- Agentforce Activation/Implementation: $6,500
- AI App Development: $4,500

Current proof:
- Aya: completed $1,500 construction dashboard. StreetEasy/co-living work is no longer active proof.
- Altmark: paid client. Insurance expiration workflow live and paid. Rent delinquency workflow paid initial 50%, currently top proof/revenue gate. Proof must stay privacy-safe unless accepted/anonymized/permissioned.
- Internal proof assets: PM Front Desk + Exception Desk, AI Ops Teardowns, n8n workflow concepts/templates, property maintenance triage, construction job tracker, wholesale order-intake/reorder concepts.

Current outreach system:
- Pipeline researches prospects, scores T1/T2/T3, drafts LinkedIn/email, syncs drafts/decks to Drive, then I manually send.
- T1 = 80+ score with strong proof proximity and buyer/channel quality; custom proof-led outreach; custom demo only if reusable IP.
- T2 = 60-79; niche template, buyer/channel validation, no custom demo before reply unless reusable template can be configured fast.
- T3 = 40-59; market-sensing only, no custom build/deck/demo.
- Contact completeness rule: send-ready prospects should have both LinkedIn profile URL and verified email.
- Current sequencing: LinkedIn M1 day 1, LinkedIn M2 day 3-4, email day 8-11 if no reply and verified email exists. LinkedIn + email same day is banned.
- JT never auto-sends through agents. All outreach is manually reviewed and sent.

Current cold message principles:
- Lead with the prospect’s world, not my bio.
- Keep M1 short: specific observation, implied operational problem, soft curiosity CTA.
- M1 usually avoids proof/demo; M2 introduces proof or a useful artifact.
- Low-friction CTAs like “Curious what that process looks like right now?”
- Calendly only after positive reply or later follow-up, not M1.

Known failure:
- Across months of outreach, I have gotten 0 responses.
- This likely means the issue is not only copy. It may be offer-market fit, trust gap, proof visibility, channel strategy, targeting, timing, weak CTA, not enough volume, not enough social proof, too much cold direct pitch, or a mismatch between “I can help” and “I already did the work for you.”

My original instinct:
I wanted to build workflows, decks, diagnostics, and artifacts first so I could send prospects something proactive: “I already mapped/built the workflow for your type of business. If you hire me, this becomes yours.” The aim is to stick out from generic cold pitches by showing specific work already done, without overbuilding bespoke demos for bad-fit prospects.

What I need from you:

1. Diagnose why the current strategy likely produced 0 responses.
   - Separate copy problems from strategy problems.
   - Identify the top 5 failure modes ranked by likelihood and impact.
   - Be blunt. If the current sequencing or no-proof-in-M1 rule is wrong, say so.

2. Decide the optimal strategic shift.
   - Should I move from cold-message-first to artifact-first?
   - Should M1 include a screenshot, workflow map, Loom, teardown, one-page diagnostic, or “I mapped this for you” asset?
   - Which artifact is most likely to create replies from property managers, contractors, distributors, or Salesforce/insurance operators?
   - What should be built once and reused versus customized per prospect?

3. Redesign the outbound operating system.
   - ICP priority for the next 30 days.
   - Prospect scoring changes.
   - Minimum proof/artifact required before sending.
   - Channel strategy: LinkedIn DM, connection request, email, comment warm-up, referral, content reply, or direct company form.
   - New touch sequence with timing and what each touch contains.
   - Volume targets realistic for a solo consultant.
   - Clear stop rules so I do not keep chasing dead prospects.

4. Rewrite the offer framing.
   - Make it specific, buyer-readable, and hard to dismiss.
   - Avoid generic “AI automation” language.
   - Use my Spectrum BSA/operator background without sounding like a resume.
   - Frame the deliverable as a low-risk operational improvement, not a vague AI project.

5. Give me concrete assets to create.
   - Name 3 reusable proof assets I should build first.
   - For each: target niche, buyer pain, what it shows, format, how long it should take, and how it plugs into outreach.
   - Include one “sendable screenshot/one-pager” spec for the highest-leverage asset.

6. Produce new outbound examples.
   - Give me M1, M2, and email-pivot examples for:
     a) NYC property management
     b) plumbing/HVAC/skilled trades
     c) wholesale distribution
   - Include versions with and without an attached artifact.
   - Keep them short, human, and non-salesy.

7. Design a measurement loop.
   - What should I track per prospect?
   - What counts as signal before changing strategy?
   - How many sends are needed before judging a message/asset?
   - What weekly review should decide?

Constraints:
- Do not recommend mass-blast spam.
- Do not recommend pretending I built something custom if it is a template.
- Do not use fake case studies or unverifiable metrics.
- Do not rely on public client naming unless permissioned.
- Do not recommend developer-heavy positioning.
- Do not give me generic cold email advice.

Output format:

Start with:
“The current system is failing because…”

Then provide:
1. Brutal Diagnosis
2. Optimal Strategic Shift
3. New 30-Day Outbound System
4. Proof/Artifact Stack
5. Revised Offer Framing
6. New Message Examples
7. Measurement Loop
8. Immediate Next 72 Hours

For “Immediate Next 72 Hours,” give me exactly 5 actions in order. Each action must be concrete enough for an AI agent or me to execute.
```

