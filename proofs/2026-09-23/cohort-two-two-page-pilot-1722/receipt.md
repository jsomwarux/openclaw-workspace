# Cohort-Two Controlled Two-Page Pilot — Execution 1722

- **Date:** 2026-09-23
- **Authorization:** one controlled cohort-two two-page pilot; public-source GETs and configured Anthropic calls allowed; local artifacts and normal cursor/ledger updates allowed; exactly-five all-or-nothing; all downstream capabilities disabled.
- **Deployed source:** `n8n-agent@41ef3bfb49dd6a0579377355cc5d0af7ce442093`
- **Workflow:** `c2discoveryMAIN1` (`cohort-two-prospect-discovery`)
- **Execution:** `1722`
- **Run ID:** `01M380N5W8HQE6BT7HP9NG6A58`

## Verified result

- Launcher exit: `0`; n8n execution status: `success`; terminal node: `N44 Run Complete`.
- Two-page planner emitted exactly two offsets: `800` and `1200`.
- N07 returned `400 + 400 = 800` registration rows.
- N07B emitted four 200-registration contact chunks; N08 returned four envelopes.
- N09 resolved nine organizations; every organization was skipped as `recheck-not-due`.
- N09F emitted zero fetchable candidates; no Anthropic call occurred.
- Exactly-five contract held: `0 of 5`, no partial cohort, no review packet, no Mission Control post.
- Cursor advanced `800 -> 1600`; discovery ledger remained nine entries; carryover remained empty.
- Both workflows remained inactive. Weekly schedule, Mission Control post, heartbeat, suppression, drafting, activation, and send paths remained disabled. The workflow contains zero send-capable nodes.

## Artifacts

- Run receipt: `/Users/jtsomwaru/projects/n8n-agent/clients/cohort-two-discovery/out/01M380N5W8HQE6BT7HP9NG6A58/run-receipt.json`
- Complete marker: `/Users/jtsomwaru/projects/n8n-agent/clients/cohort-two-discovery/out/01M380N5W8HQE6BT7HP9NG6A58/COMPLETE.json`
- Short-cohort report: `/Users/jtsomwaru/projects/n8n-agent/clients/cohort-two-discovery/out/01M380N5W8HQE6BT7HP9NG6A58/short-cohort-report.md`

## Evidence-based branch

The sparse-frame defect is closed: two consecutive pages were fetched and combined atomically. The active blocker is the prospect universe. The seed roster contains exactly nine organizations, and the discovery ledger currently holds all nine under recheck windows. The two earliest rechecks are 2026-09-30, which is still below the required cohort size of five. Another blind frame is not authorized or useful.

The generated, unposted empty-run Mission Control payload also contains a stale first action pointing to a nonexistent `review-packet.md`; correct that wording when the prospect-universe change is implemented.
