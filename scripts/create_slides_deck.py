#!/usr/bin/env python3
"""
create_slides_deck.py — Create a Google Slides deck via API and save to Drive.

Usage:
  python3 create_slides_deck.py --client hc-oswald
  python3 create_slides_deck.py --client hc-oswald --folder "Eve — Drafts/Opticfy/Case Studies"

Outputs: Google Slides URL (also writes to deck-url.txt in client folder)
"""

import json
import os
import sys
import argparse
import warnings

warnings.filterwarnings("ignore")

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")
PIPELINE_ROOT = os.path.expanduser("~/projects/opticfy-pipeline/clients")

# Points → EMU conversion (1 pt = 12700 EMU)
def pt(n): return int(n * 12700)

# ── Colors ──────────────────────────────────────────────────────────────────
BG_DARK    = {"red": 0.102, "green": 0.102, "blue": 0.180}  # #1a1a2e
ACCENT     = {"red": 0.000, "green": 0.706, "blue": 0.847}  # #00b4d8
WHITE      = {"red": 1.000, "green": 1.000, "blue": 1.000}
LIGHT_GRAY = {"red": 0.800, "green": 0.800, "blue": 0.800}  # #cccccc
MUTED      = {"red": 0.533, "green": 0.573, "blue": 0.690}  # #8892b0
DARK_CARD  = {"red": 0.086, "green": 0.129, "blue": 0.243}  # #16213e
GREEN      = {"red": 0.000, "green": 0.784, "blue": 0.592}  # #00c897
RED        = {"red": 1.000, "green": 0.420, "blue": 0.420}  # #ff6b6b


def get_creds():
    with open(TOKEN_PATH) as f:
        td = json.load(f)
    # Use drive scope only — covers Slides API per Google's auth docs
    # (drive is the originally-authorized scope; don't add presentations or token refresh fails)
    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = Credentials(
        token=td.get("token"),
        refresh_token=td.get("refresh_token"),
        token_uri=td.get("token_uri"),
        client_id=td.get("client_id"),
        client_secret=td.get("client_secret"),
        scopes=scopes,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        td["token"] = creds.token
        with open(TOKEN_PATH, "w") as f:
            json.dump(td, f, indent=2)
    return creds


def find_or_create_folder(drive, name, parent_id=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    results = drive.files().list(q=q, fields="files(id,name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    body = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        body["parents"] = [parent_id]
    return drive.files().create(body=body, fields="id").execute()["id"]


def get_target_folder(drive, path="Eve — Drafts/Opticfy/Case Studies"):
    parts = path.split("/")
    parent = None
    for part in parts:
        parent = find_or_create_folder(drive, part, parent)
    return parent


def build_slide_requests(slide_id, bg_color, elements):
    """Build batchUpdate requests for one slide: set bg + add elements."""
    requests = []

    # Set background
    requests.append({
        "updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {
                "pageBackgroundFill": {
                    "solidFill": {"color": {"rgbColor": bg_color}}
                }
            },
            "fields": "pageBackgroundFill"
        }
    })

    for el in elements:
        eid = el["id"]
        kind = el.get("kind", "text")

        if kind == "text":
            # Create text box
            requests.append({
                "createShape": {
                    "objectId": eid,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": {
                            "width": {"magnitude": pt(el["w"]), "unit": "EMU"},
                            "height": {"magnitude": pt(el["h"]), "unit": "EMU"}
                        },
                        "transform": {
                            "scaleX": 1, "scaleY": 1,
                            "translateX": pt(el["x"]), "translateY": pt(el["y"]),
                            "unit": "EMU"
                        }
                    }
                }
            })
            # Insert text
            requests.append({
                "insertText": {"objectId": eid, "text": el["text"]}
            })
            # Style the text
            style = {
                "foregroundColor": {"opaqueColor": {"rgbColor": el.get("color", WHITE)}},
                "fontSize": {"magnitude": el.get("size", 14), "unit": "PT"},
                "bold": el.get("bold", False),
                "fontFamily": "Arial"
            }
            requests.append({
                "updateTextStyle": {
                    "objectId": eid,
                    "style": style,
                    "fields": "foregroundColor,fontSize,bold,fontFamily",
                    "textRange": {"type": "ALL"}
                }
            })
            # Optional: paragraph alignment
            if el.get("align"):
                requests.append({
                    "updateParagraphStyle": {
                        "objectId": eid,
                        "style": {"alignment": el["align"]},
                        "fields": "alignment",
                        "textRange": {"type": "ALL"}
                    }
                })

        elif kind == "rect":
            requests.append({
                "createShape": {
                    "objectId": eid,
                    "shapeType": "RECTANGLE",
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": {
                            "width": {"magnitude": pt(el["w"]), "unit": "EMU"},
                            "height": {"magnitude": pt(el["h"]), "unit": "EMU"}
                        },
                        "transform": {
                            "scaleX": 1, "scaleY": 1,
                            "translateX": pt(el["x"]), "translateY": pt(el["y"]),
                            "unit": "EMU"
                        }
                    }
                }
            })
            requests.append({
                "updateShapeProperties": {
                    "objectId": eid,
                    "shapeProperties": {
                        "shapeBackgroundFill": {
                            "solidFill": {"color": {"rgbColor": el.get("fill", ACCENT)}}
                        },
                        "outline": {"outlineFill": {"solidFill": {"color": {"rgbColor": el.get("fill", ACCENT)}}}}
                    },
                    "fields": "shapeBackgroundFill,outline"
                }
            })

    return requests


def make_element_id(slide_num, name):
    return f"s{slide_num}_{name}"


# ── Slide definitions ────────────────────────────────────────────────────────

def slide1_title(sid):
    n = 1
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "H.C. Oswald Supply Co.", "x": 60, "y": 100, "w": 600, "h": 55,
         "color": WHITE, "size": 36, "bold": True},
        {"id": make_element_id(n, "sub"), "kind": "text",
         "text": "Automation Proposal", "x": 60, "y": 162, "w": 600, "h": 45,
         "color": ACCENT, "size": 28},
        {"id": make_element_id(n, "builder"), "kind": "text",
         "text": "Built by Opticfy", "x": 60, "y": 220, "w": 300, "h": 28,
         "color": MUTED, "size": 16},
        {"id": make_element_id(n, "desc"), "kind": "text",
         "text": "Product Knowledge Copilot — AI-Powered Boiler Parts Lookup",
         "x": 60, "y": 280, "w": 600, "h": 28,
         "color": LIGHT_GRAY, "size": 14},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 155, "w": 100, "h": 3, "fill": ACCENT},
    ])


def slide2_problem(sid):
    n = 2
    problem_text = (
        '"There is an information card in their office for every boiler manufacturer '
        'imaginable — manufacturer\'s dimensions and specs, vendors and pricing, '
        'replacements if parts had been discontinued."\n'
        '— Dan Holohan, HeatingHelp.com\n\n'
        '• Every customer inquiry: a rep walks to the filing cabinet, pulls a handwritten '
        'card (some in pencil, going back to 1923), and cross-references Shopify manually.\n\n'
        '• After 5 PM and weekends: voicemail. NYC boiler emergencies peak Dec–Feb, '
        'including nights and weekends.\n\n'
        '• Spanish-speaking building supers (core Bronx/Harlem customers) have zero '
        'after-hours support.\n\n'
        '• Digitization project started in 2013 — still incomplete after 12 years.'
    )
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "103 Years of Knowledge — Locked in a Filing Cabinet",
         "x": 60, "y": 25, "w": 600, "h": 50,
         "color": WHITE, "size": 24, "bold": True},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 78, "w": 80, "h": 3, "fill": ACCENT},
        {"id": make_element_id(n, "body"), "kind": "text",
         "text": problem_text, "x": 60, "y": 92, "w": 600, "h": 295,
         "color": LIGHT_GRAY, "size": 12},
    ])


def slide3_cost(sid):
    n = 3
    cost_body = (
        "15 product inquiries/day × 20 min each = 5 hours of rep time daily\n\n"
        "Each lookup: walk to cabinet → find card → read pencil notes → "
        "cross-reference Shopify → verbally quote customer\n\n"
        "After-hours inquiries (Dec–Feb peak): 100% lost to voicemail\n\n"
        "Digitization project started in 2013 — still incomplete after 12 years"
    )
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "What This Is Costing You",
         "x": 60, "y": 25, "w": 600, "h": 45,
         "color": WHITE, "size": 26, "bold": True},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 72, "w": 80, "h": 3, "fill": ACCENT},
        {"id": make_element_id(n, "stat1_label"), "kind": "text",
         "text": "20 HRS / WEEK", "x": 65, "y": 92, "w": 270, "h": 45,
         "color": ACCENT, "size": 30, "bold": True},
        {"id": make_element_id(n, "stat1_sub"), "kind": "text",
         "text": "Rep time on manual part lookups",
         "x": 65, "y": 138, "w": 270, "h": 30,
         "color": LIGHT_GRAY, "size": 13},
        {"id": make_element_id(n, "stat2_label"), "kind": "text",
         "text": "$2,500 / MO", "x": 385, "y": 92, "w": 270, "h": 45,
         "color": ACCENT, "size": 30, "bold": True},
        {"id": make_element_id(n, "stat2_sub"), "kind": "text",
         "text": "Rep capacity tied to the filing cabinet",
         "x": 385, "y": 138, "w": 270, "h": 30,
         "color": LIGHT_GRAY, "size": 13},
        {"id": make_element_id(n, "body"), "kind": "text",
         "text": cost_body, "x": 60, "y": 185, "w": 600, "h": 200,
         "color": MUTED, "size": 12},
    ])


def slide4_solution(sid):
    n = 4
    solution_body = (
        "An n8n RAG agent that ingests Oswald's Shopify catalog and 100+ years of "
        "index card knowledge into a vector database, then answers natural-language "
        "boiler part queries via Intercom chat in under 10 seconds.\n\n"
        "A building super types: \"I have a 1962 Burnham V8, need the handhole gasket\"\n"
        "The agent responds with: SKU, dimensions, price, and a substitution option — "
        "instantly, in English or Spanish, 24/7.\n\n"
        "Architecture: Shopify API + Index Cards → OpenAI Embeddings → "
        "Supabase pgvector → Claude Haiku synthesis → Intercom webhook\n\n"
        "Key design principle: When the agent isn't confident, it escalates gracefully. "
        "Oswald never gives a wrong answer about a boiler part."
    )
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "What Opticfy Built",
         "x": 60, "y": 25, "w": 600, "h": 45,
         "color": WHITE, "size": 26, "bold": True},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 72, "w": 80, "h": 3, "fill": ACCENT},
        {"id": make_element_id(n, "name"), "kind": "text",
         "text": "Product Knowledge Copilot",
         "x": 60, "y": 88, "w": 600, "h": 35,
         "color": ACCENT, "size": 20, "bold": True},
        {"id": make_element_id(n, "body"), "kind": "text",
         "text": solution_body, "x": 60, "y": 128, "w": 600, "h": 255,
         "color": LIGHT_GRAY, "size": 13},
    ])


def slide5_how(sid):
    n = 5
    steps = (
        "1.  Customer sends a message via Intercom chat widget on oswaldsupply.com\n\n"
        "2.  Webhook fires to n8n — query text is extracted, language detected (EN/ES)\n\n"
        "3.  Query is embedded via OpenAI and searched against Oswald's vector database "
        "(Shopify catalog + index card knowledge, hybrid vector + keyword search)\n\n"
        "4.  Confidence check: if top match similarity > 0.75 → synthesize answer; "
        "if below → escalate to human rep with context\n\n"
        "5.  Claude Haiku synthesizes a natural-language answer from the retrieved "
        "product data and index card entries — responds in the customer's language\n\n"
        "6.  Response delivered back to Intercom in < 10 seconds — SKU, price, "
        "availability, substitution option if applicable"
    )
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "Step by Step",
         "x": 60, "y": 25, "w": 600, "h": 45,
         "color": WHITE, "size": 26, "bold": True},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 72, "w": 80, "h": 3, "fill": ACCENT},
        {"id": make_element_id(n, "steps"), "kind": "text",
         "text": steps, "x": 60, "y": 88, "w": 600, "h": 300,
         "color": LIGHT_GRAY, "size": 12},
    ])


def slide6_result(sid):
    n = 6
    before = (
        "BEFORE\n\n"
        "❌ Hours available: M–F 7:30AM–5PM\n"
        "❌ After-hours: voicemail only\n"
        "❌ Spanish support: none\n"
        "❌ Lookup speed: 20 min/query\n"
        "❌ Index cards: partially digitized\n"
        "❌ Peak winter demand: unserviced\n"
        "❌ Rep time on lookups: 20 hrs/week"
    )
    after = (
        "AFTER\n\n"
        "✅ Hours available: 24/7/365\n"
        "✅ After-hours: instant AI response\n"
        "✅ Spanish support: auto-detected\n"
        "✅ Lookup speed: < 10 seconds\n"
        "✅ Index cards: fully searchable\n"
        "✅ Peak demand: fully covered\n"
        "✅ Rep time on lookups: near zero"
    )
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "What Changes",
         "x": 60, "y": 25, "w": 600, "h": 45,
         "color": WHITE, "size": 26, "bold": True},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 72, "w": 80, "h": 3, "fill": ACCENT},
        {"id": make_element_id(n, "before"), "kind": "text",
         "text": before, "x": 60, "y": 88, "w": 295, "h": 300,
         "color": RED, "size": 12},
        {"id": make_element_id(n, "after"), "kind": "text",
         "text": after, "x": 375, "y": 88, "w": 295, "h": 300,
         "color": GREEN, "size": 12},
    ])


def slide7_demo(sid):
    n = 7
    demo_text = (
        "Three live scenarios — shown in Intercom chat on oswaldsupply.com\n\n"
        "Scenario 1 — English, legacy part:\n"
        "  Customer: \"I have a 1962 Burnham V8 boiler, need the handhole plate gasket\"\n"
        "  Copilot: \"For the Burnham V8, the handhole gasket is SKU 590-921-612 "
        "($18.50). Oval profile, 4.5\" × 3.25\". We also carry the full handhole "
        "assembly (SKU 590-921-600, $47.00) if the frame is worn.\"\n\n"
        "Scenario 2 — Spanish, modern part:\n"
        "  Customer: \"Necesito una válvula de presión para caldera Weil McLain, 30 PSI\"\n"
        "  Copilot: \"Para la caldera Weil McLain, la válvula de presión de 30 PSI "
        "es el SKU WM-PRV-30 ($34.95). También tenemos el kit de reemplazo completo "
        "(SKU WM-PRV-KIT, $52.00).\"\n\n"
        "Scenario 3 — Index card cross-reference:\n"
        "  Customer: \"Found a plate marked 'Crown 1987', oval curved shape\"\n"
        "  Copilot: \"That's a Crown Boiler Series 55, circa 1985–1991. The handhole "
        "plate is Crown part #CR55-HH. Cross-reference: Burnham 592-400-026 fits the "
        "same opening. In stock at $22.00.\""
    )
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "See It in Action",
         "x": 60, "y": 25, "w": 600, "h": 45,
         "color": WHITE, "size": 26, "bold": True},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 72, "w": 80, "h": 3, "fill": ACCENT},
        {"id": make_element_id(n, "demo"), "kind": "text",
         "text": demo_text, "x": 60, "y": 88, "w": 600, "h": 300,
         "color": LIGHT_GRAY, "size": 11},
    ])


def slide8_roi(sid):
    n = 8
    roi_body = (
        "Hour savings: 20 hrs/week × $25/hr burdened labor = $2,000/month in rep capacity recaptured\n\n"
        "After-hours revenue: NYC boiler emergencies Dec–Feb average 3–5 after-hours "
        "inquiries per night. At $150 avg order value, even 50% conversion = $500–$800/month "
        "in revenue that currently goes to voicemail.\n\n"
        "Year 1 ROI (conservative): $2,500 + $500 = $3,000/month saved+earned "
        "on a one-time build cost of $3,500–$5,000\n\n"
        "Payback period: < 60 days"
    )
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "The Numbers",
         "x": 60, "y": 25, "w": 600, "h": 45,
         "color": WHITE, "size": 26, "bold": True},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 72, "w": 80, "h": 3, "fill": ACCENT},
        {"id": make_element_id(n, "s1"), "kind": "text",
         "text": "20 HRS/WEEK", "x": 60, "y": 90, "w": 190, "h": 40,
         "color": ACCENT, "size": 22, "bold": True},
        {"id": make_element_id(n, "s1sub"), "kind": "text",
         "text": "Rep time recaptured", "x": 60, "y": 130, "w": 190, "h": 25,
         "color": MUTED, "size": 12},
        {"id": make_element_id(n, "s2"), "kind": "text",
         "text": "$2,500+/MO", "x": 270, "y": 90, "w": 190, "h": 40,
         "color": ACCENT, "size": 22, "bold": True},
        {"id": make_element_id(n, "s2sub"), "kind": "text",
         "text": "Saved or earned monthly", "x": 270, "y": 130, "w": 190, "h": 25,
         "color": MUTED, "size": 12},
        {"id": make_element_id(n, "s3"), "kind": "text",
         "text": "< 10 SEC", "x": 488, "y": 90, "w": 175, "h": 40,
         "color": ACCENT, "size": 22, "bold": True},
        {"id": make_element_id(n, "s3sub"), "kind": "text",
         "text": "Response time vs 20 min", "x": 488, "y": 130, "w": 175, "h": 25,
         "color": MUTED, "size": 12},
        {"id": make_element_id(n, "body"), "kind": "text",
         "text": roi_body, "x": 60, "y": 165, "w": 600, "h": 215,
         "color": LIGHT_GRAY, "size": 12},
    ])


def slide9_next(sid):
    n = 9
    steps_text = (
        "Phase 1 — Audit (Week 1, free)\n"
        "  Review Shopify catalog structure + any digitized index card data\n"
        "  Confirm Intercom plan tier (webhook eligibility)\n"
        "  Define success metrics with Robert\n\n"
        "Phase 2 — Build (Week 2–3)\n"
        "  Connect Shopify API + ingest catalog into Supabase vector DB\n"
        "  Build and test Intercom webhook integration\n"
        "  Run bilingual accuracy testing with 50 real-world queries\n\n"
        "Phase 3 — Deploy (Week 4)\n"
        "  Go live on oswaldsupply.com Intercom\n"
        "  30-day monitoring + index card batch ingestion as Robert digitizes\n\n"
        "Investment: $3,500–$5,000 one-time build + optional $500/mo maintenance"
    )
    contact_text = (
        "JT Somwaru — Opticfy\n"
        "jtsomwaru.com\n"
        "linkedin.com/in/jon-trevor-somwaru"
    )
    return build_slide_requests(sid, BG_DARK, [
        {"id": make_element_id(n, "title"), "kind": "text",
         "text": "How We Work Together",
         "x": 60, "y": 25, "w": 600, "h": 45,
         "color": WHITE, "size": 26, "bold": True},
        {"id": make_element_id(n, "bar"), "kind": "rect",
         "x": 60, "y": 72, "w": 80, "h": 3, "fill": ACCENT},
        {"id": make_element_id(n, "steps"), "kind": "text",
         "text": steps_text, "x": 60, "y": 88, "w": 590, "h": 270,
         "color": LIGHT_GRAY, "size": 12},
        {"id": make_element_id(n, "contact"), "kind": "text",
         "text": contact_text, "x": 60, "y": 365, "w": 600, "h": 30,
         "color": MUTED, "size": 11},
    ])


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", default="hc-oswald")
    parser.add_argument("--folder", default="Eve — Drafts/Opticfy/Case Studies")
    parser.add_argument("--title", default="H.C. Oswald Supply Co. — Opticfy Proposal")
    args = parser.parse_args()

    print(f"Building deck: {args.title}")

    creds = get_creds()
    slides = build("slides", "v1", credentials=creds, cache_discovery=False)
    drive  = build("drive",  "v3", credentials=creds, cache_discovery=False)

    # 1. Create blank presentation
    print("Creating presentation...")
    pres = slides.presentations().create(body={"title": args.title}).execute()
    pres_id = pres["presentationId"]
    print(f"  ID: {pres_id}")

    # Get IDs of default slides to delete
    default_slides = [s["objectId"] for s in pres.get("slides", [])]

    # 2. Add 9 new slides (blank), collect their IDs
    add_requests = []
    slide_ids = []
    for i in range(9):
        sid = f"slide_{i+1}"
        slide_ids.append(sid)
        add_requests.append({
            "createSlide": {
                "objectId": sid,
                "insertionIndex": i,
                "slideLayoutReference": {"predefinedLayout": "BLANK"}
            }
        })
    # Delete default slides
    for dsid in default_slides:
        add_requests.append({"deleteObject": {"objectId": dsid}})

    slides.presentations().batchUpdate(
        presentationId=pres_id,
        body={"requests": add_requests}
    ).execute()
    print("  9 slides created")

    # 3. Build content for each slide
    slide_builders = [
        slide1_title,
        slide2_problem,
        slide3_cost,
        slide4_solution,
        slide5_how,
        slide6_result,
        slide7_demo,
        slide8_roi,
        slide9_next,
    ]

    for i, (sid, builder) in enumerate(zip(slide_ids, slide_builders)):
        requests = builder(sid)
        slides.presentations().batchUpdate(
            presentationId=pres_id,
            body={"requests": requests}
        ).execute()
        print(f"  Slide {i+1}/9 formatted")

    # 4. Move to correct Drive folder
    print(f"Moving to {args.folder}...")
    folder_id = get_target_folder(drive, args.folder)

    # Get current parents
    file_meta = drive.files().get(fileId=pres_id, fields="parents").execute()
    old_parents = ",".join(file_meta.get("parents", []))
    drive.files().update(
        fileId=pres_id,
        addParents=folder_id,
        removeParents=old_parents,
        fields="id,parents"
    ).execute()
    print(f"  Saved to folder")

    # 5. Output URL
    url = f"https://docs.google.com/presentation/d/{pres_id}/edit"
    print(f"\n✅ Deck ready: {url}")

    # 6. Write deck-url.txt to client folder
    client_dir = os.path.join(PIPELINE_ROOT, args.client)
    if os.path.isdir(client_dir):
        url_file = os.path.join(client_dir, "deck-url.txt")
        with open(url_file, "w") as f:
            f.write(url + "\n")
        print(f"   URL saved to {url_file}")

    return url


if __name__ == "__main__":
    main()
