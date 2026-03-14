# Tasks

_Managed by Eve. Updated during heartbeats and on request._

---

## 🔴 High Priority

- [ ] **Apply to Squarespace People AI SA** — Score 19/25, posted Feb 21, salary $126K–$180K hybrid NYC. JD literally says "vibe-code." Time-sensitive — apply this week.
  **Steps:**
  1. Open resume: https://docs.google.com/document/d/12Uow8QM6w15DxaTGuekoQOIdehO66Th4USrhqwYdEyI/edit
  2. Fill in LinkedIn URL and correct Spectrum dates (I used 2019–2025)
  3. Add Education section if you want it
  4. Open cover letter: https://docs.google.com/document/d/1NZeeO2P4AuySixcKA1b-ACTENNb99rUTuUnMt6I3tAk/edit
  5. Review — especially Para 4 (People domain acknowledgement). Adjust tone if needed.
  6. Export both as PDF from Google Docs (File → Download → PDF)
  7. Apply at: https://jobs.technyc.org/companies/squarespace/jobs/68335131-people-ai-solutions-architect
  | Added: 2026-02-24

- [x] **Apply to Salesforce Lead Agentforce SE** — ✅ SUBMITTED. Score 24/25, $148K–$198K NYC. JT reconsidered after initial removal (2026-02-24) — application confirmed done in Mission Control. Deadline 03/27/2026 — watch for interview/follow-up. Link: https://careers.salesforce.com/en/jobs/jr329627/

- [x] **jtsomwaru.com — Personal Website** — ✅ LIVE as of 2026-02-24 ~5:30 PM EST
  - URL: https://jtsomwaru.com (also www.jtsomwaru.com)
  - Stack: Next.js 16 + Tailwind + Framer Motion → Vercel (iad1)
  - Sections: Hero, Work (8 projects), Services (3), About + timeline, Contact
  - SSL: Vercel auto-provisioned | OG/Twitter meta configured
  - Repo: ~/projects/jtsomwaru-com (deployed via CLI, GitHub repo not yet created)
  | Added: 2026-02-24 | Completed: 2026-02-24

- [x] **Feb 24 content drafts** — STALE, cleared 2026-03-13. Amodei/chatbot era/DeepSeek drafts are 3 weeks old and no longer timely. Content system now generates fresh weekly posts every Monday.
  | Updated: 2026-03-13

- [ ] **Vista pre-launch marketing** — 5 drafts live in Google Drive (Eve — Drafts/Vista/). Review + post when App Store approves.
  **Steps:**
  1. Check App Store Connect for review status: https://appstoreconnect.apple.com
  2. On approval: post X Thread (Launch) first → then Reddit r/Letterboxd → then Reddit r/iOSProgramming
  3. Submit Product Hunt listing (draft ready in Drive/Vista/Product Hunt)
  4. Tag @letterboxd and relevant film accounts in launch tweet
  | Updated: 2026-02-23

---

## 🟠 Builds — Demos for jtsomwaru.com Portfolio

- [ ] **AgentGuard — Responsible AI Governance Layer** — Build AI governance demo: confidence scoring, human-in-the-loop routing, decision audit log, explainability report. Flagship portfolio piece; directly supports Squarespace application.
  **Steps:**
  1. Tell Eve: "Build AgentGuard — spawn coding agent in ~/projects/agentguard"
  2. Eve scaffolds: n8n workflow + confidence scoring logic + SQLite audit log + weekly report
  3. Test with an existing JT Somwaru Consulting workflow (e.g. Aya dashboard)
  4. Get a public demo URL (Ngrok or Vercel deployment)
  5. Add to jtsomwaru.com /work page with live demo link
  6. Add to resume/LinkedIn: "Implemented human oversight checkpoints, decision logging, responsible deployment practices"
  **Estimated build time:** 2–3 days via Claude Code
  | Added: 2026-02-24

- [ ] **Claude Cowork Plugin Demo — Construction Niche** — Build live Cowork plugin for construction progress reporting. Most timely demo given today's Cowork announcement.
  **Steps:**
  1. Sign up for Claude Enterprise/Team plan (required for Cowork plugin creation)
  2. Tell Eve: "Build Cowork construction plugin — scaffold the plugin file and skills"
  3. Eve builds plugin definition (skills, slash commands, connectors)
  4. Upload to Cowork Customize menu → test the workflow
  5. Screenshot/record the demo for jtsomwaru.com
  6. Use as Spectrum outreach proof point
  **Estimated build time:** 1–2 days
  | Added: 2026-02-24

- [ ] **AI Research Demo — Public-Facing Niche Monitor** — Build a live demo: enter a company name → get a structured AI automation opportunity brief. Makes consulting service tangible.
  **Steps:**
  1. Tell Eve: "Build a public research demo UI — Next.js form → research agent → structured brief output"
  2. Eve builds lightweight Next.js app with the demo interface
  3. Deploy to Vercel (subdomain: demo.jtsomwaru.com or research.jt-consulting.ai)
  4. Embed on jtsomwaru.com /work page
  **Estimated build time:** 1 day
  | Added: 2026-02-24

- [ ] **Agentforce Demo Agent — jtsomwaru.com portfolio** — Build a live, displayable Agentforce demo agent that prospects and employers can see in action. Prerequisite for H.C. Oswald outreach and job applications. Complements AgentGuard (n8n) by showing Salesforce-native AI.
  **Steps:**
  1. Tell Eve: "Scope the Agentforce demo — what workflow to automate, what it shows, how to demo it live"
  2. Spawn agentforce-agent in ~/projects/agentforce-agent to build the Flow/Agent
  3. Deploy to jt-dev Salesforce sandbox — get a shareable screen recording or public link
  4. Add to jtsomwaru.com /work page with demo link or embedded recording
  5. Use as proof point in H.C. Oswald + Spectrum outreach
  **Estimated build time:** 2 days via coding agent
  | Added: 2026-02-27

- [ ] **Nash Satoshi — Rebuild on n8n + x-research + whale scoring** — Remove Gumloop dependency, run x-research skill directly for per-token X research, update scoring prompts to weight KOL/whale backing. Improves product quality + makes it fully self-hosted.
  **Steps:**
  1. Audit current Gumloop workflow: identify each node and its function
  2. Tell Eve: "Rebuild Nash Satoshi ranking pipeline in n8n — replicate Gumloop flow, swap X nodes for x-research skill calls"
  3. Spawn n8n-agent for the build: ~/projects/n8n-agent
  4. Update LLM scoring prompts in Nash Satoshi to add KOL/whale backing as weighted criterion
  5. Test full pipeline end-to-end on 5 tokens
  6. Cut over from Gumloop → n8n, decommission Gumloop
  **Estimated build time:** 2–3 days
  | Added: 2026-02-27

- [ ] **Vibe Marketing Agent — Full Build** — Automate all marketing for personal projects: SEO, X/Reddit content, TikTok/Reels (UGC avatars, slideshows). Covers Vista, Nash Satoshi, Glow Index, dynasty fantasy, and all future apps. One agent, multiplies across all projects.
  **Steps:**
  1. Tell Eve: "Spec the Vibe Marketing Agent — what it automates, what tools it needs (ElevenLabs, Opus Clip, n8n, X API), what the workflow looks like per app"
  2. Build modular: start with X + Reddit content (quick win) → add TikTok/Reels later
  3. Define a content brief template per app (tone, target audience, platform-specific format)
  4. Wire to n8n for scheduling + posting
  5. Test on Vista first (most time-sensitive — App Store pending)
  **Estimated build time:** 3–5 days (X/Reddit phase), 1–2 weeks (full TikTok/video phase)
  | Added: 2026-02-27

---

## 🟡 JT Somwaru Consulting — Business Development

- [ ] **Pitch distressed property platform to NYC brokers** — Aya said the acquisitions dashboard wasn't a fit because they source deals through broker relationships — which means brokers are the right ICP. Brokers need deal intelligence to surface properties for buyers like Aya. Product is already built (or nearly so). Pivot the pitch, not the product.
  **Steps:**
  1. Tell Eve: "Research NYC real estate brokers who specialize in distressed/value-add properties — find 10 targets with contact info"
  2. Eve drafts outreach tailored to brokers (different pain than operators: they need to bring deals, not manage them)
  3. Pitch: "I built a deal intelligence tool for a NYC property firm — they told me brokers are the better fit. Here's what it does."
  4. Goal: 2–3 broker conversations → refine product fit → potentially resell the platform or offer as SaaS
  | Added: 2026-02-27

- [ ] **Research enterprise platforms beyond Agentforce for consulting** — Agentforce is one vertical (Salesforce users). Research other platforms already embedded in businesses where JT can build Claude Code agents: ServiceNow, HubSpot, Monday.com, Zendesk, SAP, Oracle, Notion, Airtable. Goal: expand JT Somwaru Consulting's service menu beyond Salesforce shops.
  **Steps:**
  1. Tell Eve: "Research enterprise platforms with AI/automation extension points — which have APIs, agent frameworks, or plugin systems JT could build on"
  2. Evaluate each: market size, difficulty to build on, how many SMBs use it, overlap with current niches
  3. Pick top 2–3 → document in memory/research/enterprise-platforms.md
  4. Update consulting services page + outreach templates for the best new platform
  | Added: 2026-02-27

- [ ] **Research web app types similar to Aya construction tracker** — The construction dashboard is a proven format: real-time data → AI summaries → stakeholder views. Research what other industries need the same pattern. Find 5–10 other "personalized ops dashboard" opportunities for NYC SMBs.
  **Steps:**
  1. Tell Eve: "Research industries where the Aya construction tracker pattern applies — what data do they track, who are the stakeholders, what's the pain"
  2. Examples to explore: property management (leasing pipeline), insurance (claims tracker), wholesale (inventory + order status), skilled trades (job site progress)
  3. Output: ranked list of 5 app types with ICP, pain point, and rough build complexity
  4. Use output to inform next 3 prospect pitches + add to jtsomwaru.com /work pipeline
  | Added: 2026-02-27

- [ ] **Spectrum outreach — Claude Cowork pitch** — JT has inside workflow knowledge from 6 years there. Pitch governed Enterprise Cowork vs previous shadow IT concern.
  **Steps:**
  1. Identify 2–3 contacts still at Spectrum (LinkedIn — former colleagues in IT, Operations, or People teams)
  2. Send LinkedIn DM or email: "Hey [name] — I've been building AI automation systems since I left. Anthropic just launched something that directly addresses the data security concerns Spectrum had. Would love to show you for 20 min."
  3. In the demo: lead with governance (admin controls, no training, ZDR, audit logs)
  4. Show a concrete workflow you know they need (product catalog documentation, onboarding runbooks, vendor eval)
  5. Propose: JT Somwaru Consulting scopes the right workflows + builds the plugins + trains the team
  6. Target workflows to pitch: process docs, standup summaries, offer letters, internal KB — NOT subscriber data or CPNI
  | Added: 2026-02-24

- [ ] **JT Somwaru Consulting: Add Cowork Plugin Implementation as a Service** — New offering: assess workflows, build custom plugins, launch private marketplace, train teams.
  **Steps:**
  1. Define the service scope (Eve can draft): discovery session → plugin design → build → deploy → training
  2. Add to jtsomwaru.com /services page
  3. Build a 1-page PDF service brief (Eve can generate)
  4. Add to LinkedIn Services section
  5. Use Cowork construction demo as proof point in outreach
  | Added: 2026-02-24

- [ ] **JT Somwaru Consulting: first 50 leads researched** — Use research agent to find NYC prospects in target niches.
  **Steps:**
  1. `cd ~/projects/research-agent`
  2. Tell Eve or spawn coding agent: "Research 10 wholesale distribution prospects in NYC — run the research pipeline and output to clients/"
  3. Repeat for each niche: insurance, construction, property management, real estate
  4. Review briefs → shortlist top 10 most promising
  5. Use Apollo connector (now in Cowork) or LinkedIn to find contact emails
  6. Draft outreach email (Eve can write) — lead with specific automation opportunity for their niche
  | Updated: 2026-02-22

- [ ] **JT Somwaru Consulting: design pipeline agent handoff schema** — Standardize client brief JSON so all 4 agents share consistent handoff format.
  **Steps:**
  1. Read current research agent output: `~/projects/research-agent/clients/`
  2. Tell Eve: "Design a standard client brief schema — JSON with fields for company, niche, pain points, recommended automation, demo type, expected ROI"
  3. Update research-agent CLAUDE.md to output this schema
  4. Update n8n-agent CLAUDE.md to consume this schema as input
  5. Commit and push both repos
  | Added: 2026-02-22

- [ ] **JT Somwaru Consulting: build first demo deck (construction niche)** — Aya dashboard is the proof point; 10-slide deck for NYC contractor pitch.
  **Steps:**
  1. Tell Eve: "Build a 10-slide JT Somwaru Consulting construction pitch deck — Google Slides via Drive API, save to Eve — Drafts/JT Somwaru Consulting/Case Studies"
  2. Slides: Problem → JT Somwaru Consulting solution → Aya case study → ROI → how it works → next steps
  3. Review and edit in Google Slides
  4. Use as leave-behind in all construction niche outreach
  | Added: 2026-02-21

---

## 🟡 Job Market

- [x] ~~**Salesforce Lead Agentforce SE**~~ — **REMOVED** (2026-02-24). Too technical for JT's background. Not pursuing.

- [ ] **Fifth Dimension AI — AI Solutions Architect** — Score 16/25, salary est. $150K–$190K NYC hybrid.
  **Steps:**
  1. Retrieve full JD: https://careers.fifthdimensionai.com/jobs/6798350-ai-solutions-architect-new-york
  2. Verify role doesn't require hands-on coding as primary activity
  3. Tell Eve: "Create tailored resume + cover letter for Fifth Dimension AI SA role"
  4. Apply if coding requirement is not a blocker
  | Added: 2026-02-24

---

## 🟢 Low Priority / Ongoing

- [ ] **Nash Satoshi landing page** — Build minimal public landing page to link from jtsomwaru.com portfolio.
  **Steps:**
  1. Tell Eve: "Build Nash Satoshi landing page — Next.js, dark theme, explains 4-LLM methodology, deploy to Vercel"
  2. Connect to GitHub repo jsomwarux/Nash-Satoshi (make public or create landing page repo)
  3. Link from jtsomwaru.com /work page
  | Added: 2026-02-24

- [ ] **Dynasty fantasy football app** — AI correlates advanced stats with fantasy production.
  **Steps:**
  1. Research data providers: Sportradar, FantasyPros API, ESPN API
  2. Define player scoring model: which stats → fantasy score
  3. Tell Eve: "Scope the fantasy football app — data sources, stack, MVP feature set"
  | Added: 2026-02-21

- [ ] **Vibe Marketing Agent** — Moved to 🟠 Builds. See above.

- [ ] **Data visualization agent** — Spreadsheets → interactive dashboard web app.
  **Steps:**
  1. Tell Eve: "Create the data visualization agent workspace — CSV/Excel input → Next.js dashboard output"
  | Added: 2026-02-21

- [ ] **Calendar integration** — Add Google Calendar to morning brief.
  **Steps:**
  1. Confirm Google OAuth token covers Calendar API scope
  2. Tell Eve: "Add Google Calendar read to the morning brief — next 24h events summary"
  | Added: 2026-02-21

- [ ] **App Store monitoring** — Alert when Vista review status changes.
  **Steps:**
  1. Tell Eve: "Set up App Store Connect monitoring — poll review status daily, Telegram alert on change"
  | Added: 2026-02-21

- [ ] **x402 + agentic marketplace research** — Three angles: (1) x402 payment protocol integration into our agents, (2) publish agents on Moltlaunch (OpenClaw marketplace), (3) Virtuals Protocol ACP for tokenized agent deployment.
  **Steps:**
  1. Review x402.org — understand payment flow, what agents can monetize, how to wire it
  2. Research Moltlaunch (moltlaunch.com) — what's the submission process, what agent types perform well, revenue model
  3. Research Virtuals ACP — how agents get listed, what the token mechanics are ($NOX context: JT holds Virtuals ecosystem tokens)
  4. Tell Eve: "Research x402 + Moltlaunch + Virtuals ACP — what's the fastest path to monetizing one of our agents on each platform"
  5. Identify which existing agent (Eve, crypto-agent, research-agent) is best positioned to publish first
  6. Document in memory/research/agentic-marketplaces.md
  | Updated: 2026-02-27

- [ ] **Exploding Topics email scraper → automation/app idea generator** — Weekly automation: scrape JT's Exploding Topics newsletter emails → feed trending topics to LLM → generate automation/app ideas ranked by build feasibility + market timing. Feeds the App Factory pipeline.
  **Steps:**
  1. Tell Eve: "Build Exploding Topics scraper — Gmail API to pull newsletter emails, extract trending topics, feed to Claude, output ranked app/automation ideas to memory/drafts/exploding-topics-ideas.md"
  2. Schedule as isolated Sonnet cron: Sunday 8:30AM (after weekly synthesis)
  3. Output format: topic + search volume trend + 1-2 build ideas + estimated effort
  | Added: 2026-02-27

- [ ] **YOLO prompt nightly cron** — Inspired by @chrisalbon: every night, throw one wild project idea at Claude and let it run. Wake up to a prototype or research report. Forces creative exploration without consuming daytime focus.
  **Steps:**
  1. Tell Eve: "Set up YOLO cron — 11PM nightly, main session prompt asking JT for tonight's wild idea"
  2. When JT replies with an idea, spawn isolated Sonnet session to run with it overnight (timeout: 30 min)
  3. Results delivered in morning brief
  4. Keep a running log at memory/yolo-experiments.md
  | Added: 2026-02-27

- [ ] **App building factory** — Meta-system: researches niches, scrapes discussion boards, identifies pain points, generates app ideas, JT approves/rejects, builds or saves. Build incrementally — start with the idea generation layer, add the build trigger later.
  **Steps:**
  1. Phase 1 (research + ideas): Tell Eve: "Build app idea generator — scrape Reddit pain points in 3 niches, run through Claude, output ranked ideas with market size + competition + build effort"
  2. Phase 2 (approval gate): Add a Mission Control UI where JT approves/rejects ideas
  3. Phase 3 (build trigger): Approved idea → spawn coding agent to scaffold the app
  4. Reference docs: memory/research/nash-satoshi-niche-expansion.md (scoring methodology)
  | Added: 2026-02-27

- [ ] **Whop opportunity scanner** — Scan Whop marketplace for app/automation/community ideas that overlap with JT's projects. Scope as a lightweight research cron, not a full agent.
  **Steps:**
  1. Tell Eve: "Run Whop market scan — fetch top products in AI tools, automation, and ranking app categories, look for gaps or adjacent ideas"
  2. Output to memory/research/whop-opportunities.md
  3. Run once manually first, then decide if weekly cron is worth it
  | Added: 2026-02-27

- [ ] **Ensemble site building agent** — Agent that builds the frontend for ensemble ranking apps (Nash Satoshi pattern) automatically. Scope unclear — revisit when Nash Satoshi rebuild (n8n) is complete.
  **Steps:**
  1. After Nash Satoshi rebuild is done: tell Eve "Scope the ensemble site agent — what does it generate, what's the input, how reusable is it across apps"
  2. Define the template: dark theme, leaderboard UI, methodology page, token detail pages
  3. Build as a coding-agent skill that takes a config JSON → outputs a deployable Next.js app
  | Added: 2026-02-27

---

## ✅ Completed

- [x] **Push research-agent to GitHub** — live at `jsomwarux/research-agent` | Done: 2026-02-22
- [x] **Set up Google Sheet → crypto intelligence pipeline** — Dexscreener price fetching live, 10/10 coins, 3 crons active, GitHub pushed | Done: 2026-02-22
- [x] **Set git global identity** — confirmed set: JT Somwaru / jsomwarux@yahoo.com ✅ | Done: 2026-02-23
- [x] **n8n: set API credentials** — all 4 LLM creds confirmed live; Glow Index workflow active | Done: 2026-02-23
- [x] **n8n agent imported** — cloned to `~/projects/n8n-agent/` | Done: 2026-02-22
- [x] **Agentforce agent imported** — cloned to `~/projects/agentforce-agent/`, sf CLI installed, `jt-dev` org authenticated | Done: 2026-02-22
- [x] **Research agent built** — `~/projects/research-agent/` with 5 niche files | Done: 2026-02-22
- [x] **JT Somwaru Consulting competitive landscape research** — full report at `memory/research/jt-consulting-competitive-landscape-2026-02-22.md` | Done: 2026-02-22
- [x] **Launch Mission Control dashboard** — LaunchAgents live, always-on at http://localhost:3000 | Done: 2026-02-21
- [x] **Nash Satoshi: niche expansion research** — scored all 5; baby products #1, skincare #2 | Done: 2026-02-21
- [x] **Crypto agent allocation history system** — saves daily JSON, tomorrow's brief compares vs today | Done: 2026-02-24
- [x] **Morning brief cron fixed** — isolated → main session, prevents context overflow | Done: 2026-02-24
- [x] **Job market agent profile updated** — pipeline architecture, ops stack, salary carve-out, portfolio pieces added | Done: 2026-02-24
- [x] **Squarespace application docs created** — tailored resume + cover letter as Google Docs | Done: 2026-02-24
- [x] **Seed knowledge base** — 53 items indexed | Done: 2026-02-22
- [x] **Eve workspace setup** — SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, TOOLS.md, HEARTBEAT.md | Done: 2026-02-21
- [x] **Health tracking system** — SQLite + NLP parser + weekly report + 2 crons | Done: 2026-02-21
- [x] **Automated backup system** — LaunchAgent daily 2 AM, 7-day retention | Done: 2026-02-21
- [x] **Session cleanup automation** — LaunchAgent daily 3 AM | Done: 2026-02-21
- [x] **Knowledge base system** — SQLite + vector embeddings at knowledge/kb.sqlite | Done: 2026-02-21
- [x] **Mission Control dashboard** — Next.js + Convex, 8 sections, LaunchAgents | Done: 2026-02-21

---

_Last updated: 2026-02-27 18:30 EST_
