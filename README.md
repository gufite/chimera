# Project Chimera

**Autonomous Influencer Network** — Agentic infrastructure for creating, governing,
and scaling AI-powered digital entities.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/protocol-MCP-green.svg)](https://modelcontextprotocol.io/)

---

## Overview

Project Chimera is a production-grade infrastructure for building autonomous AI
influencers—digital entities that research trends, generate content, and manage
engagement without human intervention.

### Key Features

- **FastRender Swarm Architecture**: Hierarchical Planner-Worker-Judge pattern
- **Model Context Protocol (MCP)**: Universal interface for external systems
- **Human-in-the-Loop (HITL)**: Confidence-based dynamic routing
- **Agentic Commerce**: Crypto wallet integration via Coinbase AgentKit

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                            │
│                                                             │
│    GlobalState → PLANNER → WORKERS → JUDGE → Approve/HITL  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ MCP Protocol
┌─────────────────────────────────────────────────────────────┐
│  Twitter MCP │ Weaviate MCP │ Coinbase MCP │ News MCP      │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/gufite/chimera.git
cd chimera

# Install dependencies with uv
uv sync

# Or with pip
pip install -e ".[dev]"
```

### Development

```bash
# Run tests
uv run pytest

# Format code
uv run ruff format .

# Type checking
uv run mypy src/
```

---

## Project Structure

```
chimera/
├── .cursor/              # IDE configuration & agent rules
│   ├── mcp.json          # MCP server configuration
│   └── rules/            # Agent operating rules
├── src/chimera/          # Main package
├── research/             # Research artifacts
│   ├── research_summary.md
│   ├── analysis.md
│   └── architecture_strategy.md
├── reports/              # Submission reports
├── specs/                # Specifications (GitHub Spec Kit)
├── skills/               # Agent skill definitions
├── tests/                # Test suite
├── pyproject.toml        # Project configuration
└── README.md
```

---

## Documentation

- [Research Summary](research/research_summary.md)
- [Architecture Strategy](research/architecture_strategy.md)
- [Analysis](research/analysis.md)

---

## Development Status

🚧 **Pre-Alpha** — Specification and infrastructure phase

### Roadmap

- [x] Task 1.1: Deep Research & Reading
- [x] Task 1.2: Domain Architecture Strategy
- [x] Task 1.3: Golden Environment Setup
- [ ] Task 2.1: Master Specification
- [ ] Task 2.2: Context Engineering
- [ ] Task 2.3: Tooling & Skills Strategy
- [ ] Task 3.1: Test-Driven Development
- [ ] Task 3.2: Containerization
- [ ] Task 3.3: CI/CD & Governance

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Ten Academy](https://10academy.org/) — FDE Training Program
- [a16z AI Infrastructure Research](https://a16z.com/)
