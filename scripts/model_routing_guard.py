#!/usr/bin/env python3
"""Fail fast when default or cron routing can leak into paid non-OpenAI models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HOME = Path.home()
OPENCLAW_CONFIG = HOME / ".openclaw/openclaw.json"
CRON_JOBS = HOME / ".openclaw/cron/jobs.json"

ALLOWED_MAIN = {"openai/gpt-5.5"}
ALLOWED_CRON_PREFIXES = ("openai/",)
PAID_PREFIXES = ("openrouter/", "moonshot/", "anthropic/")


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def model_refs(obj, path=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            next_path = f"{path}.{key}" if path else key
            if key in {"model", "primary"} and isinstance(value, str):
                yield next_path, value
            elif key == "fallbacks" and isinstance(value, list):
                for idx, item in enumerate(value):
                    if isinstance(item, str):
                        yield f"{next_path}[{idx}]", item
            yield from model_refs(value, next_path)
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            yield from model_refs(value, f"{path}[{idx}]")


def check_default_route(config: dict) -> list[str]:
    errors: list[str] = []
    model = config.get("agents", {}).get("defaults", {}).get("model", {})
    primary = model.get("primary")
    fallbacks = model.get("fallbacks", [])

    if primary not in ALLOWED_MAIN:
        errors.append(f"default primary is {primary!r}, expected one of {sorted(ALLOWED_MAIN)}")
    if fallbacks:
        errors.append(f"default fallbacks must be empty, found {fallbacks!r}")
    return errors


def check_crons(cron_data: dict, include_disabled: bool) -> list[str]:
    errors: list[str] = []
    jobs = cron_data.get("jobs", [])
    for job in jobs:
        enabled = bool(job.get("enabled"))
        if not enabled and not include_disabled:
            continue
        for ref_path, ref in model_refs(job):
            if ref.startswith(PAID_PREFIXES):
                errors.append(
                    f"cron {job.get('id')} ({job.get('name')}) has paid model ref "
                    f"{ref!r} at {ref_path}; enabled={enabled}"
                )
            elif enabled and not ref.startswith(ALLOWED_CRON_PREFIXES):
                errors.append(
                    f"enabled cron {job.get('id')} ({job.get('name')}) has non-OpenAI "
                    f"model ref {ref!r} at {ref_path}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-disabled",
        action="store_true",
        help="Also fail on paid model references in disabled cron payloads.",
    )
    args = parser.parse_args()

    errors = []
    errors.extend(check_default_route(load_json(OPENCLAW_CONFIG)))
    errors.extend(check_crons(load_json(CRON_JOBS), args.include_disabled))

    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2))
        return 1

    print(json.dumps({"ok": True, "checked": ["default_route", "cron_routes"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
