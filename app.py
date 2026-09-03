"""
app.py

Streamlit dashboard for the AI Resume Analyzer and Job Recommendation
System. Ties together resume_parser, text_cleaner, skill_extractor,
job_matcher, and roadmap_generator into an interactive tool.

Responsible AI rules implemented here (see README for the full list):
- Resume bytes are only ever held in memory (never written to disk),
  so there is no temporary file to remember to delete.
- No protected personal attributes (name, gender, age, photo, etc.) are
  ever extracted, scored, or displayed -- only job-related skill text.
- Every score is shown with a plain-language disclaimer that it is an
  estimate for guidance, not a hiring/rejection decision.
"""

import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from resume_parser import extract_resume_text, ResumeParseError
from section_detector import detect_sections
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, match_resume_to_roles, recommend_top_roles
from job_dashboard import figure_required_skill_counts, figure_role_category_breakdown
from roadmap_generator import generate_roadmap, format_roadmap_text, ROADMAP_DISCLAIMER

st.set_page_config(page_title="AI Resume Analyzer", page_icon="\U0001F4C4", layout="wide")


@st.cache_data
def _load_reference_data():
    """Cache the small reference CSVs so they aren't reloaded on every rerun."""
    return load_skill_dictionary(), load_job_roles()


def build_report_text(target_role, match_row, extracted_skills, roadmap):
    """Build a plain-text downloadable report summarizing the analysis."""
    lines = []
    lines.append("AI RESUME ANALYZER - ANALYSIS REPORT")
    lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append(f"Target Role: {target_role}")
    lines.append(f"Match Score: {match_row['match_score']}%")
    lines.append(f"  (skill overlap: {match_row['skill_overlap_score']}%, "
                 f"text similarity: {match_row['tfidf_score']}%)")
    lines.append("")
    lines.append("Skills Found:")
    for skill in extracted_skills["flat_list"]:
        lines.append(f"  - {skill}")
    lines.append("")
    lines.append("Missing Skills for Target Role:")
    for skill in match_row["missing_skills"]:
        lines.append(f"  - {skill}")
    lines.append("")
    lines.append("Suggested Learning Roadmap:")
    lines.append(format_roadmap_text(roadmap))
    lines.append("")
    lines.append("-" * 60)
    lines.append("Disclaimer: This match score is an automated estimate for")
    lines.append("self-guidance only. It is not a hiring or rejection decision,")
    lines.append("and it does not use gender, age, religion, nationality,")
    lines.append("photograph, marital status, or disability in any way.")
    lines.append(ROADMAP_DISCLAIMER)
    return "\n".join(lines)


def main():
    st.title("\U0001F4C4 AI Resume Analyzer and Job Recommendation System")
    st.caption(
        "Upload your resume to see how well it matches different job roles, "
        "what skills you're missing, and a simple learning roadmap to close the gap."
    )

    with st.expander("About this tool and Responsible AI notice", expanded=False):
        st.markdown(
            "- This tool is for **guidance only** -- it is not used for automatic "
            "hiring or rejection decisions.\n"
            "- It evaluates only **job-related skills, education, projects, and "
            "experience** found in your resume text.\n"
            "- It does **not** use your name, gender, age, religion, nationality, "
            "photograph, marital status, or disability in any calculation.\n"
            "- Match scores are **estimates**, not guarantees. A missing keyword "
            "does not always mean missing ability.\n"
            "- Your uploaded resume is processed **only in memory** for this "
            "session and is never saved to disk."
        )

    skill_dict, job_roles = _load_reference_data()

    # ------------------------------------------------------------------
    # Optional advanced feature: Job-Role Dashboard (no resume needed)
    # ------------------------------------------------------------------
    with st.expander("\U0001F4CA Explore Job Roles Dashboard (no resume needed)", expanded=False):
        st.caption(
            "Browse the reference job-role data itself -- useful for deciding which "
            "role to target before you even upload a resume."
        )
        st.plotly_chart(figure_required_skill_counts(job_roles), use_container_width=True)
        st.plotly_chart(figure_role_category_breakdown(job_roles, skill_dict), use_container_width=True)

    st.divider()

    # ------------------------------------------------------------------
    # Module 1: Resume Upload
    # ------------------------------------------------------------------
    st.header("1. Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload a PDF or DOCX resume (max 5 MB)", type=["pdf", "docx"]
    )

    if uploaded_file is None:
        st.info("Upload a resume above to get started.")
        st.stop()

    st.success(f"Uploaded: {uploaded_file.name}")

    try:
        file_bytes = uploaded_file.getvalue()
        resume_text = extract_resume_text(uploaded_file.name, file_bytes)
    except ResumeParseError as e:
        st.error(f"Could not process this resume: {e}")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred while reading the file: {e}")
        st.stop()

    # ------------------------------------------------------------------
    # Optional advanced feature: Resume Section Detection
    # ------------------------------------------------------------------
    st.header("2. Detected Resume Sections")
    sections = detect_sections(resume_text)
    section_labels = {
        "header": "Header / Summary", "summary": "Summary", "education": "Education",
        "skills": "Skills", "experience": "Experience", "projects": "Projects",
        "certifications": "Certifications",
    }
    detected_names = [s for s in sections if s != "header"]
    if detected_names:
        st.success(f"Detected {len(detected_names)} section(s): "
                   f"{', '.join(section_labels.get(s, s).title() for s in detected_names)}")
    else:
        st.info("No standard section headings (e.g. 'Skills', 'Experience') were detected -- "
                "this resume may use a non-standard layout. Skill extraction below still runs "
                "on the full resume text regardless.")

    if sections:
        tabs = st.tabs([section_labels.get(s, s).title() for s in sections])
        for tab, section_name in zip(tabs, sections):
            with tab:
                st.text(sections[section_name])

    # ------------------------------------------------------------------
    # Module 3: Skill Extraction
    # ------------------------------------------------------------------
    extracted = extract_skills(resume_text, skill_dict)

    st.header("3. Extracted Skills")
    if not extracted["flat_list"]:
        st.warning(
            "No skills from our skill dictionary were found in this resume. "
            "Try a resume with more explicit technical skill mentions."
        )
    else:
        cols = st.columns(3)
        categories = [c for c, skills in extracted["by_category"].items() if skills]
        for i, category in enumerate(categories):
            with cols[i % 3]:
                st.markdown(f"**{category}**")
                for skill in extracted["by_category"][category]:
                    st.markdown(f"- {skill}")

    # ------------------------------------------------------------------
    # Module 5: Matching and Recommendation
    # ------------------------------------------------------------------
    st.header("4. Job Role Matching")
    match_results = match_resume_to_roles(resume_text, extracted["flat_list"], job_roles)

    fig = px.bar(
        match_results.sort_values("match_score"),
        x="match_score", y="role", orientation="h",
        labels={"match_score": "Match Score (%)", "role": "Job Role"},
        title="Resume Match Score by Job Role",
        range_x=[0, 100],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 3 Recommended Roles")
    top_roles = recommend_top_roles(match_results, top_n=3)
    for i, row in top_roles.reset_index(drop=True).iterrows():
        st.markdown(f"**{i+1}. {row['role']} — {row['match_score']}%**")

    # ------------------------------------------------------------------
    # Module 6: Skill-Gap Analysis (for a user-selected target role)
    # ------------------------------------------------------------------
    st.header("5. Skill-Gap Analysis and Learning Roadmap")
    target_role = st.selectbox("Select a target role for detailed analysis:", job_roles["role"].tolist())

    target_row = match_results[match_results["role"] == target_role].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Match Score for " + target_role, f"{target_row['match_score']}%")
        st.markdown("**Skills Found (relevant to this role):**")
        if target_row["matched_skills"]:
            for skill in target_row["matched_skills"]:
                st.markdown(f"- {skill}")
        else:
            st.markdown("_None of this role's required skills were found._")

    with col2:
        st.markdown("**Missing Skills:**")
        if target_row["missing_skills"]:
            for skill in target_row["missing_skills"]:
                st.markdown(f"- {skill}")
        else:
            st.markdown("_No missing skills -- great match!_")

    roadmap = generate_roadmap(target_row["missing_skills"])
    st.subheader("Suggested Learning Roadmap")
    st.code(format_roadmap_text(roadmap), language=None)
    st.caption(ROADMAP_DISCLAIMER)

    # ------------------------------------------------------------------
    # Module 7: Downloadable Report
    # ------------------------------------------------------------------
    st.header("6. Download Your Report")
    report_text = build_report_text(target_role, target_row, extracted, roadmap)
    st.download_button(
        label="Download Analysis Report (.txt)",
        data=report_text,
        file_name=f"resume_analysis_{target_role.replace(' ', '_').lower()}.txt",
        mime="text/plain",
    )


if __name__ == "__main__":
    main()
