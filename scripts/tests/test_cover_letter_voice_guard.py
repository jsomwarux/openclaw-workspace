import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "build_resume_docx.py"
SPEC = importlib.util.spec_from_file_location("build_resume_docx", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CoverLetterVoiceGuardTests(unittest.TestCase):
    def validate(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
            handle.write(text)
            path = handle.name
        try:
            MODULE.validate_applicant_material_content(path, "Cover letter")
        finally:
            Path(path).unlink()

    def test_rejects_canned_hard_part_contrast(self):
        with self.assertRaisesRegex(ValueError, "canned or clipped"):
            self.validate("The hard part is not building a prototype. It is adoption.")

    def test_rejects_clipped_walkthrough_closes(self):
        for close in (
            "Happy to walk through the project on a call.",
            "I can walk through how I would improve the workflow.",
        ):
            with self.subTest(close=close):
                with self.assertRaisesRegex(ValueError, "canned or clipped"):
                    self.validate(close)

    def test_accepts_warm_formal_close(self):
        self.validate(
            "I would relish the opportunity to walk through how I would move "
            "one workflow from discovery to a measurable solution."
        )


if __name__ == "__main__":
    unittest.main()
