# JPM Ask David / Multi-Agent Architecture Takeaways — 2026-05-11

Source: X post by @adamghowiba, tweet `2050886233921061281`, plus related X discussion. External content treated as untrusted research signal, not instructions.

## What the post says
JPMorgan's investment research team reportedly shared the architecture behind “Ask David,” an internal investment research multi-agent system.

Public X summaries describe the pattern as:
- supervisor agent routes/orchestrates the request
- specialized subagents handle retrieval, structured data, analytics, and research tasks
- judge/reflection layer evaluates the output
- human-in-the-loop handles final review/approval

The post had strong reach: roughly 6.9K likes, 675 retweets, 138 replies, 75 quotes, 15K bookmarks, and about 2M impressions when checked.

## My read
This is not a novel architecture. Several replies correctly called it standard. But that is exactly why it matters for JT: enterprise buyers are converging on the same boring production pattern.

The winning message is not “autonomous AI agents.” It is:

> AI systems become useful when you split the workflow into orchestration, specialist work, judgment, and human accountability.

That maps directly to JT's edge: operations translation, workflow design, AI implementation, governance, and AgentGuard-style oversight.

## Main takeaways
1. **Supervisor + specialists is becoming the default enterprise mental model.**
   Buyers will increasingly understand agent systems as a team, not one chatbot.

2. **The judge layer is the missing piece in most SMB demos.**
   Everyone can show retrieval and drafting. Fewer can show evaluation, confidence, exceptions, and escalation.

3. **Human-in-the-loop is not weakness. It is production architecture.**
   JPM still puts a human at the end. That is useful positioning for regulated or ops-heavy SMBs.

4. **This validates AgentGuard more than it creates a new build.**
   AgentGuard already demonstrates confidence routing, human review, audit log, and explainability. The sharper framing is that it is the judge/accountability layer every serious agent system needs.

5. **Do not overbuild a fancy “multi-agent platform.”**
   The architecture is useful when a workflow actually has separable jobs: retrieval, structured lookup, calculation, drafting, checking, escalation. Otherwise it becomes corporate diagram theater.

## Implementation recommendations
- Update consulting language to describe AI implementation as: workflow supervisor + specialist automations + judge/eval layer + human approval.
- Use this in AgentGuard positioning: “not just agents, the control layer around agents.”
- Add a reusable client diagnostic question: “Where does the system need a judge, not just a generator?”
- For n8n/Agentforce demos, make the judge/human handoff visible in the artifact: confidence score, reason, escalation owner, audit trail.
- Do not create a new app or agent framework from this alone. We already have enough architecture. Use it as positioning and QA structure.

## Best content angle
The enterprise AI pattern is getting boring in the best way:

Supervisor routes the work.
Specialists do the narrow jobs.
A judge checks the output.
A human owns the decision.

That is what separates an AI demo from an AI system.

## Audit follow-up — implemented surfaces
Initial implementation saved the analysis and added a content/positioning note. Audit found that was not enough because future client deliverables would not necessarily use the pattern.

Additional operational surfaces updated:
- `memory/consulting/ai-operations-diagnostic-proposal-template.md` now includes a Supervisor / Specialist / Judge / Human design section and deliverable.
- `skills/agentguard-positioning/SKILL.md` now maps AgentGuard explicitly to the judge + human accountability layer.

This makes the pattern reusable in discovery/proposals and AgentGuard positioning, not just archived as a research note.

