from __future__ import annotations

import os


def fetch(post: dict) -> dict | None:
    """App Store Connect analytics connector placeholder.

    Requires App Store Connect API issuer/key id/private key configured securely outside
    workspace docs. Do not store Apple private keys in repo/workspace notes.
    """
    needed=['APPSTORE_ISSUER_ID','APPSTORE_KEY_ID','APPSTORE_PRIVATE_KEY_PATH']
    if not all(os.environ.get(k) for k in needed):
        return None
    return None
