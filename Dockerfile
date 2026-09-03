# Dockerfile for the Streamlit dashboard (app.py).
#
# Build:  docker build -t resume-analyzer-app .
# Run:    docker run -p 8501:8501 resume-analyzer-app
# Then open http://localhost:8501
#
# NOTE: this image was written and reviewed carefully but could not be
# built/tested in the development sandbox (no Docker daemon available
# there) -- please build and run it yourself and report back if
# anything needs adjusting.

FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (separate layer) so Docker can cache this
# step and skip reinstalling on every code change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code and reference data.
COPY . .

EXPOSE 8501

# Streamlit-specific flags: headless (no browser auto-open inside the
# container) and bind to all interfaces so the port mapping works.
ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.headless=true"]
