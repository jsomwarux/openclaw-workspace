#!/usr/bin/env python3
"""
reorganize_drive.py — One-time Drive restructure for JT Somwaru
- Renames "JT Somwaru" → "Consulting" under Eve — Drafts
- Creates new folder hierarchy (Clients, Content, etc.)
- Moves existing files to correct locations
- Deletes Opticfy folders
"""
import json, os, sys, warnings
warnings.filterwarnings("ignore")

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")

def get_creds():
    with open(TOKEN_PATH) as f:
        td = json.load(f)
    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = Credentials(
        token=td.get("token"), refresh_token=td.get("refresh_token"),
        token_uri=td.get("token_uri"), client_id=td.get("client_id"),
        client_secret=td.get("client_secret"), scopes=scopes,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        td["token"] = creds.token
        with open(TOKEN_PATH, "w") as f:
            json.dump(td, f, indent=2)
    return creds

def find_folder(drive, name, parent_id=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    r = drive.files().list(q=q, fields="files(id,name)").execute()
    files = r.get("files", [])
    return files[0]["id"] if files else None

def find_folder_any(drive, name):
    """Find folder by name anywhere in drive."""
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    r = drive.files().list(q=q, fields="files(id,name,parents)").execute()
    return r.get("files", [])

def find_files_in_folder(drive, parent_id):
    q = f"'{parent_id}' in parents and trashed=false"
    r = drive.files().list(q=q, fields="files(id,name,mimeType)").execute()
    return r.get("files", [])

def create_folder(drive, name, parent_id):
    body = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
    return drive.files().create(body=body, fields="id").execute()["id"]

def get_or_create(drive, name, parent_id):
    existing = find_folder(drive, name, parent_id)
    if existing:
        print(f"    exists: {name}/")
        return existing
    fid = create_folder(drive, name, parent_id)
    print(f"    created: {name}/")
    return fid

def move_file(drive, file_id, new_parent_id, old_parent_id):
    drive.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=old_parent_id,
        fields="id,parents"
    ).execute()

def trash_folder(drive, folder_id, name):
    drive.files().update(fileId=folder_id, body={"trashed": True}).execute()
    print(f"  🗑  Trashed: {name}")

def main():
    creds = get_creds()
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    # ── 1. Find root: Eve — Drafts ───────────────────────────────────────────
    print("Finding Eve — Drafts root...")
    eve_drafts_id = find_folder(drive, "Eve — Drafts")
    if not eve_drafts_id:
        print("ERROR: Eve — Drafts folder not found")
        sys.exit(1)
    print(f"  Found Eve — Drafts: {eve_drafts_id}")

    # ── 2. Rename "JT Somwaru" → "Consulting" ───────────────────────────────
    print("\nRenaming JT Somwaru → Consulting...")
    jt_somwaru_id = find_folder(drive, "JT Somwaru", eve_drafts_id)
    if jt_somwaru_id:
        drive.files().update(fileId=jt_somwaru_id, body={"name": "Consulting"}).execute()
        consulting_id = jt_somwaru_id
        print(f"  ✅ Renamed to Consulting")
    else:
        # Maybe already renamed
        consulting_id = find_folder(drive, "Consulting", eve_drafts_id)
        if consulting_id:
            print(f"  Already named Consulting: {consulting_id}")
        else:
            consulting_id = create_folder(drive, "Consulting", eve_drafts_id)
            print(f"  Created Consulting: {consulting_id}")

    # ── 3. Build Consulting subfolder structure ──────────────────────────────
    print("\nBuilding Consulting/ structure...")
    clients_id    = get_or_create(drive, "Clients",    consulting_id)
    get_or_create(drive, "Templates",  consulting_id)
    get_or_create(drive, "Case Studies", consulting_id)

    # H.C. Oswald client folder
    print("  Building Clients/H.C. Oswald/...")
    oswald_id     = get_or_create(drive, "H.C. Oswald", clients_id)
    oswald_out_id = get_or_create(drive, "Outreach",    oswald_id)
    get_or_create(drive, "LinkedIn",  oswald_out_id)
    get_or_create(drive, "Email",     oswald_out_id)
    oswald_decks_id = get_or_create(drive, "Decks",    oswald_id)
    get_or_create(drive, "Research",  oswald_id)

    # ── 4. Build top-level Content/ structure ────────────────────────────────
    print("\nBuilding Content/ structure...")
    content_id = get_or_create(drive, "Content", eve_drafts_id)
    get_or_create(drive, "X",        content_id)
    get_or_create(drive, "LinkedIn", content_id)

    # ── 5. Ensure Job Applications/ has subfolders ───────────────────────────
    print("\nChecking Job Applications/...")
    job_apps_id = find_folder(drive, "Job Applications", consulting_id)
    if not job_apps_id:
        job_apps_id = find_folder(drive, "Job Applications", eve_drafts_id)
    if job_apps_id:
        get_or_create(drive, "Resumes",        job_apps_id)
        get_or_create(drive, "Cover Letters",  job_apps_id)
        print(f"  Job Applications found and subfoldered")
    else:
        job_apps_id = get_or_create(drive, "Job Applications", eve_drafts_id)
        get_or_create(drive, "Resumes",       job_apps_id)
        get_or_create(drive, "Cover Letters", job_apps_id)

    # ── 6. Move Oswald outreach draft to correct location ────────────────────
    print("\nMoving Oswald outreach draft...")
    # Find it in Client Work or wherever it landed
    def find_file(drive, name_contains, parent_id=None):
        q = f"name contains '{name_contains}' and trashed=false and mimeType != 'application/vnd.google-apps.folder'"
        if parent_id:
            q += f" and '{parent_id}' in parents"
        r = drive.files().list(q=q, fields="files(id,name,parents)").execute()
        return r.get("files", [])

    outreach_files = find_file(drive, "Oswald")
    for f in outreach_files:
        old_parent = f["parents"][0] if f.get("parents") else None
        if old_parent:
            linkedin_folder = find_folder(drive, "LinkedIn", oswald_out_id)
            move_file(drive, f["id"], linkedin_folder, old_parent)
            print(f"  ✅ Moved '{f['name']}' → Consulting/Clients/H.C. Oswald/Outreach/LinkedIn/")

    # ── 7. Move Oswald deck to Clients/H.C. Oswald/Decks/ ───────────────────
    print("\nMoving Oswald deck...")
    oswald_decks = find_file(drive, "H.C. Oswald Supply")
    for f in oswald_decks:
        old_parent = f["parents"][0] if f.get("parents") else None
        if old_parent and old_parent != oswald_decks_id:
            move_file(drive, f["id"], oswald_decks_id, old_parent)
            print(f"  ✅ Moved '{f['name']}' → Consulting/Clients/H.C. Oswald/Decks/")
        else:
            print(f"  Already in Decks: {f['name']}")

    # ── 8. Delete Opticfy folders ─────────────────────────────────────────────
    print("\nRemoving Opticfy folders...")
    opticfy_folders = find_folder_any(drive, "Opticfy")
    if opticfy_folders:
        for f in opticfy_folders:
            trash_folder(drive, f["id"], f["name"])
    else:
        print("  No Opticfy folders found (already gone or never existed)")

    # Also check for "JT Somwaru — Client Pipeline" old folder
    pipeline_folders = find_folder_any(drive, "JT Somwaru — Client Pipeline")
    if pipeline_folders:
        for f in pipeline_folders:
            trash_folder(drive, f["id"], "JT Somwaru — Client Pipeline")

    # ── 9. Print final structure summary ────────────────────────────────────
    print("\n" + "="*50)
    print("✅ Drive restructure complete")
    print("\nNew structure under Eve — Drafts/:")
    print("  Consulting/")
    print("    Clients/")
    print("      H.C. Oswald/")
    print("        Outreach/LinkedIn/")
    print("        Outreach/Email/")
    print("        Decks/")
    print("        Research/")
    print("    Templates/")
    print("    Case Studies/")
    print("  Content/")
    print("    X/")
    print("    LinkedIn/")
    print("  Job Applications/")
    print("    Resumes/")
    print("    Cover Letters/")
    print("  Research/")
    print("  Frameworks/")
    print("  Analysis/")

    return {
        "consulting_id": consulting_id,
        "clients_id": clients_id,
        "oswald_id": oswald_id,
        "content_id": content_id,
    }

if __name__ == "__main__":
    ids = main()
    print(f"\nKey folder IDs:")
    for k, v in ids.items():
        print(f"  {k}: {v}")
