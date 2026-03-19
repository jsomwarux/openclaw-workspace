---
name: job-application
description: Creates tailored job application packages for JT Somwaru — resume, cover letter, and Google Drive upload. Use when JT says "apply to", "create a resume for", "write a cover letter for", "tailor my resume", "job application", "apply for this role", or pastes a job listing. NOT for: general career advice, job searching, salary negotiation, or interview prep (no skill covers those — handle directly).
---

# SKILL: Job Application Package
*Done 3+ times (Squarespace SA, Writer SA, Salesforce SE) — follow this exactly every time.*

---

## Step 0: Load JT's profile
Read these files before writing a single word:
- `~/.openclaw/workspace/USER.md` — JT's background, education, communication style
- `~/.openclaw/workspace/MEMORY.md` → Job Market section — current pipeline, skill gaps, salary floor
- `~/.openclaw/workspace/skills/job-application/application-intelligence.md` — **MANDATORY** — full resume/cover letter strategy, ATS rules, bullet frameworks, keyword banks, quantification tactics, anti-patterns. Supersedes any general guidance you have. Read this fully before writing.

JT's non-negotiables (never compromise):
- NOT a developer — never position as Apex coder, ML engineer, or software dev
- Salary floor: $150K minimum in application materials (target $180–220K)
- NYC metro or remote only

---

## Step 1: Analyze the role (score it first)
Use the scoring rubric from `~/projects/job-market-agent/knowledge/scoring-criteria.md`.

Score it before writing. If <15/25: flag to JT before proceeding — ask if he still wants docs.
If 15+: note the specific match points to emphasize.

Extract from the JD:
- Required skills (must hit all of these in the resume)
- Preferred skills (hit as many as honestly possible)
- Key phrases/language (mirror these in the cover letter — don't invent different words for the same thing)
- Hiring manager's pain (what problem are they trying to solve?) — the cover letter opens with this

---

## Step 2: Tailor the resume
Base: JT's experience is fixed. What changes is emphasis and framing.

**JT's strongest angles for AI roles:**
- 6 years as BSA at Spectrum Enterprise — product catalog config, cross-team coordination, system implementations. This is implementation expertise, not just consulting.
- Gap bridge: speaks both business operations AND technology — frame this explicitly, it's rare for AI roles
- JT Somwaru Consulting: AI automation consulting, n8n workflows, Agentforce implementations, real client deliverables (Aya — $1,500 dashboard, $1,000 StreetEasy scraper)
- Built: Vista (App Store), Nash Satoshi, Glow Index — proof of shipping, not just planning
- ConversationFirst framework — Agentforce UX methodology (differentiator for Salesforce roles)
- OpenClaw AI infrastructure — running 20+ autonomous agents, cron system, health tracking, cost optimization

**Resume format rules:**
- One page preferred, two max
- Lead with a 2-3 sentence summary that names the specific role and the specific value
- Bullets start with strong verbs: Built, Automated, Reduced, Delivered, Designed, Managed
- Quantify everything possible: dollar amounts, time saved, completion rates
- No: "responsible for," "helped with," "assisted in," "various," "etc."
- **Never use em dashes (—) anywhere in the resume or cover letter.** Em dashes are a clear AI writing tell. Use commas, colons, periods, or parentheses instead.

Save to: `~/.openclaw/workspace/memory/drafts/[company-slug]-resume.md`

---

## Step 3: Write the cover letter
Structure (4 paragraphs, under 350 words total):

**P1 — Open with their problem, not your credentials**
One sentence that shows you read the JD and understand what they're trying to solve. "You're looking for someone who can [X]" not "I'm excited to apply for."

**P2 — The bridge (most important paragraph)**
Connect JT's BSA background to this specific role. The BSA-to-AI-implementation path is the differentiating story. One concrete deliverable minimum (named, with outcome).

**P3 — What you'll do there**
One paragraph, specific to their context. Shows you thought about the role, not just the application.

**P4 — Close clean**
No "I look forward to hearing from you." Say something like: "Happy to walk through [specific project] on a call." Short, direct, confident.

Save to: `~/.openclaw/workspace/memory/drafts/[company-slug]-cover-letter.md`

---

## Step 4: Generate .docx and upload to Drive (mandatory)

**NEVER write resume/cover letter as markdown.** Always generate proper .docx using build_resume_docx.py.

1. Update `scripts/build_resume_docx.py` with tailored content for the role
2. Generate: `python3 ~/.openclaw/workspace/scripts/build_resume_docx.py --type both --output-dir /tmp`
3. Upload using the Drive API directly (binary → convert to Google Doc on upload):

```python
import json, os, warnings; warnings.filterwarnings("ignore")
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
TOKEN_PATH = os.path.expanduser("~/.openclaw/workspace/config/google-oauth-token.json")
with open(TOKEN_PATH) as f: td = json.load(f)
creds = Credentials(token=td["token"], refresh_token=td["refresh_token"],
    token_uri=td["token_uri"], client_id=td["client_id"],
    client_secret=td["client_secret"], scopes=td["scopes"])
if creds.expired: creds.refresh(Request())
drive = build("drive", "v3", credentials=creds, cache_discovery=False)
def find_folder(name, pid=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if pid: q += f" and '{pid}' in parents"
    r = drive.files().list(q=q, fields="files(id)").execute()
    return r["files"][0]["id"] if r["files"] else None
root = find_folder("Eve — Drafts"); ja = find_folder("Job Applications", root)
for path, folder, title in [
    ("/tmp/jt-somwaru-resume.docx", find_folder("Resumes", ja), "JT Somwaru — [COMPANY] — Resume"),
    ("/tmp/jt-somwaru-cover-letter.docx", find_folder("Cover Letters", ja), "JT Somwaru — [COMPANY] — Cover Letter"),
]:
    meta = {"name": title, "parents": [folder], "mimeType": "application/vnd.google-apps.document"}
    media = MediaFileUpload(path, mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    r = drive.files().create(body=meta, media_body=media, fields="id").execute()
    print(f"{title}: https://docs.google.com/document/d/{r['id']}/edit")
```

Design is embedded natively — Google Docs renders correctly, exports to ATS-readable PDF.
- Name: 22pt bold navy | Section headings: 12pt bold navy ALL CAPS + rule
- Job title: 11pt bold black; Company/dates: 10.5pt gray right-aligned  
- Bullets: 10.5pt black, 0.25" indent, real bullet character (•)
- Builds: inline text only — **NO TABLES** (ATS drops all table content) | Margins: 0.75"
**To submit:** File → Download → PDF in Google Docs.

Both must be uploaded. Local-only is not acceptable.

---

## Step 5: Deliver to JT
Reply with:
- Score (X/25) + 2-3 sentence rationale
- Drive links for both docs
- One honest flag: "The gap to watch: [specific skill they want that JT doesn't fully have]"
- Recommended action: apply now / tweak first / skip

---

## Tracking
After delivering: check Mission Control for an existing task for this role. If none exists, push one:
```
curl -s -X POST http://localhost:3000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Apply: [Role] — [Company] (score: X/25)","description":"Resume: [Drive link]\nCover letter: [Drive link]\n\nGap: [noted gap]\nDeadline: [if known]","status":"todo","priority":"high","assignee":"JT","project":"Job Market","sortOrder":15}'
```
