import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

steps = [
    ("Upload PDF/DOCX Resume", "app.py (Streamlit)"),
    ("Extract Resume Text", "resume_parser.py"),
    ("Detect Resume Sections\n(Education, Skills, Experience, Projects)", "section_detector.py"),
    ("Clean & Normalize Text", "text_cleaner.py"),
    ("Identify Skills\n(keyword matching)", "skill_extractor.py + skill_dictionary.csv"),
    ("Load Job-Role Requirements", "job_matcher.py + job_roles.csv"),
    ("Compare Resume vs. Each Role\n(TF-IDF + cosine similarity\n+ skill overlap)", "job_matcher.py"),
    ("Calculate Match Scores\n& Rank Roles", "job_matcher.py"),
    ("Recommend Top Roles", "app.py"),
    ("Show Missing Skills\n& Learning Roadmap", "roadmap_generator.py"),
    ("Streamlit Dashboard\n+ Downloadable Report", "app.py"),
]

fig, ax = plt.subplots(figsize=(7.5, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, len(steps) * 2 + 1)
ax.axis("off")

box_w, box_h = 7.5, 1.3
x_center = 5

y_positions = []
for i, (title, module) in enumerate(steps):
    y = len(steps) * 2 - i * 2
    y_positions.append(y)
    box = FancyBboxPatch(
        (x_center - box_w / 2, y - box_h / 2), box_w, box_h,
        boxstyle="round,pad=0.08,rounding_size=0.15",
        linewidth=1.5, edgecolor="#1a3d5c", facecolor="#eaf1f8"
    )
    ax.add_patch(box)
    ax.text(x_center, y + 0.18, title, ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1a3d5c")
    ax.text(x_center, y - 0.35, module, ha="center", va="center", fontsize=8.5, color="#555555", style="italic")

    if i > 0:
        y_prev = y_positions[i - 1]
        arrow = FancyArrowPatch(
            (x_center, y_prev - box_h / 2), (x_center, y + box_h / 2),
            arrowstyle="-|>", mutation_scale=18, linewidth=1.5, color="#2c5a7c"
        )
        ax.add_patch(arrow)

ax.set_title("AI Resume Analyzer — Architecture & Workflow", fontsize=14, fontweight="bold", color="#1a3d5c", pad=20)

plt.tight_layout()
plt.savefig("architecture_diagram.png", dpi=150, bbox_inches="tight")
print("Diagram saved.")
