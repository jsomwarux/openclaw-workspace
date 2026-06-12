#!/usr/bin/env python3
"""Apply Phase 6 bootstrap reduction and cron default-model cleanup."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path


ROOT = Path("/Users/jtsomwaru/.openclaw/workspace")
MEMORY = ROOT / "MEMORY.md"
MEMORY_FULL = ROOT / "docs/memory/MEMORY-full.md"
TOOLS = ROOT / "TOOLS.md"
TOOLS_FULL = ROOT / "docs/tools/TOOLS-full.md"
AGENTS = ROOT / "AGENTS.md"
JOBS = Path("/Users/jtsomwaru/.openclaw/cron/jobs.json")


MEMORY_INDEX = """# MEMORY.md - Current Operating Context Index
> Main-session long-term context. Do NOT load in group/shared chats.
> Full detail: `docs/memory/MEMORY-full.md` under `Current Operating Context Relocated From MEMORY.md - 2026-06-11 Phase 6`.
> Compact file: current facts and pointers only; history belongs in daily notes/archive.

## JT Snapshot
- JT Somwaru, America/New_York, Telegram primary; direct and low-ceremony.
- Background edge: business systems/product-catalog ops plus AI implementation translation.
- North Star: financial freedom through high-earning, low-maintenance streams; priorities are consulting, apps/marketing, crypto, then health.
- Constraints: no relocation, protect sleep/health/NYC stability, no developer-only positioning.
- Detail: `docs/memory/MEMORY-full.md#jt-snapshot`.

## Hard Rules / Security Essentials
- Do not modify auth/model config, OpenClaw updates, sacred files, or credentials without explicit approval.
- Never expose/store API keys outside approved auth/env homes; redact shareable artifacts.
- Never send third-party outreach for JT; draft and sync only.
- Preflight compaction failures are report-only: no config edits, restarts, or deletes.
- Detail: `docs/memory/MEMORY-full.md#hard-rules--security-essentials`.

## Consulting Positioning
- Positioning: practical AI implementation for ops-heavy SMBs, focused on outcomes and governed handoffs.
- Best lane: AI operating controls / agent-ready operating models before automation.
- ICP: NYC/metro SMBs in property ops, construction, wholesale distribution, and skilled trades; HubSpot and Salesforce/Agentforce fit when stack and ownership are clear.
- Outreach tiers remain T1 proof-led, T2 validation/template, T3 market-sensing only.
- Detail: `docs/memory/MEMORY-full.md#consulting-positioning`.

## Active Clients
- Altmark is the top paid/proof lane; rent delinquency workflow is the current acceptance/revenue gate.
- Aya remains anchor proof history: dashboard done, StreetEasy scraper active, co-living dashboard pending, acquisitions stalled.
- Client proof must stay privacy-safe until acceptance, metrics, screenshots, and permission/anonymization are verified.
- Detail: `docs/memory/MEMORY-full.md#active-clients`.

## Pipeline / Business Development
- Proof-led referrals/warm intros and buyer-channel validation beat generic LinkedIn warm-up.
- Outreach-ready prospects need LinkedIn URL plus verified email; JT sends every message.
- Guyana Summit is connector/operator validation; H.C. Oswald stays paused until site/demo proof improves.
- Consulting pipeline lives in `~/projects/jt-consulting-pipeline/`; sync deck/outreach through pipeline Drive tools.
- Detail: `docs/memory/MEMORY-full.md#pipeline--business-development`.

## Consulting Delivery / Niche Matrix
- New or active paid/discovery client work requires Client OS initialization and rigorous reusable-IP capture.
- Services-as-software delivery means manual proof, edge cases, failure modes, and metrics before automation.
- Current delivery focus: property ops first, construction/skilled trades second, Agentforce when Salesforce readiness is real.
- Detail: `docs/memory/MEMORY-full.md#consulting-delivery--niche-matrix`.

## Current Apps / Products
- `jtsomwaru.com` is the portfolio/proof hub; no untested public site work.
- Glow Index is live and in App Marketing OS; Nash Satoshi powers ranking/content proof; Vista is live with SEO pages.
- App marketing must stay proof/measurement driven and avoid unsupported claims.
- Detail: `docs/memory/MEMORY-full.md#current-apps--products`.

## Content System
- Read JT voice/corpus before drafting; first-person proof with verifiable specifics beats generic advice.
- Phase 3/4 completed: approved `memory/jt-corpus.md`, Sonnet content crons, edit-delta logging, guard wrapper, and $10/month content Sonnet cap.
- PM Front Desk + Exception Desk remains the current strongest proof asset path.
- Detail: `docs/memory/MEMORY-full.md#content-system`.

## Job Market
- Consulting-first, employment selective; only AI implementation/solutions lead roles near $150K+ NYC/remote are worth packages.
- Use job discoveries as market intel and consulting signals unless the fit is exceptional.
- Avoid Apex/SFDX-heavy developer, pure ML/research, relocation, or low-salary roles.
- Resume/cover-letter packages use the job-application skill and Sonnet.
- Detail: `docs/memory/MEMORY-full.md#job-market`.

## Crypto / Finance
- Crypto is JT's primary income stream; x402 is the forward bet.
- Never trade, transfer, spend, or execute financial transactions.
- Morning crypto/Nash ranking crons are operationally important and should be monitored through heartbeat rules.
- Detail: `docs/memory/MEMORY-full.md#crypto--finance`.

## Infrastructure / OpenClaw State
- Default route is OpenAI OAuth; non-default/premium model use needs named approval except approved Phase 4 content jobs.
- Phase 2A: audio autodetect enabled, LCM DB backed up/reset, Moonshot fallback skipped until billing is resolved.
- Phase 2B: watchdog/restart hardened, n8n and Mission Control Next loopback-bound, `/n8n` tailnet restored, requested secret artifacts redacted.
- Mission Control: `http://localhost:3000`; tailnet root `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n at `/n8n`.
- Detail: `docs/memory/MEMORY-full.md#infrastructure--openclaw-state`.

## Active Automation / Crons
- Phase 5 state: 54 enabled / 69 total before Phase 6 model cleanup; Morning Brief opens with capped Send Queue, Evening Digest runs 7PM ET.
- Digest queue: `memory/digest-queue.md`; reminder/FYI jobs append there instead of standalone Telegram.
- Cron volume guard remains required; avoid `deleteAfterRun: true`.
- Phase 6 removes default `openai/gpt-5.5` payload model overrides while preserving non-default overrides.
- Detail: `docs/memory/MEMORY-full.md#active-automation--crons`.

## Health / Training / Quality Loops
- Health DB/check-ins, cost tracker, proof guard, daily film review, and weekly skills audit remain active.
- Non-obvious solved problems become lessons in the relevant rule/skill/lesson file immediately.
- Same-day proof logging is required for substantive deliverables.
- Detail: `docs/memory/MEMORY-full.md#health--training--quality-loops`.

## Strategic Decisions Log
- Current strategy: contained SMB ops bottleneck audits/prototypes and B2B consultable proof over abstract AI advice.
- App-growth next moves: ChargeTrip Fit spec-first MVP, Nash conversion patch, Vista measurement/distribution loop.
- Future/deferred signals need explicit trigger conditions.
- Detail: `docs/memory/MEMORY-full.md#strategic-decisions-log`.

## Integrity / Fabrication Corrections
- Verify outreach, URLs, deployment, GitHub, Drive links, and task closure before claiming them.
- JT corrections require immediate Mistakes Log/rule updates with regression checks.
- Treat compacted recall as cues, not proof; expand before exact claims.
- Detail: `docs/memory/MEMORY-full.md#integrity--fabrication-corrections`.

## Setup State
- JT Operating System plugin/skills and workflow/product agents are installed; key paths live in TOOLS.
- GBrain consulting recall pilot is limited to entity lookup through the wrapper; no broad ingestion without approval.
- Drive, Mission Control, Tailscale, n8n, and core scripts remain canonical workspace infrastructure.
- Detail: `docs/memory/MEMORY-full.md#setup-state`.

## Automation / Live Opportunities
- Altmark rent delinquency is the top consulting/proof lane.
- Guyana wedge: Local Content Operations Sprint for oil/gas-adjacent suppliers; site page remains stale until rewritten.
- Nightly leverage, Guyana monitor, passive-income, North Star, App Marketing, ReelFarm, and related automations remain active unless cron list says otherwise.
- Detail: `docs/memory/MEMORY-full.md#automation--live-opportunities`.
"""


TOOLS_INDEX = """# TOOLS.md - Tool Reference
> Check this file before saying "I can't." Full command syntax lives in `docs/tools/TOOLS-full.md`.

## Health System
- DB: `health/health.sqlite`; daily 9PM check-in, Sunday 9AM report.
- Use `health/health.py` for log/report/history and `health/inbound_handler.py` for JT replies.
- Full syntax: `docs/tools/TOOLS-full.md#health-system`.

## Spanish Learning
- State: `spanish/state.json`; lessons: `spanish/lessons/YYYY-MM-DD.md`; cron `babd905a-1098-49dd-8700-772fef14f817`.
- Validate with `scripts/spanish_state_check.py`; delivery truth is the latest cron run deliveryStatus.
- Full syntax: `docs/tools/TOOLS-full.md#spanish-learning`.

## Cost Tracker
- Script: `scripts/cost-tracker.py`; common modes: snapshot, brief, check-alerts, weekly-review, check-runaway.
- `--diagnose` is not supported. Routing guard: `scripts/model_routing_guard.py --include-disabled`.
- Full syntax: `docs/tools/TOOLS-full.md#cost-tracker`.

## Audit Trail
- Proof log: `scripts/log-proof.py`; proof guard: `scripts/memory_recap_proof_guard.py`.
- Daily proof JSONL: `proofs/YYYY-MM-DD/actions.jsonl`.
- Full syntax: `docs/tools/TOOLS-full.md#audit-trail`.

## Restart / Gateway Recovery
- Approved restart path: `scripts/restart-gateway.sh "reason"`; no raw gateway restart unless explicitly approved.
- Gateway freeze/cooldown recovery details moved to full docs. Never raise `bootstrapMaxChars` above 32000.
- Full syntax: `docs/tools/TOOLS-full.md#restart-script` and `docs/tools/TOOLS-full.md#gateway-freeze--rate-limit-recovery`.

## Image / OCR
- OpenClaw image attachments require `sharp` in the OpenClaw node_modules tree.
- OCR fallback: Homebrew `tesseract`; full install/use notes in full docs.
- Full syntax: `docs/tools/TOOLS-full.md#image--ocr-tooling`.

## Diagnostics
- `openclaw doctor`; `openclaw doctor --fix` only when something is broken and root cause is unclear.

## Web / X Research
- Fresh web research: use `scripts/web_search.py` with freshness filters; do not use managed web_search for freshness/date filters.
- X research skill wrapper: `skills/x-research`; cheap default is quick limit 5.
- Full syntax: `docs/tools/TOOLS-full.md#canonical-web-search` and `docs/tools/TOOLS-full.md#x-research-skill`.

## Backups / Session Cleanup / Task Queue
- Backup script: `scripts/backup.sh`; cleanup script: `scripts/cleanup-sessions.py`.
- Task queue: `tasks/pending.jsonl`; every 2h 8AM-10PM ET.
- Full syntax: `docs/tools/TOOLS-full.md#backups`.

## Knowledge Base / Skills Scout
- KB lives in `knowledge/kb.sqlite`; CLI is `knowledge/kb.ts`.
- SkillsMP Scout is pattern intelligence only; never auto-install marketplace skills.
- Full syntax: `docs/tools/TOOLS-full.md#knowledge-base` and `docs/tools/TOOLS-full.md#skillsmp-scout`.

## Mission Control Dashboard
- Next.js: `http://localhost:3000`; Convex: 3210/3211; tailnet: `https://jts-mac-mini.tailaf2fd2.ts.net`; n8n: `/n8n`.
- If unreachable, kickstart Mission Control LaunchAgents immediately; Tailscale serve recovery details are in full docs.
- Task API is primary for priorities; task creation examples live in full docs.
- Full syntax: `docs/tools/TOOLS-full.md#mission-control-dashboard` and `docs/tools/TOOLS-full.md#mission-control--task-push`.

## Claude Code Agent Personas
- Full persona table: `docs/tools/claude-personas.md`.
- Quick map: frontend, AI/Agentforce, backend, rapid POC, review.

## Consulting / Project Agents
- Project roots: `~/projects/research-agent`, `analysis-agent`, `n8n-agent`, `agentforce-agent`, `crypto-agent`, `job-market-agent`, `ranking-app-agent`.
- Crypto full-analysis validator/writer/pipeline commands moved to full docs.
- Consulting pipeline skill: `skills/opticfy-pipeline/SKILL.md`; command details in full docs.
- Full syntax: `docs/tools/TOOLS-full.md#consulting-pipeline-agents-projects`.

## Salesforce Data Cloud
- Real-time CDP/Data 360 grounding path for Agentforce; details: `docs/tools/salesforce-data-cloud.md`.

## Drive Drafts
- Script: `scripts/drive_drafts.py`; account root: `Eve - Drafts`.
- Reusing title/path updates the existing Google Doc. Corrected high-stakes drafts require live doc verification.
- Full syntax: `docs/tools/TOOLS-full.md#drive-drafts`.

## Consulting Pipeline Drive Sync
- Script: `scripts/pipeline_drive_sync.py`; outreach confirmation: `scripts/outreach_update.py`; email pivot: `scripts/outreach_email_pivot.py`.
- Full syntax: `docs/tools/TOOLS-full.md#consulting-pipeline-drive-sync`.

## Notion
- DBs: Viral Post Swipe File `31316aff930580f6a195ca179793eb0e`; Content Calendar `32516aff930581a78659eac869c71ba8`.
- Use env `NOTION_TOKEN`; never paste tokens. Push/fetch/calendar command syntax moved to full docs.
- Cron truth: `Viral Post Swipe File - X Research`, Mon/Wed/Fri 5:45AM ET; model defaults follow cron config, not a standing isolated-sonnet rule.
- Full syntax: `docs/tools/TOOLS-full.md#notion`.

## Apps
- `jtsomwaru.com`: `~/projects/jtsomwaru-com/` -> Vercel.
- Glow Index: Replit / `jsomwarux/skincare-rankings`; fresh build required before redeploy.
- Nash Satoshi: `jsomwarux/Nash-Satoshi` private.
- Full ops details: `docs/tools/TOOLS-full.md#apps`.
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def append_relocation(dest: Path, marker: str, source_name: str, body: str) -> bool:
    current = read(dest) if dest.exists() else ""
    if marker in current:
        return False
    block = (
        f"\n\n## {marker}\n\n"
        f"> Relocated from `{source_name}` during Phase 6 bootstrap reduction. "
        "No content was deleted; compact bootstrap file now points here.\n\n"
        f"{body.rstrip()}\n"
    )
    write(dest, current.rstrip() + block)
    return True


def rewrite_agents() -> bool:
    text = read(AGENTS)
    old = (
        '11. **Intelligent Model Routing (mandatory):** Gemini Flash-Lite is the global default for cheap background execution. '
        'However, anytime JT requests complex multi-file coding, dynamic problem solving/debugging, or sharp "Systems Architect" '
        'strategy copy generation, YOU MUST SPAWN A SUB-AGENT (`sessions_spawn`) configured explicitly with '
        '`model="anthropic/claude-sonnet-4-6"`. Do not attempt to execute elite reasoning tasks on the primary Flash-Lite model in the main chat session.'
    )
    new = (
        '11. **Intelligent Model Routing (mandatory):** Complex multi-file coding, hard debugging, or high-stakes strategy work '
        'runs on Sonnet-class reasoning via sub-agent using `openrouter/anthropic/claude-sonnet-4-6`; this is a JT-approved '
        'standing exception counted against the named OpenRouter cap.'
    )
    if old not in text:
        raise RuntimeError("AGENTS Core Rule 11 expected text not found")
    write(AGENTS, text.replace(old, new, 1))
    return True


def cleanup_jobs() -> dict:
    with JOBS.open(encoding="utf-8") as f:
        data = json.load(f)
    jobs = data["jobs"] if isinstance(data, dict) else data
    before_count = len(jobs)
    removed = []
    preserved = []
    for job in jobs:
        payload = job.get("payload") or {}
        model = payload.get("model")
        if model == "openai/gpt-5.5":
            removed.append({"id": job.get("id"), "name": job.get("name")})
            del payload["model"]
        elif model:
            preserved.append({"id": job.get("id"), "name": job.get("name"), "model": model})
    if len(jobs) != before_count:
        raise RuntimeError("job count changed unexpectedly")
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup = JOBS.with_name(f"jobs.json.backup-phase6-{stamp}")
    shutil.copy2(JOBS, backup)
    fd, tmp_name = tempfile.mkstemp(prefix="jobs.json.phase6.", dir=str(JOBS.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:
            json.dump(data, tmp, indent=2, ensure_ascii=False)
            tmp.write("\n")
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_name, JOBS)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
    return {
        "backup": str(backup),
        "job_count": before_count,
        "removed_default_overrides": len(removed),
        "preserved_non_default_overrides": preserved,
    }


def main() -> None:
    before = {
        "AGENTS.md": AGENTS.stat().st_size,
        "MEMORY.md": MEMORY.stat().st_size,
        "TOOLS.md": TOOLS.stat().st_size,
        "HEARTBEAT.md": (ROOT / "HEARTBEAT.md").stat().st_size,
    }
    memory_body = read(MEMORY)
    tools_body = read(TOOLS)
    memory_moved = append_relocation(
        MEMORY_FULL,
        "Current Operating Context Relocated From MEMORY.md - 2026-06-11 Phase 6",
        "MEMORY.md",
        memory_body,
    )
    tools_moved = append_relocation(
        TOOLS_FULL,
        "Tool Command Syntax Relocated From TOOLS.md - 2026-06-11 Phase 6",
        "TOOLS.md",
        tools_body,
    )
    write(MEMORY, MEMORY_INDEX)
    write(TOOLS, TOOLS_INDEX)
    rewrite_agents()
    cron = cleanup_jobs()
    after = {
        "AGENTS.md": AGENTS.stat().st_size,
        "MEMORY.md": MEMORY.stat().st_size,
        "TOOLS.md": TOOLS.stat().st_size,
        "HEARTBEAT.md": (ROOT / "HEARTBEAT.md").stat().st_size,
        "docs/memory/MEMORY-full.md": MEMORY_FULL.stat().st_size,
        "docs/tools/TOOLS-full.md": TOOLS_FULL.stat().st_size,
    }
    print(json.dumps({
        "before_bootstrap": before,
        "after_bootstrap": after,
        "memory_relocated": memory_moved,
        "tools_relocated": tools_moved,
        "cron": cron,
    }, indent=2))


if __name__ == "__main__":
    main()
