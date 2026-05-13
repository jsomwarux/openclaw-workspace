#!/usr/bin/env python3
"""Analyze App Marketing OS metrics and write recommendations.

This does more than rank by views. It extracts content features so future
product-content generation can reuse winning structures and avoid losing ones.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path.home() / ".openclaw" / "workspace"
BASE = ROOT / "memory" / "app-marketing"
INBOX = BASE / "metrics-inbox.jsonl"
OUT = BASE / "performance-analysis.md"
RULES_OUT = BASE / "optimization-rules.md"


def load_rows() -> list[dict]:
    rows=[]
    if not INBOX.exists():
        return rows
    for line in INBOX.read_text().splitlines():
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows


def label(value: int, baseline: float) -> str:
    if baseline <= 0:
        return "baseline-needed"
    if value >= baseline * 2:
        return "winner"
    if value >= baseline * 1.25:
        return "promising"
    if value <= baseline * 0.5:
        return "loser"
    return "neutral"


def feature_extract(row: dict) -> dict:
    text = str(row.get('content_id_or_hook') or '')
    t = text.lower()
    product = row.get('product_slug') or 'unknown'
    platform = row.get('platform') or 'unknown'

    # Hook technique heuristic. Keep simple/deterministic; generation agent can refine.
    if re.search(r'\b\d+\b|\$[a-z0-9]+|gpt|claude|gemini|opus|4 ai|4 llm|4 models', t):
        hook = 'specific_number_unexpected_context'
    elif any(x in t for x in ['wrong', 'isn\'t', "isn't", 'not ', 'never']):
        hook = 'contradiction'
    elif any(x in t for x in ['you\'re', "you're", 'you are', 'your ']):
        hook = 'direct_accusation'
    elif '?' in text:
        hook = 'question_prompt'
    elif len(text.strip().split()) <= 8 and text.strip():
        hook = 'one_liner_gut_punch'
    elif any(x in t for x in ['we upgraded', 'updated rankings', 'back up', 'technical difficulties']):
        hook = 'plain_update_or_status'
    else:
        hook = 'unclear'

    # Product-specific topic pillars.
    topic = 'unclear'
    if product == 'nash-satoshi':
        if any(x in t for x in ['updated top', 'updated rankings', 'ranked', 'rankings']):
            topic = 'rankings_update'
        elif any(x in t for x in ['gpt', 'claude', 'gemini', 'opus', 'model', '4 ai', '4 llm', '4 models']):
            topic = 'model_consensus'
        elif any(x in t for x in ['methodology', 'framework', 'scorecard', 'output per token']):
            topic = 'methodology'
        elif '$' in t or 'token' in t:
            topic = 'token_spotlight'
        elif any(x in t for x in ['technical', 'back up', 'fix']):
            topic = 'technical_issue/status'
        elif 'game theory' in t or 'nash equilibrium' in t or 'math problem' in t or 'guessing game' in t or 'trader' in t:
            topic = 'game_theory_explainer'
    elif product == 'vista':
        if any(x in t for x in ['boyfriend', 'best friend', 'compatible', 'couples', 'share a brain']):
            topic = 'relationship_compatibility'
        elif any(x in t for x in ['1–100', '1-100', 'half-stars', 'imdb', 'rating', '7.1']):
            topic = 'rating_precision'
        elif any(x in t for x in ['taste', 'movie taste']):
            topic = 'taste_identity'
        elif any(x in t for x in ['movie', 'film', 'midsommar']):
            topic = 'movie_specific_take'

    # Format.
    if platform == 'tiktok':
        fmt = 'slideshow'
    elif '\n1.' in text or re.search(r'\n\d+\.', text):
        fmt = 'list/ranking'
    elif '?' in text:
        fmt = 'question_prompt'
    elif any(x in t for x in ['updated', 'we upgraded', 'back up', 'technical difficulties']):
        fmt = 'status_update'
    elif any(x in t for x in ['methodology', 'framework', 'why', 'how']):
        fmt = 'methodology_explainer'
    else:
        fmt = 'single_post'

    # Specificity.
    specificity_hits = len(re.findall(r'\b\d+\b|\$[A-Z0-9]+|GPT|Claude|Gemini|Opus|LLM|AI', text))
    specificity = 'high' if specificity_hits >= 2 else 'medium' if specificity_hits == 1 else 'low'

    # Proof type.
    proof=[]
    if '$' in text: proof.append('specific_token')
    if any(x in t for x in ['gpt', 'claude', 'gemini', 'opus', '4 ai', '4 llm', '4 models']): proof.append('model_names')
    if any(x in t for x in ['updated rankings', 'updated top', 'ranked']): proof.append('live_ranking_data')
    if any(x in t for x in ['compatible', 'boyfriend', 'best friend']): proof.append('specific_user_scenario')
    if any(x in t for x in ['methodology', 'framework', 'scorecard']): proof.append('methodology_explanation')
    if not proof: proof=['none']

    # CTA type.
    if 'http' in t or 't.co' in t or '.com' in t:
        cta = 'direct_link'
    elif '?' in text:
        cta = 'soft_question'
    elif any(x in t for x in ['check', 'see where', 'rankings']):
        cta = 'rankings_check'
    else:
        cta = 'no_cta'

    # Risk.
    risks=[]
    if product == 'nash-satoshi' and any(x in t for x in ['outperformance', 'will pump', 'buy ', 'sell ']): risks.append('financial_advice_or_return_risk')
    if product == 'vista' and any(x in t for x in ['boyfriend', 'best friend']) and platform == 'tiktok': risks.append('fake_social_claim_check')
    if not risks: risks=['clean']

    return {
        'hook': hook,
        'topic': topic,
        'format': fmt,
        'specificity': specificity,
        'proof': ','.join(proof),
        'cta': cta,
        'risk': ','.join(risks),
    }


MEANINGFUL_FEATURE_KEYS = {'hook', 'topic', 'format', 'specificity', 'proof', 'cta'}
BORING_FEATURES = {'risk:clean', 'cta:no_cta'}


def summarize_features(items: list[dict], baseline: float, target_label: str) -> dict[str, int]:
    counts=defaultdict(int)
    for x in items:
        if label(int(x.get('views_or_impressions') or 0), baseline) != target_label:
            continue
        feats = feature_extract(x)
        for k,v in feats.items():
            feature=f'{k}:{v}'
            if k not in MEANINGFUL_FEATURE_KEYS or feature in BORING_FEATURES:
                continue
            counts[feature] += 1
    return dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))


def split_feature_signal(win_features: dict[str, int], lose_features: dict[str, int]) -> tuple[dict[str, int], dict[str, tuple[int, int]], dict[str, int]]:
    """Separate reusable winners from conflicted/losing features.

    A feature is only a true reuse signal when it appears more often in winners
    than losers. This prevents tiny-sample spikes from recommending poisoned
    patterns like low specificity or proof:none when those mostly lost.
    """
    reuse: dict[str, int] = {}
    conflicted: dict[str, tuple[int, int]] = {}
    avoid: dict[str, int] = dict(lose_features)
    for feat, w_count in win_features.items():
        l_count = lose_features.get(feat, 0)
        if w_count > l_count:
            reuse[feat] = w_count
        elif l_count > 0:
            conflicted[feat] = (w_count, l_count)
            avoid.setdefault(feat, l_count)
        else:
            # No loser evidence, but only keep if not obviously low-signal.
            if feat not in {'specificity:low', 'proof:none', 'hook:unclear', 'topic:unclear'}:
                reuse[feat] = w_count
            else:
                conflicted[feat] = (w_count, 0)
    return reuse, conflicted, dict(sorted(avoid.items(), key=lambda kv: kv[1], reverse=True))


def main() -> int:
    rows=load_rows()
    groups=defaultdict(list)
    for r in rows:
        groups[(r.get('product_slug') or 'unknown', r.get('platform') or 'unknown')].append(r)

    lines=["# App Marketing OS — Performance Analysis", "", f"Last updated: {date.today().isoformat()}", ""]
    rules=["# App Marketing OS — Optimization Rules", "", f"Last updated: {date.today().isoformat()}", "", "Use this file before generating future app/product content.", ""]

    if not rows:
        lines += ["No metrics rows yet."]
        rules += ["No metrics rows yet."]

    for (product, platform), items in sorted(groups.items()):
        views=[int(x.get('views_or_impressions') or 0) for x in items]
        baseline=sum(views)/len(views) if views else 0
        best=max(items, key=lambda x:int(x.get('views_or_impressions') or 0))
        lines += [f"## {product} / {platform}", "", f"Rows: {len(items)}", f"Baseline views/impressions: {baseline:.1f}", f"Best: {best.get('content_id_or_hook')} ({best.get('views_or_impressions')} views/impressions)", "", "### Item Labels + Features"]
        for x in sorted(items, key=lambda x:int(x.get('views_or_impressions') or 0), reverse=True)[:10]:
            v=int(x.get('views_or_impressions') or 0)
            feats=feature_extract(x)
            feat_str = '; '.join(f'{k}={v}' for k,v in feats.items())
            lines.append(f"- **{label(v, baseline)}** — {v}: {x.get('content_id_or_hook')}  ")
            lines.append(f"  - features: {feat_str}")
        lines.append("")
        win_features=summarize_features(items, baseline, 'winner')
        lose_features=summarize_features(items, baseline, 'loser')
        reuse_features, conflicted_features, avoid_features = split_feature_signal(win_features, lose_features)
        lines.append("### Winning Feature Pattern")
        if win_features:
            for k,v in list(win_features.items())[:8]: lines.append(f"- {k} ({v})")
        else:
            lines.append("- No winner feature pattern yet.")
        lines.append("")
        lines.append("### Validated Reuse Signals")
        if reuse_features:
            for k,v in list(reuse_features.items())[:8]: lines.append(f"- {k} ({v} winner rows, net positive)")
        else:
            lines.append("- No validated reuse signal yet. Keep testing; do not copy winner features that also lost more often.")
        if conflicted_features:
            lines.append("")
            lines.append("### Conflicted Signals")
            for k,(w,l) in list(conflicted_features.items())[:8]: lines.append(f"- {k} (winner rows {w}, loser rows {l}) — do not reuse without stronger proof/tension")
        lines.append("")
        lines.append("### Losing Feature Pattern")
        if lose_features:
            for k,v in list(lose_features.items())[:8]: lines.append(f"- {k} ({v})")
        else:
            lines.append("- No loser feature pattern yet.")
        lines.append("")
        lines.append("### Recommendation")
        if baseline <= 0:
            lines.append("- Need more non-zero data before making content decisions.")
        else:
            winners=[x for x in items if label(int(x.get('views_or_impressions') or 0), baseline)=='winner']
            losers=[x for x in items if label(int(x.get('views_or_impressions') or 0), baseline)=='loser']
            if winners:
                f=feature_extract(winners[0])
                topic = f['topic'] if f['topic'] != 'unclear' else 'the clearest repeated winning topic'
                lines.append(f"- Double down on {topic} using {f['hook']} with {f['specificity']} specificity.")
            else:
                lines.append("- No clear winner yet. Keep testing without increasing volume.")
            if len(losers) >= 3:
                lines.append("- Retire/rework repeated low-performing feature combinations in this group.")
            lines.append("- Do not treat one spike as proof until it repeats.")
        lines.append("")

        # Rules file.
        rules += [f"## {product} / {platform}", ""]
        if reuse_features:
            rules.append("### Reuse — validated net-positive only")
            for k,v in list(reuse_features.items())[:8]: rules.append(f"- {k} ({v} winner rows, net positive vs losers)")
        if conflicted_features:
            rules.append("### Conflicted — do not blindly reuse")
            for k,(w,l) in list(conflicted_features.items())[:8]: rules.append(f"- {k} (winner rows {w}, loser rows {l})")
        if avoid_features:
            rules.append("### Avoid / Rework")
            for k,v in list(avoid_features.items())[:8]: rules.append(f"- {k} ({v} loser rows)")
        rules.append("### Generation Instruction")
        if baseline > 0 and reuse_features:
            rules.append("- Generate new posts by reusing only validated net-positive structures/topics. Do not reuse conflicted features without adding new proof, specificity, or tension.")
            rules.append("- If a feature appears in both winners and losers, treat it as unresolved until it repeats with clean performance.")
        elif baseline > 0 and win_features:
            rules.append("- Winner data exists, but no feature is net-positive yet. Treat winners as examples to study, not rules to copy.")
            rules.append("- Keep testing one variable at a time and require stronger proof/tension before scaling.")
        else:
            rules.append("- Keep testing. Do not increase volume until baseline exists.")
        rules.append("")

    OUT.write_text("\n".join(lines).rstrip()+"\n")
    RULES_OUT.write_text("\n".join(rules).rstrip()+"\n")
    print(f"APP_MARKETING_ANALYZE_OK rows={len(rows)} out={OUT} rules={RULES_OUT}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
