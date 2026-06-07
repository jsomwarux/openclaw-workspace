# Video Generation / Demo Proof Skill
> Unified capability for generating short product videos, launch reels, and proof/demo clips.

## Description
Use this when a shipped app feature, client workflow, proof pack, launch, README, PR, or portfolio update would benefit from a short MP4/GIF. Marketing videos are one use case; proof videos are now a default candidate whenever the work can be shown safely.

Core rule: if something ships and can be visually demonstrated without exposing private data, create a 20-45s demo script before deciding it is "content-ready" or "proof-ready."

## Usage
`openclaw sessions_spawn --agentId [id] --task "Create a new TikTok video for [Product] using the video-generation skill"`
For Codex: "Once the new feature UI is complete, run the video-generation skill to create a promotional reel."

## Demo Proof Workflow
1. Identify the thing shipped and the audience: JT, client, PR reviewer, portfolio visitor, X/LinkedIn/TikTok.
2. Write `script.md`: hook, 3-5 beats, captions, proof point, CTA or next action.
3. Use redacted, anonymized, or synthetic data for client work unless permission is explicit.
4. Render MP4 for social/client review; render GIF for GitHub README/PR/issue when useful.
5. Link the asset from the Client OS, proof log, portfolio queue, or content bank.

## Execution Framework (Python Mapping)
The heavy lifting is handled by Python scripts in the `scripts/` directory. 

**1. Photo Selection (`photo-selector.py`):**
Identify the product and dynamically grab its associated `real-photos/` assets.
- Command pattern: `python3 scripts/photo-selector.py --product "[Product Slug]"`

**2. Video Rendering (`reelfarm-create-slideshow.py`):**
Takes the selected photos, applies text overlays (via `tiktok-text-overlay.py` internally), calls the Reelfarm API, and returns an MP4 structure.
- Command pattern: `python3 scripts/reelfarm-create-slideshow.py`
- *Note:* Product metadata is fetched automatically using the `--product` arguments built into the scripts. Ensure `.json` output is correctly parsed by capturing the exact object format.

**3. Queueing and Posting (`vibe-post.py`):**
Once a video is generated, use this tool to queue the asset into `agents/vibe-marketing/queue.jsonl` or post it immediately.
- Command pattern: `python3 scripts/vibe-post.py`
