#!/usr/bin/env python3
"""Test script to extract ExplodingTopics data from __NEXT_DATA__ JSON."""
import requests, re, json

headers = {'User-Agent': 'Mozilla/5.0 Chrome/122'}

# Test what slugs actually return 200 with data
working_slugs = []
for slug in ['software-topics', 'startups', 'products', 'crypto', 'finance',
            'fashion', 'health', 'gaming', 'science', 'music',
            'sports', 'food', 'travel', 'education', 'business']:
    r = requests.get(f'https://explodingtopics.com/{slug}', headers=headers, timeout=10)
    if r.status_code == 200:
        text = r.text
        trends = re.findall(r'"keyword":"([^"]+)"', text)
        print(f"✅ {slug}: {r.status_code} | {len(trends)} keyword matches")
        if trends:
            working_slugs.append((slug, len(trends)))
    else:
        print(f"❌ {slug}: {r.status_code}")

print(f"\nWorking: {[s[0] for s in working_slugs]}")

# Try to extract the full JSON for software-topics
print("\n--- Testing software-topics extraction ---")
r2 = requests.get('https://explodingtopics.com/software-topics', headers=headers, timeout=15)
text2 = r2.text

# Find the trends array directly
script_match = re.search(r'__NEXT_DATA__\s*=\s*({.*)', text2, re.DOTALL)
if script_match:
    raw = script_match.group(1)
    # Balance braces to find end
    depth = 0
    end = 0
    for i, c in enumerate(raw):
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end > 0:
        json_str = raw[:end]
        print(f"Extracted JSON: {len(json_str)} chars")
        try:
            d = json.loads(json_str)
            props = d.get('props', {}).get('pageProps', {})
            trending = props.get('trendingDesktopData', {}).get('trends', [])
            print(f"Trends: {len(trending)}")
            for t in trending[:3]:
                print(f"  - keyword={t.get('keyword')} cat={t.get('category')} vol={t.get('monthlySearches')}")
        except Exception as e:
            print(f"JSON parse error: {e}")
            # Save the first 2000 chars for debugging
            print("First 2000 chars of JSON:")
            print(json_str[:2000])
