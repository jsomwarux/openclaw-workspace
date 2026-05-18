#!/usr/bin/env python3
"""Fetch TrustMRR revenue-pattern signals for passive-income pipeline.

TrustMRR is treated as directional, external, untrusted data: useful for
business-model pattern recognition, not audited financial truth.

Outputs:
  memory/passive-income/weekly-trustmrr.json
  memory/passive-income/weekly-trustmrr.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from lxml import html

WORKSPACE = Path(__file__).resolve().parent.parent
DEFAULT_JSON = WORKSPACE / "memory" / "passive-income" / "weekly-trustmrr.json"
DEFAULT_MD = WORKSPACE / "memory" / "passive-income" / "weekly-trustmrr.md"
SOURCE_URL = "https://trustmrr.com/"
USER_AGENT = "Mozilla/5.0 (compatible; OpenClawPassiveIncomeSignals/1.0)"

CATEGORY_RULES: list[tuple[str, list[str]]] = [
    ("AI content / SEO / AEO", ["seo", "aeo", "llm", "ai overview", "search engine", "content", "blog", "thumbnail", "video", "ugc", "slop"]),
    ("Creator monetization / social tools", ["creator", "social", "scheduler", "post", "reddit", "youtube", "tiktok", "instagram", "newsletter", "community"]),
    ("Lead generation / sales automation", ["lead", "linkedin", "outreach", "dm", "closer", "sales", "inbox", "crm", "book", "appointment"]),
    ("Health / wellness / medical", ["health", "medical", "telehealth", "ehr", "hormone", "weight", "fitness", "calorie", "wellness"]),
    ("Education / career / interview", ["resume", "interview", "coding", "learn", "education", "training", "course", "student", "job seeker"]),
    ("Analytics / data / attribution", ["analytics", "attribution", "data", "track", "dashboard", "notion", "warehouse"]),
    ("API / validation / infrastructure", ["api", "validate", "validation", "phone", "email", "ip", "infrastructure"]),
    ("CPG / commerce enablement", ["cpg", "brand", "e-commerce", "fulfillment", "commerce", "shop", "products"]),
    ("Local business / agency software", ["agency", "white-label", "local", "receptionist", "business owners", "software for businesses"]),
]


def clean_text(value: str) -> str:
    value = unescape(value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def money_to_int(value: str | None) -> int | None:
    if not value:
        return None
    digits = re.sub(r"[^0-9]", "", value)
    return int(digits) if digits else None


def infer_categories(name: str, description: str) -> list[str]:
    text = f"{name} {description}".lower()
    categories = []
    for category, needles in CATEGORY_RULES:
        if any(n in text for n in needles):
            categories.append(category)
    return categories or ["Other / unclear"]


def parse_records(markup: str, limit: int) -> list[dict[str, Any]]:
    doc = html.fromstring(markup)
    rows = []
    for a in doc.xpath('//a[contains(@href, "/startup/")]'):
        href = a.get("href") or ""
        if not href.startswith("/startup/"):
            continue
        row = a.xpath('ancestor::tr[1]')
        if not row:
            continue
        row = row[0]
        text = clean_text(" ".join(row.xpath('.//text()')))
        if not text or "$" not in text:
            continue

        # Rank is usually first integer in row text.
        rank_match = re.match(r"^(\d+)", text)
        rank = int(rank_match.group(1)) if rank_match else None

        # Name is image alt or first prominent div text.
        alt_values = [clean_text(x) for x in row.xpath('.//img/@alt') if clean_text(x)]
        name = alt_values[0] if alt_values else ""
        if not name:
            div_texts = [clean_text(x) for x in row.xpath('.//div/text()') if clean_text(x)]
            name = div_texts[0] if div_texts else "Unnamed"

        all_texts = [clean_text(x) for x in row.xpath('.//text()') if clean_text(x)]
        mrr_text = next((t for t in all_texts if re.fullmatch(r"\$[0-9,]+", t)), None)
        reported_mrr = money_to_int(mrr_text)

        growth_percent = None
        for t in reversed(all_texts):
            if re.fullmatch(r"\d+%", t):
                growth_percent = int(t[:-1])
                break

        description_candidates = []
        for t in all_texts:
            if t in {name, mrr_text, str(rank), "FOR SALE"}:
                continue
            if re.fullmatch(r"\d+%", t):
                continue
            if len(t) > 12:
                description_candidates.append(t)
        description = " ".join(description_candidates[:3])[:500]

        stealth_or_ambiguous = bool(re.search(r"stealth|unnamed|hidden|confidential|private venture|top secret|project", name, re.I))
        categories = infer_categories(name, description)
        rows.append({
            "rank": rank,
            "name": name,
            "url": urljoin(SOURCE_URL, href),
            "description": description,
            "reported_mrr": reported_mrr,
            "growth_percent": growth_percent,
            "categories_inferred": categories,
            "stealth_or_ambiguous": stealth_or_ambiguous,
        })
        if len(rows) >= limit:
            break

    # De-dupe by URL while preserving order.
    seen = set()
    records = []
    for row in rows:
        if row["url"] in seen:
            continue
        seen.add(row["url"])
        records.append(row)
    return records


def category_patterns(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        for cat in record.get("categories_inferred", []):
            grouped[cat].append(record)

    patterns = []
    for category, rows in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        mrrs = [r["reported_mrr"] for r in rows if isinstance(r.get("reported_mrr"), int)]
        examples = [r["name"] for r in rows[:6]]
        if mrrs:
            mrr_range = f"${min(mrrs):,}-${max(mrrs):,} reported MRR"
        else:
            mrr_range = "MRR unavailable"
        takeaway = "Revenue-backed category; use as adjacent pattern only, not copycat instruction."
        if len(rows) >= 4:
            takeaway = "Multiple visible comps; validates demand but raises saturation/copycat risk."
        if category == "Other / unclear":
            takeaway = "Ambiguous listings; weak evidence unless supported by separate demand signals."
        patterns.append({
            "category": category,
            "examples": examples,
            "count": len(rows),
            "mrr_range": mrr_range,
            "takeaway": takeaway,
        })
    return patterns


def write_markdown(path: Path, data: dict[str, Any]) -> None:
    lines = [
        "# Weekly TrustMRR Revenue Pattern Scan",
        "",
        f"Fetched: {data['fetched_at']}",
        f"Source: {data['source_url']}",
        "",
        "## Warnings",
    ]
    lines.extend(f"- {w}" for w in data["warnings"])
    lines += ["", "## Category Patterns"]
    for p in data["category_patterns"]:
        lines.append(f"- **{p['category']}** ({p['count']} comps, {p['mrr_range']}): {', '.join(p['examples'])}. {p['takeaway']}")
    lines += ["", "## Top Records"]
    for r in data["records"][:50]:
        mrr = f"${r['reported_mrr']:,}" if r.get("reported_mrr") else "n/a"
        growth = f", growth {r['growth_percent']}%" if r.get("growth_percent") is not None else ""
        stealth = " — stealth/ambiguous" if r.get("stealth_or_ambiguous") else ""
        cats = "; ".join(r.get("categories_inferred", []))
        lines.append(f"{r.get('rank')}. **{r['name']}** — reported MRR {mrr}{growth}; categories: {cats}{stealth}")
        if r.get("description"):
            lines.append(f"   - {r['description']}")
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=SOURCE_URL)
    ap.add_argument("--out", default=str(DEFAULT_JSON))
    ap.add_argument("--markdown-out", default=str(DEFAULT_MD))
    ap.add_argument("--limit", type=int, default=75)
    args = ap.parse_args()

    out = Path(args.out)
    md_out = Path(args.markdown_out)
    out.parent.mkdir(parents=True, exist_ok=True)

    resp = requests.get(args.url, headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    records = parse_records(resp.text, args.limit)
    if not records:
        raise SystemExit("No TrustMRR records parsed")

    now = datetime.now(timezone.utc).isoformat()
    data = {
        "fetched_at": now,
        "source_url": args.url,
        "freshness_days": 0,
        "records": records,
        "category_patterns": category_patterns(records),
        "warnings": [
            "TrustMRR data is external and directional; treat listed MRR as reported/listed, not audited financial truth.",
            "Stealth, unnamed, hidden, or confidential listings cannot support exact conclusions or BUILD verdicts alone.",
            "Use revenue patterns to validate adjacent opportunities; do not clone listed startups directly.",
        ],
    }
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    write_markdown(md_out, data)
    print(f"TRUSTMRR_FETCH_OK records={len(records)} json={out} md={md_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
