import sys
path = "/Users/jtsomwaru/.openclaw/workspace/scripts/vibe-post.py"
with open(path, "r") as f:
    content = f.read()

import re

# We already have parse_slides_from_content in vibe-post.py, let's use it for the caption!
replacement = """def build_caption(entry: dict) -> tuple[str, str]:
    \"\"\"Build caption (max 89 chars, no hashtags) from the first slide's text.\"\"\"
    hashtags = entry.get("hashtags", "")
    content = entry.get("content", "")
    
    # Extract slides using the already defined parse_slides_from_content function
    slides = parse_slides_from_content(content)
    
    hook = ""
    if slides and len(slides) > 0:
        hook = slides[0].get("text", "")
        # Remove any newlines or weird spacing
        hook = " ".join(hook.split())
        
    # Truncate to 89 chars if necessary
    if len(hook) > 89:
        hook = hook[:86] + "..."
        
    caption = hook if hook else "Movie Taste Profiles" # Fallback better than "watch this"
    description = hashtags if hashtags else ""
    return caption, description
"""

old_build_caption_pattern = r'def build_caption\(entry: dict\) -> tuple\[str, str\]:.*?return caption, description'

if re.search(old_build_caption_pattern, content, re.DOTALL):
    content = re.sub(old_build_caption_pattern, replacement, content, flags=re.DOTALL)
    with open(path, "w") as f:
        f.write(content)
    print("Patched build_caption")
else:
    print("Could not find build_caption")
