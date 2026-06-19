#!/usr/bin/env python3
"""Generate deduped Mission Control tasks for App Marketing OS.

Reads App Marketing OS state files and pushes the next optimal tasks per app.
Default is dry-run. Use --execute to create/update Mission Control tasks.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MC_URL = "http://localhost:3000/api/tasks"
OUT_PATH = ROOT / "memory/app-marketing/generated-mission-control-tasks.json"


@dataclass
class TaskSpec:
    title: str
    description: str
    priority: str
    assignee: str
    project: str
    sortOrder: int
    slug: str
    app: str
    category: str
    reason: str


def read_text(rel: str) -> str:
    p = ROOT / rel
    return p.read_text() if p.exists() else ""


def fetch_tasks() -> list[dict[str, Any]]:
    try:
        with urllib.request.urlopen(MC_URL, timeout=8) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Mission Control task API unavailable: {e}") from e
    if isinstance(payload, dict) and isinstance(payload.get("tasks"), list):
        return payload["tasks"]
    if isinstance(payload, list):
        return payload
    raise RuntimeError(f"Unexpected Mission Control response shape: {type(payload).__name__}")


def post_task(task: TaskSpec) -> dict[str, Any]:
    body = json.dumps({
        "title": task.title,
        "description": task.description,
        "status": "todo",
        "priority": task.priority,
        "assignee": task.assignee,
        "project": task.project,
        "sortOrder": task.sortOrder,
        "slug": task.slug,
    }).encode("utf-8")
    req = urllib.request.Request(
        MC_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:90]


def existing_keys(tasks: list[dict[str, Any]]) -> set[str]:
    keys = set()
    for t in tasks:
        title = (t.get("title") or "").strip().lower()
        slug = (t.get("slug") or "").strip().lower()
        if title:
            keys.add(title)
        if slug:
            keys.add(slug)
    return keys


def mk(title: str, app: str, category: str, priority: str, assignee: str, sort_order: int, first_action: str, why: str, done: str, refs: list[str], guardrail: str = "") -> TaskSpec:
    desc = (
        f"First action: {first_action}\n\n"
        f"Why it matters: {why}\n\n"
        f"Done looks like: {done}\n\n"
        f"References:\n" + "\n".join(f"- {r}" for r in refs)
    )
    if guardrail:
        desc += f"\n\nGuardrail: {guardrail}"
    return TaskSpec(
        title=title,
        description=desc,
        priority=priority,
        assignee=assignee,
        project="App Marketing",
        sortOrder=sort_order,
        slug="app-marketing-" + slugify(title),
        app=app,
        category=category,
        reason=why,
    )


def build_task_specs() -> list[TaskSpec]:
    registry = read_text("memory/app-marketing/app-registry.md")
    weekly = read_text("memory/app-marketing/weekly-scoreboard.md")
    exp = read_text("memory/app-marketing/experiment-calendar.md")
    durable = read_text("memory/app-marketing/durable-discovery-plan.md")

    _ = (registry, weekly, exp, durable)

    # 2026-06-18 Opus reset: keep generated tasks concentrated on measurement,
    # Action Arena's submission gate, and Glow SEO. Paid UGC is paused except
    # a future capped Action Arena kickoff test after app-live + attribution
    # gates. Older all-app/share-artifact tasks remain below for history but
    # are intentionally unreachable.
    tasks: list[TaskSpec] = []

    tasks.append(mk(
        "App Marketing OS: execute Opus strategy reset - measurement, Action Arena gate, Glow SEO bet",
        "All apps", "strategy-reset", "high", "eve", 18,
        "Open `memory/app-marketing/opus-strategy-reset-2026-06-18.md`, then update the weekly scoreboard with Action Arena gate status, Glow crawler/indexing state, Nash cap status, and Vista hold status.",
        "The app portfolio was drifting into all-app work. The reset keeps consulting first, closes the Action Arena gate, makes Glow the only ongoing app bet, caps Nash, and parks Vista.",
        "One Friday-ready scoreboard section exists with push/cap/pause/gate decisions and the active Mission Control app-marketing layer matches the reset.",
        ["memory/app-marketing/opus-strategy-reset-2026-06-18.md", "memory/app-marketing/weekly-scoreboard.md", "memory/app-marketing/app-registry.md"],
        "No new app features, no external posting automation, no daily Nash cadence, no Vista/ReelFarm scaling, no paid creators except the gated Action Arena kickoff test."
    ))

    tasks.append(mk(
        "Action Arena: clear Apple Developer org transfer, then EAS/App Store readiness",
        "Action Arena", "submission-gate", "high", "eve", 19,
        "Open `memory/app-marketing/action-arena-submission-gate-2026-06-18.md`, track the Apple Developer Organization transfer under the LLC, then after it clears confirm EAS project secrets and App Store Connect/TestFlight status from `/Users/jtsomwaru/projects/action-arena`.",
        "Action Arena is the only timed gate. Source is now found, and JT is moving the Apple Developer membership from individual to organization because in-app purchases blocked individual submission; that Apple-side blocker must clear before commissioner outreach or creator tests can convert.",
        "Apple Developer organization status is recorded, EAS secrets/status are confirmed after the transfer clears, the latest TestFlight/App Store Connect state is recorded, one next submission/build action exists, and optional UGC remains locked until app live + attribution ready.",
        ["memory/app-marketing/opus-strategy-reset-2026-06-18.md", "memory/app-marketing/action-arena-submission-gate-2026-06-18.md", "memory/app-marketing/action-arena-launch-checklist-2026-05-26.md"],
        "Do not run broad dependency upgrades inside this gate. Keep no-real-money positioning. Do not brief/pay creators before app-live + attribution gates."
    ))

    tasks.append(mk(
        "Glow Index: register GA4 source_tag and run 72h/7d SEO checks",
        "Glow Index", "seo-page-build", "high", "eve", 20,
        "Register event parameter `source_tag` as an event-scoped custom dimension in GA4 property `537965547`, then re-run Data API checks for `customEvent:source_tag`, `/rankings` page paths, `view_product`, and Search Console page/query rows.",
        "The first SEO/GEO batch is live and baseline is written, but GA4 rejects `customEvent:source_tag` as an invalid dimension. Without this setup, the site can collect page/event data but cannot segment the SEO/GEO source tags.",
        "`memory/app-marketing/glow-post-deploy-measurement-2026-06-18.md` or a follow-up dated note records source-tag dimension queryability, 72h check, 7d check, GSC rows, GA4 page/event counts, and the next-deploy yes/no recommendation.",
        ["memory/app-marketing/glow-post-deploy-measurement-2026-06-18.md", "memory/app-marketing/glow-first-five-money-pages-2026-06-18.md", "memory/app-marketing/measurement-spine.md"],
        "No new Replit rebuild, no new category/methodology page, no medical/treatment claims, no fake testimonials, and no before/after claims until measurement says the next page is worth the deploy cost."
    ))

    tasks.append(mk(
        "Glow Index: choose first five money pages after crawler gate",
        "Glow Index", "seo-pages", "high", "eve", 21,
        "After crawler access is clean, choose the first five pages by intent, affiliate fit, available product data, and claim safety; save the page queue with target query, direct-answer block, schema, and measurement tag.",
        "Glow's upside is asynchronous SEO/GEO. The page queue must be chosen by winnability and monetization, not generic volume.",
        "`memory/app-marketing/glow-first-five-money-pages-2026-06-18.md` exists with five pages, source tags, build order, claim guardrails, and indexing checks.",
        ["memory/app-marketing/glow-seo-first-page-plan-2026-06-01.md", "memory/app-marketing/glow-10-verdict-pages-status-2026-05-19.md", "memory/app-marketing/measurement-spine.md"],
        "No medical/treatment claims; no fake before/after or testimonials; no dupe pages without structured similarity criteria."
    ))

    tasks.append(mk(
        "Nash Satoshi: enforce weekly receipt cap and kill daily generic cadence",
        "Nash Satoshi", "content-cap", "medium", "eve", 60,
        "Update Nash app-marketing routines so only one weekly human-reviewed ranking-delta/model-disagreement receipt is eligible, measured by methodology-page clicks and waitlist signups.",
        "Nash has a real methodology wedge but is the highest distraction/compliance-risk app. Impressions without clicks are fake momentum.",
        "Weekly review records either one approved receipt with source tag and click/signup metrics, or `NO_NASH_RECEIPT_THIS_WEEK` because no strong delta/disagreement exists.",
        ["memory/app-marketing/app-registry.md", "memory/app-marketing/measurement-spine.md"],
        "No financial advice, no price predictions, no performance claims, no automated posting."
    ))

    tasks.append(mk(
        "Vista: keep paused and archive immediate-growth tasks unless un-pause trigger fires",
        "Vista", "pause", "low", "eve", 120,
        "Review active Vista App Marketing tasks and archive/demote anything that implies immediate share-card builds, directory pushes, or ReelFarm scaling.",
        "Vista is the clearest overbuilding trap. It can be monitored, but it should not consume current app-marketing execution time.",
        "The active board has no high-priority Vista execution tasks except passive measurement or an explicit un-pause trigger note.",
        ["memory/app-marketing/app-registry.md", "memory/app-marketing/opus-strategy-reset-2026-06-18.md"],
        "Un-pause only on proven share-to-install loop or consulting cash at $10K/month."
    ))

    return tasks

    tasks.append(mk(
        "App Marketing OS: create share-artifact specs for Vista, Nash, and Glow",
        "All apps", "share-artifact", "high", "eve", 20,
        "Open `memory/app-marketing/share-artifact-roadmap.md` and turn each primary artifact into a build-ready spec: Vista Movie Taste Card, Nash Weekly Ranking Receipt Card, Glow Product Verdict Card.",
        "Product-led share artifacts are the highest-leverage missing acquisition loop; without them, posting is mostly external push instead of user/creator pull.",
        "Three spec files exist under `memory/app-marketing/share-artifacts/` with fields, visual layout, export sizes, data inputs, guardrails, and repo/app implementation notes; follow-up coding tasks are created if app changes are needed.",
        ["memory/app-marketing/share-artifact-roadmap.md", "memory/app-marketing/revised-operating-model-2026-05-19.md"],
        "Specs only; do not edit production apps until implementation plan is approved or delegated to a coding agent."
    ))

    tasks.append(mk(
        "Vista app change: implement Movie Taste Card export/share artifact",
        "Vista", "share-artifact", "high", "eve", 25,
        "Review the Vista repo/app structure and create a build plan for a shareable Movie Taste Card export: taste profile, top/controversial ratings, 9:16 + square image export, and CTA.",
        "Vista should not rely only on TikTok/ReelFarm. Letterboxd-style social behavior shows movie taste travels when users can share identity artifacts.",
        "A build-ready implementation plan exists with repo path, screens/components to edit, required data, image export approach, acceptance tests, and one follow-up coding-agent task if needed.",
        ["memory/app-marketing/share-artifact-roadmap.md", "memory/app-marketing/competitor-mining-protocol.md"],
        "Do not position as a generic Letterboxd killer. Lead with precision/taste identity."
    ))

    tasks.append(mk(
        "Nash app change: implement Weekly Ranking Receipt Card export",
        "Nash Satoshi", "share-artifact", "high", "eve", 26,
        "Review Nash Satoshi app/repo and scope a shareable weekly ranking receipt card: top movers, model disagreement, undervalued/overhyped leaderboard, methodology note, and X/9:16 export.",
        "Nash needs to behave like a public ranking thesis engine with receipts, not another crypto dashboard.",
        "A build-ready implementation plan exists with data inputs, visual design, safe language, export path, and coding-agent task if changes are needed.",
        ["memory/app-marketing/share-artifact-roadmap.md", "memory/app-marketing/app-registry.md"],
        "No financial advice, return claims, or price predictions."
    ))

    tasks.append(mk(
        "Glow app change: implement safe Product Verdict Card export",
        "Glow Index", "share-artifact", "high", "eve", 27,
        "Review Glow Index app/repo and scope a shareable product verdict card: score/rank, formula/value/evidence/claim-check summary, safe suitability language, and TikTok/Pinterest-friendly export.",
        "Glow’s strongest growth loop is likely search + creator shopping demos; creators need a clean share card they can use safely.",
        "A build-ready implementation plan exists with data fields, visual design, claim guardrails, export path, and coding-agent task if changes are needed.",
        ["memory/app-marketing/share-artifact-roadmap.md", "memory/app-marketing/app-registry.md"],
        "No medical/dermatology/treatment claims, fake testimonials, before/after, or guaranteed outcomes."
    ))

    tasks.append(mk(
        "App Marketing OS: build borrowed-audience target lists for Vista, Nash, and Glow",
        "All apps", "borrowed-audience", "high", "eve", 30,
        "Use `memory/app-marketing/borrowed-audience-playbook.md` to research 20 targets per app: creators, newsletters, app reviewers, community mods, roundup writers, and directory owners.",
        "Borrowed audience is likely the highest-leverage low-budget channel. We need qualified targets before drafting outreach or collab asks.",
        "Files exist under `memory/app-marketing/borrowed-audience/` for Vista, Nash, and Glow with 20 targets each, audience notes, fit rationale, risk, and suggested asset/pitch angle.",
        ["memory/app-marketing/borrowed-audience-playbook.md", "memory/app-marketing/winning-pattern-research-protocol.md"],
        "Eve drafts only. JT sends any external messages."
    ))

    tasks.append(mk(
        "App Marketing OS: add experiment-card tracking to weekly review",
        "All apps", "experiment-system", "high", "eve", 35,
        "Update `memory/app-marketing/experiment-calendar.md` or the weekly review process so every promoted pattern uses `experiment-card-template.md` and the 24+/35 scoring rule.",
        "The system should not generate content/task spam from weak swipe ideas. Only scored, measurable experiments should hit Mission Control.",
        "Experiment calendar has a section for pattern score, source proof, tracking/source tag, 24h/72h/7d result, and scale/iterate/kill decision.",
        ["memory/app-marketing/experiment-card-template.md", "memory/app-marketing/winning-pattern-research-protocol.md", "memory/app-marketing/measurement-spine.md"],
        "A marketing insight cannot become a Mission Control task unless it has an experiment card or is a clear infrastructure fix."
    ))

    tasks.append(mk(
        "App Marketing OS: implement measurement spine/source tags for all new experiments",
        "All apps", "measurement", "high", "eve", 36,
        "Add the fields from `memory/app-marketing/measurement-spine.md` to `post-registry.jsonl` workflow or the weekly experiment review process.",
        "Without source tags and result windows, Eve cannot learn which channels actually produce users.",
        "New experiments created after this task include app, channel, source URL/tag, creative type, CTA, 24h/72h/7d metrics, attribution confidence, and decision.",
        ["memory/app-marketing/measurement-spine.md", "memory/app-marketing/post-registry.jsonl", "memory/app-marketing/weekly-scoreboard.md"],
        "Do not scale a channel if attribution is unknown for 2 consecutive weeks."
    ))

    tasks.append(mk(
        "Vista competitor teardown: Letterboxd/social movie app acquisition loops",
        "Vista", "competitor-mining", "high", "eve", 40,
        "Run the competitor mining protocol for Letterboxd, Serializd, TV Time, Likewise, Sequel, JustWatch, and IMDb app/social behavior.",
        "Vista’s wedge must be based on proven movie-app behavior: taste identity, lists, friends/followers, and compatibility/share artifacts.",
        "Save `memory/app-marketing/competitor-intel/vista-movie-app-teardown-YYYY-MM-DD.md` with channels, user complaints, share loops, SEO/ASO patterns, gaps, and at least 3 experiment cards.",
        ["memory/app-marketing/competitor-mining-protocol.md", "memory/app-marketing/experiment-card-template.md"],
        "Extract structure only; do not copy creatives or wording."
    ))

    tasks.append(mk(
        "Nash competitor teardown: crypto ranking/thesis tools and newsletter loops",
        "Nash Satoshi", "competitor-mining", "high", "eve", 41,
        "Run the competitor mining protocol for CoinGecko categories, DeFiLlama, Token Terminal, Messari-style research, crypto newsletters, and AI-token dashboard/search behavior.",
        "Nash needs proof-based distribution and borrowed credibility, not generic crypto-dashboard marketing.",
        "Save `memory/app-marketing/competitor-intel/nash-ranking-thesis-teardown-YYYY-MM-DD.md` with acquisition channels, content formats, partner/newsletter opportunities, trust gaps, and at least 3 experiment cards.",
        ["memory/app-marketing/competitor-mining-protocol.md", "memory/app-marketing/experiment-card-template.md"],
        "No return claims, price predictions, or investment advice."
    ))

    tasks.append(mk(
        "Glow competitor teardown: skincare scanner/ranking app acquisition loops",
        "Glow Index", "competitor-mining", "high", "eve", 42,
        "Run the competitor mining protocol for SkinSort, OnSkin, Yuka, INCIdecoder, Think Dirty, EWG Skin Deep, and Sephora/Ulta review/search behavior.",
        "Glow’s acquisition likely comes from SEO, safe product pages, creator shopping demos, and product verdict artifacts. We need competitor proof before scaling content.",
        "Save `memory/app-marketing/competitor-intel/glow-skincare-app-teardown-YYYY-MM-DD.md` with channels, review complaints, SEO patterns, creator/demo formats, gaps, and at least 3 experiment cards.",
        ["memory/app-marketing/competitor-mining-protocol.md", "memory/app-marketing/experiment-card-template.md"],
        "Avoid medical/treatment framing and do not copy creator scripts."
    ))

    tasks.append(mk(
        "Vista: submit first durable directory listing from existing pack",
        "Vista", "directory", "high", "jt", 40,
        "Open `memory/app-marketing/directory-packs-vista.md`, pick 3-5 screenshots from `~/projects/jtsomwaru-com/public/images/vista/`, then submit Vista to Uneed first.",
        "Vista is live and already has a precision-rating SEO page; a durable listing/backlink compounds while TikTok/ReelFarm metrics are still thin.",
        "One Vista listing is submitted, the submitted URL is pasted back, and `memory/app-marketing/directory-submissions.md` is updated with status + URL.",
        ["memory/app-marketing/directory-packs-vista.md", "memory/app-marketing/directory-submissions.md", "memory/app-marketing/seo-briefs-vista-1-100-movie-rating-app.md"],
        "No paid submissions without approval. Do not overclaim; position Vista as precise/private taste tracking, not a Letterboxd replacement for everyone."
    ))

    tasks.append(mk(
        "Vista: add App Store vendor number for reporting metrics",
        "Vista", "metrics", "high", "eve", 43,
        "Securely add `APPSTORE_VENDOR_NUMBER` to the approved env/config surface, then run `python3 scripts/app_marketing_connectors/app_store_metrics.py` and `python3 scripts/app_marketing_collect_metrics.py`.",
        "Vista App Store metadata auth works and connector readiness exists, but Apple sales/reporting metrics require vendor number/reporting permission before downloads or product-page metrics can flow into the scoreboard.",
        "`memory/app-marketing/app-store-metrics-status.json` reports `reporting_status: sales_report_ready` or a precise Apple-side permission/agreement blocker; Vista App Store rows appear in `memory/app-marketing/metrics-inbox.jsonl` when reporting is available.",
        ["memory/app-marketing/app-store-metrics-status.json", "memory/app-marketing/analytics-access-needed.md", "scripts/app_marketing_connectors/app_store_metrics.py"],
        "Never paste Apple private key contents, vendor number, or account secrets into docs/chat; if Apple-side agreement/role changes are required, stop and create a one-time JT action."
    ))

    tasks.append(mk(
        "Vista: run ASO baseline and one metadata/screenshot test recommendation",
        "Vista", "ASO", "high", "eve", 45,
        "Capture current Vista App Store title, subtitle, first 3 screenshots, description first 3 lines, and compare against Letterboxd/IMDb/Serializd/indie movie trackers.",
        "Vista is an App Store product; ASO is a durable acquisition lever that does not depend on ReelFarm cold starts.",
        "A short ASO report is saved under `memory/app-marketing/vista-aso-baseline-YYYY-MM-DD.md` with one metadata test and one screenshot test JT can apply.",
        ["memory/app-marketing/aso-checklist.md", "memory/app-marketing/app-registry.md"],
        "Do not change App Store Connect directly unless JT explicitly approves."
    ))

    tasks.append(mk(
        "Vista: schedule one clean rating-precision ReelFarm test and require metrics capture",
        "Vista", "experiment", "high", "both", 50,
        "Use Experiment Calendar item `Vista rating precision retest` to queue exactly one specific-movie/exact-rating slideshow in JT's ReelFarm setup.",
        "Prior data says rating precision beat vague hooks; the OS needs one clean test with captured metrics before increasing volume.",
        "One Vista ReelFarm post is queued/posted, then views/saves/comments are logged into `memory/app-marketing/post-registry.jsonl` or metrics inbox within 72 hours.",
        ["memory/app-marketing/experiment-calendar.md", "memory/app-marketing/weekly-scoreboard.md", "memory/reelfarm/vista-automation-a-current.md", "memory/reelfarm/vista-automation-b-current.md"],
        "JT laptop/ReelFarm owns posting execution. Eve must not duplicate TikTok automation on the Mac mini."
    ))

    tasks.append(mk(
        "Nash Satoshi: submit first methodology-backed directory listing",
        "Nash Satoshi", "directory", "high", "jt", 55,
        "Open `memory/app-marketing/directory-packs-nash-satoshi.md`, verify the live methodology/trust URL, select screenshots, then submit to Uneed or Futurepedia first.",
        "Nash has a methodology page and needs durable discovery beyond volatile crypto social reach.",
        "One Nash listing is submitted, URL is pasted back, and directory tracking is updated.",
        ["memory/app-marketing/directory-packs-nash-satoshi.md", "memory/app-marketing/seo-pages/nash-satoshi-methodology-page.md", "memory/app-marketing/directory-submissions.md"],
        "No return, price prediction, or financial-performance claims. Frame as game-theory/narrative/incentive analysis."
    ))

    tasks.append(mk(
        "Nash Satoshi: create one live-ranking model-disagreement post only if current data exists",
        "Nash Satoshi", "experiment", "high", "eve", 60,
        "Fetch live Nash rankings and identify one concrete model disagreement, rank movement, or updated token detail before drafting.",
        "The experiment calendar says specific rankings/model updates beat abstract methodology explainers; generic crypto content is a waste.",
        "A post draft is created only if live token/rank/model evidence exists; otherwise the slot is marked skipped with `NO_LIVE_RANKING_SIGNAL`.",
        ["memory/app-marketing/experiment-calendar.md", "memory/app-marketing/app-registry.md", "https://nashsatoshi.com/rankings"],
        "No links in X body by default, no return claims, no vague question prompts."
    ))

    tasks.append(mk(
        "Glow Index: fix/verify crawler access for sitemap, llms.txt, rankings, and categories",
        "Glow Index", "GEO", "high", "eve", 65,
        "Run `python3 scripts/glow_crawler_check.py` to capture the current blocker; then use `memory/app-marketing/glow-crawler-access-2026-05-13.md` to add narrow Cloudflare/Replit skip rules for `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/rankings`, `/categories`, and `/categories/*`.",
        "Read-only checks found 403 Cloudflare challenges on Glow discovery/category routes; AI/search visibility fails if crawlers cannot reach sitemap, llms.txt, or category pages.",
        "`python3 scripts/glow_crawler_check.py` exits 0 and `memory/app-marketing/glow-crawler-access-status.json` shows all six URLs `ok: true`; update the report with verified results.",
        ["memory/app-marketing/glow-crawler-access-2026-05-13.md", "memory/app-marketing/durable-discovery-plan.md", "memory/app-marketing/pseo-geo-module-spec-glow-index.md"],
        "Do not expand programmatic pages until crawler access and safe-claim templates are healthy."
    ))

    tasks.append(mk(
        "Glow Index: prepare first safe directory submission with screenshots selected",
        "Glow Index", "directory", "medium", "jt", 120,
        "Open `memory/app-marketing/directory-packs-glow-index.md`, select safe screenshots, and choose first target: Uneed or Futurepedia.",
        "Glow is live and has active SEO/GEO opportunity, but listings need safe consumer-research framing and visual assets.",
        "First Glow listing is ready for final approval or submitted if JT approves; directory tracking is updated with URL/status.",
        ["memory/app-marketing/directory-packs-glow-index.md", "memory/app-marketing/directory-submissions.md", "memory/app-marketing/app-registry.md"],
        "No medical, dermatology, diagnosis/treatment, fake testimonial, before/after, or guaranteed outcome claims."
    ))

    tasks.append(mk(
        "Glow Index: define metrics source before any TikTok/ReelFarm volume",
        "Glow Index", "metrics", "high", "eve", 70,
        "Add one concrete Glow metrics source to `memory/app-marketing/account-map.json` using `memory/app-marketing/web-analytics-mapping-template.md`, then run `python3 scripts/app_marketing_connectors/web_metrics.py` and `python3 scripts/app_marketing_collect_metrics.py`.",
        "Glow should not receive social volume until there is a way to measure visits/searches/clicks and learn from it.",
        "`memory/app-marketing/web-analytics-status.json` shows `glow-index` removed from `blocked_products` or a precise provider/permission/log-path blocker; `memory/app-marketing/glow-metrics-source-YYYY-MM-DD.md` documents source, access status, collection command/process, and weekly scoreboard fields.",
        ["memory/app-marketing/account-map.json", "memory/app-marketing/web-analytics-mapping-template.md", "memory/app-marketing/weekly-scoreboard.md", "memory/app-marketing/metrics-automation-plan.md", "memory/app-marketing/app-registry.md"],
        "Do not ask JT for daily manual metrics; weekly fallback only if API/log access is blocked."
    ))

    tasks.append(mk(
        "Action Arena: create waitlist/landing-page spec before marketing automation",
        "Action Arena", "prelaunch", "high", "eve", 75,
        "Draft a landing/waitlist spec for Action Arena with positioning, fake-money guardrails, beta CTA, and minimum fields to capture.",
        "Action Arena should build demand through @dynastyjig, but the OS needs somewhere to send interested users before directory/SEO tasks make sense.",
        "A build-ready spec is saved at `memory/app-marketing/action-arena-waitlist-spec-YYYY-MM-DD.md` and a follow-up build task exists if needed.",
        ["memory/app-marketing/app-registry.md", "memory/app-marketing/seo-backlog.md", "skills/sports-gm/SKILL.md"],
        "No real-money wagering claims; emphasize fake budget, strategy, competition, and no real money is wagered."
    ))

    tasks.append(mk(
        "Action Arena: add @dynastyjig signal capture to app marketing scoreboard",
        "Action Arena", "metrics", "medium", "eve", 130,
        "Map @dynastyjig post metrics and reply signals into the App Marketing weekly scoreboard without making product mentions public by default.",
        "Action Arena demand is currently invisible backdrop; the OS needs to detect whether betting/fantasy strategy content is producing beta-user signal.",
        "Scoreboard has Action Arena fields for @dynastyjig engagement, qualified replies, waitlist signups once live, and beta-interest notes.",
        ["memory/app-marketing/weekly-scoreboard.md", "memory/app-marketing/app-registry.md", "memory/sports-gm/"],
        "Do not conflate Action Arena with Dynasty Fantasy Football Simulator."
    ))

    tasks.append(mk(
        "App Marketing OS: implement weekly self-improvement decision rules",
        "All apps", "self-improvement", "high", "eve", 35,
        "Add a weekly review step that reads metrics + experiment calendar + generated MC task outcomes and outputs continue/kill/rework decisions per app/channel.",
        "Autonomy without kill/continue rules becomes stale task spam. The OS needs to stop dead channels and double down on evidence.",
        "A self-improvement rule file exists and the weekly App Marketing review prompt/script references it before generating new tasks.",
        ["memory/app-marketing/os-spec.md", "memory/app-marketing/weekly-scoreboard.md", "memory/app-marketing/experiment-calendar.md"],
        "Never auto-increase volume when metrics are missing for 2 consecutive weeks; fix measurement first."
    ))

    return tasks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true", help="Create missing Mission Control tasks")
    ap.add_argument("--json", action="store_true", help="Print JSON")
    ap.add_argument("--no-fetch", action="store_true", help="Do not call Mission Control; useful for offline/dry-run validation")
    args = ap.parse_args()

    specs = build_task_specs()
    active = [] if args.no_fetch else fetch_tasks()
    keys = existing_keys(active)
    results = []
    for spec in specs:
        duplicate = spec.title.lower() in keys or spec.slug.lower() in keys
        row = asdict(spec) | {"duplicate": duplicate, "created": False, "id": None}
        if args.execute and not duplicate:
            try:
                resp = post_task(spec)
                row["created"] = True
                row["id"] = resp.get("id")
                keys.add(spec.title.lower())
                keys.add(spec.slug.lower())
            except urllib.error.HTTPError as e:
                row["error"] = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')}"
            except Exception as e:
                row["error"] = str(e)
        results.append(row)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps({"execute": args.execute, "tasks": results}, indent=2))

    summary = {
        "execute": args.execute,
        "fetched_mission_control": not args.no_fetch,
        "total_specs": len(specs),
        "duplicates": sum(1 for r in results if r["duplicate"]),
        "created": sum(1 for r in results if r["created"]),
        "errors": [r for r in results if r.get("error")],
        "out": str(OUT_PATH),
    }
    print(json.dumps(summary if args.json else summary, indent=2))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
