# Fable 5 Context Pack: Mission Control Optimization

Date: 2026-07-11

## What Mission Control Is

Mission Control is JT Somwaru's internal operating dashboard. It is not a generic task manager. Its job is to keep JT focused on the next action that best advances his north star: consulting cash collected, proof captured, reusable IP created, and personal stability protected.

Primary user: JT Somwaru.
Secondary user/operator: Eve, JT's AI Chief of Staff.

Current product role:
- Show JT exactly what needs his attention now.
- Keep Eve-owned work visible but out of JT's way.
- Surface revenue pressure, proof gaps, operational risk, and stale work.
- Let Eve update task priority/status through the dashboard API.
- Reduce JT's cognitive load, not create another board to manage.

## JT's North Star

Priority order:
1. Collect consulting cash and proof through real client delivery.
2. Turn proof into repeatable AI implementation offers and reusable IP.
3. Build and market apps only when distribution or retention evidence exists.
4. Monitor crypto as an opportunity scan only.
5. Protect health, sleep, debt control, and NYC/location stability.

Current July 2026 mandate:
- Three workstreams only: Altmark close-out/referral unlock, MSI/Marketsmith close, contracted collections.
- Truth metric: earned consulting cash collected.
- Progress means a JT send executed, a chase surfaced on date, a gate/kill window caught on time, or a scoreboard number tied to evidence.
- App work, crypto work, job-market work, new dashboards, new proof assets, and broad strategy docs should not outrank cash/proof actions.

## Current Tech / Repo

Repo: `https://github.com/jsomwarux/openclaw-workspace`
Project subfolder: `mission-control/`
Local URL: `http://localhost:3000`
Stack: Next.js 15 App Router, TypeScript, Tailwind CSS, Convex for tasks.

Key files:
- `mission-control/app/page.tsx` - Command cockpit.
- `mission-control/app/work/page.tsx` - task router.
- `mission-control/app/consulting/page.tsx` - revenue cockpit.
- `mission-control/app/ship/page.tsx` - app/content shipping lane.
- `mission-control/app/machine/page.tsx` - agents/cron/system lane.
- `mission-control/app/evidence/page.tsx` - proof lane.
- `mission-control/app/health/page.tsx` - ops/cost/health lane.
- `mission-control/lib/mission-control/adapters.ts` - converts tasks/crons/proofs/agents into signals.
- `mission-control/lib/mission-control/score.ts` - current scoring model.
- `mission-control/lib/mission-control/command-brief.ts` - current top brief logic.
- `mission-control/lib/mission-control/hooks.ts` - fetches tasks/crons/proofs/agents/costs every 30s.
- `mission-control/convex/tasks.ts` and `mission-control/app/api/tasks/route.ts` - task CRUD.

## Current Navigation

Current primary lanes:
- Command: decisions.
- Work: tasks.
- Revenue: consulting cash path.
- Ship: apps/content.
- Machine: agents/crons/systems.
- Evidence: proof/memory/audit.
- Health: ops/cost/health.

Mobile nav only shows the first five lanes.

## Current Command Page Behavior

The `/` page currently displays:
- Four metric cards: active revenue-path tasks, high-priority revenue/job items, completed revenue-path tasks, cost today.
- `Needs You Now`: capped at 7 JT-owned decisions.
- `Eve Is Handling`: Eve-owned in-progress work.
- `Risk & Drift`: failed, stale, blocked signals.
- `Command Brief`: headline, top action, latest proof, urgent/revenue/risk counts.

Current visual language:
- Dark utilitarian UI.
- Emerald/orange/blue accents.
- Compact cards and side rails.
- Uses lucide icons.

## Current Scoring Model

Signals are scored using weighted factors:
- revenue: 30%
- unblock: 20%
- urgency: 20%
- risk: 15%
- northStar: 15%

Current weakness: the model is too generic. It treats "revenue lane" and priority as broad labels. It does not sufficiently encode JT's actual current operating mandate, cash value, exact next-send gates, deadline windows, proof leverage, or anti-distraction rules.

## Current Live Task Shape

Latest live task summary from `/api/tasks`:
- Active tasks: 285
- High-priority tasks: 14
- Top current JT high-priority items include:
  1. Altmark: send rent delinquency source/export gate and collect $2,250 closeout path
  2. Outbound v2: audit deliverability, finish COI proof pack, then launch 15 PM prospects
  3. Send Petri Plumbing M2 connection request
  4. MSI/Marketsmith: close 80-hour Nexus scope at $150/hr
  5. Complete weekly unemployment certification
  6. Review/post PM Front Desk + Exception Desk proof
  7. Send HPM/Superior M2 follow-ups
  8. Strategy: Package Outcome-Based Run Control

Top active projects by count:
- Consulting: 102
- Skills: 51
- Job Market: 45
- Content: 34
- passive-income: 15
- Operations: 9
- Apps: 6
- App Marketing: 5

## Recent Priority Correction

On 2026-07-11, Mission Control was reconciled:
- Altmark moved to #1 high-priority JT closeout task.
- MSI/Marketsmith moved to #2 high-priority JT close task.
- Vague combined North Star task archived.
- Action Arena moved from Eve active work to JT-owned low-priority Apple Developer org-transfer gate.
- Glow/Vista app work archived during July consulting-cash mandate.

This shows the desired behavior: the board should constantly prune distractions, compress duplicates, and keep the next cash/proof action at the top.

## What Needs Optimization

Mission Control needs to become a decision operating system, not a prettier kanban.

Core product questions:
1. What should JT see first every time he opens it?
2. What should be hidden, collapsed, or demoted by default?
3. How should the system make the next best action impossible to miss?
4. How should it gamify focus without turning into shallow streak mechanics?
5. How should Eve autonomously reprioritize tasks as new evidence arrives?
6. How should Mission Control explain why something is ranked where it is?
7. How should the UI protect JT from app/job/skill backlog clutter when the current mandate is consulting cash?

## Desired Product Direction

The ideal dashboard should:
- Open with one clear "Do This Next" action.
- Show the top 3 JT actions only, unless JT expands the queue.
- Separate "JT must act" from "Eve is handling" from "do not think about this now."
- Use explicit dollar/proof/deadline/risk labels rather than generic priority badges.
- Show why a task is ranked: cash impact, deadline, unblock value, proof leverage, health/stability impact.
- Penalize stale speculative tasks and duplicate tasks.
- Surface "send due today" and "decision due today" as first-class objects.
- Make completed sends or closeout actions feel rewarding in a sober, operator-focused way.
- Keep the UI calm, dense, and scannable. No marketing-style hero sections.

## Gamification Direction

Use gamification only if it reinforces the north star.

Good gamification:
- Daily "cash clock" or "send streak" tied to real sends/chases.
- A weekly closeout scoreboard.
- Progress toward specific gates: Altmark closeout, MSI close, collections.
- Friction removed count: stale tasks archived, duplicates merged, blockers cleared.
- Proof captured count, but only for verified proof.
- A "focus protection" score showing how much irrelevant work stayed out of JT's view.

Bad gamification:
- Generic points for checking boxes.
- Rewarding content quantity or task volume.
- Streaks that encourage low-value actions.
- App/product progress during a consulting-cash mandate.

## Constraints

- JT should not become the project manager of the system.
- Eve can update internal task priority/status, but JT presses send for all external messages.
- Do not design around generic productivity. Design around consulting cash, proof, and focus.
- Do not make the first screen a landing page.
- Keep the dashboard operational, dense, and repeat-use friendly.
- Mobile matters because JT checks Telegram and dashboard quickly.
- Any recommendation must be implementable in the existing Next.js/Tailwind/Convex architecture.

## Fable Output Needed

Ask Fable for:
1. A ruthless critique of the current Mission Control information architecture.
2. The optimal first-screen layout for JT.
3. A scoring/ranking model that Eve can run autonomously.
4. A gamification model that supports real progress.
5. UI component recommendations for desktop and mobile.
6. A data model/schema delta if needed.
7. A phased implementation plan for Codex/Claude Code.
8. Specific copy labels for key UI surfaces.
9. What to remove, hide, or demote.
10. Acceptance criteria for "completely optimal enough to ship."

