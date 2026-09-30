"""Build and validate immutable manual LinkedIn fixture packets."""

from __future__ import annotations

import io
import json
import re
import tempfile
from datetime import datetime, timedelta
from pathlib import Path, PurePosixPath
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from scripts.linkedin_content_os.canonical import (
    canonical_bytes,
    sha256_hex,
    write_json_atomic,
)
from scripts.linkedin_content_os.contracts import parse_timestamp


_SPEC_FIELDS = {
    "schemaVersion",
    "packetId",
    "revisionFamilyId",
    "packetVersion",
    "lane",
    "createdAt",
    "expiresAt",
    "targetReader",
    "commercialObjective",
    "whyThisWon",
    "postText",
    "sources",
    "claims",
    "earnedAngle",
    "conflictChecks",
    "visual",
    "altText",
    "cropGuidance",
    "privacyResult",
    "rightsResult",
    "qa",
}
_SOURCE_FIELDS = {
    "sourceId",
    "sourceType",
    "uri",
    "publishedAt",
    "retrievedAt",
    "publisher",
    "title",
    "excerpts",
}
_CLAIM_FIELDS = {
    "claimId",
    "text",
    "attributionType",
    "sourceId",
    "excerptIndex",
}
_ANGLE_FIELDS = {
    "kind",
    "path",
    "excerpt",
    "fileSha256",
    "confirmationPath",
    "confirmationExcerpt",
    "confirmationFileSha256",
}
_CONFLICT_FIELDS = {"check", "status", "evidence"}
_VISUAL_FIELDS = {"template", "eyebrow", "title", "subtitle", "stages", "footer"}
_RESULT_FIELDS = {"status", "details"}
_QA_FIELDS = {"evidence", "originality", "privacy", "rights", "strategicFit", "voice"}
_PACKET_FIELDS = {
    "schemaVersion",
    "packetId",
    "revisionFamilyId",
    "packetVersion",
    "lane",
    "state",
    "createdAt",
    "expiresAt",
    "targetReader",
    "commercialObjective",
    "whyThisWon",
    "postText",
    "sourceBindings",
    "claimEvidence",
    "earnedAngle",
    "conflictChecks",
    "visualRoute",
    "imageAsset",
    "altText",
    "cropGuidance",
    "privacyResult",
    "rightsResult",
    "qa",
    "decisionOptions",
    "draftSha256",
    "payloadSha256",
}
_ASSET_FIELDS = {"path", "mimeType", "width", "height", "byteLength", "sha256"}
_LANES = {"teardown", "ai_news"}
_ATTRIBUTIONS = {"public_fact", "vendor_assertion", "jt_verified_fact", "hypothesis"}
_HASH64 = re.compile(r"^[0-9a-f]{64}$")
_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_INTERNAL_TERMS = (
    "mission control",
    "openclaw",
    "content os",
    "growth os",
    "decagon",
    "job search",
)
_REQUIRED_CONFLICT_CHECKS = {
    "ai_news": {"source_identity", "claim_attribution", "protected_purpose_removed"},
    "teardown": {
        "consulting_suppression",
        "client_conflict",
        "prospect_conflict",
        "job_conflict",
        "employer_conflict",
    },
}


def _exact_fields(value: dict[str, object], fields: set[str], label: str) -> None:
    if set(value) != fields:
        raise ValueError("{} schema fields are not closed".format(label))


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError("{} must be non-empty trimmed text".format(label))
    if any(ord(character) < 32 and character not in "\n\t" for character in value):
        raise ValueError("{} contains control characters".format(label))
    return value


def _hash(value: object, label: str) -> str:
    text = _text(value, label)
    if _HASH64.fullmatch(text) is None:
        raise ValueError("{} must be a lowercase SHA-256".format(label))
    return text


def _safe_path(value: object, label: str) -> str:
    path = _text(value, label)
    parsed = PurePosixPath(path)
    if parsed.is_absolute() or any(part in {"", ".", ".."} for part in parsed.parts):
        raise ValueError("{} must be repository relative".format(label))
    return path


def _slug(value: object, label: str) -> str:
    text = _text(value, label)
    if _SLUG.fullmatch(text) is None:
        raise ValueError("{} must be a lowercase slug".format(label))
    return text


def _public_safe_text(value: object, label: str) -> str:
    text = _text(value, label)
    lowered = text.lower()
    if any(term in lowered for term in _INTERNAL_TERMS):
        raise ValueError("{} exposes prohibited internal machinery".format(label))
    if re.search(r"(?:sk-|bearer\s+|token[=:]|[0-9a-f]{40,})", text, re.IGNORECASE):
        raise ValueError("{} contains a possible secret".format(label))
    if re.search(r"\b(?:is|are)\s+not\b|,\s*not\b", lowered):
        raise ValueError("{} uses a prohibited contrast construction".format(label))
    if re.search(r":\s*\n\s*(?:[•*-]|\d+\.)", text):
        raise ValueError("{} uses a prohibited colon-led list".format(label))
    if any(phrase in lowered for phrase in ("exception layer", "where the risk lives")):
        raise ValueError("{} repeats a blocked content shape".format(label))
    return text


def _timestamp(value: object, label: str) -> datetime:
    parsed = parse_timestamp(_text(value, label), label)
    if parsed.tzinfo is None:
        raise ValueError("{} needs an explicit offset".format(label))
    return parsed


def _validate_source(source: object, lane: str, now: datetime) -> dict[str, object]:
    if not isinstance(source, dict):
        raise ValueError("source must be an object")
    _exact_fields(source, _SOURCE_FIELDS, "source")
    source_id = _text(source["sourceId"], "sourceId")
    if source["sourceType"] != "official_release":
        raise ValueError("manual fixture source must be an official release")
    uri = _text(source["uri"], "source URI")
    if not uri.startswith("https://"):
        raise ValueError("source URI must use HTTPS")
    published = _timestamp(source["publishedAt"], "publishedAt")
    retrieved = _timestamp(source["retrievedAt"], "retrievedAt")
    if published > retrieved or retrieved > now:
        raise ValueError("source chronology is invalid")
    maximum_age_days = 5 if lane == "ai_news" else 14
    fresh_until = published + timedelta(days=maximum_age_days)
    if now >= fresh_until:
        raise ValueError("source freshness window has expired")
    excerpts = source["excerpts"]
    if not isinstance(excerpts, list) or not excerpts:
        raise ValueError("source excerpts must be a non-empty list")
    normalized_excerpts = [_text(item, "source excerpt") for item in excerpts]
    unsigned = {
        "sourceId": source_id,
        "sourceType": source["sourceType"],
        "uri": uri,
        "publishedAt": source["publishedAt"],
        "retrievedAt": source["retrievedAt"],
        "publisher": _text(source["publisher"], "publisher"),
        "title": _text(source["title"], "source title"),
        "excerpts": normalized_excerpts,
    }
    return {**unsigned, "sourceSha256": sha256_hex(canonical_bytes(unsigned))}


def _validate_angle(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("earned angle must be an object")
    _exact_fields(value, _ANGLE_FIELDS, "earned angle")
    if value["kind"] != "jt_field_lesson":
        raise ValueError("earned angle must be a JT field lesson")
    path = _safe_path(value["path"], "earned angle path")
    excerpt = _text(value["excerpt"], "earned angle excerpt")
    expected_hash = _hash(value["fileSha256"], "earned angle fileSha256")
    repository = Path(__file__).resolve().parents[2]
    source_path = repository / path
    if source_path.is_symlink() or not source_path.is_file():
        raise ValueError("earned angle path is missing or symlinked")
    source_bytes = source_path.read_bytes()
    if sha256_hex(source_bytes) != expected_hash:
        raise ValueError("earned angle file hash mismatch")
    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("earned angle source must be UTF-8") from error
    if excerpt not in source_text:
        raise ValueError("earned angle excerpt is not exact source text")
    confirmation_path = _safe_path(value["confirmationPath"], "earned angle confirmation path")
    confirmation_excerpt = _text(value["confirmationExcerpt"], "earned angle confirmation excerpt")
    expected_confirmation_hash = _hash(
        value["confirmationFileSha256"], "earned angle confirmation fileSha256"
    )
    confirmation_source = repository / confirmation_path
    if confirmation_source.is_symlink() or not confirmation_source.is_file():
        raise ValueError("earned angle confirmation path is missing or symlinked")
    confirmation_bytes = confirmation_source.read_bytes()
    if sha256_hex(confirmation_bytes) != expected_confirmation_hash:
        raise ValueError("earned angle confirmation file hash mismatch")
    confirmation_text = confirmation_bytes.decode("utf-8")
    if confirmation_excerpt not in confirmation_text:
        raise ValueError("earned angle confirmation excerpt is not exact source text")
    try:
        confirmation_record = json.loads(confirmation_text)
    except json.JSONDecodeError as error:
        raise ValueError("earned angle confirmation must be JSON") from error
    if (
        not isinstance(confirmation_record, dict)
        or confirmation_record.get("schemaVersion") != "linkedin-earned-angle-confirmation.v1"
        or confirmation_record.get("posted") is not True
        or confirmation_record.get("sourceFile") != path
        or confirmation_record.get("sourceFileSha256") != expected_hash
    ):
        raise ValueError("earned angle confirmation must prove the exact posted source")
    return {
        "kind": value["kind"],
        "path": path,
        "excerpt": excerpt,
        "fileSha256": expected_hash,
        "confirmationPath": confirmation_path,
        "confirmationExcerpt": confirmation_excerpt,
        "confirmationFileSha256": expected_confirmation_hash,
    }


def _validate_conflict_checks(value: object, lane: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ValueError("conflict checks must be a list")
    normalized: list[dict[str, str]] = []
    names: set[str] = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("conflict check must be an object")
        _exact_fields(item, _CONFLICT_FIELDS, "conflict check")
        name = _text(item["check"], "conflict check name")
        if name in names:
            raise ValueError("conflict checks must be unique")
        names.add(name)
        if item["status"] != "pass":
            raise ValueError("conflict check {} did not pass".format(name))
        normalized.append(
            {"check": name, "status": "pass", "evidence": _text(item["evidence"], "conflict evidence")}
        )
    if names != _REQUIRED_CONFLICT_CHECKS[lane]:
        raise ValueError("conflict checks are incomplete for {}".format(lane))
    return sorted(normalized, key=lambda item: item["check"])


def _validate_visual(value: object, lane: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("visual must be an object")
    _exact_fields(value, _VISUAL_FIELDS, "visual")
    expected = "teardown-schematic.v1" if lane == "teardown" else "ai-news-source-card.v1"
    if value["template"] != expected:
        if lane == "ai_news":
            raise ValueError("AI news must use the original text-first source-card route")
        raise ValueError("teardown must use the schematic route")
    footer = _public_safe_text(value["footer"], "visual footer")
    if lane == "teardown" and footer != "Proposed system based on public information":
        raise ValueError("teardown must carry the public information label")
    stages = value["stages"]
    if not isinstance(stages, list) or not 4 <= len(stages) <= 5:
        raise ValueError("visual stages must contain four or five items")
    return {
        "template": expected,
        "eyebrow": _public_safe_text(value["eyebrow"], "visual eyebrow"),
        "title": _public_safe_text(value["title"], "visual title"),
        "subtitle": _public_safe_text(value["subtitle"], "visual subtitle"),
        "stages": [_public_safe_text(item, "visual stage") for item in stages],
        "footer": footer,
    }


def _load_font(size: int, *, mono: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        "/System/Library/Fonts/SFNSMono.ttf" if mono else "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    raise RuntimeError("deterministic system font is unavailable")


def _fit_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = "{} {}".format(current, word).strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _render_png(visual: dict[str, object], lane: str) -> bytes:
    image = Image.new("RGB", (1080, 1350), "#09090b")
    draw = ImageDraw.Draw(image)
    white, muted, border = "#fafafa", "#a1a1aa", "#27272a"
    accent = "#14b8a6" if lane == "teardown" else "#6366f1"
    eyebrow_font = _load_font(25, mono=True)
    title_font = _load_font(64)
    subtitle_font = _load_font(31)
    stage_font = _load_font(28)
    number_font = _load_font(24, mono=True)
    small_font = _load_font(26, mono=True)

    draw.rounded_rectangle((58, 58, 1022, 1292), radius=28, fill="#111114", outline=border, width=2)
    eyebrow = str(visual["eyebrow"])
    eyebrow_width = draw.textbbox((0, 0), eyebrow, font=eyebrow_font)[2]
    draw.rounded_rectangle((82, 82, 126 + eyebrow_width, 130), radius=18, fill=accent)
    draw.text((104, 96), eyebrow, font=eyebrow_font, fill="#ffffff")

    y = 190
    title_lines = _fit_lines(draw, str(visual["title"]), title_font, 870)
    if len(title_lines) > 3:
        raise ValueError("visual title overflows its safe area")
    for line in title_lines:
        draw.text((88, y), line, font=title_font, fill=white)
        y += 78
    y += 8
    subtitle_lines = _fit_lines(draw, str(visual["subtitle"]), subtitle_font, 870)
    if len(subtitle_lines) > 3:
        raise ValueError("visual subtitle overflows its safe area")
    for line in subtitle_lines:
        draw.text((88, y), line, font=subtitle_font, fill=muted)
        y += 43

    stages = list(visual["stages"])
    stage_top, stage_bottom = 625, 1055
    gap = 18
    box_width = int((904 - gap * (len(stages) - 1)) / len(stages))
    center_y = int((stage_top + stage_bottom) / 2)
    for index, stage in enumerate(stages):
        left = 88 + index * (box_width + gap)
        right = left + box_width
        fill = "#17201f" if lane == "teardown" else "#18182a"
        if "approval" in stage.lower():
            fill = "#28230f"
        draw.rounded_rectangle((left, stage_top, right, stage_bottom), radius=18, fill=fill, outline=accent, width=2)
        draw.ellipse((left + 18, stage_top + 20, left + 54, stage_top + 56), fill=accent)
        draw.text((left + 36, stage_top + 38), str(index + 1), font=number_font, fill="#ffffff", anchor="mm")
        stage_lines = _fit_lines(draw, str(stage), stage_font, box_width - 34)
        if len(stage_lines) > 5:
            raise ValueError("visual stage text overflows its safe area")
        line_height = 38
        line_y = center_y - int((len(stage_lines) * line_height) / 2)
        if line_y < stage_top + 80 or line_y + len(stage_lines) * line_height > stage_bottom - 24:
            raise ValueError("visual stage text overflows its safe area")
        for line in stage_lines:
            draw.text((left + 17, line_y), line, font=stage_font, fill=white)
            line_y += line_height
        if index < len(stages) - 1:
            arrow_left = right + 3
            arrow_right = right + gap - 3
            draw.line((arrow_left, center_y, arrow_right, center_y), fill=muted, width=3)
            draw.polygon(
                ((arrow_right, center_y), (arrow_right - 9, center_y - 7), (arrow_right - 9, center_y + 7)),
                fill=muted,
            )

    draw.line((88, 1138, 992, 1138), fill=border, width=2)
    footer = str(visual["footer"])
    if draw.textbbox((0, 0), footer, font=small_font)[2] > 904:
        raise ValueError("visual footer overflows its safe area")
    draw.text((88, 1184), footer, font=small_font, fill=muted)
    draw.text((992, 1234), "JT SOMWARU", font=small_font, fill=accent, anchor="ra")
    output = io.BytesIO()
    image.save(output, format="PNG", optimize=False, compress_level=9)
    return output.getvalue()


def _atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(dir=str(path.parent), prefix=".{}-".format(path.name))
    temporary = Path(temporary_name)
    try:
        with open(descriptor, "wb", closefd=True) as handle:
            handle.write(payload)
            handle.flush()
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _result(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("{} must be an object".format(label))
    _exact_fields(value, _RESULT_FIELDS, label)
    if value["status"] != "pass":
        raise ValueError("{} must pass".format(label))
    return {"status": "pass", "details": _text(value["details"], "{}.details".format(label))}


def _validate_qa(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("qa must be an object")
    _exact_fields(value, _QA_FIELDS, "qa")
    normalized: dict[str, object] = {}
    for key in sorted(_QA_FIELDS):
        allowed = {"pass"} if key != "voice" else {"pass", "pending_human_rating"}
        if value[key] not in allowed:
            raise ValueError("qa.{} has not passed".format(key))
        normalized[key] = value[key]
    return normalized


def _normalize_spec(spec: object, now: datetime) -> dict[str, object]:
    if not isinstance(spec, dict):
        raise ValueError("fixture source must be an object")
    _exact_fields(spec, _SPEC_FIELDS, "fixture source")
    if spec["schemaVersion"] != "manual-linkedin-fixture-source.v1":
        raise ValueError("unsupported fixture source schema")
    lane = spec["lane"]
    if lane not in _LANES:
        raise ValueError("unsupported fixture lane")
    packet_id = _slug(spec["packetId"], "packetId")
    revision_family = _slug(spec["revisionFamilyId"], "revisionFamilyId")
    if type(spec["packetVersion"]) is not int or spec["packetVersion"] < 1:
        raise ValueError("packetVersion must be a positive integer")
    created = _timestamp(spec["createdAt"], "createdAt")
    expires = _timestamp(spec["expiresAt"], "expiresAt")
    if created > now or expires <= now:
        raise ValueError("packet timing is invalid")
    post_text = _public_safe_text(spec["postText"], "post")

    raw_sources = spec["sources"]
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ValueError("sources must be a non-empty list")
    sources = [_validate_source(source, lane, now) for source in raw_sources]
    by_id = {str(source["sourceId"]): source for source in sources}
    if len(by_id) != len(sources):
        raise ValueError("source IDs must be unique")
    maximum_age_days = 5 if lane == "ai_news" else 14
    earliest_fresh_until = min(
        _timestamp(source["publishedAt"], "publishedAt") + timedelta(days=maximum_age_days)
        for source in sources
    )
    if expires > earliest_fresh_until:
        raise ValueError("packet expiry exceeds source freshness window")

    raw_claims = spec["claims"]
    if not isinstance(raw_claims, list) or not raw_claims:
        raise ValueError("claims must be a non-empty list")
    claims: list[dict[str, object]] = []
    claim_ids: set[str] = set()
    for raw_claim in raw_claims:
        if not isinstance(raw_claim, dict):
            raise ValueError("claim must be an object")
        _exact_fields(raw_claim, _CLAIM_FIELDS, "claim")
        claim_id = _text(raw_claim["claimId"], "claimId")
        if claim_id in claim_ids:
            raise ValueError("claim IDs must be unique")
        claim_ids.add(claim_id)
        source_id = _text(raw_claim["sourceId"], "claim sourceId")
        source = by_id.get(source_id)
        index = raw_claim["excerptIndex"]
        if source is None or type(index) is not int or index < 0 or index >= len(source["excerpts"]):
            raise ValueError("claim evidence binding is invalid")
        if raw_claim["attributionType"] not in _ATTRIBUTIONS:
            raise ValueError("claim attribution is invalid")
        excerpt = source["excerpts"][index]
        claim_text = _text(raw_claim["text"], "claim text")
        if claim_text not in str(excerpt):
            raise ValueError("claim text must be an exact span of its source excerpt")
        if post_text.count(claim_text) != 1:
            raise ValueError("claim text must be an exact span of postText")
        post_start = post_text.index(claim_text)
        claims.append(
            {
                "claimId": claim_id,
                "text": claim_text,
                "attributionType": raw_claim["attributionType"],
                "sourceId": source_id,
                "excerptIndex": index,
                "excerptSha256": sha256_hex(str(excerpt).encode("utf-8")),
                "postStart": post_start,
                "postEnd": post_start + len(claim_text),
            }
        )

    return {
        "packetId": packet_id,
        "revisionFamilyId": revision_family,
        "packetVersion": spec["packetVersion"],
        "lane": lane,
        "createdAt": spec["createdAt"],
        "expiresAt": spec["expiresAt"],
        "targetReader": _text(spec["targetReader"], "targetReader"),
        "commercialObjective": _text(spec["commercialObjective"], "commercialObjective"),
        "whyThisWon": _text(spec["whyThisWon"], "whyThisWon"),
        "postText": post_text,
        "sourceBindings": sources,
        "claimEvidence": claims,
        "earnedAngle": _validate_angle(spec["earnedAngle"]),
        "conflictChecks": _validate_conflict_checks(spec["conflictChecks"], lane),
        "visualRoute": _validate_visual(spec["visual"], lane),
        "altText": _public_safe_text(spec["altText"], "altText"),
        "cropGuidance": _text(spec["cropGuidance"], "cropGuidance"),
        "privacyResult": _result(spec["privacyResult"], "privacyResult"),
        "rightsResult": _result(spec["rightsResult"], "rightsResult"),
        "qa": _validate_qa(spec["qa"]),
    }


def _draft_binding(packet: dict[str, object]) -> dict[str, object]:
    return {
        "packetId": packet["packetId"],
        "packetVersion": packet["packetVersion"],
        "revisionFamilyId": packet["revisionFamilyId"],
        "lane": packet["lane"],
        "state": packet["state"],
        "createdAt": packet["createdAt"],
        "expiresAt": packet["expiresAt"],
        "targetReader": packet["targetReader"],
        "commercialObjective": packet["commercialObjective"],
        "whyThisWon": packet["whyThisWon"],
        "postText": packet["postText"],
        "sourceBindings": packet["sourceBindings"],
        "claimEvidence": packet["claimEvidence"],
        "earnedAngle": packet["earnedAngle"],
        "conflictChecks": packet["conflictChecks"],
        "visualRoute": packet["visualRoute"],
        "altText": packet["altText"],
        "cropGuidance": packet["cropGuidance"],
        "privacyResult": packet["privacyResult"],
        "rightsResult": packet["rightsResult"],
        "qa": packet["qa"],
        "decisionOptions": packet["decisionOptions"],
    }


def _payload_binding(packet: dict[str, object]) -> dict[str, object]:
    return {
        "draftSha256": packet["draftSha256"],
        "imageAsset": packet["imageAsset"],
    }


def build_manual_fixture(spec: object, artifact_root: Path, *, now: datetime) -> dict[str, object]:
    """Render one local manual fixture and return its exact packet."""

    normalized = _normalize_spec(spec, now)
    packet_id = str(normalized["packetId"])
    directory = Path(artifact_root) / "manual-fixtures" / packet_id
    asset_path = directory / "image.v1.png"
    packet_path = directory / "packet.v1.json"
    image_bytes = _render_png(dict(normalized["visualRoute"]), str(normalized["lane"]))
    relative_asset = asset_path.relative_to(Path(artifact_root)).as_posix()

    packet: dict[str, object] = {
        "schemaVersion": "content-packet.v1",
        **normalized,
        "state": "qa_passed",
        "imageAsset": {
            "path": relative_asset,
            "mimeType": "image/png",
            "width": 1080,
            "height": 1350,
            "byteLength": len(image_bytes),
            "sha256": sha256_hex(image_bytes),
        },
        "decisionOptions": ["approve", "reject", "skip"],
    }
    packet["draftSha256"] = sha256_hex(canonical_bytes(_draft_binding(packet)))
    packet["payloadSha256"] = sha256_hex(canonical_bytes(_payload_binding(packet)))

    if packet_path.exists():
        if packet_path.read_bytes() != canonical_bytes(packet):
            raise ValueError("conflicting replay for existing packet ID")
        if not asset_path.exists() or asset_path.read_bytes() != image_bytes:
            raise ValueError("existing replay asset does not match packet")
        return validate_manual_fixture(packet, Path(artifact_root), now=now)

    directory.mkdir(parents=True, exist_ok=True)
    _atomic_bytes(asset_path, image_bytes)
    write_json_atomic(packet_path, packet)
    return validate_manual_fixture(packet, Path(artifact_root), now=now)


def validate_manual_fixture(packet: object, artifact_root: Path, *, now: datetime) -> dict[str, object]:
    """Fail closed unless a packet and its exact image satisfy the manual fixture contract."""

    if not isinstance(packet, dict):
        raise ValueError("packet must be an object")
    _exact_fields(packet, _PACKET_FIELDS, "packet")
    if packet["schemaVersion"] != "content-packet.v1" or packet["state"] != "qa_passed":
        raise ValueError("packet lifecycle state is invalid")
    packet_id = _slug(packet["packetId"], "packetId")
    if packet["lane"] not in _LANES:
        raise ValueError("packet lane is invalid")
    if packet["decisionOptions"] != ["approve", "reject", "skip"]:
        raise ValueError("decision options are invalid")

    raw_sources = []
    for source in packet["sourceBindings"]:
        if not isinstance(source, dict):
            raise ValueError("source binding must be an object")
        raw_source = dict(source)
        recorded_source_hash = raw_source.pop("sourceSha256", None)
        normalized_source = _validate_source(raw_source, str(packet["lane"]), now)
        if recorded_source_hash != normalized_source["sourceSha256"]:
            raise ValueError("source binding hash mismatch")
        raw_sources.append(raw_source)
    raw_claims = []
    for claim in packet["claimEvidence"]:
        if not isinstance(claim, dict):
            raise ValueError("claim evidence must be an object")
        raw_claim = dict(claim)
        recorded_excerpt_hash = raw_claim.pop("excerptSha256", None)
        raw_claim.pop("postStart", None)
        raw_claim.pop("postEnd", None)
        source = next((item for item in raw_sources if item["sourceId"] == raw_claim.get("sourceId")), None)
        index = raw_claim.get("excerptIndex")
        if source is None or type(index) is not int or not 0 <= index < len(source["excerpts"]):
            raise ValueError("claim evidence binding is invalid")
        if recorded_excerpt_hash != sha256_hex(str(source["excerpts"][index]).encode("utf-8")):
            raise ValueError("claim excerpt hash mismatch")
        raw_claims.append(raw_claim)

    normalized = _normalize_spec(
        {
            "schemaVersion": "manual-linkedin-fixture-source.v1",
            "packetId": packet_id,
            "revisionFamilyId": packet["revisionFamilyId"],
            "packetVersion": packet["packetVersion"],
            "lane": packet["lane"],
            "createdAt": packet["createdAt"],
            "expiresAt": packet["expiresAt"],
            "targetReader": packet["targetReader"],
            "commercialObjective": packet["commercialObjective"],
            "whyThisWon": packet["whyThisWon"],
            "postText": packet["postText"],
            "sources": raw_sources,
            "claims": raw_claims,
            "earnedAngle": packet["earnedAngle"],
            "conflictChecks": packet["conflictChecks"],
            "visual": packet["visualRoute"],
            "altText": packet["altText"],
            "cropGuidance": packet["cropGuidance"],
            "privacyResult": packet["privacyResult"],
            "rightsResult": packet["rightsResult"],
            "qa": packet["qa"],
        },
        now,
    )
    for key, value in normalized.items():
        if packet.get(key) != value:
            raise ValueError("packet {} does not match normalized contract".format(key))
    if packet["draftSha256"] != sha256_hex(canonical_bytes(_draft_binding(packet))):
        raise ValueError("draft hash mismatch")
    if packet["payloadSha256"] != sha256_hex(canonical_bytes(_payload_binding(packet))):
        raise ValueError("payload hash mismatch")

    asset = packet["imageAsset"]
    if not isinstance(asset, dict):
        raise ValueError("image asset must be an object")
    _exact_fields(asset, _ASSET_FIELDS, "image asset")
    expected_asset_path = "manual-fixtures/{}/image.v1.png".format(packet_id)
    if asset["path"] != expected_asset_path:
        raise ValueError("image asset path is not packet-versioned")
    asset_path = Path(artifact_root) / _safe_path(asset["path"], "image asset path")
    if asset_path.is_symlink():
        raise ValueError("image asset must not be a symlink")
    if not asset_path.is_file():
        raise ValueError("image asset is missing")
    payload = asset_path.read_bytes()
    if asset["mimeType"] != "image/png" or asset["byteLength"] != len(payload):
        raise ValueError("image asset metadata mismatch")
    if _hash(asset["sha256"], "image asset SHA-256") != sha256_hex(payload):
        raise ValueError("image asset hash mismatch")
    with Image.open(io.BytesIO(payload)) as image:
        if image.format != "PNG" or image.size != (1080, 1350):
            raise ValueError("image asset dimensions or type are invalid")
        if asset["width"] != 1080 or asset["height"] != 1350:
            raise ValueError("image asset recorded dimensions are invalid")
    return packet
