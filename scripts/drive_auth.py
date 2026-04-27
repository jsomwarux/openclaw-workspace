#!/usr/bin/env python3
"""
drive_auth.py — One-time OAuth2 authorization for Google Drive access.
Run this once. It opens your browser, you click Allow, and saves a token
that drive_drafts.py uses automatically from then on.

Usage: python3 drive_auth.py
"""

import os
import warnings
warnings.filterwarnings("ignore")

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json

SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_SECRETS = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-client.json")
TOKEN_PATH = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")

def main():
    if not os.path.exists(CLIENT_SECRETS):
        print(f"ERROR: OAuth client secrets not found at:\n  {CLIENT_SECRETS}")
        print("\nDownload from Google Cloud Console:")
        print("  APIs & Services → Credentials → your OAuth 2.0 Client ID → Download JSON")
        print(f"  Save it to: {CLIENT_SECRETS}")
        return

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
    print("\n" + "="*60)
    print("This will open Chrome. Sign into openclawagenteve14@gmail.com and click Allow.")
    print("="*60)
    creds = flow.run_local_server(
        host="localhost",
        port=0,
        authorization_prompt_message="Open this URL if your browser does not open automatically:\n{url}",
        success_message="Authorization complete. You can close this tab and return to Terminal.",
        open_browser=True,
        prompt="consent",
    )

    # Save token
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes),
    }
    with open(TOKEN_PATH, "w") as f:
        json.dump(token_data, f, indent=2)
    os.chmod(TOKEN_PATH, 0o600)

    print(f"\n✅ Authorization complete! Token saved to:\n  {TOKEN_PATH}")
    print("\nYou won't need to do this again — drive_drafts.py will use this token automatically.")

if __name__ == "__main__":
    main()
