# Outreach Pipeline Script-First Preflight - 2026-06-08

Dry run: True
Prospects scanned: 58
Canonical Drive names loaded: 53

## Stage Results
- PASS: source_file_preflight - required files present
- PASS: drive_auth_preflight - Drive auth ok; Eve Drafts root visible.
- PASS: canonical_drive_names - 53 canonical names loaded
- PASS: prospect_scan - 58 client folders scanned

## Decision Summary
- skip: 57
- warm_up_only: 1

## Copy Review Queue
- HealthPass — Warm-up (`healthpass`): warm_up_only - Warm-up draft exists; do not create full outreach until warmed.

## Safety Notes
- This runner does not send outreach.
- This runner does not create public profiles or external messages.
- LLM copy generation should only run after this report identifies an eligible copy-review item.
