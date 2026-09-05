# Start with slim Python 3.13 image for smaller size
FROM python:3.13.11-slim

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory inside container
WORKDIR /app

# Add virtual environment to PATH so that we can use the installed dependencies
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better caching)
COPY pyproject.toml .python-version uv.lock README.md ./
COPY src/pipeline/ ./src/pipeline/

# Virtual environment using the uv.lock file to ensure reproducible builds
RUN uv sync --locked

# Copy ingestion script
COPY ingest_data.py ingest_data.py 

# Set entry point to run the ingestion script
ENTRYPOINT [ "python", "ingest_data.py" ]