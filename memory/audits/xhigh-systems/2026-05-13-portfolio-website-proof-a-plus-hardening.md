# A+ Hardening — Portfolio / Website / Proof Automation

Date: 2026-05-13
Scope: follow-up hardening after `/memory/audits/xhigh-systems/2026-05-13-portfolio-website-proof.md`.

## Before Grade
A-

The prior audit cleaned the main state drift and verified the site build, but four A+ blockers remained: portfolio updater instructions still referenced direct `claude --dangerously-skip-permissions`, public `llms.txt` named Aya, Glow Index was not live-state verified, and the proof/distribution layer lacked a concrete safe proof asset.

## After Grade
A

The website/proof layer is safer and more truthful now: direct forbidden Claude CLI instructions were removed from the portfolio updater workflow, public named-client proof was anonymized pending permission review, Glow Index live/public state was checked and accurately held, and a reusable anonymized proof snippet was drafted. Not A+ only because Glow Index still needs a deployment/auth fix before it can be treated as public AI-search proof or a portfolio card candidate.

## Changes Made

### 1. Portfolio updater agent modernized
File: `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/AGENT.md`

- Removed the workflow that told agents to run:
  - `cd ~/projects/jtsomwaru-com && claude --dangerously-skip-permissions ...`
- Replaced it with the approved OpenClaw background coding sub-agent/coding-agent workflow.
- Added explicit warning not to run `claude`, `claude --print`, or `claude --dangerously-skip-permissions` from the main session or synchronous exec path.
- Updated completion expectations to return files changed, lint/build status, commit SHA, and Vercel trigger expectation instead of sending external system events directly.

Validation:
- `grep -RInE "claude --dangerously|claude --print|cd ~/projects/jtsomwaru-com && claude" agents/portfolio-updater/AGENT.md` returns no forbidden executable pattern. The only remaining mention is the warning text.

### 2. Public named-client proof anonymized
Files:
- `/Users/jtsomwaru/projects/jtsomwaru-com/public/llms.txt`
- `/Users/jtsomwaru/projects/jtsomwaru-com/src/components/About.tsx`

Changed public proof label from:
- `Aya — NYC Construction & Real Estate`

to:
- `NYC construction & real-estate operator`

Reason: `llms.txt` is a public AI-citation surface. Unless explicit client permission is verified, named proof is riskier than anonymized proof. The prior audit already flagged this; this pass patched it.

Validation:
- `grep -RIn "Aya\|Altmark\|Yair\|Matt" /Users/jtsomwaru/projects/jtsomwaru-com/src /Users/jtsomwaru/projects/jtsomwaru-com/public/llms.txt` returned no matches after the patch.

### 3. Glow Index live/public state verified
Checked:
- `https://skincare-rankings.replit.app`
- `https://skincare-rankings.replit.app/llms.txt`
- `https://skincare-rankings.replit.app/robots.txt`
- Local project files under `/Users/jtsomwaru/projects/skincare-rankings`

Findings:
- Homepage returns HTTP 200 and renders Glow Index content.
- Live `/llms.txt` returns HTTP 307 redirect to Clerk sign-in.
- Live `/robots.txt` returns `User-agent: *` / `Disallow: /`.
- Local `app/robots.ts` allows crawlers, so deployed behavior likely reflects Replit/auth/proxy/deploy drift rather than intended source state.
- Local `proxy.ts` public route list omits `/llms.txt`, `/robots.txt`, and `/sitemap.xml`, which likely explains the Clerk redirect for `llms.txt`.

Decision:
- Keep `glow-index` held from public portfolio/proof until public AI-search assets are fixed and redeployed.
- Updated `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/state.json` audit notes with this finding.
- Appended update-log entry in `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/update-log.md`.

### 4. Proof asset drafted
Created:
- `/Users/jtsomwaru/.openclaw/workspace/memory/proof-assets/2026-05-13-anonymized-ai-ops-proof-snippet.md`

Includes:
- Website/proposal snippet
- LinkedIn proof angle
- X single
- Deck insert

Safety:
- Uses anonymized language only.
- Explicitly says not to name Aya, Altmark, Yair, Matt, or private clients unless JT verifies permission.

### 5. Mission Control blocker created
Created exactly one MC blocker task:
- ID: `j575kwn02jpwdx5xgvma67wmcx86nssh`
- Title: `Fix Glow Index public AI-search assets before portfolio card`
- Priority: medium
- Project: Apps
- First action: update Glow Index Clerk/proxy routing so `/llms.txt`, `/robots.txt`, and `/sitemap.xml` are public, redeploy Replit with fresh rebuild, then verify public 200/no-disallow behavior.

## Validation

Bootstrap budget check completed first:
- `AGENTS.md`: 26829 bytes
- `MEMORY.md`: 18570 bytes
- `TOOLS.md`: 13581 bytes
- `HEARTBEAT.md`: 14330 bytes

Site prerequisites:
- Read `/Users/jtsomwaru/projects/jtsomwaru-com/CLAUDE.md` before touching site files.
- Checked for site lesson files; none found under `jtsomwaru-com` max depth 4.
- For Glow verification, read `/Users/jtsomwaru/projects/skincare-rankings/tasks/lessons.md` and `DEPLOY_CHECKLIST.md` before drawing conclusions.

Site validation after source changes:
- `npm run lint` passed.
- `npm run build` passed.
- Build generated 42 static pages, including `/guyana`, `/property-family-office-ai-ops`, `/robots.txt`, `/sitemap.xml`, and all 23 `/work/[slug]` pages.

No public deploy or git push performed.

## Files Changed

Workspace:
- `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/AGENT.md`
- `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/state.json`
- `/Users/jtsomwaru/.openclaw/workspace/agents/portfolio-updater/update-log.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/proof-assets/2026-05-13-anonymized-ai-ops-proof-snippet.md`
- `/Users/jtsomwaru/.openclaw/workspace/memory/audits/xhigh-systems/2026-05-13-portfolio-website-proof-a-plus-hardening.md`

Site project:
- `/Users/jtsomwaru/projects/jtsomwaru-com/public/llms.txt`
- `/Users/jtsomwaru/projects/jtsomwaru-com/src/components/About.tsx`

Mission Control:
- Added task `j575kwn02jpwdx5xgvma67wmcx86nssh`.

Note: existing untracked/modified `.claude/audit.log` and `.claude/warden-edit-tracker` were present in the site repo and were not intentionally changed by this pass.

## Remaining Blocker

Glow Index is the only remaining blocker for A+:
- Homepage live: yes.
- Public AI-search proof live: no.
- `/llms.txt`: redirects to sign-in.
- `/robots.txt`: disallows all.

Fixing Glow proxy/auth/deploy behavior and then deciding whether to add a public portfolio card would move this layer to A+.
