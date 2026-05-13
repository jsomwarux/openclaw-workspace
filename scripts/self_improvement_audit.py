#!/usr/bin/env python3
"""Audit Eve's self-improvement loop.

Checks whether recent mistake entries include the six required fields and whether
regression checks exist. Read-only by default; prints actionable findings.
"""
from __future__ import annotations

import re
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
MISTAKES = ROOT / "docs/agents/mistakes-log-recent.md"
REGRESSION = ROOT / "docs/agents/regression-checks.md"
TRAINING = ROOT / "memory/training/training-log.md"
TARGETS = ROOT / "agents/autoresearch/targets.md"
CHECKLISTS = ROOT / "agents/autoresearch/checklists"
RESULTS = ROOT / "agents/autoresearch/results.tsv"

REQUIRED_TERMS = {
    "failure": ["failure", "mistake"],
    "root_cause": ["root cause", "root:"],
    "guardrail": ["guardrail", "rule", "prevention"],
    "regression_check": ["regression check", "check:"],
    "owner_surface": ["owner surface", "owner:"],
    "verification": ["verification", "verified", "date:"],
}

REPEAT_TERMS = ["mistake", "missed", "stale", "timeout", "hallucinated", "duplicate", "failed", "incorrect"]


def read(path: Path) -> str:
    return path.read_text(errors="ignore") if path.exists() else ""


def section_blocks(text: str) -> list[str]:
    # Capture headed detailed entries plus table rows. Good enough for drift detection.
    blocks = []
    for chunk in re.split(r"\n(?=## )", text):
        if any(t in chunk.lower() for t in REPEAT_TERMS):
            blocks.append(chunk.strip())
    for line in text.splitlines():
        if line.startswith("|") and any(t in line.lower() for t in REPEAT_TERMS):
            blocks.append(line.strip())
    return blocks


def is_recent_block(block: str, days: int = 14) -> bool:
    """Only enforce six-field standard on genuinely recent dated entries."""
    if block.startswith("# ") or block.startswith("| Date |"):
        return False
    m = re.search(r"(20\d{2}-\d{2}-\d{2})", block)
    if not m:
        return False
    try:
        d = date.fromisoformat(m.group(1))
    except ValueError:
        return False
    return d >= date.today() - timedelta(days=days)


def has_any(block: str, terms: list[str]) -> bool:
    b = block.lower()
    return any(t in b for t in terms)


def main() -> int:
    mistakes = read(MISTAKES)
    regression = read(REGRESSION)
    training = read(TRAINING)
    targets = read(TARGETS)

    findings: list[str] = []
    infos: list[str] = []

    if not regression:
        findings.append("FAIL: docs/agents/regression-checks.md missing")
    elif "## Active Checks" not in regression:
        findings.append("FAIL: regression-checks.md missing Active Checks section")

    blocks = [b for b in section_blocks(mistakes) if is_recent_block(b)]
    incomplete = []
    for block in blocks:
        missing = [name for name, terms in REQUIRED_TERMS.items() if not has_any(block, terms)]
        # Historical table rows may predate the new standard. Flag, don't fail hard.
        if missing:
            title = block.splitlines()[0][:140]
            incomplete.append((title, missing))

    if incomplete:
        findings.append(f"WARN: {len(incomplete)} recent mistake blocks do not show all six fields")
        for title, missing in incomplete[:8]:
            findings.append(f"  - {title} :: missing {', '.join(missing)}")

    pending = []
    target_rows = []
    for line in targets.splitlines():
        if line.startswith("|") and not line.startswith("| Slug") and not line.startswith("|---"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 7 and parts[0] != "—":
                target_rows.append(parts)
                if parts[3] == "pending":
                    pending.append(line)
    if pending:
        infos.append(f"INFO: {len(pending)} autoresearch targets pending; recurring sweep drains one high-value target Mon/Wed/Fri")

    missing_checklists = []
    long_checklists = []
    missing_targets = []
    for slug, path, checklist, status, *_ in target_rows:
        cp = ROOT / "agents/autoresearch" / checklist
        if not cp.exists():
            missing_checklists.append(f"{slug}: {checklist}")
        else:
            q_count = sum(1 for l in cp.read_text(errors="ignore").splitlines() if re.match(r"^\s*\d+\.", l))
            if q_count > 6:
                long_checklists.append(f"{slug}: {q_count} questions")
        if path and not path.startswith("(") and not path.startswith("cron:") and "+" not in path:
            first_path = path.split()[0]
            if first_path and not (ROOT / first_path).exists():
                missing_targets.append(f"{slug}: {path}")

    if missing_checklists:
        findings.append(f"FAIL: {len(missing_checklists)} autoresearch targets missing checklists: {', '.join(missing_checklists[:8])}")
    if long_checklists:
        findings.append(f"FAIL: {len(long_checklists)} autoresearch checklists exceed 6 questions: {', '.join(long_checklists[:8])}")
    if missing_targets:
        findings.append(f"WARN: {len(missing_targets)} autoresearch target paths missing or stale: {', '.join(missing_targets[:8])}")

    if not RESULTS.exists():
        findings.append("FAIL: agents/autoresearch/results.tsv missing — no central keep/discard/crash ledger")
    else:
        header = RESULTS.read_text(errors="ignore").splitlines()[0] if RESULTS.read_text(errors="ignore").splitlines() else ""
        required = ["date", "run_id", "slug", "baseline_score", "final_score", "status", "description"]
        if not all(col in header.split("\t") for col in required):
            findings.append("FAIL: autoresearch results.tsv header missing required experiment-ledger columns")

    recent_training = "\n".join(training.splitlines()[-30:]).lower()
    if "regression" not in recent_training:
        infos.append("INFO: latest training log entries do not mention regression checks yet")

    if findings:
        print("Self-improvement audit findings:")
        for f in findings:
            print(f)
        for info in infos:
            print(info)
    else:
        print("Self-improvement audit clean: mistake loop, regression checks, and training logs look current.")
        for info in infos:
            print(info)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
