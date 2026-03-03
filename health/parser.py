"""
Parse JT's free-form health check-in replies into structured data.

New format (pattern-focused):
  "6, jaw + shoulders, partial, no protocol / 30min walk, 7 woke tense"
  Fields: activation(1-10) | bracing sites | exhale quality | protocol+exercise | sleep

Legacy format still supported:
  "7, neck tension, chicken + salad, 20min walk, 8"
"""

import re
from typing import Optional, Tuple, Dict, Any


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

BRACING_SITES = ["jaw", "shoulders", "shoulder", "glutes", "glute", "belly",
                 "chest", "hips", "hip", "neck", "traps", "back", "none"]

EXHALE_KEYWORDS = {
    "full":    ["full", "fully", "complete", "completely", "good exhale", "clear"],
    "partial": ["partial", "partially", "somewhat", "mostly", "almost", "limited"],
    "blocked": ["blocked", "stuck", "can't", "cannot", "restricted", "tight", "no"],
}

PROTOCOL_DONE = ["yes", "did it", "done", "completed", "full protocol"]
PROTOCOL_PARTIAL = ["partial", "partly", "some", "half", "most of it", "part"]
PROTOCOL_NO = ["no", "nope", "didn't", "did not", "skipped", "skip", "none"]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _extract_number(text: str, lo: int = 1, hi: int = 10) -> Optional[int]:
    for m in re.finditer(r'\b(\d+)\b', text):
        n = int(m.group(1))
        if lo <= n <= hi:
            return n
    return None


def _normalize_field(text: str) -> str:
    return text.strip().strip(':"\'').strip()


def _extract_bracing_sites(text: str) -> Optional[str]:
    """Find bracing sites mentioned in text."""
    lower = text.lower()
    found = []
    for site in BRACING_SITES:
        if site in lower:
            found.append(site)
    if found:
        # dedupe and normalize (shoulder/shoulders → shoulders)
        found = list(dict.fromkeys(found))
        normalized = []
        seen = set()
        for s in found:
            canonical = s.rstrip("s") + "s" if s in ("shoulder", "glute") else s
            if canonical not in seen:
                normalized.append(canonical)
                seen.add(canonical)
        if "none" in normalized:
            return "none"
        return ", ".join(normalized)
    # Legacy pain keywords still supported
    legacy_sites = ["neck", "cervical", "trap", "rhomboid", "lumbar", "sacral",
                    "thoracic", "hip flexor", "psoas", "gluteal", "patella",
                    "knee", "wrist", "head", "headache"]
    for kw in legacy_sites:
        if kw in lower:
            return text.strip()
    # If no pain/bracing found, check for "none" variants
    if any(kw in lower for kw in ["no tension", "no bracing", "nothing", "all clear", "fine"]):
        return "none"
    return None


def _extract_exhale_quality(text: str) -> Optional[str]:
    """Extract exhale quality from text."""
    lower = text.lower()
    for quality, keywords in EXHALE_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return quality
    return None


def _extract_protocol(text: str) -> str:
    """Extract protocol completion from text."""
    lower = text.lower()
    for kw in PROTOCOL_DONE:
        if kw in lower:
            return "protocol: yes"
    for kw in PROTOCOL_PARTIAL:
        if kw in lower:
            return "protocol: partial"
    for kw in PROTOCOL_NO:
        if kw in lower:
            return "protocol: no"
    return "protocol: not logged"


# ─────────────────────────────────────────────────────────────────────────────
# Main parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_checkin(raw: str) -> Dict[str, Any]:
    """
    Parse a health check-in reply. Handles both new pattern-focused format and legacy format.
    Maps to schema: energy, pain_areas, food, exercise, sleep_quality, notes
    """
    result: Dict[str, Any] = {
        "energy": None,        # activation level 1-10
        "pain_areas": None,    # bracing sites
        "food": None,          # food (optional)
        "exercise": None,      # protocol + movement
        "sleep_quality": None, # sleep 1-10
        "notes": None,         # exhale quality + voice notes + anything else
    }

    text = raw.strip()
    lines = [l.strip() for l in text.replace('\r\n', '\n').replace('\r', '\n').split('\n') if l.strip()]

    # ── Strategy 1: Explicitly labeled fields only (requires : = or - separator) ──
    # These patterns require an explicit delimiter so they don't fire on comma-separated format
    label_patterns = {
        "energy":        r'\b(?:activation|activated|energy|feeling|mood|tense|tension level)\s*[:\-=]\s*(.+)',
        "pain_areas":    r'\b(?:bracing|bracing scan|holding|tension sites|tight spots|pain|sore)\s*[:\-=]\s*(.+)',
        "notes":         r'\b(?:exhale|breath|breathing)\s*[:\-=]\s*(.+)',
        "exercise":      r'\b(?:protocol|reset|exercise|workout|movement|moved)\s*[:\-=]\s*(.+)',
        "sleep_quality": r'\b(?:sleep|slept|sleeping)\s*[:\-=]\s*(.+)',
        "food":          r'\b(?:food|ate|eaten|meals?)\s*[:\-=]\s*(.+)',
    }

    matched_lines = set()
    for field, pattern in label_patterns.items():
        for i, line in enumerate(lines):
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                val = _normalize_field(m.group(1))
                if field in ("energy", "sleep_quality"):
                    result[field] = _extract_number(val) or _extract_number(line)
                else:
                    result[field] = val
                matched_lines.add(i)
                break

    # ── Strategy 2: Comma/slash-separated single line ─────────────────────────
    if sum(1 for v in result.values() if v is not None) < 2:
        # Split on commas and em-dashes only — NOT slash (slash used within fields like "protocol: no / 30min walk")
        parts = re.split(r'[,|—–]+', text)
        parts = [p.strip() for p in parts if p.strip()]

        if len(parts) >= 2:
            # Part 1: activation/energy
            if result["energy"] is None:
                result["energy"] = _extract_number(parts[0])

            # Part 5 (last number): sleep
            if result["sleep_quality"] is None and len(parts) >= 4:
                for part in reversed(parts):
                    n = _extract_number(part)
                    if n and n != result["energy"]:
                        result["sleep_quality"] = n
                        break

            # Middle parts: heuristic
            middle = parts[1:-1] if len(parts) >= 4 else parts[1:]
            for part in middle:
                lower = part.lower()

                # Bracing sites (new format)
                if result["pain_areas"] is None:
                    bracing = _extract_bracing_sites(part)
                    if bracing:
                        result["pain_areas"] = bracing
                        continue

                # Exhale quality → notes
                if result["notes"] is None:
                    exhale = _extract_exhale_quality(part)
                    if exhale:
                        result["notes"] = f"exhale: {exhale}"
                        continue

                # Protocol + exercise
                if result["exercise"] is None:
                    proto = _extract_protocol(part)
                    if proto != "protocol: not logged":
                        # Check for exercise too
                        ex_match = re.search(
                            r'(\d+\s*(?:min|minute|hour|hr)s?\s+\w+|\w+\s+\d+\s*(?:min|minute|hour|hr)s?|walk|run|gym|yoga|lift)',
                            part, re.IGNORECASE
                        )
                        result["exercise"] = f"{proto} / {ex_match.group(0)}" if ex_match else proto
                        continue

                # Food (legacy / optional)
                if result["food"] is None and any(kw in lower for kw in [
                    "chicken", "beef", "fish", "rice", "pasta", "salad", "coffee",
                    "ate", "meal", "veg", "protein", "sandwich", "soup", "pizza",
                    "snack", "nothing", "skipped meal", "eggs", "yogurt"
                ]):
                    result["food"] = part

    # ── Strategy 3: Unstructured fallback ─────────────────────────────────────
    if result["energy"] is None:
        m = re.search(r'(?:activation|feel(?:ing)?)\s+(?:like\s+)?(?:a\s+)?(\d+)', text, re.IGNORECASE)
        if m:
            result["energy"] = _extract_number(m.group(1))
        else:
            result["energy"] = _extract_number(text)

    if result["pain_areas"] is None:
        result["pain_areas"] = _extract_bracing_sites(text)

    if result["notes"] is None:
        exhale = _extract_exhale_quality(text)
        if exhale:
            result["notes"] = f"exhale: {exhale}"

    if result["exercise"] is None:
        proto = _extract_protocol(text)
        no_ex = re.search(r'\b(no exercise|didn\'t exercise|skipped exercise|rest day)\b', text, re.IGNORECASE)
        ex_match = re.search(r'(\d+\s*(?:min|minute|hour|hr)s?\s+\w+|\b(?:walked|ran|gym|lifted|yoga|swam)\b)', text, re.IGNORECASE)
        parts_ex = []
        if proto != "protocol: not logged":
            parts_ex.append(proto)
        if ex_match:
            parts_ex.append(ex_match.group(0))
        elif no_ex:
            parts_ex.append("no exercise")
        result["exercise"] = " / ".join(parts_ex) if parts_ex else None

    # ── Sleep fallback ────────────────────────────────────────────────────────
    if result["sleep_quality"] is None:
        m = re.search(r'sleep\w*\s+(?:was\s+)?(?:a\s+)?(\d+)', text, re.IGNORECASE)
        if m:
            result["sleep_quality"] = _extract_number(m.group(1))
        else:
            m2 = re.search(r'slept?\s+(\d+)\s*(?:hr|hour)', text, re.IGNORECASE)
            if m2:
                hrs = int(m2.group(1))
                result["sleep_quality"] = min(10, max(1, hrs - 1)) if hrs < 7 else min(10, hrs)

    # ── Append sleep notes (jaw clenching, woke tense) ───────────────────────
    sleep_notes = re.search(r'(?:wake|woke|waking|jaw|clench|tense)\s+\w+', text, re.IGNORECASE)
    if sleep_notes:
        existing = result["notes"] or ""
        result["notes"] = (existing + " | sleep: " + sleep_notes.group(0)).strip(" |")

    return result


def format_checkin_for_confirm(parsed: Dict[str, Any], raw: str) -> str:
    """Format parsed data for confirmation back to JT — pattern-focused."""
    lines = ["✅ *Check-in logged*\n"]

    activation = parsed.get("energy")
    if activation:
        bar = "🟢" if activation <= 3 else "🟡" if activation <= 6 else "🔴"
        lines.append(f"🧠 Activation: *{activation}/10* {bar}")
    else:
        lines.append("🧠 Activation: not logged")

    bracing = parsed.get("pain_areas")
    lines.append(f"🔒 Bracing: {bracing or 'none reported'}")

    notes = parsed.get("notes") or ""
    if "exhale" in notes.lower():
        exhale_part = [p for p in notes.split("|") if "exhale" in p.lower()]
        lines.append(f"💨 Exhale: {exhale_part[0].replace('exhale:', '').strip() if exhale_part else 'not logged'}")
    else:
        lines.append("💨 Exhale: not logged")

    ex = parsed.get("exercise") or "not logged"
    lines.append(f"⚡ Protocol: {ex}")

    sleep = parsed.get("sleep_quality")
    sleep_bar = "🟢" if sleep and sleep >= 7 else "🟡" if sleep and sleep >= 5 else "🔴" if sleep else ""
    lines.append(f"😴 Sleep: *{sleep or '?'}/10* {sleep_bar}")

    if parsed.get("food"):
        lines.append(f"🥗 Food: {parsed['food']}")

    # Pattern-specific feedback
    lines.append("")
    if activation and activation >= 7:
        lines.append("⚠️ High activation — prioritize Steps 1+2 of protocol before sleep (physiological sigh + extended exhale)")
    elif bracing and bracing != "none" and "jaw" in (bracing or "").lower():
        lines.append("💡 Jaw bracing detected — teeth apart, tongue down, soften masseter before bed")

    return "\n".join(lines)
