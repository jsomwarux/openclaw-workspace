from __future__ import annotations

import json
import re
import urllib.request


def _json_url(url: str) -> str:
    url=url.strip()
    if url.endswith('.json'):
        return url
    if '?' in url:
        url=url.split('?',1)[0]
    return url.rstrip('/') + '.json'


def fetch(post: dict) -> dict | None:
    """Fetch public Reddit score/comment metrics for a post URL.

    No auth required for basic public JSON in many cases. If Reddit blocks/rate-limits,
    fail closed and return None.
    """
    url=post.get('url_or_id') or post.get('url') or ''
    if 'reddit.com' not in url:
        return None
    req=urllib.request.Request(_json_url(url), headers={'User-Agent':'OpenClawAppMarketingMetrics/0.1 by JT'})
    with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310 - public URL from our registry
        data=json.loads(resp.read().decode('utf-8'))
    listing=data[0]['data']['children'][0]['data']
    removed = bool(listing.get('removed_by_category') or listing.get('banned_by') or listing.get('selftext') == '[removed]')
    return {
        'date': post.get('date'),
        'week_of': post.get('week_of') or post.get('date'),
        'product_slug': post.get('product_slug'),
        'platform': 'reddit',
        'content_id_or_hook': post.get('hook_or_title') or listing.get('title'),
        'views_or_impressions': int(listing.get('score') or 0),
        'likes': int(listing.get('ups') or listing.get('score') or 0),
        'comments': int(listing.get('num_comments') or 0),
        'url': url,
        'notes': f"reddit public metrics; removed={removed}; upvote_ratio={listing.get('upvote_ratio')}",
    }
