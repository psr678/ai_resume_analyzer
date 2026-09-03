"""
section_detector.py

Optional advanced feature: splits raw resume text into labeled sections
(Summary, Education, Skills, Experience, Projects, Certifications) based
on common heading keywords, before the rest of the pipeline processes it.

This runs entirely offline (no API key, no external model download) --
it works on the RAW text from resume_parser.py (before text_cleaner.py
lowercases/strips it), because section headings rely on short, distinct
lines that cleaning would otherwise blend into the surrounding paragraph.

Why this helps: showing a candidate exactly which section a detected
skill came from (e.g. "found in Skills" vs. "found in Experience") is
more transparent and trustworthy than a single flat list, and lets a
future extension weight skills differently depending on where they
appear (e.g. a skill mentioned in Experience with real usage context
is stronger evidence than the same word appearing once in a Skills list).
"""

import re

# Canonical section name -> heading keywords that indicate that section
# has started. Matching is case-insensitive and tolerant of minor
# variations (e.g. "Work Experience" vs "Experience").
SECTION_HEADERS = {
    "summary": ["summary", "objective", "profile", "about me", "professional summary"],
    "education": ["education", "academic background", "qualifications", "academics"],
    "skills": ["skills", "technical skills", "core competencies", "key skills"],
    "experience": ["experience", "work experience", "professional experience",
                   "employment history", "work history"],
    "projects": ["projects", "personal projects", "academic projects", "key projects"],
    "certifications": ["certifications", "certificates", "licenses", "licenses & certifications"],
}

# A line is considered a heading only if it's short (headings are rarely
# more than a few words) and matches a known keyword closely -- this
# avoids accidentally treating a sentence that merely mentions the word
# "experience" as a new section header.
_MAX_HEADING_WORDS = 5


def _match_section(line: str):
    """Return the canonical section name if this line looks like a heading
    for it, else None."""
    normalized = line.strip().lower().rstrip(":")
    if not normalized or len(normalized.split()) > _MAX_HEADING_WORDS:
        return None

    for section, keywords in SECTION_HEADERS.items():
        for keyword in keywords:
            if normalized == keyword or normalized.startswith(keyword):
                return section
    return None


def detect_sections(raw_text: str) -> dict:
    """Split raw (uncleaned) resume text into sections.

    Returns a dict: {section_name: "joined text for that section"}.
    Text appearing before any recognized heading is stored under
    "header" (typically the candidate's name/contact info/summary line).
    Sections not found in the resume are simply absent from the dict.
    """
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    sections = {"header": []}
    current_section = "header"

    for line in lines:
        matched = _match_section(line)
        if matched:
            current_section = matched
            sections.setdefault(matched, [])
            continue
        sections.setdefault(current_section, []).append(line)

    return {name: "\n".join(content) for name, content in sections.items() if content}


if __name__ == "__main__":
    sample = """
    Jane Smith
    Email: jane@example.com

    Summary
    Experienced data analyst with a passion for dashboards.

    Skills
    Python, SQL, Power BI, Pandas

    Experience
    Data Analyst, ABC Corp (2022-Present)
    Built dashboards and ran SQL queries.

    Projects
    Sales Dashboard: built in Power BI.

    Education
    B.Sc. Statistics, State University
    """
    sections = detect_sections(sample)
    for name, text in sections.items():
        print(f"--- {name} ---")
        print(text)
        print()
