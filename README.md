# AI Resume Analyzer and Job Recommendation System

An NLP-based Streamlit application that analyzes how well a resume matches
different job roles, identifies missing skills, and generates a simple
learning roadmap to close the gap.

![Architecture Diagram](architecture_diagram.png)

## Project Overview

- **Problem it solves:** students often don't know whether their resume
  contains the skills expected for a role. This tool gives an automated,
  transparent first estimate.
- **Approach used:** the "beginner approach" from the project brief --
  keyword-based skill extraction, TF-IDF + cosine similarity for text
  matching (blended with a direct skill-overlap ratio), and a rule-based
  learning roadmap. No labelled ML model or LLM API key is required to
  run the core features.

## Folder Structure

```
ai_resume_analyzer/
|-- app.py                    # Streamlit dashboard (entry point)
|-- api.py                     # Optional: FastAPI backend (same pipeline as a REST API)
|-- job_dashboard.py            # Optional: job-role chart-building logic
|-- resume_parser.py             # PDF/DOCX text extraction
|-- section_detector.py           # Optional: splits resume into labeled sections
|-- text_cleaner.py                # Text cleaning & normalization
|-- skill_extractor.py              # Keyword-based skill extraction
|-- job_matcher.py                   # TF-IDF + cosine similarity + skill-overlap scoring
|-- roadmap_generator.py              # Rule-based learning roadmap
|-- requirements.txt
|-- README.md
|-- .env.example                       # Only needed for the optional LLM-feedback feature
|-- .gitignore
|-- .dockerignore
|-- Dockerfile                          # Optional: containerizes the Streamlit app
|-- Dockerfile.api                       # Optional: containerizes the FastAPI backend
|-- docker-compose.yml                    # Optional: runs both together
|-- architecture_diagram.png
|-- build_sample_resumes.py                # Regenerates the sample resumes below
|-- run_pipeline_test.py                    # End-to-end pipeline sanity test
|-- test_api.py                              # FastAPI endpoint test suite
|
|-- data/
|   |-- job_roles.csv                  # 8 job roles + required skills
|   |-- skill_dictionary.csv            # 50 skills across 6 categories
|
|-- sample_resumes/                      # 3 sanitized sample resumes (PDF + DOCX)
|-- reports/                              # Downloaded reports land here locally (gitignored)
|-- tests/
    |-- test_cases.csv                      # Testing sheet (expected vs actual top role)
    |-- evaluation_notes.md                  # Extraction/precision/recall/fairness notes
```

## Setup

1. **Create and activate a virtual environment** (recommended):
   ```
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```
   streamlit run app.py
   ```
   This opens the dashboard at `http://localhost:8501`.

4. **Try it out:** upload one of the files in `sample_resumes/` (or your
   own PDF/DOCX resume), pick a target role, and explore the results.

## How It Works

See `architecture_diagram.png` for the full pipeline. In short:

1. **Upload** (`app.py`) -- accepts a PDF or DOCX file, validates type/size.
2. **Extract** (`resume_parser.py`) -- pulls raw text from every page/paragraph.
3. **Detect sections** (`section_detector.py`) -- splits the raw text into
   Header/Summary/Education/Skills/Experience/Projects/Certifications by
   matching common heading keywords, shown as tabs in the dashboard.
4. **Clean** (`text_cleaner.py`) -- lowercases and strips noisy symbols while
   preserving technical terms like `C++`, `C#`, `.NET`.
5. **Extract skills** (`skill_extractor.py`) -- matches cleaned text against
   a 50-skill controlled dictionary (`data/skill_dictionary.csv`), including
   common aliases (e.g. "ml" -> "machine learning").
6. **Match & rank roles** (`job_matcher.py`) -- for each of the 8 job roles
   in `data/job_roles.csv`, computes a blended score: 60% skill-overlap
   ratio + 40% TF-IDF/cosine text similarity.
7. **Roadmap** (`roadmap_generator.py`) -- turns the missing skills for a
   selected target role into a week-by-week learning roadmap.
8. **Dashboard** (`app.py`) -- shows all of the above, plus a downloadable
   `.txt` analysis report.

## Testing

Run the automated end-to-end sanity check (extracts, matches, and verifies
the top-recommended role for all 3 sample resumes in both PDF and DOCX form):

```
python run_pipeline_test.py
```

See `tests/test_cases.csv` for the results table and `tests/evaluation_notes.md`
for qualitative notes on extraction quality, skill precision/recall, role
ranking, score consistency, fairness, and usability.

## Responsible AI

This tool follows the responsible-AI rules from the project brief:

- **Guidance only** -- not used for automatic hiring or rejection decisions.
- **No protected attributes** -- never scores gender, age, religion,
  nationality, photograph, marital status, or disability. Only job-related
  skills, education, projects, and experience text is evaluated.
- **Estimates, not decisions** -- every score is shown with a plain-language
  disclaimer in both the dashboard and the downloadable report.
- **No permanent storage** -- uploaded resumes are processed entirely in
  memory for the current session; nothing is written to disk.
- **Keyword limits are disclosed** -- the roadmap and report explicitly
  note that a missing keyword does not always mean missing ability.

## Limitations

- **Keyword-matching skill extraction** only detects skills present in
  `data/skill_dictionary.csv` (50 skills). A resume mentioning a skill
  under an unlisted name/spelling won't be detected -- this is the
  documented tradeoff of the beginner approach vs. NLP/LLM-based extraction.
- **Scanned/image-only PDFs** cannot be read (no OCR is implemented);
  `resume_parser.py` raises a clear error in this case rather than
  silently returning empty text.
- **TF-IDF/cosine similarity is a bag-of-words method** and doesn't
  understand semantic meaning the way Sentence Transformers would (a
  documented "advanced approach" upgrade path in the project brief).
- **The 8-role, 50-skill reference data is illustrative**, not exhaustive
  -- a production version would need a broader, continuously maintained
  dataset.

## Optional Advanced Features

### Implemented: Resume Section Detection

`section_detector.py` splits the raw resume text into labeled sections
(Header, Summary, Education, Skills, Experience, Projects, Certifications)
by matching common heading keywords, before the rest of the pipeline runs.
Fully offline -- no API key or model download required. The dashboard
shows which sections were detected and lets you inspect each one in its
own tab. Verified in `run_pipeline_test.py`: all 3 sample resumes (PDF +
DOCX) correctly detect all 4 required sections (Skills, Experience,
Projects, Education).

### Implemented: Job-Role Dashboard with Charts

`job_dashboard.py` builds two charts straight from the reference data
(`data/job_roles.csv` + `data/skill_dictionary.csv`), shown in an
expandable "Explore Job Roles Dashboard" section at the top of `app.py`
-- viewable even before uploading a resume:

- **Required Skill Count by Job Role** -- a bar chart of how many skills
  each of the 8 roles requires.
- **Skill Category Composition by Job Role** -- a stacked bar chart
  showing which skill categories (Programming, Machine Learning, Cloud,
  etc.) make up each role's requirements.

Useful for a student who hasn't uploaded a resume yet and wants to get a
sense of which roles are skill-heavy or which categories matter most for
a role they're considering.

### Implemented: FastAPI Backend

`api.py` exposes the exact same pipeline (parse -> detect sections ->
extract skills -> match -> roadmap) as a REST API, independent of the
Streamlit dashboard -- useful if this project is extended with a
different frontend, a mobile app, or integrated into another system.

Endpoints:
- `GET /health` -- liveness check.
- `GET /job-roles` -- list of all 8 job roles.
- `POST /analyze` -- upload a resume file, get back match scores against
  every role, detected sections, and extracted skills as JSON.
- `GET /roadmap/{target_role}` -- given a comma-separated list of found
  skills, returns the missing skills and a week-by-week roadmap for that role.

Run it locally with `uvicorn api:app --reload`, then visit
`http://localhost:8000/docs` for interactive API documentation (Swagger UI).

Tested with `test_api.py` (FastAPI `TestClient`, no network required) and
manually verified against a live `uvicorn` server with `curl` -- all
endpoints return correct results, including error handling for
unsupported file types (400) and unknown roles (404).

### Implemented: Docker Deployment

- `Dockerfile` containerizes the Streamlit dashboard (port 8501).
- `Dockerfile.api` containerizes the FastAPI backend (port 8000).
- `docker-compose.yml` runs both together with `docker compose up --build`.

**Important caveat:** these Dockerfiles were written and carefully
reviewed but could **not be build-tested** in the development sandbox
used to create this project (no Docker daemon was available there).
They follow a standard, well-tested pattern (`python:3.11-slim` base,
cached `pip install` layer, then app code), so they are expected to work,
but please build and run them yourself (`docker build -t resume-analyzer-app .`
then `docker run -p 8501:8501 resume-analyzer-app`) and let me know if
anything needs adjusting.

### Not Implemented

Per the project brief, these remain optional upgrades beyond the required
minimum feature set, intentionally left out of this submission to keep
the core pipeline self-contained and free of external API dependencies:

- LLM-generated resume feedback (would need a Groq/Gemini/OpenAI API key
  -- see `.env.example` for the expected format if you add this).
- Sentence Transformers for semantic matching (runs locally but requires
  downloading a pretrained model on first run).
- Database persistence (SQLite/PostgreSQL) -- not needed since resumes
  are intentionally not stored (see Responsible AI notes above).

## Deployment

To deploy to Streamlit Community Cloud:

1. Push this folder to a GitHub repository (see below).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, and select this repository + `app.py` as the entry point.
3. Streamlit Cloud will install `requirements.txt` and deploy automatically.

Alternatively, deploy with Docker (see above) to any host that can run a
Docker container (Render, Railway, a VPS, etc.).

## Pushing to GitHub

```
cd ai_resume_analyzer
git init
git add .
git commit -m "Initial commit: AI Resume Analyzer and Job Recommendation System"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```
