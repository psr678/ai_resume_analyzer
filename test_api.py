"""
Manual test of api.py using FastAPI's TestClient (in-process, no network
needed) against the real sample resumes.
"""

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

# 1. Health check
resp = client.get("/health")
print("GET /health ->", resp.status_code, resp.json())
assert resp.status_code == 200

# 2. Job roles list
resp = client.get("/job-roles")
print("GET /job-roles ->", resp.status_code, resp.json())
assert resp.status_code == 200
assert "Data Analyst" in resp.json()["roles"]

# 3. Analyze a real sample resume
with open("sample_resumes/resume_B_ml_engineer.pdf", "rb") as f:
    resp = client.post(
        "/analyze",
        files={"file": ("resume_B_ml_engineer.pdf", f, "application/pdf")},
    )
print("POST /analyze ->", resp.status_code)
data = resp.json()
print("  Top recommended roles:", data["top_recommended_roles"])
print("  Skills found:", data["skills_found"])
print("  Detected sections:", data["detected_sections"])
assert resp.status_code == 200
assert data["top_recommended_roles"][0] == "Machine Learning Engineer"

# 4. Roadmap for a target role using the skills just found
skills_csv = ",".join(data["skills_found"])
resp = client.get(f"/roadmap/Machine Learning Engineer?skills_found={skills_csv}")
print("GET /roadmap/... ->", resp.status_code)
roadmap_data = resp.json()
print("  Missing skills:", roadmap_data["missing_skills"])
print("  Roadmap text:\n" + roadmap_data["roadmap_text"])
assert resp.status_code == 200

# 5. Error handling: unsupported file type
resp = client.post(
    "/analyze",
    files={"file": ("resume.txt", b"not a real resume", "text/plain")},
)
print("POST /analyze (bad file type) ->", resp.status_code, resp.json())
assert resp.status_code == 400

# 6. Error handling: unknown role
resp = client.get("/roadmap/Not A Real Role")
print("GET /roadmap/(unknown role) ->", resp.status_code)
assert resp.status_code == 404

print("\nALL API TESTS PASSED")
