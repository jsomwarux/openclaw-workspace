#!/usr/bin/env python3
"""
Reorganizes Content/X and Content/LinkedIn Drive folders into subfolders.
Creates: Weekly/, News Hooks/, Bank/, Archive/ under each platform folder.
Moves files to correct subfolder. Superseded drafts go to Archive/.
"""

import os, json, sys, warnings
warnings.filterwarnings("ignore")

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

TOKEN_PATH = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")
with open(TOKEN_PATH) as f:
    td = json.load(f)
creds = Credentials(
    token=td.get("token"), refresh_token=td.get("refresh_token"),
    token_uri="https://oauth2.googleapis.com/token",
    client_id=td.get("client_id"), client_secret=td.get("client_secret"),
    scopes=td.get("scopes", ["https://www.googleapis.com/auth/drive"]),
)
service = build("drive", "v3", credentials=creds)

def find_folder(name, parent_id=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    elif name == "Eve — Drafts":
        q += " and 'root' in parents"
    r = service.files().list(q=q, fields="files(id,name)").execute()
    files = r.get("files", [])
    return files[0]["id"] if files else None

def create_folder(name, parent_id):
    existing = find_folder(name, parent_id)
    if existing:
        return existing
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
    f = service.files().create(body=meta, fields="id").execute()
    print(f"  Created folder: {name}")
    return f["id"]

def move_file(file_id, new_parent_id, old_parent_id):
    service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=old_parent_id,
        fields="id,parents"
    ).execute()

def list_folder(folder_id):
    r = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id,name,mimeType,createdTime)",
        orderBy="createdTime"
    ).execute()
    return r.get("files", [])

# ── Find root folders ──────────────────────────────────────────────────────────
root = find_folder("Eve — Drafts")
content = find_folder("Content", root)
x_folder = find_folder("X", content)
li_folder = find_folder("LinkedIn", content)

print(f"Root: {root}")
print(f"Content: {content}")
print(f"X folder: {x_folder}")
print(f"LinkedIn folder: {li_folder}")

# ── Create subfolders ──────────────────────────────────────────────────────────
print("\n--- Creating subfolders ---")
x_weekly   = create_folder("Weekly",     x_folder)
x_hooks    = create_folder("News Hooks", x_folder)
x_bank     = create_folder("Bank",       x_folder)
x_archive  = create_folder("Archive",    x_folder)

li_weekly  = create_folder("Weekly",     li_folder)
li_hooks   = create_folder("News Hooks", li_folder)
li_bank    = create_folder("Bank",       li_folder)
li_archive = create_folder("Archive",    li_folder)

# ── Define routing rules ───────────────────────────────────────────────────────
# X files: (file_id_prefix, destination_folder_id, label)
x_routing = [
    # Superseded / old stale
    ("11x1KURJo0e_", x_archive,  "X Content — Week of 2026-03-10 → Archive"),
    ("1gqi8oRb0T-y", x_archive,  "JT Somwaru — Friday X Posts — March 13 → Archive"),
    # Current weekly
    ("1zM_DyeTQXTK", x_weekly,   "X Content — Week of 2026-03-16 → Weekly"),
    # News hooks
    ("1-AbMpx5stos", x_hooks,    "News Hook — 2026-03-16 → News Hooks"),
    ("1zuPvpuGs-5F", x_hooks,    "News Hook — 2026-03-17 → News Hooks"),
    # Bank posts
    ("1jzy-jNHFaqM", x_bank,     "Content Bank — Week of 2026-03-16 → Bank"),
    ("19tOrOkWAlqv", x_bank,     "Auto-detected agentguard-governance → Bank"),
    ("1qN-ZSoc7uwU", x_bank,     "Auto-detected agentguard-confidence → Bank"),
]

# LinkedIn files: superseded drafts of same week → Archive, keep only final
li_routing = [
    # Superseded / old
    ("1s_F9sXMqjUr", li_archive, "LinkedIn Week of 2026-03-10 → Archive"),
    ("1yniSeIystuZ", li_archive, "JT Somwaru — Friday LinkedIn March 13 → Archive"),
    ("1iwkrRC0w67Q", li_archive, "LinkedIn Week of 2026-03-16 (orig) → Archive"),
    ("1WAKoMo2Lhko", li_archive, "LinkedIn Week of 2026-03-16 (+Tue+Thu) → Archive"),
    ("1uWX6nLrdqCL", li_archive, "LinkedIn Week of 2026-03-16 (v2) → Archive"),
    # Current weekly (final is canonical)
    ("1ADJw6xo81mU", li_weekly,  "LinkedIn Week of 2026-03-16 (final) → Weekly"),
    # News hooks — superseded drafts → archive, final → news hooks
    ("13ypiAeZRI_L", li_archive, "News Hook LinkedIn 2026-03-16 (draft) → Archive"),
    ("1OF9toG9hqbp", li_archive, "McKinsey LinkedIn (revised) → Archive"),
    ("1F7QCxUa2xsN", li_hooks,   "McKinsey LinkedIn (final) → News Hooks"),
    ("1UL4hJ030qve", li_hooks,   "News Hook LinkedIn 2026-03-17 → News Hooks"),
    # Bank
    ("1PFLHPBZJHq-", li_bank,    "LinkedIn Bank — Week of 2026-03-16 Backup Swaps → Bank"),
    ("1V3Ark5vihXA", li_bank,    "Auto-detected LinkedIn agentguard → Bank"),
]

# ── Execute moves ──────────────────────────────────────────────────────────────
print("\n--- Moving X files ---")
x_files = list_folder(x_folder)
x_file_map = {f["id"][:12]: f for f in x_files}

for prefix, dest, label in x_routing:
    matched = next((f for fid, f in x_file_map.items() if fid.startswith(prefix[:12])), None)
    if matched:
        move_file(matched["id"], dest, x_folder)
        print(f"  ✓ {label}")
    else:
        print(f"  ⚠ Not found: {prefix} ({label})")

print("\n--- Moving LinkedIn files ---")
li_files = list_folder(li_folder)
li_file_map = {f["id"][:12]: f for f in li_files}

for prefix, dest, label in li_routing:
    matched = next((f for fid, f in li_file_map.items() if fid.startswith(prefix[:12])), None)
    if matched:
        move_file(matched["id"], dest, li_folder)
        print(f"  ✓ {label}")
    else:
        print(f"  ⚠ Not found: {prefix} ({label})")

print("\n--- Done. Final folder state ---")
for label, folder_id in [("X/Weekly", x_weekly), ("X/News Hooks", x_hooks), ("X/Bank", x_bank), ("X/Archive", x_archive),
                          ("LinkedIn/Weekly", li_weekly), ("LinkedIn/News Hooks", li_hooks), ("LinkedIn/Bank", li_bank), ("LinkedIn/Archive", li_archive)]:
    files = list_folder(folder_id)
    print(f"\n  📁 {label} ({len(files)} files)")
    for f in files:
        print(f"    📄 {f['name']}")
