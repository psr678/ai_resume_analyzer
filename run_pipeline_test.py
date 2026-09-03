"""
Manual end-to-end sanity test: run every sample resume (both PDF and
DOCX versions) through the full pipeline and print the top recommended
role, to verify extraction -> cleaning -> skill extraction -> matching
-> roadmap all work together correctly before wiring up the Streamlit UI.
"""

from resume_parser import extract_resume_text
from section_detector import detect_sections
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, match_resume_to_roles, recommend_top_roles
from roadmap_generator import generate_roadmap, format_roadmap_text

skill_dict = load_skill_dictionary()
job_roles = load_job_roles()

test_files = [
    ("sample_resumes/resume_A_data_analyst.pdf", "Data Analyst"),
    ("sample_resumes/resume_A_data_analyst.docx", "Data Analyst"),
    ("sample_resumes/resume_B_ml_engineer.pdf", "Machine Learning Engineer"),
    ("sample_resumes/resume_B_ml_engineer.docx", "Machine Learning Engineer"),
    ("sample_resumes/resume_C_nlp_engineer.pdf", "NLP Engineer"),
    ("sample_resumes/resume_C_nlp_engineer.docx", "NLP Engineer"),
]

all_passed = True
for path, expected_top_role in test_files:
    with open(path, "rb") as f:
        file_bytes = f.read()
    filename = path.split("/")[-1]

    text = extract_resume_text(filename, file_bytes)
    sections = detect_sections(text)
    extracted = extract_skills(text, skill_dict)
    results = match_resume_to_roles(text, extracted["flat_list"], job_roles)
    top_roles = recommend_top_roles(results, top_n=3)
    actual_top_role = top_roles.iloc[0]["role"]

    expected_sections = {"skills", "experience", "projects", "education"}
    found_sections = set(sections.keys())
    sections_ok = expected_sections.issubset(found_sections)

    status = "PASS" if (actual_top_role == expected_top_role and sections_ok) else "CHECK"
    if status == "CHECK":
        all_passed = False

    print(f"[{status}] {filename}")
    print(f"  Sections detected: {sorted(found_sections)} "
          f"({'all 4 required found' if sections_ok else 'MISSING: ' + str(expected_sections - found_sections)})")
    print(f"  Expected top role: {expected_top_role}")
    print(f"  Actual top role:   {actual_top_role} ({top_roles.iloc[0]['match_score']}%)")
    print(f"  Skills found ({len(extracted['flat_list'])}): {extracted['flat_list']}")
    print(f"  Top 3: {[(r['role'], r['match_score']) for _, r in top_roles.iterrows()]}")
    print()

print("ALL PASSED" if all_passed else "SOME MISMATCHES -- see CHECK rows above")
