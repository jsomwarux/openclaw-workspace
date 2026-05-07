# MCP Actions Roadmap — n8n, Meta Ads, Anthropic Finance, Pay.sh

Date: 2026-05-06

## Ranking for JT
1. **n8n-mcp** — highest priority because it accelerates paid consulting delivery.
2. **Meta Ads MCP / Pipeboard** — useful as read-only market and creative intelligence first; do not connect ad-spend controls yet.
3. **Anthropic financial templates** — evaluate for Altmark/family-office back-office demos and service packaging.
4. **Pay.sh** — sandbox-only strategic x402 evaluation; no mainnet wallet/funding.

## n8n-mcp optimal use
Use as a consulting delivery copilot, not autonomous production editor.

Best workflow:
`Client process doc → template search → node research → workflow draft → node validation → workflow validation → Eve QA checklist → test payloads → client runbook`

Guardrails:
- Never edit production workflows directly with AI.
- Work on copied/exported workflows or local dev instance first.
- No client credentials in MCP config during first eval.
- Require human approval before activation.
- Validate every node and full workflow; default params are unsafe.

## Meta Ads MCP optimal use
Use read-only first. The immediate value is market intelligence, not campaign management.

Best uses:
- Analyze competitor/app-category ad angles.
- Extract creative patterns: hook, offer, visual frame, CTA, funnel type.
- Validate whether a passive-income niche has paid demand.
- Inform app marketing for Vista, Glow Index, and Nash Satoshi.

Do not yet:
- Create campaigns.
- Change budgets.
- Upload creatives.
- Connect JT or client ad accounts to autonomous agents.

## Passive income agent integration
Meta Ads should be a paid-demand validation layer, not the idea source.

Add checks:
- Are advertisers actively spending in this niche?
- Are hooks/offers repeated across multiple advertisers?
- Are landing pages simple and productizable?
- Does paid acquisition imply a survivable CAC/LTV?
- Are competitors solving a narrow pain with weak UX?

## App marketing integration
For each product marketing cycle, use Meta Ads intelligence if available to create an angle brief:
- top hooks
- common claims
- visual patterns
- CTA/funnel patterns
- what to avoid because it is saturated

Product-specific:
- Vista: movie/social discovery, taste compatibility, Letterboxd-adjacent angles.
- Glow Index: skincare quiz, ingredient checker, dupe finder, beauty scoring, influencer-skeptic angles.
- Nash Satoshi: use cautiously. Crypto ads have platform restrictions. Favor fintech/AI investing/portfolio-risk angles over token promotion.

## Anthropic finance templates
Best fit is not “finance templates” broadly. Best fit is a local family-office/property-ops service wedge:
- month-end close checklist
- GL reconciliation
- statement audit-readiness
- KYC/vendor package review
- meeting prep / investment memo / market researcher

Evaluate these for Altmark/Yair referral demos.

## Pay.sh
Worth sandboxing because it validates x402. Not worth mainnet implementation yet.
