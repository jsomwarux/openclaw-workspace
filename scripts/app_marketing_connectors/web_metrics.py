from __future__ import annotations

import csv
import json
import os
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib import error, parse, request

ROOT = Path.home() / ".openclaw" / "workspace"
ACCOUNT_MAP = ROOT / "memory" / "app-marketing" / "account-map.json"
STATUS_PATH = ROOT / "memory" / "app-marketing" / "web-analytics-status.json"
ENV_PATH = Path.home() / ".config" / "env" / "global.env"
TOKEN_URL = "https://oauth2.googleapis.com/token"
GA4_RUN_REPORT = "https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
GSC_SEARCH_ANALYTICS = "https://searchconsole.googleapis.com/webmasters/v3/sites/{site_url}/searchAnalytics/query"
ACCESS_TOKEN_CACHE = Path.home() / ".cache" / "openclaw" / "app-marketing" / "ga4-oauth-token-cache.json"

GA4_ENV_KEYS = ["GA4_OAUTH_CLIENT_ID", "GA4_OAUTH_CLIENT_SECRET", "GA4_OAUTH_REFRESH_TOKEN"]


def _load_env() -> None:
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _mapping_value(row: dict) -> str | None:
    for key in ("property_id", "site_url", "log_path", "vercel_project", "plausible_site_id", "posthog_project_id"):
        val = row.get(key)
        if val:
            return key
    return None


def _map_rows() -> list[dict]:
    if not ACCOUNT_MAP.exists():
        return []
    try:
        data = json.loads(ACCOUNT_MAP.read_text())
    except Exception:
        return []
    rows = []
    for key in ["google_analytics", "web_analytics", "search_console"]:
        val = data.get(key) or []
        if isinstance(val, dict):
            val = [val]
        for row in val:
            if isinstance(row, dict):
                row = {**row, "source_group": key}
                rows.append(row)
    return rows


def _oauth_env_present() -> dict[str, bool]:
    return {k: bool(os.environ.get(k)) for k in GA4_ENV_KEYS}


def _token_from_cache() -> str | None:
    try:
        data = json.loads(ACCESS_TOKEN_CACHE.read_text())
    except Exception:
        return None
    if data.get("access_token") and float(data.get("expires_at", 0)) > time.time() + 60:
        return str(data["access_token"])
    return None


def _oauth_access_token() -> str:
    _load_env()
    cached = _token_from_cache()
    if cached:
        return cached
    missing = [k for k in GA4_ENV_KEYS if not os.environ.get(k)]
    if missing:
        raise RuntimeError(f"missing OAuth env vars: {', '.join(missing)}")
    data = parse.urlencode({
        "client_id": os.environ["GA4_OAUTH_CLIENT_ID"],
        "client_secret": os.environ["GA4_OAUTH_CLIENT_SECRET"],
        "refresh_token": os.environ["GA4_OAUTH_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = request.Request(TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"OAuth token refresh failed: HTTP {exc.code} {body}") from exc
    token = payload.get("access_token")
    if not token:
        raise RuntimeError("OAuth token refresh failed: no access_token returned")
    ACCESS_TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
    ACCESS_TOKEN_CACHE.write_text(json.dumps({
        "access_token": token,
        "expires_at": time.time() + int(payload.get("expires_in") or 3600),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))
    try:
        ACCESS_TOKEN_CACHE.chmod(0o600)
    except Exception:
        pass
    return str(token)


def _json_post(url: str, token: str, body: dict[str, Any], timeout: int = 30) -> dict[str, Any]:
    req = request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")[:800]
        raise RuntimeError(f"HTTP {exc.code} from {url}: {raw}") from exc


def _date_range(days: int = 7) -> tuple[str, str]:
    # GA4 finalizes with delay. Use yesterday as end date for stable weekly scoring.
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


def _parse_metric(row: dict[str, Any], idx: int) -> int:
    try:
        return int(float(row.get("metricValues", [])[idx].get("value") or 0))
    except Exception:
        return 0


def _ga4_fetch_row(row: dict, days: int = 7) -> dict:
    property_id = str(row.get("property_id") or "").strip()
    if not property_id:
        raise RuntimeError("missing GA4 property_id")
    start, end = _date_range(days)
    token = _oauth_access_token()
    url = GA4_RUN_REPORT.format(property_id=parse.quote(property_id, safe=""))
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "metrics": [
            {"name": "sessions"},
            {"name": "activeUsers"},
            {"name": "screenPageViews"},
            {"name": "eventCount"},
            {"name": "conversions"},
        ],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}],
        "limit": 50,
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
    }
    payload = _json_post(url, token, body)
    totals = {"sessions": 0, "active_users": 0, "pageviews": 0, "event_count": 0, "conversions": 0}
    channel_rows = []
    for rec in payload.get("rows", []) or []:
        channel = ((rec.get("dimensionValues") or [{}])[0].get("value") or "(unknown)")
        vals = {
            "channel": channel,
            "sessions": _parse_metric(rec, 0),
            "active_users": _parse_metric(rec, 1),
            "pageviews": _parse_metric(rec, 2),
            "event_count": _parse_metric(rec, 3),
            "conversions": _parse_metric(rec, 4),
        }
        for k in totals:
            totals[k] += vals[k]
        channel_rows.append(vals)
    captured = date.today().isoformat()
    return {
        "date": captured,
        "week_of": start,
        "platform": "web",
        "provider": "ga4",
        "product_slug": row.get("product_slug"),
        "account": row.get("domain") or row.get("measurement_id") or f"ga4:{property_id}",
        "content_id_or_hook": f"{row.get('product_slug')} GA4 web traffic {start} to {end}",
        "url": row.get("domain") or f"ga4:{property_id}",
        "views_or_impressions": totals["sessions"],
        "active_users": totals["active_users"],
        "pageviews": totals["pageviews"],
        "event_count": totals["event_count"],
        "conversions": totals["conversions"],
        "captured_at": captured,
        "status": "ga4_ok",
        "date_range": {"start": start, "end": end},
        "channel_breakdown": channel_rows[:12],
        "analytics_property_id": property_id,
        "measurement_id": row.get("measurement_id"),
    }


def _gsc_fetch_row(row: dict, days: int = 7) -> dict:
    site_url = str(row.get("site_url") or "").strip()
    if not site_url:
        raise RuntimeError("missing Search Console site_url")
    start, end = _date_range(days)
    token = _oauth_access_token()
    url = GSC_SEARCH_ANALYTICS.format(site_url=parse.quote(site_url, safe=""))
    body = {
        "startDate": start,
        "endDate": end,
        "dimensions": ["query"],
        "rowLimit": 25,
        "startRow": 0,
    }
    payload = _json_post(url, token, body)
    clicks = 0
    impressions = 0
    rows = []
    for rec in payload.get("rows", []) or []:
        item = {
            "query": (rec.get("keys") or [""])[0],
            "clicks": int(rec.get("clicks") or 0),
            "impressions": int(rec.get("impressions") or 0),
            "ctr": float(rec.get("ctr") or 0),
            "position": float(rec.get("position") or 0),
        }
        clicks += item["clicks"]
        impressions += item["impressions"]
        rows.append(item)
    captured = date.today().isoformat()
    return {
        "date": captured,
        "week_of": start,
        "platform": "search_console",
        "provider": "search_console",
        "product_slug": row.get("product_slug"),
        "account": site_url,
        "content_id_or_hook": f"{row.get('product_slug')} Search Console queries {start} to {end}",
        "url": site_url,
        "views_or_impressions": impressions,
        "clicks": clicks,
        "captured_at": captured,
        "status": "search_console_ok",
        "date_range": {"start": start, "end": end},
        "top_queries": rows,
    }


def readiness() -> dict:
    """Return website analytics readiness by product without requiring external writes."""
    _load_env()
    rows = _map_rows()
    oauth_present = _oauth_env_present()
    env_keys = {
        **oauth_present,
        "GA4_SERVICE_ACCOUNT_PATH": bool(os.environ.get("GA4_SERVICE_ACCOUNT_PATH")),
        "GOOGLE_APPLICATION_CREDENTIALS": bool(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")),
        "SEARCH_CONSOLE_SITE_URL": bool(os.environ.get("SEARCH_CONSOLE_SITE_URL")),
        "VERCEL_ANALYTICS_TOKEN": bool(os.environ.get("VERCEL_ANALYTICS_TOKEN")),
        "PLAUSIBLE_API_KEY": bool(os.environ.get("PLAUSIBLE_API_KEY")),
        "POSTHOG_API_KEY": bool(os.environ.get("POSTHOG_API_KEY")),
    }
    ready = []
    blocked = []
    product_details = {}
    configured_products = sorted({str(r.get("product_slug")) for r in rows if r.get("product_slug")})
    default_products = ["vista", "nash-satoshi", "glow-index", "jtsomwaru-com"]
    products = list(dict.fromkeys(default_products + configured_products))
    for product in products:
        prow = [r for r in rows if r.get("product_slug") == product]
        mapped_by = sorted({v for r in prow for v in [_mapping_value(r)] if v})
        live_sources = []
        blockers = []
        for r in prow:
            provider = r.get("provider") or r.get("source_group")
            if r.get("property_id") and provider == "ga4":
                if all(oauth_present.values()):
                    live_sources.append("ga4")
                else:
                    blockers.append("ga4_oauth_env_missing")
            elif r.get("site_url") and provider == "search_console":
                status = str(r.get("status") or "")
                if status in {"verified", "live", "active"} and all(oauth_present.values()):
                    live_sources.append("search_console")
                else:
                    blockers.append(status or "search_console_pending_verification")
            elif r.get("log_path"):
                live_sources.append("local_csv")
            elif r.get("property_id") or r.get("measurement_id") or r.get("site_url"):
                blockers.append(str(r.get("status") or "mapped_pending_activation"))
        if live_sources:
            ready.append(product)
            product_details[product] = {"status": "ready", "mapped_by": mapped_by, "live_sources": sorted(set(live_sources)), "blockers": blockers}
        else:
            blocked.append(product)
            product_details[product] = {
                "status": "blocked_no_live_web_analytics_source" if mapped_by else "blocked_no_web_analytics_source",
                "mapped_by": mapped_by,
                "blockers": blockers,
                "accepted_mappings": ["property_id", "site_url", "log_path", "vercel_project", "plausible_site_id", "posthog_project_id"],
                "example": {"product_slug": product, "provider": "ga4|search_console|vercel|plausible|posthog|local_csv", "property_id": "...", "site_url": "https://...", "log_path": "~/path/to/export.csv"},
            }
    result = {
        "connector": "web",
        "implemented": True,
        "mode": "ga4_oauth_live__search_console_after_verification__local_csv_fallback",
        "configured_rows": rows,
        "env_present": env_keys,
        "ready_products": ready,
        "blocked_products": blocked,
        "product_details": product_details,
        "status": "ready" if not blocked else "partially_ready" if ready else "provider_or_property_mapping_needed",
        "status_reason": "all_active_apps_mapped_and_live" if not blocked else "one_or_more_apps_missing_live_provider_property_or_verification",
        "mapping_template_path": "memory/app-marketing/web-analytics-mapping-template.md",
        "diagnostic_command": "cd ~/.openclaw/workspace && python3 scripts/app_marketing_connectors/web_metrics.py",
        "collector_command": "cd ~/.openclaw/workspace && python3 scripts/app_marketing_collect_metrics.py",
        "next_action": "Nash, Glow, and jtsomwaru.com are live via GA4 and Search Console. Vista App Store reporting remains blocked on APPSTORE_VENDOR_NUMBER."
    }
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def _fetch_local_log(row: dict) -> dict | None:
    path = row.get("log_path")
    if not path:
        return None
    p = Path(path).expanduser()
    if not p.exists():
        return {"platform": "web", "product_slug": row.get("product_slug"), "status": "log_path_missing", "log_path": str(p)}
    # Supports minimal CSV with date,page,views columns.
    if p.suffix.lower() == ".csv":
        total = 0
        with p.open() as f:
            for rec in csv.DictReader(f):
                try:
                    total += int(float(rec.get("views") or rec.get("pageviews") or 0))
                except ValueError:
                    pass
        return {"date": date.today().isoformat(), "week_of": date.today().isoformat(), "platform": "web", "product_slug": row.get("product_slug"), "views_or_impressions": total, "captured_at": date.today().isoformat(), "status": "local_csv"}
    return {"date": date.today().isoformat(), "week_of": date.today().isoformat(), "platform": "web", "product_slug": row.get("product_slug"), "views_or_impressions": None, "captured_at": date.today().isoformat(), "status": "local_log_present_unparsed", "log_path": str(p)}


def fetch(post: dict) -> dict | list[dict] | None:
    """Fetch website metrics for a product from all configured providers.

    GA4 and Search Console are complementary. Return all successful rows so
    durable-discovery scoring can see traffic/events and search impressions.
    """
    product = post.get("product_slug") or post.get("app")
    rows = [r for r in _map_rows() if r.get("product_slug") == product]
    failures = []
    results: list[dict] = []
    for row in rows:
        try:
            if row.get("provider") == "ga4" and row.get("property_id"):
                results.append(_ga4_fetch_row(row))
                continue
            if row.get("provider") == "search_console" and row.get("site_url"):
                if str(row.get("status") or "") in {"verified", "live", "active"}:
                    results.append(_gsc_fetch_row(row))
                else:
                    failures.append(f"search_console_not_verified:{row.get('status')}")
                continue
            local = _fetch_local_log(row)
            if local:
                results.append(local)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{row.get('provider') or row.get('source_group')}:{exc}")
    if results:
        return results
    info = readiness()
    if product:
        captured = date.today().isoformat()
        return {
            "date": captured,
            "week_of": post.get("week_of") or captured,
            "platform": "web",
            "product_slug": product,
            "content_id_or_hook": post.get("hook_or_title") or f"{product} web analytics readiness",
            "url": post.get("url_or_id") or f"web:{product}",
            "views_or_impressions": None,
            "captured_at": captured,
            "status": "blocked_no_live_web_analytics_source",
            "blocked_products": info.get("blocked_products"),
            "notes": "Add/verify GA4 property_id, Search Console site_url, or local log_path in account-map.",
            "failures": failures,
            "product_detail": info.get("product_details", {}).get(product),
            "mapping_template_path": "memory/app-marketing/web-analytics-mapping-template.md",
        }
    return None


if __name__ == "__main__":
    print(json.dumps(readiness(), indent=2, ensure_ascii=False))
