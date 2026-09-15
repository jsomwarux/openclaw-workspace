import tempfile
import unittest
from pathlib import Path
import sys

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_resume_docx


class ResumeHeaderTests(unittest.TestCase):
    def test_generated_resume_preserves_target_title_from_source_header(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "resume.md"
            output = temp / "resume.docx"
            source.write_text(
                "# JT SOMWARU\n"
                "AI Program Manager | AI Implementation Specialist | New York, NY | "
                "jtsomwaru@gmail.com | linkedin.com/in/jon-trevor-somwaru | jtsomwaru.com\n\n"
                "## PROFESSIONAL SUMMARY\nSummary.\n\n"
                "## EXPERIENCE\n\n"
                "### Business Systems Analyst\n"
                "**Spectrum Enterprise**, New York, NY, 2019-2025\n\n"
                "- Coordinated systems implementations.\n\n"
                "## EDUCATION\nBS | Ithaca College | 2018\n"
            )

            build_resume_docx.build_resume(str(output), resume_md=str(source))

            rendered = "\n".join(p.text for p in Document(output).paragraphs)
            self.assertIn("AI Program Manager | AI Implementation Specialist", rendered)


if __name__ == "__main__":
    unittest.main()
