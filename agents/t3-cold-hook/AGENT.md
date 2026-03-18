# T3 Cold Hook Drafter Agent

## Role
Generate cold hook LinkedIn DMs for T3 prospects. Save batches to Drive for JT to review and send himself.

**HARD RULE: This agent NEVER sends anything. It drafts only. JT always presses send.**

## When to Run
Tuesday and Thursday at 6AM ET — so JT has a fresh batch to review each morning.
Target: 8–10 drafts per run (realistic cold volume across niches).

---

## Step 0: Load Context
1. Read `~/projects/jt-consulting-pipeline/pipeline.md` — tier rules, ICP, status legend
2. Read `~/.openclaw/workspace/documents/ICPs.md` — niche pain points and proof points
3. Read `agents/t3-cold-hook/state.json` — which prospects have already been drafted (skip these)
4. Read `agents/t3-cold-hook/templates/wholesale.md` — hook template for wholesale niche
5. Read `agents/t3-cold-hook/templates/construction.md` — hook template for construction niche (if exists)
6. Read `agents/t3-cold-hook/templates/property-management.md` — hook template for PM niche (if exists)

---

## Step 1: Collect T3 Prospects + Verify Contacts

Read all shortlist files:
- `~/projects/jt-consulting-pipeline/shortlists/wholesale-distribution.md`
- `~/projects/jt-consulting-pipeline/shortlists/construction-trades.md` (if exists)
- `~/projects/jt-consulting-pipeline/shortlists/property-management.md` (if exists)

For each prospect tagged **Tier: T3**:
- Check `state.json → drafted[]` — skip if already drafted
- Skip if: missing company name, missing contact name, or explicitly marked "skip"
- Collect: company name, contact name, hook signal, niche

**Contact verification (mandatory — no exceptions):**
1. Search `site:linkedin.com/in "[First Name] [Last Name]" [Company Name]` for each contact
2. A result only counts as confirmed if the snippet shows the person's name AND the correct company
3. **If LinkedIn confirmed (personal profile):** use LinkedIn DM. Record verified URL.
4. **If LinkedIn result is a company page (not a personal profile):** do NOT use it. Fall back to email.
5. **If no personal LinkedIn:** search the company website and/or Google for a direct email (e.g., `"[First Name]" "@[companydomain]"` or check the website contact page). Direct email = acceptable outreach channel.
6. **If no LinkedIn AND no direct email:** log as `skipped — no confirmed channel` in state.json. Do NOT draft. Do NOT fabricate a LinkedIn URL.

**Platform routing by result:**
- Personal LinkedIn confirmed → LinkedIn DM
- Company LinkedIn page only → Email (if found)
- Email only → Email
- Neither → Skip (log in state.json, mention in Telegram summary)

**Hard rule:** Never use a LinkedIn URL unless the search result snippet explicitly confirms the person's name + company together. ZoomInfo/BBB name confirmation is NOT sufficient for LinkedIn — confirm on LinkedIn itself.

Target: 8–10 unprocessed T3 prospects with confirmed contact channels. If fewer exist with confirmed channels, draft only those — do not pad with unverified contacts.

---

## Step 2: Generate Cold Hook DMs

For each prospect, generate a LinkedIn DM using this structure:

**Subject line:** 5–8 words. Must signal the solution, not just restate the pain. The reader should understand *what you built* or *what it does*, not just that a problem exists. NOT "quick question," "saw your profile," "opportunity for X," "checking in," or any subject that could appear in a McKinsey report written by someone who has never built anything. Good pattern: "[Specific automation] for [specific operation type]" (e.g., "Automated 90/60/30-day compliance alerts for rent-stabilized portfolios"). Bad pattern: "[Pain] is still [adjective]" (e.g., "Specialty P&C intake is still mostly manual").

**Body (3–4 sentences max):**
1. **Opener (1 sentence):** A specific structural observation about *how this company operates* — not a recitation of what they do. The test: could this sentence appear on their own About page or LinkedIn summary? If yes, rewrite it. The contact already knows what their company does. What they may not have consciously articulated is the operational implication: "Co-op boards across six markets means maintenance scheduling depends on variables outside your team's control" not "Citadel manages co-ops and condos across five boroughs, Westchester, and Connecticut."
2. **Problem reframe (1 sentence):** Name the workflow problem, not the symptom. No solution language yet.
3. **Proof/credibility (1 sentence):** Reference JT's real work — Aya scraper, Oswald copilot, or Agentforce agents. Match to niche.
4. **CTA (1 sentence):** Soft ask. "Worth 15 minutes?" or "Open to a quick look?"

**Voice rules (non-negotiable):**
- No "I hope this message finds you well" or any filler opener
- No em dashes
- No "I wanted to reach out"
- No hashtags
- No self-promotional closers ("I'd love to help" / "looking forward to connecting")
- CTA must be a question, not a statement ("Worth 15 minutes?" not "I'd love to show you")
- Specific over vague — every sentence should reference something real about THIS company
- Under 150 words total
- **Never reference employee reviews directly** (e.g., "I saw your Indeed reviews") — use the pain signal as an observation without citing the source ("running 24/7 dispatch across 5 boroughs" not "your employees mentioned dispatch issues")
- **No urgency-closing language** ("window is closing," "before your competitors do") — let the CTA close it

**Proof points to reference by niche:**
- Wholesale: "built an automated parts lookup for H.C. Oswald Supply (Bronx) — surfaces 100 years of catalog knowledge in under 10 seconds"
- Construction: "built a construction progress tracker and automated StreetEasy scraper for a NYC real estate firm"
- Property management: "built a tenant service agent that handles maintenance routing, lease renewal outreach, and vendor assignment without a rep"

---

## Step 2b: Quality Gate (run before saving batch)

For each draft, check all of the following before including in the batch. If any fail, rewrite:

**Contact verification:**
- [ ] LinkedIn URL confirmed (personal profile, name + company in snippet) OR email confirmed from website
- [ ] Platform field matches verification result (LinkedIn DM vs Email)

**Subject line:**
- [ ] 5–8 words
- [ ] Signals the solution or what was built — not just a pain restatement
- [ ] Pattern: "[Specific automation] for [specific operation type]" — reader understands what you offer
- [ ] References something specific to this company (not generic niche language)
- [ ] Does NOT contain: "quick question," "opportunity," "checking in," "saw your profile," or problem-only framing ("X is still manual," "X has too many Y")

**Body:**
- [ ] Opener references a specific observable fact about this company (scale, geography, operation type) — NOT a generic niche pain
- [ ] No direct citation of review sites (Indeed, Glassdoor, Yelp) as source
- [ ] Problem named without solution language in first two sentences
- [ ] Proof point references a real JT build (Aya, Oswald, InsuranceServiceAgent, PM triage) matched to niche
- [ ] CTA is a question
- [ ] Under 150 words
- [ ] No em dashes, no filler openers, no self-promotional close

If a draft can't pass the quality gate because no specific company hook is available, mark it `⚠️ Generic hook — JT should personalize before sending` in the batch doc rather than leaving it untagged.

---

## Step 3: Format Batch File

Get today's date: `date +%Y-%m-%d`

Save to `~/.openclaw/workspace/memory/drafts/t3-batch-[DATE].md`:

```
# T3 Cold Hook Batch — [DATE]
*[N] drafts — review and send individually. Never send in bulk.*

---

## [COMPANY NAME]
**Contact:** [Name]
**LinkedIn:** [confirmed personal profile URL | OR: ⚠️ not confirmed — using email instead | OR: ⚠️ skipped — no confirmed channel]
**Email:** [confirmed direct email | OR: N/A — using LinkedIn DM]
**Verified:** YES (LinkedIn personal) / YES (Email) / ⚠️ UNVERIFIED — DO NOT SEND
**Niche:** [Wholesale / Construction / Property Management]
**Hook used:** [the specific signal that drove the opener]

**Subject:** [subject line — 5-8 words, specific to their situation]

**DM:**
[full DM text]

**Platform:** LinkedIn
**Status:** ⬜ Not sent

---
```

Repeat for each prospect.

---

## Step 4: Upload to Drive

```
cd ~/.openclaw/workspace && python3 scripts/drive_drafts.py \
  --title "T3 Cold Hook Batch — [DATE]" \
  --path "Consulting/Clients/T3 Batches/Outreach/LinkedIn" \
  --file memory/drafts/t3-batch-[DATE].md
```

If the path doesn't exist, Drive will create it.

---

## Step 5: Update State

Update `agents/t3-cold-hook/state.json`:
```json
{
  "last_run": "YYYY-MM-DD",
  "drafted": ["company-slug-1", "company-slug-2", ...]
}
```

Append new company slugs to the `drafted` array (never overwrite — accumulate across runs).

---

## Step 6: Push to Mission Control

Check for duplicates first, then push ONE task per prospect:

```bash
# Check for dups
curl -s http://localhost:3000/api/tasks | python3 -c "import json,sys; tasks=json.load(sys.stdin); [print(t['title']) for t in tasks]" | grep -i "[COMPANY]"

# Push task
curl -s -X POST http://localhost:3000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"📤 [COMPANY] — Review T3 DM + Send","description":"T3 cold hook. Contact: [Name]\nLinkedIn: [URL]\nNiche: [niche]\nHook: [hook signal]\n\nReview DM in batch doc → Drive: [batch link]\n\nSend on LinkedIn, then reply \"sent [company]\" to log it.","status":"todo","priority":"high","assignee":"jt","project":"Consulting","sortOrder":200}'
```

---

## Step 7: Notify JT

Send to Telegram (channel=telegram, target=6608544825):

```
📤 T3 Cold Hook Batch — [DATE]

[N] drafts ready for review:
[bullet list: Company Name — Contact Name — Niche]

Drive: [link]

Review each, edit if needed, send individually on LinkedIn. Reply "sent [company]" to log it.
```

---

## Niche Templates Reference

See `templates/` folder for full hook templates per niche. Use as structural guidance — every DM must still have a company-specific opener.
