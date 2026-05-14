from __future__ import annotations

import csv
import json
import os
from datetime import date
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
ACCOUNT_MAP = ROOT / "memory" / "app-marketing" / "account-map.json"
STATUS_PATH = ROOT / "memory" / "app-marketing" / "web-analytics-status.json"
ENV_PATH = Path.home() / ".config" / "env" / "global.env"


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


def readiness() -> dict:
    """Return website analytics readiness by product without requiring external writes."""
    _load_env()
    rows = _map_rows()
    env_keys = {
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
    for product in ["vista", "nash-satoshi", "glow-index"]:
        prow = [r for r in rows if r.get("product_slug") == product]
        mapped_by = sorted({v for r in prow for v in [_mapping_value(r)] if v})
        if mapped_by:
            ready.append(product)
            product_details[product] = {"status": "mapped", "mapped_by": mapped_by}
        else:
            blocked.append(product)
            product_details[product] = {
                "status": "blocked_no_web_analytics_source",
                "accepted_mappings": ["property_id", "site_url", "log_path", "vercel_project", "plausible_site_id", "posthog_project_id"],
                "example": {"product_slug": product, "provider": "ga4|search_console|vercel|plausible|posthog|local_csv", "property_id": "...", "site_url": "https://...", "log_path": "~/path/to/export.csv"},
            }
    result = {
        "connector": "web",
        "implemented": True,
        "mode": "readiness_and_local_log_only_until_provider_configured",
        "configured_rows": rows,
        "env_present": env_keys,
        "ready_products": ready,
        "blocked_products": blocked,
        "product_details": product_details,
        "status": "ready" if not blocked else "provider_or_property_mapping_needed",
        "status_reason": "all_active_apps_mapped" if not blocked else "one_or_more_apps_missing_provider_property_or_log_path",
        "mapping_template_path": "memory/app-marketing/web-analytics-mapping-template.md",
        "diagnostic_command": "cd ~/.openclaw/workspace && python3 scripts/app_marketing_connectors/web_metrics.py",
        "collector_command": "cd ~/.openclaw/workspace && python3 scripts/app_marketing_collect_metrics.py",
        "next_action": "Add GA4/Search Console/Vercel/Plausible/PostHog property mapping or a local log_path per app in memory/app-marketing/account-map.json.",
    }
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(result, indent=2))
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
        return {"platform": "web", "product_slug": row.get("product_slug"), "views_or_impressions": total, "captured_at": date.today().isoformat(), "status": "local_csv"}
    return {"platform": "web", "product_slug": row.get("product_slug"), "views_or_impressions": None, "captured_at": date.today().isoformat(), "status": "local_log_present_unparsed", "log_path": str(p)}


def fetch(post: dict) -> dict | None:
    """Fetch website metrics when a local configured source exists.

    External provider APIs are intentionally not guessed here. The connector emits
    readiness blockers until account-map has a concrete provider/property/log path.
    """
    product = post.get("product_slug") or post.get("app")
    rows = [r for r in _map_rows() if r.get("product_slug") == product]
    for row in rows:
        local = _fetch_local_log(row)
        if local:
            return local
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
            "status": "blocked_no_web_analytics_source",
            "blocked_products": info.get("blocked_products"),
            "notes": "Add GA4/Search Console/Vercel/Plausible/PostHog property mapping or local log_path in account-map.",
            "product_detail": info.get("product_details", {}).get(product),
            "mapping_template_path": "memory/app-marketing/web-analytics-mapping-template.md",
        }
    return None


if __name__ == "__main__":
    print(json.dumps(readiness(), indent=2))
