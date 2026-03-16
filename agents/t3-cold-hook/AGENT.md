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

## Step 1: Collect T3 Prospects

Read all shortlist files:
- `~/projects/jt-consulting-pipeline/shortlists/wholesale-distribution.md`
- `~/projects/jt-consulting-pipeline/shortlists/construction-trades.md` (if exists)
- `~/projects/jt-consulting-pipeline/shortlists/property-management.md` (if exists)

For each prospect tagged **Tier: T3**:
- Check `state.json → drafted[]` — skip if already drafted
- Skip if: missing company name, missing contact name, or explicitly marked "skip"
- Collect: company name, contact name, hook signal, niche
- **Find LinkedIn profile URL:** search `site:linkedin.com/in "[First Last]" [Company]` for each contact. Note the URL or 'not found — search manually' if no clear match.

Target: 8–10 unprocessed T3 prospects. If fewer exist, draft all available.

---

## Step 2: Generate Cold Hook DMs

For each prospect, generate a LinkedIn DM using this structure:

**Subject line:** One specific observation (5–8 words). NOT "quick question" or "saw your profile." Must reference something real about the company or niche.

**Body (3–4 sentences max):**
1. **Opener (1 sentence):** Specific to this company — reference the hook signal from the research. This is what makes it non-generic. If no specific hook exists beyond niche fit, use the niche pain point as the opener.
2. **Problem reframe (1 sentence):** Name the workflow problem, not the symptom. No solution language yet.
3. **Proof/credibility (1 sentence):** Reference JT's real work — Aya scraper, Oswald copilot, or Agentforce agents. Match to niche.
4. **CTA (1 sentence):** Soft ask. "Worth 15 minutes?" or "Open to a quick look?"

**Voice rules (non-negotiable):**
- No "I hope this message finds you well" or any filler opener
- No em dashes
- No "I wanted to reach out"
- No hashtags
- Specific over vague — every sentence should reference something real
- Under 150 words total

**Proof points to reference by niche:**
- Wholesale: "built an automated parts lookup for H.C. Oswald Supply (Bronx) — surfaces 100 years of catalog knowledge in under 10 seconds"
- Construction: "built a construction progress tracker and automated StreetEasy scraper for a NYC real estate firm"
- Property management: "built a tenant service agent that handles maintenance routing, lease renewal outreach, and vendor assignment without a rep"

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
**LinkedIn:** [profile URL — search `site:linkedin.com/in "[First Last]" [Company]` | if not found: 'not found — search manually']
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

## Step 6: Notify JT

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
