#!/usr/bin/env python3
"""
slides_framework.py — Reusable Google Slides creation engine for Opticfy pipeline.

Used by client-specific build-deck.py files.

Usage from a build-deck.py:
    import sys
    sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/scripts"))
    from slides_framework import create_deck, slide_text, slide_rect, pt, COLORS

API:
    url = create_deck(
        title="Company — Opticfy Proposal",
        client_slug="company-slug",
        slides=[
            ("slide_1", [slide_text("s1_title", "Headline", x, y, w, h, color, size, bold), ...]),
            ...
        ],
        drive_folder="Eve — Drafts/Opticfy/Case Studies"
    )
"""

import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH    = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")
PIPELINE_ROOT = os.path.expanduser("~/projects/opticfy-pipeline/clients")

# ── Unit helpers ─────────────────────────────────────────────────────────────
def pt(n):
    """Points to EMU (1 point = 12700 EMU)."""
    return int(n * 12700)

# ── Brand colors (RGB 0-1 floats) ────────────────────────────────────────────
COLORS = {
    "bg":         {"red": 0.102, "green": 0.102, "blue": 0.180},  # #1a1a2e
    "accent":     {"red": 0.000, "green": 0.706, "blue": 0.847},  # #00b4d8
    "white":      {"red": 1.000, "green": 1.000, "blue": 1.000},
    "light_gray": {"red": 0.800, "green": 0.800, "blue": 0.800},  # #cccccc
    "muted":      {"red": 0.533, "green": 0.573, "blue": 0.690},  # #8892b0
    "dark_card":  {"red": 0.086, "green": 0.129, "blue": 0.243},  # #16213e
    "green":      {"red": 0.000, "green": 0.784, "blue": 0.592},  # #00c897
    "red":        {"red": 1.000, "green": 0.420, "blue": 0.420},  # #ff6b6b
}

# ── Element builders ──────────────────────────────────────────────────────────

def slide_text(eid, text, x, y, w, h, color="white", size=14, bold=False, align=None):
    """Return a text element definition."""
    return {
        "id": eid, "kind": "text", "text": text,
        "x": x, "y": y, "w": w, "h": h,
        "color": COLORS.get(color, COLORS["white"]),
        "size": size, "bold": bold, "align": align,
    }

def slide_rect(eid, x, y, w, h, fill="accent"):
    """Return a rectangle element definition."""
    return {
        "id": eid, "kind": "rect",
        "x": x, "y": y, "w": w, "h": h,
        "fill": COLORS.get(fill, COLORS["accent"]),
    }

def accent_bar(slide_num, x=60, y=72, w=80):
    """Standard accent bar divider."""
    return slide_rect(f"s{slide_num}_bar", x, y, w, 3)

# ── Request builders ──────────────────────────────────────────────────────────

def build_slide_requests(slide_id, bg_color, elements):
    """Build Slides API batchUpdate requests for one slide."""
    requests = []

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
            requests.append({
                "createShape": {
                    "objectId": eid,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": {
                            "width":  {"magnitude": pt(el["w"]), "unit": "EMU"},
                            "height": {"magnitude": pt(el["h"]), "unit": "EMU"},
                        },
                        "transform": {
                            "scaleX": 1, "scaleY": 1,
                            "translateX": pt(el["x"]),
                            "translateY": pt(el["y"]),
                            "unit": "EMU",
                        }
                    }
                }
            })
            requests.append({
                "insertText": {"objectId": eid, "text": el["text"]}
            })
            style = {
                "foregroundColor": {"opaqueColor": {"rgbColor": el.get("color", COLORS["white"])}},
                "fontSize": {"magnitude": el.get("size", 14), "unit": "PT"},
                "bold": el.get("bold", False),
                "fontFamily": "Arial",
            }
            requests.append({
                "updateTextStyle": {
                    "objectId": eid,
                    "style": style,
                    "fields": "foregroundColor,fontSize,bold,fontFamily",
                    "textRange": {"type": "ALL"},
                }
            })
            if el.get("align"):
                requests.append({
                    "updateParagraphStyle": {
                        "objectId": eid,
                        "style": {"alignment": el["align"]},
                        "fields": "alignment",
                        "textRange": {"type": "ALL"},
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
                            "width":  {"magnitude": pt(el["w"]), "unit": "EMU"},
                            "height": {"magnitude": pt(el["h"]), "unit": "EMU"},
                        },
                        "transform": {
                            "scaleX": 1, "scaleY": 1,
                            "translateX": pt(el["x"]),
                            "translateY": pt(el["y"]),
                            "unit": "EMU",
                        }
                    }
                }
            })
            fill_color = el.get("fill", COLORS["accent"])
            requests.append({
                "updateShapeProperties": {
                    "objectId": eid,
                    "shapeProperties": {
                        "shapeBackgroundFill": {
                            "solidFill": {"color": {"rgbColor": fill_color}}
                        },
                        "outline": {
                            "outlineFill": {"solidFill": {"color": {"rgbColor": fill_color}}}
                        },
                    },
                    "fields": "shapeBackgroundFill,outline",
                }
            })

    return requests

# ── Auth & Drive helpers ──────────────────────────────────────────────────────

def get_creds():
    with open(TOKEN_PATH) as f:
        td = json.load(f)
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


def get_target_folder(drive, path):
    parent = None
    for part in path.split("/"):
        parent = find_or_create_folder(drive, part, parent)
    return parent

# ── Main entry point ──────────────────────────────────────────────────────────

def create_deck(title, client_slug, slides, drive_folder="Eve — Drafts/Opticfy/Case Studies"):
    """
    Create a Google Slides deck and publish to Drive.

    Args:
        title:        Presentation title (e.g. "Acme Corp — Opticfy Proposal")
        client_slug:  Pipeline slug (e.g. "acme-corp") for deck-url.txt
        slides:       List of (slide_id, bg_color, elements) tuples.
                      bg_color: a COLORS dict value.
                      elements: list of slide_text() / slide_rect() results.
        drive_folder: Drive path to save into (slash-separated).

    Returns:
        str: The Google Slides URL.
    """
    print(f"Building deck: {title}")

    creds  = get_creds()
    svc    = build("slides", "v1", credentials=creds, cache_discovery=False)
    drive  = build("drive",  "v3", credentials=creds, cache_discovery=False)

    # 1. Create blank presentation
    print("  Creating presentation...")
    pres    = svc.presentations().create(body={"title": title}).execute()
    pres_id = pres["presentationId"]

    # 2. Add slides + delete defaults
    default_ids = [s["objectId"] for s in pres.get("slides", [])]
    add_requests = []
    for i, (sid, _bg, _els) in enumerate(slides):
        add_requests.append({
            "createSlide": {
                "objectId": sid,
                "insertionIndex": i,
                "slideLayoutReference": {"predefinedLayout": "BLANK"}
            }
        })
    for dsid in default_ids:
        add_requests.append({"deleteObject": {"objectId": dsid}})
    svc.presentations().batchUpdate(
        presentationId=pres_id,
        body={"requests": add_requests}
    ).execute()
    print(f"  {len(slides)} slides added")

    # 3. Format each slide
    for i, (sid, bg, elements) in enumerate(slides):
        requests = build_slide_requests(sid, bg, elements)
        svc.presentations().batchUpdate(
            presentationId=pres_id,
            body={"requests": requests}
        ).execute()
        print(f"  Slide {i+1}/{len(slides)} formatted")

    # 4. Move to Drive folder
    print(f"  Saving to {drive_folder}...")
    folder_id = get_target_folder(drive, drive_folder)
    file_meta = drive.files().get(fileId=pres_id, fields="parents").execute()
    old_parents = ",".join(file_meta.get("parents", []))
    drive.files().update(
        fileId=pres_id,
        addParents=folder_id,
        removeParents=old_parents,
        fields="id,parents"
    ).execute()

    # 5. Build URL + write deck-url.txt
    url = f"https://docs.google.com/presentation/d/{pres_id}/edit"
    print(f"\n✅ Deck ready: {url}")

    client_dir = os.path.join(PIPELINE_ROOT, client_slug)
    if os.path.isdir(client_dir):
        with open(os.path.join(client_dir, "deck-url.txt"), "w") as f:
            f.write(url + "\n")
        print(f"   URL saved to {client_dir}/deck-url.txt")

    return url
