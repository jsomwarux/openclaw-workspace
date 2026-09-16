#!/usr/bin/env python3
"""outreach_update.py — Update prospect outreach status after JT confirms a send."""
import argparse, json, re, subprocess, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

PIPELINE_PATH = Path.home() / "projects/jt-consulting-pipeline" / "pipeline.md"
MC_API = "http://localhost:3000/api/tasks"
RUNTIME_OWNER_ROOT = "/Users/jtsomwaru/.openclaw/workspace/mission-control"
RUNTIME_OWNER_NODE = "/opt/homebrew/opt/node@22/bin/node"
RUNTIME_OWNER_SCRIPT = "/Users/jtsomwaru/.openclaw/workspace/mission-control/scripts/outreach-runtime-secrets.mjs"
RUNTIME_OWNER_TIMEOUT_SECONDS = 60
CONFIRMED_SEND_MAX_SKEW_SECONDS = 60
PRE_SEND_RECEIPT_ID = re.compile(r"pre_send_[0-9a-f]{20}")
SENT_EVENT_ID = re.compile(r"suppression_event_[0-9a-f]{20}")
HEX_64 = re.compile(r"[0-9a-f]{64}")
UTC_SECONDS = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


class ConfirmedSendError(RuntimeError):
    """A safe, operator-facing cohort-two confirmation failure."""


def record_cohort_two_confirmed_send(pre_send_receipt_id, *, now=None):
    """Record cohort-two send state using only one opaque immutable receipt ID."""
    if not isinstance(pre_send_receipt_id, str) or not PRE_SEND_RECEIPT_ID.fullmatch(
        pre_send_receipt_id
    ):
        raise ConfirmedSendError("cohort-two pre-send receipt ID is invalid")
    command = [
        RUNTIME_OWNER_NODE,
        RUNTIME_OWNER_SCRIPT,
        "record-confirmed-send",
        "--pre-send-receipt-id",
        pre_send_receipt_id,
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=RUNTIME_OWNER_ROOT,
            env={"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONHASHSEED": "0"},
            text=True,
            capture_output=True,
            timeout=RUNTIME_OWNER_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ConfirmedSendError(
            "cohort-two confirmed-send owner is unavailable"
        ) from exc

    if completed.returncode != 0 or completed.stderr or completed.stdout.count("\n") != 1:
        raise ConfirmedSendError(
            "cohort-two confirmed-send owner rejected the receipt"
        )
    try:
        result = json.loads(completed.stdout)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ConfirmedSendError(
            "cohort-two confirmed-send owner rejected the receipt"
        ) from exc
    expected = {
        "status", "preSendReceiptId", "sentEventId", "ownerRevision", "observedAt"
    }
    observed_at = result.get("observedAt") if isinstance(result, dict) else None
    if (
        not isinstance(result, dict)
        or set(result) != expected
        or result.get("status") != "RECORDED"
        or result.get("preSendReceiptId") != pre_send_receipt_id
        or not isinstance(result.get("sentEventId"), str)
        or not SENT_EVENT_ID.fullmatch(result["sentEventId"])
        or not isinstance(result.get("ownerRevision"), str)
        or not HEX_64.fullmatch(result["ownerRevision"])
        or not isinstance(observed_at, str)
        or not UTC_SECONDS.fullmatch(observed_at)
    ):
        raise ConfirmedSendError(
            "cohort-two confirmed-send owner rejected the receipt"
        )
    try:
        observed = datetime.strptime(observed_at, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError as exc:
        raise ConfirmedSendError(
            "cohort-two confirmed-send owner rejected the receipt"
        ) from exc
    current = now if now is not None else datetime.now(timezone.utc)
    if current.tzinfo is None or abs((current - observed).total_seconds()) > CONFIRMED_SEND_MAX_SKEW_SECONDS:
        raise ConfirmedSendError(
            "cohort-two confirmed-send owner rejected the receipt"
        )
    return result

def load_outreach_draft(slug):
    p = Path.home() / f"projects/jt-consulting-pipeline/clients/{slug}/outreach-draft.md"
    if not p.exists(): raise FileNotFoundError(str(p))
    return p, p.read_text()

def update_outreach_draft(path, content, message, channel, date):
    msg_num = message.upper()
    # Find Status line
    m = re.search(r'^(\*?Status[^\n]*\n)', content, re.MULTILINE)
    if not m:
        content += f"\n*Status: {msg_num} SENT {date} ({channel})*\n"
    else:
        old = m.group(1).strip()
        existing = re.findall(r'(M\d)\s+SENT\s+(\d{4}-\d{2}-\d{2})', old)
        parts = [f"{msg_num} SENT {date} ({channel})"]
        for mn, d in existing:
            if mn != msg_num: parts.append(f"{mn} SENT {d}")
        m3 = re.search(r'(M3 (?:READY|due)[^\n]*)', old)
        if m3 and msg_num != "M3": parts.append(m3.group(1))
        new = f"*Status: {' | '.join(parts)}*"
        content = content[:m.start()] + new + "\n" + content[m.end():]
    path.write_text(content)
    return content

def update_pipeline_md(slug, message, channel):
    if not PIPELINE_PATH.exists():
        print(f"WARNING: pipeline.md not found"); return
    c = PIPELINE_PATH.read_text()
    m = re.search(rf'^(\| .+? \|.*? \|.*? \|.*? \| .+? \| {re.escape(slug)} \|)', c, re.MULTILINE)
    if not m:
        print(f"WARNING: {slug} not in pipeline.md"); return
    row = m.group(1)
    mn = message.upper()
    if mn == "M1":
        new_row = re.sub(r'📤 Outreach Drafted', f'✉️ Pitched (M1)', row)
    elif mn == "M2":
        new_row = re.sub(r'✉️ Pitched \(M1\)', '✉️ Pitched (M2)', row)
    elif mn == "M3":
        new_row = re.sub(r'✉️ Pitched \(M2\)', '✉️ Pitched (M3)', row)
    else:
        new_row = row
    c = c[:m.start()] + new_row + c[m.end():]
    PIPELINE_PATH.write_text(c)
    print(f"✅ pipeline.md: {slug} → ✉️ Pitched ({mn})")

def fetch_tasks():
    data = json.loads(urllib.request.urlopen(MC_API).read())
    return data.get("tasks", data) if isinstance(data, dict) else data


def patch_task(task_id, fields):
    d = json.dumps({"id": task_id, **fields}).encode()
    r = urllib.request.Request(MC_API, data=d, method="PATCH", headers={"Content-Type":"application/json"})
    urllib.request.urlopen(r)


def close_mc_task(slug, company):
    try:
        tasks = fetch_tasks()
    except Exception as e:
        print(f"WARNING: MC fetch failed: {e}"); return
    closed = 0
    company_tokens = [tok.lower() for tok in re.findall(r"[A-Za-z0-9]+", company) if len(tok) > 2]
    slug_phrase = slug.replace("-", " ").lower()
    for t in tasks:
        title = t.get("title", "")
        description = t.get("description", "")
        if t.get("status") == "done":
            continue
        if t.get("slug") and t.get("slug") != slug:
            continue
        if not any(marker in title for marker in ["Review + Send", "Email Pivot"]):
            continue
        haystack = f"{title} {description}".lower()
        exact_slug_match = slug in haystack or slug_phrase in haystack
        exact_company_match = bool(company_tokens) and all(tok in haystack for tok in company_tokens)
        if not (exact_slug_match or exact_company_match):
            continue
        try:
            patch_task(t["_id"], {"status": "done"})
            print(f"✅ MC task closed: {title}")
            closed += 1
        except Exception as e:
            print(f"WARNING: could not close task: {e}")
    if not closed:
        print("ℹ️  No matching active Review + Send / Email Pivot MC task found")


def create_followup_task(slug, company, message):
    mn = message.upper()
    if mn == "M1":
        next_m, title, desc = "M2", f"M2: {company} — Follow-up", (
            "First action: 3–4 days after M1, check whether the LinkedIn/email reply path changed; if no reply, send the approved M2 follow-up from the outreach draft.\n\n"
            "Why it matters: follow-ups should advance one selected prospect without recreating stale outreach clutter.\n\n"
            "Done state: M2 is sent or intentionally skipped, `outreach-draft.md`/`pipeline.md` are updated, and this task is closed."
        )
    elif mn == "M2":
        next_m, title, desc = "M3", f"M3: {company} — Final follow-up", (
            "First action: 5–7 days after M2, check for reply/connection acceptance; if no reply, send the final approved M3 touch or mark the prospect cold.\n\n"
            "Why it matters: final touches must close the loop instead of leaving cold outreach chains open indefinitely.\n\n"
            "Done state: M3 is sent or the prospect is marked cold, `outreach-draft.md`/`pipeline.md` are updated, and this task is closed."
        )
    else: return
    # Read draft for contact
    dp = Path.home() / f"projects/jt-consulting-pipeline/clients/{slug}/outreach-draft.md"
    extra = ""
    if dp.exists():
        c = dp.read_text()
        for pat, lbl in [(r'\*\*Name:\*\* (.+)',"Contact"),(r'\*\*LinkedIn:\*\* (.+)','LinkedIn'),(r'\*\*Email:\*\* (.+)','Email')]:
            r2 = re.search(pat, c)
            if r2: extra += f"{lbl}: {r2.group(1).strip()}\n"
    task = {"title": title, "description": f"{desc}\n\nSource refs:\n{extra}".strip(), "status": "todo", "priority": "high", "assignee": "jt", "project": "Consulting", "sortOrder": 20, "slug": slug, "pipelineStage": next_m}
    try:
        for t in fetch_tasks():
            if t.get("title") == title and t.get("status") in {"todo", "in_progress", "pending", "blocked"}:
                print(f"↩️  Follow-up task already exists: {title}")
                return
        d = json.dumps(task).encode()
        r = urllib.request.Request(MC_API, data=d, method="POST", headers={"Content-Type":"application/json"})
        resp = json.loads(urllib.request.urlopen(r).read())
        print(f"✅ Follow-up task created: {title}")
    except Exception as e:
        print(f"WARNING: follow-up task failed: {e}")

class StoreReceiptOnce(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            raise argparse.ArgumentError(self, "may only be provided once")
        setattr(namespace, self.dest, values)


def build_parser():
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument("--slug", required=True); p.add_argument("--company", required=True)
    p.add_argument("--message", required=True); p.add_argument("--channel", required=True); p.add_argument("--date", required=True)
    p.add_argument("--cohort-two-pre-send-receipt-id", action=StoreReceiptOnce)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    if a.cohort_two_pre_send_receipt_id is not None:
        try:
            record_cohort_two_confirmed_send(a.cohort_two_pre_send_receipt_id)
        except ConfirmedSendError:
            print("ERROR: cohort-two confirmed-send failed", file=sys.stderr)
            return 1
    print(f"\n📤 Update: {a.company} — {a.message} via {a.channel} on {a.date}")
    print("="*60)
    try:
        pp, c = load_outreach_draft(a.slug)
        update_outreach_draft(pp, c, a.message, a.channel, a.date)
        print(f"✅ outreach-draft.md updated")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1
    update_pipeline_md(a.slug, a.message, a.channel)
    close_mc_task(a.slug, a.company)
    create_followup_task(a.slug, a.company, a.message)
    print("\n✅ Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
