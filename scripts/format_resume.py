#!/usr/bin/env python3
"""
format_resume.py — Apply professional design to JT's resume/cover letter Google Docs
Uses Google Docs API to format after upload via drive_drafts.py

Usage:
  python3 format_resume.py --doc-id <GOOGLE_DOC_ID> --type resume
  python3 format_resume.py --doc-id <GOOGLE_DOC_ID> --type cover_letter

Design spec (from PDF research):
  - Font: Calibri (headings bold 13-14pt, body 11pt)
  - Name: 22pt bold, navy (#1B365D)
  - Accent color: Navy Blue (#1B365D)
  - Body text: Near-black (#1A1A1A)
  - Secondary text (dates): Dark gray (#555555)
  - Single-column, ATS-safe, no tables/graphics
  - Section headings: 13pt, ALL CAPS, bold, navy, with spacing
  - Passes Notepad test + B&W print test
"""

import argparse
import json
import os
import sys

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")

# ── Design constants ──────────────────────────────────────────────────────────
NAVY = {"red": 0.106, "green": 0.212, "blue": 0.365}       # #1B365D
NEAR_BLACK = {"red": 0.102, "green": 0.102, "blue": 0.102} # #1A1A1A
DARK_GRAY = {"red": 0.333, "green": 0.333, "blue": 0.333}  # #555555
WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}

SECTION_HEADINGS_RESUME = [
    "PROFESSIONAL SUMMARY", "SUMMARY",
    "TECHNICAL SKILLS", "SKILLS", "CORE COMPETENCIES",
    "PROFESSIONAL EXPERIENCE", "WORK EXPERIENCE", "EXPERIENCE",
    "KEY PROJECTS", "PROJECTS", "CASE STUDIES",
    "CERTIFICATIONS", "EDUCATION"
]

SECTION_HEADINGS_COVER = [
    "RE:", "DEAR ", "SINCERELY", "BEST REGARDS"
]

PT = 1 / 72  # points to inches (not needed here, Docs uses pt directly)


def get_service():
    if not os.path.exists(TOKEN_PATH):
        print(f"ERROR: Token not found at {TOKEN_PATH}. Run drive_auth.py first.")
        sys.exit(1)
    with open(TOKEN_PATH) as f:
        td = json.load(f)
    creds = Credentials(
        token=td.get("token"),
        refresh_token=td.get("refresh_token"),
        token_uri=td.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=td.get("client_id"),
        client_secret=td.get("client_secret"),
        scopes=["https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/documents"]
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        td["token"] = creds.token
        with open(TOKEN_PATH, "w") as f:
            json.dump(td, f, indent=2)
    return build("docs", "v1", credentials=creds, cache_discovery=False)


def get_doc(service, doc_id):
    return service.documents().get(documentId=doc_id).execute()


def find_text_ranges(doc, search_texts):
    """Find start/end indices of text matches in the doc body."""
    results = []
    content = doc.get("body", {}).get("content", [])
    for element in content:
        if "paragraph" not in element:
            continue
        para = element["paragraph"]
        para_text = ""
        start_idx = None
        for pe in para.get("elements", []):
            tr = pe.get("textRun")
            if not tr:
                continue
            if start_idx is None:
                start_idx = pe.get("startIndex", 0)
            para_text += tr.get("content", "")
        if start_idx is None:
            continue
        stripped = para_text.strip().upper()
        for search in search_texts:
            if stripped == search.upper() or stripped.startswith(search.upper()):
                end_idx = start_idx + len(para_text)
                results.append({
                    "text": para_text.strip(),
                    "start": start_idx,
                    "end": end_idx - 1  # exclude newline
                })
                break
    return results


def find_first_line(doc):
    """Find the first non-empty line (the name)."""
    content = doc.get("body", {}).get("content", [])
    for element in content:
        if "paragraph" not in element:
            continue
        para = element["paragraph"]
        para_text = ""
        start_idx = None
        for pe in para.get("elements", []):
            tr = pe.get("textRun")
            if not tr:
                continue
            if start_idx is None:
                start_idx = pe.get("startIndex", 0)
            para_text += tr.get("content", "")
        stripped = para_text.strip()
        if stripped and start_idx is not None:
            return {"text": stripped, "start": start_idx, "end": start_idx + len(para_text) - 1}
    return None


def find_second_line(doc):
    """Find the second non-empty line (the target title)."""
    content = doc.get("body", {}).get("content", [])
    count = 0
    for element in content:
        if "paragraph" not in element:
            continue
        para = element["paragraph"]
        para_text = ""
        start_idx = None
        for pe in para.get("elements", []):
            tr = pe.get("textRun")
            if not tr:
                continue
            if start_idx is None:
                start_idx = pe.get("startIndex", 0)
            para_text += tr.get("content", "")
        stripped = para_text.strip()
        if stripped and start_idx is not None:
            count += 1
            if count == 2:
                return {"text": stripped, "start": start_idx, "end": start_idx + len(para_text) - 1}
    return None


def build_resume_requests(doc):
    requests = []

    # ── Set document default style ────────────────────────────────────────────
    # Normal text: Calibri 11pt, near-black
    requests.append({
        "updateDocumentStyle": {
            "documentStyle": {
                "defaultHeaderId": "",
                "defaultFooterId": "",
                "marginTop": {"magnitude": 72, "unit": "PT"},    # 1 inch
                "marginBottom": {"magnitude": 72, "unit": "PT"},
                "marginLeft": {"magnitude": 72, "unit": "PT"},
                "marginRight": {"magnitude": 72, "unit": "PT"},
            },
            "fields": "marginTop,marginBottom,marginLeft,marginRight"
        }
    })

    content = doc.get("body", {}).get("content", [])

    # ── Style all paragraphs by type ──────────────────────────────────────────
    name_done = False
    title_done = False
    line_count = 0

    for element in content:
        if "paragraph" not in element:
            continue
        para = element["paragraph"]
        para_text = ""
        start_idx = None
        end_idx = None

        for pe in para.get("elements", []):
            tr = pe.get("textRun")
            if not tr:
                continue
            if start_idx is None:
                start_idx = pe.get("startIndex", 0)
            end_idx = pe.get("endIndex", 0)
            para_text += tr.get("content", "")

        stripped = para_text.strip()
        if not stripped or start_idx is None:
            continue

        line_count += 1
        text_range = {"startIndex": start_idx, "endIndex": end_idx}

        # NAME (first non-empty line)
        if not name_done:
            name_done = True
            requests.append({
                "updateTextStyle": {
                    "range": text_range,
                    "textStyle": {
                        "fontSize": {"magnitude": 22, "unit": "PT"},
                        "bold": True,
                        "foregroundColor": {"color": {"rgbColor": NAVY}},
                        "weightedFontFamily": {"fontFamily": "Calibri", "weight": 700}
                    },
                    "fields": "fontSize,bold,foregroundColor,weightedFontFamily"
                }
            })
            requests.append({
                "updateParagraphStyle": {
                    "range": text_range,
                    "paragraphStyle": {
                        "alignment": "CENTER",
                        "spaceAbove": {"magnitude": 0, "unit": "PT"},
                        "spaceBelow": {"magnitude": 4, "unit": "PT"}
                    },
                    "fields": "alignment,spaceAbove,spaceBelow"
                }
            })
            continue

        # TARGET TITLE (second non-empty line — if it looks like a title)
        if not title_done and line_count <= 4:
            # Check if this looks like a title (not an email/phone/URL)
            is_contact = any(c in stripped for c in ["@", "linkedin", "http", "|", "•", "+1"])
            if not is_contact:
                title_done = True
                requests.append({
                    "updateTextStyle": {
                        "range": text_range,
                        "textStyle": {
                            "fontSize": {"magnitude": 13, "unit": "PT"},
                            "bold": False,
                            "foregroundColor": {"color": {"rgbColor": DARK_GRAY}},
                            "weightedFontFamily": {"fontFamily": "Calibri", "weight": 400}
                        },
                        "fields": "fontSize,bold,foregroundColor,weightedFontFamily"
                    }
                })
                requests.append({
                    "updateParagraphStyle": {
                        "range": text_range,
                        "paragraphStyle": {
                            "alignment": "CENTER",
                            "spaceBelow": {"magnitude": 2, "unit": "PT"}
                        },
                        "fields": "alignment,spaceBelow"
                    }
                })
                continue

        # SECTION HEADINGS
        stripped_upper = stripped.upper()
        is_section = any(stripped_upper == h or stripped_upper.startswith(h)
                        for h in SECTION_HEADINGS_RESUME)
        if is_section:
            requests.append({
                "updateTextStyle": {
                    "range": text_range,
                    "textStyle": {
                        "fontSize": {"magnitude": 12, "unit": "PT"},
                        "bold": True,
                        "foregroundColor": {"color": {"rgbColor": NAVY}},
                        "weightedFontFamily": {"fontFamily": "Calibri", "weight": 700},
                        "smallCaps": True
                    },
                    "fields": "fontSize,bold,foregroundColor,weightedFontFamily,smallCaps"
                }
            })
            requests.append({
                "updateParagraphStyle": {
                    "range": text_range,
                    "paragraphStyle": {
                        "spaceAbove": {"magnitude": 10, "unit": "PT"},
                        "spaceBelow": {"magnitude": 2, "unit": "PT"},
                        "borderBottom": {
                            "color": {"color": {"rgbColor": NAVY}},
                            "width": {"magnitude": 0.75, "unit": "PT"},
                            "padding": {"magnitude": 1, "unit": "PT"},
                            "dashStyle": "SOLID"
                        }
                    },
                    "fields": "spaceAbove,spaceBelow,borderBottom"
                }
            })
            continue

        # CONTACT LINE (has | • @ or similar separators)
        is_contact_line = any(c in stripped for c in ["|", "•", "@"])
        if is_contact_line and line_count <= 6:
            requests.append({
                "updateTextStyle": {
                    "range": text_range,
                    "textStyle": {
                        "fontSize": {"magnitude": 10, "unit": "PT"},
                        "bold": False,
                        "foregroundColor": {"color": {"rgbColor": DARK_GRAY}},
                        "weightedFontFamily": {"fontFamily": "Calibri", "weight": 400}
                    },
                    "fields": "fontSize,bold,foregroundColor,weightedFontFamily"
                }
            })
            requests.append({
                "updateParagraphStyle": {
                    "range": text_range,
                    "paragraphStyle": {
                        "alignment": "CENTER",
                        "spaceBelow": {"magnitude": 2, "unit": "PT"}
                    },
                    "fields": "alignment,spaceBelow"
                }
            })
            continue

        # JOB TITLES (bold lines that aren't headings — heuristic: ends with year or has company)
        looks_like_title = (stripped.endswith(")") or "20" in stripped) and len(stripped) < 80
        if looks_like_title:
            requests.append({
                "updateTextStyle": {
                    "range": text_range,
                    "textStyle": {
                        "fontSize": {"magnitude": 11, "unit": "PT"},
                        "bold": True,
                        "foregroundColor": {"color": {"rgbColor": NEAR_BLACK}},
                        "weightedFontFamily": {"fontFamily": "Calibri", "weight": 700}
                    },
                    "fields": "fontSize,bold,foregroundColor,weightedFontFamily"
                }
            })
            requests.append({
                "updateParagraphStyle": {
                    "range": text_range,
                    "paragraphStyle": {
                        "spaceAbove": {"magnitude": 6, "unit": "PT"},
                        "spaceBelow": {"magnitude": 1, "unit": "PT"}
                    },
                    "fields": "spaceAbove,spaceBelow"
                }
            })
            continue

        # BODY TEXT (bullets and paragraphs)
        requests.append({
            "updateTextStyle": {
                "range": text_range,
                "textStyle": {
                    "fontSize": {"magnitude": 11, "unit": "PT"},
                    "bold": False,
                    "foregroundColor": {"color": {"rgbColor": NEAR_BLACK}},
                    "weightedFontFamily": {"fontFamily": "Calibri", "weight": 400}
                },
                "fields": "fontSize,bold,foregroundColor,weightedFontFamily"
            }
        })
        requests.append({
            "updateParagraphStyle": {
                "range": text_range,
                "paragraphStyle": {
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 2, "unit": "PT"},
                    "lineSpacing": 115
                },
                "fields": "spaceAbove,spaceBelow,lineSpacing"
            }
        })

    return requests


def build_cover_letter_requests(doc):
    requests = []

    # Margins slightly more generous for cover letter (letter format)
    requests.append({
        "updateDocumentStyle": {
            "documentStyle": {
                "marginTop": {"magnitude": 72, "unit": "PT"},
                "marginBottom": {"magnitude": 72, "unit": "PT"},
                "marginLeft": {"magnitude": 72, "unit": "PT"},
                "marginRight": {"magnitude": 72, "unit": "PT"},
            },
            "fields": "marginTop,marginBottom,marginLeft,marginRight"
        }
    })

    content = doc.get("body", {}).get("content", [])
    name_done = False
    line_count = 0
    in_body = False

    for element in content:
        if "paragraph" not in element:
            continue
        para = element["paragraph"]
        para_text = ""
        start_idx = None
        end_idx = None

        for pe in para.get("elements", []):
            tr = pe.get("textRun")
            if not tr:
                continue
            if start_idx is None:
                start_idx = pe.get("startIndex", 0)
            end_idx = pe.get("endIndex", 0)
            para_text += tr.get("content", "")

        stripped = para_text.strip()
        if not stripped or start_idx is None:
            continue

        line_count += 1
        text_range = {"startIndex": start_idx, "endIndex": end_idx}

        # NAME (first line)
        if not name_done:
            name_done = True
            requests.append({
                "updateTextStyle": {
                    "range": text_range,
                    "textStyle": {
                        "fontSize": {"magnitude": 20, "unit": "PT"},
                        "bold": True,
                        "foregroundColor": {"color": {"rgbColor": NAVY}},
                        "weightedFontFamily": {"fontFamily": "Calibri", "weight": 700}
                    },
                    "fields": "fontSize,bold,foregroundColor,weightedFontFamily"
                }
            })
            requests.append({
                "updateParagraphStyle": {
                    "range": text_range,
                    "paragraphStyle": {
                        "spaceBelow": {"magnitude": 2, "unit": "PT"}
                    },
                    "fields": "spaceBelow"
                }
            })
            continue

        # Header lines (contact info, date, recipient — first 8 lines)
        if line_count <= 8:
            requests.append({
                "updateTextStyle": {
                    "range": text_range,
                    "textStyle": {
                        "fontSize": {"magnitude": 10, "unit": "PT"},
                        "bold": False,
                        "foregroundColor": {"color": {"rgbColor": DARK_GRAY}},
                        "weightedFontFamily": {"fontFamily": "Calibri", "weight": 400}
                    },
                    "fields": "fontSize,bold,foregroundColor,weightedFontFamily"
                }
            })
            requests.append({
                "updateParagraphStyle": {
                    "range": text_range,
                    "paragraphStyle": {
                        "spaceBelow": {"magnitude": 1, "unit": "PT"}
                    },
                    "fields": "spaceBelow"
                }
            })
            continue

        # Body paragraphs
        requests.append({
            "updateTextStyle": {
                "range": text_range,
                "textStyle": {
                    "fontSize": {"magnitude": 11, "unit": "PT"},
                    "bold": False,
                    "foregroundColor": {"color": {"rgbColor": NEAR_BLACK}},
                    "weightedFontFamily": {"fontFamily": "Calibri", "weight": 400}
                },
                "fields": "fontSize,bold,foregroundColor,weightedFontFamily"
            }
        })
        requests.append({
            "updateParagraphStyle": {
                "range": text_range,
                "paragraphStyle": {
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8, "unit": "PT"},
                    "lineSpacing": 115,
                    "indentFirstLine": {"magnitude": 0, "unit": "PT"}
                },
                "fields": "spaceAbove,spaceBelow,lineSpacing,indentFirstLine"
            }
        })

    return requests


def format_doc(doc_id, doc_type="resume"):
    service = get_service()
    print(f"Fetching document {doc_id}...")
    doc = get_doc(service, doc_id)
    title = doc.get("title", "Unknown")
    print(f"Document: {title}")

    if doc_type == "resume":
        requests = build_resume_requests(doc)
    else:
        requests = build_cover_letter_requests(doc)

    if not requests:
        print("No formatting requests generated.")
        return

    print(f"Applying {len(requests)} formatting operations...")

    # Batch in chunks of 50 to avoid API limits
    chunk_size = 50
    for i in range(0, len(requests), chunk_size):
        chunk = requests[i:i + chunk_size]
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": chunk}
        ).execute()
        print(f"  Applied {min(i + chunk_size, len(requests))}/{len(requests)} operations...")

    print(f"✅ Formatting complete: https://docs.google.com/document/d/{doc_id}/edit")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format a Google Doc as a professional resume or cover letter")
    parser.add_argument("--doc-id", required=True, help="Google Doc ID")
    parser.add_argument("--type", choices=["resume", "cover_letter"], default="resume")
    args = parser.parse_args()
    format_doc(args.doc_id, args.type)
