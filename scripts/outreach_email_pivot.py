#!/usr/bin/env python3
"""
outreach_email_pivot.py — Find M2-stuck prospects, draft email pivots, upload to Drive, create MC tasks.

Trigger: M2 sent 7+ days ago, no acceptance, no M3 sent → email pivot needed.
Usage:
  python3 scripts/outreach_email_pivot.py                    # scan + report only (dry run)
  python3 scripts/outreach_email_pivot.py --draft             # scan + generate email drafts
  python3 scripts/outreach_email_pivot.py --execute           # draft + Drive upload + MC tasks
  python3 scripts/outreach_email_pivot.py --prospect [slug]   # single prospect, execute mode
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

CLIENTS_DIR = Path.home() / "projects/jt-consulting-pipeline" / "clients"
PIPELINE_PATH = Path.home() / "projects/jt-consulting-pipeline" / "pipeline.md"
DRIVE_SCRIPT = Path.home() / ".openclaw/workspace/scripts/drive_drafts.py"
DRIVE_TOKEN_PATH = Path.home() / ".openclaw/workspace/config/google-oauth-token.json"
MC_API = "http://localhost:3000/api/tasks"

# Threshold: M2 sent N+ days ago = email pivot ready
EMAIL_PIVOT_THRESHOLD_DAYS = 7


def get_m1_hook(slug: str) -> str:
    """Extract the M1 hook from outreach-draft.md so we can use a different angle."""
    draft_path = CLIENTS_DIR / slug / "outreach-draft.md"
    if not draft_path.exists():
        return ""
    content = draft_path.read_text()
    # Look for "Why This Hook" or "Hook:" section
    hook_match = re.search(r'(?:## Why This Hook|Hook:)[^\n]*\n([^\n#]+)', content, re.IGNORECASE)
    if hook_match:
        return hook_match.group(1).strip()
    # Fall back to the email body first line
    email_match = re.search(r'Hi\s+\w+,([^A-Za-z\n]{5,80})', content)
    if email_match:
        return email_match.group(1).strip()
    return ""


def get_email_address(slug: str) -> str:
    """Find email address from outreach-draft, research, or shortlist."""
    # Try outreach-draft.md first
    draft_path = CLIENTS_DIR / slug / "outreach-draft.md"
    if draft_path.exists():
        content = draft_path.read_text()
        email_match = re.search(r'\*\*Email:\*\* (.+?)(?:\n|$)', content)
        if email_match:
            return email_match.group(1).strip()
    # Try research.md
    research_path = CLIENTS_DIR / slug / "research.md"
    if research_path.exists():
        content = research_path.read_text()
        email_match = re.search(r'[\w.+-]+@[\w.-]+', content)
        if email_match:
            return email_match.group(0)
    return ""


def get_contact_name(slug: str) -> str:
    """Get contact name from outreach-draft."""
    draft_path = CLIENTS_DIR / slug / "outreach-draft.md"
    if not draft_path.exists():
        return ""
    content = draft_path.read_text()
    # Try **Name:** format first
    m = re.search(r'\*\*Name:\*\* (.+)', content)
    if m:
        return m.group(1).strip()
    # Fall back to *Target: Name, Title* format
    m = re.search(r'\*Target:\s*([^,]+),', content)
    if m:
        return m.group(1).strip()
    return ""


def get_contact_title(slug: str) -> str:
    """Get contact title from outreach-draft."""
    draft_path = CLIENTS_DIR / slug / "outreach-draft.md"
    if not draft_path.exists():
        return ""
    content = draft_path.read_text()
    # Try **Title:** format first
    m = re.search(r'\*\*Title:\*\* (.+)', content)
    if m:
        return m.group(1).strip()
    # Fall back to *Target: Name, Title* format
    m = re.search(r'\*Target:\s*[^,]+,\s*(.+?)(?:\*|$)', content)
    return m.group(1).strip() if m else ""


def parse_outreach_status(slug: str) -> dict:
    """Parse outreach-draft.md for M1/M2/M3 send dates.
    Handles multiple formats:
    - | M1 | SENT | 2026-03-14 | (markdown table rows)
    - **Status:** M1 SENT 2026-03-22. M2 SENT 2026-03-24. (bold block)
    - *Status: M2 SENT 2026-03-22.* (italic block)
    - Status: M1 SENT 2026-03-22. (no decorators)
    """
    draft_path = CLIENTS_DIR / slug / "outreach-draft.md"
    if not draft_path.exists():
        return {}

    content = draft_path.read_text()
    status = {}

    # Format 1: Markdown table rows: | M1 | SENT | 2026-03-14 |
    for line in content.split('\n')[:40]:
        for letter in ['M1', 'M2', 'M3']:
            pattern = rf'\|\s*{letter}\s*\|[^|]*\|\s*(\d{{4}}-\d{{2}}-\d{{2}})'
            m = re.search(pattern, line, re.IGNORECASE)
            if m and letter not in status:
                status[letter] = datetime.strptime(m.group(1), '%Y-%m-%d').date()

    # Format 2: **Status:** M1 SENT 2026-03-22. M2 SENT 2026-03-24.
    if not status:
        s_match = re.search(r'\*\*Status:\*\* (.+)', content)
        if s_match:
            s_text = s_match.group(1)
            for letter in ['M1', 'M2', 'M3']:
                m = re.search(rf'{letter}[^0-9]*?(\d{{4}}-\d{{2}}-\d{{2}})', s_text, re.IGNORECASE)
                if m and letter not in status:
                    status[letter] = datetime.strptime(m.group(1), '%Y-%m-%d').date()

    # Format 3: *Status: M2 SENT 2026-03-22.* (single-asterisk bold)
    if not status:
        s_match = re.search(r'\*Status: (.+?)(?<!\*)\*(?=\n|$)', content)
        if s_match:
            s_text = s_match.group(1)
            for letter in ['M1', 'M2', 'M3']:
                m = re.search(rf'{letter}[^0-9]*?(\d{{4}}-\d{{2}}-\d{{2}})', s_text, re.IGNORECASE)
                if m and letter not in status:
                    status[letter] = datetime.strptime(m.group(1), '%Y-%m-%d').date()

    # Format 4: inline in message text like "M2 SENT 2026-03-22"
    if not status:
        for letter in ['M1', 'M2', 'M3']:
            m = re.search(rf'{letter}[^0-9]*?SENT[^0-9]*?(\d{{4}}-\d{{2}}-\d{{2}})', content, re.IGNORECASE)
            if m and letter not in status:
                try:
                    status[letter] = datetime.strptime(m.group(1), '%Y-%m-%d').date()
                except:
                    pass

    return status


def get_canonical_name(slug: str) -> str:
    """Look up canonical Drive folder name from drive-canonical-names.md.
    Uses fuzzy matching (SequenceMatcher) to handle name variations.
    Returns the Drive folder name (canonical), not the shortlist name.
    """
    import difflib
    canonical_path = Path.home() / "projects/jt-consulting-pipeline" / "drive-canonical-names.md"
    if not canonical_path.exists():
        return slug.replace('-', ' ').title()
    content = canonical_path.read_text()
    slug_normalized = slug.lower().replace('-', ' ')
    best_match = None
    best_ratio = 0
    for line in content.split('\n'):
        if not line.strip().startswith('|') or line.strip().startswith('|--'):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 3:
            shortlist = parts[1]
            # Try matching slug against shortlist name
            ratio1 = difflib.SequenceMatcher(None, slug_normalized, shortlist.lower().replace('-', ' ')).ratio()
            # Also try matching individual slug words against shortlist
            slug_words = set(slug_normalized.split())
            shortlist_words = set(shortlist.lower().replace('-', ' ').split())
            word_overlap = len(slug_words & shortlist_words) / max(len(slug_words), 1) if slug_words else 0
            combined = max(ratio1, word_overlap)
            if combined > best_ratio:
                best_ratio = combined
                best_match = parts[2].strip()
    if best_ratio >= 0.3:
        return best_match
    return slug.replace('-', ' ').title()


def scan_prospects() -> list:
    """Find all prospects where M2 was sent but M3 hasn't been sent."""
    prospects = []
    today = datetime.now().date()

    for slug_dir in CLIENTS_DIR.iterdir():
        if not slug_dir.is_dir():
            continue
        slug = slug_dir.name

        status = parse_outreach_status(slug)
        if 'M2' not in status or 'M3' in status:
            continue  # M2 not sent yet, or M3 already sent (no pivot needed)

        m2_date = status['M2']
        days_since_m2 = (today - m2_date).days
        m1_date = status.get('M1')

        email = get_email_address(slug)
        contact = get_contact_name(slug)
        title = get_contact_title(slug)
        hook = get_m1_hook(slug)
        canonical = get_canonical_name(slug)

        prospects.append({
            'slug': slug,
            'canonical': canonical,
            'contact': contact,
            'title': title,
            'email': email,
            'm1_date': m1_date,
            'm2_date': m2_date,
            'days_since_m2': days_since_m2,
            'm1_hook': hook,
            'pivot_ready': days_since_m2 >= EMAIL_PIVOT_THRESHOLD_DAYS,
        })

    # Sort by days since M2 (oldest first)
    prospects.sort(key=lambda x: x['days_since_m2'], reverse=True)
    return prospects


def draft_email(prospect: dict) -> str:
    """
    Generate email pivot draft using rules-based angle generation.
    The email must be DIFFERENT from the LinkedIn M1 hook.
    Returns the full email-draft.md content.
    """
    slug = prospect['slug']
    canonical = prospect['canonical']
    contact = prospect['contact']
    title = prospect['title']
    email_addr = prospect['email']
    m2_date = prospect['m2_date']
    m1_hook = prospect['m1_hook']

    # Load research.md for company context
    research_path = CLIENTS_DIR / slug / "research.md"
    research_content = ""
    if research_path.exists():
        research_content = research_path.read_text()

    # Load outreach-draft.md for original email
    draft_path = CLIENTS_DIR / slug / "outreach-draft.md"
    draft_content = ""
    if draft_path.exists():
        draft_content = draft_path.read_text()

    # Extract original email body to avoid duplicating the hook
    original_email = ""
    if "Cold Email" in draft_content or "Initial" in draft_content:
        # Find the email section
        start = draft_content.find("## Cold Email")
        if start == -1:
            start = draft_content.find("Cold Email")
        if start != -1:
            section = draft_content[start:start+2000]
            # Extract first ~200 chars after "Hi [Name],"
            m = re.search(r'Hi\s+\w+,[^\n]*\n([^\n#]{10,150})', section)
            if m:
                original_email = m.group(1).strip()

    # Determine niche from research.md or draft
    niche = "construction/specialty trades"
    if 'construction' in research_content.lower() or 'plumbing' in research_content.lower():
        niche = "construction/trades"
    if 'wholesale' in research_content.lower() or 'distribution' in research_content.lower():
        niche = "wholesale distribution"
    if 'property' in research_content.lower() or 'management' in research_content.lower():
        niche = "property management"

    # Load brief.json for service/pricing context
    brief_path = CLIENTS_DIR / slug / "brief.json"
    service_line = "n8n workflow automation"
    proof_point = "Built a workflow automation for a NYC construction company — a live dashboard pulling StreetEasy listings on a schedule, with automated alerts when criteria match."
    if brief_path.exists():
        try:
            brief = json.loads(brief_path.read_text())
            platform = brief.get('platform', 'n8n')
            if platform == 'agentforce':
                service_line = "Agentforce implementation (Salesforce)"
                proof_point = "Built and deployed InsuranceServiceAgent — a live Agentforce agent running inside Salesforce."
            elif platform == 'both':
                service_line = "n8n + Agentforce"
        except:
            pass

    # ANGLE RULES: Pick different angle from M1 hook
    # Common M1 hooks → email pivots (sentence fragments that become email body P2)
    angle_map = {
        'dispatch': ("the gap between dispatch and actual service is where your team's hours disappear", "dispatch windows"),
        'inventory': ("the order confirmation loop — where someone calls back to verify availability — is the hidden time sink", "order confirmations"),
        'job': ("field-to-office handoffs are where jobs slow down", "field reporting"),
        'quote': ("quotes that don't close themselves need manual follow-up every time", "quote follow-through"),
        'schedule': ("cross-trade scheduling is where the gaps show up first", "crew coordination"),
        'crew': ("multi-crew coordination breaks down at the handoff points", "job-site handoffs"),
        'service': ("SLA windows and 7-day coverage means the gaps compound fast", "response time"),
        'order': ("availability check loops — the callback to confirm stock — add up fast at your volume", "availability checks"),
        'report': ("manual reporting eats the time your team needs for actual work", "weekly reports"),
    }

    # Find which angle was used in M1
    used_angle_key = None
    combined = (m1_hook + original_email).lower()
    for key in angle_map:
        if key in combined:
            used_angle_key = key
            break

    # Pick a different angle's sentence fragment
    email_angle_sentence = "the gaps that slip through when processes aren't connected"
    subject = "workflow setup"
    for key, (sentence, subj) in angle_map.items():
        if key != used_angle_key:
            email_angle_sentence = sentence
            subject = subj
            break

    # First name extraction
    first_name = contact.split()[0] if contact else "there"

    # Company nickname
    company_short = canonical.split()[0] if canonical else "your"

    # First name
    first_name = contact.split()[0] if contact else "there"

    # Build email body — P1: observation about their world, P2: specific angle (different from M1)
    p1 = original_email.strip() if original_email.strip() else (
        f"At {canonical.split()[0]}, the gaps that compound over weeks are the ones that cost the most to fix"
    )

    body = f"""{first_name},

{p1}. {email_angle_sentence.capitalize()}.

{proof_point}

Worth a quick conversation?

JT Somwaru
AI Implementation Consultant | NYC
jtsomwaru.com"""

    # Format email as email-draft.md
    email_verified = "(unverified)" if email_addr and "unverified" not in email_addr.lower() else "(unverified — please confirm)"
    email_display = f"{email_addr} {email_verified}" if email_addr else "(email not yet found — needs research)"

    draft = f"""# {canonical} — Email Draft
*Target: {contact}, {title}*
*Email: {email_display}*
*Channel: Cold Email (pivot from LinkedIn — connection request sent {m2_date.strftime('%Y-%m-%d')}, not accepted as of {datetime.now().strftime('%Y-%m-%d')})*
*Drafted: {datetime.now().strftime('%Y-%m-%d')} | Script-generated pivot | Angle: {subject}*

---

## Subject
{subject}

## Body

{body}

---

## Personalization Notes
- M1 hook (LinkedIn): see outreach-draft.md
- Email angle (DIFFERENT from M1): {subject} — "{email_angle_sentence}"
- M2 sent: {m2_date.strftime('%Y-%m-%d')} ({prospect['days_since_m2']} days ago)
- Service: {service_line}

## Pre-Output Checklist
- [ ] Subject: 2-4 words, lowercase, internal-looking
- [ ] P1: specific observation about their company/niche (not generic)
- [ ] P2: different angle from LinkedIn M1
- [ ] Signature block: name, title, city, website
- [ ] Body ~75-100 words
- [ ] No reference to LinkedIn or previous message
- [ ] Email address verified before sending
"""

    return draft


def normalize_task_key(value: str) -> str:
    """Normalize MC titles enough to catch FCM/First Class style variants."""
    value = value.lower()
    value = value.replace("fcm real estate", "first class management")
    value = value.replace("fcmre", "first class management")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def check_mc_task_exists(prospect: dict) -> bool:
    """Check if an active Email Pivot MC task already exists for this prospect.

    Important: Mission Control previously accumulated duplicate Email Pivot tasks
    because the nightly cron matched only the exact generated title and ignored
    title variants. Match canonical/company/contact tokens across all non-closed
    statuses before creating anything new.
    """
    try:
        tasks = json.loads(urllib.request.urlopen(MC_API).read())["tasks"]
        title = f"Email Pivot: {prospect['canonical']} — {prospect['contact'].split()[0]}"
        canonical_key = normalize_task_key(prospect["canonical"])
        contact_first = normalize_task_key(prospect["contact"].split()[0]) if prospect.get("contact") else ""
        active_statuses = {"todo", "in-progress", "in_progress", "pending", "blocked"}
        for t in tasks:
            if t.get("status", "todo") not in active_statuses:
                continue
            task_title = t.get("title", "")
            if normalize_task_key(task_title) == normalize_task_key(title):
                return True
            task_key = normalize_task_key(task_title)
            if task_title.lower().startswith("email pivot:") and canonical_key and canonical_key in task_key:
                if not contact_first or contact_first in task_key:
                    return True
    except Exception:
        pass
    return False




def ensure_drive_auth_recovery_task() -> str:
    """Create or reference one active MC task for missing Google Drive OAuth."""
    title = "Recover Google Drive OAuth for outreach email pivots"
    active_statuses = {"todo", "in-progress", "in_progress", "pending", "blocked"}
    try:
        tasks = json.loads(urllib.request.urlopen(MC_API).read()).get("tasks", [])
        for t in tasks:
            if t.get("status", "todo") in active_statuses and normalize_task_key(t.get("title", "")) == normalize_task_key(title):
                return f"↩️  Drive OAuth recovery task already exists: {title}"

        task = {
            "title": title,
            "description": (
                f"Google Drive OAuth token is missing at `{DRIVE_TOKEN_PATH}`. "
                "Run `python3 ~/.openclaw/workspace/scripts/drive_auth.py`, then rerun the outreach email pivot job. "
                "The pivot job stopped before generating drafts or Mission Control outreach tasks to avoid duplicates."
            ),
            "status": "todo",
            "priority": "medium",
            "assignee": "jt",
            "project": "Consulting",
            "sortOrder": 35,
            "slug": "drive-oauth-outreach-pivot",
            "pipelineStage": "auth-recovery",
        }
        data = json.dumps(task).encode()
        req = urllib.request.Request(MC_API, data=data, method="POST",
                                   headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req).read()
        return f"✅ Drive OAuth recovery task created: {title}"
    except Exception as e:
        return f"⚠️  Drive OAuth missing; could not create/reuse MC recovery task: {e}"

def upload_to_drive(slug: str, canonical: str, email_content: str) -> str:
    """Upload email draft to Drive. Returns the Drive URL."""
    # Write draft to client folder first
    draft_path = CLIENTS_DIR / slug / "email-draft.md"
    draft_path.write_text(email_content)

    # Run drive_drafts.py
    cmd = [
        sys.executable, str(DRIVE_SCRIPT),
        "--title", f"{canonical} — Email Draft",
        "--path", f"Consulting/Clients/{canonical}/Outreach/Email",
        "--file", str(draft_path),
    ]
    try:
        result = os.spawnvp(os.P_WAIT, sys.executable, cmd)
        if result == 0:
            return f"✅ Uploaded to Drive: Consulting/Clients/{canonical}/Outreach/Email"
        else:
            return f"⚠️  Drive upload failed (exit {result})"
    except Exception as e:
        return f"⚠️  Drive upload error: {e}"


def create_mc_task(prospect: dict, drive_note: str) -> str:
    """Create Email Pivot task in Mission Control."""
    title = f"Email Pivot: {prospect['canonical']} — {prospect['contact'].split()[0]}"
    days = prospect['days_since_m2']
    urgency = "🔴 OVERDUE" if days > 14 else "🟠 Due"
    desc = f"""{urgency} — M2 sent {prospect['m2_date'].strftime('%Y-%m-%d')} ({days} days ago), no acceptance.

First action: review + edit email draft at `{CLIENTS_DIR / prospect['slug'] / 'email-draft.md'}` and verify the email address before sending.

Why it matters: this is a stale cold-outreach recovery lane; it should not outrank warm referrals, paid client acceptance, or proof-led distribution unless JT explicitly selects this prospect/channel again.

Done looks like: email is sent via email (not LinkedIn), JT replies "sent email pivot to [Company]", and the pipeline/outreach status is updated.

{drive_note}"""

    task = {
        "title": title,
        "description": desc,
        "status": "todo",
        "priority": "low",
        "assignee": "jt",
        "project": "Consulting",
        "sortOrder": 40,
        "slug": prospect["slug"],
        "pipelineStage": "email-pivot",
    }

    try:
        data = json.dumps(task).encode()
        req = urllib.request.Request(MC_API, data=data, method="POST",
                                   headers={"Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req).read())
        return f"✅ MC task created: {title}"
    except Exception as e:
        return f"⚠️  MC task creation failed: {e}"


def main():
    parser = argparse.ArgumentParser(description="Outreach Email Pivot Automation")
    parser.add_argument("--draft", action="store_true", help="Generate email drafts (no Drive/MC)")
    parser.add_argument("--execute", action="store_true", help="Draft + Drive upload + MC task creation")
    parser.add_argument("--prospect", help="Run on a specific prospect slug only")
    parser.add_argument("--min-days", type=int, default=EMAIL_PIVOT_THRESHOLD_DAYS,
                       help=f"Min days since M2 before pivot (default: {EMAIL_PIVOT_THRESHOLD_DAYS})")
    args = parser.parse_args()

    if not args.draft and not args.execute:
        # Default: scan only, report
        mode = "scan"
    elif args.draft:
        mode = "draft"
    else:
        mode = "execute"

    print(f"\n📧 Outreach Email Pivot Scan")
    print(f"   Mode: {mode.upper()}")
    print(f"   Threshold: {args.min_days}+ days since M2 with no acceptance")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 70)

    prospects = scan_prospects()
    pivot_ready = [p for p in prospects if p['days_since_m2'] >= args.min_days]

    if not prospects:
        print("No prospects with M2 sent found.")
        return

    print(f"\nScanned {len(prospects)} prospects with M2 sent\n")

    # Show all M2-stuck prospects
    print(f"{'Days':>5} | {'Company':<35} | {'M2 Date':<12} | {'Email':<30} | Status")
    print("-" * 100)
    for p in prospects:
        email_short = (p['email'][:28] + "..") if p['email'] else "(no email)"
        ready = "✅ READY" if p['pivot_ready'] else f"⏳ {7-p['days_since_m2']}d left"
        print(f"{p['days_since_m2']:>5} | {p['canonical'][:34]:<35} | {str(p['m2_date']):<12} | {email_short:<30} | {ready}")

    print(f"\n{len(pivot_ready)} prospects past {args.min_days}-day threshold\n")

    if not pivot_ready:
        print("No email pivots needed yet.")
        return

    if mode == "execute" and not DRIVE_TOKEN_PATH.exists():
        print(f"Drive OAuth token missing at {DRIVE_TOKEN_PATH}; stopping before draft/task generation.")
        print(ensure_drive_auth_recovery_task())
        return

    # Process each pivot-ready prospect
    results = []
    for p in pivot_ready:
        slug = p['slug']

        if args.prospect and slug != args.prospect:
            continue

        print(f"\n{'─'*60}")
        print(f"📧 {p['canonical']} — M2 sent {p['days_since_m2']} days ago")
        print(f"   Contact: {p['contact']} | Email: {p['email'] or 'TBD'}")

        # Check if email already exists
        existing = (CLIENTS_DIR / slug / "email-draft.md").exists()
        task_exists = check_mc_task_exists(p)

        if existing and task_exists:
            print(f"   ⚠️  email-draft.md and active Email Pivot MC task already exist — skipping")
            continue

        if existing and not task_exists:
            print(f"   ⚠️  email-draft.md already exists but no active MC task was found — skipping task creation to avoid duplicate/manual-review drift")
            continue

        if existing:
            if mode == "execute":
                print(f"   ⚠️  email-draft.md already exists and no active MC task was found — preserving draft, creating task only")
            elif mode == "draft":
                print(f"   ⚠️  email-draft.md already exists — skipping (use --execute only if MC task is missing)")
                continue

        if mode == "scan":
            print(f"   → Would generate email + Drive + MC task")
            continue

        # Generate draft only when it does not already exist. Existing drafts are preserved to avoid
        # silently changing JT-reviewed copy during task repair/backfill runs.
        draft_path = CLIENTS_DIR / slug / "email-draft.md"
        if existing:
            email_draft = draft_path.read_text()
            print(f"   ↩️  existing email-draft.md reused ({len(email_draft)} chars)")
        else:
            print(f"   ✍️  Generating email pivot...")
            email_draft = draft_email(p)
            draft_path.write_text(email_draft)
            print(f"   ✅ email-draft.md written ({len(email_draft)} chars)")

        if mode == "execute":
            # Upload to Drive
            drive_result = upload_to_drive(slug, p['canonical'], email_draft)
            print(f"   {drive_result}")

            # Create MC task
            mc_result = create_mc_task(p, drive_result)
            print(f"   {mc_result}")

            results.append({
                'slug': slug,
                'company': p['canonical'],
                'contact': p['contact'],
                'email': p['email'],
                'days': p['days_since_m2'],
                'draft_path': str(draft_path),
            })

    if results:
        print(f"\n{'='*70}")
        print(f"✅ {len(results)} email pivots created:")
        for r in results:
            print(f"   • {r['company']} — {r['contact']} ({r['days']}d since M2)")
            print(f"     Draft: {r['draft_path']}")
    else:
        print("\n✅ No new pivots needed.")


if __name__ == "__main__":
    main()
