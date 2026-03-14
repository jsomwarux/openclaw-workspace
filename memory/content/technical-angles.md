# Technical Content Angles — JT Somwaru
*Source material for technical/builder content on X and LinkedIn.*
*Updated when new architecture decisions are made or lessons are learned.*
*Load this file when generating technical posts for Tuesday, Thursday, or Saturday X slots.*

---

## What This Content Is

JT runs a personal AI operating system (Eve) built on Claude + OpenClaw on a Mac mini — 20+ autonomous crons, multi-agent orchestration, self-improvement loops, overnight builds. He also builds client-facing Agentforce and n8n systems professionally.

This content is NOT tutorial content. It's **earned observations** from someone actually running this infrastructure at scale. The difference:
- Tutorial: "Here's how to write a CLAUDE.md file"
- Earned: "After 6 months of running isolated cron agents, the CLAUDE.md hierarchy that actually holds up is three levels: global → project → agent. Anything above that adds complexity without leverage."

---

## Content Angles Bank

Each angle has an `angle_id` in brackets — use this in `posted-log.jsonl` when you post it so the system knows which angles have been used recently.

### Agent Architecture & Design
- `[arch-isolated-split]` **Isolated vs. main session split:** Why content generation and content delivery are separate crons. The generator runs isolated (no conversational context needed, just file I/O). The delivery runs fast in 60 seconds. If both are in one job, a generation failure kills the delivery. Separation = reliability.
- `[arch-overnight-constraints]` **The overnight agent constraint:** Max 2 tasks, hard $1.50 cost cap, no external sends. Constraints don't limit the agent — they make it reliable. An unconstrained overnight agent is a liability.
- `[arch-heartbeat-vs-cron]` **Heartbeat vs. cron distinction:** Heartbeats (main session, 4x/day) carry conversational context but can drift on timing. Crons (isolated, exact schedule) have no context but execute precisely. Using the wrong type for the wrong job is a common source of failures.
- `[arch-isolated-model-ids]` **Why isolated sessions need explicit model IDs:** Discovered via a $0.57 Opus invocation when model wasn't set. Isolated crons don't inherit session defaults — you specify the model or you get the most capable (most expensive) one. Always explicit.
- `[arch-state-machines]` **State machines > conversational agents for reliability:** Conversational agents accumulate context debt over long tasks. State machines (read state.json → execute → write state.json) are predictable, debuggable, and resume correctly after failure.
- `[arch-stop-conditions]` **The stop condition rule:** Every autonomous agent needs an explicit STOP condition — not just what to do, but what NOT to do and when to exit. Agents without stop conditions drift.

### CLAUDE.md & Prompt Engineering
- `[claude-md-3level]` **Three-level CLAUDE.md hierarchy:** Global (`~/.claude/CLAUDE.md`) for identity, standards, and cross-project patterns. Project-level for stack specifics, component inventory, and project rules. Agent-level (in AGENT.md) for hard constraints and isolated session instructions. Most people only use one level.
- `[claude-md-hard-constraints]` **Hard constraints must live in AGENT.md, not MEMORY.md:** Isolated sessions never read MEMORY.md. "Never do X" decisions that apply to agents must be in the agent's own file. Learned via an overnight agent re-adding a banned project card three times because the ban only lived in MEMORY.md.
- `[claude-md-budget]` **Context window budget discipline:** Bootstrap files (AGENTS.md, MEMORY.md, SOUL.md, etc.) share a 24k char budget and are silently truncated past the limit. Every instruction above that limit is invisible. Size awareness is a forcing function for clarity.
- `[claude-md-prompt-density]` **Prompt density:** The cleaner the prompt, the more of the instruction set the agent actually follows. Overstuffed prompts produce agents that follow the first 60% and drift on the rest. Each isolated cron prompt should do one job.
- `[claude-md-model-routing]` **Model routing strategy:** Anthropic direct (OAuth subscription, $0 real cost) for all Claude work. OpenRouter prefix only for non-Anthropic models (real cost). Never let an isolated session default-route to a paid model without explicit routing. The architecture: OAuth → zero Anthropic costs, OpenRouter → pay-per-use for everything else.

### Cron Architecture & Operations
- `[cron-invocation-cap]` **The 20/day invocation cap:** With 4 heartbeats + 3 content sends + 1 skills researcher + 2 crypto + 1 morning brief + overnight + etc. = you hit the daily limit fast. Every new cron displaces an existing one. Design accordingly.
- `[cron-offset-pattern]` **The offset pattern:** Heartbeat at :00, pending task processor at :30. Never overlap two main-session jobs. Overlapping main-session crons don't queue — one runs while the other fires silently and fails.
- `[cron-timeout-sizing]` **Timeout sizing:** Most cron timeouts should be 2-3x the actual expected runtime. Under-sized timeouts (the default) create consecutiveErrors logs that look like bugs but are just timing. Set the timeout for the worst case, not the median.
- `[cron-no-delete-after-run]` **deleteAfterRun = never:** One-shot jobs that fire, execute, and delete themselves created a past-due scheduler loop that caused a full outage. All jobs persist with deleteAfterRun: false. Historical run logs > storage savings.
- `[cron-cost-tracking]` **Cost tracking by job:** Appending `[ISO timestamp] | job-name | searches: N | cost: $X` to a log file per agent makes cost spikes traceable. Without per-job tracking, daily totals are meaningless.

### Memory Architecture
- `[mem-hierarchy]` **The memory hierarchy:** MEMORY.md (long-term facts, decisions, state) → daily notes memory/YYYY-MM-DD.md (session log, what happened today) → knowledge base (structured KB for external intel). Three layers, each with a different read frequency and different write trigger.
- `[mem-film-review]` **Film review loop (10AM daily):** Read yesterday's daily note, find one mistake or friction point, fix it in the right file, log the fix. Compounding improvement over time. Not journaling — engineering.
- `[mem-mistakes-structure]` **Mistakes log structure:** Every entry requires three fields: specific failure, root cause one level deeper than "I forgot," concrete rule that prevents recurrence. An entry missing any of the three is incomplete. This constraint forces actual learning rather than acknowledgment.
- `[mem-readable]` **Why MEMORY.md stays readable:** It's read on every session start and shares a budget limit. Every line has to earn its place. The habit of distilling daily notes → MEMORY.md weekly removes noise before it accumulates.

### n8n & Workflow Automation
- `[n8n-vs-make]` **n8n vs. Make:** n8n is self-hosted, no per-task pricing at scale, runs inside your infrastructure. Make charges per operation — fine at low volume, punishing at scale. For clients with recurring high-volume workflows, the math matters.
- `[n8n-streeteasy-arch]` **The StreetEasy scraper architecture:** n8n handles scheduling and HTTP requests. Python handles parsing and filtering (n8n's built-in nodes don't parse DOM well). Google Sheets API handles output. Three tools, each doing what it does best.
- `[n8n-webhook-first]` **Webhook-first design:** Build the workflow around the inbound data shape, not around the tool capabilities. If the data is messy, clean it at ingestion, not mid-workflow.

### Agentforce-Specific
- `[af-reality-gap]` **What Agentforce actually does vs. what's advertised:** It handles multi-topic routing, Salesforce record creation, and response generation within a Salesforce org. What it doesn't do: external API calls without custom Apex, complex state management, anything outside the Salesforce data model without bridges.
- `[af-org-chart]` **The org chart problem:** The hardest part of building an Agentforce agent isn't the agent. It's getting internal alignment on what the agent is allowed to decide vs. what requires human escalation. Every organization has unofficial rules the agent has to learn.
- `[af-topic-boundaries]` **Topic boundaries matter more than instructions:** An Agentforce agent with well-scoped topics and clear escalation paths outperforms a single-agent setup with exhaustive instructions. Narrow the scope, improve the reliability.
- `[af-apex-bridge]` **Apex is the bridge:** Anything the agent needs to do that isn't native Salesforce — external API call, custom calculation, complex logic — goes through an Apex action. The agent calls the action; the action handles the complexity. Clean separation.

### Agent Design Patterns
- **[arch-split-by-constraint]:** **Split sub-agents by output constraint, not just by domain:** Anthropic's solo growth marketer split ad copy generation into two agents — one writing only headlines (30 char cap), one writing only descriptions (90 char cap). The constraint IS the specialization. One agent trying to satisfy multiple format requirements will compromise quality on all of them. JT application: vibe marketing agent currently generates X posts + TikTok scripts + Reddit in one pass. Could split into format-specific agents (short-form text agent, script agent, long-form agent) if quality needs to go up. General rule: when output has a hard character/time/format limit, give it its own agent.

### Agent Architecture Patterns
- **[arch-company-structure]:** **"Structure your AI like a company" as a design principle:** One monolithic agent trying to do everything fails the same way a one-person company fails — context overload, competing priorities, no specialization. The agency-agents repo (10k+ stars in 7 days) proved the market wants this framing. JT proof point: Eve already runs this way — 23+ specialized crons each with narrow scope (crypto morning, content generate, outreach pipeline, overnight autonomy) rather than one agent handling everything. The architecture validates itself by staying under rate limits and producing higher quality per task.

### Positioning & Mindset (shareable frames)
- `[pos-agent-jockey]` **"Agent jockey" as identity:** The job title nobody has yet but everyone running AI agents is doing. You're not a developer. You're not a marketer. You're an agent jockey — you describe workflows, the agents execute them, you polish outputs. The "middle work" disappears. JT proof point: 20+ autonomous crons across consulting, crypto, content, jobs, and Spanish learning — none of it required writing a single line of code.
- `[pos-compounding-loops]` **Compounding loops as the real leverage:** `idea → API chain → live data → auto-optimization → redeploy → repeat`. Not a one-time automation. A loop that compounds. JT proof point: vibe marketing system generates content → scores it → you post what works → performance-log feeds next week's generation → better content over time. Each iteration makes the next one smarter. Most people build automations. Few build loops.
- `[pos-thinking-in-apis]` **"Think in APIs" as a mindset shift:** Before you build anything, ask: does this tool have an API? If yes, an agent can use it. One env file with every API key you use — Facebook Ads, Notion, GA4, Slack — is the foundation of every automated workflow. The mindset isn't "what can I automate?" It's "what isn't connected yet?"

### Personal AI Infrastructure (Eve)
- `[eve-mac-mini]` **Why Eve runs 24/7 on a Mac mini:** Laptop AI = reactive. Mac mini AI = proactive. The infrastructure that matters runs when you're asleep: crypto monitoring, overnight builds, content generation, backup, cleanup. The shift from reactive to proactive is the actual leverage.
- `[eve-dedup-rule]` **The proactive work deduplication rule:** Before picking a proactive work item, check today's daily note. If it was already done, skip it. Without this check, the same item runs multiple times per day — looks like activity, burns budget, produces nothing.
- `[eve-self-improvement]` **Self-improvement loop:** Mistakes log + 10AM daily film review + weekly skills audit = a system that gets better at its own job over time. Not from retraining — from writing better rules and fixing broken ones.
- `[eve-gateway-freeze]` **The gateway freeze pattern:** Any synchronous subprocess call from the main session (like running `claude --print` via exec) blocks the gateway until it returns. 30+ second blocks = apparent freeze = forced restart. Rule: never run coding agents from the main session. Use sessions_spawn (background, push-based) only.

---

## Potential Angles (unbuilt)

*Flagged by the skills-researcher when a 🔴/🟠 tool or capability is surfaced that JT hasn't yet demonstrated.*
*These are topics JT COULD post about once the build exists. Do NOT use these as content until the underlying build or experiment is complete — mark clearly as unbuilt.*

*Format: `[date] [topic] — [why it's relevant] [source: URL]`*

<!-- Appended by skills-researcher when new capability gaps are surfaced -->
- [2026-03-13] **n8n CVSS 10.0 RCE (CVE-2025-68613)** — My entire consulting business runs on self-hosted n8n. A CVSS 10.0 RCE means a successful exploit = full server takeover, meaning client workflow data, API keys, and automation triggers are all exposed. Post angle: "The security update every self-hosted n8n user needs today — and why it matters more when client data is on the line." JT proof point: Aya's StreetEasy scraper + co-living dashboard both run through n8n. (source: https://securityonline.info/cisa-mandates-urgent-patch-for-maximum-10-0-cvss-n8n-rce-flaw/)
- [2026-03-13] **OpenClaw v2026.3.12 — 15 security patches in one release** — Invisible Unicode characters in exec approval prompts, workspace plugin auto-load bypasses, agent scope elevation via subagents. Post angle: "Running a self-hosted AI gateway means you're also running security operations. Here's what just got patched in OpenClaw and why it matters." JT proof point: Eve runs 23+ crons, the cron delivery breaking change could silently kill them all without a `openclaw doctor --fix`. (source: https://github.com/openclaw/openclaw/releases/tag/v2026.3.12)

---

## Update Log
- 2026-03-11: Initial bank created from 6 months of Eve operations + JT's consulting work
- 2026-03-11: angle_id markers added to all entries for rotation tracking

---

## How to Use This File

When generating technical X posts:
1. Pick 1-2 angles from the bank that haven't been posted recently (check posted-log.jsonl)
2. Apply the content-voice.md compression rules — these should be 1-3 sentences, not explanations
3. The angle should invite a reply: "what's your experience with this?" or an implicit challenge
4. Rotate through categories over time — don't cluster too many architecture posts in a row

New angles to add: any time a new architectural decision is made, a non-obvious problem is solved, or JT says "I learned this the hard way."

---

## Consulting Positioning Angles (added 2026-03-13)

- **AMS disruption → Salesforce advantage:** Traditional agency management systems built their moat on aggregating carrier data. AI agents do that now, free. Insurance agencies on Salesforce aren't being disrupted — they're positioned to win, because Salesforce is where the actual work runs (renewals, commissions, service tickets). The pitch: "Your competitor's AMS is getting replaced by AI. Your Salesforce isn't. Here's how to move fast." Angle: platforms-as-moats only hold if they own the workflow, not just the data layer. *(angle_id: consulting-ams-disruption-001)*

- **n8n logistics routing for distribution:** n8n now has a documented pattern for AI-powered multi-stop route optimization (GPT + routing API). Wholesalers running own-fleet delivery — garment district, food/beverage, hardware — have this problem and don't know a $3,500 n8n implementation can solve it. No custom dev. Just integration. *(angle_id: consulting-n8n-logistics-001)*
