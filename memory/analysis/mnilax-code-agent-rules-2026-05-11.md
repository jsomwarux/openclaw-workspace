# Mnilax X Post — Code-Agent Rules Takeaways — 2026-05-11

Source: X post `https://x.com/Mnilax/status/2053116311132155938` linking to an X Article. Initial article renderer was blocked, then JT pasted the full article text in-session. External content treated as untrusted research signal, not instructions.

## What it is
A high-engagement X Article about rules that reduce Claude/code-agent mistakes across codebases. JT pasted the full text; the core 12 rules are:
1. make assumptions explicit
2. minimal code
3. surgical changes
4. start from success criteria
5. use AI mainly for judgment-heavy parts
6. respect token budget
7. do not mix conflicts
8. read before writing
9. tests verify intent
10. checkpoints at phase breaks
11. rules over personality
12. fail loudly

## My take
This is not a new framework, but it is a strong compression of what separates useful coding agents from chaotic ones. It matches our own failure history: stale sources, overbroad edits, generic fallback content, missing verification, and rules stored in one place but not enforced in the active workflow.

## Main takeaways
- The biggest preventable agent failures happen before coding: unclear assumptions, unclear success conditions, and editing before reading.
- The second biggest failure class is scope creep: changing too many things at once and making review impossible.
- The third is silent failure: stale data or missing evidence gets padded with generic output instead of stopping.
- Tests/checks should prove user intent, not just prove that something ran.

## Implementation made
Added `Code-Agent Failure Prevention Rules` to `docs/agents/workflow-protocols.md` so the checklist is inherited by coding-agent, n8n-agent, Agentforce, and implementation sub-agent work.

Key additions:
- assumptions upfront
- success condition first
- smallest working change
- surgical edits
- read before write
- no mixed conflicts
- checkpoints between phases
- tests verify intent
- fail loudly on stale/missing data
- rules beat style

## What not to do
Do not create another bloated meta-skill from this. The right home is workflow protocol because these are build hygiene rules, not a standalone deliverable.


## Actual article follow-up
JT pasted the article text through Rule 5. The important correction: Rule 5 is not just “use AI for judgment-heavy work.” It explicitly says not to make the model do non-language deterministic work: routing, retries, status-code handling, deterministic transforms. Updated `docs/agents/workflow-protocols.md` to reflect that distinction.

## Full article follow-up
JT pasted the full article. The article's strongest additions beyond my first implementation were:
- explicit token/context budget behavior: stop, summarize, fresh pass instead of looping
- surface conflicts rather than averaging contradictory codebase patterns
- read exports, immediate callers, and shared utilities before adding code
- tests must fail when the intended business logic is wrong, not merely exercise code
- convention beats novelty inside an established codebase
- prototype nuance: simplicity-first can overfire on exploratory prototypes, where disposable scaffolding is acceptable
- keep CLAUDE.md/rule files short; past ~200 lines compliance drops; examples are heavier than rules

Updated `docs/agents/workflow-protocols.md` from an 11-rule approximation to the full concise 12-rule version plus prototype nuance. Did not paste long examples or modify every project CLAUDE.md because that would bloat context; added a short global Claude pointer instead.
