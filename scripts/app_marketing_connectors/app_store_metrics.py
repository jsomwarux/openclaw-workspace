from __future__ import annotations

import base64
import csv
import gzip
import io
import json
import os
import time
import urllib.parse
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

ROOT = Path.home() / ".openclaw" / "workspace"
ENV_PATH = Path.home() / ".config" / "env" / "global.env"
STATUS_PATH = ROOT / "memory" / "app-marketing" / "app-store-metrics-status.json"
API_BASE = "https://api.appstoreconnect.apple.com/v1"


def _load_env() -> None:
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _jwt() -> str:
    _load_env()
    issuer = os.environ["APPSTORE_ISSUER_ID"]
    key_id = os.environ["APPSTORE_KEY_ID"]
    key_path = Path(os.environ["APPSTORE_PRIVATE_KEY_PATH"]).expanduser()
    now = int(time.time())
    header = {"alg": "ES256", "kid": key_id, "typ": "JWT"}
    payload = {"iss": issuer, "iat": now, "exp": now + 20 * 60, "aud": "appstoreconnect-v1"}
    signing_input = f"{_b64url(json.dumps(header, separators=(',', ':')).encode())}.{_b64url(json.dumps(payload, separators=(',', ':')).encode())}".encode()
    private_key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
    if not isinstance(private_key, ec.EllipticCurvePrivateKey):
        raise TypeError("App Store Connect private key is not ES256/EC")
    der_sig = private_key.sign(signing_input, ec.ECDSA(hashes.SHA256()))
    r, s = utils.decode_dss_signature(der_sig)
    raw_sig = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    return f"{signing_input.decode()}.{_b64url(raw_sig)}"


def _api_get(path: str, token: str, *, raw: bool = False, accept: str = "application/json") -> Any:
    req = Request(f"{API_BASE}{path}", headers={"Authorization": f"Bearer {token}", "Accept": accept})
    with urlopen(req, timeout=30) as resp:
        body = resp.read()
        if raw:
            return body
        return json.loads(body.decode("utf-8"))


def _safe_api_get(path: str, token: str, *, raw: bool = False, accept: str = "application/json") -> tuple[bool, Any, str | None]:
    try:
        return True, _api_get(path, token, raw=raw, accept=accept), None
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:1500]
        return False, None, f"HTTP {e.code}: {body}"
    except URLError as e:
        return False, None, f"NETWORK: {e.reason}"
    except Exception as e:  # noqa: BLE001
        return False, None, f"{type(e).__name__}: {e}"


def _is_no_sales_report(err: str | None) -> bool:
    if not err:
        return False
    lowered = err.lower()
    return "http 404" in lowered and "no sales for the date specified" in lowered


def readiness() -> dict:
    """Return non-secret App Store connector readiness for audit/status reports."""
    _load_env()
    needed = ["APPSTORE_ISSUER_ID", "APPSTORE_KEY_ID", "APPSTORE_PRIVATE_KEY_PATH", "APPSTORE_VISTA_APP_ID"]
    present = {k: bool(os.environ.get(k)) for k in needed}
    key_path = os.environ.get("APPSTORE_PRIVATE_KEY_PATH")
    key_exists = bool(key_path and Path(key_path).expanduser().exists())
    status = "missing_secure_credentials_or_permissions"
    app_ok = False
    app_name = None
    vendor_numbers: list[str] = []
    reporting_status = "not_checked"
    reporting_error = None
    blocked_details: list[str] = []
    if all(present.values()) and key_exists:
        try:
            token = _jwt()
            ok, app, err = _safe_api_get(f"/apps/{os.environ['APPSTORE_VISTA_APP_ID']}", token)
            app_ok = ok
            if ok:
                app_name = ((app.get("data") or {}).get("attributes") or {}).get("name")
                status = "metadata_ready"
            else:
                reporting_error = err
            vendor = os.environ.get("APPSTORE_VENDOR_NUMBER")
            if vendor:
                vendor_numbers.append("configured")
                report_path = f"/salesReports?filter[frequency]=DAILY&filter[reportDate]=2026-05-12&filter[reportSubType]=SUMMARY&filter[reportType]=SALES&filter[vendorNumber]={urllib.parse.quote(vendor)}"
                ok, report, err = _safe_api_get(report_path, token, raw=True, accept="application/a-gzip")
                if ok:
                    reporting_status = "sales_report_ready"
                    status = "reporting_ready"
                elif _is_no_sales_report(err):
                    # Apple returns 404 when the vendor/reporting path is valid but the
                    # selected report date has no sales. Treat that as reporting access
                    # working with a zero-sales day, not a permission/config blocker.
                    reporting_status = "sales_report_ready_zero_sales"
                    status = "reporting_ready"
                    reporting_error = None
                else:
                    reporting_status = "reporting_blocked_or_permission_gap"
                    reporting_error = err
                    blocked_details.append("Apple sales report endpoint rejected the configured vendor number/API key; JT may need to accept agreements or grant reporting access in App Store Connect.")
            else:
                # Apple reporting APIs require a vendor number not available from the app metadata endpoint.
                reporting_status = "vendor_number_needed"
                status = "metadata_ready_vendor_number_needed"
                blocked_details.append("APPSTORE_VENDOR_NUMBER is missing from approved secure env/config; Apple does not expose it through the app metadata endpoint.")
        except Exception as e:  # noqa: BLE001
            reporting_error = f"{type(e).__name__}: {e}"
            blocked_details.append("Connector could not complete the App Store readiness probe; inspect reporting_error without exposing secrets.")
    result = {
        "connector": "app_store",
        "implemented": True,
        "env_present": present,
        "private_key_path_exists": key_exists,
        "metadata_auth_ok": app_ok,
        "app_name": app_name,
        "reporting_status": reporting_status,
        "reporting_error": reporting_error,
        "vendor_numbers_configured": vendor_numbers,
        "status": status,
        "status_reason": reporting_status,
        "blocked_details": blocked_details,
        "approved_secret_surface": "approved env/config only; never docs/chat/repo",
        "diagnostic_command": "cd ~/.openclaw/workspace && python3 scripts/app_marketing_connectors/app_store_metrics.py",
        "collector_command": "cd ~/.openclaw/workspace && python3 scripts/app_marketing_collect_metrics.py",
        "next_action": "If reporting_status starts with sales_report_ready, App Store reporting access is wired; wait for sales/download report availability or expand report-date scanning. If permission-blocked, fix Apple reporting role/agreements.",
    }
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(result, indent=2))
    return result


def fetch(post: dict) -> dict | None:
    """Return App Store metadata/readiness row for scoreboard.

    Full download/impression reporting requires Apple vendor-number/reporting access.
    Until that exists, emit a precise metadata row instead of pretending metrics are complete.
    """
    info = readiness()
    if not info.get("metadata_auth_ok"):
        return None
    captured = date.today().isoformat()
    return {
        "date": captured,
        "week_of": post.get("week_of") or captured,
        "platform": "app_store",
        "product_slug": post.get("product_slug") or "vista",
        "content_id_or_hook": post.get("hook_or_title") or "Vista App Store reporting readiness",
        "url": post.get("url_or_id") or os.environ.get("APPSTORE_VISTA_APP_ID"),
        "post_id": post.get("post_id") or os.environ.get("APPSTORE_VISTA_APP_ID"),
        "views_or_impressions": None,
        "likes": None,
        "comments": None,
        "saves": None,
        "reposts": None,
        "captured_at": captured,
        "status": info.get("status"),
        "reporting_status": info.get("reporting_status"),
        "notes": "App Store metadata auth works; sales report access is wired when reporting_status starts with sales_report_ready. Apple may return zero/no-sales for quiet dates.",
        "blocked_details": info.get("blocked_details"),
    }


if __name__ == "__main__":
    print(json.dumps(readiness(), indent=2))
