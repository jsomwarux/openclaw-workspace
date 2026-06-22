#!/usr/bin/env python3
"""Upload generated job application docx files to Drive as Google Docs."""

import argparse
import json
import os
import warnings

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


TOKEN_PATH = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")
ROOT_FOLDER = "Eve — Drafts"
JOB_APPLICATIONS = "Job Applications"


def drive_service():
    warnings.filterwarnings("ignore")
    with open(TOKEN_PATH) as f:
        td = json.load(f)
    creds = Credentials(
        token=td["token"],
        refresh_token=td["refresh_token"],
        token_uri=td["token_uri"],
        client_id=td["client_id"],
        client_secret=td["client_secret"],
        scopes=td["scopes"],
    )
    if creds.expired:
        creds.refresh(Request())
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def find_folder(drive, name, parent_id=None):
    safe_name = name.replace("'", "\\'")
    q = f"name='{safe_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    result = drive.files().list(q=q, fields="files(id,name)", pageSize=10).execute()
    files = result.get("files", [])
    return files[0]["id"] if files else None


def upload_docx(drive, path, folder_id, title):
    metadata = {
        "name": title,
        "parents": [folder_id],
        "mimeType": "application/vnd.google-apps.document",
    }
    media = MediaFileUpload(
        path,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        resumable=False,
    )
    result = drive.files().create(body=metadata, media_body=media, fields="id,webViewLink").execute()
    return result["webViewLink"]


def main():
    parser = argparse.ArgumentParser(description="Upload job application resume and cover letter docx files.")
    parser.add_argument("--resume-docx", required=True)
    parser.add_argument("--cover-letter-docx", required=True)
    parser.add_argument("--resume-title", required=True)
    parser.add_argument("--cover-letter-title", required=True)
    args = parser.parse_args()

    drive = drive_service()
    root_id = find_folder(drive, ROOT_FOLDER)
    if not root_id:
        raise SystemExit(f"Drive folder not found: {ROOT_FOLDER}")
    job_apps_id = find_folder(drive, JOB_APPLICATIONS, root_id)
    if not job_apps_id:
        raise SystemExit(f"Drive folder not found: {ROOT_FOLDER} / {JOB_APPLICATIONS}")
    resumes_id = find_folder(drive, "Resumes", job_apps_id)
    cover_letters_id = find_folder(drive, "Cover Letters", job_apps_id)
    if not resumes_id or not cover_letters_id:
        raise SystemExit("Drive folders not found: Resumes and/or Cover Letters under Job Applications")

    resume_link = upload_docx(drive, args.resume_docx, resumes_id, args.resume_title)
    cover_letter_link = upload_docx(drive, args.cover_letter_docx, cover_letters_id, args.cover_letter_title)
    print(json.dumps({"resume": resume_link, "cover_letter": cover_letter_link}, indent=2))


if __name__ == "__main__":
    main()
