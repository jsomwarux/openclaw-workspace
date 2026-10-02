#!/usr/bin/env python3
"""Deterministic checks for plain-English cold-email M1 packets."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List


BANNED_PHRASES = (
    "fixed-scope",
    "workflow audit",
    "map the workflow",
    "map the current",
    "current handoffs",
    "exception ownership",
    "control plan",
    "escalation rules",
    "tool decision",
    "build decision",
    "before anyone buys or builds software",
)

# D1 (batch-1 X-review memo, EC-1): COI outreach copy carries no AI vocabulary.
# Whole words only; a plural counts as the word ("agents" is "agent").
AI_VOCABULARY = (
    "ai",
    "agent",
    "automation",
    "workflow",
    "platform",
    "llm",
    "pipeline",
    "integration",
    "orchestration",
    "harness",
)
AI_VOCABULARY_RE = re.compile(r"\b(" + "|".join(AI_VOCABULARY) + r")s?\b", re.IGNORECASE)
D1_ADVISORY_MAX_WORDS = 75

SIGNATURE_START = "JT Somwaru"
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)?")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]")
SECTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)


def words(text: str) -> List[str]:
    return WORD_RE.findall(text)


def _syllables(word: str) -> int:
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 0
    groups = re.findall(r"[aeiouy]+", cleaned)
    count = len(groups)
    if cleaned.endswith("e") and not cleaned.endswith(("le", "ye")) and count > 1:
        count -= 1
    return max(1, count)


def _content_without_signature(body: str) -> str:
    return body.split(SIGNATURE_START, 1)[0].strip()


def _sentences(text: str) -> List[str]:
    return [match.group(0).strip() for match in SENTENCE_RE.finditer(text)]


def estimated_grade(text: str) -> float:
    tokens = words(text)
    sentences = _sentences(text)
    if not tokens or not sentences:
        return 0.0
    syllable_count = sum(_syllables(token) for token in tokens)
    grade = 0.39 * (len(tokens) / len(sentences)) + 11.8 * (syllable_count / len(tokens)) - 15.59
    return round(max(0.0, grade), 1)


def analyze_message(subject: str, body: str) -> Dict[str, Any]:
    content = _content_without_signature(body)
    tokens = words(content)
    sentences = _sentences(content)
    sentence_lengths = [len(words(sentence)) for sentence in sentences]
    questions = [sentence for sentence in sentences if sentence.endswith("?")]
    errors: List[str] = []
    warnings: List[str] = []

    if not 50 <= len(tokens) <= 85:
        errors.append(f"body word count must be 50-85; found {len(tokens)}")
    elif len(tokens) > D1_ADVISORY_MAX_WORDS:
        warnings.append(f"body over {D1_ADVISORY_MAX_WORDS} words (D1 advisory); found {len(tokens)}")
    if sentence_lengths and max(sentence_lengths) > 20:
        errors.append(f"sentence over 20 words; found {max(sentence_lengths)}")
    average_sentence = round(sum(sentence_lengths) / len(sentence_lengths), 1) if sentence_lengths else 0.0
    if not 8 <= average_sentence <= 14:
        warnings.append(f"average sentence length should be 8-14; found {average_sentence}")

    grade = estimated_grade(content)
    if grade > 8:
        errors.append(f"estimated grade must be at most 8; found {grade}")
    elif grade > 7:
        warnings.append(f"estimated grade exceeds target 5-7; found {grade}")

    lowered = content.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            errors.append(f"banned phrase: {phrase}")
    for term in sorted({match.group(1).lower() for match in AI_VOCABULARY_RE.finditer(content)}):
        errors.append(f"AI vocabulary: {term}")

    if len(questions) != 2:
        errors.append(f"message must contain one operational question and one CTA; found {len(questions)} questions")
    if questions:
        cta_words = len(words(questions[-1]))
        if cta_words > 12:
            errors.append(f"CTA must be at most 12 words; found {cta_words}")

    if not subject or subject != subject.lower():
        errors.append("subject must be present and lowercase")
    subject_words = len(words(subject))
    if not 2 <= subject_words <= 6:
        errors.append(f"subject must contain 2-6 words; found {subject_words}")
    if "—" in body:
        errors.append("em dash is not allowed")
    if SIGNATURE_START not in body:
        errors.append("email signature is required")

    return {
        "subject": subject,
        "word_count": len(tokens),
        "grade": grade,
        "average_sentence_words": average_sentence,
        "max_sentence_words": max(sentence_lengths, default=0),
        "question_count": len(questions),
        "errors": errors,
        "warnings": warnings,
    }


def extract_messages(packet: str) -> List[Dict[str, str]]:
    matches = list(SECTION_RE.finditer(packet))
    messages: List[Dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(packet)
        block = packet[start:end]
        subject_match = re.search(r"^\*\*Subject:\*\*\s*(.+?)\s*$", block, re.MULTILINE)
        note_match = re.search(r"^\*\*Personalization note:\*\*", block, re.MULTILINE)
        if not subject_match or not note_match:
            continue
        body_start = subject_match.end()
        body = block[body_start:note_match.start()].strip()
        messages.append(
            {
                "position": match.group(1),
                "recipient": match.group(2).strip(),
                "subject": subject_match.group(1).strip(),
                "body": body,
            }
        )
    return messages


def _evidence_rows(packet: str) -> List[Dict[str, str]]:
    matches = list(SECTION_RE.finditer(packet))
    rows: List[Dict[str, str]] = []
    fields = ("To", "Source status", "Personalization note", "Verify before send")
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(packet)
        block = packet[start:end]
        row = {"position": match.group(1), "recipient": match.group(2).strip()}
        for field in fields:
            field_match = re.search(rf"^\*\*{re.escape(field)}:\*\*\s*(.+?)\s*$", block, re.MULTILINE)
            row[field] = field_match.group(1).strip() if field_match else ""
        rows.append(row)
    return rows


def compare_packet_evidence(baseline: str, candidate: str) -> List[str]:
    baseline_rows = _evidence_rows(baseline)
    candidate_rows = _evidence_rows(candidate)
    if len(baseline_rows) != len(candidate_rows):
        return [f"evidence row count mismatch: baseline={len(baseline_rows)} candidate={len(candidate_rows)}"]
    errors: List[str] = []
    for baseline_row, candidate_row in zip(baseline_rows, candidate_rows):
        if baseline_row != candidate_row:
            errors.append(f"evidence mismatch at position {baseline_row['position']}: {baseline_row['recipient']}")
    return errors


def _normalized_sentences(messages: Iterable[Dict[str, str]]) -> Counter:
    counts: Counter = Counter()
    for message in messages:
        content = _content_without_signature(message["body"])
        sentences = _sentences(content)
        for sentence in sentences:
            if sentence.endswith("?"):
                continue
            normalized = " ".join(sentence.lower().split())
            if normalized:
                counts[normalized] += 1
    return counts


def validate_batch(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    results = []
    for message in messages:
        result = analyze_message(message["subject"], message["body"])
        result["recipient"] = message["recipient"]
        result["position"] = message.get("position")
        results.append(result)

    batch_errors = []
    for sentence, count in _normalized_sentences(messages).items():
        if count > 3:
            batch_errors.append(f"repeated sentence appears {count} times: {sentence}")

    subjects = [message["subject"] for message in messages]
    duplicate_subjects = [subject for subject, count in Counter(subjects).items() if count > 1]
    if duplicate_subjects:
        batch_errors.append("duplicate subjects: " + ", ".join(sorted(duplicate_subjects)))

    return {
        "message_count": len(messages),
        "passed": not batch_errors and all(not result["errors"] for result in results),
        "batch_errors": batch_errors,
        "messages": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    packet_text = args.packet.read_text(encoding="utf-8")
    result = validate_batch(extract_messages(packet_text))
    if args.baseline:
        result["batch_errors"].extend(
            compare_packet_evidence(args.baseline.read_text(encoding="utf-8"), packet_text)
        )
        result["passed"] = not result["batch_errors"] and all(
            not message["errors"] for message in result["messages"]
        )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.json_output:
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
