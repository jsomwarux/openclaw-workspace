# xhigh Systems Audit — Content + Sports Distribution

Date: 2026-05-13
Scope: JT personal content stack, Wednesday LinkedIn, weekly X/LinkedIn generation, news hooks, Notion calendar, Drive draft behavior, Sports GM / @dynastyjig packs, dynasty replies, Reddit drafts, AI Ops Teardown, ReelFarm Intel.

## Bootstrap check

`wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md`

- AGENTS.md: 27,863 bytes, under 28k but close
- MEMORY.md: 19,161 bytes, under 20k but close
- TOOLS.md: 13,581 bytes, under 16k
- HEARTBEAT.md: 15,837 bytes, under 16k but close

No bootstrap append performed.

## Inventory

### Live cron surfaces inspected

| Cron | ID | Schedule | Enabled | Timeout |
|---|---|---:|---:|---:|
| ReelFarm Daily Strategy Intel | a97df783-31c5-4269-a4f0-3ece75af838d | 15 17 * * * | true | 900 |
| content-reminder | 5e66b4ee-aee3-497d-90ba-7aad670970a3 | 0 8 * * 2,3,4,5,6 | true | 360 |
| Daily DynastyJig Niche-Growth X Post Pack | 1e614c8a-adb8-4a02-b35f-3031db55b337 | 30 8 * * * | true | 600 |
| Daily News Hook | 4a70dda4-da77-4437-9ae0-993611e94c5a | 30 9 * * 1-5 | true | 5400 |
| dynasty-replies-gen | 8b968751-6e59-42e5-b2ce-09f57d36176c | 0 11 * * * | true | 360 |
| reddit-daily-gen | bbe49024-458a-4496-9c7c-7a278615810f | 30 11 * * * | true | 420 |
| Viral Post Swipe File — X Research | 33b8b0a2-e86c-4f51-aa4f-b8537def3107 | 45 5 * * 1,3,5 | true | 1800 |
| content-sunday | d918122d-d58c-4985-a181-126cfd7e6be7 | 0 9 * * 0 | true | 360 |
| ReelFarm Weekly Strategy Synthesis | bb0819d0-8900-4e2a-99a2-28ab950365ab | 0 17 * * 0 | true | 900 |
| Weekly Seeds Prompt | fb1d6691-5663-47aa-bb78-f90813b33203 | 0 19 * * 0 | true | 120 |
| AI Ops Teardown Weekly Draft | f96cc24f-55e6-4064-a075-b897156a22f2 | 15 19 * * 0 | true | 1800 |
| content-generate-linkedin | fe984519-ec58-4c6e-a096-9ac425f735a3 | 45 6 * * 1 | true | 900 |
| content-generate-x | cb8f29dd-0db1-4abd-b87e-3e7168ca4a97 | 0 9 * * 1 | true | 1800 |
| Sports GM Weekly Market Report | 008a349c-af59-4e6b-88bb-97f65dba61c6 | 0 9 * * 2 | true | 240 |

### Key files and output surfaces inspected

- `skills/sports-gm/SKILL.md`
- `skills/wednesday-linkedin/SKILL.md`
- `skills/content-atomizer/SKILL.md`
- `skills/high-stakes-draft-eval/SKILL.md`
- `agents/content-calendar/AGENT.md`
- `agents/content-scheduler/AGENT.md`
- `agents/vibe-marketing/AGENT.md`
- `agents/reelfarm-intel/daily-prompt.md`
- `agents/reelfarm-intel/weekly-prompt.md`
- `memory/content/weekly-2026-05-11.md`
- `memory/content/bank/2026-05-13/wednesday-linkedin.md`
- `memory/content/bank/2026-05-13/dynastyjig-niche-growth-post-pack.md`
- `memory/content/news-hooks/2026-05-13.md`
- `memory/content/reply-targets-2026-05-13.md`
- `memory/sports-gm/reports/weekly-gm-report-2026-05-12.md`
- `memory/reelfarm/reports/daily/2026-05-12.md`
- `scripts/notion-calendar-push.py`
- `scripts/drive_drafts.py` command references

## Findings

### What is already strong

1. **@dynastyjig daily pack quality is now materially better than old generic fantasy content.** The 2026-05-13 pack includes fresh Sports GM market references, native pattern teardown, rejected generic patterns, quality gate notes, and a best-post recommendation. It correctly avoids product promo in public drafts.
2. **Sports GM methodology is safer.** The 2026-05-12 market report explicitly avoids raw-value cross-source comparisons and frames rank gaps as research candidates, not public calls.
3. **Wednesday LinkedIn has the right high-stakes gate.** The 2026-05-13 replacement post includes concrete cadence, destination, and 4-hour outcome, plus Exec/Practitioner/Lurker advisory board approvals.
4. **Daily News Hook skipped instead of hallucinating timeliness.** `memory/content/news-hooks/2026-05-13.md` recorded a SKIP because searches returned no usable specific news hook.
5. **ReelFarm Intel has good no-empty/no-noise behavior.** The daily prompt and 2026-05-12 report send Telegram only when actionable recommendations exist, and later no-input checks do not overwrite useful earlier output.
6. **Dynasty replies have a hard freshness stop.** The cron prompt blocks stale reply targets and requires all final targets ≤24h old.

### Gaps patched

1. **Notion calendar script had hardcoded token fallback risk.**
   - Before: `scripts/notion-calendar-push.py` used `NOTION_TOKEN` from environment but also had a hardcoded fallback token.
   - After: env-only token; if missing, it fails cleanly before external write.

2. **Notion calendar script lacked a dry-run / duplicate-batch guard.**
   - Added `--dry-run` for payload validation without Notion writes.
   - Added in-batch duplicate detection on `(platform, date, first 120 chars of post)`.

3. **Weekly file contained a stale `[Source]` placeholder in the Sunday X learn-in-public slot.**
   - Before: placeholder copy was marked as passing checklist even though it was not citation-safe.
   - After: replaced with explicit `SKIP_SLOT` and blocker reason so delivery should not treat it as copy.

4. **Distribution gates were spread across prompts but not reusable as a local smoke check.**
   - Added `scripts/content_distribution_guard.py` to validate saved artifacts without external writes.
   - Checks: dynasty pack required sections, weekly required sections, placeholder/stale markers, em dashes, generic phrases, news-hook skip/draft sanity, Notion env-only auth, Notion dry-run support, Notion duplicate guard.

## Files changed

- `scripts/notion-calendar-push.py`
  - Removed hardcoded Notion token fallback.
  - Added `--dry-run`.
  - Added batch duplicate guard.
  - Added missing-token failure path.

- `scripts/content_distribution_guard.py`
  - New reusable smoke-check script for content distribution artifacts.

- `memory/content/weekly-2026-05-11.md`
  - Replaced stale Sunday `[Source]` X copy with `SKIP_SLOT` blocker.

## Validation

Commands run:

```bash
python3 -m py_compile scripts/content_distribution_guard.py scripts/notion-calendar-push.py
python3 scripts/content_distribution_guard.py \
  --dynasty-pack memory/content/bank/2026-05-13/dynastyjig-niche-growth-post-pack.md \
  --weekly memory/content/weekly-2026-05-11.md \
  --news-hook memory/content/news-hooks/2026-05-13.md \
  --check-notion-script
python3 scripts/notion-calendar-push.py \
  --batch '[{"platform":"X","date":"2026-05-13","post":"audit smoke test"},{"platform":"X","date":"2026-05-13","post":"audit smoke test"}]' \
  --dry-run
```

Results:

- Python compile: PASS
- Content distribution guard after patch: `CONTENT_DISTRIBUTION_GUARD_PASS`
- Notion dry-run duplicate test: one duplicate skipped, one dry-run accepted, no external Notion write
- Token scan: no hardcoded `ntn_...` token pattern found in `scripts/notion-calendar-push.py`
- Weekly source placeholder scan: `[Source] count 0`, `SKIP_SLOT count 1`

## A+ gate score

| Gate | Before | After | Notes |
|---|---:|---:|---|
| Voice quality | B+ | A- | Strong current outputs; guard catches em dashes and generic phrases, but full voice judgment still requires human/model review. |
| Current-source freshness | A- | A | Dynasty, news hook, replies, ReelFarm all have freshness/skip gates. |
| Distribution usefulness | B+ | A- | Notion dry-run + duplicate guard improves calendar hygiene. |
| Platform-native drafts | A- | A- | Sports/native teardown is strong; personal weekly content still has occasional weak slots. |
| Proof alignment | A- | A | Wednesday and Sports GM report use concrete proof and rank methodology. |
| No generic content | B+ | A- | Reusable guard now catches obvious generic/stale markers. |
| Failure alerts / skip behavior | A- | A- | Most crons skip empty/no-input. No new high-blast-radius cron edits made. |
| Delivery guards | B+ | A | Notion env-only auth, dry-run, duplicate guard; content reminders already block stale markers. |
| Task/calendar hygiene | B | A- | Notion push safer; no Mission Control task needed because fix was local and low blast radius. |

**Before grade:** B+ / A-

**After grade:** A-

## Remaining blockers / risks

1. **Not full A+ until the guard is wired into generation/delivery crons.** The script exists and passes, but cron payloads do not yet call it automatically. I did not patch cron definitions because that is higher blast radius and should be done as a controlled config change.
2. **Sports GM Weekly Market Report timeout is only 240s.** Current reports exist, but fetch/report work can easily grow. If future run duration approaches timeout, increase before failures.
3. **AGENTS, MEMORY, HEARTBEAT are near bootstrap budgets.** No append was needed here, but future edits should trim/move sections before appending.
4. **Weekly content can still be seedless.** The generator correctly warns when weekly seeds are empty, but strategic quality depends on JT/Eve capturing real seeds during the week.

## Recommendation

Do not change public posting behavior. The system should remain draft/save/review only.

Next controlled improvement: wire `scripts/content_distribution_guard.py` into `content-generate-x`, `content-generate-linkedin`, `Daily DynastyJig`, and `content-reminder` as a pre-delivery/local artifact check. Do this in one cron-hardening pass with approval or as part of the next xhigh audit batch.
