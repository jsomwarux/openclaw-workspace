# Daily Send Sheet Reconciliation Claim - 2026-07-17

## Claim
Daily Send Sheet data surfaces have been reconciled to the July 16 state without cron schedule or cron payload edits.

## Required Current State
- `memory/send-queue.md` MSI item points to `memory/clients/marketsmith/kickoff-invoice-action-2026-07-17.md`.
- MSI next action says: `Invoice MSI kickoff - $5,400 (50% of $10,800 signed; terms set: 50% kickoff / 50% completion).`
- `memory/pipeline.jsonl` MSI record has the same kickoff invoice action and source artifact.
- `memory/clients/marketsmith/kickoff-invoice-action-2026-07-17.md` exists and states proposal packet is obsolete for Daily Send Sheet routing.
- `memory/clients/marketsmith/fixed-fee-proposal-send-packet-2026-07-15.md` is marked obsolete for Daily Send Sheet routing.
- `memory/pipeline-backlog.md` marks Petri, HPM, and Superior as BENCHED until 2026-08-01.
- Mission Control marks Petri, HPM, Superior, and the HPM/Superior bundle as `snoozed`, low priority, and `benched_until_2026-08-01`.
- Mission Control MSI task is `kickoff_invoice_due`.
- Mission Control DHCR task is `client_deposit_chase`.
- `eve_mandate_jul2026.md` already agrees with MSI signed active delivery, benched Watchdog/Outbound v2, frozen offer menu, and DHCR/Ron-Yair separation; no mandate rewrite performed.

## Verifier Command
Run:

```bash
python3 - <<'PY'
import json
import subprocess
from pathlib import Path

root = Path('/Users/jtsomwaru/.openclaw/workspace')
errors = []

send_queue = (root / 'memory/send-queue.md').read_text()
pipeline = [json.loads(line) for line in (root / 'memory/pipeline.jsonl').read_text().splitlines() if line.strip()]
backlog = (root / 'memory/pipeline-backlog.md').read_text()
invoice = (root / 'memory/clients/marketsmith/kickoff-invoice-action-2026-07-17.md').read_text()
proposal = (root / 'memory/clients/marketsmith/fixed-fee-proposal-send-packet-2026-07-15.md').read_text()
mandate = (root / 'eve_mandate_jul2026.md').read_text()

needle = 'Invoice MSI kickoff - $5,400 (50% of $10,800 signed; terms set: 50% kickoff / 50% completion).'
if needle not in send_queue:
    errors.append('send-queue missing MSI invoice action')
if 'memory/clients/marketsmith/kickoff-invoice-action-2026-07-17.md' not in send_queue:
    errors.append('send-queue missing MSI kickoff invoice source')
msi = next((r for r in pipeline if r.get('name') == 'MSI engagement'), None)
if not msi or msi.get('next_action') != needle:
    errors.append('pipeline MSI next_action mismatch')
if not msi or msi.get('source') != 'memory/clients/marketsmith/kickoff-invoice-action-2026-07-17.md':
    errors.append('pipeline MSI source mismatch')
if 'Proposal packet is obsolete for Daily Send Sheet routing' not in invoice:
    errors.append('invoice artifact missing obsolete proposal guard')
if 'OBSOLETE FOR DAILY SEND SHEET ROUTING' not in proposal:
    errors.append('old proposal packet not marked obsolete')
for name in ['Petri Plumbing', 'HPM / Harlem Property Management', 'Superior Plumbing']:
    if name not in backlog or 'BENCHED' not in backlog:
        errors.append(f'backlog missing benched row for {name}')
for required in [
    'MSI / Marketsmith: SIGNED',
    'Outbound v2 | BENCHED -> AUGUST',
    'Production Support',
    'Watchdog',
    'DHCR decision chase to Matt (start-slot frame). Keep distinct from any Ron/Yair partnership talk.',
]:
    if required not in mandate:
        errors.append(f'mandate missing expected line: {required}')

tasks = subprocess.check_output(['curl','-fsS','http://localhost:3000/api/tasks'], text=True)
tasks = json.loads(tasks)['tasks']
by_title = {t['title']: t for t in tasks}
expected_snoozed = [
    'BENCHED until Aug 1: Petri Plumbing M2',
    'BENCHED until Aug 1: HPM M2',
    'BENCHED until Aug 1: Superior Plumbing M2',
    'BENCHED until Aug 1: HPM/Superior M2 bundle',
]
for title in expected_snoozed:
    task = by_title.get(title)
    if not task:
        errors.append(f'MC missing {title}')
    elif task.get('status') != 'snoozed' or task.get('pipelineStage') != 'benched_until_2026-08-01':
        errors.append(f'MC not benched: {title}')
msi_task = by_title.get('MSI: invoice kickoff $5,400 and start signed delivery')
if not msi_task or msi_task.get('pipelineStage') != 'kickoff_invoice_due':
    errors.append('MC MSI task not kickoff_invoice_due')
dhcr = by_title.get('Altmark DHCR: collect kickoff inputs after rent delinquency gate')
if not dhcr or dhcr.get('pipelineStage') != 'client_deposit_chase':
    errors.append('MC DHCR task not client_deposit_chase')

if errors:
    print('VERDICT: NOT CONFIRMED')
    for e in errors:
        print('-', e)
    raise SystemExit(1)
print('VERDICT: CONFIRMED')
PY
```

## Verifier Verdict
- CONFIRMED — 2026-07-17 fresh deterministic verifier.
