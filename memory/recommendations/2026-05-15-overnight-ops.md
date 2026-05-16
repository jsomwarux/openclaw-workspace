# 2026-05-15 Overnight Ops Recommendation

## Finding
Cron health is broadly clean, but `openclaw cron list` renders the Health Check-in delivery target as `telegram:telegram:6608544825` while status remains `ok`.

## Risk
Low current risk because delivery/status is OK, but the duplicated provider prefix is config drift. If the delivery resolver tightens validation later, this could become a silent check-in delivery failure.

## Recommended follow-up
During daytime maintenance, inspect the Health Check-in cron delivery config and normalize the target to a single Telegram recipient format. Do not edit overnight unless delivery fails.

## Evidence
Observed in `openclaw cron list` on 2026-05-15 03:00 ET:
`Health Check-in (Patt...) ... ok ... announce -> telegram:telegram:6608544825`
