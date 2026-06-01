#!/usr/bin/env python3
import unittest
from pathlib import Path

from ai_ops_teardown_drive_sync import build_upload_plan, current_bundle_from_calendar


class AiOpsTeardownDriveSyncTests(unittest.TestCase):
    def test_current_bundle_from_calendar_extracts_date_title_and_slug(self):
        text = """# AI Ops Teardowns — Delivery Calendar

## Current Bundle
### 2026-05-31 — Property Lease Renewal Deadline Queue
Status: ready to review/post.
"""
        bundle = current_bundle_from_calendar(text)

        self.assertEqual(bundle.date, "2026-05-31")
        self.assertEqual(bundle.title, "Property Lease Renewal Deadline Queue")
        self.assertEqual(bundle.slug, "property-lease-renewal-deadline-queue")

    def test_build_upload_plan_uses_stable_organized_drive_paths(self):
        workspace = Path("/workspace")
        plan = build_upload_plan(
            workspace=workspace,
            date="2026-05-31",
            slug="property-lease-renewal-deadline-queue",
            title="Property Lease Renewal Deadline Queue",
        )

        self.assertEqual(
            [item.drive_path for item in plan],
            [
                "Consulting/AI Ops Teardowns/2026-05-31/Teardowns",
                "Content/AI Ops Teardowns/2026-05-31/Drafts",
            ],
        )
        self.assertEqual(
            [item.title for item in plan],
            [
                "AI Ops Teardown — Property Lease Renewal Deadline Queue — 2026-05-31",
                "AI Ops Teardown Draft — Property Lease Renewal Deadline Queue — 2026-05-31",
            ],
        )
        self.assertEqual(
            [item.file_path for item in plan],
            [
                workspace / "memory/consulting/ai-ops-teardowns/2026-05-31-property-lease-renewal-deadline-queue.md",
                workspace / "memory/content/bank/2026-05-31/ai-ops-teardown-property-lease-renewal-deadline-queue.md",
            ],
        )


if __name__ == "__main__":
    unittest.main()
