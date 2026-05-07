#!/usr/bin/env python3
"""Update App Marketing OS weekly scoreboard from metrics-inbox.jsonl.

This intentionally supports a tiny manual/laptop handoff first. JT or Eve can append
one JSON object per post/result to memory/app-marketing/metrics-inbox.jsonl, then run
this script to summarize into weekly-scoreboard.md.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
BASE = ROOT / "memory" / "app-marketing"
INBOX = BASE / "metrics-inbox.jsonl"
SCOREBOARD = BASE / "weekly-scoreboard.md"

NUMERIC_FIELDS = [
    "views_or_impressions",
    "likes",
    "comments",
    "saves",
    "reposts",
    "clicks",
    "downloads",
    "signups",
]


def load_entries() -> tuple[list[dict], list[str]]:
    entries: list[dict] = []
    errors: list[str] = []
    if not INBOX.exists():
        return entries, [f"missing inbox: {INBOX}"]
    for i, line in enumerate(INBOX.read_text().splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"line {i}: invalid JSON: {exc}")
            continue
        required = ["date", "week_of", "product_slug", "platform", "content_id_or_hook", "views_or_impressions"]
        missing = [k for k in required if k not in obj]
        if missing:
            errors.append(f"line {i}: missing {missing}")
            continue
        entries.append(obj)
    return entries, errors


def summarize(entries: list[dict]) -> str:
    if not entries:
        return "No metrics entries yet. Add rows to `memory/app-marketing/metrics-inbox.jsonl`."

    by_week: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_week[str(e["week_of"])].append(e)

    chunks: list[str] = []
    for week in sorted(by_week.keys(), reverse=True):
        rows = by_week[week]
        chunks.append(f"## Metrics Summary — Week of {week}")
        chunks.append("")
        by_product_platform: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for e in rows:
            by_product_platform[(str(e["product_slug"]), str(e["platform"]))].append(e)

        best = None
        for (product, platform), items in sorted(by_product_platform.items()):
            totals = {field: sum(int(x.get(field) or 0) for x in items) for field in NUMERIC_FIELDS}
            chunks.append(f"### {product} / {platform}")
            chunks.append(f"- Posts/results logged: {len(items)}")
            chunks.append(f"- Views/impressions: {totals['views_or_impressions']}")
            if totals["likes"] or totals["comments"] or totals["saves"] or totals["reposts"]:
                chunks.append(f"- Engagement: likes {totals['likes']}, comments {totals['comments']}, saves {totals['saves']}, reposts {totals['reposts']}")
            if totals["clicks"] or totals["downloads"] or totals["signups"]:
                chunks.append(f"- Conversion: clicks {totals['clicks']}, downloads {totals['downloads']}, signups {totals['signups']}")
            top_item = max(items, key=lambda x: int(x.get("views_or_impressions") or 0))
            chunks.append(f"- Best item: {top_item.get('content_id_or_hook')} ({top_item.get('views_or_impressions')} views/impressions)")
            chunks.append("")
            if best is None or int(top_item.get("views_or_impressions") or 0) > int(best.get("views_or_impressions") or 0):
                best = top_item

        if best:
            chunks.append(f"**Best overall:** {best.get('product_slug')} / {best.get('platform')} — {best.get('content_id_or_hook')} ({best.get('views_or_impressions')} views/impressions)")
            chunks.append("")
        chunks.append("**Next action:** double down only after this pattern repeats or beats baseline by a clear margin.")
        chunks.append("")
    return "\n".join(chunks).rstrip()


def update_scoreboard(summary: str, errors: list[str]) -> None:
    existing = SCOREBOARD.read_text() if SCOREBOARD.exists() else "# App Marketing OS — Weekly Scoreboard\n"
    marker = "\n<!-- METRICS_SUMMARY_START -->\n"
    end = "\n<!-- METRICS_SUMMARY_END -->\n"
    block = marker + summary + "\n"
    if errors:
        block += "\n## Metrics Inbox Errors\n" + "\n".join(f"- {e}" for e in errors) + "\n"
    block += f"\n_Last updated: {date.today().isoformat()}_\n" + end
    if marker in existing and end in existing:
        before = existing.split(marker)[0]
        after = existing.split(end, 1)[1]
        SCOREBOARD.write_text(before + block + after)
    else:
        SCOREBOARD.write_text(existing.rstrip() + "\n" + block + "\n")


def main() -> int:
    entries, errors = load_entries()
    summary = summarize(entries)
    update_scoreboard(summary, errors)
    print(f"APP_MARKETING_METRICS_OK entries={len(entries)} errors={len(errors)} scoreboard={SCOREBOARD}")
    if errors:
        for e in errors:
            print(f"ERROR {e}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
