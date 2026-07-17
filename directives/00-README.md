# Eve Standing Directive Pack: July 2026

Installed 2026-07-06 after JT's Stage 1 and Stage 2 sign-off. Source audit evidence: config/cron-snapshots/jobs-2026-07-05.json, memory/audits/weekly-systems/2026-07-05-weekly-systems-review.md, proofs/, reports/cron-audit/2026-06-12-active-cron-audit-proposal.md.

Precedence: eve_mandate_jul2026.md first, these directives second, individual job prompts third. A job prompt can never relax a directive.

The pack:
1. 01-evidence-contract.md
2. 02-builder-never-grades.md
3. 03-action-classes.md
4. 04-state-file-discipline.md
5. 05-repeat-offender-digest.md

## Approved registry, 12 recurring jobs (Engine B Stage 1 idea engine kept; marketing Stage 3 rebuild pending)

| Job | Schedule | Class | Ping |
|---|---|---|---|
| Daily Send Sheet (rewritten Morning Brief) | 30 7 * * * | green | yes, 1/day |
| outreach-pipeline | 0 3 * * * | green run, yellow outputs | no |
| Pending Task Processor | 30 10,18 * * * | green plumbing | no |
| prospect-discovery | 0 23 * * 0 | green | no |
| Friday Scoreboard (new, replaces 3 jobs) | 0 16 * * 5 | green | yes, 1/week |
| Weekly Systems Review | 0 10 * * 0 | green, fixes yellow | only if red |
| weekly-unemployment-cert | 0 7 * * 0 | green reminder | yes, 1/week |
| Health Check-in (Pattern-Focused) | 0 21 * * * | green | yes, 1/day |
| Passive Income idea engine: fetch-signals, scout, strategist, delivery-guard (Engine B Stage 1) | weekly now, monthly after Engine B rewrite | green run, yellow build-recs | no |

One-shot reminders remain allowed. Everything else is disabled.

## What never counts as progress

1. Drafts created, routed to Drive, or review-ready.
2. Mission Control tasks created, updated, repointed, or closed.
3. Voice-guard scores and re-verification of already verified things.
4. Reports, syntheses, audits, or memos written, including the weekly review itself.
5. Asset counts of any kind.
6. Registering, logging, or snapshotting things into Eve's own memory or registry.
7. Fallback-only runs presented as completed runs.
8. Any claim without a pasted artifact.

Progress is only: a send JT executed from the queue, a reply or meeting or dollar that came back, a pipeline stage movement, a gate or kill window caught on its date, and a verified deletion from Eve's own registry.

## Daily Send Sheet format, one message, 7:30

```
EVE DAILY - <day> <date>
SENDS DUE (max 3)
1. <name> - <action> - draft: <path> - reply: send / edit / skip
GATES <=48H
1. <gate and when it closes>
STALE >=7 DAYS
1. <thread> - <days> - staged chase attached
YESTERDAY
Sends confirmed: <n with artifact>. Unconfirmed items listed as NOT SENT.
CASH
$<collected> MTD. $<gap> to $10K. <n> days left.
```

Nothing due means one line: "Nothing due today. Clock checked <time>." No news, intel, costs, workout, or app sections. Mandate section 6 escalations may interrupt any time. Nothing else does.

## Friday Scoreboard format, one message, Friday 16:00

```
EVE SCOREBOARD - week ending <date>
1. Cash collected month-to-date vs $10K.
2. Altmark ladder position: inputs / deployed / accepted / invoiced / paid.
3. MSI stage: kickoff / milestone n / invoiced / collected.
4. Asks sent and packets forwarded, with follow-up aging (target: 0 threads stale past 7 days).
5. Qualified calls held and audits/builds signed.
6. Exceptions.
```

Vanity metrics to never report: LinkedIn impressions/reactions, follower counts, link views without a reply, app downloads, anything crypto, and count of assets/documents produced.

## Disable list, 33 jobs

Refused scope, 12: Crypto Full Analysis (6 AM), Crypto Midday Pulse (12 PM), Crypto Evening Pulse (9 PM), Job Market Daily Research, Job Application Auto-Builder, Job Application Tracker, ReelFarm Daily Strategy Intel, ReelFarm Weekly Strategy Synthesis, TikTok App Account Warm-up Reminder (2 PM), app-marketing-weekly-scoreboard, vibe-marketing-generate, guyana-economic-opportunity-monitor.

KEEP correction, not disable: passive-income-fetch-signals, passive-income-scout, passive-income-strategist, passive-income-strategist-delivery-guard are Engine B Stage 1, the idea engine JT values. Earlier drafts of this list wrongly filed them under refused scope. Corrected 2026-07-08.

Reading not sends, 9: Niche Intelligence Monitor, Daily News Hook, Viral Post Swipe File - X Research, Autoresearch Sweep, Skills & API Researcher - Daily Scan, Skills & API Researcher - Weekly Synthesis, Evening Digest, Monthly Goal-Skills Gap Analysis, Monthly Niche Fitness Review.

Killed pending marketing rebuild, 6: content-generate-linkedin, content-generate-x, content-sunday, content-reminder, AI Ops Teardown Weekly Draft, Night Autonomy Agent (personal-brand content folds into the rebuilt marketing agent, not a content batch).
Merged into survivors, 6: Weekly North Star Command Center, Weekly Strategic Gut-Check, Weekly Intelligence Synthesis (all three into Friday Scoreboard); outreach-email-pivot-daily (into outreach-pipeline); critical-files-integrity, Weekly Health Report (both into Weekly Systems Review).

## Install checklist, on the Mini

1. Sync this repo into ~/.openclaw/workspace.
2. One batch registry edit, JT keyword on the diff: disable the 33 jobs above, set Pending Task Processor to 30 10,18 * * *, set prospect-discovery to 0 23 * * 0.
3. Rewrite the Morning Brief payload to the Daily Send Sheet format above and rename the job Daily Send Sheet. Remove the Nash probe and every non-send section.
4. Create the replacement job: Friday Scoreboard at 0 16 * * 5 with announce delivery. No marketing cron is created. The marketing agent is being rebuilt and stays off until JT approves the new strategy.
5. Create memory/job-state/ with claims/ and archive/ subfolders and one state file per surviving job from TEMPLATE.md.
6. Point the HEARTBEAT.md idempotency and dedup rules at Directive 4.
7. Do not append to AGENTS.md until it is trimmed below budget. After the trim add one line: "Standing directives live in directives/. Read 00-README.md first."
8. First Friday run 2026-07-10 produces the first scoreboard and the first repeat-offender digest.
