from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, Image, ListFlowable, ListItem, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleC', fontSize=19, leading=23, spaceAfter=4, textColor=colors.HexColor('#1a3d5c')))
styles.add(ParagraphStyle(name='SubInfo', fontSize=10, leading=14, textColor=colors.HexColor('#444444'), spaceAfter=10))
styles.add(ParagraphStyle(name='H2s', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#2c5a7c'), spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name='Bodys', parent=styles['Normal'], fontSize=9.8, leading=13.5, spaceAfter=7))
styles.add(ParagraphStyle(name='Caption', parent=styles['Normal'], fontSize=8.5, alignment=1, textColor=colors.HexColor('#555555'), spaceAfter=10))
styles.add(ParagraphStyle(name='CellHead', parent=styles['Normal'], fontSize=8.6, leading=10.5, textColor=colors.white, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='CellBody', parent=styles['Normal'], fontSize=8.4, leading=10.5))
styles.add(ParagraphStyle(name='CellBodyCenter', parent=styles['Normal'], fontSize=8.4, leading=10.5, alignment=1))
styles.add(ParagraphStyle(name='CellLink', parent=styles['Normal'], fontSize=8.4, leading=10.5, textColor=colors.HexColor('#1a56db')))
styles.add(ParagraphStyle(name='HighlightHead', parent=styles['Normal'], fontSize=11, leading=14, textColor=colors.HexColor('#1a3d5c'), fontName='Helvetica-Bold', spaceAfter=4))
styles.add(ParagraphStyle(name='HighlightBody', parent=styles['Normal'], fontSize=9.2, leading=12.8, spaceAfter=5))

def cell(text, style=None):
    return Paragraph(text, style or styles['CellBody'])

story = []

story.append(Paragraph("AI Resume Analyzer and Job Recommendation System", styles['TitleC']))
story.append(Paragraph("Major Project Report", styles['SubInfo']))

info_table = Table([
    ["Student:", "Raju_P_S", "Batch:", "AIML Batch", "Date:", "3 September 2026"],
], colWidths=[0.5*inch, 1.3*inch, 0.5*inch, 1.3*inch, 0.45*inch, 1.3*inch])
info_table.setStyle(TableStyle([
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
    ('FONTNAME', (4,0), (4,-1), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(info_table)
story.append(Spacer(1, 4))

REPO = "https://github.com/psr678/ai_resume_analyzer"

def link_cell(text, url, style=None):
    return Paragraph(f'<link href="{url}"><u>{text}</u></link>', style or styles['CellLink'])

story.append(Paragraph("Submission Deliverables &amp; GitHub Repository Links", styles['H2s']))
story.append(Paragraph(
    f'All source code, datasets, and supporting files referenced below are in the public GitHub '
    f'repository: <link href="{REPO}"><u>{REPO}</u></link>. This report is self-contained -- every '
    f'deliverable required by the assignment brief is listed here with a direct link to its exact '
    f'location, so this PDF alone is sufficient for submission and review.', styles['Bodys']))

deliverables = [
    ["1", "Working Streamlit application", link_cell("app.py", f"{REPO}/blob/main/app.py")],
    ["2", "Complete source code", link_cell("repository root (all .py modules)", f"{REPO}")],
    ["3", "Job-role and skill datasets", link_cell("data/ (job_roles.csv, skill_dictionary.csv)", f"{REPO}/tree/main/data")],
    ["4", "Sample resumes (personal info removed)", link_cell("sample_resumes/", f"{REPO}/tree/main/sample_resumes")],
    ["5", "requirements.txt", link_cell("requirements.txt", f"{REPO}/blob/main/requirements.txt")],
    ["6", "README (setup &amp; usage instructions)", link_cell("README.md", f"{REPO}/blob/main/README.md")],
    ["7", "Architecture / workflow diagram", link_cell("architecture_diagram.png", f"{REPO}/blob/main/architecture_diagram.png")],
    ["8", "Testing sheet", link_cell("tests/test_cases.csv", f"{REPO}/tree/main/tests")],
    ["9", "GitHub repository", link_cell(REPO.replace("https://", ""), REPO)],
    ["10", "Project report &amp; demonstration video", Paragraph(
        'This PDF report (self-contained). Demonstration video: '
        f'<link href="{REPO}/blob/main/demo_video.mp4"><u>demo_video.mp4</u></link>', styles['CellBody'])],
]
deliv_rows = [[cell("#", styles['CellHead']), cell("Deliverable", styles['CellHead']), cell("Location / Link", styles['CellHead'])]]
for num, name, loc in deliverables:
    loc_cell = loc if isinstance(loc, Paragraph) else cell(loc)
    deliv_rows.append([cell(num, styles['CellBodyCenter']), cell(name), loc_cell])

dt = Table(deliv_rows, colWidths=[0.3*inch, 2.35*inch, 3.05*inch])
dt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3d5c')),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f2f6f9')]),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(dt)
story.append(Spacer(1, 8))

story.append(PageBreak())

story.append(Paragraph("1. Project Objective", styles['H2s']))
story.append(Paragraph(
    "Build an NLP-based application that helps students understand how well their resume matches "
    "selected job roles. The system provides a match score, lists important missing skills, and "
    "generates a simple learning roadmap.", styles['Bodys']))

story.append(Paragraph("2. Problem Statement", styles['H2s']))
story.append(Paragraph(
    "Students often do not know whether their resume contains the skills expected for a particular "
    "role. This project creates an educational matching system that focuses on skills, projects, "
    "education, and relevant experience -- giving a quick, transparent, automated first estimate.", styles['Bodys']))

story.append(Paragraph("3. Approach Used", styles['H2s']))
story.append(Paragraph(
    "The <b>beginner approach</b> specified in the project brief: keyword-based skill extraction against "
    "a controlled 50-skill dictionary, <b>TF-IDF vectorization + cosine similarity</b> for text-level "
    "matching, blended with a direct skill-overlap ratio (60% skill overlap + 40% TF-IDF) for an "
    "interpretable match score, and a <b>rule-based learning roadmap</b> for missing skills. This runs "
    "fully offline with no external API key required. One optional advanced feature was also added: "
    "<b>resume section detection</b> (education/skills/experience/projects), also fully offline.", styles['Bodys']))

story.append(Paragraph("4. Architecture / Workflow", styles['H2s']))
story.append(Image('architecture_diagram.png', width=3.4*inch, height=7.1*inch))
story.append(Paragraph("Pipeline: Upload -> Extract -> Detect Sections -> Clean -> Extract Skills -> Load Job Roles -> Compare -> Score -> Recommend -> Roadmap -> Dashboard.", styles['Caption']))

story.append(PageBreak())

story.append(Paragraph("5. Job Roles & Skill Dictionary", styles['H2s']))
story.append(Paragraph(
    "<b>8 job roles</b> defined in data/job_roles.csv (Data Analyst, Machine Learning Engineer, AI "
    "Engineer, NLP Engineer, Computer Vision Engineer, Data Scientist, Backend Developer, Cloud "
    "Engineer). <b>50 technical skills</b> defined in data/skill_dictionary.csv across 6 categories "
    "(Programming, Databases, Data Handling, Machine Learning, Cloud, Tools & Frameworks) -- above "
    "the assignment's 20-30 skill minimum.", styles['Bodys']))

story.append(Paragraph("6. Testing Results", styles['H2s']))
story.append(Paragraph(
    "3 sanitized sample resumes (Data Analyst-, ML Engineer-, and NLP Engineer-leaning) were tested "
    "in both PDF and DOCX form (6 test cases total) via an automated end-to-end pipeline script.", styles['Bodys']))

test_data = [
    [cell("Test Resume", styles['CellHead']), cell("Format", styles['CellHead']), cell("Expected Top Role", styles['CellHead']), cell("Actual Top Role", styles['CellHead']), cell("Score", styles['CellHead'])],
    [cell("Resume A"), cell("PDF", styles['CellBodyCenter']), cell("Data Analyst"), cell("Data Analyst"), cell("80.0%", styles['CellBodyCenter'])],
    [cell("Resume A"), cell("DOCX", styles['CellBodyCenter']), cell("Data Analyst"), cell("Data Analyst"), cell("80.0%", styles['CellBodyCenter'])],
    [cell("Resume B"), cell("PDF", styles['CellBodyCenter']), cell("ML Engineer"), cell("ML Engineer"), cell("77.1%", styles['CellBodyCenter'])],
    [cell("Resume B"), cell("DOCX", styles['CellBodyCenter']), cell("ML Engineer"), cell("ML Engineer"), cell("77.1%", styles['CellBodyCenter'])],
    [cell("Resume C"), cell("PDF", styles['CellBodyCenter']), cell("NLP Engineer"), cell("NLP Engineer"), cell("81.2%", styles['CellBodyCenter'])],
    [cell("Resume C"), cell("DOCX", styles['CellBodyCenter']), cell("NLP Engineer"), cell("NLP Engineer"), cell("81.2%", styles['CellBodyCenter'])],
]
tt = Table(test_data, colWidths=[1.0*inch, 0.7*inch, 1.6*inch, 1.6*inch, 0.7*inch])
tt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3d5c')),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f2f6f9')]),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(tt)
story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Result: 6/6 test cases passed</b> -- the expected top role matched the actual top role in "
    "every case, and PDF/DOCX results were identical for each resume, confirming parser consistency "
    "across formats. All 4 required sections (Skills, Experience, Projects, Education) were also "
    "correctly detected in every test case. See tests/test_cases.csv and tests/evaluation_notes.md "
    "for full details (extraction quality, skill precision/recall, score consistency, fairness, usability).", styles['Bodys']))

story.append(Paragraph("7. Responsible AI Rules Applied", styles['H2s']))
rules = [
    "Used for guidance only -- not automatic hiring/rejection.",
    "Never scores gender, age, religion, nationality, photograph, marital status, or disability.",
    "Evaluates only job-related skills, education, projects, and experience.",
    "Every score is shown with a disclaimer that it is an estimate, not a recruiter decision.",
    "Uploaded resumes are processed in memory only -- never written to disk.",
    "The report explicitly states that missing keywords do not always mean missing ability.",
]
story.append(ListFlowable([ListItem(Paragraph(r, styles['Bodys']), bulletColor=colors.HexColor('#2c5a7c')) for r in rules], bulletType='bullet', leftIndent=14))

story.append(Paragraph("8. Optional Advanced Features Implemented", styles['H2s']))
story.append(Paragraph(
    "The assignment brief lists several optional advanced upgrades beyond the minimum requirement. "
    "<b>Four of these were implemented</b> in this submission, each with a direct code link:", styles['Bodys']))

adv_features = [
    ("&#10003; Resume Section Detection", "section_detector.py",
     "Splits resumes into Education / Skills / Experience / Projects sections before the rest of "
     "the pipeline runs; verified correct on all 6 test cases.", f"{REPO}/blob/main/section_detector.py"),
    ("&#10003; Job-Role Dashboard with Charts", "job_dashboard.py",
     "Required-skill-count and skill-category-composition charts across all 8 roles, viewable "
     "without uploading a resume.", f"{REPO}/blob/main/job_dashboard.py"),
    ("&#10003; FastAPI Backend", "api.py",
     "REST API exposing the same pipeline (/analyze, /roadmap, /job-roles, /health); tested with "
     "FastAPI TestClient and a live uvicorn + curl session.", f"{REPO}/blob/main/api.py"),
    ("&#10003; Docker Deployment", "Dockerfile, Dockerfile.api, docker-compose.yml",
     "Containerizes both the Streamlit app and the FastAPI backend. Note: written and reviewed "
     "carefully, tested locally by the student and confirmed working; not build-tested in the "
     "development sandbox itself.", f"{REPO}/blob/main/docker-compose.yml"),
]

adv_flat_rows = []
for title, filename, desc, url in adv_features:
    combined = Paragraph(
        f'{title} &mdash; <link href="{url}"><u>{filename}</u></link><br/>'
        f'<font size="9.2">{desc}</font>', styles['HighlightBody'])
    adv_flat_rows.append([combined])

adv_box = Table(adv_flat_rows, colWidths=[6.7*inch])
adv_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eef7ee')),
    ('BOX', (0,0), (-1,-1), 1.0, colors.HexColor('#2e7d32')),
    ('LINEBELOW', (0,0), (-1,-2), 0.6, colors.HexColor('#bfe0bf')),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
]))
story.append(adv_box)
story.append(Spacer(1, 4))
story.append(Paragraph(
    "These were implemented in addition to the required minimum feature set, and are not needed "
    "to satisfy the core assignment -- they were added to demonstrate extra depth.", styles['Caption']))

story.append(Paragraph("9. Limitations & Future Improvements", styles['H2s']))
story.append(Paragraph(
    "Keyword-matching skill extraction is bounded by the 50-skill dictionary (a skill mentioned under "
    "an unlisted name/spelling won't be detected); scanned/image-only PDFs cannot be read (no OCR); "
    "TF-IDF/cosine similarity is bag-of-words and doesn't capture semantic meaning the way Sentence "
    "Transformers would. Future improvements: semantic matching with Sentence Transformers, LLM-based "
    "resume feedback (optional, requires an API key), and a database layer if resume storage is ever "
    "required (intentionally not implemented now -- see Responsible AI notes).", styles['Bodys']))

story.append(Paragraph("10. Conclusion", styles['H2s']))
story.append(Paragraph(
    "This project delivers a complete, working, offline resume-to-job-role matching pipeline covering "
    "every required module: upload, text extraction, cleaning, skill extraction (50 skills, well above "
    "the 20-30 minimum), matching against 8 job roles via TF-IDF + cosine similarity blended with "
    "skill overlap, skill-gap analysis, a rule-based learning roadmap, and an interactive Streamlit "
    "dashboard with a downloadable report. All 6 end-to-end test cases passed, and the codebase follows "
    "the responsible-AI rules specified in the project brief throughout.", styles['Bodys']))

doc = SimpleDocTemplate(
    "Raju_P_S_AI_Resume_Analyzer_Project_Report.pdf",
    pagesize=letter,
    topMargin=0.55*inch, bottomMargin=0.55*inch,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    title="AI Resume Analyzer - Project Report - Raju_P_S",
    author="Raju_P_S", creator="Raju_P_S",
)
doc.build(story)

from pypdf import PdfReader, PdfWriter
reader = PdfReader("Raju_P_S_AI_Resume_Analyzer_Project_Report.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
writer.add_metadata({
    "/Author": "Raju_P_S", "/Creator": "Raju_P_S", "/Producer": "Raju_P_S",
    "/Title": "AI Resume Analyzer - Project Report - Raju_P_S",
})
with open("Raju_P_S_AI_Resume_Analyzer_Project_Report.pdf", "wb") as f:
    writer.write(f)

print("PDF built.")
