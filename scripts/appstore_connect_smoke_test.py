#!/usr/bin/env python3
"""Smoke test App Store Connect API credentials without printing secrets.

Loads APPSTORE_* values from ~/.config/env/global.env, signs an ES256 JWT using
cryptography, and fetches the configured Vista app record.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

API_BASE = "https://api.appstoreconnect.apple.com/v1"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def make_jwt(issuer_id: str, key_id: str, private_key_path: Path) -> str:
    now = int(time.time())
    header = {"alg": "ES256", "kid": key_id, "typ": "JWT"}
    payload = {
        "iss": issuer_id,
        "iat": now,
        "exp": now + 20 * 60,
        "aud": "appstoreconnect-v1",
    }

    signing_input = f"{b64url(json.dumps(header, separators=(',', ':')).encode())}.{b64url(json.dumps(payload, separators=(',', ':')).encode())}".encode()

    private_key = serialization.load_pem_private_key(
        private_key_path.read_bytes(),
        password=None,
    )
    if not isinstance(private_key, ec.EllipticCurvePrivateKey):
        raise TypeError("Private key is not an EC private key; App Store Connect keys should be ES256/EC.")

    der_sig = private_key.sign(signing_input, ec.ECDSA(hashes.SHA256()))
    r, s = utils.decode_dss_signature(der_sig)
    raw_sig = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    return f"{signing_input.decode()}.{b64url(raw_sig)}"


def api_get(path: str, token: str) -> Dict:
    req = Request(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    load_env_file(Path.home() / ".config/env/global.env")

    required = [
        "APPSTORE_ISSUER_ID",
        "APPSTORE_KEY_ID",
        "APPSTORE_PRIVATE_KEY_PATH",
        "APPSTORE_VISTA_APP_ID",
    ]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print("FAIL missing_env=" + ",".join(missing))
        return 2

    key_path = Path(os.environ["APPSTORE_PRIVATE_KEY_PATH"]).expanduser()
    if not key_path.exists() or key_path.stat().st_size == 0:
        print(f"FAIL private_key_file_missing_or_empty path={key_path}")
        return 2

    try:
        token = make_jwt(os.environ["APPSTORE_ISSUER_ID"], os.environ["APPSTORE_KEY_ID"], key_path)
        app_id = os.environ["APPSTORE_VISTA_APP_ID"]
        data = api_get(f"/apps/{app_id}", token)
        attrs = data.get("data", {}).get("attributes", {})
        print("OK appstore_connect_auth=success")
        print("app_id=" + str(data.get("data", {}).get("id", "")))
        print("bundle_id=" + str(attrs.get("bundleId", "")))
        print("name=" + str(attrs.get("name", "")))
        print("sku=" + str(attrs.get("sku", "")))
        return 0
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:1000]
        print(f"FAIL http_status={e.code}")
        print(body)
        return 1
    except URLError as e:
        print(f"FAIL network_error={e.reason}")
        return 1
    except Exception as e:
        print(f"FAIL {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
