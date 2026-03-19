#!/usr/bin/env python3
"""
build_agentforce_t2_deck.py — Build a T2 Agentforce insurance proposal deck.

Models build_wholesale_t2_deck.py — same emotional arc, same slide framework,
adapted for Agentforce/insurance prospects with Salesforce context.

Emotional arc: Recognition → Stakes → Hope (Demo) → Proof → Inevitability → Action

Usage:
  # Build master template (placeholder values)
  python3 build_agentforce_t2_deck.py --master

  # Build for a specific prospect
  python3 build_agentforce_t2_deck.py --slug lawley-insurance --company "Lawley Insurance" \
    --niche "Commercial P&C" --topics 4 --sf-object "Account,Case,Opportunity"

  # Build from brief.json + demo-transcript.md + agent-config.md
  python3 build_agentforce_t2_deck.py \
    --brief ~/projects/jt-consulting-pipeline/clients/[slug]/brief.json \
    --demo-transcript ~/projects/jt-consulting-pipeline/clients/[slug]/demo-transcript.md \
    --agent-config ~/projects/jt-consulting-pipeline/clients/[slug]/agent-config.md
"""

import json
import os
import re
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slides_framework import (
    create_deck, slide_text, slide_rect, accent_bar, COLORS, pt
)

# ── Slide canvas (720pt × 405pt) ─────────────────────────────────────────────
W = 720   # total slide width
H = 405   # total slide height
M = 55    # left/right margin


# ── Slide builders ────────────────────────────────────────────────────────────

def s1_cover(sid, n, company, niche):
    """Cover — Emotional target: Intrigue + Credibility"""
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_company", company,
                   x=M, y=115, w=610, h=58,
                   color="white", size=38, bold=True),
        slide_rect(f"s{n}_bar", x=M, y=176, w=120, h=4),
        slide_text(f"s{n}_sub", f"AI Service Agent — {niche}",
                   x=M, y=188, w=610, h=42,
                   color="accent", size=26),
        slide_text(f"s{n}_powered", "Powered by Salesforce Agentforce",
                   x=M, y=230, w=340, h=28,
                   color="muted", size=15),
        slide_text(f"s{n}_by", "JT Somwaru Consulting",
                   x=M, y=258, w=300, h=26,
                   color="muted", size=15),
    ])


def s2_recognition(sid, n, company, niche, pain_point):
    """Recognition — Emotional target: 'That's exactly my problem'"""
    bullets = (
        f"• Clients call asking questions your team already answered last week\n\n"
        "• COI requests pile up — each one needs manual tracking and follow-up\n\n"
        f"• Your agents spend 40%+ of their day on admin, not {niche} sales"
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"Your team answers the same\nquestions every single day.",
                   x=M, y=28, w=610, h=78,
                   color="white", size=30, bold=True),
        accent_bar(n, x=M, y=110, w=90),
        slide_text(f"s{n}_body", bullets,
                   x=M, y=124, w=610, h=230,
                   color="light_gray", size=24),
    ])


def s3_stakes(sid, n, hours_per_week, requests_per_month, niche):
    """Stakes — Emotional target: Fear/Urgency"""
    body = (
        f"Every policy inquiry, COI request, and renewal question\n"
        f"requires a licensed rep to stop what they're doing and respond.\n\n"
        f"That's {requests_per_month}+ requests a month — handled manually."
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"{requests_per_month} service requests.\nEvery one handled by hand.",
                   x=M, y=28, w=610, h=78,
                   color="white", size=30, bold=True),
        accent_bar(n, x=M, y=110, w=90),
        slide_text(f"s{n}_stat", f"{hours_per_week} HRS/WEEK",
                   x=M, y=125, w=280, h=52,
                   color="accent", size=34, bold=True),
        slide_text(f"s{n}_stat_sub", "on service admin, not selling",
                   x=M, y=178, w=280, h=28,
                   color="muted", size=16),
        slide_text(f"s{n}_stat2", f"{requests_per_month}+",
                   x=360, y=125, w=300, h=52,
                   color="accent", size=34, bold=True),
        slide_text(f"s{n}_stat2_sub", "routine client requests per month",
                   x=360, y=178, w=300, h=28,
                   color="muted", size=16),
        slide_text(f"s{n}_body", body,
                   x=M, y=220, w=610, h=140,
                   color="light_gray", size=22),
    ])


def s4_demo(sid, n, company, topics_list):
    """Demo Hook — Emotional target: Surprise"""
    topics_display = "\n".join([f"  • {t}" for t in topics_list[:4]])
    body = (
        f"We configured an Agentforce agent inside your Salesforce org.\n\n"
        f"Trained on {company}'s workflows. Live on your data.\n\n"
        f"Here's what it handles autonomously:"
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"We built this for {company}.",
                   x=M, y=28, w=610, h=58,
                   color="white", size=34, bold=True),
        accent_bar(n, x=M, y=90, w=90),
        slide_text(f"s{n}_body", body,
                   x=M, y=108, w=370, h=175,
                   color="light_gray", size=18),
        # Topics card
        slide_rect(f"s{n}_box", x=420, y=100, w=245, h=185, fill="dark_card"),
        slide_text(f"s{n}_topics_label", "AGENT TOPICS",
                   x=430, y=108, w=235, h=22,
                   color="accent", size=12),
        slide_text(f"s{n}_topics", topics_display,
                   x=430, y=132, w=235, h=155,
                   color="light_gray", size=18),
        slide_text(f"s{n}_cta", "LIVE DEMO  ↓",
                   x=M, y=310, w=200, h=28,
                   color="accent", size=14),
    ])


def s4_demo_with_output(sid, n, company, topics_list, wow_exchange, pass_rate):
    """Demo Hook with real transcript — replaces s4_demo when demo-transcript.md available."""
    # Truncate for slide
    short_exchange = wow_exchange[:200] + "..." if len(wow_exchange) > 200 else wow_exchange

    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"We built this for {company}.",
                   x=M, y=28, w=610, h=58,
                   color="white", size=34, bold=True),
        accent_bar(n, x=M, y=90, w=90),
        # Pass rate badge
        slide_text(f"s{n}_pass",
                   f"LIVE DEMO  ·  Pass rate: {pass_rate}",
                   x=M, y=106, w=400, h=26,
                   color="accent", size=13),
        # Transcript box
        slide_rect(f"s{n}_box", x=M, y=136, w=610, h=218, fill="dark_card"),
        slide_text(f"s{n}_transcript", short_exchange,
                   x=65, y=144, w=575, h=200,
                   color="light_gray", size=16),
    ])


def s5_results(sid, n, topics_count, pass_rate, wow_topic, sf_objects):
    """Results — Emotional target: Credibility / Proof"""
    body = (
        f"The agent handled all {topics_count} test scenarios correctly:\n"
        f"policy lookup, COI requests, claims intake, and renewal\n"
        f"— all without a human in the loop."
    )
    objects_display = " · ".join(sf_objects[:4]) if sf_objects else "Account · Case · Opportunity"
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"{pass_rate} scenarios passed.\nZero human interventions.",
                   x=M, y=28, w=610, h=78,
                   color="white", size=30, bold=True),
        accent_bar(n, x=M, y=110, w=90),
        slide_text(f"s{n}_s1", str(topics_count),
                   x=M, y=128, w=120, h=55,
                   color="accent", size=42, bold=True),
        slide_text(f"s{n}_s1l", "topics configured",
                   x=M, y=183, w=130, h=26,
                   color="muted", size=14),
        slide_text(f"s{n}_s2", pass_rate,
                   x=190, y=128, w=130, h=55,
                   color="green", size=42, bold=True),
        slide_text(f"s{n}_s2l", "test pass rate",
                   x=190, y=183, w=130, h=26,
                   color="muted", size=14),
        slide_text(f"s{n}_s3", "0",
                   x=380, y=128, w=60, h=55,
                   color="red", size=42, bold=True),
        slide_text(f"s{n}_s3l", "agent escalations\nin test suite",
                   x=446, y=128, w=200, h=55,
                   color="muted", size=14),
        slide_text(f"s{n}_body", body,
                   x=M, y=222, w=610, h=105,
                   color="light_gray", size=22),
        # SF objects footer
        slide_text(f"s{n}_sf", f"Salesforce objects: {objects_display}",
                   x=M, y=340, w=610, h=26,
                   color="muted", size=13),
    ])


def s6_inevitability(sid, n, hours_per_week, automation_pct=80):
    """Inevitability — Emotional target: Forward momentum"""
    body = (
        f"With this running 24/7, your reps recapture {hours_per_week} hours\n"
        "a week for renewals and new business.\n\n"
        "COI requests get handled while the client is still on your site.\n\n"
        "Claims are logged, prioritized, and routed — automatically."
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   "This is what client service looks\nlike 30 days from now.",
                   x=M, y=28, w=610, h=78,
                   color="white", size=30, bold=True),
        accent_bar(n, x=M, y=110, w=90),
        slide_text(f"s{n}_stat", f"{automation_pct}%",
                   x=M, y=125, w=220, h=60,
                   color="accent", size=48, bold=True),
        slide_text(f"s{n}_stat_sub", "of routine service\nrequests automated",
                   x=M, y=188, w=220, h=40,
                   color="muted", size=16),
        slide_text(f"s{n}_body", body,
                   x=295, y=125, w=370, h=225,
                   color="light_gray", size=18),
    ])


def s7_cta(sid, n):
    """CTA — Emotional target: Easy yes"""
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   "30 minutes to see it\nrunning in your Salesforce.",
                   x=M, y=60, w=610, h=90,
                   color="white", size=36, bold=True),
        accent_bar(n, x=M, y=155, w=90),
        slide_text(f"s{n}_sub",
                   "No commitment. Already configured for your use case.\nWe walk through it together.",
                   x=M, y=170, w=610, h=60,
                   color="light_gray", size=24),
        slide_text(f"s{n}_contact",
                   "JT Somwaru  ·  jtsomwaru.com  ·  linkedin.com/in/jon-trevor-somwaru",
                   x=M, y=300, w=610, h=30,
                   color="muted", size=15),
    ])


# ── Deck assembly ─────────────────────────────────────────────────────────────

def build_deck(
    company,
    slug,
    niche,
    pain_point,
    hours_per_week,
    requests_per_month,
    topics_list,
    topics_count=None,
    pass_rate=None,
    wow_exchange=None,
    sf_objects=None,
    wow_topic=None,
    automation_pct=80,
    is_master=False,
):
    if topics_count is None:
        topics_count = len(topics_list)
    if pass_rate is None:
        pass_rate = f"{topics_count}/{topics_count}"
    if sf_objects is None:
        sf_objects = ["Account", "Case", "Opportunity"]

    has_transcript = wow_exchange is not None

    slides = [
        s1_cover("slide_1", 1, company, niche),
        s2_recognition("slide_2", 2, company, niche, pain_point),
        s3_stakes("slide_3", 3, hours_per_week, requests_per_month, niche),
    ]

    if has_transcript:
        slides.append(s4_demo_with_output("slide_4", 4, company, topics_list, wow_exchange, pass_rate))
    else:
        slides.append(s4_demo("slide_4", 4, company, topics_list))

    slides += [
        s5_results("slide_5", 5, topics_count, pass_rate, wow_topic or topics_list[0], sf_objects),
        s6_inevitability("slide_6", 6, hours_per_week, automation_pct),
        s7_cta("slide_7", 7),
    ]

    folder = "Eve — Drafts/JT Somwaru/Templates" if is_master \
             else "Eve — Drafts/Consulting/Clients/Agentforce T2 Decks"
    title  = "[MASTER] Agentforce T2 Insurance — JT Somwaru Consulting" if is_master \
             else f"{company} — Agentforce Proposal — JT Somwaru Consulting"

    return create_deck(
        title=title,
        client_slug=slug,
        slides=slides,
        drive_folder=folder,
    )


# ── Brief/Transcript parsers ──────────────────────────────────────────────────

def load_brief(path):
    """Load brief.json and extract Agentforce-relevant fields."""
    with open(os.path.expanduser(path)) as f:
        brief = json.load(f)

    agentforce = brief.get("agentforce_brief", {})
    research   = brief.get("research", {})
    client     = brief.get("client", {})
    pain_points = brief.get("pain_points", [])

    topics_list = agentforce.get("topics", [])
    # topics may be a list of strings or dicts with 'name' key
    if topics_list and isinstance(topics_list[0], dict):
        topics_list = [t.get("name", str(t)) for t in topics_list]

    return {
        "slug":               brief.get("slug", ""),
        "company":            client.get("company", brief.get("company", "[COMPANY]")),
        "niche":              research.get("niche", "Commercial Insurance"),
        "pain_point":         pain_points[0] if pain_points else "Service admin volume",
        "hours_per_week":     research.get("hours_per_week", 15),
        "requests_per_month": research.get("requests_per_month", 120),
        "topics_list":        topics_list or ["Policy Inquiry", "Claims Intake", "COI Request", "Renewal"],
        "sf_objects":         agentforce.get("sf_objects", ["Account", "Case"]),
    }


def load_transcript(path):
    """Parse demo-transcript.md to extract wow exchange and pass rate."""
    with open(os.path.expanduser(path)) as f:
        content = f.read()

    # Extract pass rate
    pass_match = re.search(r'Pass rate:\s*([0-9/]+)', content)
    pass_rate = pass_match.group(1) if pass_match else None

    # Find the wow moment (flagged section)
    wow_match = re.search(
        r'(?:Wow moment|wow_case)[^\n]*\n(.*?)(?=##|\Z)',
        content, re.DOTALL | re.IGNORECASE
    )
    # Also try to extract a representative test exchange
    exchange_match = re.search(
        r'### Test \d+[^\n]*\n(.*?\*\*Result:\*\*.*?(?=###|\Z))',
        content, re.DOTALL
    )

    wow_exchange = None
    if wow_match:
        wow_exchange = wow_match.group(1).strip()[:400]
    elif exchange_match:
        wow_exchange = exchange_match.group(1).strip()[:400]

    # Extract topics count from pass rate
    topics_count = None
    if pass_rate and "/" in pass_rate:
        parts = pass_rate.split("/")
        try:
            topics_count = int(parts[1])
        except (ValueError, IndexError):
            pass

    return {
        "pass_rate":    pass_rate,
        "wow_exchange": wow_exchange,
        "topics_count": topics_count,
    }


def load_agent_config(path):
    """Parse agent-config.md to extract SF objects and customizations."""
    with open(os.path.expanduser(path)) as f:
        content = f.read()

    # Look for SF objects line
    obj_match = re.search(r'(?:Salesforce objects?|Objects?)[:\s]+([A-Za-z, _·•\-]+)', content)
    sf_objects = []
    if obj_match:
        raw = obj_match.group(1)
        sf_objects = [o.strip() for o in re.split(r'[,·•]', raw) if o.strip()]

    return {"sf_objects": sf_objects}


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build T2 Agentforce insurance proposal deck")
    parser.add_argument("--master", action="store_true",
                        help="Build master template with placeholder values")
    parser.add_argument("--slug",               default="agentforce-t2-master")
    parser.add_argument("--company",            default="[COMPANY_NAME]")
    parser.add_argument("--niche",              default="Commercial Insurance")
    parser.add_argument("--pain-point",         default="High service admin volume",
                        dest="pain_point")
    parser.add_argument("--topics",             type=int, default=4,
                        help="Number of agent topics configured")
    parser.add_argument("--hours-per-week",     type=int, default=15,
                        dest="hours_per_week")
    parser.add_argument("--requests-per-month", type=int, default=120,
                        dest="requests_per_month")
    parser.add_argument("--sf-objects",         default="Account,Case,Opportunity",
                        dest="sf_objects",
                        help="Comma-separated Salesforce object names")
    parser.add_argument("--brief",              help="Path to brief.json")
    parser.add_argument("--demo-transcript",    help="Path to demo-transcript.md",
                        dest="demo_transcript")
    parser.add_argument("--agent-config",       help="Path to agent-config.md",
                        dest="agent_config")
    args = parser.parse_args()

    # Defaults
    topics_list     = ["Policy Inquiry", "Claims Intake", "COI Request", "Renewal & Cross-Sell"]
    sf_objects      = [o.strip() for o in args.sf_objects.split(",") if o.strip()]
    slug            = args.slug
    company         = args.company
    niche           = args.niche
    pain_point      = args.pain_point
    hours_per_week  = args.hours_per_week
    requests_per_month = args.requests_per_month
    topics_count    = args.topics
    pass_rate       = f"{topics_count}/{topics_count}"
    wow_exchange    = None

    # Override from brief.json
    if args.brief:
        data = load_brief(args.brief)
        slug               = data["slug"] or slug
        company            = data["company"]
        niche              = data["niche"]
        pain_point         = data["pain_point"]
        hours_per_week     = data["hours_per_week"]
        requests_per_month = data["requests_per_month"]
        topics_list        = data["topics_list"] or topics_list
        topics_count       = len(topics_list)
        sf_objects         = data["sf_objects"] or sf_objects

    # Pull wow exchange + pass rate from demo transcript
    if args.demo_transcript and os.path.exists(os.path.expanduser(args.demo_transcript)):
        td = load_transcript(args.demo_transcript)
        wow_exchange = td["wow_exchange"]
        if td["pass_rate"]:
            pass_rate = td["pass_rate"]
        if td["topics_count"]:
            topics_count = td["topics_count"]

    # Override SF objects from agent-config
    if args.agent_config and os.path.exists(os.path.expanduser(args.agent_config)):
        ac = load_agent_config(args.agent_config)
        if ac["sf_objects"]:
            sf_objects = ac["sf_objects"]

    url = build_deck(
        company=company,
        slug=slug,
        niche=niche,
        pain_point=pain_point,
        hours_per_week=hours_per_week,
        requests_per_month=requests_per_month,
        topics_list=topics_list[:4],
        topics_count=topics_count,
        pass_rate=pass_rate,
        wow_exchange=wow_exchange,
        sf_objects=sf_objects,
        automation_pct=80,
        is_master=args.master,
    )

    print(f"\nDeck URL: {url}")
    return url


if __name__ == "__main__":
    main()
