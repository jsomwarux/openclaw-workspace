# Resume & Cover Letter Drive Upload Rules
> Read this file whenever building a resume or cover letter for a job application.

## Resume & Cover Letter Drive Upload Rule
Whenever a resume or cover letter is generated (for any job application):
1. **Write the resume to `memory/drafts/[company-slug]-resume.md` and cover letter to `memory/drafts/[company-slug]-cover-letter.md`** — these are the source of truth.
2. **Build .docx by passing the markdown files directly to the script** (NEVER rely on hardcoded content):
   ```
   mkdir -p /tmp/resume-out && cd ~/.openclaw/workspace && python3 scripts/build_resume_docx.py \
     --type both --output-dir /tmp/resume-out \
     --resume-md memory/drafts/[company-slug]-resume.md \
     --cover-letter-md memory/drafts/[company-slug]-cover-letter.md
   ```
3. Upload the .docx to Google Drive: `python3 scripts/drive_drafts.py --title "[Company] — Resume" --path "Job Applications/Resumes" --file /tmp/resume-out/jt-somwaru-resume.docx`
4. Include the Drive link in the reply to JT.
5. Both resume AND cover letter must be uploaded if both are generated.
6. **Never skip `--resume-md` and `--cover-letter-md`.** Calling the script without these flags = hardcoded fallback content = wrong version goes to Drive. Always pass the md files.
