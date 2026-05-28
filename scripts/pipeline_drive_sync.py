#!/usr/bin/env python3
"""
pipeline_drive_sync.py — Sync consulting client pipeline artifacts to Google Drive.

Automatically uploads outreach drafts and presentation deck references for any
pipeline client into the structured Consulting/Clients Drive folder.

Usage:
  # Sync both artifacts for a client
  python3 pipeline_drive_sync.py --slug hc-oswald --client "HC Oswald Supply Co"

  # Sync only outreach draft
  python3 pipeline_drive_sync.py --slug hc-oswald --client "HC Oswald Supply Co" --stage outreach

  # Sync only presentation deck link
  python3 pipeline_drive_sync.py --slug hc-oswald --client "HC Oswald Supply Co" --stage deck

  # List all client folders in Drive
  python3 pipeline_drive_sync.py --list

Drive structure created:
  Eve — Drafts/
  └── Consulting/
      └── Clients/
          └── [Client Name]/
              ├── Outreach/LinkedIn/  ← outreach drafts (Google Docs)
              └── Decks/              ← deck links (Google Docs)

Pipeline folder (local): ~/projects/jt-consulting-pipeline/clients/[slug]/
Required files:
  - outreach: clients/[slug]/outreach-draft.md
  - deck:     clients/[slug]/deck-url.txt (URL to Google Slides)

Auth: ~/.openclaw/workspace/config/google-oauth-token.json
"""

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH     = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")
ROOT_FOLDER    = "Eve — Drafts"
PIPELINE_ROOT  = "Consulting"
CLIENTS_FOLDER = "Clients"
CLIENTS_BASE   = os.path.expanduser("~/projects/jt-consulting-pipeline/clients")


def get_drive():
    if not os.path.exists(TOKEN_PATH):
        print(f"ERROR: OAuth token not found at {TOKEN_PATH}")
        print("Run: python3 ~/.openclaw/workspace/scripts/drive_auth.py")
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


def find_root_folder(drive):
    """Return the top-level Eve — Drafts folder, not same-named nested drift folders."""
    q = (
        f"name='{ROOT_FOLDER}' and "
        "mimeType='application/vnd.google-apps.folder' and "
        "trashed=false and 'root' in parents"
    )
    res = drive.files().list(q=q, fields="files(id,name)", spaces="drive", pageSize=10).execute()
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
    print(f"  📁 Created folder: {name}")
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


def create_doc(drive, title, content, folder_id):
    """Create a Google Doc unless the exact title already exists in the target folder."""
    existing = find_doc(drive, title, folder_id)
    if existing:
        print(f"  ↩️  Existing doc reused: {title}")
        return f"https://docs.google.com/document/d/{existing['id']}/edit"
    media = MediaInMemoryUpload(content.encode("utf-8"), mimetype="text/plain", resumable=False)
    meta = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [folder_id],
    }
    f = drive.files().create(body=meta, media_body=media, fields="id").execute()
    return f"https://docs.google.com/document/d/{f['id']}/edit"


def get_client_folder(drive, client_name):
    """Get or create the Drive folder for this client under Consulting/Clients/."""
    root_id        = find_root_folder(drive)
    if not root_id:
        print(f"ERROR: '{ROOT_FOLDER}' not found in Drive.")
        sys.exit(1)
    consulting_id  = get_or_create_folder(drive, PIPELINE_ROOT, root_id)
    clients_id     = get_or_create_folder(drive, CLIENTS_FOLDER, consulting_id)
    client_id      = get_or_create_folder(drive, client_name, clients_id)
    return client_id


def sync_outreach(drive, slug, client_name, client_folder_id):
    outreach_path = Path(CLIENTS_BASE) / slug / "outreach-draft.md"
    if not outreach_path.exists():
        print(f"  ⚠️  outreach-draft.md not found at {outreach_path} — skipping")
        return None

    # Route to Outreach/LinkedIn subfolder
    outreach_id = get_or_create_folder(drive, "Outreach", client_folder_id)
    linkedin_id = get_or_create_folder(drive, "LinkedIn", outreach_id)

    content = outreach_path.read_text()
    title   = f"{client_name} — LinkedIn DM (3-touch)"
    url     = create_doc(drive, title, content, linkedin_id)
    print(f"  ✅ Outreach Draft → {url}")
    return url


def sync_deck(drive, slug, client_name, client_folder_id):
    deck_url_path = Path(CLIENTS_BASE) / slug / "deck-url.txt"
    deck_url = None
    if deck_url_path.exists():
        deck_url = deck_url_path.read_text().strip()

    # Build a reference doc with the Slides link + client context
    if deck_url:
        content = f"""{client_name} — Presentation Deck

Google Slides: {deck_url}

---
This is a reference document. Open the link above to access the full presentation deck.

Client: {client_name}
Pipeline Slug: {slug}
Local path: ~/projects/jt-consulting-pipeline/clients/{slug}/
"""
    else:
        content = f"""{client_name} — Presentation Deck

Deck not yet built for this client.

When the presentation agent completes, update deck-url.txt at:
  ~/projects/jt-consulting-pipeline/clients/{slug}/deck-url.txt

Then re-run:
  python3 pipeline_drive_sync.py --slug {slug} --client "{client_name}" --stage deck
"""

    # Route to Decks subfolder
    decks_id = get_or_create_folder(drive, "Decks", client_folder_id)
    title = f"{client_name} — Presentation Deck"
    url   = create_doc(drive, title, content, decks_id)
    if deck_url:
        print(f"  ✅ Presentation Deck reference → {url}")
    else:
        print(f"  ⚠️  Deck not built yet — placeholder created → {url}")
    return url


def list_clients(drive):
    root_id = find_root_folder(drive)
    if not root_id:
        print(f"'{ROOT_FOLDER}' not found.")
        return
    pipeline_id = find_folder(drive, PIPELINE_ROOT, root_id)
    if not pipeline_id:
        print(f"No '{PIPELINE_ROOT}' folder yet.")
        return
    print(f"\n{ROOT_FOLDER} / {PIPELINE_ROOT}/")
    q = f"'{pipeline_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    clients = drive.files().list(q=q, fields="files(id,name)", orderBy="name").execute().get("files", [])
    if not clients:
        print("  (empty — no clients synced yet)")
        return
    for c in clients:
        print(f"  📁 {c['name']}")
        q2 = f"'{c['id']}' in parents and trashed=false"
        docs = drive.files().list(q=q2, fields="files(id,name,mimeType)", orderBy="name").execute().get("files", [])
        for d in docs:
            icon = "📄" if "document" in d["mimeType"] else "📊"
            print(f"      {icon} {d['name']}")
    print()


def sync_agentforce_artifacts(drive, slug, client_name, client_folder_id):
    """Sync Agentforce-specific pipeline artifacts: agent-config.md + demo-transcript.md"""
    base = Path(CLIENTS_BASE) / slug

    # Agent config
    config_path = base / "agent-config.md"
    if config_path.exists():
        research_id = get_or_create_folder(drive, "Research", client_folder_id)
        content = config_path.read_text()
        title = f"{client_name} — Agentforce Agent Config"
        url = create_doc(drive, title, content, research_id)
        print(f"  ✅ Agent Config → {url}")
    else:
        print(f"  ⚠️  agent-config.md not found — skipping")

    # Demo transcript
    transcript_path = base / "demo-transcript.md"
    if transcript_path.exists():
        research_id = get_or_create_folder(drive, "Research", client_folder_id)
        content = transcript_path.read_text()
        title = f"{client_name} — Agentforce Demo Transcript"
        url = create_doc(drive, title, content, research_id)
        print(f"  ✅ Demo Transcript → {url}")
    else:
        print(f"  ⚠️  demo-transcript.md not found — skipping")


def main():
    parser = argparse.ArgumentParser(description="Sync consulting pipeline artifacts to Google Drive")
    parser.add_argument("--slug",     help="Client slug (e.g. hc-oswald)")
    parser.add_argument("--client",   help='Client display name (e.g. "HC Oswald Supply Co")')
    parser.add_argument("--stage",    choices=["outreach", "deck", "agentforce", "all"], default="all",
                        help="Which artifact to sync (default: all). Use 'agentforce' for agent-config + demo-transcript.")
    parser.add_argument("--platform", choices=["n8n", "agentforce", "auto"], default="auto",
                        help="Platform context: auto-detects based on files present (default: auto)")
    parser.add_argument("--list",     action="store_true", help="List all synced clients in Drive")
    args = parser.parse_args()

    drive = get_drive()

    if args.list:
        list_clients(drive)
        return

    if not args.slug or not args.client:
        parser.error("--slug and --client are both required")

    # Auto-detect platform if not specified
    base = Path(CLIENTS_BASE) / args.slug
    if args.platform == "auto":
        if (base / "demo-transcript.md").exists() or (base / "agent-config.md").exists():
            platform = "agentforce"
        else:
            platform = "n8n"
    else:
        platform = args.platform

    print(f"\n🔄 Syncing: {args.client} (platform={platform}, stage={args.stage})")
    client_folder_id = get_client_folder(drive, args.client)

    if args.stage in ("outreach", "all"):
        sync_outreach(drive, args.slug, args.client, client_folder_id)

    if args.stage in ("deck", "all"):
        sync_deck(drive, args.slug, args.client, client_folder_id)

    if args.stage in ("agentforce", "all") and platform == "agentforce":
        sync_agentforce_artifacts(drive, args.slug, args.client, client_folder_id)

    print(f"\n📂 Drive: Eve — Drafts / {PIPELINE_ROOT} / {args.client}\n")


if __name__ == "__main__":
    main()
