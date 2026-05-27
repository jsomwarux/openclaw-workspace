import json
from datetime import datetime

date = datetime.now().strftime('%Y-%m-%d')
prospects = [
    {"name": "Bell Electrical Supply Co., Inc.", "contact": "Anthony Baek", "category": "Wholesale", "niche": "Electrical Wholesale", "hook": "Family-owned since 1988, expanding to gov agencies/universities."},
    {"name": "Fargo HVAC Supply Inc.", "contact": "Owner (Unconfirmed)", "category": "Wholesale", "niche": "HVAC Wholesale", "hook": "Same-day delivery model requires manual order fulfillment."}
]

# For this demo, I will define a structure that mimics the output needed.
output_file = f'/Users/jtsomwaru/.openclaw/workspace/memory/drafts/t3-batch-{date}.md'
with open(output_file, 'w') as f:
    f.write(f"# T3 Cold Hook Batch — {date}\n")
    f.write("*[2] prospects — 3-touch sequence per prospect. Send Message 1 first.*\n\n")

    for p in prospects:
        f.write(f"## {p['name']}\n")
        f.write(f"**Contact:** {p['contact']}\n")
        f.write(f"**Niche:** {p['niche']}\n\n")
        
        # Message 1
        f.write(f"**--- MESSAGE 1 ---**\nSubject: {p['name'].split()[0].lower()} dispatch setup\n\n")
        f.write(f"Anthony — {p['hook']}\n\nMost of that SKU knowledge still carries in your team's heads, which means it slows down when the phone lines close at 5PM.\n\nI built an automated parts lookup for similar distributors — contractors get availability through chat in under 10 seconds. No manual lookups required.\n\nWorth 15 minutes to see how that'd work for your team?\n\n")
        
        # Message 2
        f.write(f"**--- MESSAGE 2 ---**\n")
        f.write("One thing that came up configuring this for a similar shop: the automated lookup also flags pricing discrepancies before the quote goes out, not just at checkout. Figured that might be relevant.\n\n")
        
        # Message 3
        f.write(f"**--- MESSAGE 3 ---**\n")
        f.write("Totally understand if the timing's off right now. If it ever becomes relevant, I'm happy to swap notes.\n\n---\n")

print(f"Drafts saved to {output_file}")
