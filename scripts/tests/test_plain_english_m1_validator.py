import json
import tempfile
import unittest
from pathlib import Path

from scripts.plain_english_m1_validator import (
    analyze_message,
    compare_packet_evidence,
    extract_messages,
    validate_batch,
)


PLAIN_BODY = """Darrell,

IEW runs bridge, utility, and transportation jobs. How does your team track COI renewals after a subcontractor starts work?

I help contractors find missed renewals, pick who follows up, and fix the gaps first. You get a short fix list before spending money on new software.

Worth a quick look?

JT Somwaru
New York City
jtsomwaru.com"""


class AnalyzeMessageTests(unittest.TestCase):
    def test_plain_message_passes_hard_gates(self):
        result = analyze_message("coi renewals", PLAIN_BODY)
        self.assertEqual([], result["errors"])
        self.assertLessEqual(result["grade"], 8.0)
        self.assertGreaterEqual(result["word_count"], 50)
        self.assertLessEqual(result["word_count"], 85)

    def test_rejects_consultant_abstraction(self):
        body = PLAIN_BODY.replace(
            "I help contractors find missed renewals, pick who follows up, and fix the gaps first.",
            "I run a fixed-scope workflow audit that maps the current handoffs and exception ownership.",
        )
        result = analyze_message("coi renewals", body)
        self.assertTrue(any("banned phrase" in error for error in result["errors"]))

    def test_rejects_long_sentence(self):
        body = PLAIN_BODY.replace(
            "IEW runs bridge, utility, and transportation jobs.",
            "IEW runs bridge, utility, and transportation jobs across many sites where project teams, vendors, office staff, and outside partners all share records every day.",
        )
        result = analyze_message("coi renewals", body)
        self.assertTrue(any("sentence over 20 words" in error for error in result["errors"]))

    def test_rejects_oversized_cta(self):
        body = PLAIN_BODY.replace(
            "Worth a quick look?",
            "Would you be open to setting up a thirty minute call with me next week?",
        )
        result = analyze_message("coi renewals", body)
        self.assertTrue(any("CTA" in error for error in result["errors"]))


class PacketTests(unittest.TestCase):
    def test_extracts_numbered_messages(self):
        packet = f"""# Packet

## 1. Darrell Harms, IEW Construction Group

**Subject:** coi renewals

{PLAIN_BODY}

**Personalization note:** verified signal

## 2. Jane Doe, Example Co

**Subject:** coi follow-up

{PLAIN_BODY.replace('Darrell', 'Jane').replace('IEW', 'Example Co')}

**Personalization note:** verified signal
"""
        messages = extract_messages(packet)
        self.assertEqual(2, len(messages))
        self.assertEqual("Darrell Harms, IEW Construction Group", messages[0]["recipient"])

    def test_flags_repeated_batch_sentence(self):
        messages = []
        for index in range(4):
            messages.append(
                {
                    "recipient": f"Person {index}, Company {index}",
                    "subject": f"coi note {index}",
                    "body": PLAIN_BODY.replace("Darrell", f"Person{index}"),
                }
            )
        result = validate_batch(messages)
        self.assertTrue(any("repeated sentence" in error for error in result["batch_errors"]))

    def test_baseline_comparison_rejects_changed_evidence(self):
        baseline = """## 1. Darrell Harms, IEW Construction Group
**To:** d@example.com
**Source status:** verified
**Subject:** old subject

Old body.

**Personalization note:** exact evidence note
**Verify before send:** exact send gate
"""
        candidate = baseline.replace("old subject", "new subject").replace("Old body.", "New body.")
        self.assertEqual([], compare_packet_evidence(baseline, candidate))

        changed = candidate.replace("exact evidence note", "shortened note")
        errors = compare_packet_evidence(baseline, changed)
        self.assertTrue(any("evidence mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
