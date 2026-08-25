#!/usr/bin/env python3
"""Verify that the job-market cron uses resilient discovery controls."""

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_job_market_cron_prompt.py PROMPT_FILE")
        return 2

    prompt = Path(sys.argv[1]).read_text()
    required = {
        "rolling 30-day window": "rolling 30-day",
        "broad result count": "--count 15",
        "separate ATS searches": "one ATS domain per query",
        "post-discovery filters": "Apply location, compensation, coding, seniority, and evidence gates after discovery",
        "named top-three proof": "For each of the top three responsibilities, record a named Spectrum or paid-consulting proof point",
        "zero-yield failure": "SEARCH_FAILURE",
        "candidate rejection log": "rejection reason",
        "deduplication": "deduplicate",
        "safe environment loading": "set -a; source /Users/jtsomwaru/.config/env/global.env; set +a",
    }
    missing = [name for name, marker in required.items() if marker not in prompt]
    if missing:
        print("FAIL missing=" + ", ".join(missing))
        return 1
    print(f"PASS controls={len(required)} chars={len(prompt)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
