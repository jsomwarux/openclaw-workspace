# Nightly Leverage Anti-Repeat Audit — 2026-05-29

## Finding
JT's read was correct. The Nightly Leverage Agent was directionally aligned with the North Star, but not optimized enough. Recent runs were not exact duplicates, but they clustered around the same Altmark rent-delinquency gate:

- 2026-05-23: Altmark acceptance/access/payment closeout and referral gate.
- 2026-05-27: DHCR delivery assets, explicitly parked behind rent delinquency.
- 2026-05-27 night: rent-delinquency testing pack and sample-report gate.
- 2026-05-28: synthetic smoke-test sheet.
- 2026-05-29: redacted real-export/reviewer/exception-rules gate.

The work advanced the client lane, but the nightly loop treated adjacent prep artifacts as fresh progress even when the actual next move still required JT/client input.

## Root Cause
The prompt weighted active revenue/client delivery correctly, but it lacked:

- a definition of material progress
- a same-blocker cooldown
- a rule for "blocked by JT/client input"
- a rotation path to self-serve work after repeated nights on the same blocker
- a required report field proving tonight's work changed something versus the last two runs

## Optimal Behavior
The agent should still prioritize Altmark when new evidence/input exists. It should not manufacture another artifact when the blocker is unchanged.

Material progress means one of:

- new client/JT/source input arrived
- verification produced new pass/fail evidence
- a task can be closed, corrected, or repointed because reality changed
- a deliverable exists that changes tomorrow's action, not just restates it
- a different self-serve North Star lane advanced after the top blocker stalled

Not material:

- another checklist/request for the same missing client input
- cosmetic note/task updates
- repeating the same "tomorrow ask"
- creating another runbook when the next action is unchanged
- full Nightly Leverage Report without a clear delta from the last two nightly runs

## Implemented Change
Patched live cron `003191af-45a7-4e3b-a824-f7a6cd52f8c7` / `nightly-autonomous-leverage-agent` with:

- required last-7-days nightly scan before action
- material-progress gate before writes/reports
- two-night same-blocker cooldown
- blocked-by-JT/client behavior
- self-serve rotation order
- mandatory `Material delta` in full reports
- "no full report" behavior when no material work is available

## Second-Pass Hardening
Follow-up audit found the cron prompt was strong, but the morning review path only referenced regression checks generally. `docs/agents/heartbeat-extended-rules.md` now explicitly requires 10AM film review to validate any Nightly Leverage Report for either a concrete `Material delta` versus the prior two nightly runs or `NO_ACTION_NEEDED`, and to patch the cron if the same blocker repeats without new input/evidence.
