# XHigh Systems Audit — Consulting Pipeline / Outreach
Date: 2026-05-13
Auditor: OpenClaw subagent

## Overall grade
- Before: B-
- After: A-
- Status: materially hardened, not perfect. The core loop is safe enough to run, but still carries stale cold-outreach backlog and one noisy/high-cost nightly pipeline cron.

## Inventory
### Crons
- `outreach-pipeline` (`651fa1da-84d7-44b3-8e10-6a46e1c05cf6`): daily 3:00 AM ET, isolated, `openai-codex/gpt-5.5`, timeout 1800s, failure alert enabled. Last run 2026-05-13 ok, 146s, **delivery not delivered**. Recent prior runs delivered.
- `outreach-email-pivot-daily` (`9d9b165b-a52f-4dc6-bc02-58f154bcff06`): daily 6:45 AM ET, isolated. Patched from `openai-codex/gpt-5.5` + Telegram delivery to `moonshot/kimi-k2.6`, thinking off, no routine delivery, failure alert enabled. Last run ok, ~19s.
- Related strategic/niche jobs found but not pipeline-specific: nightly autonomous leverage, monthly niche fitness review, monthly goal-skills gap.

### Scripts
- `scripts/outreach_update.py`
- `scripts/outreach_email_pivot.py`
- `scripts/pipeline_drive_sync.py`
- `scripts/drive_drafts.py`
- supporting: `scripts/mission_control_north_star_audit.py`, `scripts/slides_framework.py`

### Skills / rules / docs
- `skills/opticfy-pipeline/SKILL.md`
- `skills/opticfy-pipeline/scripts/preflight.sh`
- `skills/cold-email/SKILL.md`
- `docs/agents/outreach-rules.md`
- `~/projects/jt-consulting-pipeline/EMAIL-PIVOT-RULES.md`
- `~/projects/jt-consulting-pipeline/pipeline.md`
- `~/projects/jt-consulting-pipeline/drive-canonical-names.md`
- `agents/autoresearch/checklists/jt-consulting-pipeline.md`
- `agents/autoresearch/checklists/outreach-email-pivot.md`

## Gate scores
| Gate | Before | After | Notes |
|---|---:|---:|---|
| Purpose alignment | B | B+ | Strong ICP/channel rules, but cold backlog still competes with warmer/referral work. North Star audit has demoted stale tasks. |
| Model/thinking/timeout | B- | A- | Main pipeline has enough timeout; email pivot was overpowered and chatty. Patched to cheap model/no routine delivery. |
| Producer-consumer timing | A | A | Main pipeline 3 AM -> pivot 6:45 AM leaves >90 min gap. |
| Input freshness | B | B+ | Research/doc gates exist; active backlog still has old M-sequence state. |
| Output finality | B | A- | Drive links and MC tasks exist; patched Drive upload idempotency and no-overwrite pivot behavior. |
| Delivery/Drive behavior | C+ | A- | Fixed nonstandard outreach title in `pipeline_drive_sync.py`; made Drive upload idempotent by title+folder. |
| Mission Control hygiene | C | B+ | Found historical duplicate Email Pivot tasks. Active exact-title duplicates now 0; scripts now avoid duplicate follow-ups and close Email Pivot tasks on send confirmation. |
| Same-turn send updates | B | A- | Rule existed. Script now closes Review + Send and Email Pivot tasks and prevents duplicate follow-up task creation. |
| Failure alerts | B | A- | Pivot cron had no failure alert; now enabled. Main pipeline already had alert but latest delivery failed despite ok run. |
| Safe search/API path | B+ | B+ | Cron prompt uses local/scripted paths and warns against unsafe Drive/title behavior; web search not central to pivot scan. |
| Duplication/stale-noise control | C | B+ | Patched idempotency and dedup. Remaining stale backlog is demoted, not eliminated. |

## Issues found
1. **Email pivot cron used an expensive reasoning model and delivered routine “no eligible prospects” messages.** This created cost/noise for a deterministic scanner.
2. **Email pivot cron had no failure alert.** A silent scanner failure would block email-pivot follow-up.
3. **Drive upload scripts created duplicate Google Docs on repeat runs.** `drive_drafts.py` and `pipeline_drive_sync.py` created new docs every time.
4. **`pipeline_drive_sync.py` still titled LinkedIn outreach docs `[Company] — Outreach Draft`, contradicting the pipeline rule requiring `[Company] — LinkedIn DM (3-touch)`.**
5. **`outreach_email_pivot.py --execute` overwrote existing `email-draft.md` when the MC task was missing.** That could silently mutate JT-reviewed copy during repair/backfill.
6. **`outreach_update.py` only closed the first matching Review + Send task and did not close Email Pivot tasks.** It also created duplicate follow-up tasks if rerun.
7. **Active MC state had historical duplicate email-pivot churn.** Exact active duplicates are now clear, but many done duplicates remain in archive as evidence of prior loop.
8. **21 `brief.json` files were missing either `tier` or `jt_review_required`.** Patched all active brief files to include both fields, defaulting review required true.
9. **Latest `outreach-pipeline` cron run was `ok` but delivery was `not-delivered`.** Prior runs delivered, so this is an alertable drift, not a hard failure yet.

## Patches applied
- `scripts/drive_drafts.py`
  - Added `find_doc()` and idempotent doc reuse by exact title + folder.
  - Applies to text and docx upload paths.
- `scripts/pipeline_drive_sync.py`
  - Added idempotent doc reuse by exact title + folder.
  - Changed LinkedIn outreach doc title from `[Company] — Outreach Draft` to `[Company] — LinkedIn DM (3-touch)`.
- `scripts/outreach_email_pivot.py`
  - If `email-draft.md` and an active Email Pivot task already exist, skip.
  - If draft exists but task is missing, preserve the local draft and create the missing task instead of overwriting copy.
  - Scan mode now distinguishes “existing draft, missing task” from “would generate new pivot.”
- `scripts/outreach_update.py`
  - Added task fetch/patch helpers using supported `/api/tasks` PATCH shape.
  - Closes active matching `Review + Send` and `Email Pivot` tasks on send confirmation.
  - Avoids duplicate active M2/M3 follow-up tasks.
- Cron `outreach-email-pivot-daily`
  - Model: `moonshot/kimi-k2.6`
  - Thinking: off
  - Routine delivery: disabled
  - Failure alert: enabled to Telegram after 1 error, 24h cooldown
- Client `brief.json` files
  - Added missing `jt_review_required: true` and normalized/inferred missing `tier` on 17 active brief files.
- MC cleanup during validation
  - Closed accidental test-created Atlas M2 task and stale duplicate Atlas Email Pivot active tasks.
  - Re-created one Atlas Email Pivot MC task through the fixed script to restore correct active state.

## Commands/tests run
```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
python3 -m py_compile scripts/outreach_update.py scripts/outreach_email_pivot.py scripts/pipeline_drive_sync.py scripts/drive_drafts.py
openclaw cron list --json
openclaw cron runs --id 651fa1da-84d7-44b3-8e10-6a46e1c05cf6 --limit 3
openclaw cron runs --id 9d9b165b-a52f-4dc6-bc02-58f154bcff06 --limit 5
python3 scripts/outreach_email_pivot.py --min-days 7
python3 scripts/outreach_email_pivot.py --execute --prospect atlas-nyc --min-days 7
python3 scripts/drive_drafts.py --title "Audit Idempotency Test — 2026-05-13" --path "Research/Audit Tests" --file /tmp/drive-idempotency-test.txt
python3 scripts/drive_drafts.py --title "Audit Idempotency Test — 2026-05-13" --path "Research/Audit Tests" --file /tmp/drive-idempotency-test.txt
openclaw cron edit 9d9b165b-a52f-4dc6-bc02-58f154bcff06 --model moonshot/kimi-k2.6 --thinking off --no-deliver --failure-alert --failure-alert-after 1 --failure-alert-channel telegram --failure-alert-to 6608544825 --failure-alert-cooldown 24h --failure-alert-mode announce
openclaw cron show 9d9b165b-a52f-4dc6-bc02-58f154bcff06
```

## Validation results
- Python compile: ✅ all patched scripts compile.
- Email pivot scan after patches: ✅ 8 stale M2 prospects found; all have existing draft + active Email Pivot task; no new pivots created.
- Email pivot execute for Atlas after patches: ✅ skipped because draft + active task already exist; no duplicate task/doc created.
- Drive idempotency: ✅ second upload reused the same Google Doc URL: `https://docs.google.com/document/d/14ReeGK9w4wiivzuzMMiVcap1r1fP4d21vVOWolhcyOo/edit`.
- Active MC exact-title duplicates: ✅ Email Pivot 0, Review + Send 0, M2 0, M3 0, M4 0.
- Review + Send assignee check: ✅ 0 active Review + Send tasks assigned to Eve.
- High-priority stale outreach tasks: ✅ 0; stale outreach tasks are low/demoted.
- `brief.json` guard fields: ✅ 0 missing `tier`/`jt_review_required` after patch.
- Cron patch: ✅ pivot cron now cheap/no routine delivery/failure-alerted.

## Remaining blockers / recommendations
1. **Main `outreach-pipeline` cron delivery drift:** latest run was ok but `deliveryStatus=not-delivered`. If this repeats, patch to no routine delivery + failure-only alert, or send only when new artifacts are created.
2. **Main pipeline prompt is huge and costly.** It consumes ~80K-100K input tokens per run. This should be collapsed into a script-first runner plus concise prompt.
3. **Stale cold backlog is controlled, not gone.** MC has many low-priority demoted cold tasks; this is acceptable only because the North Star audit demotes them. A monthly cold-backlog archive sweep would make the board cleaner.
4. **Historical duplicate Drive docs likely remain.** The scripts now prevent new exact-title duplicates, but old duplicates need a one-time Drive cleanup if JT cares.
5. **Brief-field backfill used safe defaults.** `jt_review_required` defaults true; inferred missing tier defaults T2 for client brief artifacts. Review edge demo/template briefs before using them operationally.

## Final judgment
The system is **not fully optimal**, but it is now materially safer and cleaner. The biggest remaining improvement is reducing the 3 AM pipeline from a broad LLM cron into deterministic script stages with LLM only for new-copy generation.
