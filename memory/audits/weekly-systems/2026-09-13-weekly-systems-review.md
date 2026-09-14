# Weekly Systems Review — 2026-09-13

## North Star Scoreboard

- Cash collected MTD: **$0** from Mission Control via `north_star_pipeline.py`; gap to $10K: **$10,000**. MSI is recorded fully paid/closed on Sep 9, but its exact cleared-payment date is not logged, so it is not counted as September cash.
- Pipeline stage movement this week: **1** — MSI moved to `closed_won_collected` on Sep 9. Altmark, DHCR, and Maiky did not move.
- Waiting-on items older than seven days: **3** — Altmark rent delinquency (client + JT, last touch Aug 10), DHCR/Altmark decision (Yair + Adi, Aug 25), and Maiky cost review (Aug 10).

## Six Outcome KPIs

1. Posts delivered vs posted: **0 / 0 evidenced** for Sep 7–13. The content lane is frozen and `memory/content/posted-log.jsonl` has no current-week rows.
2. Engagement per posted item: **N/A (0 posted)**. A future posted item still needs URL, impressions, reactions, replies, and date captured in the distribution ledger.
3. Outreach packets completed vs sent vs replied: **5 / 0 / 0 evidenced**. Five cohort-one buyer messages cleared independent review on Sep 10; the send window moved to Sep 15 and no send/reply proof exists yet.
4. Consulting pipeline stage movement: **1 record moved** — MSI closed as fully paid/collected; three waiting-on records remain stale.
5. Cron delivery rate: **11/13 (84.6%) latest runs healthy**; explicit announce jobs were **3/4 (75%) delivered**. Friday Scoreboard failed before producing content.
6. Dollars spent: **OpenRouter $0.00 + X API $0.00 = $0.00** for the tracked week. Monthly model-spend pace is **$1.02** against the $50 target.

## Systems Audit

- Cron health: **13 jobs checked**; all have run at least once and none are within 10% of timeout. Two are red: `skill-collection-review-main` has 3 consecutive failures because writable `SKILL.md` content is 273,999 bytes against the 240,000-byte cap; `Friday Scoreboard` has 5 consecutive rate-limit failures and resets Sep 14 at 9:23 PM ET. The Friday run produced no content, so there was nothing to resend. No fixed Sunday 10 AM conflict was found, though the system-owned hourly heartbeat can overlap. Non-heartbeat weekday schedule remains below 20 invocations/day; including the hourly system heartbeat exceeds 20 and remains a tracked owner-level drift.
- File budgets: `AGENTS.md` **38,781/28,000 FAIL**; `MEMORY.md` **13,770/20,000 PASS**. Root `TOOLS.md` and `HEARTBEAT.md` are missing; the only heartbeat file found is `memory/HEARTBEAT.md`. The embedded tool-reference section (~5 KB), relocated USER context (~5.1 KB), and duplicate operational sections are the clearest AGENTS extraction candidates. This cron did not self-modify the protected file.
- Processes: gateway reachable/active at PID 1415, sampled at 4.5% CPU and about **974 MB RSS** after >10 days. CPU is below threshold, but memory exceeds the 500 MB threshold. No other long-running Node process crossed the review thresholds.
- Watchdog/config: watchdog loaded; gateway `ThrottleInterval=10`; watchdog `StartInterval=600`. The watchdog plist has no separate `ThrottleInterval`, which is acceptable with the 600-second start interval.
- Version: installed **2026.8.1**. Official docs identify 2026.8.1 as the current release; no verified newer version was found. No update was attempted.
- Plugins: `context-mode@context-mode=false`. Extensions contain only `.openclaw-install-backups`; no unexpected active extension found.
- Integrity: mistakes log, watchdog script, health database, and pending JSONL all exist/read/parse.
- Backup signal: `openclaw status` reports the last archive backup was **12 days ago**, which is stale enough to investigate.

## Weekly Maintenance

- Autoresearch: **no enrollment**. Only 11 backup copies (`SKILL.md.bak`) changed in the last seven days; no new repeated, scoreable skill/agent qualified.
- Future signals: **none graduated**. All active triggers remain unmet or frozen under the 90 Day Playbook.
- Passive-income queue: Mission Control returned **0** todo tasks titled `Build idea:` or `[PI]` with `sortOrder >= 500`; nothing pruned or promoted.
- Skill collection cleanup: moved 11 stale `.bak` copies (48,089 bytes) from `skills/` to Trash. This was recoverable, but a fresh review still reported **273,999 bytes**, proving the cap is based on active `SKILL.md` content rather than backups.
- Cost review: seven-day spend **$0.00**; monthly pace **$1.02**; **$48.98** headroom.
- Monthly prompt ritual: not due (Sep 13 is not the first Sunday); Sep 7 proposals remain staged and uninstalled.

## Issues Fixed This Run

- Removed 11 stale, recoverable `.bak` files from the writable skills tree. This reduced disk clutter but did not clear the active-skill review limit.
- Updated the existing high-priority Mission Control remediation task with current evidence and the Sep 14 post-reset validation gate.

## Needs JT Attention

1. Approve a bounded compaction of `AGENTS.md` below 28,000 bytes and active skills below 240,000 bytes. The active skill collection needs at least **34 KB** removed or extracted; backups were not the cause.
2. Verify the first natural Friday Scoreboard run after the Sep 14 subscription reset. Do not change model/provider routing without approval.
3. Diagnose sustained gateway RSS (~974 MB) and the stale 12-day archive backup in an approved maintenance window.
4. Restore canonical root `TOOLS.md`/`HEARTBEAT.md` routing or update the bootstrap contract to their actual locations.
5. Rotate `memory/weekly-recaps/current-week.md`; its header is still `Week of 2026-08-24`.

## Grade

**C+** — gateway, watchdog, core integrity, version, and most deliveries are healthy, but two red jobs, oversized bootstrap/skill surfaces, high gateway RSS, stale backup state, and missing root routing files block an A-level result.

Next review: 2026-09-20.
