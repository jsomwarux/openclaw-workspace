#!/usr/bin/env python3
"""
drive_drafts.py — Automatically create Google Docs in the Eve — Drafts Drive folder.

Usage:
  python3 drive_drafts.py --title "Vista — X Thread" --project "Vista" --type "X Threads" --content "Tweet content..."
  python3 drive_drafts.py --title "Vista — X Thread" --project "Vista" --type "X Threads" --file path/to/draft.md
  python3 drive_drafts.py --list-folders   # show all folders in Eve — Drafts

Requires one-time auth: python3 drive_auth.py
Token stored at: ~/.openclaw/workspace/config/google-oauth-token.json
"""

import argparse
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")

from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH  = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")
ROOT_FOLDER = "Eve — Drafts"

# BANNED title patterns for outreach docs — these create confusion and duplicates
# Always use "[Company] — LinkedIn DM (3-touch)" or "[Company] — Research Brief" etc.
# BANNED title patterns for outreach docs — use standard naming instead
# '[Company] — LinkedIn DM (3-touch)' is the correct outreach doc title
BANNED_TITLE_PATTERNS = [
    "Outreach Draft",
    "outreach draft",
]

def check_title(title):
    """Warn on non-standard titles but don't block uploads (docs may be solo docs for a client)."""
    for banned in BANNED_TITLE_PATTERNS:
        if banned in title:
            print(f"WARNING: Title '{title}' uses non-standard pattern '{banned}'.", file=sys.stderr)
            print("Preferred: '[Company] — LinkedIn DM (3-touch)' or '[Company] — Research Brief'", file=sys.stderr)
            print("Continuing upload — rename manually or re-upload with correct title.", file=sys.stderr)


def get_drive():
    if not os.path.exists(TOKEN_PATH):
        print(f"ERROR: OAuth token not found at {TOKEN_PATH}")
        print("Run this first:  python3 ~/.openclaw/workspace/scripts/drive_auth.py")
        sys.exit(1)

    with open(TOKEN_PATH) as f:
        td = json.load(f)

    creds = Credentials(
        token=td.get("token"),
        refresh_token=td.get("refresh_token"),
        token_uri=td.get("token_uri"),
        client_id=td.get("client_id"),
        client_secret=td.get("client_secret"),
        scopes=td.get("scopes"),
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        td["token"] = creds.token
        with open(TOKEN_PATH, "w") as f:
            json.dump(td, f, indent=2)

    return build("drive", "v3", credentials=creds, cache_discovery=False)


def find_folder(drive, name, parent_id=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    res = drive.files().list(q=q, fields="files(id,name)", spaces="drive").execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None


def get_or_create_folder(drive, name, parent_id):
    fid = find_folder(drive, name, parent_id)
    if fid:
        return fid
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    f = drive.files().create(body=meta, fields="id").execute()
    return f["id"]


def find_doc(drive, title, folder_id):
    """Return an existing non-trashed Google Doc with this exact title in folder."""
    escaped = title.replace("'", "\\'")
    q = (
        f"name='{escaped}' and "
        "mimeType='application/vnd.google-apps.document' and "
        f"'{folder_id}' in parents and trashed=false"
    )
    res = drive.files().list(q=q, fields="files(id,name)", spaces="drive", pageSize=10).execute()
    files = res.get("files", [])
    return files[0] if files else None


def doc_url(file_id):
    return f"https://docs.google.com/document/d/{file_id}/edit"


def create_doc(drive, title, content, folder_id):
    """Upload plain text, auto-convert to Google Doc, place in folder. Idempotent by title+folder."""
    existing = find_doc(drive, title, folder_id)
    if existing:
        print(f"↩️  Existing doc reused: {title}")
        return doc_url(existing["id"])
    media = MediaInMemoryUpload(content.encode("utf-8"), mimetype="text/plain", resumable=False)
    meta  = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [folder_id],
    }
    f = drive.files().create(body=meta, media_body=media, fields="id").execute()
    return doc_url(f["id"])


def create_doc_from_docx(drive, title, content_bytes, folder_id):
    """Upload a .docx binary, auto-convert to Google Doc, place in folder. Idempotent by title+folder."""
    existing = find_doc(drive, title, folder_id)
    if existing:
        print(f"↩️  Existing doc reused: {title}")
        return doc_url(existing["id"])
    media = MediaInMemoryUpload(
        content_bytes,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        resumable=False
    )
    meta = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [folder_id],
    }
    f = drive.files().create(body=meta, media_body=media, fields="id").execute()
    return doc_url(f["id"])


def list_folders(drive):
    root_id = find_folder(drive, ROOT_FOLDER)
    if not root_id:
        print(f"ERROR: '{ROOT_FOLDER}' not found. Make sure you're authorised as the right Google account.")
        sys.exit(1)
    print(f"{ROOT_FOLDER}/")
    q = f"'{root_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    for p in drive.files().list(q=q, fields="files(id,name)", orderBy="name").execute().get("files", []):
        print(f"  {p['name']}/")
        q2 = f"'{p['id']}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        for s in drive.files().list(q=q2, fields="files(id,name)", orderBy="name").execute().get("files", []):
            print(f"    {s['name']}/")


def get_folder_by_path(drive, path_str):
    """
    Traverse or create folders along a slash-separated path under Eve — Drafts.
    e.g. "Consulting/Clients/H.C. Oswald/Outreach/LinkedIn"
    """
    root_id = find_folder(drive, ROOT_FOLDER)
    if not root_id:
        print(f"ERROR: '{ROOT_FOLDER}' folder not found in your Drive.")
        sys.exit(1)
    parts = [p.strip() for p in path_str.split("/") if p.strip()]
    parent = root_id
    for part in parts:
        parent = get_or_create_folder(drive, part, parent)
    return parent, path_str


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title",        help="Document title")
    parser.add_argument("--path",         help="Full folder path under Eve — Drafts (slash-separated). "
                                               "e.g. 'Consulting/Clients/H.C. Oswald/Outreach/LinkedIn'")
    parser.add_argument("--project",      help="Legacy: top-level project folder")
    parser.add_argument("--type",         help="Legacy: subfolder under project")
    parser.add_argument("--content",      help="Document text (use \\n for newlines)")
    parser.add_argument("--file",         help="Path to a text/markdown file to use as content")
    parser.add_argument("--list-folders", action="store_true")
    args = parser.parse_args()

    drive = get_drive()

    if args.list_folders:
        list_folders(drive)
        return

    if not args.title:
        parser.error("--title is required")

    # Enforce title naming standards
    check_title(args.title)

    # Resolve folder
    if args.path:
        folder_id, display_path = get_folder_by_path(drive, args.path)
    elif args.project and args.type:
        root_id = find_folder(drive, ROOT_FOLDER)
        if not root_id:
            print(f"ERROR: '{ROOT_FOLDER}' folder not found in your Drive.")
            sys.exit(1)
        project_id = get_or_create_folder(drive, args.project, root_id)
        folder_id  = get_or_create_folder(drive, args.type, project_id)
        display_path = f"{args.project}/{args.type}"
    else:
        parser.error("Provide --path OR both --project and --type")

    if args.file:
        filepath = os.path.expanduser(args.file)
        if filepath.endswith(".docx"):
            with open(filepath, "rb") as f:
                content_bytes = f.read()
            url = create_doc_from_docx(drive, args.title, content_bytes, folder_id)
        else:
            with open(filepath) as f:
                content = f.read()
            url = create_doc(drive, args.title, content, folder_id)
    elif args.content:
        content = args.content.replace("\\n", "\n")
        url = create_doc(drive, args.title, content, folder_id)
    else:
        parser.error("Provide --content or --file")

    print(f"✅ {args.title}")
    print(f"   {ROOT_FOLDER} / {display_path}")
    print(f"   {url}")


if __name__ == "__main__":
    main()
