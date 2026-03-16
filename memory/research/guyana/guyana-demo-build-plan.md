# Guyana Demo Build Plan — JT Somwaru Consulting
**Created:** March 15, 2026
**Purpose:** Three demo builds to show capability to a Guyanese government/consulting firm

---

## Build Priority Order

| Build | Name | Problem It Solves | Est. Build Time | Wow Factor |
|-------|------|-------------------|-----------------|------------|
| 1 | Georgetown City Services Agent | Drainage crisis + digital services | 1–2 days | ⭐⭐⭐⭐⭐ |
| 2 | Infrastructure Project Intelligence Dashboard | Roads/bridges/dams spend accountability | 2–3 days | ⭐⭐⭐⭐ |
| 3 | Procurement Audit Agent | Contract waste / corruption transparency | 1 day | ⭐⭐⭐⭐ (differentiator) |

**Build 1 first.** It uses real Georgetown context, directly references what President Ali just committed to (December 2025 announcement), and has the highest "when can we start?" potential.

---

## Build 1: Georgetown City Services Agent

### The Problem It Solves
Georgetown's drains are flooded, garbage isn't collected, and residents have no formal way to report issues. The government just committed to digital mapping and modernization of drainage systems (December 2025). There is no citizen-facing reporting layer.

### What It Does (Demo Flow)
1. Citizen visits a simple web form OR sends a WhatsApp/SMS message
   - Example input: "There's a blocked drain on Regent Street causing flooding near the market"
2. Claude classifies: issue type (drain / garbage / pothole / flooding / structural), urgency level, extracts street name / location
3. Workflow routes to the correct department:
   - Drainage → Drainage and Irrigation authority dispatch message
   - Garbage → City Constabulary / M&CC sanitation
   - Pothole → Ministry of Public Works
4. Citizen receives auto-confirmation: ticket number + expected response window
5. Department receives: citizen report + AI-generated dispatch summary + location + urgency tag
6. Live dashboard: all open tickets by category, Georgetown neighborhood, days open, status

### Tech Stack
- **Intake:** Tally (free, clean web form) or Typeform
- **Automation:** n8n (already running)
- **AI:** Claude via n8n HTTP node (classify, extract, draft dispatch)
- **Log/DB:** Google Sheets (ticket log)
- **Notifications:** Gmail or Telegram
- **Dashboard:** Looker Studio (free, connects to Sheets) OR lightweight Next.js

### Demo Specifics — Use Real Georgetown Context
Use these real street names and departments in demo data:
- Water Street → Drainage and Irrigation / M&CC
- Regent Street → City Constabulary sanitation
- Sheriff Street → Ministry of Public Works
- Camp Street → Public Infrastructure
- Bourda Market area → M&CC (known flooding hotspot)

**Why this matters:** Walking in with demo data that uses actual Georgetown street names signals you've done your homework. It's not a generic "City X" demo — it's their city.

### Proof Point to Reference
The Aya construction dashboard: same workflow pattern (field report → AI classification → routed notification → dashboard). You built that for $1,500. Show it as precedent. Government version is 100x the scale.

### Status: NOT YET BUILT

---

## Build 2: Infrastructure Project Intelligence Dashboard

### The Problem It Solves
Guyana is spending billions on roads, bridges, dams, and hospitals simultaneously. No unified real-time view of project status, budget vs. actuals, or early warning on cost overruns. Ministry leadership gets monthly paper reports that are already outdated.

### What It Does
1. Contractor or site supervisor submits daily update via WhatsApp or Tally form:
   - Project name, % complete, spend to date, blockers
2. Claude extracts structured data, classifies project status:
   - On Track / At Risk / Over Budget / Blocked
   - Generates one-line executive summary per project
3. Dashboard shows:
   - All active projects by ministry
   - Budget vs. actual spend with variance flag
   - Days behind schedule
   - Unresolved blockers (with days outstanding)
4. Weekly auto-generated briefing: "Projects at risk this week" — auto-emails to ministry contacts
5. Budget overrun threshold → auto-alert to project manager + ministry

### Tech Stack
- Tally/WhatsApp → n8n → Claude → Google Sheets → Looker Studio dashboard
- Weekly briefing: n8n scheduled cron → Claude → Gmail

### Proof Point to Reference
This IS the Aya construction dashboard, scaled. Show Aya dashboard screenshots first, then show the government version with multi-project view. The Aya project was $1,500. A government deployment monitoring $500M+ in projects is a $50K–$200K engagement.

### Status: NOT YET BUILT (Aya dashboard is proof of concept)

---

## Build 3: Procurement Audit Agent

### The Problem It Solves
Guyana's NPTA (National Tender & Procurement Administration) publishes all government contracts publicly at npta.gov.gy. But nobody is systematically monitoring for anomalies: sole-sourced contracts above threshold, vendors winning disproportionate share from one ministry, contract awards significantly above published estimates.

### What It Does
1. Scraper pulls weekly contract awards from NPTA.gov.gy:
   - Vendor name, amount, ministry, contract type (competitive bid vs. sole-source), award date
2. Claude analyzes against rules:
   - Flag: sole-sourced contracts over $X threshold
   - Flag: same vendor winning 3+ contracts from same ministry in 30 days
   - Flag: award price >20% above published estimate
   - Flag: contracts awarded without published tender
3. Weekly plain-English report: "3 contracts this week may warrant review" with specifics
4. Dashboard: spend by ministry, competitive vs. sole-source ratio, anomaly log, trend over time

### Positioning (Critical)
**Do NOT call this a corruption detection tool.** Frame as:
- "Budget optimization and procurement transparency dashboard"
- "Helps ministry leadership identify efficiency opportunities and ensure procurement best practices"
- "Supports the government's accountability commitments to citizens"

Same product. Politically viable framing.

### Why This Wins the Room
Nobody else walking into a Guyanese government meeting has this. It directly addresses what international bodies (IMF, World Bank, US State Dept) have flagged as Guyana's biggest governance risk as oil money flows in. It positions JT as aligned with the government's own stated accountability goals — not adversarial.

### Tech Stack
- Python scraper or Cloudflare /crawl against npta.gov.gy
- n8n pipeline → Claude analysis → Google Sheets → weekly email + dashboard

### Status: NOT YET BUILT

---

## The Pitch Sequence

### In the room:
1. Lead with **Build 1** — everyone in the room has seen Georgetown's flooded streets. Start there.
2. Once they're nodding, reference Aya dashboard as proof you've built this before (show screenshots)
3. Mention Build 3 last — "We also built a procurement monitoring layer that automatically reviews NPTA contract data" — let that land

### The narrative:
> "I build AI automation systems for governments and businesses that are scaling fast. Georgetown has a drainage problem and a project accountability problem — here's what a working solution looks like right now, today."

### What NOT to do:
- Don't show all three demos simultaneously — overwhelming
- Don't pitch without a working live demo of at least Build 1
- Don't go in without local partner or warm intro — procurement decisions are relationship-driven

---

## Next Steps

- [ ] Get warm intro from contact to local firm or ministry connection
- [ ] Build 1 (Georgetown City Services Agent) — target: this week
- [ ] Research local Guyanese tech/consulting firms to partner with
- [ ] Register at npta.gov.gy to monitor active tenders
- [ ] Consider travel to Georgetown for in-person meetings (required for government relationships)
