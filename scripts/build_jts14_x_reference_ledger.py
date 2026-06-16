#!/usr/bin/env python3
"""Build the @jts_14 X reference ledger from saved local research artifacts."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class LedgerRow:
    source: str
    url: str
    lane: str
    why_selected: str
    analyzed: str
    influence_type: str
    applied_to: str


def read_if_exists(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def workspace_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def clean(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = value.replace("|", "/")
    return value


def lane_for(text: str) -> str:
    lower = text.lower()
    if "agentforce" in lower or "salesforce" in lower:
        return "Insurance / Agentforce Operations"
    if "x402" in lower or "wallet" in lower or "transact" in lower or "payment" in lower:
        return "x402 / Agentic Payments"
    if "solo" in lower or "one-person" in lower or "agency" in lower:
        return "Productized Services / Solo Operator Systems"
    if "smb" in lower or "buyer" in lower:
        return "SMB AI Implementation"
    if "local" in lower or "mac mini" in lower or "agent" in lower or "workflow" in lower:
        return "AI Operating Systems / Agent Orchestration"
    if "app" in lower or "distribution" in lower:
        return "App Growth / App Marketing OS"
    return "AI Operating Systems / Agent Orchestration"


def analyzed_mechanic(text: str) -> str:
    lower = text.lower()
    if "production" in lower or "sessions" in lower or "meetings" in lower:
        return "Production numbers create credibility, then invite inspection of queues, approvals, and logs."
    if "agentforce" in lower or "script" in lower or "canvas" in lower:
        return "Tool-control language points toward explicit stop rules and behavior design."
    if "local" in lower or "mac mini" in lower:
        return "Concrete hardware and cost details make local-first implementation tangible."
    if "wallet" in lower or "transact" in lower:
        return "Transaction framing raises the need for budgets, receipts, and shutdown rules."
    if "resource" in lower or "roundup" in lower or "list" in lower:
        return "Resource-list structure can earn saves, but risks generic engagement bait."
    if "low" in lower or "generic" in lower or "promo" in lower:
        return "Rejected because the source did not supply a buyer-specific or proof-specific mechanic."
    return "Source supplied structure or constraint signal for governed AI workflow content."


def source_label(raw: str) -> str:
    match = re.search(r"@([A-Za-z0-9_]+)", raw)
    return f"@{match.group(1)}" if match else "Saved report finding"


def extract_url(raw: str) -> str:
    match = re.search(r"https://(?:x\.com|twitter\.com)/\S+", raw)
    return match.group(0).rstrip(").,") if match else ""


def parse_usable_posts(report_text: str) -> list[LedgerRow]:
    rows: list[LedgerRow] = []
    in_section = False
    for line in report_text.splitlines():
        if re.match(r"^##\s+Usable Posts\b", line, re.I):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.strip().startswith("- "):
            continue
        url = extract_url(line)
        if not url:
            continue
        body = clean(line.lstrip("- "))
        rows.append(
            LedgerRow(
                source=source_label(body),
                url=url,
                lane=lane_for(body),
                why_selected=body.split("Relevant because", 1)[-1].strip(". ") if "Relevant because" in body else body,
                analyzed=analyzed_mechanic(body),
                influence_type="Structure",
                applied_to="Supported 2026-06-15 X queue and reply-target mechanics.",
            )
        )
    return rows


def parse_reply_targets(reply_text: str) -> list[LedgerRow]:
    rows: list[LedgerRow] = []
    blocks = re.split(r"\n(?=##\s+@)", reply_text)
    for block in blocks:
        if not block.lstrip().startswith("## @"):
            continue
        url = extract_url(block)
        if not url:
            continue
        first_line = block.splitlines()[0]
        draft = ""
        for line in block.splitlines():
            if line.lower().startswith("draft reply:"):
                draft = line.split(":", 1)[1].strip()
                break
        body = clean(f"{first_line} {draft}")
        rows.append(
            LedgerRow(
                source=source_label(first_line),
                url=url,
                lane=lane_for(body),
                why_selected="Reply target showed a usable current conversation around AI workflow control.",
                analyzed=analyzed_mechanic(body),
                influence_type="Structure",
                applied_to="Applied to reply draft structure and validated future X reply posture.",
            )
        )
    return rows


def parse_weekly_reference_rows(weekly_text: str) -> list[LedgerRow]:
    rows: list[LedgerRow] = []
    chunks = re.split(r"\n(?=Reference row\s+\d+:)", weekly_text, flags=re.I)
    for chunk in chunks:
        if "Source URL:" not in chunk:
            continue
        url_match = re.search(r"Source URL:\s*(https://(?:x\.com|twitter\.com)/\S+)", chunk)
        if not url_match:
            continue
        niche_match = re.search(r"^Niche:\s*(.+)$", chunk, flags=re.I | re.M)
        mechanic_match = re.search(r"^Hook mechanic:\s*(.+)$", chunk, flags=re.I | re.M)
        translation_match = re.search(r"^JT translation:\s*(.+)$", chunk, flags=re.I | re.M)
        source = source_label(url_match.group(1))
        rows.append(
            LedgerRow(
                source=source,
                url=url_match.group(1).rstrip(".,)"),
                lane=clean(niche_match.group(1)) if niche_match else lane_for(chunk),
                why_selected="Already selected in the weekly artifact as a reference mechanic.",
                analyzed=clean(mechanic_match.group(1)) if mechanic_match else analyzed_mechanic(chunk),
                influence_type="Structure",
                applied_to=clean(translation_match.group(1)) if translation_match else "Applied to weekly X reference mechanics.",
            )
        )
    return rows


def parse_rejections(report_text: str, report_path: Path) -> list[LedgerRow]:
    rows: list[LedgerRow] = []
    in_section = False
    saved_url = f"saved in `{workspace_rel(report_path)}`"
    for line in report_text.splitlines():
        if re.match(r"^##\s+Low Signal / Rejected\b", line, re.I):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.strip().startswith("- "):
            continue
        body = clean(line.lstrip("- "))
        rows.append(
            LedgerRow(
                source="Rejected query cluster",
                url=saved_url,
                lane=lane_for(body),
                why_selected=body,
                analyzed=analyzed_mechanic(body),
                influence_type="Rejected",
                applied_to="Not applied to drafts; recorded as a constraint against generic source use.",
            )
        )
    return rows


def add_weekly_constraints(rows: list[LedgerRow], report_path: Path, report_text: str) -> list[LedgerRow]:
    saved_url = f"saved in `{workspace_rel(report_path)}`"
    rows.append(
        LedgerRow(
            source="Source coverage contract",
            url=saved_url,
            lane="AI Operating Systems / Agent Orchestration",
            why_selected="The ledger is built from saved local X research artifacts rather than prompt memory.",
            analyzed="Every weekly X draft should be traceable to an applied, rejected, or constraining source row.",
            influence_type="Constraint",
            applied_to="Supports future verification; not applied as a standalone topic.",
        )
    )
    if "NO_STRONG_SIGNAL" in report_text:
        rows.append(
            LedgerRow(
                source="Run-level signal judgment",
                url=saved_url,
                lane="AI Operating Systems / Agent Orchestration",
                why_selected="The run explicitly marked NO_STRONG_SIGNAL after thin core query results.",
                analyzed="No new topic should be overclaimed from this run; use only structure, replies, or constraints.",
                influence_type="Constraint",
                applied_to="Constrained 2026-06-15 X content to existing proof and governance mechanics.",
            )
        )
    return rows


def render(date_label: str, rows: list[LedgerRow], sources: list[Path]) -> str:
    lines = [
        f"# jts_14 X Reference Ledger - Week of {date_label}",
        "",
        "Purpose: make @jts_14 X research inspectable from source to draft.",
        "",
        "## Source artifacts",
    ]
    for source in sources:
        if source.exists():
            lines.append(f"- `{workspace_rel(source)}`")
    lines.extend(
        [
            "",
            "## Standard",
            "- `Topic selection`: source directly influenced what the post was about.",
            "- `Structure`: source influenced hook shape, reply shape, pacing, format, or compression.",
            "- `Credibility/proof`: source validated proof, operating surfaces, or stack specificity.",
            "- `Niche signal only`: source reinforced future direction but did not touch a draft.",
            "- `Rejected`: source was reviewed and excluded.",
            "- `Constraint`: run-level finding that limits what the drafts may claim.",
            "",
            "## Applied References",
            "",
            "| Source | URL | Lane | Why selected | Analyzed | Influence type | Applied to |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    clean(row.source),
                    clean(row.url),
                    clean(row.lane),
                    clean(row.why_selected),
                    clean(row.analyzed),
                    clean(row.influence_type),
                    clean(row.applied_to),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Week-Level Judgment",
            "Topic selection came from current proof and weekly recovery needs. X research mainly supplied structure, reply posture, credibility/proof mechanics, rejected source constraints, and the run-level NO_STRONG_SIGNAL constraint.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_ledger(report: Path, replies: Path | None, weekly: Path | None, output: Path) -> list[LedgerRow]:
    report_text = read_if_exists(report)
    reply_text = read_if_exists(replies)
    weekly_text = read_if_exists(weekly)

    rows: list[LedgerRow] = []
    rows.extend(parse_usable_posts(report_text))
    rows.extend(parse_reply_targets(reply_text))
    rows.extend(parse_weekly_reference_rows(weekly_text))
    rows.extend(parse_rejections(report_text, report))
    rows = add_weekly_constraints(rows, report, report_text)

    if not rows:
        raise SystemExit("No ledger rows could be built from the provided artifacts.")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(output_date(output), rows, [report, replies or Path(), weekly or Path()]), encoding="utf-8")
    return rows


def output_date(output: Path) -> str:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", output.name)
    return match.group(1) if match else date.today().isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the weekly @jts_14 X reference ledger from saved artifacts.")
    parser.add_argument("--report", required=True, type=Path, help="Saved X research report markdown")
    parser.add_argument("--replies", type=Path, help="Saved X reply-target markdown")
    parser.add_argument("--weekly", type=Path, help="Weekly content artifact with X reference mechanics")
    parser.add_argument("--output", required=True, type=Path, help="Output ledger markdown path")
    args = parser.parse_args()

    rows = build_ledger(report=args.report, replies=args.replies, weekly=args.weekly, output=args.output)
    print(f"WROTE_JTS14_LEDGER {args.output} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
