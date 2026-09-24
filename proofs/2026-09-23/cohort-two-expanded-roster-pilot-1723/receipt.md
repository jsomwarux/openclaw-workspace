# Cohort-Two Expanded-Roster Pilot — Execution 1723

- **Authorization:** one controlled cohort-two expanded-roster pilot.
- **Deployed source:** `n8n-agent@7863deee563406d96b6c508ad17777655d4bab57`
- **Workflow:** `c2discoveryMAIN1` (`cohort-two-prospect-discovery`), inactive.
- **Execution:** `1723`
- **Result:** failed closed at `N04 Read Contact Universe`; no retry was attempted.

## Root cause

N03 derived `run.as_of` by slicing the UTC `started_at` timestamp. The execution began at `2026-09-24T02:11:12Z`, which was still September 23 in the workflow's configured `America/New_York` timezone. N03 therefore requested:

`/Users/jtsomwaru/.openclaw/workspace/reports/outreach-pipeline/2026-09-24-script-first-preflight.json`

The exclusion producer had freshly generated the correct New York business-day artifact:

`/Users/jtsomwaru/.openclaw/workspace/reports/outreach-pipeline/2026-09-23-script-first-preflight.json`

The workflow correctly refused the missing path rather than continuing without exclusions.

## Safety evidence

- Launcher initialized the reviewed n8n 2.14.1 license provider, then exited `1` after the workflow error.
- Failure occurred before public prospect research or any Anthropic request.
- No output directory or cohort artifact was created.
- State remained unchanged:
  - cursor offset: `1600`; SHA-256 `fb5c296549799bcea956fcde4cef65932bfd04af1727f6b9096a527a8ad99bcf`
  - ledger entries: `9`; SHA-256 `4dad929d1c32ecf2822e35a8cbccea81728cd65a47306e7f90f48b6f30d6fde9`
  - carryover prospects: `0`; SHA-256 `194a56458599ea6796aa460b26114cd26bfb171afc40798b20b4e49cc4759552`
- Both workflows remain inactive and contain zero send-capable nodes.
- Weekly schedule, Mission Control post, and heartbeat post remain disabled.

## Required repair

Make `run.as_of` and `contact_universe_path` use the workflow's New York business date rather than the UTC calendar date, with boundary tests on both sides of New York midnight. Preserve `started_at` as UTC and preserve the fail-closed same-business-day exclusion check.

