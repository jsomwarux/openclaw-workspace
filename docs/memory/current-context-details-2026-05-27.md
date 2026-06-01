# Current Context Details — 2026-05-27
> Source: `MEMORY.md`. Extracted to keep bootstrap memory near 90% of budget.

## Content System Detail
- Content niche source of truth: `memory/content/current-niche-map.md`. Default LinkedIn content prioritizes consulting/proof + authority/career lanes before product/app lanes. Claude Code is a tool/proof ingredient, not a primary niche.
- Recurring content must use platform+niche reference mechanics, not generic swipe claims. New LinkedIn/X queues must save source URL, platform, niche, format, hook mechanic, opening-line mechanic, proof mechanism, emotional driver, specificity level, CTA type, why it worked, and JT translation, then pass `content_distribution_guard.py --require-reference-map`; `content_calendar_audit.py` enforces both LinkedIn and X reference maps.
- App Marketing OS owns low-cost acquisition/research/hooks/scoreboarding/tasks. Current reset: TikTok/ReelFarm slideshow posting paused after 0-view behavior; recommendations capped at `Medium - hypothesis` until 20+ normally distributed posts/account; Automation B is screenshot-demo only. Status: `memory/app-marketing/current-status-2026-05-26.md`; calibration: `memory/reelfarm/calibration-2026-05-27.md`.
- Swipe-file generation must fetch Notion Viral Posts Swipe references and include hook mappings in saved draft files. Priority niches: AI Consulting, NYC SMB, Construction, Property Management, Wholesale Distribution, Skilled Trades, AI Agents/OpenClaw, Job Market, Nash Satoshi/x402, Personal Brand.
- Sports GM / @dynastyjig Phase 1 detail: `docs/memory/sports-gm-content-system-current.md`. Drafts are niche-native trust content, not app promo; product names are banned by default. Daily packs need `Native pattern teardown` + `Rejected generic patterns`; reply targets must be <=24h old and cached pools are banned.

## App Product Detail
- Vista: App Store live at `https://apps.apple.com/us/app/vista-movie-taste-profiles/id6758186885`; durable SEO page live on jtsomwaru.com for 1–100 movie rating positioning.
- 2026-05-27 app-marketing reset: run a Vista-first, artifact-led growth sprint; use 5-7 total weekly app posts across the portfolio, with Vista getting 60-70%, Nash getting 20-30%, and Glow staying SEO/AI-search first until crawler/claim-safety/measurement gates are healthy.

## Active Automation Detail
- Passive-income strategist guard cron `e7d45070` runs Sundays 3:20PM ET and executes `scripts/passive_income_strategist_delivery_guard.py --send`.
- App Marketing OS task generation: `scripts/app_marketing_task_generator.py`; weekly reviews read self-improvement rules, assign states, rerun generator after metrics refresh.
- App Marketing OS web metrics: GA4/Search Console OAuth via `scripts/app_marketing_connectors/web_metrics.py`. Nash, Glow, and jtsomwaru.com integrations are live. Ref: `memory/app-marketing/ga4-integration-reference.md`.
- Crypto Morning requires fresh full-universe X API research before allocation delivery via `scripts/run-x-research.py` and `scripts/x-research-guard.py`; timeout 1200s.

## Strategic Decisions Detail
- 2026-04-26: Consulting acquisition wedge is contained 7-day ops bottleneck audits/prototypes, not broad AI transformation. First workflows: property maintenance triage, construction field-note to punch item/customer update, wholesale stock/ETA/order-status reply drafts.
- 2026-05-04: Exception Dashboard positioning: AI as exception layer, not chatbot. Draft: `memory/drafts/exception-dashboard-consulting-post-2026-05-04.md`.
- 2026-03-31: Consulting positioning remains practical AI implementation for ops-heavy SMBs until explicitly changed.
- 2026-03-23: No anime/NBA apps right now; prioritize B2B consultable products and client-work proof.
- AgentSync deferred; Mission Control is enough orchestration for now.
- Zapier MCP and Railway MCP not needed now; Selenium MCP still useful despite Cloudflare `/crawl`.
- x402 / agentic commerce remains an active content pillar and app-readiness lens. Post 1-2x/week max from operator-builder POV. Do not sell generic x402 installation to SMBs; frame tested work as Agent-Ready Revenue Layer / x402 Readiness Sprint for API/data/product companies. Source: `memory/consulting/agent-ready-revenue-layer/positioning.md`.
