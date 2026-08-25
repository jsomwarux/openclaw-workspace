#!/usr/bin/env python3
"""Fetch and report whether a backup repository can be pushed safely."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


class PreflightError(RuntimeError):
    pass


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise PreflightError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def inspect_repository(repo: Path, branch: str) -> dict[str, object]:
    repo = repo.resolve()
    if not (repo / ".git").exists():
        raise PreflightError(f"not a git working tree: {repo}")
    run_git(repo, "fetch", "origin", branch)
    counts = run_git(repo, "rev-list", "--left-right", "--count", f"HEAD...origin/{branch}")
    try:
        ahead, behind = (int(value) for value in counts.split())
    except (ValueError, TypeError) as exc:
        raise PreflightError(f"unexpected rev-list output: {counts!r}") from exc
    if behind and ahead:
        status = "DIVERGED"
    elif behind:
        status = "REMOTE_AHEAD"
    elif ahead:
        status = "LOCAL_AHEAD"
    else:
        status = "SYNCED"
    return {
        "repo": str(repo),
        "branch": branch,
        "ahead": ahead,
        "behind": behind,
        "status": status,
        "push_safe": behind == 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = inspect_repository(Path(args.repo), args.branch)
    except PreflightError as exc:
        result = {"status": "ERROR", "push_safe": False, "error": str(exc)}
        print(json.dumps(result, sort_keys=True) if args.json else f"ERROR {exc}")
        return 2
    print(json.dumps(result, sort_keys=True) if args.json else result["status"])
    return 0 if result["push_safe"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
