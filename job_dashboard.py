"""
job_dashboard.py

Optional advanced feature: a job-role dashboard with charts, independent
of any uploaded resume -- lets a student explore the reference data
itself (which roles need the most skills, which skill categories matter
most for which roles) before or instead of uploading a resume.

Fully offline: builds charts directly from data/job_roles.csv and
data/skill_dictionary.csv, no external service required.
"""

import pandas as pd
import plotly.express as px


def build_role_skill_counts(job_roles: pd.DataFrame) -> pd.DataFrame:
    """One row per role: how many required skills it lists."""
    counts = job_roles["required_skills_list"].apply(len)
    return pd.DataFrame({
        "role": job_roles["role"],
        "required_skill_count": counts,
    }).sort_values("required_skill_count", ascending=False)


def build_role_category_matrix(job_roles: pd.DataFrame, skill_dict: pd.DataFrame) -> pd.DataFrame:
    """Long-form DataFrame: role, category, count -- how many of a role's
    required skills fall into each skill category (Programming, Cloud, etc).
    Used to build a stacked bar chart per role.
    """
    skill_to_category = dict(zip(skill_dict["skill"].str.lower(), skill_dict["category"]))

    rows = []
    for _, role_row in job_roles.iterrows():
        role = role_row["role"]
        category_counts = {}
        for skill in role_row["required_skills_list"]:
            category = skill_to_category.get(skill.lower(), "Other")
            category_counts[category] = category_counts.get(category, 0) + 1
        for category, count in category_counts.items():
            rows.append({"role": role, "category": category, "count": count})

    return pd.DataFrame(rows)


def figure_required_skill_counts(job_roles: pd.DataFrame):
    counts_df = build_role_skill_counts(job_roles)
    fig = px.bar(
        counts_df.sort_values("required_skill_count"),
        x="required_skill_count", y="role", orientation="h",
        labels={"required_skill_count": "Number of Required Skills", "role": "Job Role"},
        title="Required Skill Count by Job Role",
    )
    return fig


def figure_role_category_breakdown(job_roles: pd.DataFrame, skill_dict: pd.DataFrame):
    matrix_df = build_role_category_matrix(job_roles, skill_dict)
    fig = px.bar(
        matrix_df, x="role", y="count", color="category",
        labels={"count": "Number of Required Skills", "role": "Job Role", "category": "Skill Category"},
        title="Skill Category Composition by Job Role",
    )
    fig.update_layout(xaxis_tickangle=-30)
    return fig


if __name__ == "__main__":
    from job_matcher import load_job_roles
    from skill_extractor import load_skill_dictionary

    job_roles = load_job_roles()
    skill_dict = load_skill_dictionary()

    counts = build_role_skill_counts(job_roles)
    print(counts)
    print()
    matrix = build_role_category_matrix(job_roles, skill_dict)
    print(matrix.head(15))
