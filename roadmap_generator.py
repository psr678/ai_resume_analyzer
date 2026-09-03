"""
roadmap_generator.py

Generates a simple, rule-based weekly learning roadmap for the skills
missing from a resume relative to a selected target role. This is the
"beginner approach" (rule-based roadmap) specified in the assignment;
an LLM-generated roadmap is listed there only as an optional advanced
improvement.

Responsible AI note: this roadmap is a generic, skill-based learning
suggestion. It does not claim that completing it guarantees a job offer,
and it explicitly avoids implying that missing keywords equal missing
ability -- see the disclaimer text returned alongside the roadmap.
"""

# A short, curated learning-topic hint per skill. Not exhaustive -- any
# missing skill not listed here still gets a roadmap entry via the
# generic fallback message, so the roadmap never silently drops a skill.
LEARNING_HINTS = {
    "python": "Core Python syntax, data structures, and writing clean functions.",
    "sql": "SQL fundamentals: SELECT/JOIN/GROUP BY queries and basic schema design.",
    "excel": "Excel formulas, pivot tables, and basic data cleaning.",
    "power bi": "Building interactive dashboards and DAX basics in Power BI.",
    "pandas": "DataFrame operations: filtering, grouping, merging, and cleaning data.",
    "numpy": "Array operations and vectorized computation with NumPy.",
    "machine learning": "Core ML concepts: train/test splits, overfitting, common algorithms.",
    "scikit-learn": "Building and evaluating models with scikit-learn's estimator API.",
    "fastapi": "Building and documenting REST APIs with FastAPI.",
    "docker": "Containerizing an application with a Dockerfile and running it locally.",
    "mlflow": "Tracking experiments and model versions with MLflow.",
    "deep learning": "Neural network fundamentals: layers, activation functions, backpropagation.",
    "pytorch": "Building and training a basic neural network in PyTorch.",
    "tensorflow": "Building and training a basic neural network in TensorFlow/Keras.",
    "nlp": "Text preprocessing, tokenization, and basic NLP pipelines.",
    "transformers": "Using pretrained transformer models for text tasks.",
    "hugging face": "Loading and fine-tuning models from the Hugging Face Hub.",
    "spacy": "Named entity recognition and text processing with spaCy.",
    "opencv": "Basic image processing operations with OpenCV.",
    "cnn": "Convolutional neural network fundamentals for image tasks.",
    "yolo": "Object detection basics using a YOLO model.",
    "llm": "How large language models work and how to call them via an API.",
    "rag": "Retrieval-augmented generation: combining search with an LLM.",
    "aws": "Core AWS services: S3, EC2, and IAM basics.",
    "azure": "Core Azure services and basic cloud deployment.",
    "gcp": "Core Google Cloud services and basic cloud deployment.",
    "kubernetes": "Container orchestration basics: pods, deployments, services.",
    "cloud deployment": "Deploying a simple app to a cloud platform end-to-end.",
    "ci/cd": "Setting up an automated build/test/deploy pipeline.",
    "django": "Building a basic web application with Django.",
    "flask": "Building a lightweight REST API with Flask.",
    "rest apis": "Designing and consuming RESTful APIs.",
    "apis": "Working with third-party APIs: authentication, requests, and responses.",
    "git": "Version control basics: commits, branches, and pull requests.",
    "github": "Collaborating on GitHub: issues, pull requests, and Actions.",
    "postgresql": "Relational database design and queries with PostgreSQL.",
    "mongodb": "Document database basics with MongoDB.",
}

DEFAULT_HINT = "Review the fundamentals and build one small practice project using this skill."


def generate_roadmap(missing_skills: list, weeks_per_skill_group: int = 1) -> list:
    """Turn a list of missing skills into a week-by-week roadmap.

    Groups skills one (or more) per week, in the order given (callers
    should pass missing_skills already ordered by importance/priority
    if that matters for their use case).

    Returns a list of dicts: [{"week": 1, "skills": [...], "focus": "..."}]
    """
    if not missing_skills:
        return []

    roadmap = []
    for week_index, i in enumerate(range(0, len(missing_skills), weeks_per_skill_group), start=1):
        week_skills = missing_skills[i:i + weeks_per_skill_group]
        hints = [f"{skill}: {LEARNING_HINTS.get(skill.lower(), DEFAULT_HINT)}" for skill in week_skills]
        roadmap.append({
            "week": week_index,
            "skills": week_skills,
            "focus": " | ".join(hints),
        })
    return roadmap


def format_roadmap_text(roadmap: list) -> str:
    """Human-readable multi-line roadmap, matching the example output style
    in the assignment PDF ('Week 1: FastAPI basics', etc.)."""
    if not roadmap:
        return "No missing skills identified for this role -- great match!"

    lines = []
    for entry in roadmap:
        skills_str = ", ".join(entry["skills"])
        lines.append(f"Week {entry['week']}: {skills_str}")
    return "\n".join(lines)


ROADMAP_DISCLAIMER = (
    "This roadmap is a generic starting point based on missing keywords, not a "
    "guarantee of readiness or employability. Missing a keyword does not always "
    "mean missing ability -- you may already have equivalent experience under a "
    "different name. Use this as a starting point for further learning, not a "
    "final judgment."
)


if __name__ == "__main__":
    missing = ["fastapi", "docker", "mlflow", "cloud deployment"]
    roadmap = generate_roadmap(missing)
    print(format_roadmap_text(roadmap))
    print()
    print(ROADMAP_DISCLAIMER)
