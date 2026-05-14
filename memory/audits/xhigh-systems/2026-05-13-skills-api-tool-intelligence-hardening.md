# Skills / API / Tool Intelligence Hardening — Backlog Prune

Date: 2026-05-13
Executor: subagent `hardening-skills-api-tool-intelligence`
Prior audit: `memory/audits/xhigh-systems/2026-05-13-skills-api-tool-intelligence.md`

## Executive Result

**Before grade:** A-

Reason: the discovery/research loop was already patched and safe, but the Mission Control `Skills` backlog had 60 active tasks, many stale/superseded/generic enough to hide real work.

**After grade:** A

Reason: active `Skills` backlog is now 14 tasks, each retained task has a concrete first action, why-now, and done state. The researcher instructions now enforce a ≤15 backlog cap, required evidence/expiry fields, and skip-to-KB behavior when a finding cannot survive backlog pressure.

A+ is close; remaining gap is execution of the retained tasks, especially OpenClaw v2026.5.10-beta.5 decision, autoresearch cost-cap wrapper, and Agentforce/Data Cloud skill creation.

## Bootstrap Budget Preflight

```
27013 AGENTS.md
19258 MEMORY.md
14496 TOOLS.md
15578 HEARTBEAT.md
```

All bootstrap files were under their hard budgets at task start.

## Before / After Counts

- Active `project=Skills` before: **60**
- Active `project=Skills` after: **14**
- Tasks changed: **60**
- Kept and rewritten as actionable: **14**
- Marked done: **2** (`OpenClaw v2026.5.3` already installed; backlog-prune blocker closed after validation)
- Archived: **44**

## Retained Active Skills Tasks

1. `j57071t61a2ah12sr5pnhp96r586kgdm` — [🔴] OpenClaw v2026.5.10-beta.5 — safety/runtime fixes for Eve (high, sort 20)
2. `j57f1aj7t529vsdajsjkkptwvh86m0pe` — Autoresearch: add deterministic cost-cap wrapper (medium, sort 30)
3. `j57824c4zmj7tj9hmm3q1bhs2x86qrnn` — Fix Spanish weekly evaluation + curriculum progression (medium, sort 40)
4. `j57921fagb0pc697p6z23btfc18239zg` — Skills gap: Wire qmd skill into Opticfy research pipeline (medium, sort 60)
5. `j57atmpdsbfn5akwgh48gc2qpn823kf4` — Skills gap: Activate prompt-library for job application cover letter standardization (medium, sort 70)
6. `j573mpgb5h5n2m7yfwwskvg5r985wj24` — Build Agentforce/Data Cloud implementation skill (medium, sort 80)
7. `j57ack3f758g4vk0prytms6y1n85wd51` — Build AI governance readiness audit skill (medium, sort 90)
8. `j575s36mc8pvh942pfs041m3pn85x6vd` — Build LLM evaluation and monitoring skill (medium, sort 100)
9. `j5784wxtqcexdnmz6qfg11f16h85m2ex` — [🟠] Salesforce Headless 360 — every workflow now API/MCP/CLI (TDX 2026) (medium, sort 110)
10. `j57bm9pcjvw0kksswmcsaqrfjs864wta` — [🟠] HouseCanary MCP — Property valuations agent tool (medium, sort 120)
11. `j571y8kczkznyzmxncwpv69ms98656ry` — [🟠] ATTOM MCP Server — Professional property data access (medium, sort 130)
12. `j574jqfegwx5r598pmwj1887fh869cyr` — [🔴] n8n — Native Microsoft Agent 365 Integration (medium, sort 140)
13. `j57091wmhf98sw44xkj6h5jdpn86drf3` — [🟠] OpenRouter new cheap/free models — smoke-test Gemini 3.1 Flash Lite + Ring-2.6-1T for cron routing (medium, sort 150)
14. `j57bqwm5rrb13h3ar4y570dzj985xz4a` — Research HubSpot AI automation playbook (medium, sort 160)

## Task Changes

### kept+updated (14)

- `j57071t61a2ah12sr5pnhp96r586kgdm` — [🔴] OpenClaw v2026.5.10-beta.5 — safety/runtime fixes for Eve — current/actionable retained task
- `j57f1aj7t529vsdajsjkkptwvh86m0pe` — Autoresearch: add deterministic cost-cap wrapper — current/actionable retained task
- `j57824c4zmj7tj9hmm3q1bhs2x86qrnn` — Fix Spanish weekly evaluation + curriculum progression — current/actionable retained task
- `j57921fagb0pc697p6z23btfc18239zg` — Skills gap: Wire qmd skill into Opticfy research pipeline — current/actionable retained task
- `j57atmpdsbfn5akwgh48gc2qpn823kf4` — Skills gap: Activate prompt-library for job application cover letter standardization — current/actionable retained task
- `j573mpgb5h5n2m7yfwwskvg5r985wj24` — Build Agentforce/Data Cloud implementation skill — current/actionable retained task
- `j57ack3f758g4vk0prytms6y1n85wd51` — Build AI governance readiness audit skill — current/actionable retained task
- `j575s36mc8pvh942pfs041m3pn85x6vd` — Build LLM evaluation and monitoring skill — current/actionable retained task
- `j5784wxtqcexdnmz6qfg11f16h85m2ex` — [🟠] Salesforce Headless 360 — every workflow now API/MCP/CLI (TDX 2026) — current/actionable retained task
- `j57bm9pcjvw0kksswmcsaqrfjs864wta` — [🟠] HouseCanary MCP — Property valuations agent tool — current/actionable retained task
- `j571y8kczkznyzmxncwpv69ms98656ry` — [🟠] ATTOM MCP Server — Professional property data access — current/actionable retained task
- `j574jqfegwx5r598pmwj1887fh869cyr` — [🔴] n8n — Native Microsoft Agent 365 Integration — current/actionable retained task
- `j57091wmhf98sw44xkj6h5jdpn86drf3` — [🟠] OpenRouter new cheap/free models — smoke-test Gemini 3.1 Flash Lite + Ring-2.6-1T for cron routing — current/actionable retained task
- `j57bqwm5rrb13h3ar4y570dzj985xz4a` — Research HubSpot AI automation playbook — current/actionable retained task

### kept+updated_then_done (1)

- `j579v94mtzbafr767qgyt9ey0n86q762` — Skills/API intelligence: prune stale tool backlog — Backlog-prune blocker resolved after validation: active Skills count <=15 and report path recorded.

### marked_done (1)

- `j57eq6fqad8ndbsnsmz2jxn4kh863mxm` — [🟠] OpenClaw v2026.5.3 — New File-Transfer Plugin + Fixes — Marked done 2026-05-13 hardening: local OpenClaw reports 2026.5.3-1 installed; task was for v2026.5.3 fixes.

### archived (44)

- `j5749s63d5kfx6kavsfd99fcwd86dnbx` — [🔴] OpenClaw v2026.5.9-beta.1 — smoke-test Codex harness/runtime fixes before enabling anything — Archived 2026-05-13 hardening: superseded by newer v2026.5.10-beta.5 safety/runtime task.
- `j57cj7fwvs0c7nmrzrqm2ndetd868233` — [🟠] Blend — Autopilot MCP for Lending — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57ccwpnhgt5ykkehx70ve6fks8692hs` — [🟠] Meta — Ads MCP Server Launch — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j573ncn2p23s7jr91c74ysndt986836y` — [🔴] Anthropic — 10 Financial Agent Templates — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57ekdqaz2aecvngp16tap23gn866v8v` — [🟠] OpenClaw 2026.5.5 — reliability fixes for Eve/runtime — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j574wkznhdke3gmp2v74j3rdad865t95` — [🟠] OpenClaw v2026.5.4 — upgrade for plugin/secrets fixes + Gateway performance — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57bvekbbbxa8662n0kd83dfwd8651qj` — [🟠] Claude Design — Collaborative visual collaboration tool — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j579jcrt6aensrt47009b3712n8625sk` — [🟠] DeepSeek V3.1 — Switch Fallback for ~25% Cost Savings — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j570hj9t7cndww1v346z15xvx9863ps8` — [🟠] OpenClaw v2026.5.1 — Upgrade for Codex binary fix + plugin ecosystem expansion — Archived 2026-05-13 hardening: superseded by current/newer OpenClaw release tasks.
- `j57askv145bpv1d3075sr7nsd985w7yz` — Add pre-outreach demo QA gate rule if repeated — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j574wxr8zrrgf675g4kad1sm5h85wg8g` — Create 7-day ops bottleneck audit packager agent — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j579tm9szswv047gsx1j1nv62s85wr2q` — Create cloud architecture proof-map for JT — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j5733sjmx2b41ahb38mm9kvkyd85thkd` — [🟠] OpenClaw v2026.4.26 — Upgrade for Google Live Talk + realtime voice plugins — Archived 2026-05-13 hardening: superseded by newer OpenClaw release tasks.
- `j5708jtyz8653hw8nneegdn9m185pkax` — [🟠] Claude Code v2.1.121 — alwaysLoad MCP + plugin prune cleanup — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j571q8s3590xe88pehc208ksr585mawn` — Add HyperFrames to launch-strategy workflow — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j579fdgmax4d1gz68ce0ha8kkx85nh3x` — Create backlink opportunity map wrapper for AI SEO audits — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j573zx4x41tzy58frzbaxb8yvd85m0h6` — Build Common Crawl backlink lookup utility — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57c33bxr41kj74nbczvwhtkas85mjqj` — Add X API cost/freshness logging to x-research runs — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57267r5tncq0vgp3z43va7q2n85njp1` — Create X Trend Radar digest cron with empty-result guard — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57brzfb6khv92rs646zzad59185nvsg` — Build X Trend Radar query packs for JT niches — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57aybpsag97tdjz5ej4b2sp3n85na90` — Install and test notcrawl only for approved Notion scope — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j573a4ff5mkyemhdf1xejn8abd85m3fw` — Decide approved Notion scope for notcrawl mirror — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j572zkqwpcn6nvgntdv96b554s85n7zg` — Replace brittle Drive/Docs checks with gog read-only helpers — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j571y6xneh7ztg1qewzh4bhzj585mx8x` — Authorize gog with the Eve drafts Google account — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57cj3wa1ypfv52eq6skwmmw7185mnb2` — Wire verified X Lists into recurring intel workflows — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57fytzejww54t462ew2htn8g585nxkf` — Send verified X List URLs/IDs to Eve — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57bcvhcvpdphq460xaad01w8d85m6vr` — Export X archive for birdclaw import — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j5749qxjypdr0j5fdzh2qz6e6185npzf` — Evaluate notcrawl source install for Notion local mirror — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57dzrkftym4nwbkgt4j1n1p9n85mv4t` — Authorize gog Google Workspace CLI for Drive/Docs read workflows — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j570ps660pjb45djcgrnx08ses85nrtv` — Authorize birdclaw X archive import for local content mining — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j570x15szxp90qredckayz4kc985nven` — Create curated X Lists for recurring workflows — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57fc086cwfp84v7n82j85j66185ghym` — [🟠] Clawdi v2.0 — cross-agent sync (iCloud for AI agents) — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57b93kv52q43z3sy4tmhscxsx85h3xx` — [🟠] OpenAI GPT-5.5 Spud — check OpenRouter availability + test routing — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57bxs2feqfkr7zd9p4jcx6b4585cvj6` — [🟠] OpenClaw v2026.4.22 — xAI TTS/image gen + /models add from chat + TUI mode — Archived 2026-05-13 hardening: superseded by newer OpenClaw release tasks.
- `j57dga7s2g6rh6bwpjjeq2gyrx859v5n` — [🟠] Claude Code Routines — automate standardized n8n build sequences — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j575wdfnp8h7kbsjbjfnvd9ve5859wjh` — [🟠] OpenClaw MyClaw — per-agent model picks + 13,700-skill marketplace now live — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57bsqxa4t4c7r97sg5sgmemvx859d08` — [🟠] Shopify Official MCP Server — plug H.C. Oswald catalog into Claude natively — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57c1bnq3b4bq7yd6mdvcfr0hs84yzsq` — Evaluate ZoomInfo — unlock Salesforce PM firm discovery — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j575vreqsac7g2ec95dcnyh4wn84dadj` — AI Video Agent — Build Phase 1 prototype — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j57bjc57ywzyx638r26sxbhby5847pwa` — Drop 2-4 content seeds by Sunday night (30 seconds, huge payoff) — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j573ygb2z1gtefxe06rdnhbzsn845q3j` — 🔴 OpenClaw v2026.4.14 — Update from v2026.3.28 (8-version jump) — Archived 2026-05-13 hardening: superseded by newer OpenClaw v2026.5.x tasks/current v2026.5.10-beta.5 safety task.
- `j57cc890d1gvrbkasya74e2cwh841m71` — Close skill gap: Salesforce Data Cloud Trailhead — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j5756m670nfxx8xykt4ds60y45840nfg` — Close skill gap: Microsoft Copilot Studio (2-3 hrs) — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.
- `j578jb4agt7bcb4rhy9kt0tzbd840p6f` — Write Python AI patterns cheat sheet for JT interview prep — Archived 2026-05-13 hardening: stale/superseded/generic Skills backlog item; no current first-action evidence strong enough to compete with retained ≤15 task set.

## Files Changed

- `agents/skills-researcher/AGENT.md`
  - MC task template now requires exact first action, why-now, done state, source/evidence date, cost/security notes, and expiry/archive condition.
  - Added backlog survivability gate: if open Skills tasks are already ≥15, the researcher must archive a stale/superseded task in the same run or skip MC creation and write to KB/weekly-log only.
  - Tightened priority mapping so 🔴 only becomes HIGH when security/runtime/client-blocking action is needed within 48h.
- `memory/audits/xhigh-systems/2026-05-13-skills-api-tool-intelligence-hardening.md` — this report.

## Validation

```
before_open_skills=60
after_open_skills=14
after_done_active_list=5
archived_skills_total=107

AFTER OPEN SKILLS:
01. j57071t61a2ah12sr5pnhp96r586kgdm | high | sort 20 | 2026-05-12 | actionable=True | [🔴] OpenClaw v2026.5.10-beta.5 — safety/runtime fixes for Eve
02. j57f1aj7t529vsdajsjkkptwvh86m0pe | medium | sort 30 | 2026-05-13 | actionable=True | Autoresearch: add deterministic cost-cap wrapper
03. j57824c4zmj7tj9hmm3q1bhs2x86qrnn | medium | sort 40 | 2026-05-13 | actionable=True | Fix Spanish weekly evaluation + curriculum progression
04. j57921fagb0pc697p6z23btfc18239zg | medium | sort 60 | 2026-03-01 | actionable=True | Skills gap: Wire qmd skill into Opticfy research pipeline
05. j57atmpdsbfn5akwgh48gc2qpn823kf4 | medium | sort 70 | 2026-03-01 | actionable=True | Skills gap: Activate prompt-library for job application cover letter standardization
06. j573mpgb5h5n2m7yfwwskvg5r985wj24 | medium | sort 80 | 2026-05-01 | actionable=True | Build Agentforce/Data Cloud implementation skill
07. j57ack3f758g4vk0prytms6y1n85wd51 | medium | sort 90 | 2026-05-01 | actionable=True | Build AI governance readiness audit skill
08. j575s36mc8pvh942pfs041m3pn85x6vd | medium | sort 100 | 2026-05-01 | actionable=True | Build LLM evaluation and monitoring skill
09. j5784wxtqcexdnmz6qfg11f16h85m2ex | medium | sort 110 | 2026-04-27 | actionable=True | [🟠] Salesforce Headless 360 — every workflow now API/MCP/CLI (TDX 2026)
10. j57bm9pcjvw0kksswmcsaqrfjs864wta | medium | sort 120 | 2026-05-05 | actionable=True | [🟠] HouseCanary MCP — Property valuations agent tool
11. j571y8kczkznyzmxncwpv69ms98656ry | medium | sort 130 | 2026-05-05 | actionable=True | [🟠] ATTOM MCP Server — Professional property data access
12. j574jqfegwx5r598pmwj1887fh869cyr | medium | sort 140 | 2026-05-07 | actionable=True | [🔴] n8n — Native Microsoft Agent 365 Integration
13. j57091wmhf98sw44xkj6h5jdpn86drf3 | medium | sort 150 | 2026-05-09 | actionable=True | [🟠] OpenRouter new cheap/free models — smoke-test Gemini 3.1 Flash Lite + Ring-2.6-1T for cron routing
14. j57bqwm5rrb13h3ar4y570dzj985xz4a | medium | sort 160 | 2026-05-01 | actionable=True | Research HubSpot AI automation playbook
```

Additional validation:
- `agents/skills-researcher/AGENT.md` contains `Backlog cap`, `Expires/archive if`, `Required MC task fields`, and the no-generic-review rule.
- Local OpenClaw version check returned `OpenClaw 2026.5.3-1`; therefore the v2026.5.3 task was marked done, while newer v2026.5.10-beta.5 safety/runtime task was preserved.
- `Skills/API intelligence: prune stale tool backlog` was marked done after active count validated at 14.

## Remaining Blockers

1. Execute the retained high-value tasks; pruning alone does not implement the capabilities.
2. Decide whether to update OpenClaw from 2026.5.3-1 to v2026.5.10-beta.5 in a controlled window.
3. Build deterministic autoresearch cost-cap wrapper.
4. Create/fold Agentforce/Data Cloud, governance, and eval-monitoring skills so consulting delivery IP improves instead of remaining task-board intent.

## Recommendation

Keep the Skills discovery system running, but treat Mission Control as scarce execution inventory. New discoveries that cannot beat the retained top 14 should go to KB/weekly-log, not MC.
