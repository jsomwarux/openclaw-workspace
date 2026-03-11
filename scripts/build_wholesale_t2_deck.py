#!/usr/bin/env python3
"""
build_wholesale_t2_deck.py — Build a T2 wholesale distribution proposal deck.

Uses the upgraded presentation agent principles:
  - Declarative headlines (statements, not labels)
  - Emotional arc: Recognition → Stakes → Hope → Proof → Inevitability → Action
  - 28pt+ body text, max 5 lines per slide, one idea per slide
  - Large accent stats as visual anchors

Usage:
  # Build master template (placeholder values)
  python3 build_wholesale_t2_deck.py --master

  # Build for a specific prospect (reads demo-results.json automatically)
  python3 build_wholesale_t2_deck.py --slug brothers-supply --company "Brothers Supply Corp" \
    --sku-count 12 --supplier-count 3 --category "HVAC/Plumbing"

  # Build from brief.json + demo-results.json
  python3 build_wholesale_t2_deck.py --brief ~/projects/jt-consulting-pipeline/clients/[slug]/brief.json \
    --demo-results ~/projects/jt-consulting-pipeline/clients/[slug]/demo-results.json
"""

import json
import os
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

def s1_cover(sid, n, company, category):
    """Cover — Emotional target: Intrigue + Credibility"""
    return (sid, COLORS["bg"], [
        # Company name — the prospect sees their own name first
        slide_text(f"s{n}_company", company,
                   x=M, y=115, w=610, h=58,
                   color="white", size=38, bold=True),
        # Accent bar under company name
        slide_rect(f"s{n}_bar", x=M, y=176, w=120, h=4),
        # What was built
        slide_text(f"s{n}_sub", f"AI Inventory Intelligence — {category}",
                   x=M, y=188, w=610, h=42,
                   color="accent", size=26),
        # Byline
        slide_text(f"s{n}_by", "JT Somwaru Consulting",
                   x=M, y=238, w=300, h=26,
                   color="muted", size=15),
    ])


def s2_recognition(sid, n, company, sku_count, supplier_count):
    """Recognition — Emotional target: 'That's exactly my problem'"""
    bullets = (
        f"• {sku_count} SKUs across {supplier_count} suppliers — tracked manually\n\n"
        "• Stockouts surface when a customer is already on the phone\n\n"
        "• Reorder calls go out when someone remembers, not when stock requires it"
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   "You know which SKUs are running low.\nYou find out too late.",
                   x=M, y=28, w=610, h=78,
                   color="white", size=30, bold=True),
        accent_bar(n, x=M, y=110, w=90),
        slide_text(f"s{n}_body", bullets,
                   x=M, y=124, w=610, h=230,
                   color="light_gray", size=24),
    ])


def s3_stakes(sid, n, sku_count, supplier_count, hours_per_week, po_value_estimate):
    """Stakes — Emotional target: Fear/Urgency"""
    body = (
        f"Every reorder is a manual decision: check the count, call the supplier,\n"
        f"follow up on lead time. {sku_count} SKUs × {supplier_count} suppliers\n"
        f"= hours your team spends every week that don't grow the business."
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"{sku_count} SKUs. {supplier_count} Suppliers.\nAll tracked by hand.",
                   x=M, y=28, w=610, h=78,
                   color="white", size=30, bold=True),
        accent_bar(n, x=M, y=110, w=90),
        # Big stat
        slide_text(f"s{n}_stat", f"{hours_per_week} HRS/WEEK",
                   x=M, y=125, w=280, h=52,
                   color="accent", size=34, bold=True),
        slide_text(f"s{n}_stat_sub", "on manual reorder work",
                   x=M, y=178, w=280, h=28,
                   color="muted", size=16),
        slide_text(f"s{n}_stat2", f"${po_value_estimate:,}+",
                   x=360, y=125, w=300, h=52,
                   color="accent", size=34, bold=True),
        slide_text(f"s{n}_stat2_sub", "in POs placed reactively, not predictively",
                   x=360, y=178, w=300, h=28,
                   color="muted", size=16),
        slide_text(f"s{n}_body", body,
                   x=M, y=220, w=610, h=140,
                   color="light_gray", size=22),
    ])


def s4_demo(sid, n, company, category):
    """The Demo Hook — Emotional target: Surprise"""
    body = (
        f"We loaded {company}'s product catalog into the system\n"
        f"and ran a live inventory check.\n\n"
        "Here's what it flagged."
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"We built this for {company}.",
                   x=M, y=28, w=610, h=58,
                   color="white", size=34, bold=True),
        accent_bar(n, x=M, y=90, w=90),
        slide_text(f"s{n}_body", body,
                   x=M, y=108, w=610, h=165,
                   color="light_gray", size=28),
        # Demo label
        slide_text(f"s{n}_label", f"LIVE DEMO  ↓  {category.upper()} INVENTORY CHECK",
                   x=M, y=290, w=610, h=30,
                   color="accent", size=14),
        # Demo output box background
        slide_rect(f"s{n}_box", x=M, y=320, w=610, h=65,
                   fill="dark_card"),
        slide_text(f"s{n}_output",
                   "[ Demo output shown here — see next slide ]",
                   x=70, y=328, w=590, h=50,
                   color="muted", size=18),
    ])


def s4_demo_with_output(sid, n, company, category, wow_output, latency_ms):
    """The Demo Hook with real output — replaces s4_demo when demo-results.json is available."""
    # Truncate output for slide display
    short_output = wow_output[:220] + "..." if len(wow_output) > 220 else wow_output
    latency_sec = f"{latency_ms/1000:.1f}s" if latency_ms else "< 5s"

    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"We built this for {company}.",
                   x=M, y=28, w=610, h=58,
                   color="white", size=34, bold=True),
        accent_bar(n, x=M, y=90, w=90),
        # Demo label
        slide_text(f"s{n}_label",
                   f"LIVE RUN — {category.upper()} INVENTORY  ·  Response: {latency_sec}",
                   x=M, y=106, w=610, h=26,
                   color="accent", size=13),
        # Output box
        slide_rect(f"s{n}_box", x=M, y=134, w=610, h=220, fill="dark_card"),
        slide_text(f"s{n}_output", short_output,
                   x=65, y=142, w=590, h=205,
                   color="light_gray", size=16),
    ])


def s5_results(sid, n, reorder_count, critical_count, total_po_value, supplier_count):
    """Results — Emotional target: Credibility/Proof"""
    body = (
        f"In one automated check: {reorder_count} items flagged for reorder,\n"
        f"{critical_count} marked critical. Purchase orders generated\n"
        f"for {supplier_count} suppliers automatically — no manual counts,\n"
        f"no phone calls, no guessing."
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   f"{reorder_count} items flagged. ${total_po_value:,.0f} in POs.\nGenerated in seconds.",
                   x=M, y=28, w=610, h=78,
                   color="white", size=30, bold=True),
        accent_bar(n, x=M, y=110, w=90),
        # Stats row
        slide_text(f"s{n}_s1", str(reorder_count),
                   x=M, y=128, w=130, h=55,
                   color="accent", size=42, bold=True),
        slide_text(f"s{n}_s1l", "items to reorder",
                   x=M, y=183, w=130, h=26,
                   color="muted", size=14),
        slide_text(f"s{n}_s2", str(critical_count),
                   x=220, y=128, w=130, h=55,
                   color="red", size=42, bold=True),
        slide_text(f"s{n}_s2l", "critical — act now",
                   x=220, y=183, w=130, h=26,
                   color="muted", size=14),
        slide_text(f"s{n}_s3", f"${total_po_value:,.0f}",
                   x=390, y=128, w=270, h=55,
                   color="green", size=42, bold=True),
        slide_text(f"s{n}_s3l", "in POs auto-generated",
                   x=390, y=183, w=270, h=26,
                   color="muted", size=14),
        slide_text(f"s{n}_body", body,
                   x=M, y=222, w=610, h=148,
                   color="light_gray", size=22),
    ])


def s6_inevitability(sid, n, hours_per_week, time_saved_pct=85):
    """Inevitability — Emotional target: Forward momentum / FOMO"""
    body = (
        f"With this running, your team recaptures {hours_per_week} hours a week.\n\n"
        "Reorders go out before customers notice the stockout.\n\n"
        "You stop reacting. The system handles it."
    )
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   "This is what your inventory\nlooks like in 30 days.",
                   x=M, y=28, w=610, h=78,
                   color="white", size=30, bold=True),
        accent_bar(n, x=M, y=110, w=90),
        slide_text(f"s{n}_stat", f"{time_saved_pct}%",
                   x=M, y=125, w=220, h=60,
                   color="accent", size=48, bold=True),
        slide_text(f"s{n}_stat_sub", "of reorder work\neliminated",
                   x=M, y=188, w=220, h=40,
                   color="muted", size=16),
        slide_text(f"s{n}_body", body,
                   x=295, y=125, w=370, h=205,
                   color="light_gray", size=24),
    ])


def s7_cta(sid, n):
    """CTA — Emotional target: Easy yes"""
    return (sid, COLORS["bg"], [
        slide_text(f"s{n}_headline",
                   "30 minutes to see it\nwith your live data.",
                   x=M, y=60, w=610, h=90,
                   color="white", size=36, bold=True),
        accent_bar(n, x=M, y=155, w=90),
        slide_text(f"s{n}_sub",
                   "No commitment. No setup on your end.\nWe walk through it together.",
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
    category,
    sku_count,
    supplier_count,
    hours_per_week,
    po_value_estimate,
    reorder_count=None,
    critical_count=None,
    total_po_value=None,
    wow_output=None,
    latency_ms=None,
    is_master=False,
):
    # Defaults for master template
    if reorder_count is None: reorder_count = 7
    if critical_count is None: critical_count = 2
    if total_po_value is None: total_po_value = po_value_estimate
    has_demo_output = wow_output is not None

    slides = [
        s1_cover("slide_1", 1, company, category),
        s2_recognition("slide_2", 2, company, sku_count, supplier_count),
        s3_stakes("slide_3", 3, sku_count, supplier_count, hours_per_week, po_value_estimate),
    ]

    # Slide 4: demo hook — use real output if available, placeholder if not
    if has_demo_output:
        slides.append(s4_demo_with_output("slide_4", 4, company, category, wow_output, latency_ms))
    else:
        slides.append(s4_demo("slide_4", 4, company, category))

    slides += [
        s5_results("slide_5", 5, reorder_count, critical_count, total_po_value, supplier_count),
        s6_inevitability("slide_6", 6, hours_per_week),
        s7_cta("slide_7", 7),
    ]

    folder = "Eve — Drafts/JT Somwaru/Templates" if is_master else "Eve — Drafts/JT Somwaru/Case Studies"
    title  = f"[MASTER] Wholesale Distribution T2 — JT Somwaru Consulting" if is_master else \
             f"{company} — JT Somwaru Consulting Proposal"

    return create_deck(
        title=title,
        client_slug=slug,
        slides=slides,
        drive_folder=folder,
    )


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build T2 wholesale proposal deck")
    parser.add_argument("--master", action="store_true",
                        help="Build master template with placeholder values")
    parser.add_argument("--slug",    default="wholesale-t2-master")
    parser.add_argument("--company", default="[COMPANY_NAME]")
    parser.add_argument("--category", default="Wholesale Distribution")
    parser.add_argument("--sku-count", type=int, default=12)
    parser.add_argument("--supplier-count", type=int, default=3)
    parser.add_argument("--hours-per-week", type=int, default=8)
    parser.add_argument("--po-value-estimate", type=int, default=4200)
    parser.add_argument("--brief",        help="Path to brief.json")
    parser.add_argument("--demo-results", help="Path to demo-results.json")
    args = parser.parse_args()

    # Override from brief.json if provided
    if args.brief:
        with open(args.brief) as f:
            brief = json.load(f)
        args.slug    = brief.get("slug", args.slug)
        args.company = brief.get("company", args.company)
        if "research" in brief:
            r = brief["research"]
            args.sku_count      = r.get("sku_count", args.sku_count)
            args.supplier_count = r.get("supplier_count", args.supplier_count)

    # Pull wow case from demo-results.json if provided
    wow_output = None
    latency_ms = None
    reorder_count = None
    critical_count = None
    total_po_value = None

    if args.demo_results:
        with open(args.demo_results) as f:
            dr = json.load(f)
        for test in dr.get("tests", []):
            if test.get("notes", {}).get("wow_case") or "wow" in str(test.get("notes", "")).lower():
                wow_output = test.get("actual_output", "")
                latency_ms = test.get("latency_ms")
                break
        # Pull summary stats from the first test's output if they exist
        summary = dr.get("summary", {})
        reorder_count  = summary.get("reorder_count")
        critical_count = summary.get("critical_count")
        total_po_value = summary.get("total_po_value")

    url = build_deck(
        company          = args.company,
        slug             = args.slug,
        category         = args.category,
        sku_count        = getattr(args, "sku_count", 12),
        supplier_count   = getattr(args, "supplier_count", 3),
        hours_per_week   = getattr(args, "hours_per_week", 8),
        po_value_estimate= getattr(args, "po_value_estimate", 4200),
        reorder_count    = reorder_count,
        critical_count   = critical_count,
        total_po_value   = total_po_value,
        wow_output       = wow_output,
        latency_ms       = latency_ms,
        is_master        = args.master,
    )

    print(f"\nDeck URL: {url}")
    return url


if __name__ == "__main__":
    main()
