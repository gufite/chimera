# Project Chimera - Containerized Development & Test Environment
# Python 3.11 slim base for minimal image size
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv (official installation method)
# Ref: https://docs.astral.sh/uv/getting-started/installation/
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first (cache-friendly layering)
# README.md is required by hatchling during package build
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv
# Include dev dependencies (pytest, etc.)
RUN uv sync --frozen --all-extras

# Copy project files
COPY . .

# Ensure src/chimera is in PYTHONPATH
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Default command: run tests
# Use the virtual environment directly
CMD [".venv/bin/pytest", "-v"]
