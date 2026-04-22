import sys
import importlib.util

spec = importlib.util.spec_from_file_location("vibe_post", "/Users/jtsomwaru/.openclaw/workspace/scripts/vibe-post.py")
vibe_post = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vibe_post)

content = """FORMAT: ugc_reaction
SOURCE TAKE: a common take: 'this coin has 28% staking APY — it's a no-brainer'
SOURCE TYPE: representative_take

SLIDE 1: [Hook — "28% APY sounds like free money. Here's what game theory actually sees."]

SLIDE 2: [The staking APY on screen — labeled as "a common take: 28% APY"]

SLIDE 3: [Why high APY is structurally a prisoner's dilemma — 1-2 sentences]
  - Early exiters capture the yield. Late holders absorb the dilution.
  - High APY often signals tokenomics misalignment — not project strength.

SLIDE 4: [Nash Satoshi ranking as counter-evidence — rankings-table.png with callout]
  - Coins with 20%+ APY consistently rank low on game theory positioning
  - The yield is the trap, not the signal.
SLIDE 5: [The insight — what the 4-model ensemble sees that yield-chasing misses]
  - Coordination dynamics. Validator concentration. Holder time horizons.
  - Nash Satoshi scores what the crowd is missing.
SLIDE 6: [CTA — "Full game theory rankings at nashsatoshi.com"]

CAPTION: pov: you just found out why high staking APY is the worst signal to follow
HASHTAGS: #crypto #gametheory #AIcrypto #cryptostrategy #nashequilibrium
"""

hook, slides = vibe_post.parse_slides_from_content(content)
print(f"Hook: {hook}")
for i, s in enumerate(slides):
    print(f"Slide {i+2}: {s['text']}")
