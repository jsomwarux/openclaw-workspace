#!/usr/bin/env python3
"""
build_resume_docx.py — Generate properly formatted .docx resume and cover letter for JT.

Design spec:
  - Font: Calibri throughout
  - Name: 22pt bold, navy (#1B365D), centered
  - Contact line: 10pt dark gray (#555555), centered
  - Section headings: 12pt bold ALL CAPS navy, letter spacing, thin navy rule below
  - Job title: 11pt bold black, left-aligned
  - Company/dates: 10.5pt dark gray, right-aligned on same line
  - Bullets: 10.5pt black, 0.25" indent
  - Body text: 10.5pt black
  - Margins: 0.75" all sides
  - Colors: Navy #1B365D, Near-black #1A1A1A, Dark gray #555555
"""

import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ── Color constants ────────────────────────────────────────────────────────────
NAVY     = RGBColor(0x1B, 0x36, 0x5D)
BLACK    = RGBColor(0x1A, 0x1A, 0x1A)
GRAY     = RGBColor(0x55, 0x55, 0x55)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
LT_GRAY  = RGBColor(0xF5, 0xF5, 0xF5)
BDR_GRAY = RGBColor(0xDD, 0xDD, 0xDD)


def set_run_color(run, color):
    run.font.color.rgb = color


def rgb_hex(color):
    """Convert RGBColor to hex string."""
    return f'{int(color[0]):02X}{int(color[1]):02X}{int(color[2]):02X}'

# Redefine colors as tuples for hex conversion
NAVY_HEX  = '1B365D'
BLACK_HEX = '1A1A1A'
GRAY_HEX  = '555555'
WHITE_HEX = 'FFFFFF'
LTGRAY_HEX = 'F5F5F5'

def add_horizontal_rule(para, color_hex=NAVY_HEX, width_pt=0.75):
    """Add a thin colored bottom border to a paragraph (acts as a divider rule)."""
    pPr = para._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(int(width_pt * 8)))  # sz in eighths of a point
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), color_hex)
    pBdr.append(bottom)
    pPr.append(pBdr)


def set_para_spacing(para, before_pt=0, after_pt=0, line_spacing=None):
    pPr = para._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(before_pt * 20)))
    spacing.set(qn('w:after'), str(int(after_pt * 20)))
    if line_spacing:
        spacing.set(qn('w:line'), str(int(line_spacing * 240)))
        spacing.set(qn('w:lineRule'), 'auto')
    pPr.append(spacing)


def set_tab_stop(para, position_inches, alignment='right'):
    """Add a right tab stop for right-aligned dates on same line as left text."""
    pPr = para._p.get_or_add_pPr()
    tabs = OxmlElement('w:tabs')
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), alignment)
    tab.set(qn('w:pos'), str(int(position_inches * 1440)))  # twips
    tabs.append(tab)
    pPr.append(tabs)


def set_indent(para, left_inches=0, hanging_inches=0):
    pPr = para._p.get_or_add_pPr()
    ind = OxmlElement('w:ind')
    ind.set(qn('w:left'), str(int(left_inches * 1440)))
    if hanging_inches:
        ind.set(qn('w:hanging'), str(int(hanging_inches * 1440)))
    pPr.append(ind)


def add_section_heading(doc, text):
    """Section heading: 12pt bold ALL CAPS navy + thin navy rule below."""
    para = doc.add_paragraph()
    set_para_spacing(para, before_pt=10, after_pt=3)
    run = para.add_run(text.upper())
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = NAVY
    # Letter spacing via rPr/w:spacing
    rPr = run._r.get_or_add_rPr()
    spacing_el = OxmlElement('w:spacing')
    spacing_el.set(qn('w:val'), '20')  # 1pt = 20 twips
    rPr.append(spacing_el)
    add_horizontal_rule(para)
    return para


def add_job_header(doc, title, location, company, dates, content_width=7.0):
    """Job title + location on line 1, company + dates on line 2."""
    # Line 1: Title (bold black left) + Location (gray right)
    p1 = doc.add_paragraph()
    set_para_spacing(p1, before_pt=8, after_pt=1)
    set_tab_stop(p1, content_width)
    r1 = p1.add_run(title)
    r1.font.name = 'Calibri'
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = BLACK
    if location:
        tab_run = p1.add_run('\t')
        loc_run = p1.add_run(location)
        loc_run.font.name = 'Calibri'
        loc_run.font.size = Pt(10.5)
        loc_run.font.color.rgb = GRAY

    # Line 2: Company (gray left) + Dates (gray right)
    p2 = doc.add_paragraph()
    set_para_spacing(p2, before_pt=0, after_pt=1)
    set_tab_stop(p2, content_width)
    comp_run = p2.add_run(company)
    comp_run.font.name = 'Calibri'
    comp_run.font.size = Pt(10.5)
    comp_run.font.color.rgb = GRAY
    if dates:
        tab_run = p2.add_run('\t')
        dates_run = p2.add_run(dates)
        dates_run.font.name = 'Calibri'
        dates_run.font.size = Pt(10.5)
        dates_run.font.color.rgb = GRAY


def add_bullet(doc, text):
    """Standard bullet point."""
    para = doc.add_paragraph(style='List Bullet')
    set_para_spacing(para, before_pt=0, after_pt=2)
    # Clear default bullet formatting and apply ours
    para.clear()
    # Use actual bullet character
    run = para.add_run('• ' + text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.font.color.rgb = BLACK
    # Remove list style to use our custom bullet
    para.style = doc.styles['Normal']
    set_indent(para, left_inches=0.25)
    set_para_spacing(para, before_pt=0, after_pt=2)
    return para


def add_skills_line(doc, category, skills_text):
    """Skills: 'Category: skill1, skill2' with bold category."""
    para = doc.add_paragraph()
    set_para_spacing(para, before_pt=0, after_pt=3)
    cat_run = para.add_run(category + ': ')
    cat_run.font.name = 'Calibri'
    cat_run.font.size = Pt(10.5)
    cat_run.font.bold = True
    cat_run.font.color.rgb = BLACK
    skills_run = para.add_run(skills_text)
    skills_run.font.name = 'Calibri'
    skills_run.font.size = Pt(10.5)
    skills_run.font.bold = False
    skills_run.font.color.rgb = BLACK
    return para


def set_cell_bg(cell, color_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)


def add_builds_table(doc, builds):
    """
    DEPRECATED — DO NOT USE. ATS systems cannot parse tables and will drop all content.
    Selected Builds must use inline text format (add_builds_inline). This function is
    kept only as a reference for the visual spec; it is never called.
    builds: list of (project, description, status)
    """
    raise RuntimeError("add_builds_table is deprecated — use inline text format for ATS compatibility.")
    table = doc.add_table(rows=1 + len(builds), cols=3)
    table.style = 'Table Grid'

    # Remove all borders and set custom ones
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBdr = OxmlElement('w:tcBdr')
            for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                bdr = OxmlElement(f'w:{side}')
                bdr.set(qn('w:val'), 'nil')
                tcBdr.append(bdr)
            tcPr.append(tcBdr)

    # Column widths (approx): 1.8" | 4.0" | 1.2"
    col_widths = [Inches(1.8), Inches(4.0), Inches(1.2)]
    for i, col in enumerate(table.columns):
        for cell in col.cells:
            cell.width = col_widths[i]

    # Header row
    header_row = table.rows[0]
    header_data = ['Project', 'Description', 'Status']
    for i, cell in enumerate(header_row.cells):
        set_cell_bg(cell, '1B365D')
        para = cell.paragraphs[0]
        para.clear()
        set_para_spacing(para, before_pt=4, after_pt=4)
        run = para.add_run(header_data[i])
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = WHITE

    # Data rows
    for row_idx, (project, description, status) in enumerate(builds):
        row = table.rows[row_idx + 1]
        bg = 'F5F5F5' if row_idx % 2 == 0 else 'FFFFFF'
        data = [project, description, status]
        for i, cell in enumerate(row.cells):
            set_cell_bg(cell, bg)
            para = cell.paragraphs[0]
            para.clear()
            set_para_spacing(para, before_pt=4, after_pt=4)
            run = para.add_run(data[i])
            run.font.name = 'Calibri'
            run.font.size = Pt(10)
            run.font.color.rgb = BLACK


def build_resume(output_path):
    doc = Document()

    # ── Page setup ────────────────────────────────────────────────────────────
    section = doc.sections[0]
    section.page_width  = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin   = Inches(0.75)
    section.right_margin  = Inches(0.75)
    section.top_margin    = Inches(0.75)
    section.bottom_margin = Inches(0.75)

    content_width = 7.0  # 8.5 - 0.75 - 0.75

    # ── Default paragraph style ───────────────────────────────────────────────
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(10.5)
    style.font.color.rgb = BLACK

    # ── HEADER ───────────────────────────────────────────────────────────────
    # Name
    name_para = doc.add_paragraph()
    name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_para_spacing(name_para, before_pt=0, after_pt=4)
    name_run = name_para.add_run('Jon Trevor Somwaru')
    name_run.font.name = 'Calibri'
    name_run.font.size = Pt(22)
    name_run.font.bold = True
    name_run.font.color.rgb = NAVY

    # Contact line
    contact_para = doc.add_paragraph()
    contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_para_spacing(contact_para, before_pt=0, after_pt=6)
    contact_run = contact_para.add_run(
        'New York City Metro · jtsomwaru@gmail.com · '
        'linkedin.com/in/jon-trevor-somwaru · jtsomwaru.com'
    )
    contact_run.font.name = 'Calibri'
    contact_run.font.size = Pt(10)
    contact_run.font.color.rgb = GRAY
    add_horizontal_rule(contact_para)

    # ── SUMMARY ──────────────────────────────────────────────────────────────
    add_section_heading(doc, 'Summary')
    summary_para = doc.add_paragraph()
    set_para_spacing(summary_para, before_pt=4, after_pt=6, line_spacing=1.15)
    summary_run = summary_para.add_run(
        'AI adoption and automation specialist with 6 years of enterprise cross-functional delivery '
        '(Charter/Spectrum Enterprise) and an active consulting practice deploying AI systems for real clients. '
        'Specializes in bridging the gap between AI capability and organizational adoption — running production '
        'AI infrastructure, building repeatable automation frameworks, and translating technical systems into '
        'measurable business outcomes. Comfortable working with C-suite executives and technical builders in '
        'the same engagement.'
    )
    summary_run.font.name = 'Calibri'
    summary_run.font.size = Pt(10.5)
    summary_run.font.color.rgb = BLACK

    # ── EXPERIENCE ────────────────────────────────────────────────────────────
    add_section_heading(doc, 'Experience')

    add_job_header(doc,
        title='AI Automation Consultant',
        location='New York City',
        company='JT Somwaru Consulting',
        dates='2025–Present',
        content_width=content_width
    )
    bullets_consulting = [
        'Designed and deployed a multi-agent AI operations infrastructure running 35 autonomous jobs — prospect research, outreach pipelines, content generation, market intelligence, and cost monitoring — entirely without manual input; built monitoring, watchdog processes, model routing, and cost controls from scratch.',
        'Built AgentGuard, a confidence-gated AI governance layer for HR/compliance decisions — confidence ≥70% auto-routes, <70% triggers human review queue with full audit trail; live at agentguard-delta.vercel.app.',
        'Delivered a construction project tracking dashboard for NYC-based client ($1,500) — replaced manual WhatsApp update chains with real-time field reporting system; client immediately commissioned two follow-on projects ($1,000 StreetEasy scraper, $2,500 co-living dashboard scoped).',
        'Built PM Maintenance Triage n8n workflow: multi-tier complaint classification (routine / urgent / emergency), automated vendor dispatch, tenant confirmation, and Google Sheets audit log; deployed for NYC property management clients.',
        'Developed the ConversationFirst framework — a 25-point Agentforce UX methodology for conversation design, persona cards, and flow architecture — adopted as a repeatable implementation standard across insurance and PM deployments.',
        'Built and deployed Agentforce agents for insurance claims intake routing, PM tenant service, and employee self-service — sandbox-to-production across Salesforce orgs.',
        'Shipped Vista (live on Apple App Store) and Nash Satoshi (4-LLM ensemble crypto rankings) — proof of ability to take products from concept to production deployment.',
    ]
    for b in bullets_consulting:
        add_bullet(doc, b)

    add_job_header(doc,
        title='Business Systems Analyst',
        location='New York City',
        company='Charter Communications / Spectrum Enterprise',
        dates='2019–2025',
        content_width=content_width
    )
    bullets_charter = [
        'Managed configuration and cross-team adoption of enterprise product catalog systems across a $1B+ service portfolio — coordinating between Sales, Product, Engineering, and Operations to ensure consistent implementation.',
        'Led system implementation projects requiring alignment across 8+ internal teams, translating technical constraints into operational workflows non-technical stakeholders could execute.',
        'Designed and delivered internal training materials that reduced product catalog error rates and onboarding time for new reps — structured learning programs for audiences from frontline reps to regional directors.',
        'Served as primary point of contact between business stakeholders and technical teams on multi-quarter implementation projects — managing scope, timelines, and stakeholder expectations through delivery.',
        'Developed internal documentation and playbooks for complex product configurations, adopted as standard reference material across the BSA team.',
    ]
    for b in bullets_charter:
        add_bullet(doc, b)

    # ── SELECTED BUILDS ───────────────────────────────────────────────────────
    add_section_heading(doc, 'Selected Builds (Production-Deployed)')
    builds_inline = [
        ('AgentGuard',               'Confidence-gated AI governance layer; EEOC audit trail, human-in-the-loop review queue — built to address the enterprise AI accountability gap',  'Live'),
        ('Agentforce Agents',        'Insurance claims intake routing, PM tenant service, and employee self-service agents — sandbox to production on Salesforce orgs',                 'Deployed'),
        ('Construction Job Tracker', 'Replaced manual WhatsApp update chains with real-time field reporting dashboard; client immediately commissioned two follow-on projects',          'Deployed, client'),
        ('PM Maintenance Triage',    'Multi-tier complaint classification, automated vendor dispatch, tenant confirmation, and audit log for NYC property management firms',             'Deployed'),
    ]
    for name, desc, status in builds_inline:
        para = doc.add_paragraph()
        set_para_spacing(para, before_pt=2, after_pt=2)
        name_run = para.add_run(name + ' — ')
        name_run.font.name = 'Calibri'
        name_run.font.size = Pt(10.5)
        name_run.font.bold = True
        name_run.font.color.rgb = BLACK
        desc_run = para.add_run(desc + '  ')
        desc_run.font.name = 'Calibri'
        desc_run.font.size = Pt(10.5)
        desc_run.font.bold = False
        desc_run.font.color.rgb = BLACK
        status_run = para.add_run(f'[{status}]')
        status_run.font.name = 'Calibri'
        status_run.font.size = Pt(10.5)
        status_run.font.bold = False
        status_run.font.color.rgb = GRAY

    # ── SKILLS ────────────────────────────────────────────────────────────────
    p = doc.add_paragraph()  # spacer
    set_para_spacing(p, before_pt=4, after_pt=0)
    add_section_heading(doc, 'Skills')

    skills = [
        ('AI / Agents',  'Agentforce, OpenAI API, Anthropic Claude, n8n workflow automation, multi-agent orchestration, OpenClaw, agent governance'),
        ('Technical',    'Webhook architecture, API integration, AI system monitoring, cost controls, Google Sheets/Drive automation, Supabase, Vercel'),
        ('Enablement',   'Technical training design, workshop facilitation, executive briefings, adoption frameworks, playbook development'),
        ('Business',     'Enterprise cross-functional coordination, implementation project management, stakeholder communication, system documentation'),
    ]
    for cat, text in skills:
        add_skills_line(doc, cat, text)

    # ── EDUCATION ─────────────────────────────────────────────────────────────
    add_section_heading(doc, 'Education')
    edu_para = doc.add_paragraph()
    set_para_spacing(edu_para, before_pt=4, after_pt=2)
    edu_r1 = edu_para.add_run('Ithaca College')
    edu_r1.font.name = 'Calibri'
    edu_r1.font.size = Pt(10.5)
    edu_r1.font.bold = True
    edu_r1.font.color.rgb = BLACK
    edu_r2 = edu_para.add_run(' — BS Sport Management, Legal Studies Minor · 2014–2018')
    edu_r2.font.name = 'Calibri'
    edu_r2.font.size = Pt(10.5)
    edu_r2.font.bold = False
    edu_r2.font.color.rgb = GRAY

    doc.save(output_path)
    print(f'✅ Resume saved: {output_path}')


def build_cover_letter(output_path):
    doc = Document()

    section = doc.sections[0]
    section.page_width  = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin   = Inches(1.0)
    section.right_margin  = Inches(1.0)
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)

    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    style.font.color.rgb = BLACK

    # ── HEADER ───────────────────────────────────────────────────────────────
    name_para = doc.add_paragraph()
    name_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_para_spacing(name_para, before_pt=0, after_pt=2)
    name_run = name_para.add_run('Jon Trevor Somwaru')
    name_run.font.name = 'Calibri'
    name_run.font.size = Pt(20)
    name_run.font.bold = True
    name_run.font.color.rgb = NAVY

    contact_para = doc.add_paragraph()
    set_para_spacing(contact_para, before_pt=0, after_pt=12)
    contact_run = contact_para.add_run(
        'jtsomwaru@gmail.com · jtsomwaru.com · linkedin.com/in/jon-trevor-somwaru'
    )
    contact_run.font.name = 'Calibri'
    contact_run.font.size = Pt(10)
    contact_run.font.color.rgb = GRAY
    add_horizontal_rule(contact_para)

    # Date + recipient block
    date_para = doc.add_paragraph()
    set_para_spacing(date_para, before_pt=8, after_pt=2)
    date_run = date_para.add_run('March 2026')
    date_run.font.name = 'Calibri'
    date_run.font.size = Pt(11)
    date_run.font.color.rgb = GRAY

    recip_para = doc.add_paragraph()
    set_para_spacing(recip_para, before_pt=0, after_pt=12)
    recip_run = recip_para.add_run('Hiring Manager, OpenAI')
    recip_run.font.name = 'Calibri'
    recip_run.font.size = Pt(11)
    recip_run.font.color.rgb = GRAY

    # ── BODY PARAGRAPHS ──────────────────────────────────────────────────────
    body_paras = [
        ('The gap between an enterprise buying ChatGPT Enterprise and actually using it at scale isn\'t a '
         'product problem. It\'s an adoption problem — and most organizations don\'t have anyone who can '
         'build the bridge between what the platform does and what their teams actually do every day.'),

        ('That\'s the problem I\'ve spent six years learning how to solve, and the last year building AI '
         'systems that make it concrete. At Charter/Spectrum Enterprise, I spent six years as a Business '
         'Systems Analyst responsible for cross-functional adoption of enterprise product systems across a '
         '$1B+ service portfolio. The job wasn\'t building the system — it was getting eight different '
         'internal teams to use it correctly, training audiences from frontline reps to regional directors, '
         'and building the playbooks that made complex configurations repeatable. When I moved into AI '
         'consulting, I took that same operational model and applied it to AI deployment: I\'ve now built '
         'and delivered automation systems for real clients — including a construction project tracking '
         'dashboard that replaced manual WhatsApp chains with real-time field reporting, immediately '
         'generating two follow-on projects for the same client. I\'ve also built a confidence-gated AI '
         'governance layer (AgentGuard) that demonstrates exactly what I try to help clients understand: '
         'that reliable AI deployment requires defined escalation paths, audit trails, and '
         'human-in-the-loop controls — not just a capable model.'),

        ('What I\'d bring to the AI Deployment Manager role specifically is that I\'ve personally lived '
         'the problem your customers are trying to solve. I run 35 autonomous AI agents in production — '
         'with model routing logic, cost controls, error handling, and watchdog processes — and I\'ve had '
         'to figure out what "reliable" actually means when AI systems operate without daily supervision. '
         'That operational experience is what lets me run a workshop for a technical team in the morning '
         'and an executive briefing in the afternoon: I understand what the system can and can\'t do, and '
         'I know how to explain what matters to each audience.'),

        'I\'d be glad to walk through the production infrastructure or any of the client deployments on a call — whichever would be most useful.',
    ]

    for body_text in body_paras:
        p = doc.add_paragraph()
        set_para_spacing(p, before_pt=0, after_pt=10, line_spacing=1.15)
        run = p.add_run(body_text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = BLACK

    # ── CLOSING ──────────────────────────────────────────────────────────────
    p = doc.add_paragraph()
    set_para_spacing(p, before_pt=6, after_pt=2)
    run = p.add_run('Sincerely,')
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.color.rgb = BLACK

    p2 = doc.add_paragraph()
    set_para_spacing(p2, before_pt=14, after_pt=1)
    r1 = p2.add_run('Jon Trevor Somwaru')
    r1.font.name = 'Calibri'
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = BLACK

    p3 = doc.add_paragraph()
    set_para_spacing(p3, before_pt=0, after_pt=0)
    r2 = p3.add_run('jtsomwaru@gmail.com · jtsomwaru.com')
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10)
    r2.font.color.rgb = GRAY

    doc.save(output_path)
    print(f'✅ Cover letter saved: {output_path}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['resume', 'cover_letter', 'both'], default='both')
    parser.add_argument('--output-dir', default='/tmp')
    args = parser.parse_args()

    if args.type in ('resume', 'both'):
        build_resume(f'{args.output_dir}/jt-somwaru-resume.docx')
    if args.type in ('cover_letter', 'both'):
        build_cover_letter(f'{args.output_dir}/jt-somwaru-cover-letter.docx')
