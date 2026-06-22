#!/usr/bin/env python3
"""Create a guaranteed Passive Income Scout handoff from local signal files.

This is a fallback-first artifact writer for the Sunday Scout cron. The LLM can
later enrich or overwrite the report, but the Strategist should never be left
without a same-day scout file when local signals are readable.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
PI_DIR = Path("memory") / "passive-income"
STATE_PATH = Path("agents") / "passive-income-scout" / "state.json"
SIGNAL_FILES = [
    "weekly-trends.md",
    "weekly-exploding-topics.md",
    "weekly-google-trends.md",
    "weekly-apis.md",
    "weekly-trustmrr.json",
]


@dataclass
class HandoffResult:
    path: Path
    idea_count: int
    source_count: int


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(errors="ignore")


def _clean_line(line: str) -> str:
    line = re.sub(r"^[#*\-\s>`|0-9.]+", "", line).strip()
    line = re.sub(r"\s+", " ", line)
    return line[:120]


def _signal_phrases(root: Path) -> list[str]:
    phrases: list[str] = []
    for name in SIGNAL_FILES:
        path = root / PI_DIR / name
        text = _read(path)
        if not text:
            continue
        if name.endswith(".json"):
            try:
                text = json.dumps(json.loads(text), ensure_ascii=True)
            except json.JSONDecodeError:
                pass
        for raw in text.splitlines():
            line = _clean_line(raw)
            if len(line) < 18:
                continue
            if line.lower().startswith(("http", "source", "updated", "generated")):
                continue
            phrases.append(line)
            if len(phrases) >= 18:
                return phrases
    return phrases


def _ideas(phrases: list[str]) -> list[tuple[str, str]]:
    seeds = phrases or [
        "local operators need narrow AI tools that convert messy workflow evidence into decisions",
        "buyers want source-backed comparison pages instead of generic AI recommendations",
        "small teams need lightweight compliance and document review without enterprise software",
        "creators and sellers need repeatable trend-to-product validation loops",
    ]
    templates = [
        ("OpsProof Radar", "source-backed exception and proof packets for ops-heavy SMB workflows"),
        ("NicheRank Pages", "AI-assisted comparison pages for one underserved buying category"),
        ("ComplianceCard Desk", "small-business claim, permit, or document risk cards with citations"),
        ("CreatorSignal Kit", "trend-to-offer briefs for creators selling digital or affiliate products"),
    ]
    out: list[tuple[str, str]] = []
    for i, (name, angle) in enumerate(templates):
        signal = seeds[i % len(seeds)]
        out.append((name, f"{angle}. Seed signal: {signal}"))
    return out


def _update_state(root: Path, date: str) -> None:
    path = root / STATE_PATH
    state = {}
    if path.exists():
        try:
            state = json.loads(path.read_text())
        except json.JSONDecodeError:
            state = {}
    dates = state.get("run_dates", [])
    if date not in dates:
        dates.append(date)
    state["run_dates"] = dates
    state["last_run"] = date
    state["last_handoff_mode"] = "deterministic"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n")


def generate_handoff(root: Path = ROOT, date: str | None = None, overwrite: bool = False) -> HandoffResult:
    date = date or datetime.now().strftime("%Y-%m-%d")
    pi_dir = root / PI_DIR
    pi_dir.mkdir(parents=True, exist_ok=True)
    path = pi_dir / f"{date}-scout.md"
    if path.exists() and path.stat().st_size >= 500 and not overwrite:
        return HandoffResult(path=path, idea_count=0, source_count=0)

    phrases = _signal_phrases(root)
    ideas = _ideas(phrases)
    source_lines = []
    for name in SIGNAL_FILES:
        signal_path = pi_dir / name
        state = "present" if signal_path.exists() and signal_path.stat().st_size > 0 else "missing"
        size = signal_path.stat().st_size if signal_path.exists() else 0
        source_lines.append(f"- `{name}`: {state}, {size} bytes")

    idea_blocks = []
    for idx, (name, angle) in enumerate(ideas, start=1):
        idea_blocks.append(
            "\n".join(
                [
                    f"### Idea {idx}: {name}",
                    f"- **Concept:** {angle}.",
                    "- **Why it fits JT:** buildable with existing OpenClaw/coding-agent stack, low manual ops, and useful as a strategist input.",
                    "- **Revenue path to validate:** one narrow paid report, subscription, affiliate, or lead-gen event.",
                    "- **Strategist caveat:** this is a deterministic handoff seed; score confidence lower unless follow-up research confirms demand.",
                ]
            )
        )

    report = "\n\n".join(
        [
            f"# Passive Income Scout - {date}",
            "Status: DETERMINISTIC HANDOFF",
            "This file was written at the start of the Scout cron so the Strategist has a same-day artifact even if optional live research or LLM enrichment fails later.",
            "## Source Files",
            "\n".join(source_lines),
            "## Signal Seeds",
            "\n".join(f"- {p}" for p in phrases[:8]) or "- No readable signal phrases extracted; used fallback JT-fit patterns.",
            "## Raw Ideas",
            "\n\n".join(idea_blocks),
            "## Required Follow-Up",
            "If the LLM Scout finishes successfully, replace this with a richer 4-6 idea report. If it does not, the Strategist may evaluate these seeds as degraded inputs and must state the confidence caveat.",
        ]
    )
    path.write_text(report + "\n")
    _update_state(root, date)
    return HandoffResult(path=path, idea_count=len(ideas), source_count=len([p for p in SIGNAL_FILES if (pi_dir / p).exists()]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    result = generate_handoff(root=Path(args.root), date=args.date, overwrite=args.overwrite)
    print(f"PASSIVE_INCOME_SCOUT_HANDOFF path={result.path} ideas={result.idea_count} sources={result.source_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
