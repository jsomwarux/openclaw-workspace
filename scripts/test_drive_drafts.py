#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import drive_drafts


class _Request:
    def __init__(self, result=None, hook=None):
        self.result = result or {}
        self.hook = hook

    def execute(self):
        if self.hook:
            self.hook()
        return self.result


class _Files:
    def __init__(self, existing=None):
        self.existing = existing
        self.created = []
        self.updated = []

    def list(self, **_kwargs):
        return _Request({"files": [self.existing] if self.existing else []})

    def create(self, **kwargs):
        self.created.append(kwargs)
        return _Request({"id": "new-doc"})

    def update(self, **kwargs):
        self.updated.append(kwargs)
        return _Request({"id": kwargs["fileId"]})


class _Drive:
    def __init__(self, existing=None):
        self._files = _Files(existing)
        self._http = type("Http", (), {"credentials": object()})()

    def files(self):
        return self._files


class _Documents:
    def __init__(self):
        self.batch_updates = []

    def get(self, **_kwargs):
        return _Request({"body": {"content": [{"endIndex": 1}, {"endIndex": 14}]}})

    def batchUpdate(self, **kwargs):
        self.batch_updates.append(kwargs)
        return _Request({})


class _Docs:
    def __init__(self, documents):
        self._documents = documents

    def documents(self):
        return self._documents


class DriveDraftsTests(unittest.TestCase):
    def test_create_doc_replaces_existing_google_doc_body(self):
        drive = _Drive(existing={"id": "existing-doc", "name": "Draft"})
        documents = _Documents()

        with patch.object(drive_drafts, "build", return_value=_Docs(documents)):
            url = drive_drafts.create_doc(drive, "Draft", "fresh body", "folder")

        self.assertEqual(url, "https://docs.google.com/document/d/existing-doc/edit")
        self.assertEqual(drive.files().created, [])
        requests = documents.batch_updates[0]["body"]["requests"]
        self.assertEqual(requests[0]["deleteContentRange"]["range"], {"startIndex": 1, "endIndex": 13})
        self.assertEqual(requests[1]["insertText"]["text"], "fresh body")

    def test_create_doc_from_docx_updates_existing_google_doc(self):
        drive = _Drive(existing={"id": "existing-doc", "name": "Resume"})

        url = drive_drafts.create_doc_from_docx(drive, "Resume", b"docx bytes", "folder")

        self.assertEqual(url, "https://docs.google.com/document/d/existing-doc/edit")
        self.assertEqual(drive.files().created, [])
        self.assertEqual(drive.files().updated[0]["fileId"], "existing-doc")
        self.assertEqual(
            drive.files().updated[0]["body"],
            {"mimeType": "application/vnd.google-apps.document"},
        )


if __name__ == "__main__":
    unittest.main()
