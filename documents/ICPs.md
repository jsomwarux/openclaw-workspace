# JT Somwaru Consulting — Ideal Customer Profiles (ICPs)
> Load this file in any agent doing research, outreach, content, or proposal work.
> These are dossiers — not summaries. Use the specifics, not the headlines.

---

## ICP 1 — NYC Wholesale Distributor

**Who they are:**
Family-owned or founder-led wholesale distribution company, typically $3M–$20M revenue, 5–30 employees. NYC metro (Bronx, Queens, Brooklyn, Lower Manhattan are hotspots). Usually in a physical industry: plumbing/HVAC parts, food/beverage, garment/textile, electrical supplies, hardware/industrial. In business 10–40+ years. The owner is often also the operations manager.

**Their tech stack:**
- ERP/inventory: QuickBooks (most common), occasionally NetSuite or Sage
- Order management: spreadsheets or legacy desktop software they've used for years
- Communication: email, phone, WhatsApp group chats with staff
- Website: static or barely functional — not a priority
- NO Salesforce (this disqualifies Agentforce — use n8n instead)

**Their actual pain (what they say vs. what they mean):**
- "We're too busy" → they have no systems, everything runs through the owner's head
- "We need to hire someone" → they need automation, not another employee
- "We lose orders" → no structured order tracking, things fall through in WhatsApp
- "Customers complain they can't reach us" → no after-hours support, no self-service
- "We can't find the price we quoted that customer last year" → no CRM, everything in email

**How they make buying decisions:**
- Owner decides, usually alone. No procurement process.
- Trust is the #1 buying signal — they don't buy from strangers
- They want to see the thing built, not a slide deck
- ROI framing works: "this saves you X hours/week" or "you'll stop losing orders like this"
- Price sensitivity: real but not a dealbreaker if they believe in the value. $2,500–$5,000 is a real discussion; $10,000 is a stretch without a referral
- Timeline: slow starters, then fast. They'll ignore you for 2 weeks then suddenly say "can you start Monday?"

**Hook signals to look for:**
- Yelp/Google reviews mentioning "hard to reach" or "need to call multiple times"
- Job posts asking for "someone to manage orders" or "coordinate between warehouse and office"
- Website with no product search or contact form — catalog knowledge is locked offline
- The company is known but has no online presence — they're established but analog
- LinkedIn posts from owner showing pride in the business history

**Demo that closes them:**
n8n workflow that automates their single biggest manual process. For parts distributors: a parts lookup agent (like the H.C. Oswald Copilot). For food/beverage: an inventory reorder trigger. Show it connected to QuickBooks or their existing system. Make it feel like their world, not a generic demo.

**Real example:** H.C. Oswald Supply Co. — 103-year-old boiler parts distributor in the Bronx. Catalog knowledge locked in filing cards. Spanish-speaking contractor customer base with no after-hours support. Built a Shopify catalog search agent via Intercom. Pitch hook: "Your catalog is already digital. It just can't answer questions yet."

---

## ICP 2 — NYC Construction & Skilled Trades ($3M–$20M)

**July 2026 outbound status:** Secondary lane only. Do not scale trades outreach until the Job Status Dashboard proof asset exists: blurred Aya-style dashboard snapshot plus 60-second Loom showing floor-by-floor / room-by-room visibility from existing tracking sheets. Sequence is email plus phone, not LinkedIn-first.

**Who they are:**
General contractors, specialty subcontractors (plumbing, electrical, HVAC, roofing), or construction management firms. Typically 5–50 employees, $3M–$20M in annual revenue. NYC-based or NYC metro. Often hold state licensing (electrical, plumbing, general contractor). Family business or founder-led. May operate on ServiceTitan, Jobber, or Buildertrend — or nothing at all.

**Their tech stack:**
- Field management: ServiceTitan (mid-size), Jobber (small), or spreadsheets
- Estimating: Excel or QuickBooks
- Project tracking: WhatsApp group with foreman, phone calls, paper
- NO Salesforce — not a Salesforce shop

**Their actual pain:**
- "We can't track what's happening on site without calling the foreman" → no field reporting system
- "Change orders always become arguments" → no documentation trail
- "We invoiced late and the client disputed it" → no automated milestone tracking
- "We bid that job but lost track of why we won or lost" → no post-bid analysis
- "We have guys waiting on site because materials weren't ordered" → procurement disconnected from schedule

**How they make buying decisions:**
- Owner + sometimes a project manager. Very relationship-driven.
- They buy from people who understand construction, not tech consultants
- Want to see something that maps directly to a problem they had last week
- Referrals are gold — one Aya referral is worth 10 cold emails
- Budget: $2,500–$7,500 is realistic for a first project. Bigger once trust is established.

**Hook signals to look for:**
- Recent projects featured on their website — good conversation starter
- Google reviews mentioning project management issues or communication problems
- Job posts for "project coordinator" or "field supervisor" — they're trying to solve coordination problems with headcount
- LinkedIn posts from owner about job wins, company milestones, or team shoutouts

**Demo that closes them:**
Construction progress tracker (like Aya dashboard) or job cost tracking automation. Live demo showing daily site updates flowing into a client-visible dashboard without the foreman needing to file a report. Or: automated change order documentation that creates a paper trail without adding work.

**Real example:** Aya — NYC real estate/construction firm. $1,500 construction progress tracker (first project). Led to $1,000 StreetEasy scraper, then co-living dashboard discussion ($2,500 pending), then acquisitions dashboard (stalled). The anchor client pattern — one good build creates ongoing work.

---

## ICP 3 — NYC Property Management (Small–Mid)

**July 2026 outbound priority:** Primary cold-outbound lane for the next 30 days. Target NYC metro firms around 200-3,000 units, especially rent-stabilized exposure or AppFolio/Yardi/Buildium signals. First proof asset is COI Compliance Autopilot: vendor cert expiration tracking, 30/14/7-day alerts, drafted chase emails, and logged review state. Send-ready requires a named buyer plus verified email OR accepted LinkedIn connection.

**Who they are:**
Independent property managers or small PM firms handling 50–500 units across NYC residential/commercial. May manage for third-party owners (common in NYC) or own the properties themselves. Often using AppFolio, Buildium, or Rent Manager — NOT Salesforce.

**Their tech stack:**
- PM software: AppFolio (most common mid-size), Buildium (small), Rent Manager, or Yardi (larger)
- Maintenance coordination: email + phone, sometimes ServiceTitan
- Tenant communication: email, sometimes a tenant portal built into AppFolio
- NO Salesforce unless they're a large enterprise

**Their actual pain:**
- "We're drowning in maintenance requests" → no triage or routing automation
- "Vendors keep no-showing and we find out from the tenant" → no automated follow-up chain
- "Lease renewals sneak up on us" → no proactive expiration tracking
- "Compliance deadlines are everywhere and we track them in a spreadsheet" → no automated compliance calendar
- "We spend all day answering tenant questions about when the repair is coming" → no tenant-facing status updates

**How they make buying decisions:**
- Owner/principal or operations director. More process-oriented than construction owners.
- They appreciate automation but need proof it works with their existing tools (AppFolio API, etc.)
- More likely to respond to operational efficiency framing than ROI dollar amounts
- Budget: $3,000–$8,000 for a focused automation. Recurring/maintenance arrangement possible.

**Hook signals:**
- Reviews on Google/Yelp/Apartmentlist from tenants complaining about slow maintenance response
- Job posts for "maintenance coordinator" or "tenant communication specialist"
- LinkedIn posts about portfolio growth (new buildings = more operational pressure)

**Demo that closes them:**
Multi-agent maintenance triage system: tenant submits request → AI classifies urgency + type → routes to right vendor → sends automated status updates to tenant → logs to AppFolio. Or: lease renewal alert system that triggers outreach 90/60/30 days before expiration.

**Agentforce eligibility:** Only if they're using Salesforce (rare for this segment — mostly AppFolio shops). Default to n8n.

---

## ICP 4 — Insurance Operations (Mid-Size, Salesforce Shop)

**Who they are:**
Mid-size insurance agencies or MGAs (Managing General Agents) with 20–200 employees. Using Salesforce as CRM/operations platform. NYC, remote-serviceable. Often struggling with claims intake, renewal workflows, or agent productivity.

**Their tech stack:**
- Salesforce (confirmed — this is the qualifying criteria for Agentforce)
- Claims management: varies (Guidewire, Duck Creek, or homegrown Salesforce setup)
- Document management: SharePoint or Google Drive

**Their actual pain:**
- Claims intake requires manual data entry across systems
- Renewal reminders are done manually or poorly automated
- Agents waste time on status questions that a bot could answer
- Compliance documentation is inconsistent

**Why Agentforce fits:**
As of March 2026, Agentforce is bundled into Salesforce Suites for SMBs — meaning most targets in this ICP already have Agentforce access and don't know it. The pitch is NOT "should you use Agentforce" or "here's a new tool." The pitch is: "You're already paying for this. Let me activate it and configure it for your specific workflow." This is a fundamentally lower-friction sale — no new budget line, no new vendor approval. The client just needs someone to turn it on correctly.

**Distribution path (April 2026 — AgentExchange):** AgentExchange (launched TDX 2026, April 15) is now the unified catalog for Agentforce solutions. JT can publish completed engagements there — giving consulting work a referral pipeline and a credential that survives any single client relationship. Use AgentExchange as a trust anchor in cold outreach: "Solutions are published to Salesforce's official AgentExchange catalog — this isn't a side project, it's a production deployment."

**Technical credibility signal (April 2026 — Headless 360):** All Salesforce objects now exposed as native MCP tools per Headless 360 architecture. Consulting engagements no longer need custom API integration scoping — the surface is standardized. Scope conversations are shorter, and prospects can verify the architecture themselves on Salesforce's developer documentation.

**Pricing angle (post-March 2026):** Salesforce's CFO has flagged that Agentforce token pricing will commoditize. Never compete on per-token cost. Position value on outcomes and time saved: "You don't pay me per API call. You pay me once for a system that handles X without a human rep touching it."

**Budget:** $6,500–$15,000 for an Agentforce deployment. Larger than n8n engagements because of Salesforce complexity and enterprise context.

**Demo:** Insurance Service Agent (already built) — claims intake, routing, FAQ handling. Directly applicable.

**New hook signal (March 2026):** Agentforce Contact Center launched at Enterprise Connect 2026 as a CRM-native execution layer for contact center automation. Directly applicable to insurance and PM prospects running inbound claims/maintenance request queues. Use this as a conversation anchor: "Salesforce just launched a contact center agent designed for exactly this — and if you're on Salesforce, you probably already have access to it."

**Urgency signal (March 2026 — active now):** WTW survey (Insurance Journal, March 25 2026) shows straight-through processing (STP) in claims workflow automation set to nearly triple: 36% of insurers plan to introduce it, up from 14% currently. This is a concrete near-term demand spike. Translation: insurance ops leaders are actively building the budget case for claims automation NOW. Timing hook for any insurance outreach: the industry is moving fast on this, and firms that activate Agentforce ahead of competitors will have a workflow advantage before it commoditizes. Source: insurancejournal.com/news/national/2026/03/25/863287.htm

---

---

## ICP 5 — Financial Services / RIAs (Emerging Agentforce Target — added 2026-04-01)

**Status: Emerging (21/30 niche fitness score). Not yet actively outreaching — build one demo first.**

**Who they are:**
Independent Registered Investment Advisors (RIAs), boutique wealth managers, and independent broker-dealers. Typically 5–50 advisors, $50M–$500M AUM. NYC metro. Using Salesforce Financial Services Cloud as CRM — this is the qualifying criteria. Often on Salesforce because compliance and client management require it.

**Their tech stack:**
- Salesforce Financial Services Cloud (qualifying criteria — if not on SFSC, disqualify)
- Document management: SharePoint, DocuSign
- Portfolio management: Orion, Schwab, Fidelity integrations
- Compliance: branch-level manual reviews, periodic audits

**Their actual pain:**
- New client onboarding is 12-step manual process — advisors doing admin instead of advising
- Compliance documentation is inconsistent across advisors — error risk
- Client review scheduling is handled by phone/email, no automated cadence
- Advisors can't answer "what happened with this client's last 3 touches" without digging through notes
- Quarterly review preparation takes 2-3 hours per client manually

**How they make buying decisions:**
- Managing partner or COO. More process-oriented than construction/wholesale buyers.
- Compliance is the #1 concern — any automation must have audit trail and be explainable
- Salesforce-native solutions are easier to approve (already in the stack, no new vendor)
- Deal sizes $8-15K — they will pay if the ROI is clear
- Referrals from other RIAs or Salesforce partners carry significant weight

**Hook signals:**
- LinkedIn posts from advisors complaining about admin overhead or compliance burden
- Job posts for "Client Service Associate" or "Operations Coordinator" — they're trying to solve with headcount
- Firm is growing (new advisors hired) — scaling without adding ops staff is the pressure point

**Demo that closes them:**
Agentforce agent on Financial Services Cloud: new client onboarding workflow (intake → KYC document checklist → account setup tasks → onboarding communication to client). Or: client review prep agent that aggregates portfolio data and drafts meeting agenda automatically. **This demo does not exist yet — build it before outreaching.**

**Why Agentforce fits:**
Salesforce Financial Services Cloud penetration in mid-size RIAs is 40%+. Agentforce is already in the stack. Same pitch as insurance: "You're already paying for this. Let me activate it for your onboarding workflow." Salesforce is actively pushing Financial Services Cloud + Agentforce to this segment in 2026.

**Budget:** $8,000–$15,000 for an Agentforce deployment. Larger than n8n engagements.

---

## Notes for All ICPs
- JT is NOT a developer — do not pitch coding/custom dev work. Pitch implementation.
- Proof points: Aya dashboard ($1,500), StreetEasy scraper ($1,000), Agentforce demo suite (live on jtsomwaru.com)
- First meeting goal: NOT to sell a project. Goal is to understand their biggest manual process and identify if automation fits. The pitch comes after.
- NYC-specific signal: Spanish-speaking staff/customers is common in Bronx/Queens wholesale and construction — bilingual agent capability is a genuine differentiator.

## Deferred Niches (April 2026 — do not outreach until conditions change)
| Niche | Score | Why Deferred | Condition to Revisit |
|-------|-------|--------------|----------------------|
| Legal / Professional Services | 20/30 | Cold credibility (no client, no demo), commodity SaaS risk (Harvey, Clio eating workflow layer) | Land one legal client organically OR Harvey/Clio pull back from SMB consultants |
| Staffing Agencies | 19/30 | Lowest score in matrix, Bullhorn/ATS already automating most workflows, no SF penetration signal strong enough | Bullhorn or Crelate clients actively asking for custom Agentforce; 3 confirmed SF staffing JDs |

---

### AgentExchange & Headless 360 (TDX 2026 — April 15, 2026)
- **AgentExchange:** Salesforce launched AgentExchange at TDX 2026 — unified marketplace combining AppExchange, Slack Marketplace, and Agentforce ecosystem into one destination for agentic apps and agents. Partners can now publish directly to a unified catalog. Changes distribution path for Agentforce solutions: certified partners (like JT) can publish to the catalog, giving consulting engagements a referral pipeline and credibility anchor. When prospect asks "is this a real solution?" — AgentExchange is the answer.
- **Headless 360:** Salesforce introduced unified API-driven architecture stacking data, workflows, and AI agents behind a single API layer. All Salesforce objects now exposed as MCP tools, APIs, or CLI commands — the entire SF platform is "agent-readable" by default. Implication: prospects don't need to manually expose their SF data for agents to read it. The consulting engagement is now easier to scope because the API surface is standardized.
- **Pitch impact:** "You're already licensed for Agentforce. AgentExchange shows it's a real product category, not a bet. And Headless 360 means connecting it to your data is now standardized work — not a custom integration." This closes the "is this production-ready" objection.

## Recent Competitive Intelligence
> Auto-updated by Weekly Intelligence Synthesis. Last updated: 2026-06-28.
> Use these signals in outreach hooks, pitch framing, and ICP targeting decisions.

### ICP 1 — Wholesale Distribution
- **UNFI AI inventory (Mar 2026):** Enterprise wholesale (UNFI, ~12 sites) rolling out AI inventory planning. Mid-market distributors (JT's ICP, 5-75 employees) won't see this for 12-18 months — the window is real. Pitch angle: "the Amazons have it. The family-run distributors don't. Yet."
- **Warehouse robotics AMR/AGV:** Physical automation (robots) growing at 9.6% CAGR into mid-market. Important: this is PHYSICAL, not digital workflow. JT's lane (order intake, catalog access, dispatch) is unaffected — these buyers are spending on the warehouse floor, not the back-office ops workflow. Do NOT conflate.

### ICP 2 — Construction & Skilled Trades
- **Acumatica construction ERP AI (Mar 2026):** Acumatica added AI risk detection, forecasting, anomaly detection, and progress billing automation. Key implication: ERP buyers are getting AI features bundled. JT's angle is NOT the ERP — it's the workflow ABOVE the ERP (dispatch coordination, job status visibility, crew communication). These are gaps Acumatica doesn't touch. Reframe from "we build automations" to "we connect the ERP to the field."
- **38% contractor AI adoption (Apr 2026):** Adoption more than doubled YoY per marketingcode.com. Firms using AI are winning bids and cutting costs. Early-mover window for NYC SMBs is this year. Urgency angle is now credible in outreach: "Your peers are building this now."

### ICP 3 — Property Management
- **Entrata Agentic PMS (Mar 2026):** Entrata launched 100+ embedded AI agents for leasing, maintenance, accounting, payments, resident ops — explicitly marketed as industry's first "Agentic PMS." This is enterprise multifamily (200+ units, institutional). JT's ICP (AppFolio/Buildium shops, 500-5000 units, small teams) won't switch to Entrata. But it validates the AI agent pattern in PM. Pitch angle: "Entrata built this for enterprise. We build the equivalent for AppFolio shops."
- **DoorLoop AI (Mar 2026):** DoorLoop (smaller PM platform) added AI-powered rent analysis and predictive maintenance alerts. Signal: even the smaller PM SaaS players are adding AI features. The gap JT fills is NOT features — it's workflow orchestration between platforms and the human team. Focus outreach on the coordination problems, not the feature gap.
- **McKinsey PM ROI numbers (Apr 2026):** Rental orgs seeing 3-7% renewal rate improvement with AI workflows; lead response times improved 90%+ with 24/7 agents (Forbes/McKinsey March 2026). These are now citable, published numbers. Use in M2 follow-ups and proposals: "McKinsey's March report showed rental operations improving renewal rates by 3-7% with agent workflows. I'm building the same layer for AppFolio shops."

### ICP 4 — Insurance Operations
- **WTW Survey (Mar 2026):** 36% of insurers plan straight-through claims processing automation (up from 14% current). Stat is citable in outreach: "WTW's March 2026 survey shows your peers are actively building the business case for claims automation right now." Use in M2 follow-up when a prospect has shown prior interest — not in cold M1.
- **Salesforce Ambient Intelligence (Mar 2026):** Salesforce showcased real-time sales call AI + Agentforce governance upgrades. Insurance orgs already on Salesforce are getting direct product demos of this. Pitch angle: "Salesforce is showing your exec team what's possible at Dreamforce. We implement the specific piece that your claims workflow needs."

### May 2026 — Vertical AI Platform Acceleration
- **Wholesale distribution:** Canals raised $35M to automate distributor workflows across messy email, PDF, spreadsheet, ERP, sales order, AP, and purchasing-validation inputs. This validates JT's wholesale wedge: SMB distributors do not need an AI chatbot first; they need the manual document-to-system work turned into structured workflow. Pitch angle: "Canals is proving the enterprise version of this category. I build the focused version for the workflow your team touches every day."
- **Construction/skilled trades:** NavigateAI launched with $25M to build AI copilots for field workers, with construction and real-estate launch partners including Lennar/Tishman-adjacent names. This pushes construction AI closer to jobsite media, training, QC, and field documentation. JT's SMB angle should stay on the work after the field note exists: status visibility, exception routing, owner alerts, change-order evidence, and follow-up discipline.
- **Property management:** Entrata filed for IPO after a 23% Q1 2026 revenue jump and 2.5M units on-platform, reinforcing that PM operating software plus embedded AI is now a capital-market story. For AppFolio/Buildium shops, the pitch is "enterprise PM platforms are baking this in; the smaller operators still need the workflow layer above the tools they already use."
- **Insurance:** Roots Automation launched Bevaya, an AI-agent platform built exclusively for insurance across underwriting, claims, and policy servicing. This confirms insurance automation is verticalizing fast. Salesforce shops need Agentforce activation plus insurance-specific workflow judgment, not generic "AI assistant" copy.

### Weekly Intelligence Additions — 2026-04-26
- **Agentforce ARR acceleration ($800M ARR, +169% YoY):** Enterprise AI-agent adoption is no longer hypothetical. Use as urgency proof across Salesforce-adjacent prospects: "the market has moved from pilots to budgeted external adoption." Best fit: insurance, PM firms on Salesforce, and any prospect evaluating platform-led AI.
- **Salesforce + Google Cloud Agentforce partnership:** Cross-platform agent workflows across Salesforce and Google Cloud reinforce the orchestration pitch. For SMB/mid-market buyers, the useful angle is not platform complexity — it is that agent workflows are becoming the default enterprise operating model, and smaller firms need a practical version.
- **ConstructConnect Takeoff Boost:** AI-powered construction estimating is moving into mainstream construction software. For construction/skilled trades ICPs, pitch around estimating, document extraction, bidding speed, and back-office throughput before generic "AI agents."
- **Vertafore Velocity AI:** Insurance vendors are packaging AI around friction reduction across the distribution chain. For Salesforce insurance shops, pitch specific workflow relief — claims intake, broker servicing, renewal prep, documentation — not abstract transformation.

### Weekly Intelligence Additions — 2026-05-03
- **Property management AI adoption gap:** GlobeSt / Building Engines report that 60%+ of property management teams have not implemented AI yet. This keeps PM firmly in the "implementation gap" lane: buyers know AI is coming but need practical workflow pilots, not enterprise platform pitches.
- **Wholesale competitor movement:** Augment acquired Merlin AI to expand into wholesale distribution, validating wholesale/distribution as an active AI automation category. Pitch angle: competitors are building AI teammates for distributors; mid-market firms need an operator-grade first workflow before platform vendors define the market for them.
- **Construction AI training gap:** DEWALT's AI training study shows construction workers are interested in AI but lack hands-on, jobsite-relevant training. This strengthens JT's construction angle: implementation has to include field workflow mapping and adoption support, not just software setup.

### Weekly Intelligence Additions — 2026-05-10
- **Wholesale distribution automation keeps moving up-market:** Associated Wholesale Grocers approved a major warehouse automation investment while Augment/Merlin activity validates AI teammates for distributors. JT's mid-market wedge should stay workflow-first: inventory exception queues, PO/vendor follow-up, catalog cleanup, and dispatch/ETA handoffs before robotics or full WMS replacement.
- **Property management wedge is operational, not feature parity:** Recent SMB PM signals reinforce that maintenance triage, leasing follow-up, resident/owner communications, and back-office exceptions are the buyer language. Avoid competing with Entrata/AppFolio feature roadmaps; sell the connective workflow layer around the PMS.
- **Construction AI adoption is now a training + workflow problem:** The construction market keeps validating AI demand, but the blocker is jobsite-relevant adoption. Pitch field workflow mapping, document/estimate extraction, and handoff automation before generic "AI transformation."

### Weekly Intelligence Additions — 2026-05-17
- **Property management AI is moving from adoption gap to portfolio-scale rollout:** A property-management operator reported an EliseAI rollout across 3,000 units with a plan for 8,000 more. This validates PM AI beyond vendor marketing. JT's wedge should avoid "AI leasing assistant" feature parity and instead target the exception layer around AppFolio/Buildium/Rent Manager: aging vendor follow-ups, owner-visible maintenance issues, leasing handoffs, and human approval points.
- **Insurance AI targeting must be stack-qualified:** Insurance-native agentic platforms are now packaging underwriting, FNOL, and claims workflows, but JT's Agentforce wedge only strengthens when the prospect has visible Salesforce, Salesforce-based insurance platforms, Novidea, or a clear CRM/AMS handoff. MGA size alone is not enough; use stack evidence before making an Agentforce claim.
- **AI agents are becoming accountable seats, not invisible scripts:** Recent agent-platform signals emphasize named AI agent actions, override paths, ticket history, and escalation. This reinforces JT's implementation angle across all ICPs: build workflows with identity, audit trail, and human handoff before promising autonomy.
- **Agentforce Operations validates the back-office wedge:** Salesforce is now explicitly packaging Agentforce for outdated back-office process automation, with flow-triggering ecosystem integrations entering beta in May 2026. For Salesforce-adjacent insurance, PM, and operations-heavy SMBs, pitch one measurable back-office cycle first: intake, status routing, renewal prep, exception review, or document follow-up.


### Weekly Intelligence Additions — 2026-05-24
- **Insurance agencies are moving from exploration to 2026 AI investment:** ReSource Pro reports 98% of insurance agencies are planning AI investments in 2026. This strengthens ICP 4, but it does not loosen the Salesforce gate: prioritize agencies with Salesforce/Novidea/Salesforce-native workflow evidence, then pitch one claims, renewal, broker-servicing, or documentation cycle with auditability. Source: resourcepro.com/blogs/why-ai-in-insurance-agencies-is-defining-2026
- **Property management AI bottleneck is data-entry-to-workflow, not tool awareness:** The latest PM signal says inspection findings still die before they become tracked work. This reinforces JT's AppFolio/Buildium exception-layer wedge: convert inspection notes, maintenance findings, vendor follow-ups, and owner-visible issues into accountable queues.
- **Construction AI remains adoption-and-workflow constrained:** Fresh construction coverage this week stayed around safety, training, project data, and skilled-trades labor pressure, not a new platform release. Keep the pitch field-first: map the jobsite/admin handoff, then automate the smallest cycle with clear ownership.

### Weekly Intelligence Additions — 2026-06-07
- **Property management front desk AI is becoming table stakes:** Fresh June PM signals cluster around AI front desk, missed-call text-back, leasing follow-up, maintenance intake, tenant support, and vendor routing. For AppFolio/Yardi/RealPage-style shops, the pitch should not be "AI assistant." It should be "front desk plus exception desk": capture the tenant/resident request, classify it, route it, and show the manager aging exceptions before tenants escalate.
- **Construction field evidence capture is productizing:** Sitemetric launched an AI construction camera and June construction software coverage keeps emphasizing field photos, notes, inspections, and site updates. JT's construction wedge should stay one step after capture: what changed, who owns the blocker, what evidence supports the change order, and what update the owner/client sees.
- **Insurance AI demand is shifting from tooling to confidence:** Insurance Business reported nearly 90% of insurance respondents expect more underwriting tasks to be automated and 65.9% plan additional AI underwriting tools in 2026. For Salesforce insurance shops, pitch governed workflow activation: intake, review queues, underwriting/claims status routing, human approval, and audit trail.
- **Agentforce is becoming an operating layer, not a feature:** Agentforce ARR reached $1.2B with 205% year-over-year growth in Q1 FY2027 reporting, while Salesforce's Contentful acquisition gives Agentforce a structured content layer. For Agentforce-eligible prospects, use this as market proof that the platform is crossing from pilot narrative into budgeted operating infrastructure.

### Weekly Intelligence Additions — 2026-06-14
- **Construction AI is moving from capture to project-level risk control:** Document Crunch, a Trimble company, launched project-level AI risk intelligence, and McCarthy's Palantir partnership points to connected construction operating systems rather than one-off document review. JT's SMB construction wedge should stay practical: field evidence, contract risk, blocker ownership, change-order support, and the manager queue that shows what needs action.
- **Wholesale/distribution automation is broadening beyond warehouse robotics:** Fresh distribution coverage is pairing AI-powered WMS, inventory velocity, warehouse modernization, and AR action queues. For family-run distributors, do not pitch full WMS replacement. Pitch one daily operating queue: orders stuck in email/PDF, aging AR follow-up, inventory exceptions, vendor follow-up, or cross-branch availability.
- **Insurance AI is verticalizing around underwriting, claims, and vendor governance:** Insurance-native AI platforms are now packaging underwriting extraction, claims intake, document routing, renewal status, and policy servicing. Salesforce insurance prospects still need the Agentforce activation frame, but the hook should name confidence thresholds, human review, audit trail, and status logging before automation volume.
- **Agentforce monetization is shifting toward consumption and outcome billing:** Salesforce's definitive agreement to acquire m3ter adds native high-volume metering, rating, and usage/outcome billing to Agentforce Revenue Management. Pitch impact: do not argue tokens or license price. Show the workflow result, the approval boundary, and the measurable event the business would be willing to pay for.

### Weekly Intelligence Additions — 2026-06-21
- **Construction AI is becoming a data-access and document-control fight:** Trunk Tools launched Cortex as a construction intelligence layer over drawings, RFIs, schedules, submittals, contracts, change orders, bids, and specifications, while the Procore/Trunk Tools access conflict shows the real constraint is controlled project data access. JT's SMB construction wedge should be a practical run-control layer: what changed, which document/source supports it, who owns the next action, and what gets reviewed before the client asks.
- **Insurance AI orchestration is packaging governance as the product:** Earnix launched AIOS as an insurance-native AI orchestration system for high-stakes decisions, combining agents, models, workflows, governance, and human oversight. For Salesforce insurance shops, keep the pitch stack-qualified and specific: claims, underwriting, renewals, or broker-service workflows with confidence thresholds, human review, audit trail, and status logging.
- **Agentforce service automation is consolidating around proven customer-agent tech:** Salesforce's definitive agreement to acquire Fin for about $3.6B strengthens Agentforce's customer-service automation surface. For insurance and any Salesforce-backed service queue, the pitch should not be "AI chatbot." It should be activation plus run control: intake, routing, approval boundary, escalation, and measurable resolution event.
- **AI transformation hiring validates the run-control proof need:** Fresh Xplor, Arcadia, and Jobgether signals keep repeating use-case intake, tool registry, privacy/security review, pilots-to-production, executive reporting, and quantified outcomes. This supports packaging JT's proof around operating-model ownership, not another isolated demo.

### Weekly Intelligence Additions — 2026-06-28
- **B2B commerce is moving toward text-native procurement:** Salesforce's June 24 Agentforce Commerce release puts B2B Buyer Agent inside WhatsApp/SMS with catalog, inventory, contract pricing, and order context. For wholesale/distribution prospects, this raises buyer expectations around reorder convenience. JT's wedge stays practical: make the catalog, pricing, inventory, and approval rules clean enough for an agent-ready reorder workflow before pitching a full commerce platform. Sources: salesforce.com/news/stories/agentforce-commerce-announcement/ and digitalcommerce360.com/2026/06/24/salesforce-releases-ai-agents-b2b-ecommerce-updates/
- **Property-management AI now has to include governance, not just leasing automation:** Grant Thornton's June 23 multifamily AI piece frames leasing automation, guided AI tours, instant lead response, and renewal package generation as real front-office use cases, but says growth starts with governance. For AppFolio/Buildium shops, the sharper pitch is still "front desk plus exception desk": capture the request, route it, show the manager the aging or risky item, and keep approval/audit boundaries visible. Source: grantthornton.com/insights/articles/real-estate/2026/multifamily-ai-growth-starts-with-governance
- **Insurance AI is turning into core-governed orchestration:** Fresh insurance coverage points to AI agents spreading across underwriting, claims, and service while Duck Creek and governance vendors emphasize trusted core context, partner agents, human-in-the-loop underwriting, and oversight. For Salesforce insurance prospects, generic "claims AI" copy is weaker than a governed run-control offer: one workflow, confidence threshold, human review, audit trail, and status logging. Sources: dig-in.com/news/where-insurers-stand-on-ai-agents, iireporter.com/duck-creek-ceo-trusted-ai-starts-in-the-core/, and intellectai.com/ai-governance-in-commercial-insurance/
