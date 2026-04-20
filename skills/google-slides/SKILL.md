# Google Slides Generation Skill
> Unified capability for generating dynamic Google Slides presentations via the OpenClaw script framework.

## Description
This skill leverages the existing `scripts/slides_framework.py` engine to programmatically create Google Slides decks, inject dynamic text, build emotional-arc narratives, and output shareable Drive URLs. Used for client proposals, case studies, or any structured presentation.

## Usage
`openclaw sessions_spawn --agentId [id] --task "Create a 5-slide Google Slides presentation on [Topic] using the google-slides skill"`
For Codex: "Review this data and pipe it into a Google Slides presentation using the python framework defined in this skill."

## Execution Framework (Python Mapping)
The heavy lifting is handled by Python scripts in the `scripts/` directory, which use the official Google APIs and service account credentials.

**1. The Engine (`slides_framework.py`):**
Contains the core class methods for presentation building:
- `create_presentation(title)`
- `add_slide(presentation_id, layout_mode)`
- `insert_text(presentation_id, shape_id, text)`

**2. The Implementations (Examples):**
If you need to build a new type of deck, copy the architecture of:
- `scripts/create_slides_deck.py`
- `scripts/build_wholesale_t2_deck.py`

## Building a New Deck (Codex/Agent Instructions)
1. **Analyze Content:** Determine the narrative arc (e.g., Problem → Stakes → Solution → Proof → ROI → CTA).
2. **Prepare Data:** Format your content into a clean JSON dict mapping slide layout keys to exact text.
3. **Execute Scripting:** Write a one-off python script that imports `slides_framework.py`, passes your JSON data into the slide generators, and runs the main loop.
4. **Deliver URL:** The script will output a valid Google Slides URL. Return this URL to the user.

*Note: All Google API auth is handled automatically by the environment variables available to the OpenClaw Python process. You do not need to write new authentication logic.*
