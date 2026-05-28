#!/usr/bin/env python3
"""Script-first preflight runner for the consulting outreach pipeline.

This runner does the deterministic work before any LLM copy generation:
Drive auth preflight, local source loading, M-status dedupe, T3 sent flags,
existing draft/doc checks, warm-up holds, and concise report generation.
It intentionally does not send outreach or create public artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "~/.openclaw/workspace")).expanduser()
PIPELINE_ROOT = Path(os.environ.get("JT_CONSULTING_PIPELINE", "~/projects/jt-consulting-pipeline")).expanduser()
REPORT_DIR = WORKSPACE / "reports" / "outreach-pipeline"
DRIVE_DOC_RE = re.compile(r"https://docs\.google\.com/document/d/([A-Za-z0-9_-]+)")
M_STATUS_RE = re.compile(
    r"\b(M1\s+SENT|M2\s+SENT|M3\b|M4\b|Pitched|Email Pivot|EMAIL PIVOT)\b",
    re.IGNORECASE,
)
T3_SENT_RE = re.compile(r"T3\s+ALREADY\s+SENT", re.IGNORECASE)


@dataclass
class StageResult:
    name: str
    ok: bool
    detail: str


@dataclass
class ProspectState:
    slug: str
    company: str
    local_files: list[str]
    has_outreach_draft: bool
    has_research: bool
    has_brief: bool
    has_warm_up: bool
    has_email_draft: bool
    has_drive_doc_link: bool
    m_sequence_active: bool
    t3_already_sent: bool
    decision: str
    reason: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def run_drive_preflight(workspace: Path) -> StageResult:
    cmd = [sys.executable, str(workspace / "scripts" / "drive_drafts.py"), "--list-folders"]
    try:
        proc = subprocess.run(cmd, cwd=workspace, text=True, capture_output=True, timeout=45)
    except Exception as exc:  # noqa: BLE001 - report exact preflight failure
        return StageResult("drive_auth_preflight", False, f"{type(exc).__name__}: {exc}")
    if proc.returncode == 0 and "Eve" in proc.stdout:
        return StageResult("drive_auth_preflight", True, "Drive auth ok; Eve Drafts root visible.")
    detail = (proc.stderr or proc.stdout or "no output").strip().splitlines()[:4]
    return StageResult("drive_auth_preflight", False, " | ".join(detail))


def load_canonical_names(path: Path) -> dict[str, str]:
    text = read_text(path)
    names: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line or "Shortlist Name" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 2 and parts[0] and parts[1]:
            names[parts[0]] = parts[1]
    return names


def candidate_company_name(slug: str, texts: Iterable[str]) -> str:
    for text in texts:
        for line in text.splitlines()[:20]:
            clean = line.strip("# -*\t")
            if not clean or clean[0] in "{[":
                continue
            if clean and len(clean) < 100 and not clean.lower().startswith(("targeting", "hook", "drive")):
                return clean.split(" - ")[0].split(" | ")[0].strip()
    return slug.replace("-", " ").title()


def collect_shortlist_text(root: Path) -> str:
    pieces = [read_text(root / "pipeline.md")]
    for path in sorted((root / "shortlists").glob("*.md")):
        pieces.append(read_text(path))
    return "\n".join(pieces)


def scan_prospects(root: Path, max_prospects: int | None = None) -> list[ProspectState]:
    clients = root / "clients"
    shortlist_text = collect_shortlist_text(root)
    states: list[ProspectState] = []

    for client_dir in sorted(p for p in clients.iterdir() if p.is_dir()):
        files = {p.name: p for p in client_dir.iterdir() if p.is_file()}
        relevant_names = [
            "outreach-draft.md",
            "research.md",
            "brief.json",
            "brief.md",
            "warm-up.md",
            "email-draft.md",
            "email-pivot.md",
        ]
        texts = [read_text(files[name]) for name in relevant_names if name in files]
        combined = "\n".join(texts)
        slug = client_dir.name
        company = candidate_company_name(slug, texts)
        local_names = sorted(name for name in relevant_names if name in files)
        haystack = combined + "\n" + "\n".join(
            line for line in shortlist_text.splitlines() if slug in line or company.lower() in line.lower()
        )

        has_outreach = "outreach-draft.md" in files
        has_drive_doc = bool(DRIVE_DOC_RE.search(haystack))
        m_active = bool(M_STATUS_RE.search(haystack))
        t3_sent = bool(T3_SENT_RE.search(haystack))
        has_warmup = "warm-up.md" in files

        if any(token in slug for token in ("template", "demo")):
            decision, reason = "skip", "Template/demo folder, not an outreach prospect."
        elif t3_sent:
            decision, reason = "skip", "T3 already sent flag found."
        elif m_active:
            decision, reason = "skip", "M-sequence already active or pitched."
        elif has_outreach and has_drive_doc:
            decision, reason = "skip", "Local outreach draft and Drive doc already exist."
        elif has_warmup and not m_active:
            decision, reason = "warm_up_only", "Warm-up draft exists; do not create full outreach until warmed."
        elif has_outreach:
            decision, reason = "local_review", "Local draft exists; verify Drive/task state before any new copy."
        elif "research.md" in files or "brief.json" in files or "brief.md" in files:
            decision, reason = "eligible_for_copy_review", "Research/brief exists and no active M-status detected."
        else:
            decision, reason = "needs_research", "No research/brief/draft found."

        states.append(
            ProspectState(
                slug=slug,
                company=company,
                local_files=local_names,
                has_outreach_draft=has_outreach,
                has_research="research.md" in files,
                has_brief=("brief.json" in files or "brief.md" in files),
                has_warm_up=has_warmup,
                has_email_draft=("email-draft.md" in files or "email-pivot.md" in files),
                has_drive_doc_link=has_drive_doc,
                m_sequence_active=m_active,
                t3_already_sent=t3_sent,
                decision=decision,
                reason=reason,
            )
        )
        if max_prospects and len(states) >= max_prospects:
            break
    return states


def summarize(states: list[ProspectState]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for state in states:
        counts[state.decision] = counts.get(state.decision, 0) + 1
    return counts


def write_reports(
    states: list[ProspectState],
    stages: list[StageResult],
    canonical_count: int,
    dry_run: bool,
) -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d")
    json_path = REPORT_DIR / f"{stamp}-script-first-preflight.json"
    md_path = REPORT_DIR / f"{stamp}-script-first-preflight.md"
    summary = summarize(states)
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dry_run": dry_run,
        "pipeline_root": str(PIPELINE_ROOT),
        "canonical_drive_names": canonical_count,
        "stages": [asdict(s) for s in stages],
        "summary": summary,
        "prospects": [asdict(s) for s in states],
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        f"# Outreach Pipeline Script-First Preflight - {stamp}",
        "",
        f"Dry run: {dry_run}",
        f"Prospects scanned: {len(states)}",
        f"Canonical Drive names loaded: {canonical_count}",
        "",
        "## Stage Results",
    ]
    for stage in stages:
        status = "PASS" if stage.ok else "FAIL"
        lines.append(f"- {status}: {stage.name} - {stage.detail}")
    lines += ["", "## Decision Summary"]
    for key, value in sorted(summary.items()):
        lines.append(f"- {key}: {value}")
    lines += ["", "## Copy Review Queue"]
    queue = [s for s in states if s.decision in {"eligible_for_copy_review", "local_review", "warm_up_only"}]
    if not queue:
        lines.append("- None.")
    for state in queue[:25]:
        lines.append(f"- {state.company} (`{state.slug}`): {state.decision} - {state.reason}")
    lines += [
        "",
        "## Safety Notes",
        "- This runner does not send outreach.",
        "- This runner does not create public profiles or external messages.",
        "- LLM copy generation should only run after this report identifies an eligible copy-review item.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run outreach pipeline deterministic preflight stages.")
    parser.add_argument("--dry-run", action="store_true", help="Report only; default behavior also reports only.")
    parser.add_argument("--max-prospects", type=int, default=None, help="Limit client folder scan for testing.")
    parser.add_argument("--json", action="store_true", help="Print compact JSON summary.")
    args = parser.parse_args()

    stages: list[StageResult] = []
    required = [
        PIPELINE_ROOT / "pipeline.md",
        PIPELINE_ROOT / "drive-canonical-names.md",
        PIPELINE_ROOT / "EMAIL-PIVOT-RULES.md",
        WORKSPACE / "scripts" / "drive_drafts.py",
    ]
    missing = [str(p) for p in required if not p.exists()]
    stages.append(StageResult("source_file_preflight", not missing, "missing: " + ", ".join(missing) if missing else "required files present"))
    stages.append(run_drive_preflight(WORKSPACE))

    canonical = load_canonical_names(PIPELINE_ROOT / "drive-canonical-names.md")
    stages.append(StageResult("canonical_drive_names", bool(canonical), f"{len(canonical)} canonical names loaded"))

    states = scan_prospects(PIPELINE_ROOT, args.max_prospects)
    stages.append(StageResult("prospect_scan", bool(states), f"{len(states)} client folders scanned"))

    json_path, md_path = write_reports(states, stages, len(canonical), dry_run=True)
    output = {
        "ok": all(s.ok for s in stages if s.name != "drive_auth_preflight"),
        "drive_auth_ok": next((s.ok for s in stages if s.name == "drive_auth_preflight"), False),
        "prospects_scanned": len(states),
        "summary": summarize(states),
        "json_report": str(json_path),
        "md_report": str(md_path),
    }
    print(json.dumps(output, indent=2 if args.json else None, sort_keys=True))
    return 0 if output["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
