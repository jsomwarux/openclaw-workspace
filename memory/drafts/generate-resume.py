#!/usr/bin/env python3
"""
JT Somwaru — Resume Generator
Generates a clean, ATS-friendly PDF resume optimized for AI Implementation / Solutions Architect roles.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT = os.path.expanduser("~/.openclaw/workspace/memory/drafts/jt-somwaru-resume.pdf")

# ── Colors ─────────────────────────────────────────────────────────────────────
CHARCOAL     = HexColor("#1a1a2e")
TEAL         = HexColor("#0d7377")
TEAL_LIGHT   = HexColor("#14a085")
MID_GRAY     = HexColor("#555555")
LIGHT_GRAY   = HexColor("#888888")
RULE_COLOR   = HexColor("#d0d5dd")
BG_TAG       = HexColor("#f0f8f7")

# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=0.65*inch,
    rightMargin=0.65*inch,
    topMargin=0.55*inch,
    bottomMargin=0.55*inch,
)

W = letter[0] - 1.3*inch  # usable width

# ── Styles ─────────────────────────────────────────────────────────────────────
S = {}

S["name"] = ParagraphStyle("name",
    fontName="Helvetica-Bold", fontSize=24, textColor=CHARCOAL,
    spaceAfter=2, leading=28)

S["title"] = ParagraphStyle("title",
    fontName="Helvetica", fontSize=12, textColor=TEAL,
    spaceAfter=4, leading=15)

S["contact"] = ParagraphStyle("contact",
    fontName="Helvetica", fontSize=9, textColor=MID_GRAY,
    spaceAfter=0, leading=12)

S["section"] = ParagraphStyle("section",
    fontName="Helvetica-Bold", fontSize=10.5, textColor=TEAL,
    spaceBefore=10, spaceAfter=3, leading=14, textTransform="uppercase",
    letterSpacing=0.8)

S["summary"] = ParagraphStyle("summary",
    fontName="Helvetica", fontSize=9.5, textColor=MID_GRAY,
    spaceAfter=0, leading=14)

S["job_title"] = ParagraphStyle("job_title",
    fontName="Helvetica-Bold", fontSize=10, textColor=CHARCOAL,
    spaceBefore=7, spaceAfter=1, leading=13)

S["job_meta"] = ParagraphStyle("job_meta",
    fontName="Helvetica-Oblique", fontSize=9, textColor=LIGHT_GRAY,
    spaceAfter=3, leading=12)

S["bullet"] = ParagraphStyle("bullet",
    fontName="Helvetica", fontSize=9.2, textColor=MID_GRAY,
    leftIndent=12, firstLineIndent=-12, spaceAfter=2.5, leading=13.5,
    bulletText="•")

S["bullet_bold"] = ParagraphStyle("bullet_bold",
    fontName="Helvetica-Bold", fontSize=9.2, textColor=CHARCOAL,
    leftIndent=12, firstLineIndent=-12, spaceAfter=2.5, leading=13.5,
    bulletText="•")

S["skills_label"] = ParagraphStyle("skills_label",
    fontName="Helvetica-Bold", fontSize=9.2, textColor=CHARCOAL,
    spaceAfter=1, leading=13)

S["skills_val"] = ParagraphStyle("skills_val",
    fontName="Helvetica", fontSize=9.2, textColor=MID_GRAY,
    spaceAfter=4, leading=13)

S["tag_row"] = ParagraphStyle("tag_row",
    fontName="Helvetica", fontSize=8.8, textColor=MID_GRAY,
    spaceAfter=0, leading=13)

def rule():
    return HRFlowable(width="100%", thickness=0.6, color=RULE_COLOR, spaceAfter=4, spaceBefore=2)

def section(title):
    return [Paragraph(title, S["section"]), rule()]

def bullet(text, bold=False):
    style = S["bullet_bold"] if bold else S["bullet"]
    return Paragraph(f"• {text}", style)

def job(title, company_date, bullets):
    items = [
        Paragraph(title, S["job_title"]),
        Paragraph(company_date, S["job_meta"]),
    ]
    for b in bullets:
        items.append(bullet(b))
    return items

# ── Content ────────────────────────────────────────────────────────────────────
story = []

# ── HEADER ─────────────────────────────────────────────────────────────────────
story.append(Paragraph("JT Somwaru", S["name"]))
story.append(Paragraph("AI Implementation Lead &amp; Automation Architect", S["title"]))
story.append(Paragraph(
    "New York, NY &nbsp;·&nbsp; jsomwarux@yahoo.com &nbsp;·&nbsp; "
    "linkedin.com/in/jtsomwaru &nbsp;·&nbsp; github.com/jsomwarux",
    S["contact"]
))
story.append(Spacer(1, 8))
story.append(rule())

# ── SUMMARY ────────────────────────────────────────────────────────────────────
story += section("Professional Summary")
story.append(Paragraph(
    "Business Systems Analyst with 6 years at Spectrum Enterprise / Charter Communications, "
    "now designing and deploying AI automation systems through Opticfy. "
    "Bridges the gap between business operations and agentic AI — configuring Salesforce Agentforce, "
    "building multi-agent orchestration pipelines, and shipping production AI tools via AI-directed development. "
    "Rare profile: deep enterprise BSA experience combined with hands-on AI agent orchestration, "
    "responsible AI practices, and a track record of building and delivering working AI systems.",
    S["summary"]
))
story.append(Spacer(1, 6))

# ── CORE COMPETENCIES ──────────────────────────────────────────────────────────
story += section("Core Competencies")
tags = (
    "Multi-Agent Orchestration  ·  Salesforce Agentforce  ·  n8n Workflow Automation  ·  "
    "AI Systems Architecture  ·  Business Systems Analysis  ·  Responsible AI Practices  ·  "
    "LLM Integration (Claude · GPT · Gemini · Grok)  ·  Prompt Engineering  ·  "
    "RAG Pipeline Design  ·  AI-Directed Development  ·  Stakeholder Management  ·  "
    "Requirements Gathering &amp; Specification"
)
story.append(Paragraph(tags, S["tag_row"]))
story.append(Spacer(1, 6))

# ── EXPERIENCE ─────────────────────────────────────────────────────────────────
story += section("Professional Experience")

story += job(
    "Founder &amp; AI Automation Consultant",
    "Opticfy  ·  New York, NY  ·  2025 – Present",
    [
        "<b>Designed a 4-stage multi-agent delivery pipeline</b> — Research Agent → n8n Workflow Builder → "
        "Presentation Agent → Production Builder — standardizing AI consulting handoffs from prospect "
        "research through production deployment.",
        "Delivered construction progress tracking dashboard for Aya ($1,500 engagement) — automated "
        "field input collection, AI-powered status summarization, and stakeholder reporting pipeline.",
        "Built and operate a <b>10-agent autonomous operations stack</b>: market intelligence monitors, "
        "job market scanners, crypto portfolio analysis with game-theoretic scoring, health tracking, "
        "and automated backup systems — demonstrating AI infrastructure design at production scale.",
        "Developed <b>4-LLM cross-validation ensemble methodology</b> (Claude + GPT + Gemini + Grok) "
        "for high-confidence AI analysis, deployed in Nash Satoshi rankings platform.",
        "Implemented responsible AI practices across all deployments: human oversight checkpoints, "
        "automated confidence scoring, decision logging, and AI explainability reporting.",
        "Shipped iOS app (Vista — movie taste profiles) and web platform (Glow Index — skincare rankings) "
        "via AI-directed development using Claude Code and specialized coding agents.",
    ]
)

story += job(
    "Business Systems Analyst",
    "Spectrum Enterprise / Charter Communications  ·  New York, NY  ·  2019 – 2025",
    [
        "Led product catalog configuration and system implementations across Salesforce and enterprise "
        "platforms for a Fortune 100 telecom serving enterprise clients.",
        "Translated complex business requirements into technical specifications for cross-functional "
        "engineering, product, and operations teams — serving as the primary business-to-technology bridge.",
        "Coordinated multi-stakeholder implementation projects end-to-end: requirements gathering, "
        "scoping, configuration, QA, deployment, and ongoing iteration.",
        "Managed ongoing system configuration and quality assurance for enterprise-grade production "
        "systems with direct impact on revenue-generating product catalog.",
        "Established credibility across both business operations (stakeholder language) and technical "
        "implementation (specification depth) — the foundation of the Opticfy consulting model.",
    ]
)

# ── SALESFORCE / AGENTFORCE ────────────────────────────────────────────────────
story += section("Salesforce Agentforce Deployments")

story += job(
    "Employee Assistant — Internal Agentforce Agent",
    "InternalCopilot  ·  3 Topics · 7 Actions  ·  2025",
    [
        "Configured full Agentforce agent in Agent Builder UI: topic definitions, action mappings, "
        "channel configuration, and GenAiPlanner orchestration.",
        "Designed conversational flows for internal workforce automation — routing, lookup, and "
        "self-service capabilities across HR and operations use cases.",
    ]
)

story += job(
    "Ecommerce Service Agent — Customer-Facing Agentforce Agent",
    "ExternalCopilot  ·  2025",
    [
        "Deployed external-facing Agentforce agent for customer service automation — "
        "order management, product inquiry, and escalation routing.",
        "Managed full deployment lifecycle via SFDX-directed process, Salesforce Flows integration, "
        "and Agent Builder configuration.",
    ]
)

# ── AI PROJECTS ────────────────────────────────────────────────────────────────
story += section("AI Products &amp; Systems")

projects = [
    ("<b>Nash Satoshi</b> — Crypto Game Theory Rankings Platform",
     "4-LLM cross-validation ensemble (Claude, GPT, Gemini, Grok) producing consensus game-theoretic "
     "token analysis. Leaderboard + individual scorecards. Methodology expandable to skincare, "
     "consumer products, college, and neighborhood rankings."),
    ("<b>Mission Control</b> — AI Operations Dashboard",
     "Always-on Next.js + Convex dashboard for agent monitoring, task management (Kanban), cost tracking, "
     "and deployment audit trail. Runs via launchd agents — zero manual restarts required."),
    ("<b>Vista</b> — iOS Movie Rating &amp; Taste Profile App",
     "AI-directed iOS app with taste profiling, performer rankings, and 30-day trending analysis. "
     "Pending App Store review."),
    ("<b>Glow Index</b> — Skincare Rankings Platform",
     "Consumer product rankings platform using structured AI analysis. Deployed and live."),
]

for title, desc in projects:
    story.append(Paragraph(title, S["job_title"]))
    story.append(Paragraph(desc, S["summary"]))
    story.append(Spacer(1, 4))

# ── SKILLS ────────────────────────────────────────────────────────────────────
story += section("Technical Skills")

skills = [
    ("AI Agents &amp; Orchestration",
     "Salesforce Agentforce, n8n (4-LLM ensemble patterns), multi-agent pipeline design, "
     "RAG pipeline architecture, prompt engineering (advanced — XML tagging, multi-shot, chain-of-thought)"),
    ("LLM APIs",
     "Anthropic Claude (4.6), OpenAI GPT, Google Gemini, xAI Grok — integration, chaining, "
     "ensemble cross-validation"),
    ("Development",
     "Python (automation, data processing, API scripting), TypeScript/JavaScript (AI-directed), "
     "Git / GitHub, Next.js, SQLite"),
    ("Salesforce",
     "Agentforce Agent Builder, Salesforce Flows, data model (Account, Contact, Case, Opportunity, Order), "
     "SFDX-directed deployment"),
    ("Tools &amp; Platforms",
     "Claude Code, Firecrawl, Brave Search API, Dexscreener API, Google Drive API, Convex, "
     "LaunchAgents (macOS automation)"),
    ("Methodologies",
     "AI-directed development, responsible AI practices, business process automation, "
     "multi-stakeholder implementation, requirements specification"),
]

for label, val in skills:
    story.append(Paragraph(label, S["skills_label"]))
    story.append(Paragraph(val, S["skills_val"]))

# ── BUILD ──────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"✅ Resume written to: {OUTPUT}")
