"""
skill_extractor.py

Identifies technical skills present in cleaned resume text, using a
controlled skill dictionary (data/skill_dictionary.csv) with keyword
matching. Each skill can have one or more aliases (e.g. "ml" for
"machine learning") so common abbreviations are also detected.

This is the "beginner approach" (keyword matching) specified in the
assignment; spaCy/LLM-based extraction is listed there as an optional
advanced improvement, not a requirement.
"""

import re
import pandas as pd

from text_cleaner import clean_resume_text


def load_skill_dictionary(csv_path: str = "data/skill_dictionary.csv") -> pd.DataFrame:
    """Load the controlled skill list. Missing aliases are treated as empty."""
    df = pd.read_csv(csv_path)
    df["aliases"] = df["aliases"].fillna("")
    return df


def _normalize_term(term: str) -> str:
    """Apply the same hyphen/punctuation normalization that text_cleaner applies
    to resume text, so dictionary terms like "scikit-learn" (hyphen) correctly
    match cleaned text where the hyphen has become a space ("scikit learn").
    Preserved technical symbols (+, #, ., /) are left untouched.
    """
    return re.sub(r"[^a-z0-9\s+#./]", " ", term.lower()).strip()


def _build_skill_pattern(term: str) -> re.Pattern:
    """Build a word-boundary-safe regex for a single skill term.

    Standard \\b word boundaries don't work well with terms containing
    symbols like "c++" or ".net" (since \\b is defined around word
    characters), so boundaries are only required on sides that are
    alphanumeric; symbol-adjacent terms rely on whitespace/string edges
    instead, which is safe because the text has already been cleaned
    and whitespace-normalized by text_cleaner.
    """
    term = re.sub(r"\s+", " ", _normalize_term(term)).strip()
    escaped = re.escape(term)
    left = r"(?<![a-z0-9])" if term[0].isalnum() else r"(?<!\S)"
    right = r"(?![a-z0-9])" if term[-1].isalnum() else r"(?!\S)"
    return re.compile(left + escaped + right)


def extract_skills(resume_text: str, skill_dict: pd.DataFrame) -> dict:
    """Search cleaned resume text for every skill (and its aliases).

    Returns a dict: {category: [skill, skill, ...]} for skills found,
    covering every category present in the dictionary (empty categories
    are included as empty lists so the dashboard can show them cleanly).
    """
    cleaned = clean_resume_text(resume_text)

    found_by_category = {cat: [] for cat in skill_dict["category"].unique()}
    found_flat = []

    for _, row in skill_dict.iterrows():
        skill = row["skill"].strip().lower()
        category = row["category"]
        terms_to_check = [skill]
        if row["aliases"]:
            terms_to_check += [a.strip().lower() for a in row["aliases"].split(";") if a.strip()]

        matched = any(_build_skill_pattern(term).search(cleaned) for term in terms_to_check)
        if matched:
            found_by_category[category].append(row["skill"])
            found_flat.append(row["skill"])

    return {
        "by_category": found_by_category,
        "flat_list": sorted(set(found_flat)),
    }


if __name__ == "__main__":
    skill_dict = load_skill_dictionary()
    sample_resume = """
    Experienced developer skilled in Python, Pandas, SQL, and scikit-learn.
    Familiar with Docker and basic ML workflows. Built REST APIs with FastAPI.
    """
    result = extract_skills(sample_resume, skill_dict)
    print("Flat skill list:", result["flat_list"])
    print()
    for cat, skills in result["by_category"].items():
        if skills:
            print(f"{cat}: {skills}")
