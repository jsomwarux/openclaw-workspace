# North Star Alignment Snapshot - June 2026

Created: 2026-06-11
Scope: information gathering only. No system changes made for this report.

## Source Rules

- File/log ground truth used: `/Users/jtsomwaru/.openclaw/cron/jobs.json`, `/Users/jtsomwaru/.openclaw/cron/runs/*.jsonl`, Mission Control API at `http://localhost:3000/api/tasks`, `reports/`, `docs/audits/`, and project files under `~/projects/jt-consulting-pipeline`.
- Per JT instruction, anything sourced from `MEMORY.md`, `docs/memory/MEMORY-full.md`, or `memory/**` is labeled `UNVERIFIED`.
- No external web research was performed.
- "Stale" is measured against 2026-06-11.

## 1. Income Picture

| Stream | Amounts in files/logs | Status | Dates | Source |
|---|---:|---|---|---|
| Altmark Group - full AI Operations Build | $34,750 total proposed buildout; $1,500/month support, 3-month minimum after buildout | Active paid client; top near-term consulting/proof lane | Proposal/status last updated 2026-05-30 | UNVERIFIED: `memory/clients/altmark-group/status.md` |
| Altmark - Foundation Infrastructure | $4,000 | Paid in full at kickoff per status file | 2026-05-30 status | UNVERIFIED: `memory/clients/altmark-group/status.md` |
| Altmark - Insurance Expiration Tracking | $2,250 | Production launched; final 50% paid | 2026-05-30 status | UNVERIFIED: `memory/clients/altmark-group/status.md` |
| Altmark - Rent Delinquency Outreach | $4,500; initial 50% paid | Active build/test; synthetic dry run passed; waiting on redacted Altmark source export, source path, cadence, reviewer, exception rules | Synthetic run 2026-05-29; review pack 2026-06-06 | UNVERIFIED: `memory/clients/altmark-group/status.md`, `memory/clients/altmark-group/client-os/acceptance-checklist-rent-delinquency.md`, `memory/clients/altmark-group/proof-assets/rent-delinquency-plan-review-pack-2026-06-06.md` |
| Altmark - DHCR Lease Renewal Automation Phase 1 | $3,500; 50% kickoff = $1,750; 50% delivery = $1,750 | Proposal reviewed; sequence after rent delinquency unless Altmark reprioritizes | Proposal review 2026-05-26 | UNVERIFIED: `memory/clients/altmark-group/dhcr-lease-renewal-proposal-review-2026-05-26.md` |
| Altmark - remaining proposed workflows | Loan Management $5,750; WhatsApp AI Bot $9,000; Flagstar to QuickBooks $4,500; Cash Management/Overdraft Prevention $4,750 | Proposed buildout, not confirmed as active in current files | Proposal/status 2026-05-30 | UNVERIFIED: `memory/clients/altmark-group/status.md` |
| Altmark referral upside | No dollar amount for referrals; strategic opportunity says Yair may connect JT to about 15 NYC family offices | Pending proof/acceptance gate | 2026-05-30 status | UNVERIFIED: `memory/clients/altmark-group/status.md` |
| Aya dashboard | $1,500 | Completed proof history | Current memory index | UNVERIFIED: `MEMORY.md` |
| Aya StreetEasy scraper | $1,000 | Active | Current memory index | UNVERIFIED: `MEMORY.md` |
| Aya co-living dashboard | $2,500 | Pending | Current memory index | UNVERIFIED: `MEMORY.md` |
| Aya acquisitions dashboard | NO DATA | Stalled after two follow-ups; task says park 3-4 weeks then one final check-in | Mission Control task active; task created from legacy details | Mission Control API |
| Marketsmith | $175/hr or $15k/month if revived | Watch-only / potential upside; no active next-dollar evidence in current logs | Referenced in North Star review 2026-06-07 | UNVERIFIED: `reports/north-star/2026-06-07-weekly-review.md` |
| JT Somwaru Consulting quick-win Data Anomaly Audit | $500-$1,500 | Packaged entry service idea; not current confirmed revenue | Mission Control task exists | Mission Control API |
| Apps - Vista | NO DATA revenue; app is live on Apple App Store | Active app; measurement/distribution first; no downloads/revenue number found | Registry current | UNVERIFIED: `memory/app-marketing/app-registry.md` |
| Apps - Nash Satoshi | NO DATA revenue; GA4 showed 11 sessions, 7 active users, 15 pageviews, 60 events for week of 2026-06-01 | Active product; monetization not figured out | Scoreboard week 2026-06-01 | UNVERIFIED: `memory/app-marketing/app-registry.md`, `memory/app-marketing/weekly-scoreboard.md` |
| Apps - Glow Index | NO DATA revenue; Search Console 3 impressions and GA4 0 web sessions for week of 2026-06-01 | Active live app; SEO/GEO first; claim-safety constraints | Registry and scoreboard | UNVERIFIED: `memory/app-marketing/app-registry.md`, `memory/app-marketing/weekly-scoreboard.md` |
| Apps - ChargeTrip Fit | Future affiliate path; possible $7 downloadable fit report; possible $19/year watchlist later | Spec-first MVP selected, no build/revenue yet | App ensemble 2026-06-08 | UNVERIFIED: `memory/passive-income/app-idea-ensemble-2026-06-08.md` |
| W2 prospects | $150K minimum; $180K-$220K target; Intradiem Director, Enterprise AI Enablement scored 19/25 but stronger as consulting bridge; ApartmentIQ task says 20/25 or 22/25 if comp clears floor; Salesforce Lead Agentforce SE was submitted at $148K-$198K | Selective/job-market-as-signal; no active employment income | Job market file and Mission Control tasks | UNVERIFIED: `memory/job-market.md`; Mission Control API for active tasks |
| Crypto | NO DATA current P/L or holdings; memory says crypto is JT's primary income stream and x402 is forward bet | Monitoring only; no trades/transfers permitted | Current memory index | UNVERIFIED: `MEMORY.md`; run logs show crypto analyses written, not income |
| Unemployment certification | NO DATA amount | Weekly certification reminder/task exists | Cron run created MC task recently | Cron run logs |

Known monthly run-rate in ground-truth files: NO DATA / unknown. The clearest file-backed current revenue is project-based consulting, with Altmark as the strongest active paid lane.

## 2. Deal And Client State

### Active / High-Relevance Deals

| Name | Stage | Dollar value | Last activity | Staleness | Next action | Source |
|---|---|---:|---|---:|---|---|
| Altmark Group | Active paid client; rent delinquency acceptance gate | $34,750 proposed total; $4,000 foundation paid; $2,250 insurance paid; $4,500 rent delinquency 50% paid; $1,500/mo support after buildout | 2026-06-06 Plan Review Pack; 2026-05-30 status | 5 days from review pack | JT sends/confirms redacted sample export ask: source export, path/process, cadence, reviewer, exception rules | UNVERIFIED: `memory/clients/altmark-group/status.md`, `memory/clients/altmark-group/proof-assets/rent-delinquency-plan-review-pack-2026-06-06.md` |
| Altmark DHCR Lease Renewal Phase 1 | Proposal reviewed; pending after rent delinquency or reprioritization | $3,500; $1,750 kickoff / $1,750 delivery | 2026-05-26 | 16 days | Confirm kickoff/payment, command sheet owner/date, RGB rates, included units/properties, recipients, DHCR rent rolls | UNVERIFIED: `memory/clients/altmark-group/dhcr-lease-renewal-proposal-review-2026-05-26.md` |
| Aya | Prior/active client proof lane | $1,500 completed dashboard; $1,000 StreetEasy active; $2,500 co-living pending; acquisitions value NO DATA | Current memory index; MC acquisitions task legacy active | UNVERIFIED date; acquisitions task stale | StreetEasy/co-living status needs JT/client confirmation; acquisitions final check-in only after parked window | UNVERIFIED: `MEMORY.md`; Mission Control API |
| Petri Plumbing | T2 proof-led prospect; M1 sent | NO DATA | M1 sent 2026-06-01; email enriched 2026-06-02 | 9-10 days | Follow-up-ready after LinkedIn M2 window; verified email `michael@petriplumbing.com` | UNVERIFIED: `memory/consulting/prospect-tier-action-review-2026-06-02.md`; project files in `~/projects/jt-consulting-pipeline/clients/petri-plumbing` |
| HPM / Harlem Property Management | T2 proof-led prospect; M1 sent | NO DATA | M1 sent 2026-06-01; route enriched 2026-06-02 | 9-10 days | Prefer LinkedIn M2 first; email pivot day 8-11 if no reply; route caveat `robb@harlemlofts.com` | UNVERIFIED: `memory/consulting/prospect-tier-action-review-2026-06-02.md`; project files |
| Superior Plumbing & Heating of NYC | T2 proof-led prospect; M1 sent | NO DATA | M1 sent 2026-06-01; email enriched 2026-06-02 | 9-10 days | Follow-up-ready after LinkedIn M2 window; verified route `SUPERIORNYC@VERIZON.NET` | UNVERIFIED: `memory/consulting/prospect-tier-action-review-2026-06-02.md`; project files |
| New York Plumbing Supply | T2 contact-incomplete / wholesale test | NO DATA | Draft/research last file activity 2026-05-15; re-scored 2026-06-02 | 9 days from re-score | Verify Derek Price email; only after proof-led PM/construction follow-ups | UNVERIFIED: `memory/consulting/prospect-tier-action-review-2026-06-02.md`; project files |
| A-List Janitorial Supplies | T2 contact-incomplete / wholesale limited test | NO DATA | Draft/research last file activity 2026-05-07; re-scored 2026-06-02 | 9 days from re-score | Find and verify Steve Argentine email | UNVERIFIED: `memory/consulting/prospect-tier-action-review-2026-06-02.md`; project files |
| Atlantic Global Risk | T2 contact-incomplete / strategic Agentforce proof | NO DATA | Files last activity 2026-05-13; re-scored 2026-06-02 | 9 days from re-score | Verify David Haigh direct LinkedIn/person route and email; no custom demo/deck before channel verified or reply appears | UNVERIFIED: `memory/consulting/prospect-tier-action-review-2026-06-02.md`; project files |
| Human Agency | Job-signal strategy lead, not normal cold outreach | NO DATA | Re-scored 2026-06-02 | 9 days | Find hiring owner or AI implementation lead plus verified email before any outreach | UNVERIFIED: `memory/consulting/prospect-tier-action-review-2026-06-02.md`; `~/projects/jt-consulting-pipeline/prospects/human-agency-job-signal/outreach-draft.md` |
| H.I.G. Capital | Hold / strategy signal | NO DATA | Re-scored 2026-06-02 | 9 days | Do not cold outreach; use as AI enablement operating-system proof/spec signal | UNVERIFIED: `memory/consulting/prospect-tier-action-review-2026-06-02.md` |
| HealthPass | Warm-up only | NO DATA | Outreach preflight 2026-06-11 | 0 days | Warm-up draft exists; do not create full outreach until warmed | Ground truth: `reports/outreach-pipeline/2026-06-11-script-first-preflight.md` |
| Guyana Local Content Summit lane | Connector/operator validation, not standard SMB queue | NO DATA | Summit email drafts revised 2026-06-03; monitor run 2026-06-11 | 0-8 days | Monitor accepts/replies; route through warm connectors; ask for operator perspective, not sales meeting | UNVERIFIED: `memory/drafts/guyana-local-content-summit-email-drafts-2026-06-01.md`; cron run logs for Guyana monitor |
| Marketsmith | Watch-only potential | $175/hr or $15k/month if revived | 2026-06-07 North Star review | 4 days | Pending product-team discovery/follow-up; exact external state not found in current ground files | UNVERIFIED: `reports/north-star/2026-06-07-weekly-review.md` |
| PM Front Desk + Exception Desk proof asset | Proof/distribution asset, not client yet | NO DATA | Mission Control task active, created 2026-06-07/08 | 3-4 days | JT reviews/posts or uses asset in qualified PM/warm-lead reply | Mission Control API |

### Guyana Connector / Operator Lane

Source: UNVERIFIED `memory/consulting/prospect-tier-action-review-2026-06-02.md` and Guyana draft files.

| Name | Stage | Dollar value | Last activity | Next action |
|---|---|---:|---|---|
| Excel Guyana | T2 contact-incomplete; strongest workflow fit | NO DATA | 2026-06-02 | Warm intro first; verify ops/admin/procurement contact + email |
| GLASS / Guyana Logistics and Support Services | T2 contact-incomplete | NO DATA | 2026-06-02 | Warm intro via AmCham/GCCI/logistics network; verify operator + email |
| IGOT Guyana | T2 contact-incomplete | NO DATA | 2026-06-02 | Confirm buyer/contact via GCCI or warm intro |
| TLC Guyana | T2 contact-incomplete | NO DATA | 2026-06-02 | Confirm local operator and verified email |
| AquaTerra Marine Guyana | T2 contact-incomplete | NO DATA | 2026-06-02 | Verify local contact route |
| Lars Mangal / TOTALTEC | T2 connector, not buyer | NO DATA | Email draft 2026-06-03 | Use as operator-intro ask; public email route in draft |
| Kathy Smith / GCCI | T2 connector | NO DATA | Email draft 2026-06-03 | Ask for 1-2 operator/member routes |
| Josephine Tapp / WCCIG | T2 connector | NO DATA | Email draft 2026-06-03 | Ask for operator/member routes |
| Jaysen Toocaram / Newrest | T2 contact-incomplete | NO DATA | Email draft 2026-06-03 | Verify Jaysen-specific route or use supplier inbox carefully |
| Iman Cummings / AmCham | T2 connector | NO DATA | Email draft 2026-06-03 | Use Richard Leo route first if he replies; fallback to AmCham inbox only if JT chooses |
| Chandradat Chintamani, Dominique Fraser, John Percival, Elchin Rzayev, Natina Singh | Research/connection lane | NO DATA | 2026-06-02 | Send only after accept or if JT expands Summit lane |

### Consulting Pipeline Client/Prospect Files Found

These are findable in `~/projects/jt-consulting-pipeline/clients`. Dollar value is `NO DATA` unless stated elsewhere above. Stage reflects file state only, not live external status.

| Prospect/client | Stage from files | Last file activity | Staleness |
|---|---|---:|---:|
| A-List Janitorial Supplies | T2 draft/research/brief | 2026-05-07 | 35 days |
| Aarco Contracting | T2 draft/research/brief | 2026-05-13 | 29 days |
| AFGO Mechanical | T2 draft/research | 2026-04-15 | 57 days |
| Air Tactical HVAC Services | T2 draft/research/brief | 2026-05-13 | 29 days |
| Aladdin Plumbing | Draft/research; email route found | 2026-05-22 | 20 days |
| AMAF Supply Inc | Warm-up file only | 2026-05-19 | 23 days |
| AssuredPartners | T2 draft/research | 2026-03-22 | 81 days |
| Atlantic Global Risk | T2/T3 draft/research/brief; active re-score says T2 contact-incomplete | 2026-05-13 | 29 days |
| Atlas NYC Property Management | T2 draft/research/brief; send evidence in files | 2026-05-13 | 29 days |
| BenefitsGuide | Warm-up file only | 2026-05-24 | 18 days |
| Biz2Credit | Draft/research | 2026-04-21 | 51 days |
| BJD Property | T2 draft/research; send evidence in files | 2026-04-15 | 57 days |
| Brick Property Mgmt | T2 draft/research | 2026-03-22 | 81 days |
| Brothers Supply | T2 draft/research/brief; send evidence in files | 2026-05-13 | 29 days |
| Citadel Property | T2 draft/research; send evidence in files | 2026-04-15 | 57 days |
| Common Living | Draft/research; Agentforce PM draft exists | 2026-04-21 | 51 days |
| Conner Strong | Draft/research; send evidence in files | 2026-05-13 | 29 days |
| Dirty Gloves Drain | Draft/research | 2026-05-22 | 20 days |
| Distinguished Programs | T2 draft/research | 2026-03-22 | 81 days |
| FCM Real Estate | T2 draft/research/brief; send evidence in files | 2026-05-13 | 29 days |
| Five Boro Building Supply | Warm-up file only | 2026-05-19 | 23 days |
| G&G Electric | T2 draft/research; send evidence in files | 2026-05-13 | 29 days |
| G-Net Construction | T2 draft/research/brief | 2026-05-13 | 29 days |
| Gil Meyerowitz Inc | Warm-up file only | 2026-05-19 | 23 days |
| Globe Electric | T2 draft/email; send evidence in files | 2026-04-01 | 71 days |
| H.C. Oswald | Research/brief/deck/workflow files; memory says paused until site/demo proof improves | 2026-05-13 | 29 days |
| HealthPass | Warm-up only per preflight | 2026-05-23 | 19 days |
| Henick Lane | T2 draft/research; send evidence in files | 2026-04-15 | 57 days |
| HPM / Harlem Property Management | T2 sent/research/brief; contact route found | 2026-06-02 | 9 days |
| HubSpot MCP Insurance Demo | Demo/brief artifact | 2026-04-19 | 53 days |
| HubSpot T2 Template | Template/brief artifact | 2026-04-12 | 60 days |
| Independent Pipe | T2 sent/research/brief | 2026-05-13 | 29 days |
| L. Richards Plumbing | Warm-up file only | 2026-05-24 | 18 days |
| Lawley Insurance | T3 sent/research/deck URL | 2026-05-13 | 29 days |
| Madison Insurance Group | T2 warm-up/draft/brief | 2026-05-21 | 21 days |
| Maxwell Plumb Mechanical | T2 draft/research/brief | 2026-05-13 | 29 days |
| Michaels Electrical Supply | T2 draft/research/brief | 2026-05-13 | 29 days |
| MyPropertyMan | T2 sent/research/brief | 2026-05-13 | 29 days |
| New York Heating | T2 warm-up/draft/research | 2026-04-28 | 44 days |
| New York Plumbing Supply | T2 draft/research; active re-score says contact-incomplete | 2026-05-15 | 27 days |
| Park Ave Building | T2 sent/research | 2026-04-15 | 57 days |
| Petri Plumbing | T2 sent/research/brief; verified email | 2026-06-02 | 9 days |
| Premier HVAC | T2 sent/research | 2026-05-13 | 29 days |
| ProRealty USA | Sent/research | 2026-05-13 | 29 days |
| Rampart Insurance | T3 draft/research/brief | 2026-05-13 | 29 days |
| REM Residential | T2 draft/research | 2026-05-13 | 29 days |
| RSI MGA | T3 draft/research | 2026-04-14 | 58 days |
| S B Electric Supply Corp | Warm-up file only | 2026-05-19 | 23 days |
| SDL GHS | Sent/research | 2026-04-01 | 71 days |
| Silvercrest | Agentforce/RIA draft/research/brief | 2026-05-13 | 29 days |
| Spring Health | Agentforce/healthcare draft/research | 2026-04-21 | 51 days |
| Sterling Sanitary Supply | Warm-up file only | 2026-05-24 | 18 days |
| Superior Plumbing & Heating of NYC | T2 sent/research/brief; verified route | 2026-06-02 | 9 days |
| T.F. O'Brien | Warm-up file only | 2026-05-24 | 18 days |
| Weather Makers NYC | Warm-up file only | 2026-05-24 | 18 days |
| Webster Plumbing | T2 sent/research | 2026-04-15 | 57 days |
| The Whitmore Group | T3 draft/research/brief | 2026-05-13 | 29 days |
| Wynne Plumbing | T2 sent/research | 2026-04-15 | 57 days |

### Mission Control Items With Deal/Revenue Relevance

| Task | Stage | Dollar value | Last update | Staleness | Next action |
|---|---|---:|---|---:|---|
| Review/post PM Front Desk + Exception Desk proof | Active high-priority proof/distribution | NO DATA | 2026-06-08 | 3 days | JT posts or uses the asset in one qualified PM/warm-lead reply |
| Apply Plan Review Pack to Altmark rent delinquency gate | Done | Tied to Altmark $4,500 workflow | 2026-06-06 | 5 days | JT reviews pack, sends sample request or confirms inputs exist |
| Apply to ApartmentIQ AI Operations Lead | Active W2 prospect | Salary not confirmed; task says 20/25 role, 22/25 if comp plausibly $150K+ | 2026-06-08 | 3 days | JT opens live posting and applies only if comp clears floor |
| ChargeTrip Fit build-spec task | Active passive-income product spec | Future affiliate/$7/$19 paths only; current revenue NO DATA | 2026-06-08 | 3 days | Eve can draft spec-first MVP under sanctioned content/product-prep lane only if prioritized |
| Nash Satoshi conversion-focused landing page | Passive-income conversion patch | NO DATA | Mission Control active | Unknown | Audit promise/CTA/proof/mobile/ranking explanation; replace with scoped patch if selected |
| Data Anomaly Audit quick-win service | Consulting service idea | $500-$1,500 | Mission Control active | Unknown | Add service one-pager/materials if selected |
| Aya acquisitions dashboard | Stalled engagement | NO DATA | Mission Control active, legacy | Unknown | Parked; one final check-in after 3-4 weeks if still relevant |

## 3. Job-To-Goal Mapping For 53 Enabled Cron Jobs

Lanes: consulting cash engine; proof and IP; apps; crypto scanning; health and stability; ops and meta.

| Cron job | Lane | Last 30-day concrete outputs from run logs | Vote | Reasoning |
|---|---|---|---|---|
| Morning Brief | ops and meta | 104 runs; latest delivered brief with Altmark, PM proof, runtime drift priorities | DEEPEN | It is the daily control surface; deepen by keeping it focused on next-dollar gates and Send Queue, not more sections. |
| Weekly Health Report | health and stability | 18 runs; latest output says report could not run because command tool unavailable | KEEP | Health is foundational, but output reliability is mixed; keep until health data path is fixed. |
| Job Market Daily Research | proof and IP | 109 runs; 80 ok/29 error; latest error from tool/file read; produced job-market briefs used as positioning intel | KEEP | Useful for W2 optionality and consulting language, but not a primary cash engine. |
| Niche Intelligence Monitor | consulting cash engine | 77 runs; latest `NEW_HIGH_FINDINGS_LOGGED_AND_SENT` | DEEPEN | Directly tunes ICP/pitch criteria; worth keeping close to outreach and PM/property lanes. |
| Weekly Intelligence Synthesis | proof and IP | 17 runs; updated ICPs, cold-email skill, strategic recommendations, weekly intel brief; created MC task | KEEP | Good synthesis loop; no need to expand unless it moves a live outreach/proof action. |
| Crypto Full Analysis (6 AM) | crypto scanning | 109 runs; latest wrote `latest-analysis.md`, Telegram summary, history, allocation-history JSON | DEEPEN | Primary crypto signal pipeline; keep high-quality/freshness because crypto is a stated income lane. |
| Crypto Midday Pulse (12 PM) | crypto scanning | 105 runs; latest `NO_ALERT_LOGGED` | KEEP | Intraday risk/opportunity check; keep if low-noise. |
| Crypto Evening Pulse (9 PM) | crypto scanning | 101 runs; latest auth cooldown error | KEEP | Keep, but current output reliability is weaker than morning/midday. |
| Pending Task Processor | ops and meta | 426 runs; latest no-op/check behavior | KEEP | Prevents deferred work from disappearing; high volume but operationally useful. |
| Viral Post Swipe File - X Research | proof and IP | 46 runs; latest auth cooldown error; feeds content corpus/swipe file | KEEP | Supports distribution quality; keep but do not let it outrank client proof. |
| Skills & API Researcher - Daily Scan | ops and meta | 97 runs; latest found OpenClaw runtime upgrade smoke and created MC task/sent Telegram | KEEP | Useful for capability/risk awareness; keep constrained to actionable high signals. |
| Skills & API Researcher - Weekly Synthesis | ops and meta | 15 runs; latest sent weekly synthesis, added KB items, archived/reset logs | KEEP | Good weekly hygiene; not a revenue driver but protects operating leverage. |
| Monthly Goal-Skills Gap Analysis | proof and IP | 4 runs; latest updated training log, created 6 MC tasks, sent Telegram | KEEP | Useful monthly calibration; enough at current cadence. |
| Health Check-in (Pattern-Focused) | health and stability | 101 runs; mostly delivered; latest output text indicates a tool availability failure in-run | KEEP | Health layer matters; ensure real check-in freshness before making workload claims. |
| Monthly Niche Fitness Review | consulting cash engine | 4 runs; latest shifted June GTM to property ops first, construction second, wholesale limited-test | DEEPEN | Directly aligned with consulting cash engine. |
| Weekly Strategic Gut-Check | ops and meta | 16 runs; latest delivered gut-check to Telegram | KEEP | Useful strategic friction check; keep but avoid duplicating North Star review. |
| Daily News Hook | proof and IP | 72 runs; latest saved/sent CNBC bank AI agents hook with 20% sales lift / 50% coverage datapoint | KEEP | Helps content stay timely; keep if it feeds proof-led posts. |
| Job Application Tracker | proof and IP | 29 runs; latest no stale or urgent active applications | KEEP | Low-cost W2 optionality; keep selective. |
| content-reminder | proof and IP | 66 runs; latest blocked a repetitive X send despite guard pass | KEEP | Good distribution guard; keep because it prevents stale/low-quality posting. |
| content-sunday | proof and IP | 13 runs; latest sent Sunday LinkedIn + X and wrote pending posted-reply state | KEEP | Useful weekly distribution, but watch duplication with new content crons. |
| outreach-pipeline | consulting cash engine | 97 runs; latest preflight PASS, 0 eligible copy-review items, 1 warm-up hold, 57 skipped, no sends | DEEPEN | Core consulting pipeline safety/scanner; deepen around proof-led active prospects only. |
| prospect-discovery | consulting cash engine | 26 runs; latest auth cooldown error | KEEP | Prospect sourcing matters, but current output should stay gated by tier/contact rules. |
| t3-cold-hook | consulting cash engine | 29 runs; latest tool/API failure; earlier created low-priority T3 batches | CUT | T3 volume is not the next-dollar lane; cut or keep dormant unless contact completeness and re-score justify it. |
| vibe-marketing-generate | apps | 16 runs; latest not-delivered / Codex stopped before confirmation | KEEP | App distribution matters, but reliability must be verified before deepening. |
| content-generate-linkedin | proof and IP | 16 runs; latest delivered weekly LinkedIn queue, Drive doc, guard pass | DEEPEN | Directly builds public proof; now corpus-first/Sonnet and worth using for consulting authority. |
| content-generate-x | proof and IP | 17 runs; latest delivered X queue, Drive doc, Notion 7/7 slots | KEEP | Useful distribution engine; deepen only if metrics/replies show buyer signal. |
| Weekly Systems Review | ops and meta | 16 runs; latest tool failure; now KPI-based by Phase 7 prompt | KEEP | Essential maintenance loop, but should stay systems-only. |
| reddit-karma-daily-reminder | proof and IP | 85 runs; latest auth cooldown error; now digest-queue style | CUT | Low direct revenue/proof leverage relative to noise unless tied to specific app/community KPI. |
| weekly-unemployment-cert | health and stability | 14 runs; latest created MC task for unemployment certification | KEEP | Practical financial stability support; keep. |
| Job Application Auto-Builder | proof and IP | 83 runs; latest no qualified active job application | KEEP | Keep selective; do not build packages without qualifying role. |
| passive-income-fetch-signals | apps | 10 runs; latest source file status check across trend/API sources | KEEP | Supports app ideation, but should stay subordinate to consulting proof. |
| Weekly Seeds Prompt | apps | 10 runs; latest sent seeds prompt to Telegram | CUT | Too generic unless it produces selected, measured app moves. |
| Build Ideas Sync | apps | 63 runs; latest pushed 0, skipped 17 | CUT | Current outputs show backlog churn, not income; reduce unless tied to selected app gates. |
| critical-files-integrity | health and stability | 60 runs; latest `INTEGRITY_OK`; now includes cron snapshot | KEEP | Core reliability/proof guard; keep. |
| passive-income-scout | apps | 11 runs; latest Codex stopped before confirming | KEEP | Keep weekly scout only if it feeds ranked app decisions, not idea sprawl. |
| passive-income-strategist | apps | 10 runs; latest evaluated no scout file and wrote 2026-06-07 strategist path | KEEP | Useful when paired with app-idea ensemble and gates. |
| outreach-email-pivot-daily | consulting cash engine | 59 runs; latest no eligible prospects | KEEP | Good safety net for follow-up route; keep if it only acts on verified prospects. |
| dynasty-replies-gen | apps | 53 runs; latest generated Dynasty X reply targets | KEEP | Supports sports product/audience lane; keep if engagement data exists. |
| reddit-daily-gen | proof and IP | 54 runs; latest generated Reddit growth drop from fresh crypto policy signal | KEEP | Can support app/crypto distribution; keep but avoid promotional spam. |
| guyana-economic-opportunity-monitor | consulting cash engine | 7 runs; latest delivered Guyana Local Content Summit signal | DEEPEN | Strongest non-NYC relationship wedge; deepen as connector validation, not cold selling. |
| Sports GM Weekly Market Report | apps | 6 runs; latest auth cooldown error | KEEP | Supports Dynasty/Action Arena content lane; not near-term revenue. |
| Daily DynastyJig Niche-Growth X Post Pack | apps | 45 runs; latest saved pack and sent Telegram review packet | KEEP | Supports sports audience, but needs metrics to justify daily cadence. |
| Weekly North Star Command Center | ops and meta | 7 runs; latest delivered 2026-06-07 review with income gaps and top actions | DEEPEN | Best alignment cron; deepen its use as decision input, not add new system changes. |
| ReelFarm Daily Strategy Intel | apps | 41 runs; latest auth cooldown error; earlier wrote strategy reports | KEEP | Useful for app distribution, but daily cadence may be high without metrics. |
| ReelFarm Weekly Strategy Synthesis | apps | 5 runs; latest saved weekly report and sent strategic shift | KEEP | Better than daily for app strategy; keep. |
| app-marketing-weekly-scoreboard | apps | 7 runs; latest reported Nash web 11 sessions/7 active users/15 pageviews/60 events; Glow 0 GA4 sessions | DEEPEN | This is the app lane's measurement spine. |
| Autoresearch Sweep | ops and meta | 14 runs; latest auth cooldown error | KEEP | Useful for skill/agent quality, but not a revenue priority. |
| AI Ops Teardown Weekly Draft | proof and IP | 4 runs; latest not-delivered / Codex stopped before confirmation | DEEPEN | Strong fit for consulting proof if it reliably produces buyer-readable assets. |
| passive-income-strategist-delivery-guard | apps | 2 runs; latest FAILED because delivery marker missing despite report | KEEP | Guard is useful because passive-income reports otherwise disappear. |
| Reminder: YouTube TV midday | health and stability | 0 runs in last 30 days; scheduled one-time 2026-06-25 | CUT | Not North Star aligned except personal reminder; should not compete with core system attention. |
| TikTok App Account Warm-up Reminder (2 PM) | apps | 6 runs; latest delivered warm-up instruction for Vista/Nash/Glow accounts | KEEP | App accounts need trust before posting; keep until manual posting cadence stabilizes. |
| Evening Digest | ops and meta | 0 runs yet; newly added 7 PM digest queue | KEEP | Should reduce notification noise; needs first natural run evidence. |
| Night Autonomy Agent | ops and meta | 0 runs yet; newly added 11 PM merged agent | DEEPEN | Potentially high leverage if it completes one artifact per night inside sanctioned lanes; first run still unproven. |

## 4. Top Revenue Moves

These are ranked by likely income impact in the next 30 days. They are not system-change recommendations; they are actions and what Eve can prepare under existing sanctioned lanes.

1. Close the Altmark rent delinquency acceptance gate.
   - Why: It is the clearest next-dollar path in the files: active paid workflow, initial 50% already paid, synthetic smoke passed, and support/referral upside depends on acceptance.
   - Eve can autonomously prepare: a client-safe redacted-sample request packet, review-only run checklist, proof-safe output summary template, acceptance wording draft, and support-scope draft. JT must send/client-confirm.

2. Turn Altmark proof into a family-office/property-ops referral packet after acceptance.
   - Why: Files say Yair may connect JT to about 15 NYC family offices; support retainer is $1,500/month after buildout; one warm family-office diagnostic/build is the fastest credible +$10K/mo path in the North Star review.
   - Eve can autonomously prepare: anonymized proof spine, before/after workflow map, one-page "property ops workflow control layer" asset, referral ask draft, and target qualification checklist. JT/client permission required before use.

3. Execute the Petri / HPM / Superior follow-up lane with verified route discipline.
   - Why: They are the freshest proof-led T2 prospects with M1 sent 2026-06-01 and contact enrichment completed 2026-06-02.
   - Eve can autonomously prepare: M2/email pivot drafts, proof-safe PM/construction asset attachments, reply triage matrix, and Mission Control state cleanup. JT must send.

4. Use the PM Front Desk + Exception Desk proof asset as a public/warm-lead distribution piece.
   - Why: Mission Control has it high-priority; North Star review calls it the best proof asset to reuse in property-ops outreach without named Altmark claims.
   - Eve can autonomously prepare: LinkedIn post, short X variant, reply/DM version, and buyer-readable one-pager with no client-private claims. JT must post/send.

5. Apply only to W2 roles that clear the $150K+ non-developer filter, starting with ApartmentIQ if live comp clears.
   - Why: W2 is not the primary strategy, but one high-fit AI Ops role can materially change income. Mission Control has ApartmentIQ as 20/25 or 22/25 if compensation clears floor; job-market logs surfaced Intradiem as a 19/25 signal but stronger as consulting positioning.
   - Eve can autonomously prepare: live-posting verification packet, resume/cover letter package if the role clears filters, and proof alignment bullets. JT must submit.

## 5. Blind Spots

Specific missing information blocking a managed consulting pipeline:

1. Confirmed monthly income baseline.
   - Missing: current consulting cash collected by month, expected collection dates, any recurring retainers, app revenue, crypto income/P&L, unemployment amount, and W2 application outcomes.

2. Altmark payment and acceptance truth after 2026-05-30.
   - Missing: whether the rent delinquency redacted export was sent, whether Altmark named a reviewer, whether exception rules were confirmed, whether remaining 50% is invoiced/paid, and whether DHCR kickoff/payment moved forward.

3. Aya current truth.
   - Missing: StreetEasy scraper status, co-living dashboard decision, whether the $2,500 pending scope is still live, and whether the acquisitions dashboard should get a final check-in or be closed.

4. Prospect reply state.
   - Missing: whether Petri, HPM, Superior, Guyana contacts, or any prior T2/T3 prospects accepted/replied outside the logged files. The pipeline has drafts and tasks, but not a single canonical reply ledger with current external status.

5. Contact verification completeness.
   - Missing: verified direct emails for many T2/T3 prospects; exact source confidence; which LinkedIn-only prospects are intentionally parked versus awaiting enrichment.

6. JT send/post confirmations.
   - Missing: final URLs or "sent" confirmations for many drafted assets. Eve cannot safely close loops without JT-provided send/post results.

7. App monetization and analytics access.
   - Missing: Vista App Store downloads/ratings/conversion, Nash CTA clicks/account growth, Glow traffic beyond low Search Console/GA4 snippets, TikTok/ReelFarm metrics, and any revenue/affiliate data.

8. Crypto income picture.
   - Missing: holdings, realized/unrealized P/L, position sizing, x402 thesis status, and what "primary income" means numerically. Eve should not infer or act financially.

9. W2 application status.
   - Missing: whether ApartmentIQ is still live and salary-confirmed, Salesforce application response status, Guyana Growth resume send status, and whether Intradiem deserves an application or only positioning reuse.

10. Health/energy currentness.
   - Missing: fresh health check-in pattern. North Star review says health data is stale, so workload capacity and deep-work recommendations are under-specified.

11. Pipeline economics.
   - Missing: standard offer prices by ICP, close probability by tier, expected cycle length, current open proposal count, and which prospects can realistically close within 30 days.

12. External-party pending queue.
   - Missing: canonical list of "waiting on Yair", "waiting on Aya", "waiting on prospect reply", "waiting on JT send", and due dates. The data exists in fragments but not as one current managed-system ledger.

## Compact Source Index

- Cron inventory: `/Users/jtsomwaru/.openclaw/cron/jobs.json`
- Cron outputs: `/Users/jtsomwaru/.openclaw/cron/runs/*.jsonl`
- Mission Control tasks: `http://localhost:3000/api/tasks`
- Outreach preflight: `reports/outreach-pipeline/2026-06-11-script-first-preflight.md`
- North Star reviews: `reports/north-star/2026-06-07-weekly-review.md`, `reports/north-star/2026-05-31-weekly-review.md`
- Altmark files: `memory/clients/altmark-group/status.md`, `memory/clients/altmark-group/client-os/acceptance-checklist-rent-delinquency.md`, `memory/clients/altmark-group/proof-assets/rent-delinquency-plan-review-pack-2026-06-06.md`, `memory/clients/altmark-group/dhcr-lease-renewal-proposal-review-2026-05-26.md`
- App files: `memory/app-marketing/app-registry.md`, `memory/app-marketing/weekly-scoreboard.md`, `memory/passive-income/app-idea-ensemble-2026-06-08.md`
- Job market: `memory/job-market.md`
- Consulting prospect review: `memory/consulting/prospect-tier-action-review-2026-06-02.md`
- Consulting pipeline client dirs: `~/projects/jt-consulting-pipeline/clients/*`
