# XHigh Systems Audit — Crypto Allocation X Research Hardening

Date: 2026-05-14
Auditor: Eve subagent, isolated xhigh systems audit
Scope: `/Users/jtsomwaru/projects/crypto-agent` allocation system after 2026-05-14 X-research hardening
Safety: Read-only first; no trades, transfers, wallet actions, or external messages. Small reversible patches only.

## Executive Summary

The 2026-05-14 6AM crypto run delivered an allocation while explicitly logging that X searches were skipped for cost. That was a real systems failure because X is the real-time coordination layer for these microcap/narrative allocations.

The post-run hardening materially improved the system: `run-x-research.py`, `x-research-guard.py`, `CLAUDE.md`, `config/settings.yaml`, and the `eve-crypto-morning-008` cron payload now hard-require fresh X coverage before allocation delivery.

I patched two remaining A+ blockers:
1. `x-research-guard.py` now validates freshness from embedded per-entry `ran_at_utc` timestamps, not mutable file mtime.
2. `run-x-research.py` now parses and reports estimated X API cost from CLI output for future runs.
3. `eve-crypto-morning-008` cron final response contract now requires `x_research_guard_passed`, `x_research_entries`, and `x_research_estimated_cost_usd`; omission is explicitly incomplete.

Current assessment: **before hardening: C-**. **After my patches: A- system design / pending A validation on the next scheduled run**.

## Grade Before / After

| Category | Before 2026-05-14 hardening | After main hardening + this audit patch | Notes |
|---|---:|---:|---|
| Mandatory X coverage | D | A | Before: cost could override X. After: full cron payload requires `run-x-research.py` + `x-research-guard.py` before scoring and again before send. |
| X result quality / noise control | C+ | A- | Uses narrative query, full portfolio/watchlist, `--quick --limit 5`, likes sort, and noise exclusions for airdrop/giveaway/scanner/retweet/reply spam. Remaining gap: ticker-only searches can still catch unrelated cashtag spam. |
| Stale / failure blocking | C- | A | Guard now blocks missing JSON, invalid JSON, command failures, missing portfolio coverage, and stale embedded run timestamps. |
| Allocation incorporation | D | B+ pending proof | Cron/CLAUDE require incorporation into narrative, coordination, virality, phase, alpha, final allocation. But the current `latest-analysis.md` is still the 6AM pre-hardening allocation that skipped X. Need tomorrow's run to prove incorporation. |
| Delivery verification | B | A- | Cron payload requires explicit `message` tool send, not cron announce delivery. Latest 05-14 cron log shows `delivered: true`, `deliveryStatus: not-requested` because delivery mode is none and explicit message tool sent. |
| Cost discipline | B- | A- | Cost discipline now reduces depth, not coverage. Script will report estimated X API cost on future runs. Existing 07:35 X JSON predates this field, so cost summary appears next run. |
| Maintainability | B | A- | Dedicated scripts, config settings, and cron payload are clear. Remaining maintainability gap: scripts are currently untracked in git (`?? scripts/run-x-research.py`, `?? scripts/x-research-guard.py`). |

## Files Inspected

- `/Users/jtsomwaru/projects/crypto-agent/CLAUDE.md`
- `/Users/jtsomwaru/projects/crypto-agent/config/settings.yaml`
- `/Users/jtsomwaru/projects/crypto-agent/scripts/run-x-research.py`
- `/Users/jtsomwaru/projects/crypto-agent/scripts/x-research-guard.py`
- `/Users/jtsomwaru/projects/crypto-agent/data/x-research-latest.md`
- `/Users/jtsomwaru/projects/crypto-agent/data/x-research-latest.json`
- `/Users/jtsomwaru/projects/crypto-agent/data/cost-log.md`
- `/Users/jtsomwaru/projects/crypto-agent/data/latest-analysis.md`
- `/Users/jtsomwaru/projects/crypto-agent/data/telegram-summary.txt`
- `/Users/jtsomwaru/.openclaw/cron/jobs.json` via `openclaw cron show` / targeted JSON inspection for `eve-crypto-morning-008`
- Latest `eve-crypto-morning-008` run history via `openclaw cron runs --id eve-crypto-morning-008 --limit 1`

## Files Changed

- `/Users/jtsomwaru/projects/crypto-agent/scripts/run-x-research.py`
  - Added `estimate_cost_usd()` parser for x-search CLI `~$...` cost markers.
  - Adds `estimated_cost_usd` per result in future `x-research-latest.json` writes.
  - Adds `Estimated X API cost` to future `x-research-latest.md` summaries.
  - Adds `estimated_x_api_cost_usd` to script stdout JSON.

- `/Users/jtsomwaru/projects/crypto-agent/scripts/x-research-guard.py`
  - Added ISO timestamp parser for `ran_at_utc`.
  - Freshness now uses embedded per-entry run timestamps instead of file mtime.
  - Blocks entries missing valid `ran_at_utc`.

- `eve-crypto-morning-008` cron payload in `/Users/jtsomwaru/.openclaw/cron/jobs.json` via `openclaw cron edit`
  - Final response contract now requires exact fields: `x_research_guard_passed`, `x_research_entries`, `x_research_estimated_cost_usd`.
  - Adds explicit incomplete-run language if those fields are omitted.

## Current Evidence

### Latest X research artifact

- `data/x-research-latest.json` exists, size ~44KB.
- 20 entries: 19 current portfolio/watchlist coins + `__NARRATIVE__`.
- Guard passes current freshness/coverage.
- Missing coverage: none.
- Zero-result tickers: `$PRXVT`, `$A0T` — acceptable as signal, not a command failure.
- Existing JSON was generated before my cost parser patch, so it does not yet contain `estimated_cost_usd`. Future runs will.

### Latest 05-14 6AM allocation artifact

- `data/cost-log.md` explicitly says: `X searches: skipped in this pass to preserve cost after live Dexscreener + whale refresh.`
- `data/latest-analysis.md` and `data/telegram-summary.txt` are therefore pre-hardening allocation artifacts, even though fresh X research exists later at 07:35.
- The next scheduled `eve-crypto-morning-008` run is the real validation point for allocation incorporation.

### Cron payload

Current cron payload includes:
- `CRITICAL X RESEARCH GATE`
- `run-x-research.py --since 1d --limit 5`
- `x-research-guard.py --max-age-hours 3`
- “Do not skip it for cost control.”
- “If X research fails/stales/misses coverage, DO NOT deliver allocation.”
- Final response fields: `x_research_guard_passed`, `x_research_entries`, `x_research_estimated_cost_usd`.

## Verification Commands / Results

### Bootstrap budget check

```bash
wc -c AGENTS.md MEMORY.md TOOLS.md HEARTBEAT.md
```

Result:
- `AGENTS.md`: 27013
- `MEMORY.md`: 19541
- `TOOLS.md`: 14776
- `HEARTBEAT.md`: 15578

All under hard caps.

### Python syntax check

```bash
cd /Users/jtsomwaru/projects/crypto-agent
python3 -m py_compile scripts/run-x-research.py scripts/x-research-guard.py
```

Result: passed.

### Live guard check

```bash
python3 scripts/x-research-guard.py --max-age-hours 3
```

Result:

```text
OK: fresh X research verified — entries=20, age_hours=0.97, portfolio_covered=20/20
```

### Cost parser unit check

```bash
python3 - <<'PY'
import importlib.util
spec=importlib.util.spec_from_file_location('rx','scripts/run-x-research.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
print('cost_parser_ok', mod.estimate_cost_usd('quick (~$0.0500) plus (~$0.0100)') == 0.06)
PY
```

Result:

```text
cost_parser_ok True
```

### Stale embedded timestamp negative test

```bash
# Created temporary x-research JSON with all ran_at_utc values set to 2000-01-01T00:00:00+00:00
python3 scripts/.x-research-guard-test.py --max-age-hours 3
```

Result:

```text
FAIL: X research stale by embedded run timestamp: 231132.50h old > 3.0h
OK: stale embedded timestamp is blocked with rc=2
```

### Coverage check

```bash
python3 - <<'PY'
import json
portfolio=json.load(open('data/portfolio.json')).get('coins',[])
expected={c.get('ticker') for c in portfolio if c.get('ticker')}
expected.add('__NARRATIVE__')
x=json.load(open('data/x-research-latest.json'))
seen={r.get('ticker') for r in x}
print('portfolio_coins', len(portfolio))
print('expected_entries', len(expected))
print('x_entries', len(x))
print('missing', sorted(expected-seen))
print('extra', sorted(seen-expected))
PY
```

Result:

```text
portfolio_coins 19
expected_entries 20
x_entries 20
missing []
extra []
```

### Cron payload verification

```bash
python3 - <<'PY'
import json
from pathlib import Path
p=Path('/Users/jtsomwaru/.openclaw/cron/jobs.json')
d=json.load(open(p))
jobs=d.get('jobs', d if isinstance(d,list) else [])
if isinstance(jobs, dict): jobs=list(jobs.values())
job=next(j for j in jobs if j.get('id')=='eve-crypto-morning-008')
msg=job['payload']['message']
for phrase in ['CRITICAL X RESEARCH GATE','x_research_guard_passed','x_research_entries','x_research_estimated_cost_usd','If you omit x_research_guard_passed']:
    print(phrase, phrase in msg)
print('timeoutSeconds', job['payload'].get('timeoutSeconds'))
print('delivery_mode', job.get('delivery',{}).get('mode'))
PY
```

Result:

```text
CRITICAL X RESEARCH GATE True
x_research_guard_passed True
x_research_entries True
x_research_estimated_cost_usd True
If you omit x_research_guard_passed True
timeoutSeconds 1200
delivery_mode none
```

### Latest cron run check

```bash
openclaw cron runs --id eve-crypto-morning-008 --limit 1
```

Selected result:

```text
status ok
runAtMs 1778752800026
durationMs 584083
model gpt-5.5
provider openai-codex
delivered True
deliveryStatus not-requested
summary_has_guard_field False
```

Interpretation: this was the pre-patch 05-14 run. It sent via explicit message tool but omitted `x_research_guard_passed`; cron payload now blocks that omission in future final responses.

## Remaining A+ Blockers

1. **Next-run proof required.** The system is now designed correctly, but the current `latest-analysis.md` is still the 6AM artifact that skipped X. Need the next 6AM run to prove X data is actually incorporated into scoring/allocation.

2. **Ticker-only searches can still be noisy.** Noise filters are good, but cashtag-only searches can catch unrelated spam. A+ quality would add project-name/website/handle disambiguation when available from `portfolio.json` or coin-intelligence files.

3. **Scripts are untracked.** `git status --short scripts/run-x-research.py scripts/x-research-guard.py` reports both as untracked. If crypto-agent is meant to be version controlled, these should be committed or intentionally ignored; otherwise the hardening can be lost.

4. **Existing X JSON lacks new cost fields.** This is expected because the artifact predates my patch. Future `run-x-research.py` runs will include cost fields.

## Recommendation for JT-facing Summary

“Caught and hardened the crypto allocation failure mode. Yesterday’s allocation did ship without X because cost discipline overrode research quality. That path is now closed: the 6AM cron must run fresh X across the full universe, pass a guard before scoring and again before sending, and report X guard/cost fields in its final output. I also patched the guard so stale files can’t pass by mtime and added X cost reporting. Current grade moved from C- to A-, pending tomorrow’s run proving the allocation actually incorporates the fresh X signal.”
