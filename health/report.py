"""
Weekly health report generator.
Analyzes 7 days of check-ins and produces a specific, actionable report.
"""
import re
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from collections import Counter
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from db import get_recent_checkins


# ── Keyword maps ──────────────────────────────────────────────────────────────

# Primary bracing sites for JT's pattern
BRACING_KEYWORDS = {
    "jaw":        ["jaw", "masseter", "clench", "teeth", "tmj"],
    "shoulders":  ["shoulder", "trap", "traps", "rotator", "scapula"],
    "glutes":     ["glute", "glutes", "gluteal", "piriformis"],
    "belly":      ["belly", "abdominal", "abdomen", "stomach", "core"],
    "chest":      ["chest", "pec", "pecs", "sternum", "ribcage", "ribs"],
    "neck":       ["neck", "cervical", "suboccipital"],
    "hips":       ["hip", "hips", "hip flexor", "psoas"],
    "lower_back": ["lower back", "lumbar", "sacral"],
}

# Legacy pain keywords (backward compat)
PAIN_KEYWORDS = {
    "neck":        ["neck", "cervical"],
    "shoulders":   ["shoulder", "trap", "traps", "rotator"],
    "upper_back":  ["upper back", "thoracic", "rhomboid"],
    "lower_back":  ["lower back", "lumbar", "sacral", "si joint"],
    "hips":        ["hip", "hips", "hip flexor", "psoas", "glute", "gluteal"],
    "knees":       ["knee", "knees", "patella"],
    "wrists":      ["wrist", "wrists", "forearm"],
    "headache":    ["head", "headache", "migraine"],
}

EXHALE_MAP = {"full": 3, "partial": 2, "blocked": 1}

FOOD_QUALITY = {
    "good":       ["vegetable", "veg", "salad", "fruit", "chicken", "fish", "salmon",
                   "rice", "quinoa", "egg", "protein", "legume", "bean", "lentil", "oat",
                   "greek yogurt", "nuts", "avocado", "sweet potato"],
    "processed":  ["pizza", "burger", "fries", "chips", "soda", "fast food", "mcdonald",
                   "taco bell", "kfc", "wendy", "mcflurry", "ice cream", "candy", "cookie",
                   "pastry", "donut", "processed", "frozen", "microwaved"],
    "mixed":      ["pasta", "bread", "sandwich", "wrap", "coffee"],
}


def _avg(values: List[Optional[int]]) -> Optional[float]:
    nums = [v for v in values if v is not None]
    return round(sum(nums) / len(nums), 1) if nums else None


def _trend(values: List[Optional[int]]) -> str:
    nums = [v for v in values if v is not None]
    if len(nums) < 3:
        return "insufficient data"
    first_half = nums[:len(nums)//2]
    second_half = nums[len(nums)//2:]
    avg_first = sum(first_half)/len(first_half)
    avg_second = sum(second_half)/len(second_half)
    diff = avg_second - avg_first
    if diff >= 1:
        return "↑ improving"
    elif diff <= -1:
        return "↓ declining"
    else:
        return "→ stable"


def _count_bracing_sites(checkins: List[Dict]) -> Counter:
    """Count how often each bracing site appears across check-ins."""
    counter: Counter = Counter()
    for c in checkins:
        raw = (c.get("pain_areas") or "").lower()
        if not raw or raw in ("none", "nothing", "no bracing", "fine", "good", "n/a"):
            continue
        for site, keywords in BRACING_KEYWORDS.items():
            if any(kw in raw for kw in keywords):
                counter[site] += 1
    return counter


def _count_pain_areas(checkins: List[Dict]) -> Counter:
    """Legacy — uses combined bracing + pain keywords."""
    counter: Counter = Counter()
    for c in checkins:
        raw = (c.get("pain_areas") or "").lower()
        if not raw or raw in ("none", "nothing", "no pain", "fine", "good", "n/a"):
            continue
        for area, keywords in {**BRACING_KEYWORDS, **PAIN_KEYWORDS}.items():
            if any(kw in raw for kw in keywords):
                counter[area] += 1
    return counter


def _analyze_exhale(checkins: List[Dict]) -> Dict[str, Any]:
    """Track exhale quality from notes field."""
    scores = []
    blocked_days = 0
    full_days = 0
    for c in checkins:
        notes = (c.get("notes") or "").lower()
        if "exhale" not in notes:
            continue
        for quality, score in EXHALE_MAP.items():
            if quality in notes:
                scores.append(score)
                if quality == "blocked":
                    blocked_days += 1
                elif quality == "full":
                    full_days += 1
                break
    return {
        "logged": len(scores),
        "avg_score": round(sum(scores) / len(scores), 1) if scores else None,
        "blocked_days": blocked_days,
        "full_days": full_days,
    }


def _analyze_protocol(checkins: List[Dict]) -> Dict[str, Any]:
    """Track protocol completion from exercise field."""
    done, partial, missed, not_logged = 0, 0, 0, 0
    for c in checkins:
        ex = (c.get("exercise") or "").lower()
        if "protocol: yes" in ex:
            done += 1
        elif "protocol: partial" in ex:
            partial += 1
        elif "protocol: no" in ex:
            missed += 1
        else:
            not_logged += 1
    return {"done": done, "partial": partial, "missed": missed, "not_logged": not_logged}


def _analyze_diet(checkins: List[Dict]) -> Dict[str, Any]:
    good_days, processed_days, logged_days = 0, 0, 0
    protein_days, vegetable_days = 0, 0

    for c in checkins:
        food = (c.get("food") or "").lower()
        if not food or food in ("none", "not logged", "n/a"):
            continue
        logged_days += 1
        has_good = any(kw in food for kw in FOOD_QUALITY["good"])
        has_processed = any(kw in food for kw in FOOD_QUALITY["processed"])
        has_protein = any(kw in food for kw in ["chicken", "beef", "fish", "salmon", "egg",
                                                  "protein", "steak", "tuna", "turkey", "greek yogurt"])
        has_veg = any(kw in food for kw in ["vegetable", "veg", "salad", "broccoli", "spinach",
                                              "kale", "greens", "cucumber", "carrot", "pepper"])
        if has_good and not has_processed:
            good_days += 1
        elif has_processed:
            processed_days += 1
        if has_protein:
            protein_days += 1
        if has_veg:
            vegetable_days += 1

    return {
        "logged_days": logged_days,
        "good_days": good_days,
        "processed_days": processed_days,
        "protein_days": protein_days,
        "vegetable_days": vegetable_days,
    }


def _analyze_exercise(checkins: List[Dict]) -> Dict[str, Any]:
    exercise_days = 0
    rest_days = 0
    activities = []

    for c in checkins:
        ex = (c.get("exercise") or "").lower().strip()
        if not ex or ex in ("none", "no", "skipped", "rest day", "rest", "n/a", "not logged"):
            rest_days += 1
        elif ex:
            exercise_days += 1
            activities.append(ex)

    return {
        "exercise_days": exercise_days,
        "rest_days": rest_days,
        "activities": activities,
    }


def _pattern_suggestion(
    bracing_counter: Counter,
    avg_activation: Optional[float],
    exhale: Dict,
    protocol: Dict,
    avg_sleep: Optional[float],
    checkins: List[Dict],
) -> str:
    """
    Generate ONE specific, actionable suggestion for JT's centrally-driven tension pattern.
    Addresses the three mechanisms in priority order based on the week's data.
    """
    n = len(checkins)

    # ── Mechanism 3: Respiratory restriction (highest structural priority) ────
    if exhale["blocked_days"] and exhale["blocked_days"] >= 2:
        return (
            f"Your exhale was blocked {exhale['blocked_days']} days this week — this is the "
            "respiratory restriction mechanism active. The system is locked in extension. "
            "Priority this week: Step 1 of your protocol FIRST THING EVERY MORNING before "
            "you check your phone. Do 2 physiological sighs immediately on waking (double "
            "inhale + long exhale), then 10 cycles of 4-in/8-out. The exhale is the brake "
            "pedal of your nervous system. Until this clears, the bracing pattern will keep "
            "reasserting no matter what else you do."
        )

    # ── Mechanism 1: Autonomic dysregulation (if activation running high) ─────
    if avg_activation is not None and avg_activation >= 6.5:
        return (
            f"Average activation this week: {avg_activation}/10 — your sympathetic system is "
            "running persistently high. This is the upstream driver of everything else. "
            "The most efficient intervention: extend your exhales throughout the day, not "
            "just in protocol time. Every time you're waiting (phone, elevator, stoplight) "
            "— do one 4-in/8-out breath. 10 of these spread across your day drops your "
            "baseline more than a single 10-minute session. Also: jaw check at every transition "
            "— teeth apart, tongue down, jaw soft. You're probably clenching unconsciously."
        )

    # ── Protocol adherence check ──────────────────────────────────────────────
    total_logged = protocol["done"] + protocol["partial"] + protocol["missed"]
    if total_logged >= 3 and protocol["missed"] > protocol["done"]:
        return (
            f"Protocol completion this week: {protocol['done']} full, {protocol['partial']} partial, "
            f"{protocol['missed']} missed. The pattern requires daily input — this is the "
            "minimum effective dose. If the full 7 minutes feels like too much, use the "
            "emergency reset on missed days: Steps 1+2 only (physiological sigh × 2 + "
            "10 cycles of extended exhale). That's 3 minutes and hits the highest-leverage "
            "mechanism. Something every day beats nothing 4 days + full session 3 days."
        )

    # ── Mechanism 2: Structural — most frequent bracing site ─────────────────
    if bracing_counter:
        top_site = bracing_counter.most_common(1)[0][0]
        count = bracing_counter.most_common(1)[0][1]
        suggestions = {
            "jaw": (
                f"Jaw bracing showed up {count}/{n} days — this is your most accessible "
                "reset point. The jaw and pelvic floor share autonomic tone; releasing one "
                "releases the other. Practice this every time you sit down to work: "
                "teeth apart, tongue resting on the floor of your mouth (not the roof), "
                "masseter soft. Set an hourly phone reminder just with 🦷 as the trigger. "
                "Also add jaw circles to your protocol (Step 2): 5 each direction after the "
                "30-second hold."
            ),
            "shoulders": (
                f"Shoulder/trap bracing appeared {count}/{n} days — common compensation "
                "pattern downstream of the gunstock asymmetry loading the kinetic chain "
                "unevenly. Focus: Step 4 of your protocol (shoulder asymmetry release) — "
                "identify which shoulder is higher each session and focus the release there. "
                "During the day: every time you catch yourself, do one shoulder DROP — "
                "lift shoulders to ears, hold 2 seconds, let them completely fall. Your "
                "resting position is likely one shoulder forward and up."
            ),
            "glutes": (
                f"Glute bracing appeared {count}/{n} days — this is a protective pattern "
                "often related to pelvic instability or hip asymmetry in your kinetic chain. "
                "Your pelvis is likely tilted or rotated as a compensation. Prioritize Step 4 "
                "of your protocol: pelvic neutral reset + hip/psoas release. Consciously "
                "notice whether you're bracing your glutes when sitting — you shouldn't need "
                "to clench to stay upright in a chair."
            ),
            "belly": (
                f"Belly/abdominal bracing appeared {count}/{n} days — this directly drives "
                "the respiratory restriction. When the belly is braced, the diaphragm can't "
                "drop fully, which truncates the exhale. This is the structural-respiratory "
                "bridge. Priority: Step 3 of your protocol (ribcage expansion). Place your "
                "hands on your lower ribs and specifically practice letting the belly RELEASE "
                "on the inhale. If it stays rigid, you're breathing paradoxically."
            ),
            "chest": (
                f"Chest tension appeared {count}/{n} days — chest bracing locks the ribcage "
                "in partial extension, which directly maintains the respiratory restriction. "
                "Your exhale can't complete if your chest stays lifted and forward. "
                "Step 3 of your protocol is your focus: ribcage compression on exhale — "
                "feel the chest actively drop DOWN and IN as you exhale. The exhale should "
                "feel like a release, not a forced push."
            ),
            "neck": (
                f"Neck bracing appeared {count}/{n} days — often a forward head compensation "
                "from the structural pattern. During screen time: chin tucks (pull chin "
                "straight back, not down) hold 3 seconds × 10, every hour. This re-positions "
                "your atlas and resets the suboccipital muscles that drive cervicogenic tension. "
                "Also check: is your monitor too low? The top of the screen should be eye level."
            ),
        }
        if top_site in suggestions:
            return suggestions[top_site]

    # ── Sleep as secondary factor ─────────────────────────────────────────────
    if avg_sleep is not None and avg_sleep < 6.5:
        return (
            f"Sleep averaged {avg_sleep}/10 this week — poor sleep directly elevates "
            "sympathetic tone the next day, which maintains the bracing pattern. "
            "Your protocol's Step 1 (extended exhale breathing) done for 5 minutes before "
            "sleep will significantly improve sleep quality — this is clinically validated for "
            "autonomic dysregulation. Also: jaw and shoulders during sleep — if you wake "
            "tense, you're bracing at night too. Consider a night guard assessment."
        )

    # ── Good week ─────────────────────────────────────────────────────────────
    return (
        "Solid week. To keep improving: track your activation baseline — what number do "
        "you register FIRST THING in the morning before anything stimulates you? That number "
        "is your true resting sympathetic tone. The goal is to watch it drop over weeks "
        "from consistent protocol work. If it's still ≥5 on waking, the autonomic "
        "dysregulation is the layer that needs the most attention."
    )


def _specific_suggestion(
    pain_counter: Counter,
    avg_energy: Optional[float],
    avg_sleep: Optional[float],
    diet: Dict,
    exercise: Dict,
    checkins: List[Dict],
) -> str:
    """
    Generate ONE specific, actionable suggestion based on actual data.
    Priority: most frequent pain area > sleep > energy > diet > exercise.
    """
    # ── Pain-specific stretching suggestions ─────────────────────────────────
    if pain_counter:
        top_pain = pain_counter.most_common(1)[0][0]

        suggestions = {
            "neck": (
                "Your neck showed up most this week. Tonight before bed: drop your right ear to "
                "your right shoulder, hold 30s, switch sides. Then do 10 slow chin tucks (pull "
                "your chin straight back, hold 3s). This targets the suboccipital muscles that "
                "usually drive neck tension when screen time is high."
            ),
            "shoulders": (
                "Shoulder/trap tension dominated this week. Do this right now: stand in a doorway, "
                "arms at 90°, gently press hands into the frame for 5s, then step forward slowly. "
                "Hold the stretch 30s. Follow with 10 shoulder circles backward. Your traps are "
                "likely overworked from a forward head posture at your desk."
            ),
            "upper_back": (
                "Your upper back was the main tension area. Try this tonight: lie on your back with "
                "a foam roller or rolled towel under your thoracic spine (mid-back), arms crossed "
                "over chest, and gently extend backward over it for 2 minutes. This counteracts "
                "the flexion posture most people hold all day."
            ),
            "lower_back": (
                "Lower back came up most this week. Before bed: lie on your back, pull both knees "
                "to your chest for 30s, then do 10 pelvic tilts (flatten your back against the "
                "floor, hold 3s, release). Your hip flexors are probably tight from sitting — "
                "follow with a 2-minute kneeling hip flexor stretch on each side."
            ),
            "hips": (
                "Hip tension was your theme this week. Tonight: 5 minutes of hip flexor stretching — "
                "kneel on your right knee, left foot forward, drive your hips forward gently until "
                "you feel a stretch in the front of your right hip. Hold 45s each side. If you sit "
                "for long stretches, set a 45-minute timer to stand and do 10 glute bridges."
            ),
            "knees": (
                "Your knees were a recurring issue. Check your footwear — worn-out soles shift "
                "load to the knee. Tonight: 2 minutes of calf stretching against a wall (straight "
                "and bent-knee variations), and 15 slow terminal knee extensions with a light band "
                "or just bodyweight to strengthen your VMO (inner quad), which stabilizes the knee."
            ),
            "wrists": (
                "Wrist tension keeps showing up — likely from keyboard/mouse usage. Try this every "
                "2 hours: extend one arm forward, palm up, and gently pull your fingers down with "
                "your other hand for 20s. Then palm down, pull fingers up for 20s. Also consider "
                "raising your monitor to reduce wrist extension while typing."
            ),
            "headache": (
                "Recurring headaches this week — these are almost always cervicogenic (neck-driven) "
                "or dehydration-related. First: drink a full glass of water now. Tonight: massage "
                "the base of your skull (suboccipitals) in small circles for 2 minutes, and do 10 "
                "slow neck rotations. If headaches keep coming, check your monitor height — the "
                "top of the screen should be at eye level."
            ),
        }
        if top_pain in suggestions:
            return suggestions[top_pain]

    # ── Sleep suggestion ──────────────────────────────────────────────────────
    if avg_sleep is not None and avg_sleep < 6.5:
        return (
            f"Your average sleep was {avg_sleep}/10 this week — that's your biggest performance "
            "lever right now. Try this: set a hard cutoff to put your phone face-down 45 minutes "
            "before bed (not just on silent — face-down removes the temptation to check). "
            "Keep your room at 67–68°F if possible. Poor sleep compounds muscle tension, "
            "so fixing sleep will likely help your pain areas too."
        )

    # ── Energy suggestion ─────────────────────────────────────────────────────
    if avg_energy is not None and avg_energy < 6.0:
        return (
            f"Energy averaged {avg_energy}/10 this week. The fastest lever to pull: eat protein "
            "within 90 minutes of waking — aim for 30g+ (3 eggs, Greek yogurt + protein shake, "
            "or leftover chicken). Skipping breakfast or eating mostly carbs in the morning "
            "causes blood sugar crashes by noon that tank afternoon energy."
        )

    # ── Diet suggestion ───────────────────────────────────────────────────────
    if diet["logged_days"] > 0:
        if diet["vegetable_days"] < diet["logged_days"] / 2:
            return (
                "You logged food {logged} days this week, and vegetables only showed up {veg} days. "
                "Easiest fix: add a handful of spinach to whatever you're already eating — "
                "throw it in eggs, blend it in a shake (you won't taste it), or add a side "
                "salad. This isn't about eating 'clean' — it's about getting micronutrients "
                "that reduce inflammation and improve recovery from tension/stress."
            ).format(logged=diet["logged_days"], veg=diet["vegetable_days"])

        if diet["protein_days"] < diet["logged_days"] / 2:
            return (
                "Protein only showed up in your food logs {prot} out of {logged} days. Muscle "
                "tension recovery requires protein for tissue repair. Aim for at least one "
                "protein-focused meal daily: 4-6oz chicken/fish/beef, or 1 cup Greek yogurt, "
                "or 3 eggs. This directly supports your muscle tension issues."
            ).format(prot=diet["protein_days"], logged=diet["logged_days"])

    # ── Exercise suggestion ───────────────────────────────────────────────────
    if exercise["exercise_days"] < 3:
        return (
            f"You exercised {exercise['exercise_days']} out of 7 days. You don't need a gym — "
            "10 minutes of morning movement (10 squats, 10 push-ups, 10 hip bridges, 30s plank) "
            "done consistently does more than 2 intense workouts separated by 5 sedentary days. "
            "Start tomorrow morning before you open your phone."
        )

    return (
        "Solid week overall. To keep building: add one intentional recovery session — "
        "20 minutes of slow, deliberate stretching while watching something, focusing on "
        "whatever area felt tightest this week. Recovery is where the gains happen."
    )


def generate_weekly_report(days: int = 7) -> str:
    """Generate a weekly health report focused on JT's nervous system tension pattern."""
    checkins = get_recent_checkins(days)

    if not checkins:
        return "📊 *Weekly Health Report*\n\nNo check-in data yet — start logging with the evening check-ins!"

    n = len(checkins)
    activations = [c.get("energy") for c in checkins]   # 'energy' field = activation level
    sleeps      = [c.get("sleep_quality") for c in checkins]

    avg_activation = _avg(activations)
    avg_sleep      = _avg(sleeps)
    activation_trend = _trend(activations[::-1])
    sleep_trend      = _trend(sleeps[::-1])

    bracing_counter = _count_bracing_sites(checkins)
    exhale          = _analyze_exhale(checkins)
    protocol        = _analyze_protocol(checkins)
    diet            = _analyze_diet(checkins)

    # ── Format activation ─────────────────────────────────────────────────────
    if avg_activation:
        act_bar = "🟢 calm" if avg_activation <= 3 else "🟡 elevated" if avg_activation <= 6 else "🔴 high"
        act_summary = f"{avg_activation}/10 {act_bar} · Trend: {activation_trend}"
    else:
        act_summary = "not enough data"

    # ── Format bracing sites ──────────────────────────────────────────────────
    if bracing_counter:
        bracing_summary = ", ".join(
            f"{site} ({cnt}×)" for site, cnt in bracing_counter.most_common(4)
        )
    else:
        bracing_summary = "none reported ✓"

    # ── Format exhale quality ─────────────────────────────────────────────────
    if exhale["logged"] > 0:
        exhale_label = (
            "🟢 mostly full" if exhale["avg_score"] and exhale["avg_score"] >= 2.5
            else "🟡 partial most days" if exhale["avg_score"] and exhale["avg_score"] >= 1.8
            else "🔴 frequently blocked"
        )
        exhale_summary = f"{exhale_label} ({exhale['logged']}/{n} days logged)"
    else:
        exhale_summary = "not logged — add exhale quality to check-ins"

    # ── Format protocol adherence ─────────────────────────────────────────────
    proto_total = protocol["done"] + protocol["partial"] + protocol["missed"]
    if proto_total > 0:
        adherence_pct = round(((protocol["done"] + 0.5 * protocol["partial"]) / proto_total) * 100)
        proto_bar = "🟢" if adherence_pct >= 70 else "🟡" if adherence_pct >= 40 else "🔴"
        proto_summary = f"{proto_bar} {adherence_pct}% ({protocol['done']} full · {protocol['partial']} partial · {protocol['missed']} missed)"
    else:
        proto_summary = "not logged"

    # ── Sleep summary ─────────────────────────────────────────────────────────
    sleep_bar = "🟢" if avg_sleep and avg_sleep >= 7 else "🟡" if avg_sleep and avg_sleep >= 5.5 else "🔴"
    sleep_summary = f"{avg_sleep or 'N/A'}/10 {sleep_bar} · Trend: {sleep_trend}" if avg_sleep else "not enough data"

    # ── Diet (brief) ──────────────────────────────────────────────────────────
    diet_note = f"logged {diet['logged_days']}/{n} days" if diet["logged_days"] else "not logged"

    # ── Pattern-specific suggestion ───────────────────────────────────────────
    suggestion = _pattern_suggestion(
        bracing_counter, avg_activation, exhale, protocol, avg_sleep, checkins
    )

    # ── Week range ────────────────────────────────────────────────────────────
    dates = sorted(c["date"] for c in checkins)
    week_range = f"{dates[0]} → {dates[-1]}" if len(dates) > 1 else dates[0]

    report = f"""📊 *Weekly Health Report*
_{week_range} · {n} check-in{'s' if n != 1 else ''}_

*🧠 Mechanism 1 — Autonomic (Activation)*
{act_summary}

*💨 Mechanism 3 — Respiratory (Exhale Quality)*
{exhale_summary}

*🔒 Mechanism 2 — Structural (Bracing Sites)*
Most frequent: {bracing_summary}

*⚡ Protocol Adherence*
{proto_summary}

*😴 Sleep*
{sleep_summary}

*🥗 Food*
{diet_note}

*💡 Focus This Week*
{suggestion}

---
_Protocol reference: ~/.openclaw/workspace/health/protocol.md_
_Reply with evening check-in anytime or ask for specific data._"""

    return report


if __name__ == "__main__":
    print(generate_weekly_report())
