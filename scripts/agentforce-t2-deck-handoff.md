# build_agentforce_t2_deck.py — Handoff

## What Was Built

A Python script that generates a 7-slide Google Slides proposal deck for Agentforce T2 insurance prospects. Modeled exactly after `build_wholesale_t2_deck.py` — same emotional arc (Recognition → Stakes → Demo → Proof → Inevitability → Action), same `slides_framework.py` engine, adapted for Agentforce/Salesforce/insurance context. Includes COI requests, claims intake, policy inquiry, and renewal topics as the default insurance use case.

## How to Use It

**Master template (placeholders only):**
```
python3 scripts/build_agentforce_t2_deck.py --master
```

**Specific prospect (quick build):**
```
python3 scripts/build_agentforce_t2_deck.py \
  --slug lawley-insurance \
  --company "Lawley Insurance" \
  --niche "Commercial P&C" \
  --topics 5 \
  --hours-per-week 18 \
  --requests-per-month 150 \
  --sf-objects "Account,Case,Opportunity"
```

**Full pipeline (after Agentforce agent runs):**
```
python3 scripts/build_agentforce_t2_deck.py \
  --brief ~/projects/jt-consulting-pipeline/clients/[slug]/brief.json \
  --demo-transcript ~/projects/jt-consulting-pipeline/clients/[slug]/demo-transcript.md \
  --agent-config ~/projects/jt-consulting-pipeline/clients/[slug]/agent-config.md
```
When `demo-transcript.md` is present, the deck uses real conversation exchanges from the demo. Without it, it uses instructional placeholder text.

## How to Maintain It

**What could break:**
- `slides_framework.py` changes → test with `python3 scripts/build_agentforce_t2_deck.py --master` after any framework update
- Google Drive folder name changes → update `folder` variable in `build_deck()` function (line ~190)
- New insurance niches → may need to update default `topics_list` in `main()` (line ~240)
- `brief.json` schema changes → update `load_brief()` parser (line ~175)

**Syntax check:** `python3 -m py_compile scripts/build_agentforce_t2_deck.py`

## v2 Ideas

1. **Niche variants** — add `--template` flag to switch between insurance, property management, and construction templates (each with niche-specific headlines, stats, and pain points)
2. **Real demo screenshot embedding** — accept a `--screenshot` path to embed an actual Agentforce conversation screenshot into slide 4 instead of text transcript
3. **Auto-pipeline trigger** — after Agentforce agent completes and writes `demo-transcript.md`, a cron detects it and auto-runs this script + uploads to Drive + pushes a 🌙 Review MC task
