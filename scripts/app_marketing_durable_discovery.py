#!/usr/bin/env python3
"""Generate durable discovery action plan for App Marketing OS.

This turns directory/SEO/ASO backlogs into one weekly compounding action.
No external submissions are made.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
BASE = ROOT / "memory" / "app-marketing"
OUT = BASE / "durable-discovery-plan.md"
DIR = BASE / "directory-submissions.md"
SEO = BASE / "seo-backlog.md"
ASO = BASE / "aso-checklist.md"
REGISTRY = BASE / "app-registry.md"


def week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def app_store_blocked() -> bool:
    # App Store Connect is blocked until Apple agreements clear; do not select it as top action.
    today_note = ROOT / "memory" / f"{date.today().isoformat()}.md"
    if today_note.exists() and "REQUIRED_AGREEMENTS_MISSING_OR_EXPIRED" in today_note.read_text(errors="ignore"):
        return True
    return False


def main() -> int:
    today=date.today()
    week=week_start(today)
    registry=REGISTRY.read_text() if REGISTRY.exists() else ""
    seo=SEO.read_text() if SEO.exists() else ""
    directory=DIR.read_text() if DIR.exists() else ""
    aso=ASO.read_text() if ASO.exists() else ""

    # Deterministic priority: active apps first, avoid App Store metrics while blocked.
    actions=[]
    actions.append({
        "app":"Glow Index",
        "type":"Directory + crawler access",
        "title":"Glow directory pack + crawlability check",
        "why":"Glow product/category SEO pages are now shipped. The next compounding move is getting durable listings/backlinks and confirming AI/search crawlers can actually reach sitemap, llms.txt, rankings, and category pages instead of hitting Cloudflare challenges.",
        "done":"Glow directory pack is reviewed with screenshots selected; first low-risk listing target is ready for JT approval; crawler-access issue is documented with exact blocked URLs and required fix path.",
        "blocker":"No external submissions without JT approval. Do not make medical, dermatologist, treatment, acne/eczema/rosacea, before/after, or guaranteed-outcome claims.",
    })
    actions.append({
        "app":"Glow Index",
        "type":"pSEO/GEO expansion hold",
        "title":"Hold ingredient/dupe/concern pages until data model supports them",
        "why":"The safe pSEO batch is shipped. More routes now would risk thin or medically sensitive content unless ingredient/source data is added.",
        "done":"Next pSEO expansion is blocked until structured ingredient/product facts, uniqueness checks, and safe claim templates exist.",
        "blocker":"Do not build ingredient, dupe, concern, acne, eczema, rosacea, or treatment pages from current data.",
    })
    actions.append({
        "app":"Vista",
        "type":"Directory submission pack",
        "title":"Vista movie app directory pack",
        "why":"Vista is live in the App Store and should not rely only on TikTok velocity.",
        "done":"Submission copy exists for Product Hunt, AlternativeTo, Uneed, and iOS/movie app directories.",
        "blocker":"App Store Connect metrics still blocked by Apple agreements; directory pack can proceed anyway.",
    })
    actions.append({
        "app":"Nash Satoshi",
        "type":"Directory submission pack",
        "title":"Nash Satoshi Product Hunt/Uneed/Futurepedia pack",
        "why":"Methodology page is live, so Nash now has a trust asset for directories and AI/tool listings.",
        "done":"Submission copy exists: tagline, 50-word/150-word descriptions, categories, tags, founder note, screenshots needed, pricing/status, safe disclaimers.",
        "blocker":"Do not submit externally without JT approval.",
    })

    selected=actions[0]
    lines=[
        "# App Marketing OS — Durable Discovery Plan",
        "",
        f"Week of: {week.isoformat()}",
        f"Generated: {today.isoformat()}",
        "",
        "## Rule",
        "Every weekly app marketing review should include one compounding discovery action: SEO page, directory/backlink pack, ASO improvement, or competitor intel scan.",
        "",
        "## Selected Next Action",
        f"- **App:** {selected['app']}",
        f"- **Type:** {selected['type']}",
        f"- **Action:** {selected['title']}",
        f"- **Why now:** {selected['why']}",
        f"- **Done looks like:** {selected['done']}",
        f"- **Blocker/guardrail:** {selected['blocker']}",
        "",
        "## Backlog Queue",
    ]
    for a in actions[1:]:
        lines += [
            f"### {a['app']} — {a['title']}",
            f"- Type: {a['type']}",
            f"- Why: {a['why']}",
            f"- Done: {a['done']}",
            f"- Guardrail: {a['blocker']}",
            "",
        ]
    lines += [
        "## Current Source Health",
        f"- App registry loaded: {'Vista' in registry and 'Nash Satoshi' in registry and 'Glow Index' in registry}",
        f"- SEO backlog loaded: {'Vista Backlog' in seo and 'Nash Satoshi Backlog' in seo and 'Glow Index Backlog' in seo}",
        f"- Directory backlog loaded: {'Priority Directories' in directory}",
        f"- ASO checklist loaded: {'Vista — Initial ASO Focus' in aso}",
        f"- App Store Connect blocked: {app_store_blocked()}",
    ]
    OUT.write_text("\n".join(lines).rstrip()+"\n")
    print(f"APP_MARKETING_DURABLE_DISCOVERY_OK out={OUT} selected={selected['app']}::{selected['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
