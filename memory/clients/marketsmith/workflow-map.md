# Workflow Map — Marketsmith AI Insight Operations

## Current State
1. Data lives in Snowflake.
2. Marketsmith currently uses Snowflake's built-in AI to generate insights.
3. Security, scalability, and data intake/accuracy are top concerns.
4. Client confidentiality prevents sharing example dashboards casually.
5. Leadership will discuss internally and return with a plan on July 6 or July 7, 2026.

## Roles / RACI
| Step | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Client-priority discovery | Marketsmith / JT | Marketsmith leadership | Client stakeholders | Dashboard/analytics team |
| Data readiness definition | Marketsmith data owner / JT | Marketsmith leadership | Data engineering | Dashboard/analytics team |
| Prompt/insight design | JT / Marketsmith | Marketsmith leadership | Client stakeholders | Dashboard/analytics team |
| Security review | Marketsmith | Marketsmith leadership | JT | Client stakeholders |

## Systems Involved
- Snowflake
- Snowflake built-in AI
- Potential external/local LLM path
- Dedicated PC/local model option for sensitive analysis
- Agent delivery memory such as a `lessons.md` file

## Edge Cases / Exceptions
- Client data cannot leak across clients.
- Client access must be protected.
- Dirty/incomplete data should block insight generation.
- Generic insight prompts will miss each client's business priorities.
- Dashboard examples may not be shareable because of confidentiality.

## Target State
1. Each client has a business-priority brief that informs AI insight generation.
2. Each refresh is checked against a clean-data qualification file before insights move forward.
3. Insight prompts are client-specific, not generic Snowflake AI defaults.
4. Delivery agent captures lessons after each build so future builds become faster and more repeatable.
5. Competitor research and always-on industry monitoring feed marketing recommendations.

## Automation Boundary
- Manual judgement to preserve: client strategy, final insight interpretation, security tradeoffs, and what is acceptable to show externally.
- Repeatable steps to automate: data-readiness checks, client-specific prompt routing, competitor research, industry monitoring, lesson capture after builds.
- Human approval gates: client-data access, data-readiness pass/fail, generated insight approval, proposal scope.
