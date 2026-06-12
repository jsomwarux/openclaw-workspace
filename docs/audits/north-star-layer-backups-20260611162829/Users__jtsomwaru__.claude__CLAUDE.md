# Global Claude Code Configuration — JT Somwaru's Environment

## Who You're Building For
JT Somwaru — AI Automation Consultant, NYC. Founder of JT Somwaru Consulting.
Background: 6 years BSA at Spectrum Enterprise. Builds AI agents, n8n workflows, Agentforce agents, and apps.
Active clients: Aya (NYC real estate — construction tracker + StreetEasy scraper).
Target niches: construction, wholesale distribution, property management.

## Key Project Paths
- `~/projects/jtsomwaru-com/` → personal website (Next.js 15, Vercel auto-deploy on push to main)
- `~/projects/agentforce-agent/` → Salesforce Agentforce agents — ALWAYS `git pull origin main` before any work here
- `~/projects/jt-consulting-pipeline/` → client research + outreach pipeline (research-agent, n8n-agent, analysis-agent)
- `~/projects/crypto-agent/` → crypto portfolio tracking

## MCP Servers
- **context7** ✅ INSTALLED (remote MCP, no auth required) — injects live, up-to-date library docs into context. Prevents hallucinated API methods and deprecated patterns.
  - **Usage:** Add `use context7` anywhere in your prompt. Works automatically.
  - **When to use:** Any build touching Next.js APIs, Supabase, Salesforce/Agentforce SDK, OpenAI SDK, or any library where docs drift matters. Mandatory for overnight autonomous builds.
  - Supports: Next.js, React, Supabase, MongoDB, Stripe, OpenAI, Anthropic SDK, and thousands more.
- **n8n-mcp** ✅ INSTALLED (API key configured) — MCP server with docs for 1,084 n8n nodes (537 core + 547 community), 2,646 real node configurations, 2,709 workflow templates. Prevents hallucinated node names and wrong property schemas.
  - **Setup:** Sign up at dashboard.n8n-mcp.com (free tier: 100 calls/day), get API key, add as `Authorization: Bearer <key>` header in settings.json.
  - **When to use:** All n8n workflow builds. Supersedes context7 for n8n-specific work — use both together.
  - **n8n Build Rule update:** Add "query n8n-mcp for [NodeName] node schema before writing any node configuration" to sub-agent prompts.

## Model Routing Guardrail
- Default OpenClaw conversation and cron routing should use OpenAI OAuth (`openai/gpt-5.5`) without OpenRouter/Moonshot/Anthropic fallback chains. Add non-OpenAI routing only for an explicit, named task that justifies the cost and has JT approval.
- OpenClaw cron volume guard: run `python3 ~/.openclaw/workspace/scripts/cron_volume_guard.py`. Current cap is ≤35 scheduled invocations/day average and ≤28 agentTurn/day average; >30/day is warning territory. Do not disable useful crons just to satisfy the retired blunt ≤20/day cap.
- If OpenClaw reports "Preflight compaction required but failed" in any form, immediately tell JT the exact error. Do not modify compaction config, restart the gateway, or delete files.

## Plugins
- **claude-context-mode** ✅ INSTALLED (v1.0.18) — loads files into context by reference instead of full content. Use on any session working with large codebases.
- **design-and-refine** ✅ INSTALLED — generates 5 distinct UI variations side-by-side, collects Figma-style feedback, synthesizes a refined version. Reads your existing Tailwind config/CSS variables automatically. Outputs `DESIGN_PLAN.md` + `DESIGN_MEMORY.md` when done.
  - Install: `/plugin marketplace add 0xdesign/design-plugin` then `/plugin install design-and-refine@design-plugins`
  - Usage: `/design-and-refine:start` or `/design-and-refine:start ComponentName`
  - Cleanup: `/design-and-refine:cleanup`
  - **Requires dev server running** — start `npm run dev` before invoking. View variations at `http://localhost:3001/__design_lab`
  - Use for: new components/sections on jtsomwaru.com, client dashboard UI (Aya, Guyana demos), any time you're unsure which layout/density approach is right
  - Do NOT use for: copy-only changes, single-prop tweaks, overnight/autonomous builds (requires JT present)

## Superpowers Plugin (v5.0.1)

Installed and auto-loads on session start. Provides composable skills for structured development.

### Workflow by work type

**Client deliverables + overnight builds (reliability > speed):**
1. `brainstorming` → clarify requirements before any code
2. `writing-plans` → 2-5 min tasks, exact file paths, verification steps
3. `subagent-driven-development` → fresh subagent per task, two-stage review
4. `test-driven-development` → RED-GREEN-REFACTOR, no exceptions
5. `systematic-debugging` → 4-phase RCA on any failure
6. `verification-before-completion` → always before declaring done

**Quick demos / prototypes (speed > reliability):**
- `brainstorming` + `writing-plans` only
- Skip TDD and subagent workflow
- Execute directly

**Debugging (always use this, never ad-hoc):**
- `systematic-debugging` → 4-phase: observe → hypothesize → test → verify
- `verification-before-completion` → before declaring fixed
- **Hard rule: never change more than one variable at a time.** Isolate the cause first, confirm it, then apply the minimal fix. Multiple simultaneous changes = you don't know what worked or what broke something else.

### Available skills
brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, test-driven-development, systematic-debugging, verification-before-completion, requesting-code-review, receiving-code-review, using-git-worktrees, finishing-a-development-branch, writing-skills, using-superpowers

### Commands
- `/brainstorm` — refine spec before writing code
- `/write-plan` — break work into verified task chunks
- `/execute-plan` — run plan with checkpoints

## Planning Mode Rule
For ANY non-trivial feature (more than a copy change or single-component edit):
1. Shift-tab into planning mode first
2. Include "research best practices and known issues using web search" in the prompt
3. READ the plan — adjust before executing
4. Plans survive context compaction. Vibe-prompted features do not.

## Reference Documents
- `~/.openclaw/workspace/documents/ICPs.md` — Ideal Customer Profiles for all 4 JT consulting niches. Load for any research, outreach, proposal, or content work.
- Consulting prospect tiers are score-gated in `~/.openclaw/workspace/skills/opticfy-pipeline/SKILL.md`: T1 = 80+ proof-led custom, T2 = 60-79 template/validation, T3 = 40-59 market-sensing only.
- `~/projects/jtsomwaru-com/documents/styleguide.md` — full visual system for jtsomwaru.com (colors, typography, component patterns). Load before any UI work on the site.
- App Marketing TikTok/ReelFarm status as of 2026-06-06: Vista, Nash, and Glow TikTok accounts are in manual warm-up after 0-view/throttling. Daily 2:00PM ET reminder cron `8033e775-29d2-42f2-83e9-1392352f6493` and 7:45PM ET reminder cron `d163df4a-5d96-4de7-90eb-0242b671800e` nudge JT to warm accounts. Do not treat slideshow tasks as overdue or resume auto-post scaling. Use `~/.openclaw/workspace/memory/app-marketing/tiktok-reentry-plan-2026-06-01.md`; JT owns manual TikTok posting, Eve owns source tags, post-registry reconciliation, and 24h/72h/7d metric capture.

## Overnight / Autonomous Builds
Builds run without human oversight. Reliability is the only metric that matters.
- OpenClaw Phase 7 merged the old 9:45PM Nightly Leverage job and 3:20AM Overnight Autonomy job into `Night Autonomy Agent` at 11PM ET. Autonomous completion authority is limited to content ready state, complete prospect packets for JT to send, and ops self-healing.
- Always use the full client deliverable workflow (brainstorming → plan → subagents → TDD)
- Commit incrementally — never one giant commit at the end
- If a test fails: use systematic-debugging, do NOT skip or comment out tests
- When done: `openclaw system event --text "[project] build complete — [summary]" --mode now`

## Code Standards
- TypeScript strict mode — no `any` unless absolutely unavoidable
- `next/image` for all images in Next.js projects (no raw `<img>` tags)
- No `console.log` in production code
- Mobile-first responsive design (Tailwind responsive prefixes on all layout elements)
- Commit messages: conventional commits format (`feat:`, `fix:`, `chore:`)
- Always run `npm run build` before pushing — catch TypeScript errors locally

## GEO (AI Search Optimization)
jtsomwaru.com is optimized for AI search engines (ChatGPT, Perplexity, Claude).
- `public/llms.txt` → machine-readable site summary for LLMs
- JSON-LD schema on all pages (Person + WebPage types)
- `robots.txt` allows all AI crawlers (GPTBot, PerplexityBot, ClaudeBot, etc.)
Keep these files accurate when updating site content.
## Eve workflow skills added 2026-05-11
- `~/.openclaw/workspace/skills/workflow-skillify/SKILL.md`: use when JT says skillify/make repeatable/bake this in, or when a repeated workflow/correction should become a durable skill/checklist/regression check.
- `~/.openclaw/workspace/skills/high-stakes-draft-eval/SKILL.md`: use before important outreach, positioning, proposals, job applications, landing page copy, or when checking whether copy reads generic.
- `~/.openclaw/workspace/consulting/entity-propagation/template.md`: use as the lightweight consulting fact propagation template for client/prospect/contact/pipeline/daily-note consistency.

## JT Content Voice Guard Delta — 2026-06-07
- `~/.openclaw/workspace/scripts/jt_voice_guard.py` now includes the high-signal Stop Slop delta: false agency, narrator-from-distance phrasing, vague declaratives, generic Wh-opener setups, pull-quote endings, and high-confidence passive voice.
- Do not apply generic anti-slop rules wholesale. JT's content should keep practical qualifiers and concrete constraint stacks when they prove judgment.
## GBrain consulting recall pilot — 2026-05-11
- Sandbox install: `~/projects/gbrain`; pilot home: `~/projects/gbrain-pilot-home`; sanitized source: `~/projects/gbrain-pilot-source`.
- Use `~/.openclaw/workspace/scripts/gbrain-consulting-search.sh "Entity"` only for consulting/prospect entity lookup.
- Pilot result: entity lookup useful; natural-language recall weak without embeddings.
- Do not add GBrain crons, skillpacks, broad ingestion, or embedding/auth wiring without JT approval.

## Code-Agent Failure Prevention — 2026-05-11
For non-trivial build work, follow the concise 12-rule checklist in `~/.openclaw/workspace/docs/agents/workflow-protocols.md` before coding: assumptions, simplicity, surgical edits, success criteria, model-only-for-judgment, context budget stop/summarize, conflict surfacing, read-before-write, intent tests, checkpoints, conventions, fail loud. Keep project CLAUDE.md files short; do not paste long generic examples into them.

## Goal-Mode / Long-Running Agent Work — 2026-05-11
Codex `/goal` is not currently installed/enabled in JT's OpenClaw environment. Do not install/enable/change Codex or OpenClaw config without JT approval. For any long-running autonomous goal, use `~/.openclaw/workspace/templates/goal-mode-spec-template.md` and the Goal-Mode rule in `~/.openclaw/workspace/docs/agents/workflow-protocols.md`: one durable objective, allowed/forbidden scope, stop condition, validation evidence, checkpoints/progress log, board visibility, budget/stop rules, and completion audit.

## Mission Control North Star Priority Audit — 2026-05-12
## Material Delta Task Rule — 2026-05-31
Whenever a material delta is implemented — artifact, queue, research finding, proof pack, Drive bundle, automation, or decision-ready output — add or update the single optimal Mission Control next-use task. Cite the path/link, assign the real owner, set the right priority/order, and include first action + why + done state. If no task is justified, log why.

- Daily Morning Brief flow now runs `python3 /Users/jtsomwaru/.openclaw/workspace/scripts/mission_control_north_star_audit.py` before surfacing tasks.
- Purpose: keep Mission Control high-priority layer aligned to JT's North Star: immediate consulting cash, client proof, warm opportunities, current app distribution, and health/financial stability.
- Guardrail: the auditor patches priority/sortOrder/description only; it does not delete tasks or send external messages.
- Report path: `/Users/jtsomwaru/.openclaw/workspace/reports/mission-control-priority/YYYY-MM-DD.md`.

## Autoresearch Sweep — 2026-05-12
- Cron `ec9f36d3-3bf8-4bc9-a4b1-06aa886a24ff` runs Mon/Wed/Fri 11:15 AM ET.
- It reads `agents/autoresearch/weekly-sweep-prompt.md`, selects one high-value pending/active target, scores it against its checklist, applies validated small improvements, updates `targets.md`, appends `results.tsv`, and logs inputs/results/changelog.
- Guardrail: one target per run, max 3 test inputs, max 5 rounds, cost cap $0.50, no Telegram unless blocker/error/material improvement.

- 2026-05-12: AI Ops Teardown Agent active at `~/.openclaw/workspace/agents/ai-ops-teardown/`; cron `f96cc24f` runs Sunday 7:15PM ET and produces one review-ready “If I were building AI ops for...” bundle without auto-posting.

## JT Operating-System Routing — 2026-05-31
- Capability map: `~/.openclaw/workspace/docs/agents/capability-routing-map.md`.
- New skills: `client-proof-capture` for accepted/shipped client work becoming proof/IP/referrals/content; `plan-review-pack` for turning internal plans/specs into human-readable client/collaborator review artifacts; `linkedin-corpus` for LinkedIn post/account intake and pattern extraction; `ai-context-os` for agent-ready company context, knowledge readiness, and eval-pack sprint delivery.
- New agents: `agents/client-proof-engine/AGENT.md` and `agents/linkedin-corpus/AGENT.md`; both are registered in Mission Control.
- Portable plugin scaffold: `~/plugins/jt-operating-system` with marketplace entry at `~/.agents/plugins/marketplace.json`.
- Consulting pipeline repo now has `~/projects/jt-consulting-pipeline/CLAUDE.md` and `AGENTS.md`; read them before changing prospect/client/delivery/proof files there.

## JT Toolkit Synthesis — 2026-06-02
- Audit source: `https://github.com/jsomwarux/jt-claude-toolkit`; synthesis doc: `~/.openclaw/workspace/docs/agents/jt-toolkit-synthesis-2026-06-02.md`.
- Adopted the useful portable pieces into OpenClaw: `skills/n8n-blueprint`, `skills/proposal-pdf`, `skills/product-build-loop`, `agents/workflow-strategist`, `agents/product-quality-pass`.
- Expanded Codex plugin `~/plugins/jt-operating-system` to v0.2.0 with those three extra skills.
- Keep project `CLAUDE.md`/`AGENTS.md` thin: local stack, paths, commands, credentials references, lessons, and hard constraints only. Reusable proposal/workflow/product quality method belongs in skills/plugins.
- Do not import Claude toolkit's `resume-tailor`, generic `new-client`, or global prettier hook as-is; OpenClaw job-application, consulting pipeline, and repo-specific formatting rules are stricter.
