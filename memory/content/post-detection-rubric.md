# Post-Detection Rubric
*Used by all autonomous agents (overnight, outreach-pipeline, main session) to evaluate whether a work event is worth generating a content post.*
*Shared standard — update this file to tighten or loosen detection across all agents simultaneously.*

---

## The Core Test
**Would a builder or consultant who does similar work find this immediately useful, surprising, or recognizable as a problem they've hit?**

If yes: generate a post.
If not: skip.

---

## PASS — Generate a Post

At least ONE of these must be true:

1. **Non-obvious problem solved** — the solution isn't in any docs, tutorial, or Stack Overflow post. It required actually running this system to discover.
   - Example: "Spanish lesson cron was delivering to @jtsomwaru (username) instead of 6608544825 (numeric ID) — silent fail every night. Telegram requires numeric IDs for isolated sessions."

2. **Something broke in an unexpected way** — the failure mode teaches something about how the system actually behaves.
   - Example: "Skills researcher timed out at exactly 300s three weeks in a row. timeoutSeconds was set to 600. Turns out the scheduler has an internal 300s cap that overrides the job setting. The fix was a config key, not the timeout value."

3. **Real outcome with a specific number** — a client result, time saved, cost, or metric that makes the outcome concrete.
   - Example: "StreetEasy scraper ran for the 6th time tonight. 0 manual searches since deployment. $1,000 project."

4. **Pattern across multiple instances** — observed in 2+ prospects, builds, or runs this week. Worth naming.
   - Example: "Third property management prospect this week with AppFolio confirmed but zero automation layer. The tool is there. The workflow isn't. That's the pitch."

5. **Architectural decision with real tradeoffs** — a design choice where the wrong option was plausible and the right one has a concrete reason.
   - Example: "Switched content generation and delivery to separate crons. Generator: isolated, 5+ minutes. Delivery: 60 seconds. One failure can't kill the other. Separation IS the reliability."

---

## FAIL — Skip

ALL of these cause an automatic skip:

- Routine task completion with no insight ("processed 3 T2 prospects tonight")
- Generic AI observation that doesn't require having built this system
- Same topic already in posted-log.jsonl within 30 days
- Build that's already been posted about recently (check posted-log)
- Something that requires context only JT has to be meaningful to anyone else
- Observation that's better suited for consulting-observations.md or job-market-observations.md (those are lower-signal inputs; this rubric is for post-ready insights)

---

## Volume Expectation
Target: 1-3 autonomous posts per week across all detection points. If a week produces 0, the rubric is working (nothing truly post-worthy happened). If a week produces 5+, the rubric is too loose — review and tighten.

---

## Output Format (when a post qualifies)

Generate TWO posts per event — one X post and one LinkedIn post. Write both to bank immediately.

**LinkedIn format for auto-detected builds:**
- Format: "Behind the Build" or "Proof of Work" — 3–5 short paragraphs
- Lead with the problem the build solves, not the build itself
- Include one specific architectural decision or tradeoff
- End on capability proof, never advice or self-promotion
- Must pass content-voice.md audit checklist before writing to bank
- File: `memory/content/bank/[MONDAY-DATE]/auto-[slug]-linkedin.md`

**File path:** `~/.openclaw/workspace/memory/content/bank/[THIS-MONDAY-DATE]/auto-[slug].md`

**Format:**
```
# auto-[slug] — [YYYY-MM-DD]
Pillar: autonomous-detection
Source: [overnight | outreach-pipeline | main-session | build]
Rubric: [which PASS criteria triggered — e.g. "non-obvious problem solved"]
angle_id: null

---

[post text — 2-4 tweets, X format, lowercase where appropriate, no banned words]
```

**Drive upload (X):**
```bash
cd ~/.openclaw/workspace && python3 scripts/drive_drafts.py \
  --title "Auto-detected post — [slug] ([DATE])" \
  --path "Content/X" \
  --file memory/content/bank/[THIS-MONDAY-DATE]/auto-[slug].md
```

**Drive upload (LinkedIn):**
```bash
cd ~/.openclaw/workspace && python3 scripts/drive_drafts.py \
  --title "Auto-detected LinkedIn — [slug] ([DATE])" \
  --path "Content/LinkedIn" \
  --file memory/content/bank/[THIS-MONDAY-DATE]/auto-[slug]-linkedin.md
```

**posted-log entries:**
```json
{"date": "[YYYY-MM-DD]", "platform": "x", "pillar": "autonomous-detection", "topic": "[topic]", "banked": true, "posted": false, "source": "[source]", "rubric": "[which criterion]"}
{"date": "[YYYY-MM-DD]", "platform": "linkedin", "pillar": "autonomous-detection", "topic": "[topic]", "banked": true, "posted": false, "source": "[source]", "rubric": "[which criterion]"}
```

---

## What Makes a Good Auto-Detected Post

The post must read like it came from operational experience, not observation. Test: **could a content marketer with no implementation background have written this?** If yes, it failed the rubric even if it passed one of the PASS criteria above.

Good: "isolated crons don't inherit session defaults. found this when an unconfigured job defaulted to Opus — $0.57 for one run. always set model explicitly."

Bad: "always test your AI agent configurations before going live in production"
