# Aya Referral Meeting Prep — Gil
Date: 2026-03-20

## What We Know About Aya
- Co-living operator and real estate developer, NYC (Manhattan + Brooklyn)
- 11-50 employees, founded 2013
- Two business lines: (1) construction/development, (2) co-living property management
- Partners page shows corporate housing clients (companies sending interns/employees) — not construction vendors
- Gil is on the construction side — JT built the $1,500 construction progress dashboard for him
- Active pipeline: $1,000 StreetEasy scraper (signed), $2,500 co-living dashboard (pending), acquisitions dashboard (stalled)

## Aya's Likely Vendor/Partner Ecosystem

Because Aya does both construction AND property management, Gil's network spans two categories:

### Construction Side (his vendors)
| Vendor Type | Examples | What they do manually |
|---|---|---|
| HVAC subcontractors | Smaller NYC HVAC firms ($2M-$10M) | Scheduling, job status updates, invoice tracking |
| Plumbing/electrical subs | Trade contractors, 5-30 employees | Same — all via phone/text/spreadsheet |
| General subcontractors | Carpentry, masonry, drywall | Job progress reporting, punch lists |
| Material suppliers | Lumber yards, plumbing supply, electrical supply | Reorder tracking, delivery coordination |
| Architecture/design firms | If Aya does ground-up development | Drawing revisions, permit tracking |

### Property Management Side (their partners)
| Partner Type | What they do | Pain |
|---|---|---|
| Real estate owners/landlords | Partner with Aya to manage their units | Vacancy tracking, maintenance coordination |
| Maintenance vendors | Cleaners, handymen, appliance repair | Dispatch, scheduling, status reporting |
| Leasing/brokerage firms | Fill units for Aya | Application tracking, lead handoff |

---

## The Most Valuable Intel To Extract From Gil

These are your questions — ask them naturally in conversation, not as an interview:

**On construction vendors:**
- "The dashboard has been really useful — are any of the subs you work with dealing with the same kind of visibility problem you had?"
- "Who do you call the most when something's stalled on a site?"
- "Are any of your HVAC or electrical guys still running on spreadsheets? Or just group texts?"

**On property management partners:**
- "On the co-living side, are the property owners you work with managing their own maintenance, or does that go through you?"
- "What's the messiest part of managing multiple properties at once for you guys?"

**The warm intro ask (use after good conversation):**
- "I'm starting to work with a few other companies in construction and real estate. Is there anyone in your network you think would get value from something similar? Even a quick intro would be great."
- Follow immediately: "What do you know about how they're currently handling [X]? Even a rough sense of their setup would help me come in with something relevant."

---

## Vendor Types By Automation Opportunity (priority order for demos)

### 1. HVAC/Plumbing/Electrical Subcontractors — HIGHEST PRIORITY
**Why:** Same exact profile as Aya's construction problem. Job tracker already built.
**Pain:** Foremen text job status. Office doesn't know what's stalled. Clients call to ask for updates.
**Demo:** Construction Job Completion Automation (already built — Hd0eJo1uRKb1JJHy)
**Pitch:** "I built this for Gil's team. One message from the foreman, client gets a professional update, status logged automatically. Saves 30+ minutes a day."
**Stack needed:** n8n + Claude + Sheets. Already done.

### 2. Property Maintenance Vendors (cleaners, handymen)
**Why:** Aya manages co-living — they have maintenance vendors. Those vendors get dispatched manually.
**Pain:** Tenant submits a problem, someone texts the vendor, nobody tracks status.
**Demo:** PM Maintenance Triage (KFsT3zSrilh1EXrA — already built)
**Pitch:** "Built this for a property management firm — tenant submits, AI classifies urgency, routes the vendor, sends a status update automatically."
**Stack needed:** Already done.

### 3. Material Suppliers / Distributors
**Why:** If Aya does ground-up construction, they have supplier relationships. Suppliers are wholesale distribution = JT's ICP.
**Pain:** Reorder tracking via email/spreadsheet. No visibility on low stock until it's a problem.
**Demo:** AI Inventory Reorder & Supplier Notification (KP8oXZvmoGTvcWUd — already built)
**Pitch:** H.C. Oswald angle — same pattern.

### 4. Real Estate Owners (Aya's PM clients)
**Why:** Aya's property management partners are owners who gave Aya their units to manage.
**Pain:** Portfolio visibility — occupancy, maintenance status, revenue — usually scattered.
**Demo:** Same Aya construction dashboard pattern, adapted for PM (multi-property status).
**Note:** These are harder to reach directly — Gil is the intermediary.

---

## Demo Assets Already Built (nothing new needed for tomorrow)

| Demo | Workflow ID | What it does | Relevant to |
|---|---|---|---|
| Construction Job Completion | Hd0eJo1uRKb1JJHy | Foreman texts → client update automated | HVAC, plumbing, electrical subs |
| PM Maintenance Triage | KFsT3zSrilh1EXrA | Tenant submits → vendor routed → status sent | Property maintenance vendors |
| AI Inventory Reorder | KP8oXZvmoGTvcWUd | Low stock → supplier notified automatically | Material suppliers |
| Georgetown City Services | 1YbGhdUxSKO0nL6z | Complaint → classified → dispatched → confirmed | Government (not relevant here) |

All four are live in n8n at localhost:5678. All need credentials relinked if showing live.

---

## Conversation Anchor: Lead With the Dashboard

Open with what Gil already knows works. Something like:
*"The dashboard's been going well — I've been thinking about what else in your world could use something similar. The same pattern — something messy that could be automated — seems to come up with a lot of companies in construction and real estate."*

Then let him talk. The names he mentions = your next research targets.

---

## After the Call: What to Tell Eve

After the meeting, message Eve with:
- Names of any companies Gil mentioned
- What he said about how they operate (even vague notes)
- Whether he offered a warm intro or just said "there might be someone"

Eve will research each company and build a targeted demo brief within 24 hours.

---

## What NOT to Do Tomorrow
- Don't pitch specific services unprompted — you're in listening mode
- Don't mention pricing unless he asks
- Don't close with "let me know if you think of anyone" — too passive, too vague
- Don't let referral talk pull focus if active Aya pipeline items need closing first
