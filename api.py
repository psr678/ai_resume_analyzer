"""
api.py

Optional advanced feature: a FastAPI backend exposing the same resume
analysis pipeline as a REST API, independent of the Streamlit dashboard.
Useful if this project is extended into a real backend service consumed
by a separate frontend, mobile app, or another system.

Run locally with:
    uvicorn api:app --reload

Then see interactive docs at http://localhost:8000/docs

Responsible AI note: exactly the same rules as app.py -- resumes are
processed only in memory (never written to disk), no protected personal
attributes are used, and every response includes a disclaimer field.
"""

from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from resume_parser import extract_resume_text, ResumeParseError
from section_detector import detect_sections
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, match_resume_to_roles, recommend_top_roles
from roadmap_generator import generate_roadmap, format_roadmap_text, ROADMAP_DISCLAIMER

app = FastAPI(
    title="AI Resume Analyzer API",
    description="REST API for resume-to-job-role matching, skill-gap analysis, "
                "and a rule-based learning roadmap. Guidance only -- not a hiring decision.",
    version="1.0.0",
)

# Load reference data once at startup rather than per-request.
_skill_dict = load_skill_dictionary()
_job_roles = load_job_roles()


class RoleMatch(BaseModel):
    role: str
    match_score: float
    skill_overlap_score: float
    tfidf_score: float
    matched_skills: List[str]
    missing_skills: List[str]


class AnalyzeResponse(BaseModel):
    filename: str
    detected_sections: List[str]
    skills_found: List[str]
    role_matches: List[RoleMatch]
    top_recommended_roles: List[str]
    disclaimer: str


@app.get("/health")
def health_check():
    """Simple liveness check."""
    return {"status": "ok"}


@app.get("/job-roles")
def get_job_roles():
    """List all job roles this API can match against."""
    return {"roles": _job_roles["role"].tolist()}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """Upload a PDF or DOCX resume and get match scores against every job role.

    The file is read entirely in memory and never written to disk.
    """
    file_bytes = await file.read()

    try:
        resume_text = extract_resume_text(file.filename, file_bytes)
    except ResumeParseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error reading file: {e}")

    sections = detect_sections(resume_text)
    extracted = extract_skills(resume_text, _skill_dict)
    match_results = match_resume_to_roles(resume_text, extracted["flat_list"], _job_roles)
    top_roles = recommend_top_roles(match_results, top_n=3)

    role_matches = [
        RoleMatch(
            role=row["role"],
            match_score=row["match_score"],
            skill_overlap_score=row["skill_overlap_score"],
            tfidf_score=row["tfidf_score"],
            matched_skills=row["matched_skills"],
            missing_skills=row["missing_skills"],
        )
        for _, row in match_results.iterrows()
    ]

    return AnalyzeResponse(
        filename=file.filename,
        detected_sections=[s for s in sections if s != "header"],
        skills_found=extracted["flat_list"],
        role_matches=role_matches,
        top_recommended_roles=top_roles["role"].tolist(),
        disclaimer=(
            "This is an automated estimate for guidance only, not a hiring or "
            "rejection decision. It does not use gender, age, religion, "
            "nationality, photograph, marital status, or disability."
        ),
    )


@app.get("/roadmap/{target_role}")
def get_roadmap(target_role: str, skills_found: str = ""):
    """Generate a learning roadmap for a target role, given a comma-separated
    list of skills already found (typically the skills_found list from a
    prior /analyze call). Returns the missing skills and a week-by-week plan.
    """
    matching_roles = _job_roles[_job_roles["role"].str.lower() == target_role.lower()]
    if matching_roles.empty:
        raise HTTPException(status_code=404, detail=f"Unknown role: {target_role}")

    found_skills = [s.strip().lower() for s in skills_found.split(",") if s.strip()]
    role_row = matching_roles.iloc[0]
    required = role_row["required_skills_list"]
    missing = [s for s in required if s not in found_skills]

    roadmap = generate_roadmap(missing)
    return {
        "role": role_row["role"],
        "missing_skills": missing,
        "roadmap": roadmap,
        "roadmap_text": format_roadmap_text(roadmap),
        "disclaimer": ROADMAP_DISCLAIMER,
    }
