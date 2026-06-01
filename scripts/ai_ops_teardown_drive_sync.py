#!/usr/bin/env python3
"""Upload AI Ops Teardown bundles to organized Google Drive folders."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
CALENDAR = WORKSPACE / "memory/consulting/ai-ops-teardowns/delivery-calendar.md"
DRIVE_DRAFTS = WORKSPACE / "scripts/drive_drafts.py"
SYNC_LOG = WORKSPACE / "memory/consulting/ai-ops-teardowns/drive-sync-log.jsonl"


@dataclass(frozen=True)
class Bundle:
    date: str
    title: str
    slug: str


@dataclass(frozen=True)
class UploadItem:
    title: str
    drive_path: str
    file_path: Path


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def current_bundle_from_calendar(calendar_text: str) -> Bundle:
    marker = "## Current Bundle"
    start = calendar_text.find(marker)
    if start == -1:
        raise ValueError("delivery calendar has no '## Current Bundle' section")

    rest = calendar_text[start + len(marker) :]
    match = re.search(r"^###\s+(\d{4}-\d{2}-\d{2})\s+[—-]\s+(.+?)\s*$", rest, re.MULTILINE)
    if not match:
        raise ValueError("delivery calendar current bundle heading was not found")

    date, title = match.groups()
    return Bundle(date=date, title=title.strip(), slug=slugify(title))


def build_upload_plan(workspace: Path, date: str, slug: str, title: str) -> list[UploadItem]:
    teardown = workspace / f"memory/consulting/ai-ops-teardowns/{date}-{slug}.md"
    draft = workspace / f"memory/content/bank/{date}/ai-ops-teardown-{slug}.md"
    return [
        UploadItem(
            title=f"AI Ops Teardown — {title} — {date}",
            drive_path=f"Consulting/AI Ops Teardowns/{date}/Teardowns",
            file_path=teardown,
        ),
        UploadItem(
            title=f"AI Ops Teardown Draft — {title} — {date}",
            drive_path=f"Content/AI Ops Teardowns/{date}/Drafts",
            file_path=draft,
        ),
    ]


def load_bundle(args: argparse.Namespace) -> Bundle:
    if args.date and args.slug and args.title:
        return Bundle(date=args.date, slug=args.slug, title=args.title)
    if any([args.date, args.slug, args.title]):
        raise SystemExit("--date, --slug, and --title must be provided together")
    return current_bundle_from_calendar(CALENDAR.read_text())


def upload_item(item: UploadItem, dry_run: bool) -> dict[str, str]:
    if not item.file_path.exists():
        raise FileNotFoundError(f"missing expected AI Ops Teardown file: {item.file_path}")

    command = [
        sys.executable,
        str(DRIVE_DRAFTS),
        "--title",
        item.title,
        "--path",
        item.drive_path,
        "--file",
        str(item.file_path),
    ]
    if dry_run:
        return {
            "title": item.title,
            "drive_path": item.drive_path,
            "file": str(item.file_path),
            "url": "DRY_RUN",
        }

    result = subprocess.run(command, cwd=WORKSPACE, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"drive upload failed for {item.file_path}:\n{result.stderr}\n{result.stdout}")

    url_match = re.search(r"https://docs\.google\.com/document/d/[^\s]+", result.stdout)
    return {
        "title": item.title,
        "drive_path": item.drive_path,
        "file": str(item.file_path),
        "url": url_match.group(0) if url_match else "",
    }


def append_log(bundle: Bundle, uploads: list[dict[str, str]], dry_run: bool) -> None:
    if dry_run:
        return
    record = {
        "synced_at": datetime.now().isoformat(timespec="seconds"),
        "date": bundle.date,
        "slug": bundle.slug,
        "title": bundle.title,
        "uploads": uploads,
    }
    with SYNC_LOG.open("a") as f:
        f.write(json.dumps(record) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload the current AI Ops Teardown bundle to Drive.")
    parser.add_argument("--date", help="Bundle date, YYYY-MM-DD")
    parser.add_argument("--slug", help="Bundle slug")
    parser.add_argument("--title", help="Human-readable bundle title")
    parser.add_argument("--dry-run", action="store_true", help="Print upload plan without touching Drive")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()

    bundle = load_bundle(args)
    plan = build_upload_plan(WORKSPACE, bundle.date, bundle.slug, bundle.title)
    uploads = [upload_item(item, args.dry_run) for item in plan]
    append_log(bundle, uploads, args.dry_run)

    summary = {"bundle": bundle.__dict__, "uploads": uploads, "dry_run": args.dry_run}
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print("AI_OPS_TEARDOWN_DRIVE_SYNC_OK")
        for upload in uploads:
            print(f"- {upload['title']}")
            print(f"  {upload['drive_path']}")
            print(f"  {upload['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
