# Networking & Relationship Agent

**Purpose:** Track warm contacts, follow-up timing, relationship warmth, and event attendance. Different from the outreach pipeline (cold prospects) — this covers people JT has actually met or has a warm connection to.

---

## Data Store

`~/.openclaw/workspace/memory/networking/contacts.md` — warm contact log
`~/.openclaw/workspace/memory/networking/events.md` — events attended + upcoming
`~/.openclaw/workspace/memory/networking/state.json` — last run timestamps

---

## Contact Schema (contacts.md)

Each contact entry:
```
### [Name] — [Company] — [Role]
- **Met via:** [event / warm intro / Aya referral / LinkedIn / etc.]
- **Date met:** YYYY-MM-DD
- **Warmth:** 🔥 Hot (recent convo, expressed interest) | 🟡 Warm (met, positive) | 🧊 Cold (met once, no follow-up)
- **Last touch:** YYYY-MM-DD — [what happened]
- **Next action:** [specific action + by when]
- **Notes:** [pain points mentioned, personal details, what they do]
- **ICP fit:** High / Medium / Low — [reason]
```

---

## Warmth Decay Rules

| Last touch | Warmth status |
|---|---|
| < 14 days | Maintain current |
| 14-30 days | Downgrade one level |
| 30-60 days | 🧊 Cold unless reconnect |
| > 60 days | Flag for re-engage or archive |

Hot contacts not followed up within 7 days → flag immediately in morning brief.

---

## Weekly Cron Behavior (runs inside heartbeat or standalone)

1. Read contacts.md
2. Apply warmth decay to all contacts based on last touch date
3. Identify: any Hot contacts not touched in 7+ days → flag HIGH in Telegram
4. Identify: any next actions overdue → list in Telegram
5. Identify: upcoming events in events.md → remind 48h before
6. Output: brief Telegram summary with action list

**Telegram format:**
```
🤝 Relationship Check
🔥 Hot — follow up needed: [Name] ([days since last touch])
📅 Event: [Name] — [date] — [what to bring]
⏰ Overdue actions: [Name] — [what]
```

---

## Events Log (events.md)

Each event:
```
### [Event Name] — [Date] — [Venue/Link]
- **Status:** Attending / Considering / Attended
- **ICP relevance:** [who attends — construction? PM? insurance?]
- **Contacts met:** [names if attended]
- **Notes:** [what to bring, follow up from]
```

**NYC Events to track (seed list):**
- BOMA NY — building managers, PM companies
- REBNY events — real estate, PM
- AGC NYC chapter — contractors, construction
- NYC Chamber of Commerce — broad SMB
- Brooklyn Chamber of Commerce — local construction/trades heavy
- Eventbrite NYC "AI business" / "construction tech" / "property management"
- Meetup: NY AI & Machine Learning, NYC Tech
- NYC SBS (Small Business Services) events
- Salesforce World Tour NYC (when scheduled)

---

## Triggering Manual Updates

When JT says:
- "I met [Name] at [event]" → Eve logs contact entry, warmth = Warm, prompts for details
- "Had a call with [Name]" → update last touch, ask for next action
- "Gil gave me [Name]" → log as referral, warmth = Hot, ICP = High, move to outreach pipeline if ICP fit
- "Going to [event]" → log in events.md, set 48h reminder cron

---

## Integration with Outreach Pipeline

When a networking contact expresses interest or asks "how does this work?" → promote to T1 in consulting pipeline.
When Gil or another client gives a name → create contact entry + create T2 research task in MC immediately.

---

## Gil Meeting Protocol (standing)

After every Gil meeting/call:
1. Log what was discussed in contacts.md under Gil's entry
2. Ask: did he mention any names? → log each as new Hot contact, ICP High
3. Create MC task to research + draft targeted outreach for each name within 24h
4. Update Aya client status in MEMORY.md if project status changed

---
