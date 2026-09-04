FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
WORKDIR /code
# Add virtual environment to PATH so that we can use the installed dependencies
ENV PATH="/code/.venv/bin:$PATH"
COPY pyproject.toml .python-version uv.lock README.md ./
COPY src/pipeline/ ./src/pipeline/
# Virtual environment using the uv.lock file to ensure reproducible builds
RUN uv sync --locked
COPY pipeline.py .
ENTRYPOINT ["python", "pipeline.py"]