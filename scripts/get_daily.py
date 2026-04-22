import json
import glob

total = 0
for path in sorted(glob.glob('/Users/jtsomwaru/.openclaw/workspace/memory/costs/2*.json')):
    try:
        d = json.load(open(path))
        usd = d.get('total_usd',0)
        total += usd
        print(f"{path.split('/')[-1]} | Total: ${usd:.2f}")
    except Exception as e:
        print(f"Error on {path}: {e}")
print(f"Grand Total: ${total:.2f}")
