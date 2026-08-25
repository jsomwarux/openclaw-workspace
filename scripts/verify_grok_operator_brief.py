#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_grok_operator_brief.py PATH")
        return 2
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []

    expected = [f"## {i}." for i in range(14)]
    positions = []
    for heading in expected:
        pos = text.find(heading)
        if pos < 0:
            failures.append(f"missing section heading: {heading}")
        positions.append(pos)
    present_positions = [p for p in positions if p >= 0]
    if present_positions != sorted(present_positions):
        failures.append("section headings are not in numeric order")

    required_phrases = [
        "**FACT**", "**INFERENCE**", "**UNKNOWN**",
        "AUTOMATION AUTOPSY", "WHAT EVE WAS GOOD AND BAD AT",
        "WHAT GROK BOT SHOULD INVENT", "ONE-PAGE SEED FOR GROK BOT",
        "QUESTIONS ONLY JT CAN ANSWER", "$5,400", "2026-09-02",
        "2026-09-15", "2026-11-17", "2 priced conversations/week",
        "Daily Workout Card", "Friday Scoreboard",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            failures.append(f"missing required phrase: {phrase}")

    if len(text) < 20000:
        failures.append(f"brief unexpectedly short: {len(text)} characters")
    if len(re.findall(r"\|", text)) < 100:
        failures.append("brief lacks expected operational tables")

    secret_patterns = {
        "OpenAI-style key": r"\bsk-[A-Za-z0-9_-]{20,}\b",
        "Bearer token": r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}",
        "private key": r"BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY",
    }
    for label, pattern in secret_patterns.items():
        if re.search(pattern, text):
            failures.append(f"possible secret detected: {label}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS sections=14 chars={len(text)} tables={text.count('|')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
