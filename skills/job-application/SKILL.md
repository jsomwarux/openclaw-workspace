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
- Independent consulting work: AI automation consulting, n8n workflows, Agentforce implementations, and anonymized client deliverables such as operational dashboards, data pipelines, approval queues, and governed AI workflows
- Built: Vista (App Store), Nash Satoshi, Glow Index — proof of shipping, not just planning
- ConversationFirst framework — Agentforce UX methodology (differentiator for Salesforce roles)
- OpenClaw AI infrastructure — running 44 autonomous agents, cron system, health tracking, cost optimization

**5 mandatory quality rules (apply to every resume — no exceptions):**

**Rule 1 — Consulting bullets: outcomes, not activity.**
Every bullet under independent consulting work must follow: [specific thing built/done] → [specific result/outcome]. Never describe what JT 'does' generically. Use anonymized client descriptors only.
Bad: 'Develop and execute AI transformation roadmaps... identifying use cases, evaluating vendors...'
Good: 'Mapped and automated 3 client workflows (construction, PM, insurance) — eliminated daily manual coordination loops; 2 follow-on projects from the same anchor client.'

**Rule 2 — Spectrum bullets need numbers.**
At least 2-3 Spectrum bullets must include a real metric: teams coordinated, processes affected, timeline compressed, error rate, dollar scope. '$1B+ portfolio' is a scope descriptor, not an outcome. Add at least: (1) team count or stakeholder scope, (2) a process/delivery outcome. Rough estimates with ranges are fine.

**Rule 3 — Title is role-adaptive.**
The resume header title is not fixed. Match it to the role type:
- Transformation/change management/AI adoption roles: 'AI Transformation Consultant'
- Implementation/operations/embedded roles: 'AI Implementation Specialist'
- Strategy/roadmap/enablement roles: 'AI Strategy & Implementation Consultant'
Never use 'AI Automation Consultant' on a resume — it signals pipeline builder, not program leader.

**Rule 4 — Nash Satoshi elevated framing.**
Nash Satoshi must be described as multi-model orchestration, not a crypto app. Required framing:
'Built production 4-LLM ensemble (Claude, GPT-4, Gemini, Grok) that generates consensus rankings via cross-model validation — demonstrating agent orchestration, model bias mitigation, and AI ops at scale.'
This is the single strongest technical proof point for multi-model/AI ops roles. Never bury it in one line.

**Rule 5 — AgentGuard leads Key Projects.**
AgentGuard (confidence-gated routing, human-in-the-loop, audit trail, explainability) speaks directly to enterprise AI governance — the #1 concern at companies over 500 employees. It must be listed FIRST in Key Projects with 3 bullets minimum. It outranks Vista and Nash Satoshi for any enterprise role.

**Rule 6 — Zero em dashes in resume AND cover letter.**
Em dashes are a clear AI writing tell. Apply to both documents without exception. Replace with commas, colons, periods, or semicolons depending on context.

**Resume format rules:**
- One page preferred, two max
- Lead with a 2-3 sentence summary that names the specific role and the specific value
- Bullets start with strong verbs: Built, Automated, Reduced, Delivered, Designed, Managed
- Quantify everything possible: dollar amounts, time saved, completion rates
- No: "responsible for," "helped with," "assisted in," "various," "etc."
- No evaluator/verdict language inside the resume: never write "Strong fit," "good fit," "great fit," "ideal candidate," "perfect fit," or "fit for [company/role]." That belongs in internal scoring notes or JT-facing recommendation, not applicant-facing materials.
- No specific consulting client names in the resume or cover letter. Use anonymized descriptors such as "a NYC construction client," "a property management client," "a Bronx HVAC distributor," or "an operations-heavy client." This applies even when the client name is useful proof.
- **Never use em dashes (—) anywhere in the resume or cover letter.** Em dashes are a clear AI writing tell. Use commas, colons, periods, or parentheses instead.

Save to: `~/.openclaw/workspace/memory/drafts/[company-slug]-resume.md`

---

## Step 3: Write the cover letter

**Before writing a single word — run this JD mapping check:**
1. List every hard requirement from the JD (years of experience, specific platform/tool, domain, must-have skill)
2. For each: identify exactly which line of JT's experience addresses it
3. If a requirement is not explicitly addressed by at least one sentence in P2 or P3, the cover letter is incomplete

This check is mandatory. A cover letter that ignores a hard requirement fails the screen, even if the prose is clean.

Structure (4 paragraphs, under 350 words total — **each paragraph max 100 words**):

**P1 — Open with their problem, not your credentials**
One or two sentences that show you read the JD and understand what they're trying to solve. "You're looking for someone who can [X]" not "I'm excited to apply for."

**P2 — The bridge (most important paragraph — MAX 100 WORDS)**
Connect JT's BSA background to this specific role. Use the language from the JD requirement directly (if they say "CRM implementation," say "CRM implementation" not "system rollouts"). One concrete deliverable minimum (named, with outcome). If the JD has a years-of-experience requirement, name the relevant background explicitly in terms that match their phrasing.

**P3 — What you'll do there (MAX 100 WORDS)**
One paragraph, specific to their context. Shows you thought about the role, not just the application. Reference a named client project or deliverable.

**P4 — Close clean**
No "I look forward to hearing from you." Say something like: "Happy to walk through [specific project] on a call." Short, direct, confident. One or two sentences max.

**Before finalizing — run this cover letter audit:**
- [ ] Every hard JD requirement appears in P2 or P3 using the JD's own language
- [ ] P2 is under 100 words
- [ ] P3 is under 100 words
- [ ] No em dashes anywhere
- [ ] No "I am excited to apply" or "I look forward to hearing from you"
- [ ] At least one named project/deliverable with an outcome
- [ ] No mention of "JT Somwaru Consulting" as a business name — say "independent consulting work" or describe work directly
- [ ] No specific consulting client names anywhere — anonymize client proof before finalizing
- [ ] No specific dollar figures anywhere in the letter
- [ ] Closing does NOT sound like a consulting pitch — fits a job application context

**Cover letter markdown format (exact structure required — parser needs exactly two `---` separators):**
```
# Cover Letter — [Company], [Role Title]

---

Applying for: | [Company] [Role Title]

---

[P1 — opening paragraph]

[P2 — bridge paragraph]

[P3 — what you'll do there]

[P4 — close]

Jon Trevor Somwaru
jtsomwaru@gmail.com | jtsomwaru.com
```
The `Applying for:` line is how the parser extracts the company name. The body starts after the second `---`. Missing either separator = blank cover letter.

Save to: `~/.openclaw/workspace/memory/drafts/[company-slug]-cover-letter.md`

---

## Step 4: Generate .docx and upload to Drive (mandatory)

**NEVER write resume/cover letter as markdown.** Always generate proper .docx using build_resume_docx.py.

**MANDATORY parse verification before uploading** — NEVER use `exec(full_src)` on build_resume_docx.py (it triggers main() with no args and overwrites /tmp with fallback content). Use isolated function extraction only:

```python
# Resume verification — extract only the parse function, do not run main()
src = open('/Users/jtsomwaru/.openclaw/workspace/scripts/build_resume_docx.py').read()
local_ns = {}
exec(src.split('if __name__')[0], local_ns)
data = local_ns['parse_resume_md']('/path/to/[company-slug]-resume.md')
print("Name:", data['name'])
print("Skills:", [s[0] for s in data['skills']])
print("Experience:", [(j['title'], j['company']) for j in data['experience']])
print("Education:", data['education'])
# STOP if: name wrong, Spectrum missing, JT Somwaru Consulting present, any field empty, specific consulting client names appear, or resume contains evaluator/verdict language such as "Strong fit"
```

```python
# Cover letter verification — same pattern
src = open('/Users/jtsomwaru/.openclaw/workspace/scripts/build_resume_docx.py').read()
local_ns = {}
exec(src.split('if __name__')[0], local_ns)
cl = local_ns['parse_cover_letter_md']('/path/to/[company-slug]-cover-letter.md')
print("Company:", cl['company'])
print("Paragraphs:", len(cl['paragraphs']))
print("P1:", cl['paragraphs'][0][:80] if cl['paragraphs'] else 'EMPTY')
# STOP if: paragraphs == 0, P1 is a markdown header/metadata line, or specific consulting client names appear
```

If either check fails — fix the markdown, do not upload.

**Resume markdown format (exact structure required):**
```
# JT SOMWARU
contact line

## PROFESSIONAL SUMMARY
text

## SKILLS
**Category:** skill1, skill2

## EXPERIENCE

### Job Title
**Company Name**, Location, YYYY-Present

- Bullet one
- Bullet two

## KEY PROJECTS
**Project Name:** description

## EDUCATION
Degree | School | Year
```

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
    ("/tmp/jt-somwaru-resume.docx", find_folder("Resumes", ja), "[Job Title] - [Company] - Resume"),
    ("/tmp/jt-somwaru-cover-letter.docx", find_folder("Cover Letters", ja), "[Job Title] - [Company] - Cover Letter"),
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
