import json
import glob

for path in sorted(glob.glob('/Users/jtsomwaru/.openclaw/workspace/memory/costs/2*.json')):
    try:
        d = json.load(open(path))
        print(f"=== {path.split('/')[-1]} | Total: ${d.get('total_usd',0):.2f} ===")
        sess = sorted(d['sessions'].values(), key=lambda x: x.get('cost_usd',0), reverse=True)
        for v in sess[:5]:
            label = v.get('label', 'unlabeled')
            model = v.get('model', 'unknown')
            print(f"  ${v.get('cost_usd',0):>6.2f} | In: {v.get('input_tokens',0):>7,} | Out: {v.get('output_tokens',0):>6,} | {model[:25]:<25} | {label}")
    except Exception as e:
        print(f"Error on {path}: {e}")
