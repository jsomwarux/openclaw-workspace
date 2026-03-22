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

**Pricing angle (post-March 2026):** Salesforce's CFO has flagged that Agentforce token pricing will commoditize. Never compete on per-token cost. Position value on outcomes and time saved: "You don't pay me per API call. You pay me once for a system that handles X without a human rep touching it."

**Budget:** $6,500–$15,000 for an Agentforce deployment. Larger than n8n engagements because of Salesforce complexity and enterprise context.

**Demo:** Insurance Service Agent (already built) — claims intake, routing, FAQ handling. Directly applicable.

---

## Notes for All ICPs
- JT is NOT a developer — do not pitch coding/custom dev work. Pitch implementation.
- Proof points: Aya dashboard ($1,500), StreetEasy scraper ($1,000), Agentforce demo suite (live on jtsomwaru.com)
- First meeting goal: NOT to sell a project. Goal is to understand their biggest manual process and identify if automation fits. The pitch comes after.
- NYC-specific signal: Spanish-speaking staff/customers is common in Bronx/Queens wholesale and construction — bilingual agent capability is a genuine differentiator.
