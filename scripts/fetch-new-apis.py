#!/usr/bin/env python3
"""
API Discovery Pipeline — fetches newly launched/added free APIs from 3 sources
and writes a merged intelligence report to memory/passive-income/weekly-apis.md.

Sources:
  1. APIs.guru — new APIs added in last 14 days
  2. public-apis GitHub — recent commits adding free APIs
  3. Product Hunt — newest API tool launches
"""

import json
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

WORKSPACE = Path(__file__).resolve().parent.parent
LIBRARY_FILE = WORKSPACE / "agents" / "passive-income-scout" / "api-library.json"
OUTPUT_DIR = WORKSPACE / "memory" / "passive-income"
OUTPUT_FILE = OUTPUT_DIR / "weekly-apis.md"

HEADERS = {"User-Agent": "PassiveIncomeScout/1.0 (API discovery pipeline)"}
GITHUB_HEADERS = {
    "User-Agent": "PassiveIncomeScout/1.0",
    "Accept": "application/vnd.github.v3+json",
}


def load_library():
    """Load the curated API library."""
    if not LIBRARY_FILE.exists():
        print(f"WARNING: Library file not found at {LIBRARY_FILE}")
        return []
    with open(LIBRARY_FILE) as f:
        return json.load(f)


def fetch_apis_guru():
    """Source 1: APIs.guru — filter entries added in last 14 days."""
    print("Fetching: APIs.guru catalog...")
    results = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=14)

    try:
        resp = requests.get(
            "https://api.apis.guru/v2/list.json",
            headers=HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        catalog = resp.json()

        for api_name, api_data in catalog.items():
            preferred = api_data.get("preferred", "")
            versions = api_data.get("versions", {})
            version_data = versions.get(preferred, {})
            if not version_data:
                version_data = next(iter(versions.values()), {})

            added_str = version_data.get("added")
            if not added_str:
                continue

            try:
                added_date = datetime.fromisoformat(
                    added_str.replace("Z", "+00:00")
                )
                if added_date.tzinfo is None:
                    added_date = added_date.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                continue

            if added_date >= cutoff:
                info = version_data.get("info", {})
                results.append({
                    "name": info.get("title", api_name),
                    "description": (info.get("description", "") or "")[:200],
                    "url": version_data.get("swaggerUrl", ""),
                    "added": added_date.strftime("%Y-%m-%d"),
                    "source": "apis_guru",
                })

        print(f"  -> {len(results)} new APIs found (last 14 days)")
    except Exception as e:
        print(f"  ERROR fetching APIs.guru: {e}")

    return results


def fetch_public_apis_github():
    """Source 2: public-apis GitHub — recent commits adding free APIs."""
    print("Fetching: public-apis GitHub repo...")
    results = []
    since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

    try:
        commits_url = (
            "https://api.github.com/repos/public-apis/public-apis/commits"
        )
        resp = requests.get(
            commits_url,
            params={"since": since, "path": "README.md", "per_page": 5},
            headers=GITHUB_HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        commits = resp.json()

        if not commits:
            print("  -> No recent commits to README.md")
            return results

        for commit in commits[:3]:
            sha = commit.get("sha", "")
            commit_date = (
                commit.get("commit", {})
                .get("committer", {})
                .get("date", "unknown")
            )

            diff_url = (
                f"https://api.github.com/repos/public-apis/public-apis"
                f"/commits/{sha}"
            )
            diff_resp = requests.get(
                diff_url,
                headers={
                    **GITHUB_HEADERS,
                    "Accept": "application/vnd.github.v3.diff",
                },
                timeout=30,
            )

            if diff_resp.status_code != 200:
                continue

            for line in diff_resp.text.split("\n"):
                if not line.startswith("+"):
                    continue
                if line.startswith("+++"):
                    continue

                content = line[1:].strip()

                # Table row format: | Name | Description | Auth | HTTPS | CORS |
                if "|" not in content:
                    continue

                parts = [p.strip() for p in content.split("|")]
                parts = [p for p in parts if p]

                if len(parts) < 3:
                    continue

                name_field = parts[0]
                desc_field = parts[1] if len(parts) > 1 else ""
                auth_field = parts[2] if len(parts) > 2 else ""

                # Skip header rows
                if name_field.startswith("---") or name_field == "API":
                    continue

                # Filter for free APIs
                auth_lower = auth_field.lower()
                if auth_lower not in ("no", "apikey", "", "yes"):
                    continue

                # Extract link from markdown [Name](url)
                api_name = name_field
                if "[" in name_field and "](" in name_field:
                    api_name = name_field.split("[")[1].split("]")[0]

                results.append({
                    "name": api_name,
                    "description": desc_field[:200],
                    "url": "",
                    "added": commit_date[:10] if commit_date != "unknown" else "unknown",
                    "source": "public_apis_github",
                })

        print(f"  -> {len(results)} new free APIs found in recent commits")
    except Exception as e:
        print(f"  ERROR fetching public-apis GitHub: {e}")

    return results


def fetch_product_hunt():
    """Source 3: Product Hunt — newest API tool launches."""
    print("Fetching: Product Hunt API tools topic...")
    results = []

    try:
        resp = requests.get(
            "https://www.producthunt.com/topics/api-tools",
            params={"order": "newest"},
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
            },
            timeout=30,
        )

        if resp.status_code != 200:
            print(f"  Product Hunt returned status {resp.status_code}")
            return results

        html = resp.text

        # Try to extract JSON-LD structured data
        import re

        ld_json_matches = re.findall(
            r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
            html,
            re.DOTALL,
        )
        for match in ld_json_matches:
            try:
                data = json.loads(match)
                items = []
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    items = data.get("itemListElement", [data])

                for item in items:
                    name = item.get("name", "")
                    desc = item.get("description", "")
                    url = item.get("url", "")
                    if name and ("api" in name.lower() or "api" in desc.lower()):
                        results.append({
                            "name": name,
                            "description": desc[:200],
                            "url": url,
                            "added": datetime.now().strftime("%Y-%m-%d"),
                            "source": "product_hunt",
                        })
            except json.JSONDecodeError:
                continue

        # Fallback: extract from og: tags
        if not results:
            og_titles = re.findall(
                r'<meta[^>]*property="og:title"[^>]*content="([^"]*)"',
                html,
            )
            og_descs = re.findall(
                r'<meta[^>]*property="og:description"[^>]*content="([^"]*)"',
                html,
            )
            for i, title in enumerate(og_titles[:5]):
                desc = og_descs[i] if i < len(og_descs) else ""
                if title and title != "Product Hunt":
                    results.append({
                        "name": title,
                        "description": desc[:200],
                        "url": "https://www.producthunt.com/topics/api-tools",
                        "added": datetime.now().strftime("%Y-%m-%d"),
                        "source": "product_hunt",
                    })

        print(f"  -> {len(results)} API-related launches found")
    except Exception as e:
        print(f"  ERROR fetching Product Hunt: {e}")

    return results


def write_report(library, apis_guru, public_apis, product_hunt):
    """Write the merged intelligence report."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Group library by category
    categories = {}
    for api in library:
        cat = api.get("category", "Uncategorized")
        categories.setdefault(cat, []).append(api)

    lines = [
        f"# API Intelligence Report — {date_str}",
        f"Generated: {timestamp}",
        "",
        "## Curated Library Summary",
        f"Total APIs in library: {len(library)}",
        f"Categories: {', '.join(sorted(categories.keys()))}",
        "",
        "## Newly Discovered APIs (last 14 days)",
        "",
    ]

    # APIs.guru section
    lines.append("### From APIs.guru")
    if apis_guru:
        for api in apis_guru:
            url_part = f" | {api['url']}" if api["url"] else ""
            lines.append(
                f"- **{api['name']}**: {api['description']} "
                f"— Added {api['added']}{url_part}"
            )
    else:
        lines.append("- No new APIs found in last 14 days")
    lines.append("")

    # public-apis GitHub section
    lines.append("### From public-apis GitHub")
    if public_apis:
        for api in public_apis:
            lines.append(
                f"- **{api['name']}**: {api['description']} "
                f"— Added via commit {api['added']}"
            )
    else:
        lines.append("- No new free APIs added in recent commits")
    lines.append("")

    # Product Hunt section
    lines.append("### From Product Hunt")
    if product_hunt:
        for api in product_hunt:
            url_part = f" | {api['url']}" if api["url"] else ""
            lines.append(
                f"- **{api['name']}**: {api['description']} "
                f"— Launched {api['added']}{url_part}"
            )
    else:
        lines.append("- No new API tool launches found")
    lines.append("")

    # Full curated library
    lines.append("## Full Curated Library")
    lines.append("")
    for cat in sorted(categories.keys()):
        lines.append(f"### {cat}")
        for api in categories[cat]:
            potential = api.get("niche_potential", "medium")
            lines.append(
                f"- **{api['name']}** [{potential}]: "
                f"{api.get('rankable_data', 'N/A')}"
            )
        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines))
    return len(apis_guru) + len(public_apis) + len(product_hunt)


def main():
    print("=== API Discovery Pipeline ===\n")

    # Load curated library
    library = load_library()
    print(f"Curated library: {len(library)} APIs loaded\n")

    # Fetch from all 3 sources
    apis_guru = fetch_apis_guru()
    public_apis = fetch_public_apis_github()
    product_hunt = fetch_product_hunt()

    # Write report
    total_new = write_report(library, apis_guru, public_apis, product_hunt)

    print(f"\n=== Done ===")
    print(f"New APIs discovered: {total_new}")
    print(f"Report written to: {OUTPUT_FILE.relative_to(WORKSPACE)}")


if __name__ == "__main__":
    main()
