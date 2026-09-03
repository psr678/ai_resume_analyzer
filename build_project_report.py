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
    "fully offline with no external API key required.", styles['Bodys']))

story.append(Paragraph("4. Architecture / Workflow", styles['H2s']))
story.append(Image('architecture_diagram.png', width=3.6*inch, height=6.7*inch))
story.append(Paragraph("Pipeline: Upload -> Extract -> Clean -> Extract Skills -> Load Job Roles -> Compare -> Score -> Recommend -> Roadmap -> Dashboard.", styles['Caption']))

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
    "across formats. See tests/test_cases.csv and tests/evaluation_notes.md for full details "
    "(extraction quality, skill precision/recall, score consistency, fairness, usability).", styles['Bodys']))

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

story.append(Paragraph("8. Limitations & Future Improvements", styles['H2s']))
story.append(Paragraph(
    "Keyword-matching skill extraction is bounded by the 50-skill dictionary (a skill mentioned under "
    "an unlisted name/spelling won't be detected); scanned/image-only PDFs cannot be read (no OCR); "
    "TF-IDF/cosine similarity is bag-of-words and doesn't capture semantic meaning the way Sentence "
    "Transformers would. Future improvements: semantic matching with Sentence Transformers, LLM-based "
    "resume feedback (optional, requires an API key), resume section detection, and FastAPI/Docker "
    "deployment for a production backend.", styles['Bodys']))

story.append(Paragraph("9. Conclusion", styles['H2s']))
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
