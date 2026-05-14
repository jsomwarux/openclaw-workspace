#!/usr/bin/env python3
"""Check Consulting Client OS hardening completeness for active/proof clients.

This is intentionally conservative: it only checks internal controllables
(file existence/non-empty and core proof/privacy/handoff keywords). It does
not infer client acceptance, payment, or proof permission.
"""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "dashboard.md",
    "weekly-updates.md",
    "decision-log.md",
    "failure-log.md",
    "workflow-map.md",
    "automation-candidates.md",
    "metrics.md",
    "quarterly-review.md",
    "reusable-ip-log.md",
    "handoff.md",
]
REQUIRED_DIR_READMES = [
    "raw-inputs/README.md",
    "cleaned-inputs/README.md",
    "outputs/README.md",
]
KEYWORDS = ["acceptance", "proof", "privacy", "redact", "handoff", "reusable"]


def non_empty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 40


def check_client_os(path: Path) -> list[str]:
    issues: list[str] = []
    for rel in REQUIRED_FILES + REQUIRED_DIR_READMES:
        p = path / rel
        if not non_empty(p):
            issues.append(f"missing_or_empty:{rel}")
    acceptance = list(path.glob("acceptance-checklist*.md"))
    if not acceptance:
        issues.append("missing_acceptance_checklist")
    corpus = "\n".join(p.read_text(errors="ignore").lower() for p in path.rglob("*.md") if p.is_file())
    for kw in KEYWORDS:
        if kw not in corpus:
            issues.append(f"missing_keyword:{kw}")
    return issues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path.home() / ".openclaw/workspace"))
    ap.add_argument("--clients-root", default=str(Path.home() / "projects/jt-consulting-pipeline/clients"))
    args = ap.parse_args()
    root = Path(args.root)
    targets = {
        "aya": root / "memory/clients/aya",
        "altmark-group": root / "memory/clients/altmark-group/client-os",
    }
    failed = False
    for name, path in targets.items():
        issues = check_client_os(path)
        if issues:
            failed = True
            print(f"FAIL {name}: {', '.join(issues)}")
        else:
            print(f"OK {name}: Client OS internal controls present")
    print("NOTE: external acceptance/payment/proof permission must be verified from client evidence; this script does not certify it.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
