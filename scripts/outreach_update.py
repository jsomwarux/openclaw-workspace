#!/usr/bin/env python3
"""outreach_update.py — Update prospect outreach status after JT confirms a send."""
import argparse, json, re, sys, urllib.request
from pathlib import Path

PIPELINE_PATH = Path.home() / "projects/jt-consulting-pipeline" / "pipeline.md"
MC_API = "http://localhost:3000/api/tasks"

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

def close_mc_task(slug, company):
    try:
        tasks = json.loads(urllib.request.urlopen(MC_API).read())["tasks"]
    except Exception as e:
        print(f"WARNING: MC fetch failed: {e}"); return
    for t in tasks:
        if "Review + Send" in t.get("title","") and company.split()[0] in t.get("title",""):
            try:
                d = json.dumps({"status": "done"}).encode()
                r = urllib.request.Request(f"{MC_API}/{t['_id']}", data=d, method="PATCH", headers={"Content-Type":"application/json"})
                urllib.request.urlopen(r)
                print(f"✅ MC task closed: {t['title']}")
                return
            except Exception as e:
                print(f"WARNING: could not close task: {e}")

def create_followup_task(slug, company, message):
    mn = message.upper()
    if mn == "M1": next_m, title, desc = "M2", f"M2: {company} — Follow-up", f"M1 sent. M2 due 3-4 days after M1.\nCheck connection acceptance first."
    elif mn == "M2": next_m, title, desc = "M3", f"M3: {company} — Final follow-up", f"M2 sent, no reply. M3 due 5-7 days after M2."
    else: return
    # Read draft for contact
    dp = Path.home() / f"projects/jt-consulting-pipeline/clients/{slug}/outreach-draft.md"
    extra = ""
    if dp.exists():
        c = dp.read_text()
        for pat, lbl in [(r'\*\*Name:\*\* (.+)',"Contact"),(r'\*\*LinkedIn:\*\* (.+)','LinkedIn'),(r'\*\*Email:\*\* (.+)','Email')]:
            r2 = re.search(pat, c)
            if r2: extra += f"{lbl}: {r2.group(1).strip()}\n"
    task = {"title": title, "description": f"{desc}\n\n{extra}", "status": "todo", "priority": "high", "assignee": "jt", "project": "Consulting", "sortOrder": 45}
    try:
        d = json.dumps(task).encode()
        r = urllib.request.Request(MC_API, data=d, method="POST", headers={"Content-Type":"application/json"})
        resp = json.loads(urllib.request.urlopen(r).read())
        print(f"✅ Follow-up task created: {title}")
    except Exception as e:
        print(f"WARNING: follow-up task failed: {e}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True); p.add_argument("--company", required=True)
    p.add_argument("--message", required=True); p.add_argument("--channel", required=True); p.add_argument("--date", required=True)
    a = p.parse_args()
    print(f"\n📤 Update: {a.company} — {a.message} via {a.channel} on {a.date}")
    print("="*60)
    try:
        pp, c = load_outreach_draft(a.slug)
        update_outreach_draft(pp, c, a.message, a.channel, a.date)
        print(f"✅ outreach-draft.md updated")
    except FileNotFoundError as e:
        print(f"❌ {e}"); sys.exit(1)
    update_pipeline_md(a.slug, a.message, a.channel)
    close_mc_task(a.slug, a.company)
    create_followup_task(a.slug, a.company, a.message)
    print("\n✅ Done.")
