#!/usr/bin/env python3
"""
notion-swipe-seed.py — One-time seed of the Notion Swipe File with high-quality
viral post examples across JT's niches. Run once to pre-populate the database.

These are structural archetypes — real viral post patterns with anonymized/composite
examples. The recurring cron will find and add real posts from X going forward.

Run: python3 ~/.openclaw/workspace/scripts/notion-swipe-seed.py
"""

import subprocess
import sys

SCRIPT = "/Users/jtsomwaru/.openclaw/workspace/scripts/notion-swipe-push.py"

def push(text, author, url, niche, fmt, why, engagement, hook):
    result = subprocess.run([
        sys.executable, SCRIPT,
        "--text", text,
        "--author", author,
        "--url", url,
        "--niche", niche,
        "--format", fmt,
        "--why", why,
        "--engagement", str(engagement),
        "--hook", hook
    ], capture_output=True, text=True)
    print(result.stdout.strip() or result.stderr.strip())

# ── AI CONSULTING / OPTICFY ──────────────────────────────────────────────────

push(
    text="Most consultants sell decks.\n\nI sold a $1,500 AI dashboard that runs while the client sleeps.\n\nThe deck is dead. The agent is the deliverable.",
    author="@archetype_consulting",
    url="https://x.com/archetype_consulting/status/1",
    niche="AI Consulting,Personal Brand",
    fmt="Hot Take",
    why="Attacks a common consulting norm (decks) and replaces it with a concrete alternative. Makes other consultants want to defend or pile on — drives replies.",
    engagement=4200,
    hook="Contrarian claim"
)

push(
    text="A NYC contractor asked me: 'Can AI tell me if my project is on track?'\n\nWe built it in 3 weeks.\n\nNow it flags delays before his PM does.",
    author="@archetype_consulting",
    url="https://x.com/archetype_consulting/status/2",
    niche="AI Consulting",
    fmt="Story",
    why="Specific client question → specific outcome. Concrete before/after with a punchy last line that implies ROI without stating it.",
    engagement=2800,
    hook="Personal story"
)

push(
    text="The $50K Salesforce implementation vs the $1,500 AI agent that does the same job.\n\nChoose wisely.",
    author="@archetype_consulting",
    url="https://x.com/archetype_consulting/status/3",
    niche="AI Consulting",
    fmt="Contrarian",
    why="Price contrast creates immediate cognitive dissonance. 'Choose wisely' is low-key provocative without being aggressive. Drives quote tweets from both sides.",
    engagement=6100,
    hook="Data surprise"
)

push(
    text="Nobody is selling AI to contractors.\n\nThey're too busy on job sites to go to tech conferences.\n\nThat's the entire opportunity.",
    author="@archetype_consulting",
    url="https://x.com/archetype_consulting/status/4",
    niche="AI Consulting",
    fmt="Hot Take",
    why="Identifies a specific overlooked market segment. Feels like insider knowledge. Makes consultants want to ask 'how do you reach them' — drives replies.",
    engagement=3500,
    hook="Curiosity gap"
)

# ── AI AGENTS ────────────────────────────────────────────────────────────────

push(
    text="We're not building tools anymore.\n\nWe're building employees that never sleep, never complain, and cost $20/month.\n\nThe org chart is about to look very different.",
    author="@archetype_aiagents",
    url="https://x.com/archetype_aiagents/status/5",
    niche="AI Agents",
    fmt="Bold Prediction",
    why="'Employees that never sleep' is a memorable analogy. '$20/month' is a data point that grounds the prediction. 'Org chart' is a specific image that makes it shareable to people in corporate roles.",
    engagement=12400,
    hook="Bold prediction"
)

push(
    text="The AI agent hype is real.\n\nBut 90% of what people call 'agents' are just if/then logic wrapped in a ChatGPT API call.\n\nHere's what a real agent actually looks like:",
    author="@archetype_aiagents",
    url="https://x.com/archetype_aiagents/status/6",
    niche="AI Agents",
    fmt="Thread Opener",
    why="Validates the topic (hype is real) before attacking the execution. The '90%' stat creates insider/outsider framing. Thread hook promises the payoff.",
    engagement=8900,
    hook="Contrarian claim"
)

push(
    text="What happens when your AI agent starts making money without you watching?\n\nWe're about to find out.",
    author="@archetype_aiagents",
    url="https://x.com/archetype_aiagents/status/7",
    niche="AI Agents,x402",
    fmt="Question",
    why="Open-ended question that's slightly unsettling. 'Without you watching' creates mild anxiety that makes people stop. Short and re-readable — high dwell.",
    engagement=5200,
    hook="Provocative question"
)

push(
    text="Agents don't replace workers.\n\nThey replace the work nobody wanted to do anyway.\n\nBig difference.",
    author="@archetype_aiagents",
    url="https://x.com/archetype_aiagents/status/8",
    niche="AI Agents",
    fmt="Contrarian",
    why="Reframes a common fear into a positive. The structure (claim → reframe → mic drop) is a proven viral template. 'Big difference' is a confident close that invites pushback.",
    engagement=9800,
    hook="Contrarian claim"
)

# ── CRYPTO / x402 ────────────────────────────────────────────────────────────

push(
    text="Everyone is looking at price.\n\nI'm looking at the coordination mechanism.\n\nWhen the incentives align, price follows. Not the other way around.",
    author="@archetype_crypto",
    url="https://x.com/archetype_crypto/status/9",
    niche="Crypto",
    fmt="Contrarian",
    why="Positions the author as a sophisticated thinker vs the crowd. 'Coordination mechanism' sounds technical enough to be credible. Invites people to ask what coins have good mechanisms.",
    engagement=3100,
    hook="Contrarian claim"
)

push(
    text="The x402 payment protocol is going to do to AI agents what Stripe did to websites.\n\nMost people haven't heard of it yet.\n\nThat's the opportunity.",
    author="@archetype_crypto",
    url="https://x.com/archetype_crypto/status/10",
    niche="Crypto,AI Agents,x402",
    fmt="Bold Prediction",
    why="Stripe analogy is instantly understandable. 'Most people haven't heard' creates insider knowledge framing. Drops without explaining — forces profile clicks to learn more.",
    engagement=4700,
    hook="Bold prediction"
)

push(
    text="Narrative > fundamentals in the short term.\n\nFundamentals > narrative in the long term.\n\nMost people mix up the timeframe and lose money on both.",
    author="@archetype_crypto",
    url="https://x.com/archetype_crypto/status/11",
    niche="Crypto",
    fmt="Data Drop",
    why="Simple binary framework that sounds obvious once stated but isn't. The third line adds the twist that makes it shareable. Easy to quote tweet with 'this.'",
    engagement=7200,
    hook="Data surprise"
)

# ── JOB MARKET ───────────────────────────────────────────────────────────────

push(
    text="I spent 6 years configuring enterprise software for a Fortune 500.\n\nNow I'm building AI agents that do in a day what used to take my team a week.\n\nThe skill gap is real. Most companies don't know it yet.",
    author="@archetype_jobmarket",
    url="https://x.com/archetype_jobmarket/status/12",
    niche="Job Market,Personal Brand",
    fmt="Story",
    why="Specific tenure + specific company type adds credibility. The before/after framing is universal. 'Most companies don't know yet' creates urgency for hiring managers who are reading.",
    engagement=5600,
    hook="Personal story"
)

push(
    text="AI Solutions Architect is the most undervalued job title of 2025.\n\nCompanies are paying $180K+ for people who can bridge business problems and AI tools.\n\nThere are almost no candidates.",
    author="@archetype_jobmarket",
    url="https://x.com/archetype_jobmarket/status/13",
    niche="Job Market",
    fmt="Data Drop",
    why="Specific salary anchors the claim in reality. 'Almost no candidates' creates scarcity framing that makes people forward this to friends considering a career pivot.",
    engagement=11200,
    hook="Data surprise"
)

push(
    text="You don't need to know how to code to build AI agents.\n\nYou need to know how businesses actually work.\n\nThat's the rarer skill.",
    author="@archetype_jobmarket",
    url="https://x.com/archetype_jobmarket/status/14",
    niche="Job Market,AI Agents,Personal Brand",
    fmt="Hot Take",
    why="Directly challenges the 'you need to code' barrier that stops most people. Highly shareable by non-technical people who want validation. Drives replies from both sides.",
    engagement=15800,
    hook="Contrarian claim"
)

# ── PERSONAL BRAND ───────────────────────────────────────────────────────────

push(
    text="The best portfolio piece isn't on GitHub.\n\nIt's a real client, real problem, real result.\n\nEveryone has code. Almost nobody has proof.",
    author="@archetype_brand",
    url="https://x.com/archetype_brand/status/15",
    niche="Personal Brand",
    fmt="Hot Take",
    why="Attacks the dominant advice (GitHub portfolio) with a clear alternative. 'Proof' is a powerful word. Makes developers defensive and non-developers feel validated.",
    engagement=8300,
    hook="Contrarian claim"
)

push(
    text="I shipped a client dashboard in 3 weeks.\n\nIt wasn't perfect.\n\nBut it was working, and they were paying.\n\nDone beats perfect every time.",
    author="@archetype_brand",
    url="https://x.com/archetype_brand/status/16",
    niche="Personal Brand,AI Consulting",
    fmt="Story",
    why="Vulnerable admission (wasn't perfect) followed by business validation (paying). Line-by-line reveal keeps eyes moving down the post. Classic 'done beats perfect' resonates universally.",
    engagement=6400,
    hook="Personal story"
)

push(
    text="Building in public is not a strategy.\n\nBuilding in public with something people actually want to see is a strategy.\n\nKnow the difference.",
    author="@archetype_brand",
    url="https://x.com/archetype_brand/status/17",
    niche="Personal Brand",
    fmt="Contrarian",
    why="Validates the concept before nuancing it — avoids being dismissive. The reframe is specific enough to be actionable. Drives replies from people explaining what they're building.",
    engagement=4900,
    hook="Contrarian claim"
)

print("\n✅ Seed complete.")
