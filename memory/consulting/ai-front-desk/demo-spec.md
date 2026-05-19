# AI Front Desk Demo Spec — Property + Construction Operators

**Purpose:** turn the restaurant chatbot pattern into JT's stronger consulting wedge: a request-capture, triage, escalation, and reporting layer for ops-heavy SMBs.

## Demo company
**MetroWorks Property & Build Co.** — fictional NYC operator managing 850 rental units plus small renovation/maintenance crews.

## Buyer pain to show
- Leasing questions arrive after hours and go unanswered.
- Maintenance requests come in through phone, email, web forms, and texts with missing details.
- Estimating requests waste staff time when service area, budget, or urgency are unclear.
- Managers lack a weekly view of what requests came in, what got resolved, and what should have escalated.

## Demo promise
"Your team should only see the requests that need a human. The AI Front Desk captures the rest, asks the missing questions, routes urgent items, and shows you what it handled each week."

## Core workflows
1. **Leasing inquiry capture**
   - Collect name, phone/email, desired move-in date, budget, neighborhood/building, bedroom count, pet needs, showing availability.
   - Route qualified leads to leasing inbox/CRM/Sheet.

2. **Maintenance triage**
   - Capture unit/building, issue type, severity, photos if available, access permission, callback number.
   - Escalate emergencies immediately.
   - Send non-emergency summary to maintenance queue.

3. **Construction / estimate intake**
   - Capture project type, address/borough, timing, budget range, site access, decision maker, photos/plans if available.
   - Filter out non-service-area or unqualified requests politely.

4. **Vendor / tenant FAQ**
   - Answer only from approved source-of-truth: hours, office contact, rent payment process, maintenance submission process, showing policy, emergency line.
   - If uncertain, escalate instead of guessing.

5. **Weekly ops report**
   - Show conversations, qualified leads, maintenance requests, emergencies escalated, incomplete requests, top repeated questions, response times, and estimated staff time saved.

## Required intake fields
- requester name
- role: tenant / prospect / vendor / owner / other
- phone + email
- property/building or service address
- request type
- urgency
- preferred callback time
- attachments/photos/plans if available
- consent to route request to team

## Escalation rules
Escalate immediately when request includes:
- leak, flood, gas smell, fire, no heat in legal window, lockout, active security issue
- injury, legal threat, media inquiry, discrimination/fair-housing language
- payment dispute, eviction, rent concession, lease legal interpretation
- project value above threshold, e.g. $25K+
- any question not covered by source-of-truth

## Safety / trust boundaries
- Do not provide legal, medical, financial, or fair-housing advice.
- Do not promise availability, pricing, approval, timeline, or lease terms unless in source-of-truth.
- Do not pretend to be human. If asked, disclose: "I'm the automated front desk assistant, and I can get the right details to the team."
- For emergencies, tell the user to call the emergency line immediately and route internally.

## 10 demo questions
1. "Do you have any 2-bedrooms under $3,500 in Astoria?"
2. "Can I tour Saturday afternoon?"
3. "My ceiling is leaking in unit 4B. What do I do?"
4. "The heat hasn't worked since last night."
5. "Can I pay rent by Zelle?"
6. "I'm a vendor. Where do I send COI and W-9?"
7. "We need a contractor for a lobby renovation in Brooklyn. Can you quote it?"
8. "Do you work in Staten Island?"
9. "Can I sublet my apartment for 3 months?"
10. "I have photos of water damage. Can I send them?"

## Demo build path
**Fast prototype:** Voiceflow or simple web chat + Claude prompt + Google Sheet/Email routing.

**Consulting-grade version:**
- Web form/chat intake
- Claude prompt with source-of-truth and escalation policy
- n8n workflow routes requests to Google Sheet/Airtable/CRM/email/SMS
- Slack/Telegram/email alert for emergency escalations
- weekly report generated from structured log

## Monthly report metrics
- total conversations
- requests resolved without human follow-up
- qualified leasing leads captured
- estimate/project leads captured
- maintenance requests triaged
- emergency escalations
- incomplete requests needing human callback
- top 10 repeated questions
- average response time
- estimated admin hours saved
- revenue/risk opportunities captured

## Demo success criteria
A prospect should understand in under 90 seconds:
1. This is not a generic chatbot.
2. It captures structured requests their team currently chases manually.
3. It escalates risk instead of freelancing answers.
4. The weekly report proves ongoing value.
