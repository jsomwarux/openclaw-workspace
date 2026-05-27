import json
from pathlib import Path

def eval_voicebox():
    # 1. Update Technical Angles for Content
    ta_path = Path('memory/content/technical-angles.md')
    if ta_path.exists():
        content = ta_path.read_text()
        new_angle = "- **Local-First Voice Infrastructure:** Local TTS (Voicebox/MLX) eliminates the trust barrier for high-stakes voice cloning. Businesses that won't touch cloud TTS will deploy a local 'Voice Operator' on-site for automated (human-approved) customer/maintenance alerts. Moat = security + hardware proximity."
        if "Local-First Voice Infrastructure" not in content:
            ta_path.write_text(content.strip() + "\n" + new_angle + "\n")
            print("Updated Technical Angles with Local-First Voice.")

    # 2. Log as Future Signal if not ready for immediate build
    fs_path = Path('memory/future-signals.md')
    if fs_path.exists():
        content = fs_path.read_text()
        signal = "\n- **Signal:** Local-First High-Quality Voice (Voicebox). **Trigger:** Altmark rent-delinquency deployment + proof capture. **Value:** Expansion offer for 'Local-First Voice Desk' (automated human-approved voice alerts)."
        if "Voicebox" not in content:
            fs_path.write_text(content.strip() + signal + "\n")
            print("Logged Voicebox to Future Signals.")

eval_voicebox()
