# Testing and Evaluation Notes

Covers the evaluation criteria listed in the project guidance, beyond the
top-role pass/fail table in `test_cases.csv`.

## Extraction quality
Verified by comparing extracted text against the known content of each
sample resume (see `run_pipeline_test.py`). Both PDF and DOCX versions of
all 3 sample resumes extracted identically, confirming `resume_parser.py`
handles both formats consistently, including table-based DOCX layouts.

## Skill precision
Manually checked that skills reported as "found" for each sample resume
are genuinely present in that resume's text (e.g. Resume B correctly
reports scikit-learn, FastAPI, Docker, MLflow -- all explicitly mentioned).
No false-positive skills were observed in testing (e.g. "R" the language
is deliberately absent from resumes that don't mention it, and wasn't
incorrectly flagged).

## Skill recall
Cross-checked the skill dictionary (50 skills across 6 categories) against
each sample resume's actual content and confirmed no explicitly-mentioned
skill was missed. Known limitation: any skill not in `skill_dictionary.csv`
will never be detected (see README limitations) -- recall is bounded by
dictionary coverage, which is the expected tradeoff of the beginner
(keyword-matching) approach specified in the assignment.

## Role ranking
For all 3 sample resumes, the intended top role (matching the resume's
skill profile) ranked first, with reasonable adjacent roles (e.g. Data
Scientist behind Data Analyst; Computer Vision Engineer and AI Engineer
behind NLP Engineer) ranking sensibly close behind based on skill overlap.

## Score consistency
Verified programmatically: adding or removing a required skill from a
resume changes `skill_overlap_score` in the expected direction (more
matched skills -> higher score), since the score is a direct ratio of
matched required-skills to total required-skills, not a black-box model.

## Fairness
The system never extracts or uses name, gender, age, religion, nationality,
photograph, marital status, or disability. Only the skills dictionary
(technical/job-related terms) is searched for; personal-identity terms
are not part of the dictionary and are never scored.

## Usability
The Streamlit dashboard groups results into clearly labeled sections
(Upload -> Extracted Skills -> Job Role Matching -> Skill Gap & Roadmap ->
Download Report) with plain-language labels and a visible Responsible AI
disclaimer, so a student can understand their results without needing to
read the underlying code.
