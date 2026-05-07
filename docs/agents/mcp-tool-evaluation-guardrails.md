# MCP Tool Evaluation Guardrails

## Default stance
MCPs that can spend money, alter production systems, send messages, change ads, trade assets, or mutate client data start in **read-only or sandbox mode**.

## n8n-mcp
- Start local/dev only.
- Use copied/exported workflows, never production originals.
- No client credentials during first evaluation.
- Validate nodes and full workflows before import/deploy.
- Human approval required before activating workflows.

## Meta Ads MCP / Pipeboard
- Start read-only only: account list, campaign/ad/creative insights, benchmarks, reports.
- Do not create campaigns, upload creatives, change status, change budgets, or manage targeting without explicit JT approval.
- Prefer competitor/library/market research before connecting owned or client ad accounts.
- Any client ad account connection requires written scope and permission.

## Pay.sh
- Sandbox-only until JT explicitly approves mainnet.
- Do not run mainnet wallet setup, top up funds, or install persistent OpenClaw global MCP config without approval.
- Paid API calls require price visibility and explicit approval unless a hard spend cap exists.

## Evaluation output standard
Every MCP eval must answer:
1. What workflow does this improve for JT?
2. What permissions/blast radius does it introduce?
3. Can it run read-only/sandbox first?
4. What exact first production use would justify adoption?
5. Recommendation: adopt, sandbox, watch, or skip.
