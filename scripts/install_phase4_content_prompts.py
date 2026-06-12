#!/usr/bin/env python3
"""Install Eve Optimization Phase 4 content prompts into cron jobs."""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/jtsomwaru/.openclaw/workspace")
PLAYBOOK = ROOT / "docs/audits/eve-playbook-2026-06-11.md"
JOBS = Path.home() / ".openclaw/cron/jobs.json"
MODEL = "openrouter/anthropic/claude-sonnet-4-6"

APPENDICES = {
    "content-generate-linkedin": "Appendix A",
    "content-generate-x": "Appendix B",
}


def extract_prompt(text: str, appendix: str) -> str:
    pattern = rf"## {re.escape(appendix)}:.*?\n\n.*?```(?:\n)(.*?)(?:\n)```"
    match = re.search(pattern, text, flags=re.S)
    if not match:
        raise SystemExit(f"missing prompt block for {appendix}")
    prompt = match.group(1)
    prompt = prompt.replace(
        "python3 /Users/jtsomwaru/.openclaw/workspace/scripts/content_distribution_guard.py --weekly /Users/jtsomwaru/.openclaw/workspace/memory/content/weekly-[MONDAY-DATE].md --require-reference-map linkedin --check-notion-script",
        "/Users/jtsomwaru/.openclaw/workspace/scripts/run_content_guard.sh linkedin [MONDAY-DATE]",
    )
    prompt = prompt.replace(
        "python3 /Users/jtsomwaru/.openclaw/workspace/scripts/content_distribution_guard.py --weekly /Users/jtsomwaru/.openclaw/workspace/memory/content/weekly-[MONDAY-DATE].md --require-reference-map x --check-notion-script",
        "/Users/jtsomwaru/.openclaw/workspace/scripts/run_content_guard.sh x [MONDAY-DATE]",
    )
    return prompt


def main() -> None:
    playbook_text = PLAYBOOK.read_text(encoding="utf-8")
    prompts = {name: extract_prompt(playbook_text, appendix) for name, appendix in APPENDICES.items()}

    data = json.loads(JOBS.read_text(encoding="utf-8"))
    jobs = data.get("jobs")
    if not isinstance(jobs, list):
        raise SystemExit("jobs.json schema missing jobs list")

    found: dict[str, dict] = {}
    for job in jobs:
        name = job.get("name")
        if name in prompts:
            found[name] = job

    missing = sorted(set(prompts) - set(found))
    if missing:
        raise SystemExit(f"missing content cron jobs: {', '.join(missing)}")

    backup = JOBS.with_name(f"jobs.json.backup-phase4-{datetime.now():%Y%m%d%H%M%S}")
    shutil.copy2(JOBS, backup)

    for name, job in found.items():
        payload = job.setdefault("payload", {})
        if not isinstance(payload, dict):
            raise SystemExit(f"{name} payload is not an object")
        payload["message"] = prompts[name]
        payload["model"] = MODEL

    tmp = JOBS.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(JOBS)

    print(json.dumps({
        "ok": True,
        "backup": str(backup),
        "updated": sorted(found),
        "model": MODEL,
        "wrapper_substitution": "/Users/jtsomwaru/.openclaw/workspace/scripts/run_content_guard.sh <platform> [MONDAY-DATE]",
    }, indent=2))


if __name__ == "__main__":
    main()
