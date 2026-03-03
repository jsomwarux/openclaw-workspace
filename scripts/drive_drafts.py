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


def create_doc(drive, title, content, folder_id):
    """Upload plain text, auto-convert to Google Doc, place in folder."""
    media = MediaInMemoryUpload(content.encode("utf-8"), mimetype="text/plain", resumable=False)
    meta  = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [folder_id],
    }
    f = drive.files().create(body=meta, media_body=media, fields="id").execute()
    return f"https://docs.google.com/document/d/{f['id']}/edit"


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title",        help="Document title")
    parser.add_argument("--project",      help="Project folder (e.g. Vista, Nash Satoshi, Opticfy)")
    parser.add_argument("--type",         help="Content type subfolder (e.g. 'X Threads', Reddit, 'Product Hunt')")
    parser.add_argument("--content",      help="Document text (use \\n for newlines)")
    parser.add_argument("--file",         help="Path to a text/markdown file to use as content")
    parser.add_argument("--list-folders", action="store_true")
    args = parser.parse_args()

    drive = get_drive()

    if args.list_folders:
        list_folders(drive)
        return

    if not all([args.title, args.project, args.type]):
        parser.error("--title, --project, and --type are all required")

    if args.file:
        with open(os.path.expanduser(args.file)) as f:
            content = f.read()
    elif args.content:
        content = args.content.replace("\\n", "\n")
    else:
        parser.error("Provide --content or --file")

    root_id    = find_folder(drive, ROOT_FOLDER)
    if not root_id:
        print(f"ERROR: '{ROOT_FOLDER}' folder not found in your Drive.")
        sys.exit(1)

    project_id = get_or_create_folder(drive, args.project, root_id)
    type_id    = get_or_create_folder(drive, args.type, project_id)
    url        = create_doc(drive, args.title, content, type_id)

    print(f"✅ {args.title}")
    print(f"   {ROOT_FOLDER} / {args.project} / {args.type}")
    print(f"   {url}")


if __name__ == "__main__":
    main()
