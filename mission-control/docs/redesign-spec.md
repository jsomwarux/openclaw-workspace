# Mission Control — Five-Lane Redesign Specification

**Status:** Draft for JT approval. No code written.
**Author:** Eve · 2026-07-28
**Scope:** IA + layout + schema + copy + build order. Next.js 15 / Tailwind / Convex. No new dependencies.

---

## 0. North star & design intent

Mission Control is JT's personal operating cockpit — calm, dense, operational, repeat-use. It exists to keep four things in view:

1. **Consulting cash collected** (the truth metric)
2. **Client proof captured**
3. **Reusable AI implementation IP**
4. **Personal stability**

Today's nav is three lanes — **Cockpit / Money / Systems** — which collapsed six sub-surfaces (work, ship, evidence, health, machine, memory) behind "Systems." That was right when the app was task-first. It no longer matches how JT works: the day is now organized around *clients* and *the tools he can bring to them*, neither of which has a home.

This redesign moves to **five lanes, each answering exactly one question:**

| Lane | Route | Question it answers |
|---|---|---|
| **Today** | `/` | What do I do right now? |
| **Clients** | `/clients` | Where does each client stand? |
| **Money** | `/consulting` | Where is the cash? |
| **Library** | `/library` | What tools do I have? |
| **Systems** | `/machine` | Is the machine healthy? |

> **⚠️ CLAUDE.md conflict to approve:** the project `CLAUDE.md` currently hard-codes "Primary nav is three lanes" and "Do not re-add them to the nav," plus a four-band "Cockpit contract." This spec supersedes those two sections. If you approve the five-lane IA, the `## Cockpit contract` and nav paragraphs in `CLAUDE.md` must be rewritten in the same PR so the guardrails match the app. The four-band **behavior** of Today is preserved verbatim (see §3.1); only the lane count and nav change.

---

## 1. Current-state audit (what exists today)

### Routes that already work
- `/` — four-band cockpit (cash strip → NOW → UP NEXT → collapsed Waiting/Eve/Risk). Backed by `useMissionControlData` → `commandQueue` (score.ts). **Keep as-is.**
- `/consulting` — "Money" lane. Reads `north-star.md` + `pipeline.jsonl` server-side, renders 4 metric cards + pipeline table + send-queue + `RevenueTaskRails`.
- `/machine` — "Systems" lane. `useMissionControlData` → `machineSummary`/`machineGroups`. 5 metric tiles + 4 rails (cron/agents/cost/work).
- `/skills` — searchable skill grid via `/api/skills` (reads `~/.openclaw/workspace/skills/**/SKILL.md` + bundled). **This is 80% of the Library lane already.**
- `/ship`, `/evidence`, `/health`, `/work`, `/passive-income` — live subpages, reachable but not in nav.
- Legacy: `/tasks`→`/work`, `/vibe`→`/ship`, `/agents`→`/machine`, `/audit`→`/evidence`, `/monitor`/`/costs`→`/health` (redirect map in `routes.ts`).

### Data backplane
- **Convex tables:** `tasks`, `focus`, `priorityAudit`, `pideas`. Tasks already carry `dollars`, `stageProbability`, `pipelineStage`, `lane`, `project`, `waitingOn` — but **no `clientId`**.
- **Filesystem reads (API routes):** `/api/revenue`, `/api/skills`, `/api/agents` (reads `data/agents.json` + auto-discovers `~/projects/*`), `/api/cron`, `/api/proofs`, `/api/costs`, `/api/memory`.
- **Client data lives on disk, not in the app:** `memory/clients/{altmark-group,aya,karen-vitale,marketsmith}/` with `status.md`, `metrics.md`, `README.md`, proof assets. Nothing in Mission Control reads it. Clients appear only as free-text `pipeline.jsonl` rows and as `project` strings on tasks.

### The collected-cash defect (must-fix, called out in the brief)
`pipeline.jsonl` **zeroes `value` the moment a client pays** (`SoberLife` and `Aya` are `value:0, stage:"closed_won_collected"`; Altmark's $8,500 of already-collected buildout cash is *not represented at all* — only the $2,250 remainder). Consequences:

- `parsePipelineJsonl` sums `openWeighted` and `closedValue` — but closed items have `value:0`, so **closed/collected cash is structurally $0.**
- `/api/revenue` therefore reports `consultingCollected $0, totalCollected $0` (confirmed live 2026-07-28).
- The cockpit's cash strip and `score.ts` ship-cap read `metrics.totalCollected` from a **fragile regex over `north-star.md` prose** (`moneyAfter("Total collected:", …)`). Collected cash is a *parsed string*, not stored data.
- **Net: the cockpit cannot represent collected cash at all.** The one number the whole app orbits is derived from a file that discards it.

Ground truth (reconciled ledger confirmed with JT 2026-07-28): **$19,400 collected all-time; $9,400 collected July MTD** — Altmark $8,500 (Foundation $4,000 pre-July + COI expiration $2,250 pre-July + Rent-Delinquency 50% $2,250 pre-July), Aya $2,500 (Dashboard $1,500 pre-July + Dashboard updates $1,000 July), SoberLife Phase 1 $3,000 (July), MSI Kickoff 50% $5,400 (July). Against the **monthly** $10K gate, July MTD $9,400 leaves a **$600 gap**. None of this is queryable today. (The four pre-July payments have no logged day — `paidOn` is set to the first of a best-known month with `source: "date not logged, month inferred"`; the three July payments use the 2026-07-28 confirmation date.)

**§5 specifies the fix: a `payments` table as the system of record for collected cash, with the `$10K` gate stored as an explicit, typed field rather than assumed.**

---

## 2. Design system (extend, don't invent)

Reuse the existing dark tokens. No new palette, no new dependency.

- **Surfaces:** `#0a0b0d` (page), `#0d1014`/`#0d0d0d` (card), `#111` (raised), border `#20262d`/`#2a2a2a`.
- **Accent — keep both in play, don't unify:** emerald `#10b981` = money/healthy/proof; amber `#f0883e` = attention/NOW/cash-gap. These already encode meaning across lanes; preserve the split.
- **Status tones (existing):** red `failed/blocked`, amber `stale/in-progress`, emerald `done`, blue `neutral-active`, purple = Eve.
- **Type:** JetBrains Mono for labels/metrics (already global), zinc scale for text.
- **Primitives already in the system:** `StateBlock` (loading/empty/gap/stale), `MetricCard` (consulting), `Metric` (machine), `SkillCard`, `SignalRow`+`Rail` (machine), `ReasonChipRow`, `InspectionDrawer`, `CollapsedStrip`.

Mobile is bottom-nav + `mobileMainClassName` (`pt-12 pb-28 md:ml-52`). The bottom nav grid is **`grid-cols-3` today and must become `grid-cols-5`** (`nav-layout.ts`).

---

## 3. Lane-by-lane layout (desktop + mobile)

### 3.1 Today (`/`) — "What do I do right now?"

**Unchanged behavior.** Keep the four-band cockpit exactly: NOW single card (~3× visual weight), UP NEXT capped at 7 (rows 2–7 of `commandQueue`), collapsed Waiting/Eve/Risk strips (Risk only when count > 0). No numeric score on the page; rank via reason-code chips only. `score.ts` and `commandQueue` are **not touched**.

Two additive changes only, both data-source swaps behind the existing UI:
1. **Cash strip reads the payments-derived `collected`** (§5) instead of the `north-star.md` regex. Same `cashStrip()` component, same look; the number is now real.
2. **NOW/UP NEXT rows that belong to a client** show a small client tag (reuses the existing `project` slot in the row — no new element). Tapping a client tag deep-links to that client's detail in Clients.

- **Desktop:** as today (single column, max content width, bands stacked).
- **Mobile:** as today. NOW card stays dominant; UP NEXT rows keep the visible age + first reason chip.

**Do not turn Today into a task list.** It stays one-decision-at-a-time.

---

### 3.2 Clients (`/clients`) — "Where does each client stand?" *(new lane)*

The lane JT is missing. A per-client roster backed by the new `clients` table + `payments` + tasks (`clientId`), enriched by the on-disk `memory/clients/*` status.

**List view — desktop:** responsive grid of **ClientCard** (`sm:grid-cols-2 xl:grid-cols-3`), sorted by open-dollars desc, then last-touch desc. Above the grid, one dense summary strip (reuses `Metric`): `Active clients` · `Open $` · `Collected $ (all-time)` · `Oldest untouched`.

**ClientCard contents:**
- Client name + emoji, stage badge (`Active delivery` / `Blocked` / `Pending` / `Closed-won`).
- One-line status (from `clients.status`, seeded from `status.md`).
- Row of stats: **Last touch** (relative), **Open tasks** (count), **Open $** (sum of open task `dollars`), **Collected $** (sum of cleared `payments`).
- `waiting_on` chip when blocked (who + age), reusing the waiting tone.

**List view — mobile:** single-column stacked ClientCards; stats collapse to a two-up grid inside the card. Tap → detail.

**Detail view (`/clients/[slug]`) — desktop:** two-column.
- **Left (primary):** header (name, stage, status line, memory-path link) → **Open work** (all incomplete tasks for this client, ranked high→med→low then newest — reuse the `/work` priority sort + row treatment; each row opens `InspectionDrawer`) → **Completed this week** section (tasks done within 7 days) → **Older completions** behind an **Archive toggle** (default collapsed; reuses `CollapsedStrip`).
- **Right (rail):** **Money** mini-panel (Collected to date, Open $, next milestone from `payments`/pipeline) → **Proof** links (client's `proof-assets/` via `/api/clients`) → **Referral** eligibility flag (from status).

**Detail — mobile:** single column, same order: header → open work → completed-this-week → archive toggle → money → proof.

> Client roster is small (4 active). This lane is about **density and recall, not CRUD** — JT reads it to know who's owed a touch and who's owed an invoice.

---

### 3.3 Money (`/consulting`) — "Where is the cash?" *(largely as-is)*

Keep the current layout: metric row + pipeline table + send-queue + `RevenueTaskRails`. Three corrections, all driven by §5:

1. **"Earned Consulting" / "Total Collected" now read the `payments` table**, not the `north-star.md` regex. The current card copy ("Current June earned income…") is hardcoded and wrong; replace with the stored gate basis (§4 copy).
2. **Add a "Collected — by client & date" panel** below the metric row: a compact ledger (client · milestone · amount · date · cleared/pending) sourced from `payments`. This is the surface that finally shows the $19,400 all-time / $9,400 July MTD that `pipeline.jsonl` hides. Reuses the pipeline-table row grid.
3. **`pipeline.jsonl` is demoted to forecast-only.** The "Consulting Pipeline" table keeps reading it for weighted-forecast rows (open items), but **collected/closed cash is never derived from it again.** Add a one-line footnote naming the split so the model that maintains these files stops zeroing collected cash into oblivion.

- **Desktop:** metric row (4) → NEW collected ledger → `[pipeline table | send-queue + rails]` two-column as today.
- **Mobile:** metric row 2×2 → ledger (stacked rows) → pipeline (stacked) → send-queue → rails.

The `$10K gate` card shows the **stored basis label** ("monthly" or "all-time," §4) so the gap is never ambiguous again.

---

### 3.4 Library (`/library`) — "What tools do I have?" *(new lane, mostly reuse)*

A searchable catalog of JT's reusable capability: **skills** + **agents**. The brief names "the jt-claude-toolkit folder" — that folder does **not exist locally**; per `CLAUDE.md`, the toolkit was *synthesized into* `~/.openclaw/workspace/skills/` (38 dirs) and `~/.openclaw/workspace/agents/` (24 dirs) plus `data/agents.json`. Those are the real sources. (If you want the GitHub repo `jsomwarux/jt-claude-toolkit` as a third source, that's a follow-on; flagging so we don't spec a phantom path.)

This lane is the existing `/skills` page generalized:
- Reuse `SkillCard`, the search box, and the filter chips verbatim.
- Add a **type filter**: `All · Skills · Agents · Bundled`.
- Add an **AgentCard** (small new variant of SkillCard) for agent defs: name/emoji, role, domain, status (active/planned), linked crons, workspace path.
- Search matches name/slug/description/commands across both types (extends the existing `displayed` filter).

- **Desktop:** header (counts) + filter/search bar → sectioned grids (Custom Skills / Agents / Bundled), `xl:grid-cols-3`.
- **Mobile:** single-column cards, sticky filter/search bar.

`/skills` is retained as an alias of `/library` (or redirected) so nothing breaks.

---

### 3.5 Systems (`/machine`) — "Is the machine healthy?" *(as-is)*

Keep the current machine cockpit: 5 metric tiles (Cron / Failed / Agents active / Cost today / Risks) + 4 rails (Cron health / Agent posture / Cost pressure / Automation work). No structural change. It absorbs evidence/health/cost surfaces as it does today.

Only change: it drops out of the "everything else" role — Clients, Money, and Library now carry what used to be jammed under Systems, so Systems is purely ops health.

- **Desktop/mobile:** unchanged from current `/machine`.

---

## 4. UI copy (every label)

**Nav (desktop sidebar `label` / `desc`, mobile `label`):**
| Route | Label | Desc | Mobile |
|---|---|---|---|
| `/` | Today | Next decision | Today |
| `/clients` | Clients | Who stands where | Clients |
| `/consulting` | Money | Cash path | Money |
| `/library` | Library | Tools & agents | Library |
| `/machine` | Systems | Machine health | Systems |

**Today:** unchanged (`Cockpit` eyebrow → rename to `Today`; H1 "One decision at a time"; bands "Now" / "Up next" / "Waiting on others" / "Eve has it" / "Risk"; empty "Queue clear. Protect the block.").

**Clients — list:** eyebrow `Clients`; H1 "Where each client stands". Summary tiles: `Active clients`, `Open $`, `Collected (all-time)`, `Oldest untouched`. Card stage badges: `Active delivery`, `Blocked`, `Pending`, `Closed-won`. Card stats: `Last touch`, `Open tasks`, `Open $`, `Collected`. Empty: "No clients on file yet."

**Clients — detail:** sections `Open work`, `Completed this week`, `Older completions` (toggle: "Show older completions" / "Hide older completions"); rail `Money`, `Proof`, `Referral`. Money rail rows: `Collected to date`, `Open $`, `Next milestone`. Referral flag: "Referral ask eligible" / "Referral gated".

**Money:** eyebrow `Money`; H1 "Cash path". Metric cards: `Earned consulting` (detail: "Collected consulting cash. The truth metric."), `Weighted pipeline` (detail: "Value × probability from pipeline.jsonl. Not cash."), `$10K gate` (detail: "{basis} target. {gap} to go."), `Total collected` (detail: "Includes ${unemployment} unemployment, tracked separately."). NEW ledger: heading "Collected — by client & date"; columns `Client`, `Milestone`, `Amount`, `Date`, `Status` (`Cleared`/`Pending`). Footnote: "Collected cash is stored in the payments ledger. pipeline.jsonl is forecast-only and zeroes items once paid — never read collected cash from it."

**Library:** H1 "Library"; subtitle "{n} skills · {m} agents". Filters: `All`, `Skills`, `Agents`, `Bundled`. Search placeholder "Search tools, agents, commands…". Section heads: `Custom Skills`, `Agents`, `Bundled Skills`. AgentCard fields: `role`, `domain`, `status` (`active`/`planned`), `crons`. Empty: "No tools match."

**Systems:** unchanged.

---

## 5. Schema additions

All additive. No changes to existing table shapes beyond one optional field on `tasks`.

### 5.1 `clients` table *(new)*
```ts
clients: defineTable({
  slug: v.string(),                 // "altmark-group" — matches memory/clients/<slug>
  name: v.string(),                 // "Altmark"
  emoji: v.optional(v.string()),
  stage: v.union(                   // drives the stage badge
    v.literal("active-delivery"),
    v.literal("blocked"),
    v.literal("pending"),
    v.literal("closed-won"),
    v.literal("archived"),
  ),
  status: v.optional(v.string()),   // one-line status, seeded from status.md
  waitingOn: v.optional(waitingOn), // reuse existing waitingOn object
  lastTouch: v.optional(v.number()),
  memoryPath: v.optional(v.string()),// "memory/clients/altmark-group"
  referralEligible: v.optional(v.boolean()),
  createdAt: v.number(),
  updatedAt: v.number(),
}).index("by_slug", ["slug"]).index("by_stage", ["stage"]),
```

### 5.2 `payments` table *(new — the collected-cash system of record)*
This is the fix for the pipeline-zeroing defect. Collected cash becomes stored, per-payment, queryable data — never re-derived from a file that discards it.
```ts
payments: defineTable({
  clientId: v.optional(v.id("clients")), // link when client exists
  clientName: v.string(),                 // denormalized, always present
  amount: v.number(),                     // USD, positive = money in
  paidOn: v.number(),                     // epoch ms — the clearance date
  milestone: v.optional(v.string()),      // "Foundation", "Insurance 50%", "MSI kickoff"
  kind: v.union(
    v.literal("consulting"),
    v.literal("unemployment"),
    v.literal("other"),
  ),
  cleared: v.boolean(),                    // true = cleared, false = invoiced/pending
  source: v.optional(v.string()),          // evidence ref (file path / note)
  createdAt: v.number(),
  updatedAt: v.number(),
}).index("by_client", ["clientId"]).index("by_paidOn", ["paidOn"]).index("by_kind", ["kind"]),
```
**Derived `collected` (new `lib/mission-control/collected.ts`):** `consultingCollected = Σ amount where kind="consulting" ∧ cleared`; `totalCollected = consultingCollected + Σ unemployment`. This value feeds:
- Money lane metric cards + the new ledger,
- Today's cash strip,
- `buildScoreContext({ collected })` → `score.ts` ship-cap — **no change to `score.ts`; it already consumes `ctx.collected`.**

`north-star.md` stays the source for *prose + weighted forecast*; it is **no longer** the source for collected cash. `pipeline.jsonl` stays the source for *open weighted forecast* only.

### 5.3 `gateConfig` — store the $10K gate explicitly *(new, tiny)*
The monthly-vs-all-time ambiguity is currently an unstated assumption. Make it a stored, typed field.
```ts
gateConfig: defineTable({
  amount: v.number(),                      // 10000
  basis: v.union(v.literal("monthly"), v.literal("all-time")),
  effectiveFrom: v.number(),
  note: v.optional(v.string()),
}).index("by_effectiveFrom", ["effectiveFrom"]),
```
Alternative (lighter): add `gateBasis: v.union("monthly","all-time")` to the existing `focus` table, which already holds `gate: number`. **Recommendation: extend `focus`** — it already carries `gate` and is already read by the scorer, so one field closes the ambiguity with zero new wiring. Default `basis: "monthly"` (matches the Friday Scoreboard's "cash collected month-to-date vs $10K"). Surface the label on the Money `$10K gate` card so the gap is self-describing.

### 5.4 `tasks` — one optional field
```ts
clientId: v.optional(v.id("clients")),   // + .index("by_client", ["clientId"])
```
Keep `project: string` for back-compat and non-client work. `clientId` is the authoritative link when present; a migration backfills it from `project`/title against `clients.slug`.

### 5.5 Library — no schema
Filesystem-sourced. Reuse `/api/skills`; add an agents read (from `data/agents.json` + `/api/agents`) into a merged `/api/library` (or extend `/api/skills` with an `agents` array). No table.

---

## 6. Component inventory — reuse / retire / new

### Reuse verbatim (or with data-source swap only)
| Component | Reused for |
|---|---|
| `InspectionDrawer` | Today, Clients detail (open-work rows), Money task rails |
| `StateBlock` | every lane's loading/empty/gap states |
| `MetricCard` (consulting) | Money cards, Clients summary tiles |
| `Metric` (machine) | Clients summary strip, Systems (unchanged) |
| `SignalRow` + `Rail` (machine) | Systems (unchanged) |
| `SkillCard` + search/filter (skills page) | Library |
| `ReasonChipRow` / reason-codes | Today (unchanged) |
| `CollapsedStrip` | Today strips (unchanged) + Clients "Older completions" toggle |
| `cashStrip`, `commandBrief`, `commandQueue`, `score.ts` | Today — **untouched logic**, cash number re-sourced |
| `RevenueTaskRails` | Money (unchanged) |
| `/work` priority sort (`work-priority.ts`) | Clients detail open-work ranking |

### Retire / demote
- **`pipeline.jsonl` as a collected-cash source** — demoted to forecast-only. `parsePipelineJsonl` stays for open weighted rows; its `closedValue` output stops feeding any "collected" number.
- **`north-star.md` regex for collected cash** (`moneyAfter("Total collected:"…)`) — retired as the app's cash source (kept only for prose/forecast display and as a human-editable mirror).
- **Hardcoded "Current June earned income" copy** on the Money card — removed (it's stale and wrong).
- **Legacy routes** (`/legacy/*`, `/tasks` kanban, `/vibe`, `/audit`, `/monitor`, `/costs`) — keep redirects, drop from any nav consideration (already out of nav).

### New primitives — each justified
| New | Why it can't be reuse |
|---|---|
| `ClientCard` | No per-client card exists; clients are only free-text pipeline rows + folder reads. Smallest new surface that answers "where does this client stand." Built from existing tokens + `Metric` stats. |
| `/clients` list page + `/clients/[slug]` detail | New lane; no existing route renders client-scoped work. Detail reuses `InspectionDrawer` + `/work` sort + `CollapsedStrip`. |
| `AgentCard` | `SkillCard` has no slot for role/domain/status/crons. A thin variant, not a new system. |
| `/api/clients` route | Merges `clients` table + `payments` + client-scoped tasks + on-disk `memory/clients/*` proof/status. No existing route joins these. |
| `lib/mission-control/collected.ts` | Pure derivation of collected cash from `payments`. Isolates the fix; keeps `score.ts` untouched. |
| Convex `clients`, `payments` mutations/queries + `payments` seed | The system-of-record fix. |
| `/library` page (or `/skills` generalized) + merged skills+agents fetch | Extends existing skills page; new only in that it adds the agents source + type filter. |

---

## 7. Phased build order

### Phase 1 — ships in 1–2 sessions (foundation + the cash fix + nav)
**Goal: kill the $0-collected defect and stand up the five-lane nav.** No Clients detail yet.
1. Schema: add `payments` table + `clients` table (empty ok) + `focus.gateBasis`; add `tasks.clientId` (optional). Deploy with `bunx convex dev`.
2. `convex/payments.ts` mutations/queries + a one-time seed of the known ledger (Altmark ×3, Aya, Karen) with real `paidOn` where known, `cleared:true`.
3. `lib/mission-control/collected.ts` + `/api/payments`. Wire `useMissionControlData` + Money page to read collected from payments; feed `buildScoreContext({ collected })`.
4. Money lane: swap card sources, add the "Collected — by client & date" ledger, add the pipeline footnote, show gate basis label.
5. Nav: `routes.ts` 3→5 entries; `nav-layout.ts` mobile grid `grid-cols-3`→`grid-cols-5`; rename `/` eyebrow to "Today". `/library` = alias/redirect of `/skills` for now.

**Phase 1 verification:** Money shows **July MTD consulting collected = $9,400** and **gap to the $10K gate = $600**, with the full ledger itemized (all-time $19,400) and the gate-basis label reading "monthly"; cash strip on Today shows the real collected number; nav has five entries desktop+mobile (`grid-cols-5`); `score.ts` and `commandQueue` untouched; `bun test` green; `bun run build` clean (`NEXT_DIST_DIR=.next-build`).

### Phase 2 — Clients lane
6. `clients` seed from `memory/clients/*` (slug, name, stage, status, lastTouch, memoryPath). Backfill `tasks.clientId` from `project`/title.
7. `/api/clients` join route. `ClientCard`. `/clients` list (grid + summary strip).
8. `/clients/[slug]` detail: open-work (reuse `/work` sort + `InspectionDrawer`), Completed-this-week, Older-completions toggle, Money/Proof/Referral rail.
9. Client tag on Today NOW/UP NEXT rows deep-links to detail.

### Phase 3 — Library + polish
10. `AgentCard` + merged skills+agents source + type filter; promote `/library` to a real page.
11. Systems: confirm unchanged; retire any now-dead links.
12. Update `CLAUDE.md` (nav + cockpit-contract sections) to match shipped IA.

---

## 8. Explicit REMOVE / HIDE list
- **Remove** the `pipeline.jsonl`→collected-cash derivation everywhere; collected cash comes only from `payments`.
- **Remove** the `north-star.md` regex as the app's collected-cash source (keep file for prose/forecast).
- **Remove** the hardcoded "Current June earned income excluding unemployment" detail on the Money "Earned Consulting" card.
- **Hide from nav** (keep as reachable subpages/redirects): `/work`, `/ship`, `/evidence`, `/health`, `/passive-income`, `/tasks`, `/vibe`, `/audit`, `/monitor`, `/costs`, `/legacy/*`.
- **Hide** the old three-lane labels ("Cockpit", "Systems-as-everything") — replaced by the five-lane set.
- **Do NOT build:** the passive-income idea cron (explicitly out of scope). `/passive-income` stays as the existing read-only subpage; no new automation.

---

## 9. Constraints compliance
- ✅ Next.js 15 / Tailwind / Convex only. **No new dependencies** (all new UI from existing tokens + lucide icons already installed).
- ✅ **`score.ts` and `commandQueue` untouched** — collected cash reaches the scorer through the existing `ctx.collected` seam.
- ✅ Extends existing dark tokens; no new palette.
- ✅ Builds stay isolated: `NEXT_DIST_DIR=.next-build` (never write live `.next` under the LaunchAgent).
- ✅ No passive-income cron.
- ⚠️ Requires a `CLAUDE.md` update (nav + cockpit contract) — flagged for approval, not done unilaterally.

---

## 10. Biggest changes from today's design (approve or redirect)

1. **Nav goes 3 → 5 lanes.** Cockpit→**Today**, add **Clients**, keep **Money**, add **Library**, Systems narrows to pure ops health. This overrides the "three lanes / do-not-re-add-to-nav" rule in `CLAUDE.md`, which must be rewritten in the same PR.
2. **Collected cash becomes real, stored data.** New `payments` table replaces the `pipeline.jsonl`/`north-star.md`-regex derivation that structurally reports **$0**. The Money lane now shows **$9,400 collected July MTD ($600 to the gate), $19,400 all-time**, itemized by client and date. This is the single highest-value change and the one you flagged.
3. **The $10K gate stops being an assumption.** Its **basis (monthly vs all-time) becomes a stored `focus.gateBasis` field**, surfaced on the Money card, so the gap number is never ambiguous again. (Recommended default: `monthly`.)
4. **Clients gets a real home** — a roster + per-client detail with open work, completed-this-week, archive toggle, open/collected dollars — reusing the drawer and `/work` ranking, not a new task system.
5. **Library = the existing `/skills` page generalized** to skills **+ agents**, sourced from `~/.openclaw/workspace/skills` and `agents` (the "jt-claude-toolkit" is already synthesized into these; the standalone folder does not exist locally — flagged).
6. **Today barely changes.** Four-band behavior preserved verbatim; only the cash number is re-sourced and client tags deep-link out. `score.ts` is not touched.

**Spec file:** `docs/redesign-spec.md`

**Decisions I need before any code:** (a) approve 5-lane nav + the `CLAUDE.md` rewrite; (b) confirm gate basis default = **monthly**; (c) confirm the `payments` seed values (esp. Karen $1,500 vs $750, and missing `paidOn` dates — see the cash reconciliation from earlier today); (d) confirm Library sources = workspace `skills/` + `agents/` (not the phantom toolkit folder).
