import json
try:
    d = json.load(open('/Users/jtsomwaru/.openclaw/workspace/memory/costs/2026-04-20.json'))
    sess = [(k, v) for k, v in d['sessions'].items()]
    sess.sort(key=lambda x: x[1].get('cost_usd', 0), reverse=True)
    print(f"Total: ${d.get('total_usd', 0):.2f}\n")
    for k, v in sess[:15]:
        name = v.get('label', k.split(':')[-2] if ':' in k else k)
        model = v.get('model', 'unknown')
        if "05024e45" in k: name = "Weekly Synthesis (05024e45)"
        if "4a70dda4" in k: name = "Daily News Hook (4a70dda4)"
        if "ebb843af" in k: name = "Prospect Discovery (ebb843af)"
        if "be59a068" in k: name = "Overnight Autonomy (be59a068)"
        if "f368e18b" in k: name = "Passive Income Fetch (f368e18b)"
        if "870bf3ff" in k: name = "Vibe Generation (870bf3ff)"
        if "0036ee7c" in k: name = "Crypto Multi-Agent Engine (0036ee7c)"
        print(f"${v.get('cost_usd', 0):>6.2f} | In: {v.get('input_tokens', 0):>7,} | Out: {v.get('output_tokens', 0):>6,} | {model[:25]:<25} | {name}")
except Exception as e:
    print(f"Error loading JSON: {e}")
