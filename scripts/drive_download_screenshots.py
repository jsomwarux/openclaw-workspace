#!/usr/bin/env python3
"""
drive_download_screenshots.py — Download app screenshot files from Google Drive for vibe marketing.

Usage:
  python3 drive_download_screenshots.py --product nash-satoshi --output-dir /tmp/screenshots/
  python3 drive_download_screenshots.py --product vista --output-dir /tmp/screenshots/
  python3 drive_download_screenshots.py --list --product nash-satoshi

Drive path: Eve — Drafts / Vibe Marketing / App Screenshots / [product-slug] /

Requires: config/google-oauth-token.json (same auth as drive_drafts.py)
"""

import argparse
import io
import json
import os
import sys
import warnings
warnings.filterwarnings("ignore")

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH   = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")
ROOT_FOLDER  = "Eve — Drafts"
SCREENSHOTS_PATH = ["Vibe Marketing", "App Screenshots"]   # under root

# Supported image extensions
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def get_drive():
    if not os.path.exists(TOKEN_PATH):
        print(f"ERROR: OAuth token not found at {TOKEN_PATH}")
        print("Run:  python3 ~/.openclaw/workspace/scripts/drive_auth.py")
        sys.exit(1)
    with open(TOKEN_PATH) as f:
        td = json.load(f)
    creds = Credentials(
        token=td.get("token"),
        refresh_token=td.get("refresh_token"),
        token_uri=td.get("token_uri"),
        client_id=td.get("client_id"),
        client_secret=td.get("client_secret"),
        scopes=td.get("scopes", ["https://www.googleapis.com/auth/drive"]),
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w") as f:
            json.dump({
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": list(creds.scopes),
            }, f, indent=2)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def find_folder(service, name, parent_id=None):
    """Find a folder by name under parent_id (or root if None)."""
    q = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    results = service.files().list(q=q, fields="files(id,name)", pageSize=10).execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def resolve_path(service, path_parts):
    """Resolve a sequence of folder names into a folder ID."""
    parent_id = None
    for part in path_parts:
        fid = find_folder(service, part, parent_id)
        if not fid:
            return None
        parent_id = fid
    return parent_id


def list_files_in_folder(service, folder_id):
    """List all files in a folder (non-recursive)."""
    q = f"'{folder_id}' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'"
    results = service.files().list(q=q, fields="files(id,name,mimeType,size)", pageSize=100).execute()
    return results.get("files", [])


def download_file(service, file_id, dest_path):
    """Download a binary file from Drive."""
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.close()


def main():
    parser = argparse.ArgumentParser(description="Download app screenshots from Drive for vibe marketing.")
    parser.add_argument("--product", required=True, help="Product slug: nash-satoshi or vista")
    parser.add_argument("--output-dir", help="Local directory to save downloaded files")
    parser.add_argument("--list", action="store_true", help="List available screenshots without downloading")
    args = parser.parse_args()

    service = get_drive()

    # Resolve path: Eve — Drafts / Vibe Marketing / App Screenshots / [product]
    full_path = [ROOT_FOLDER] + SCREENSHOTS_PATH + [args.product]
    folder_id = resolve_path(service, full_path)

    if not folder_id:
        print(f"⚠️  Folder not found: {' / '.join(full_path)}")
        print(f"Create it in Drive and upload screenshots to: {' / '.join(full_path)}")
        sys.exit(0)

    files = list_files_in_folder(service, folder_id)
    image_files = [f for f in files if os.path.splitext(f["name"].lower())[1] in IMAGE_EXTS]

    if not image_files:
        print(f"⚠️  No image files found in {' / '.join(full_path)}")
        print("Upload .png or .jpg screenshots to that folder.")
        sys.exit(0)

    if args.list:
        print(f"📸 Screenshots available for {args.product} ({len(image_files)} files):")
        for f in image_files:
            size_kb = int(f.get("size", 0)) // 1024
            print(f"  {f['name']} ({size_kb}KB)")
        sys.exit(0)

    # Download
    if not args.output_dir:
        print("ERROR: --output-dir required for download")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    downloaded = []
    for f in image_files:
        dest = os.path.join(args.output_dir, f["name"])
        print(f"Downloading {f['name']}...")
        download_file(service, f["id"], dest)
        downloaded.append(dest)

    print(f"\n✅ Downloaded {len(downloaded)} screenshots to {args.output_dir}")
    for path in downloaded:
        print(f"  {path}")
    return downloaded


if __name__ == "__main__":
    main()
