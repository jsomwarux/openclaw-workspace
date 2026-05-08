#!/usr/bin/env python3
"""Generate the App Marketing OS weekly experiment calendar.

Purpose:
- Convert metrics + optimization rules + current test briefs into a small set of
  named weekly experiments.
- Keep product marketing as experiments, not random posts.
- Deterministic and safe: no external posting, no API writes.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
BASE = ROOT / "memory" / "app-marketing"
METRICS = BASE / "metrics-inbox.jsonl"
REGISTRY = BASE / "post-registry.jsonl"
OUT = BASE / "experiment-calendar.md"


def load_jsonl(path: Path) -> list[dict]:
    rows=[]
    if not path.exists():
        return rows
    for line in path.read_text().splitlines():
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows


def week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def latest_test_brief() -> Path | None:
    files=sorted(BASE.glob('test-briefs-*.md'))
    return files[-1] if files else None


def text_topic(product: str, text: str) -> str:
    t=text.lower()
    if product == 'vista':
        if any(x in t for x in ['imdb','midsommar','half-star','half stars','rating','1–100','1-100','87']):
            return 'rating_precision'
        if any(x in t for x in ['compatible','boyfriend','best friend','couples']):
            return 'relationship_compatibility'
        if 'taste' in t:
            return 'taste_identity'
    if product == 'nash-satoshi':
        if any(x in t for x in ['updated rankings','updated top','$cred','$clawd','ranked','rankings']):
            return 'rankings_update'
        if any(x in t for x in ['4 ai','4 ais','4 llm','4 models','gpt','claude','gemini','grok','opus','model']):
            return 'model_consensus'
        if any(x in t for x in ['methodology','scorecard','framework']):
            return 'methodology_explainer'
        if any(x in t for x in ['game theory','guessing game','math problem','nash']):
            return 'game_theory_explainer'
    if product == 'glow-index':
        if any(x in t for x in ['glow index summary','geo','llms','faq','schema','ai search','product page']):
            return 'product_page_geo'
        if any(x in t for x in ['serum','moisturizer','spf','cleanser','category']):
            return 'category_seo'
        if any(x in t for x in ['ingredient','formula','value','safety','skin compatibility']):
            return 'formula_research'
    return 'unclear'


def summarize_group(rows: list[dict]) -> dict:
    if not rows:
        return {'count':0,'baseline':0,'best':None,'losers':[]}
    values=[int(r.get('views_or_impressions') or 0) for r in rows]
    baseline=sum(values)/len(values)
    best=max(rows, key=lambda r:int(r.get('views_or_impressions') or 0))
    losers=[r for r in rows if baseline > 0 and int(r.get('views_or_impressions') or 0) <= baseline*0.5]
    return {'count':len(rows),'baseline':baseline,'best':best,'losers':losers}


def planned_count(product: str, platform: str) -> int:
    rows=load_jsonl(REGISTRY)
    return sum(1 for r in rows if r.get('product_slug')==product and r.get('platform')==platform and (r.get('status')=='planned' or str(r.get('url_or_id','')).startswith('planned:')))


def build_experiment(product: str, platform: str, rows: list[dict], brief_text: str) -> dict:
    summary=summarize_group(rows)
    best=summary['best'] or {}
    best_text=str(best.get('content_id_or_hook') or '')
    best_topic=text_topic(product, best_text)

    if product == 'vista' and platform == 'tiktok':
        return {
            'name':'Vista rating precision retest',
            'hypothesis':'Specific movie + exact rating-number tension beats relationship-compatibility hooks.',
            'channel':'TikTok/ReelFarm',
            'post_plan':'1 ReelFarm slideshow using a specific movie/rating hook. Use the latest test brief unless metrics reject it.',
            'success':'≥2x Vista TikTok baseline or ≥500 views, whichever is lower while sample is thin.',
            'retire':'Do not run relationship-compatibility again until rating precision gets another clean test or compatibility has real proof.',
            'evidence':f"Best observed Vista TikTok topic: {best_topic}; best={best_text[:120]!r} views={best.get('views_or_impressions')}",
        }
    if product == 'nash-satoshi' and platform == 'x':
        return {
            'name':'Nash ranking/model update',
            'hypothesis':'Specific rankings/model updates beat abstract methodology explainers.',
            'channel':'X @NashSatoshi',
            'post_plan':'1 rankings/model-disagreement post only if live ranking/token details are available. Otherwise skip.',
            'success':'≥1.5x Nash X baseline or ≥300 impressions while sample is thin.',
            'retire':'Avoid direct links, vague question prompts, and generic methodology explainers unless tied to a new live page/update.',
            'evidence':f"Best observed Nash X topic: {best_topic}; best={best_text[:120]!r} views={best.get('views_or_impressions')}",
        }
    if product == 'nash-satoshi' and platform == 'tiktok':
        return {
            'name':'Nash model-consensus slideshow',
            'hypothesis':'Model-consensus/game-theory hooks with a concrete number beat vague “watch this” slides.',
            'channel':'TikTok/ReelFarm',
            'post_plan':'1 slideshow around 4-AI agreement/disagreement. Add token/score only if live proof is visible.',
            'success':'≥2x Nash TikTok baseline or ≥150 views while sample is thin.',
            'retire':'Never approve “watch this” or unclear title slides again.',
            'evidence':f"Best observed Nash TikTok topic: {best_topic}; best={best_text[:120]!r} views={best.get('views_or_impressions')}",
        }
    if product == 'glow-index' and platform == 'seo':
        return {
            'name':'Glow product-page GEO baseline',
            'hypothesis':'Direct-answer product summaries, safe schema, FAQs, and llms.txt should create a stronger AI-search foundation before social fanout.',
            'channel':'SEO/GEO',
            'post_plan':'Verify deployed product-page GEO patch, then monitor indexed/crawlable product pages. Do not create TikTok volume until tracking and assets exist.',
            'success':'Product pages show summary/FAQ/schema live and `llms.txt` is accessible; next week, move to one category-page pilot if crawl surfaces are healthy.',
            'retire':'Do not build ingredient/dupe/concern pages until structured data supports unique, safe pages.',
            'evidence':'Glow is active at https://glowindex.co; product-page GEO patch pushed in `d28afc6`; no social metrics baseline yet.',
        }
    return {
        'name':f'{product} {platform} baseline builder',
        'hypothesis':'Need more clean metrics before increasing volume.',
        'channel':platform,
        'post_plan':'1 tightly scoped test only if OS rules and product registry allow it.',
        'success':'Any clean non-zero result with exact post ID tracked.',
        'retire':'Skip if no compliant product-native angle exists.',
        'evidence':f"Rows={summary['count']} baseline={summary['baseline']:.1f}",
    }


def main() -> int:
    today=date.today()
    week=week_start(today)
    metrics=load_jsonl(METRICS)
    groups=defaultdict(list)
    for r in metrics:
        groups[(r.get('product_slug') or 'unknown', r.get('platform') or 'unknown')].append(r)
    brief=latest_test_brief()
    brief_text=brief.read_text() if brief else ''

    priority_keys=[('glow-index','seo'),('vista','tiktok'),('nash-satoshi','x'),('nash-satoshi','tiktok')]
    experiments=[build_experiment(p, plat, groups.get((p,plat), []), brief_text) for p,plat in priority_keys]

    lines=[
        '# App Marketing OS — Experiment Calendar',
        '',
        f'Week of: {week.isoformat()}',
        f'Generated: {today.isoformat()}',
        '',
        '## Rule',
        'Every generated product post should map to a named experiment, a success threshold, and a retire/rework rule. If it does not, skip it.',
        '',
        '## Inputs used',
        f'- Metrics rows: {len(metrics)}',
        f'- Latest test brief: `{brief.name if brief else "none"}`',
        f'- Planned rows currently waiting for live post IDs: {sum(planned_count(p, plat) for p,plat in priority_keys)}',
        '',
        '## This Week’s Experiments',
    ]
    for i,e in enumerate(experiments,1):
        lines += [
            '',
            f'### {i}. {e["name"]}',
            f'- **Channel:** {e["channel"]}',
            f'- **Hypothesis:** {e["hypothesis"]}',
            f'- **Post plan:** {e["post_plan"]}',
            f'- **Success threshold:** {e["success"]}',
            f'- **Retire/rework rule:** {e["retire"]}',
            f'- **Evidence:** {e["evidence"]}',
        ]
    lines += [
        '',
        '## Do Not Test This Week',
        '- Vista relationship compatibility unless a real proof asset exists. Current winner is rating precision.',
        '- Glow TikTok/ReelFarm volume until account, assets, and metric path are confirmed.',
        '- Glow ingredient/dupe/concern pSEO pages until structured data supports unique safe pages.',
        '- Nash generic methodology explainers without a live ranking, model-update, or methodology-page launch angle.',
        '- Any “watch this” TikTok/ReelFarm title or unclear slideshow hook.',
        '',
        '## Measurement Requirement',
        '- Every approved draft must create or update a planned row in `memory/app-marketing/post-registry.jsonl`.',
        '- Discovery must reconcile planned rows to exact live post IDs before performance is judged.',
        '- If a post cannot be tracked, do not use it as evidence for future strategy.',
    ]
    OUT.write_text('\n'.join(lines).rstrip()+'\n')
    print(f'APP_MARKETING_EXPERIMENT_CALENDAR_OK out={OUT} experiments={len(experiments)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
