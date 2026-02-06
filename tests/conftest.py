"""
Pytest configuration and shared fixtures for Project Chimera tests.

Fixtures provide:
- Mock MCP clients
- Sample data contracts (Agent, Campaign, Task, Result Artifact)
- Mock Persona (SOUL.md) objects
- Correlation ID generators
"""

import uuid
from datetime import UTC, datetime
from typing import Any

import pytest


@pytest.fixture
def correlation_id() -> str:
    """Generate a unique correlation ID for tracing."""
    return str(uuid.uuid4())


@pytest.fixture
def mock_agent() -> dict[str, Any]:
    """Mock Agent data contract per specs/technical.md §3.1"""
    return {
        "agent_id": str(uuid.uuid4()),
        "name": "TestAgent",
        "persona_ref": "/personas/test_persona.md",
        "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        "status": "active",
        "created_at": datetime.now(UTC).isoformat(),
        "config": {},
    }


@pytest.fixture
def mock_persona() -> dict[str, Any]:
    """Mock Persona (SOUL.md) data contract per specs/technical.md §3.2"""
    return {
        "name": "Test Tech Analyst",
        "id": "test-analyst-001",
        "backstory": "A data-driven technology analyst focused on AI/ML trends.",
        "voice_traits": ["analytical", "data-driven", "concise"],
        "directives": [
            "cite sources when making claims",
            "avoid hype and speculation",
            "focus on actionable insights",
        ],
        "core_beliefs": [
            "Technology should empower humans",
            "Transparency builds trust",
        ],
    }


@pytest.fixture
def mock_campaign(mock_agent) -> dict[str, Any]:
    """Mock Campaign data contract per specs/technical.md §3.3"""
    return {
        "campaign_id": str(uuid.uuid4()),
        "goal_description": "Analyze and explain new AI regulations to startup founders",
        "agent_ids": [mock_agent["agent_id"]],
        "priority": "high",
        "budget_allocation": {"daily_limit_usd": 50.0, "per_task_limit_usd": 5.0},
        "status": "active",
        "created_at": datetime.now(UTC).isoformat(),
        "created_by": "test_operator",
        "constraints": {
            "platforms": ["twitter", "linkedin"],
            "content_types": ["analysis", "thread"],
        },
    }


@pytest.fixture
def mock_task(mock_campaign) -> dict[str, Any]:
    """Mock Task data contract per specs/technical.md §3.4"""
    return {
        "task_id": str(uuid.uuid4()),
        "campaign_id": mock_campaign["campaign_id"],
        "task_type": "generate_content",
        "priority": "high",
        "status": "pending",
        "context": {
            "goal": "Create analysis post about EU AI Act impact on startups",
            "persona_constraints": {"persona_ref": "/personas/test_persona.md"},
            "target_platforms": ["twitter"],
        },
        "acceptance_criteria": [
            "Content aligns with persona voice",
            "Content includes source citations",
            "Content length appropriate for platform",
        ],
        "assigned_worker_id": None,
        "created_at": datetime.now(UTC).isoformat(),
        "deadline": None,
        "retry_count": 0,
        "max_retries": 3,
    }


@pytest.fixture
def mock_result_artifact(mock_task) -> dict[str, Any]:
    """Mock Result Artifact data contract per specs/technical.md §3.5"""
    return {
        "result_id": str(uuid.uuid4()),
        "task_id": mock_task["task_id"],
        "worker_id": "worker-001",
        "artifact_type": "content",
        "content": {
            "text": "The EU AI Act establishes a risk-based framework...",
            "media_refs": [],
            "hashtags": ["#AIRegulation", "#EUAIAct"],
        },
        "confidence_score": 0.85,
        "tool_usage": [
            {
                "tool_name": "text_completion",
                "input_params": {"prompt": "Analyze EU AI Act"},
                "output_summary": "Generated analysis",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        ],
        "provenance": {"memory_refs": [], "signal_refs": ["trend-eu-ai-act-001"]},
        "created_at": datetime.now(UTC).isoformat(),
        "execution_duration_ms": 2340,
    }


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client for testing skills that call MCP Tools/Resources."""

    class MockMCPClient:
        def __init__(self):
            self.calls = []

        def call_tool(self, tool_name: str, params: dict[str, Any]) -> dict[str, Any]:
            """Mock MCP Tool call."""
            self.calls.append({"tool": tool_name, "params": params})
            return {"status": "success", "result": f"Mock result from {tool_name}"}

        def read_resource(self, resource_uri: str) -> dict[str, Any]:
            """Mock MCP Resource read."""
            self.calls.append({"resource": resource_uri})
            return {"status": "success", "data": f"Mock data from {resource_uri}"}

    return MockMCPClient()
