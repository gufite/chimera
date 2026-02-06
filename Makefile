# Project Chimera - Build Automation Makefile
# Task 3.2: Containerization & Automation

.PHONY: help test test-verbose test-coverage docker-build docker-test docker-shell clean format lint

# Default target
help:
	@echo "Project Chimera - Available Make Targets:"
	@echo ""
	@echo "  Local Development:"
	@echo "    make test              - Run tests quietly"
	@echo "    make test-verbose      - Run tests with verbose output"
	@echo "    make test-coverage     - Run tests with coverage report"
	@echo "    make format            - Format code with ruff"
	@echo "    make lint              - Lint code with ruff and mypy"
	@echo "    make clean             - Remove cache and build artifacts"
	@echo ""
	@echo "  Docker:"
	@echo "    make docker-build      - Build Docker image (chimera:dev)"
	@echo "    make docker-test       - Run tests inside Docker container"
	@echo "    make docker-shell      - Open interactive shell in container"
	@echo ""

# Local test commands
test:
	uv run pytest -q

test-verbose:
	uv run pytest -v

test-coverage:
	uv run pytest --cov=src/chimera --cov-report=term-missing --cov-report=html

# Code quality
format:
	uv run ruff format .

lint:
	uv run ruff check .
	uv run mypy src/

# Docker commands
docker-build:
	docker build -t chimera:dev .

docker-test:
	docker run --rm chimera:dev

docker-shell:
	docker run --rm -it chimera:dev /bin/bash

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo "✓ Cleaned cache and build artifacts"
