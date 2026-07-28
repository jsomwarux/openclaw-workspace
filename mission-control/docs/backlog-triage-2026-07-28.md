# Backlog Triage Proposal — 2026-07-28 (apply nothing)

Branch: `mc-backlog-triage`. **Nothing applied — awaiting JT approval.**

- Open tasks: **250** · idle >30d (in scope): **205** · fresh ≤30d (not in scope): **45**
- Mechanical **KEEP: 0** · **CONVERT: 30** · **ARCHIVE: 175**
- Plus **4 KEEP-by-exception** carve-outs pulled out of ARCHIVE (below) — archiving them is risky even though they fail the strict bar.

**Why KEEP is 0:** the strict bar is client-scoped / cash-bearing / real external deadline. The Phase 2a `clientId` backfill touched all 10 client-scoped tasks today, so they're fresh (<30d) and out of the idle set. Nothing idle 30+ days is client, cash, or dated. During a cash mandate that is the correct result — a 70-day-old idea is noise, not a task.

---

## KEEP — by exception (4) — do NOT bulk-archive

These fail the strict cash/client/deadline bar but should not be blindly archived. Recommend individual review.

| taskId | age | title | why keep |
|---|---|---|---|
| j5729aecmf0msjcw3drys6pgy187e9hw | 62d | [🔴] SECURITY: OpenClaw/ClawHub RCE (CVE-2026-25253) | Security fix — verify already patched before archiving |
| j575mzd8dxw60zejq747ryyrw98921zg | 36d | Complete weekly unemployment certification | Income continuity obligation (recurring deadline) |
| j573d6vqs20z29fstqn8nzf59h899pg0 | 33d | [🟠] OpenClaw v2026.6.10 stable runtime fixes | Newest stable — keep ONE upgrade task, archive the older betas |
| j576zn0e3pag6dpmxfx99t8k7986mp6x | 75d | Mission Control hygiene: retire stale backlog + fix task quality gates | This IS the current triage — execute then close |

---

## CONVERT (30) — preserve as pideas / memory note, then remove as open tasks

All are product/offer concepts worth keeping, but not open tasks competing with cash. Move to the `pideas` table (or a `memory/ideas` note) and close.

| taskId | age | title |
|---|---|---|
| j5794aa0933p7xasdjea8jkn5d86ntn4 | 75d | Build idea: AgentOps Console — production AI agent operations |
| j578tzkc28x24717tnxcjqxmb586ggvv | 75d | Build idea: AI Pilot Governance Kit |
| j5797wm1hz8tbh5nwmdmecz0f5865t3j | 75d | Build: Exception Dashboard demo spec |
| j571aqwgaxeh9xcezwfhjej0e185sys9 | 75d | Build idea: BedrockBridge — Enterprise RAG Agent on AWS |
| j57cssa420edqmmy6wy555ryyd85rs0p | 75d | Build idea: AI Transformation Readiness Advisor |
| j57c8nn6gv1qg3w7whz8s7sdbd85ndf1 | 75d | [Score 7.8] Sports GM receipts-backed content engine |
| j571f0jsybgn39pqcbq0vr633h85me22 | 75d | [Score 7.7] Sports GM market snapshot engine |
| j5735cqmyvcy3y8gfvzdrrpr1x85nev0 | 75d | [Score 8.0] Sports GM paid dynasty roster audit offer |
| j578jtxvdtwt7t9vx18mg9ebg185a4k0 | 75d | Build idea: AdoptAI — Client Adoption Playbook Generator |
| j579agtfns9qjsbqgjrgdmvfp185abqr | 75d | Build idea: AgentBridge M365 — Cross-Stack AI Agent Demo |
| j571tz5wdhj2w5afd0tp9keh8s8587wh | 75d | Build idea: Agent Evaluation Frameworks / Observability: EvalKit |
| j57b9r66cem0t7yjxv1d9ggm3n858qdx | 75d | Build idea: Outcome-Based AI Implementation Design: OutcomeFirst |
| j570bykg71mgxdq534sqvqbxgd859rpt | 75d | Build idea: Conversation Design: ConversationFirst |
| j57dcfjyxdar8hjyb8d5vx84px859qpd | 75d | Build idea: LangChain / LangGraph: Pipeline Translator |
| j57cj6tn7re8htqs8rpjkng4k585945w | 75d | Build idea: Responsible AI / AI Governance: AgentGuard |
| j5701qrb018z4wbmb8af7srtxh81zbhq | 75d | Ensemble site building agent |
| j578zp34g3e45dvv32a6dhay9981yt5d | 75d | Whop opportunity scanner |
| j57bmbq13r7932977cw9dsb7v181zcb2 | 75d | App building factory |
| j572t9n7138c8kr4vp79096mwh86pphz | 74d | Build idea: AIPortfolioOps Console |
| j572yvh5n6x7t87023wte6rcgx86s6s5 | 73d | Build idea: VerticalOps Blueprint |
| j57eswqccsv94wm06eehmgxan986thx7 | 72d | Build idea: AgentOps Console GitHub control-plane extension |
| j57cpjc52nksch3901endjcnr986xj3h | 71d | Build idea: AutoPilotOps — autonomous agent pipeline governance |
| j57bvvdmxah0q1dpcdb7dt8yyx86zyx5 | 70d | Build idea: AssessmentProof Pack |
| j573ws48gxqs61q32f0k9m1kvh8708nt | 69d | Build idea: ProcurePilot AI COE Blueprint |
| j57c4zzk8e835herjf41chbamd874ek2 | 67d | Build idea: RegulatedAI Enablement Console |
| j572jt7kg0fpsc6pg2psckxrq9876esv | 66d | Build idea: MarTechAgent Accelerator |
| j579c8t7sp6489d0nqrmmeg3zd87a9mn | 64d | Build idea: EnablementOps Blueprint |
| j574tvr1mjbfs210t6kc89qf3187da71 | 63d | Build idea: IdentityGate for Agents |
| j570pt93sc8y598e7hzdvhh3vh81zcgz | 61d | Exploding Topics email scraper → weekly idea generator |
| j5771w6c33m7k6etdqff372pnn87n71c | 59d | Build idea: DealDesk AI Control Plane |

---

## ARCHIVE (175) — by theme

### Runtime infra & upgrades (36) — bulk-archivable; version tasks self-supersede
Carve out for KEEP: `j5729aec…` (SECURITY CVE) and `j573d6vqs…` (newest stable). Every older `OpenClaw vX beta` is superseded by a newer one — safe to archive as a block. (List: all 36 minus the 2 carve-outs.)
j5717qakd…(75d) Harden weekly systems review · j57209enn…(75d) reusable n8n insurance template · j5766rrkt…(75d) n8n-mcp · j57d1s79r…(75d) Niche Review PM n8n vertical · j579spqyf…(74d) OpenClaw v2026.5.12-beta.8 · j57071t61…(74d) OpenClaw v2026.5.10-beta.5 · j57091wmh…(74d) OpenRouter cheap models smoke-test · j574jqfeg…(74d) n8n Microsoft Agent 365 · j574qvzb6…(66d) OpenClaw v2026.5.20 · j5713kbf6…(63d) Harden cost/cron/security A+ · j5726a7mt…(62d) ClawSec suite · j5721av39…(62d) n8n Microsoft Agent Node · j57dmje1s…(58d) n8n MS Agent 365 Trigger · j570wd8er…(55d) OpenRouter MiniMax M3 · j5733dy1c…(55d) OpenClaw v2026.6.1-beta.2 · j579ekmed…(55d) Cron health Overnight Autonomy · j570zvw91…(54d) OpenClaw v2026.6.1-beta.3 · j578rx51f…(54d) Cron health Viral Post Swipe · j5788knrs…(53d) OpenClaw 2026.6.1 stable · j5798x9s7…(49d) OpenRouter workspace governance · j575ndp1j…(49d) OpenClaw v2026.6.5-beta.2 · j576ggkz4…(49d) Bootstrap budgets trim · j57cg7ht3…(46d) delete stale disabled cron jobs · j572j139c…(46d) Recompute cron delivery rate · j5761qtnn…(46d) OpenClaw runtime upgrade smoke · j5718pb51…(46d) Weekly systems review June 7 drift · j57bx7032…(45d) OpenClaw 2026.6.6 · j572rph35…(42d) OpenClaw v2026.6.8 beta · j57bgkk2z…(41d) OpenClaw v2026.6.8-beta.2 · j570jax17…(39d) OpenClaw 2026.6.8 · j57127s67…(38d) OpenRouter Fusion Router · j573ythjt…(35d) OpenClaw v2026.6.10-beta.2 · j575kgmgb…(34d) n8n 2.28 update · j5779c7et…(31d) OpenRouter Unified Image API

### Cold outreach & prospecting (28) — benched/stale prospect touches
j57ah0tt4…(75d) Pitch distressed property to NYC brokers · j57a98vzt…(74d) Email Pivot: Premier HVAC · j5768phba…(74d) Email Pivot: Globe Electric · j57d4sex7…(74d) Email Pivot: Atlas NYC PM · j57d7gqqd…(74d) Email Pivot: First Class Mgmt · j5735t6yt…(74d) Email Pivot: ProRealty · j5787gm1p…(74d) Email Pivot: Lawley Insurance · j57bcswg4…(74d) Email Pivot: R.E.M. Residential · j577zg7nc…(74d) Email Pivot: Conner Strong · j5766dvmg…(67d) Email Pivot: Forest Building Supply · j577pprme…(67d) Email Pivot: Park Avenue R&B · j5765t9v2…(67d) Email Pivot: AFGO Mechanical · j57fmdvtt…(64d) Send M2: Bell Electrical · j574krer4…(64d) Send M2: Edmer Supply · j57bmkd18…(64d) Send M2: Benfield Electric · j5721t67m…(54d) NYCB contributor-list pilot · j57fsdd6z…(55d) Wholesale limited-test · j57d0mx71…(55d) Verify channel: A-List Janitorial · j576vybg4…(55d) Verify channel: Atlantic Global Risk · j57fbg7w5…(55d) Verify channel: NY Plumbing Supply · j570cc9mm…(55d) Verify buyer: Human Agency · j575sdype…(63d) Land first wholesale pilot · j57228krq…(46d) ARC Excess T3 DM · j57537a44…(46d) York International T3 DM · j57d1jb89…(53d) Fernstone T3 DM · j57es53z5…(53d) Avallon AI T3 DM · j57a609g2…(53d) L. Richards T3 DM · j57aqbxn3…(33d) Email Pivot: NY Plumbing Supply

### Content & social drafts (23)
j5734shsw…(31d) PM Resolution Ledger LinkedIn · j57btafkc…(32d) AI Enablement tool-stack LinkedIn · j570stgta…(35d) Post Nash Satoshi week 06-22 · j576729qs…(37d) PM Control Record LinkedIn · j579xqefg…(33d) AI Run Control LinkedIn · j579hkgeq…(41d) Night Autonomy rent report · j5726465…(43d) Night Autonomy Exception Control · j57bkqafp…(44d) Night Autonomy PM rent control · j57073kjj…(46d) Night Autonomy PM readiness · j577q5bbm…(49d) Weekly X queue 06-08 · j57fcx2gv…(49d) Weekly LinkedIn queue 06-08 · j57e9fq6b…(57d) corpus thresholds · j576qpej2…(57d) niche creator corpus · j577hcbmr…(57d) Post PM AI Ops proof angle · j575se3bx…(63d) Telegram posted replies handler · j57faf3mz…(75d) Content gap resource roundup · j574n9em4…(75d) Claude Code postmortem take · j573sxaf4…(57d) Backfill Viral Swipe · j578vw9tq…(75d) format DNA slideshows · j579snc2c…(75d) X Trend Radar to idea bank · j573cpyjc…(75d) Assessment-first post · j570b7976…(75d) Post: YC rebuilding consulting · j57bdczpj…(75d) Post: 80% enterprises struggling

### Job applications & bridges (20)
j570vgh7j…(41d) Apply: AI Engagement Mgr · j57cgd5t2…(42d) Apply: Cassidy · j57a2qz84…(59d) Dual-track H.I.G. · j5726zhzf…(61d) AI SEO n8n roundup outreach · j57bkn213…(62d) Lead: WEF AI Enablement · j576zvjn8…(66d) Apply: YouTube/Google SA · j57d0fky9…(67d) Lead: Datavant · j57ayd3av…(68d) Lead: Anaplan · j5767ehcd…(57d) Dual-track Coupa · j5742tn0b…(69d) Dual-track Anaplan · j5735k32y…(68d) Review+Submit: Gusto · j57a9x69y…(73d) Lead: Adaptive Innovations · j57e73ts5…(73d) Review buyer: Whitmore · j579rsgzs…(61d) Review+Send: Rampart Insurance · j574vgd9b…(74d) Verify job signal: Cribl · j5732g1rf…(75d) Dual-track Embark · j5773ks2c…(75d) Dual-track Gusto · j576h6ccf…(75d) Apply: CAI · j57883c4g…(75d) Apply: Mercury · j573rbrax…(75d) Apply: Ramp

### Uncategorized (23) — one-off items, review the two carve-outs
Carve out for KEEP: `j575mzd8…` (unemployment cert) and `j576zn0e…` (this triage). Rest archive.
j57bh4ys3…(33d) Entrata webinar proof language · j578snvhp…(38d) PM COI expansion buyer routes · j57989nsf…(41d) Review MC 7-Lane Slice 1.7 · j571zf9nf…(45d) Spec MC pipeline escalation timers · j57fzrq4y…(54d) Archive old content-signals · j573yp1mj…(55d) Review JT Claude Toolkit · j570c2p0h…(57d) LinkedIn sentence-rhythm scoring · j57evb00a…(59d) Vibe Prospecting test · j57d3tcfa…(61d) AI SEO directory submissions · j57bmj22z…(70d) AI Front Desk validation list · j57e2sg06…(74d) Anthropic SMB plugin · j579wp38j…(63d) Health Telegram inbound handler · j570vv3rf…(78d) Agent-Ready Revenue Layer offer · j570n03kt…(78d) x402 commerce thread · j573az8k7…(75d) Finish Client OS rollout · j57a8828v…(76d) Consulting acquisition reset · j579m6fma…(56d) Collect LinkedIn swipe examples · j57b6x1jp…(75d) Send G-Net prototype to Vincent · j570de55g…(75d) AI Video Agent plan · j57190jvn…(75d) Rename opticfy-pipeline folder · j57b9hyd5…(75d) Build Pipeline Translator LangGraph

### Skills-gap & internal tooling (12)
j573ve784…(56d) MC task gate/Drive shortcuts · j57bkzhsv…(56d) governance proof-packager mode · j573a2g02…(56d) LLM/RAG eval checklist · j570393vz…(56d) architecture proof-map · j57fbr6me…(73d) Golden Test Case Agent spec · j571c65sv…(73d) Governance + Risk Agent v1 · j573xq87q…(73d) Implementation Pattern Library v1 · j57e1pqxm…(73d) Workflow Discovery Agent v1 · j575s36mc…(74d) LLM eval/monitoring skill · j57atmpds…(74d) prompt-library cover letters · j57921fag…(74d) qmd into Opticfy · j579v0yhf…(75d) Calendar integration morning brief

### Tools/MCP & integrations to evaluate (12)
j57evj4w2…(56d) HubSpot CRM playbook · j5755ehws…(62d) Voicebox MCP on Mac Mini · j5714j7a7…(82d) Pay.sh sandbox x402 · j571zjmt8…(75d) Anthropic Financial Agent Templates · j574dd6j2…(75d) Meta Ads MCP · j571y8kcz…(74d) ATTOM MCP · j57bm9pcj…(74d) HouseCanary MCP · j57dn24ys…(75d) Stripe Link for agents · j57bqwm5r…(74d) HubSpot AI playbook · j5784wxtq…(74d) Salesforce Headless 360 · j57309p6d…(75d) HubSpot MCP Demo screencast · j576a16yc…(75d) Decide: WealthAgent path

### Positioning & strategy angles (7)
j57eh31gy…(34d) Turn Run Control into sales asset · j57avjgqj…(57d) Package Property Ops Control Plane Proof · j579h2x49…(75d) AI Adoption OS / Champions · j571hkm81…(75d) AI Adoption Ops as consulting wedge · j57393dd0…(75d) Reframe around specialist proof · j577dhmeg…(75d) Specialist vs Generalist · j5702hz1s…(75d) Audit Outreach + Content Execution

### Side projects & misc (14)
j570m3jba…(62d) Dynasty Simulator prelaunch plan · j57862tw4…(73d) Rewrite Agent Ops Audit buyer language · j57d6k7mf…(73d) Agent Ops Audit content seed · j571dm0sf…(73d) joke-vertical AI filter · j57f1aj7t…(74d) Autoresearch cost-cap wrapper · j5789q390…(88d) Health Constraint Layer audit · j575akc03…(75d) backlink citation map · j57e7z1kz…(75d) Google Business Profile · j574q20yn…(75d) NYC networking event · j57c49hyp…(75d) Build T2 Construction Job Cost Monitor · j57dcny6a…(75d) Data Anomaly Audit service · j570ngtjw…(75d) YOLO nightly creative cron · j57d6jp1z…(75d) Research web app similar to Aya · j576zwrvs…(75d) Build construction pitch deck

---

## How to approve
- **"Archive all"** → I archive the 175 (I'll auto-hold the 4 carve-outs unless you say otherwise).
- **"Archive all + carve-outs"** → include the 4.
- **By theme** → name the themes to archive (e.g. "runtime, outreach, content, job-apps").
- **CONVERT** → say whether to move the 30 into `pideas` or a `memory/ideas` note before closing.
