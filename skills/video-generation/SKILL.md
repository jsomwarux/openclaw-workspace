# Video Generation (Vibe Marketing) Skill
> Unified capability for dynamically generating TikTok videos and Instagram Reels for new apps and products.

## Description
This skill leverages OpenClaw's existing image-processing and video-synthesis framework (`vibe-marketing`) to automatically compile product screenshots, overlay compelling text, render an MP4 slideshow via the Reelfarm API, and queue it for posting.

## Usage
`openclaw sessions_spawn --agentId [id] --task "Create a new TikTok video for [Product] using the video-generation skill"`
For Codex: "Once the new feature UI is complete, run the video-generation skill to create a promotional reel."

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
