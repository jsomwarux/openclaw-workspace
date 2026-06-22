#!/usr/bin/env python3
"""Verify Passive Income Strategist produced today's artifact and delivery.

This guard exists because OpenClaw cron status can be ok even when the isolated
agent did not create the strategist report or Telegram delivery was not marked
delivered. It is intentionally deterministic and small.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path.home() / ".openclaw" / "workspace"
PI_DIR = ROOT / "memory" / "passive-income"
JOB_ID = "922082ee-da62-4b6e-b9e3-909c3446e381"
TARGET = "6608544825"


def sh(cmd: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)


def telegram_send(text: str) -> str | None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("TELEGRAM_BOT_TOKEN missing", file=sys.stderr)
        return None
    data = urllib.parse.urlencode({"chat_id": TARGET, "text": text}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8", "replace")
            ok = json.loads(body).get("ok")
            if not ok:
                print(body, file=sys.stderr)
                return None
            data = json.loads(body)
            return str(data.get("result", {}).get("message_id") or "")
    except Exception as e:
        print(f"telegram_send failed: {e}", file=sys.stderr)
        return None


def write_delivery_marker(marker: Path, report: Path, message_id: str, mode: str) -> None:
    marker.write_text(
        json.dumps(
            {
                "ok": True,
                "channel": "telegram",
                "target": TARGET,
                "messageId": message_id,
                "report": str(report),
                "sentAt": datetime.now(ZoneInfo("America/New_York")).isoformat(),
                "mode": mode,
            },
            indent=2,
        )
        + "\n"
    )


def latest_run() -> dict:
    # `openclaw cron runs` currently emits JSON without --json.
    cp = sh(["openclaw", "cron", "runs", "--id", JOB_ID, "--limit", "1"], timeout=20)
    if cp.returncode != 0:
        return {"error": cp.stderr or cp.stdout, "returncode": cp.returncode}
    try:
        data = json.loads(cp.stdout)
        entries = data.get("entries") or []
        return entries[0] if entries else {"error": "no run entries"}
    except Exception as e:
        return {"error": f"failed to parse cron runs JSON: {e}", "raw": cp.stdout[:1000]}


def summarize_report(path: Path) -> str:
    text = path.read_text(errors="replace")
    lines = text.splitlines()
    # Keep this Telegram-safe and useful. Prefer top sections + verdict/count lines.
    picked: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#") or "BUILD" in s or "WATCH" in s or "PASS" in s or "Verdict" in s or "Score:" in s:
            picked.append(s)
        if len("\n".join(picked)) > 2600:
            break
    if not picked:
        picked = lines[:40]
    digest = "\n".join(picked).strip()
    if len(digest) > 3000:
        digest = digest[:2950].rstrip() + "\n…"
    return digest


def create_degraded_report(root: Path = ROOT, date: str | None = None) -> Path:
    """Write a conservative strategist fallback from the same-day Scout report."""
    date = date or datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
    pi_dir = root / "memory" / "passive-income"
    scout = pi_dir / f"{date}-scout.md"
    report = pi_dir / f"{date}-strategist.md"
    scout_text = scout.read_text(errors="replace") if scout.exists() else ""
    idea_lines: list[str] = []
    for line in scout_text.splitlines():
        s = line.strip()
        if s.startswith("### Idea") or s.startswith("- **Concept:**"):
            idea_lines.append(s)
        if len(idea_lines) >= 12:
            break
    if not idea_lines:
        idea_lines = ["- No parseable ideas found in the same-day Scout report."]
    body = "\n".join(
        [
            f"# Passive Income Strategist - {date}",
            "",
            "Status: DEGRADED FALLBACK",
            "",
            "The LLM Strategist run did not produce a fresh report, but the same-day Scout handoff exists. This fallback prevents a stale blocked report from remaining as the pipeline state.",
            "",
            "## Verdict",
            "No BUILD recommendation from this fallback. Treat all ideas as WATCH until a full Strategist pass validates saturation, demand, competition, autonomy, and revenue ceiling.",
            "",
            "## Scout Ideas Preserved",
            *idea_lines,
            "",
            "## Counts",
            "- BUILD: 0",
            "- WATCH: all preserved Scout seeds",
            "- PASS: 0",
            "",
            "## Mission Control",
            "No Mission Control task changes from fallback mode.",
            "",
            "## Next Step",
            "Run the full Strategist when the isolated LLM runner is stable, or keep this as a degraded weekly record if passive-income work is not the current priority.",
        ]
    )
    pi_dir.mkdir(parents=True, exist_ok=True)
    report.write_text(body + "\n")
    return report


def report_is_blocked(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(errors="replace")[:3000]
    return (
        "## Status" in text
        and "BLOCKED" in text
        and "Pre-strategist handoff check failed" in text
    )


def run_message_tool_delivered(run: dict) -> bool:
    delivery = run.get("delivery") if isinstance(run.get("delivery"), dict) else {}
    if delivery.get("delivered") is True:
        return True
    sent_to = delivery.get("messageToolSentTo")
    return isinstance(sent_to, list) and len(sent_to) > 0


def marker_confirms_report(marker: Path, report: Path) -> bool:
    if not marker.exists() or not report.exists():
        return False
    try:
        state = json.loads(marker.read_text(errors="replace"))
    except Exception:
        return False
    if marker.stat().st_mtime < report.stat().st_mtime:
        return False
    return (
        state.get("ok") is True
        and state.get("channel") == "telegram"
        and str(state.get("target")) == TARGET
        and bool(state.get("messageId"))
        and state.get("report") == str(report)
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d"))
    ap.add_argument("--send", action="store_true", help="Send Telegram alert/resend when verification fails")
    args = ap.parse_args()

    report = PI_DIR / f"{args.date}-strategist.md"
    scout = PI_DIR / f"{args.date}-scout.md"
    marker = PI_DIR / f"{args.date}-strategist-delivery.json"
    if scout.exists() and scout.stat().st_size >= 500:
        report_stale = report.exists() and report.stat().st_mtime < scout.stat().st_mtime
        report_bad = (not report.exists()) or report.stat().st_size < 500 or report_stale
        if report_bad:
            report = create_degraded_report(ROOT, args.date)
    run = latest_run()
    cron_delivered = (
        run.get("delivered") is True
        or run.get("deliveryStatus") == "delivered"
        or run_message_tool_delivered(run)
    )
    status = run.get("status")
    blocked_report = report_is_blocked(report)

    marker_state: dict = {"exists": marker.exists()}
    message_tool_delivered = False
    if marker.exists():
        try:
            marker_state.update(json.loads(marker.read_text(errors="replace")))
            message_tool_delivered = marker_confirms_report(marker, report)
            marker_state["fresh_for_report"] = message_tool_delivered
        except Exception as e:
            marker_state["error"] = f"failed to parse marker: {e}"

    delivered = cron_delivered or message_tool_delivered

    problems: list[str] = []
    if not blocked_report and (not scout.exists() or scout.stat().st_size < 500):
        problems.append(f"Scout missing/too small: {scout}")
    if not report.exists() or (report.stat().st_size < 500 and not blocked_report):
        problems.append(f"Strategist report missing/too small: {report}")
    if status != "ok" and not message_tool_delivered:
        problems.append(f"Latest strategist run status is {status!r}")
    if not delivered:
        problems.append(
            "Strategist delivery not confirmed by cron or message-tool marker: "
            f"cron delivered={run.get('delivered')} deliveryStatus={run.get('deliveryStatus')} "
            f"marker={marker_state}"
        )

    result = {
        "ok": not problems,
        "date": args.date,
        "report": str(report),
        "report_exists": report.exists(),
        "report_size": report.stat().st_size if report.exists() else 0,
        "blocked_report": blocked_report,
        "delivery_marker": marker_state,
        "message_tool_delivered": message_tool_delivered,
        "cron_delivered": cron_delivered,
        "latest_run": {
            "ts": run.get("ts"),
            "status": run.get("status"),
            "delivered": run.get("delivered"),
            "deliveryStatus": run.get("deliveryStatus"),
            "durationMs": run.get("durationMs"),
            "sessionKey": run.get("sessionKey"),
        },
        "problems": problems,
    }
    print(json.dumps(result, indent=2))

    if problems and args.send:
        if report.exists() and report.stat().st_size >= 500:
            msg = "⚠️ Passive Income Strategist delivery guard: cron delivery was not confirmed, so I’m resending the digest.\n\n" + summarize_report(report)
        else:
            msg = (
                "🚨 Passive Income Strategist failed silently today.\n\n"
                f"Date: {args.date}\n"
                f"Problems:\n- " + "\n- ".join(problems) + "\n\n"
                "No valid strategist report exists, so there is nothing safe to resend. Eve needs to rerun the strategist."
            )
        message_id = telegram_send(msg)
        if message_id:
            write_delivery_marker(marker, report, message_id, "delivery-guard-fallback")
            print(f"telegram_guard_action=sent messageId={message_id}")
            return 0
        return 3

    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
