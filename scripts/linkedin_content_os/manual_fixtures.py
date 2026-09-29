"""Build and validate immutable manual LinkedIn fixture packets."""

from __future__ import annotations

import io
import re
import tempfile
from datetime import datetime
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
_ANGLE_FIELDS = {"kind", "path", "excerpt", "fileSha256"}
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
_INTERNAL_TERMS = (
    "mission control",
    "openclaw",
    "content os",
    "growth os",
    "decagon",
    "job search",
)


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
    if (now - published).total_seconds() > maximum_age_days * 86400:
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
    return {
        "kind": value["kind"],
        "path": _safe_path(value["path"], "earned angle path"),
        "excerpt": _text(value["excerpt"], "earned angle excerpt"),
        "fileSha256": _hash(value["fileSha256"], "earned angle fileSha256"),
    }


def _validate_visual(value: object, lane: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("visual must be an object")
    _exact_fields(value, _VISUAL_FIELDS, "visual")
    expected = "teardown-schematic.v1" if lane == "teardown" else "ai-news-source-card.v1"
    if value["template"] != expected:
        if lane == "ai_news":
            raise ValueError("AI news must use the original text-first source-card route")
        raise ValueError("teardown must use the schematic route")
    footer = _text(value["footer"], "visual footer")
    if lane == "teardown" and footer != "Proposed system based on public information":
        raise ValueError("teardown must carry the public information label")
    stages = value["stages"]
    if not isinstance(stages, list) or not 4 <= len(stages) <= 5:
        raise ValueError("visual stages must contain four or five items")
    return {
        "template": expected,
        "eyebrow": _text(value["eyebrow"], "visual eyebrow"),
        "title": _text(value["title"], "visual title"),
        "subtitle": _text(value["subtitle"], "visual subtitle"),
        "stages": [_text(item, "visual stage") for item in stages],
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
    return ImageFont.load_default()


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
    stage_font = _load_font(26)
    small_font = _load_font(21, mono=True)

    draw.rounded_rectangle((58, 58, 1022, 1292), radius=28, fill="#111114", outline=border, width=2)
    eyebrow = str(visual["eyebrow"])
    eyebrow_width = draw.textbbox((0, 0), eyebrow, font=eyebrow_font)[2]
    draw.rounded_rectangle((82, 82, 126 + eyebrow_width, 130), radius=18, fill=accent)
    draw.text((104, 96), eyebrow, font=eyebrow_font, fill="#ffffff")

    y = 190
    for line in _fit_lines(draw, str(visual["title"]), title_font, 870):
        draw.text((88, y), line, font=title_font, fill=white)
        y += 78
    y += 8
    for line in _fit_lines(draw, str(visual["subtitle"]), subtitle_font, 870):
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
        draw.text((left + 29, stage_top + 27), str(index + 1), font=small_font, fill="#ffffff", anchor="mm")
        line_y = center_y - 45
        for line in _fit_lines(draw, str(stage), stage_font, box_width - 34):
            draw.text((left + 17, line_y), line, font=stage_font, fill=white)
            line_y += 35
        if index < len(stages) - 1:
            arrow_left = right + 3
            arrow_right = right + gap - 3
            draw.line((arrow_left, center_y, arrow_right, center_y), fill=muted, width=3)
            draw.polygon(
                ((arrow_right, center_y), (arrow_right - 9, center_y - 7), (arrow_right - 9, center_y + 7)),
                fill=muted,
            )

    draw.line((88, 1138, 992, 1138), fill=border, width=2)
    draw.text((88, 1184), str(visual["footer"]), font=small_font, fill=muted)
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
    packet_id = _text(spec["packetId"], "packetId")
    revision_family = _text(spec["revisionFamilyId"], "revisionFamilyId")
    if type(spec["packetVersion"]) is not int or spec["packetVersion"] < 1:
        raise ValueError("packetVersion must be a positive integer")
    created = _timestamp(spec["createdAt"], "createdAt")
    expires = _timestamp(spec["expiresAt"], "expiresAt")
    if created > now or expires <= now:
        raise ValueError("packet timing is invalid")
    post_text = _text(spec["postText"], "postText")
    lowered = post_text.lower()
    if any(term in lowered for term in _INTERNAL_TERMS):
        raise ValueError("post exposes prohibited internal machinery")
    if re.search(r"(?:sk-|bearer\s+|token[=:]|[0-9a-f]{40,})", post_text, re.IGNORECASE):
        raise ValueError("post contains a possible secret")

    raw_sources = spec["sources"]
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ValueError("sources must be a non-empty list")
    sources = [_validate_source(source, lane, now) for source in raw_sources]
    by_id = {str(source["sourceId"]): source for source in sources}
    if len(by_id) != len(sources):
        raise ValueError("source IDs must be unique")

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
        claims.append(
            {
                "claimId": claim_id,
                "text": _text(raw_claim["text"], "claim text"),
                "attributionType": raw_claim["attributionType"],
                "sourceId": source_id,
                "excerptIndex": index,
                "excerptSha256": sha256_hex(str(excerpt).encode("utf-8")),
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
        "visualRoute": _validate_visual(spec["visual"], lane),
        "altText": _text(spec["altText"], "altText"),
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
        "postText": packet["postText"],
        "sourceBindings": packet["sourceBindings"],
        "claimEvidence": packet["claimEvidence"],
        "earnedAngle": packet["earnedAngle"],
        "visualRoute": packet["visualRoute"],
    }


def _payload_binding(packet: dict[str, object]) -> dict[str, object]:
    return {
        "draftSha256": packet["draftSha256"],
        "imageAsset": packet["imageAsset"],
        "altText": packet["altText"],
        "cropGuidance": packet["cropGuidance"],
        "privacyResult": packet["privacyResult"],
        "rightsResult": packet["rightsResult"],
        "qa": packet["qa"],
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
        "decisionOptions": ["approve", "edit", "reject", "hold"],
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
    if packet["lane"] not in _LANES:
        raise ValueError("packet lane is invalid")
    if packet["decisionOptions"] != ["approve", "edit", "reject", "hold"]:
        raise ValueError("decision options are invalid")
    if _timestamp(packet["expiresAt"], "expiresAt") <= now:
        raise ValueError("packet has expired")
    if packet["draftSha256"] != sha256_hex(canonical_bytes(_draft_binding(packet))):
        raise ValueError("draft hash mismatch")
    if packet["payloadSha256"] != sha256_hex(canonical_bytes(_payload_binding(packet))):
        raise ValueError("payload hash mismatch")

    asset = packet["imageAsset"]
    if not isinstance(asset, dict):
        raise ValueError("image asset must be an object")
    _exact_fields(asset, _ASSET_FIELDS, "image asset")
    asset_path = Path(artifact_root) / _safe_path(asset["path"], "image asset path")
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
