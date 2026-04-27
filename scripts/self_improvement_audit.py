#!/usr/bin/env python3
"""Audit Eve's self-improvement loop.

Checks whether recent mistake entries include the six required fields and whether
regression checks exist. Read-only by default; prints actionable findings.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MISTAKES = ROOT / "docs/agents/mistakes-log-recent.md"
REGRESSION = ROOT / "docs/agents/regression-checks.md"
TRAINING = ROOT / "memory/training/training-log.md"
TARGETS = ROOT / "agents/autoresearch/targets.md"

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


def has_any(block: str, terms: list[str]) -> bool:
    b = block.lower()
    return any(t in b for t in terms)


def main() -> int:
    mistakes = read(MISTAKES)
    regression = read(REGRESSION)
    training = read(TRAINING)
    targets = read(TARGETS)

    findings: list[str] = []

    if not regression:
        findings.append("FAIL: docs/agents/regression-checks.md missing")
    elif "## Active Checks" not in regression:
        findings.append("FAIL: regression-checks.md missing Active Checks section")

    blocks = section_blocks(mistakes)
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
    for line in targets.splitlines():
        if line.startswith("|") and " pending " in line:
            pending.append(line)
    if pending:
        findings.append(f"WARN: {len(pending)} autoresearch targets are pending; prioritize high-use ones")

    recent_training = "\n".join(training.splitlines()[-30:]).lower()
    if "regression" not in recent_training:
        findings.append("INFO: latest training log entries do not mention regression checks yet")

    if findings:
        print("Self-improvement audit findings:")
        for f in findings:
            print(f)
    else:
        print("Self-improvement audit clean: mistake loop, regression checks, and training logs look current.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
