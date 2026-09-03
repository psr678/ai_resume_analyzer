"""
job_matcher.py

Compares a resume against a set of job roles and produces a ranked list
of match scores. Implements the "beginner approach" specified in the
assignment: TF-IDF vectorization + cosine similarity, blended with a
direct skill-overlap ratio for a more interpretable score.

Why blend two signals instead of using TF-IDF alone:
- TF-IDF/cosine similarity captures overall textual similarity between the
  resume and a role's description, which is useful but can be noisy (a
  resume that happens to share a lot of common words with a role's
  description, without having the actual required skills, could still get
  a moderate cosine score).
- The skill-overlap ratio (skills found / skills required) is simple,
  transparent, and directly answers the question a student cares about:
  "of the skills this role needs, how many do I actually have?"
- Blending them (60% skill overlap, 40% TF-IDF) keeps the score grounded
  in concrete skill matches while still rewarding broader textual
  relevance (e.g. relevant project descriptions, not just a skills list).
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from text_cleaner import clean_resume_text

SKILL_OVERLAP_WEIGHT = 0.6
TFIDF_WEIGHT = 0.4


def load_job_roles(csv_path: str = "data/job_roles.csv") -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["required_skills_list"] = df["required_skills"].apply(
        lambda s: [skill.strip().lower() for skill in s.split(",")]
    )
    return df


def _skill_overlap_score(found_skills: list, required_skills: list) -> float:
    """Fraction of a role's required skills that were found in the resume."""
    if not required_skills:
        return 0.0
    found_lower = {s.lower() for s in found_skills}
    matched = [s for s in required_skills if s in found_lower]
    return len(matched) / len(required_skills)


def match_resume_to_roles(resume_text: str, found_skills: list, job_roles: pd.DataFrame) -> pd.DataFrame:
    """Score the resume against every job role and return a ranked DataFrame.

    Returns columns: role, match_score (0-100), skill_overlap_score,
    tfidf_score, matched_skills, missing_skills -- sorted by match_score
    descending.
    """
    cleaned_resume = clean_resume_text(resume_text)

    # Build one "role document" per role (required skills + description) so
    # TF-IDF has enough text to compute a meaningful similarity, not just a
    # short skills list.
    role_documents = (
        job_roles["required_skills"] + " " + job_roles["description"]
    ).apply(clean_resume_text).tolist()

    documents = [cleaned_resume] + role_documents
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0:1]
    role_vectors = tfidf_matrix[1:]
    tfidf_scores = cosine_similarity(resume_vector, role_vectors).flatten()

    rows = []
    for i, (_, role_row) in enumerate(job_roles.iterrows()):
        required = role_row["required_skills_list"]
        overlap_score = _skill_overlap_score(found_skills, required)
        tfidf_score = float(tfidf_scores[i])

        final_score = SKILL_OVERLAP_WEIGHT * overlap_score + TFIDF_WEIGHT * tfidf_score
        final_score_pct = round(final_score * 100, 1)

        found_lower = {s.lower() for s in found_skills}
        matched_skills = [s for s in required if s in found_lower]
        missing_skills = [s for s in required if s not in found_lower]

        rows.append({
            "role": role_row["role"],
            "match_score": final_score_pct,
            "skill_overlap_score": round(overlap_score * 100, 1),
            "tfidf_score": round(tfidf_score * 100, 1),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        })

    result_df = pd.DataFrame(rows).sort_values("match_score", ascending=False).reset_index(drop=True)
    return result_df


def recommend_top_roles(match_results: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """Return the top-N ranked roles (already sorted by match_resume_to_roles)."""
    return match_results.head(top_n)


if __name__ == "__main__":
    from skill_extractor import load_skill_dictionary, extract_skills

    job_roles = load_job_roles()
    skill_dict = load_skill_dictionary()

    sample_resume = """
    Experienced in Python, Machine Learning, scikit-learn, Pandas, and SQL.
    Built REST APIs with FastAPI and containerized services with Docker.
    """
    extracted = extract_skills(sample_resume, skill_dict)
    results = match_resume_to_roles(sample_resume, extracted["flat_list"], job_roles)
    print(results[["role", "match_score", "skill_overlap_score", "tfidf_score"]])
    print()
    print("Top 3 recommended roles:")
    print(recommend_top_roles(results)[["role", "match_score"]])
