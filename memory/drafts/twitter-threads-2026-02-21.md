# Draft X Threads — 2026-02-21
*Account: @jts_14 | Drafted by Eve during 8 PM heartbeat*

---

## Thread 1: "Building an AI assistant that actually works while you sleep"

*Angle: Builder content. Shows the infrastructure work. Authentic process post.*

---

**Tweet 1 (hook):**
I spent the day building an AI assistant infrastructure that runs 24/7 on my Mac mini — no cloud, no subscriptions, no babysitting.

Here's everything I set up and why it matters 🧵

---

**Tweet 2:**
The problem with AI assistants: they're stateless.

Every new conversation, they forget who you are, what you're building, and what you decided last week.

My fix: a structured file system that IS the memory.

SOUL.md, MEMORY.md, daily notes. The AI reads them at startup.

---

**Tweet 3:**
What the setup does automatically every day:

→ 2 AM: backs up everything (7-day retention)
→ 3 AM: cleans up orphan sessions (sessions.json was 77MB before this)
→ 7:30 AM: sends me a morning brief via Telegram
→ 9 PM: prompts my health check-in

Zero terminals. Zero manual work.

---

**Tweet 4:**
The health tracker is interesting.

I describe my day naturally: "7, neck tight, chicken + rice, 30min walk, 8"

It parses the energy, pain areas, food, exercise, sleep → writes to SQLite → generates weekly trend reports.

Turns out I get neck pain on days I skip walking.

---

**Tweet 5:**
Also built a Mission Control dashboard — Next.js + local Convex DB.

Always-on at localhost:3000 via LaunchAgents (macOS native, more reliable than crontab).

8 sections: tasks, schedule, memory browser, agents, monitor, costs, audit trail.

The AI can create tasks programmatically via API.

---

**Tweet 6:**
The part that changed how I think about AI tools:

Local-first means no API keys in the cloud, no data leaving my machine, no monthly bills scaling with usage.

The AI runs on my hardware, reads my files, knows my context.

That's a different relationship than a chatbot.

---

**Tweet 7 (close):**
This is one setup — but the pattern scales.

Same infrastructure can run specialized business agents: one for client research, one for content, one for code.

Building towards Opticfy on top of this foundation.

The infrastructure IS the moat.

---

---

## Thread 2: "I scored 5 expansion niches for Nash Satoshi using the same 4-LLM methodology"

*Angle: Shows Nash Satoshi's methodology. Teases expansion. Good for investor/builder/crypto audience.*

---

**Tweet 1 (hook):**
Nash Satoshi uses 4 AI models cross-checking each other to generate consensus crypto rankings.

I scored 5 new niches using the same methodology to see where it should expand next.

The winner surprised me 🧵

---

**Tweet 2:**
Quick background on the methodology:

GPT-5.2, Opus 4.6, Gemini 3 Pro, and Grok 4 independently analyze each asset.

They cross-check each other's reasoning.

Consensus score + game theory positioning = rankings you can't game by paying one reviewer.

---

**Tweet 3:**
The 5 expansion candidates I evaluated:

1. Skincare product rankings
2. Alcohol/spirits quality rankings
3. Baby product rankings
4. College rankings
5. Neighborhood rankings for real estate

Scored each on: market size, competition, monetization, user acquisition, virality, and methodology fit.

---

**Tweet 4:**
College rankings scored highest on methodology fit (5/5).

US News & World Report is being actively boycotted by Yale Law, Harvard Med, Stanford.

"4 AI models that can't be gamed by universities gaming their methodology" is literally the solution the market is asking for.

But the monetization is hard.

---

**Tweet 5:**
Skincare scored highest on virality (5/5).

r/SkincareAddiction has 1.2M members and "best retinol under $30" posts go viral constantly.

The differentiation: existing sites (INCIDecoder, Beautypedia) focus on ingredients.

Nash Satoshi would rank whole products. Different angle.

---

**Tweet 6:**
The winner: baby products (25/30).

Not the most obvious choice. But think about it:

→ Parents KNOW Amazon reviews are gamed
→ Stakes are high (child safety)
→ "4 AI models that can't be sponsored" is the exact pitch anxious parents want
→ Affiliate on car seats ($300-800 avg) is lucrative

---

**Tweet 7:**
The positioning basically writes itself:

"The only baby gear rankings built by AI models that can't accept payments."

Launch wedge: car seats. One category, high stakes, massive search volume.

Get 3-5 viral Reddit posts in r/BabyBumps. Expand from there.

---

**Tweet 8 (close):**
The Nash Satoshi methodology works in any niche where:
- Reviews are gamed or biased
- Stakes are high enough that people want objectivity
- Consensus across multiple perspectives adds genuine value

Crypto was just the first application.

More coming.

---

---

## Quick Post: Mission Control screenshot drop

*Single tweet, good for engagement*

---

Built a Mission Control dashboard for my AI infrastructure today.

Dark theme, real-time Kanban, memory browser, audit trail.

Runs locally on my Mac mini. Always on. No cloud needed.

The assistant can create tasks via API. I can track what it's done vs. what's pending.

Local-first > SaaS for personal infrastructure.

[screenshot would go here]

---

*Notes for JT:*
- Thread 1 is the strongest for builder/indie hacker audience
- Thread 2 works well timed to any Nash Satoshi news or milestone
- The single screenshot tweet is great for quick engagement; grab a screenshot of localhost:3000 first
- Both threads can be adapted for LinkedIn with slightly more formal tone
