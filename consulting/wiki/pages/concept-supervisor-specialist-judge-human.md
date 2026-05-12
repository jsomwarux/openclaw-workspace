# Supervisor / Specialist / Judge / Human

Type: concept
Created: 2026-05-11
Sources:
- `memory/analysis/jpm-ask-david-agent-architecture-2026-05-11.md`
- `memory/consulting/ai-operations-diagnostic-proposal-template.md`
- `skills/agentguard-positioning/SKILL.md`

## Summary
Enterprise AI systems are converging on a production control pattern:
1. **Supervisor** routes work and selects the workflow path.
2. **Specialists** do narrow jobs: retrieval, structured lookup, analysis, drafting, checking, updates.
3. **Judge** checks confidence, source support, completeness, risk, and exception conditions.
4. **Human** approves, overrides, handles exceptions, and owns accountability.

## Why it matters for JT
This makes JT's AI implementation positioning more concrete. He is not selling generic chatbots or “autonomous agents.” He is helping businesses convert messy workflows into controlled AI systems.

## Consulting use
Use in AI Operations Diagnostic and AI Enablement Sprint work:
- ask where the workflow needs a judge, not just a generator
- define escalation thresholds and human ownership
- make audit trail, confidence, and exception routing visible in the design

## AgentGuard mapping
AgentGuard is strongest as the **judge + human accountability layer**:
- confidence-based routing
- review queue
- override reason capture
- audit trail
- governance metrics

## Content angle
The enterprise AI pattern is getting boring in the best way: route the work, split narrow jobs, check the output, keep a human accountable. That is what separates an AI demo from an AI system.
