# Skill: Fetch Trends

> **Skill ID:** `skill_fetch_trends`  
> **Version:** 1.0.0  
> **Status:** Contract Defined (Not Implemented)  
> **Owner:** FDE Trainee (Lead Architect)

---

## 1. Purpose

Aggregate trending topics, hashtags, and mentions from multiple MCP Resources
(news APIs, social signals) and rank them by relevance to the agent's persona
and current campaign goals.

This skill provides the **perception layer** for content planning by translating
raw external signals into actionable trend metadata that the Planner can use
for task prioritization.

---

## 2. Invocation Context

### Who Calls This Skill?

- **Primary:** Worker Agents executing `task_type: fetch_signals` tasks
- **Secondary:** Planner (for re-planning triggers when context drift occurs)

### When Is It Called?

- Periodic perception loops (e.g., every 15 minutes per campaign)
- On-demand when Planner detects stale context
- After campaign initialization (bootstrap trending context)

### Invocation Pattern

```python
# Pseudo-invocation (implementation detail)
result = skill_fetch_trends.execute(
    correlation_id="<uuid>",
    agent_id="<uuid>",
    campaign_id="<uuid>",
    persona_constraints=<Persona>,
    time_window_hours=24,
    max_trends=10
)
```

---

## 3. Input Contract

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `correlation_id` | UUID | Trace ID for audit and observability |
| `agent_id` | UUID | Agent requesting trends (for persona filtering) |
| `campaign_id` | UUID | Campaign context (for goal relevance scoring) |
| `persona_constraints` | Object | Reference to Persona (SOUL.md) for filtering |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `time_window_hours` | Integer | 24 | How far back to look for trends |
| `max_trends` | Integer | 10 | Maximum number of trends to return |
| `platforms` | List[String] | `["twitter", "news"]` | Which MCP Resources to query |
| `language` | String | `"en"` | Language filter for trends |
| `geo_region` | String | `null` | Geographic filter (ISO country code) |

### Input Shape (JSON-like)

```json
{
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "123e4567-e89b-12d3-a456-426614174000",
  "campaign_id": "789e0123-e89b-12d3-a456-426614174999",
  "persona_constraints": {
    "persona_ref": "/personas/tech_analyst.md",
    "voice_traits": ["analytical", "data-driven"],
    "directives": ["focus on AI/ML topics"]
  },
  "time_window_hours": 48,
  "max_trends": 15,
  "platforms": ["twitter", "news", "reddit"],
  "language": "en"
}
```

---

## 4. Output Contract

### Success Output

| Field | Type | Description |
|-------|------|-------------|
| `status` | Enum | `"success"` |
| `trends` | List[TrendObject] | Ranked list of trends |
| `metadata` | Object | Execution metadata |

#### TrendObject Schema

| Field | Type | Description |
|-------|------|-------------|
| `trend_id` | String | Unique identifier (hash of topic + timestamp) |
| `topic` | String | The trending topic or hashtag |
| `relevance_score` | Float | 0.0–1.0 score based on persona/goal alignment |
| `volume` | Integer | Mention count in time window |
| `sentiment` | Enum | `positive`, `neutral`, `negative` |
| `sources` | List[String] | Which platforms/resources detected this |
| `sample_posts` | List[String] | Up to 3 example posts/headlines |
| `detected_at` | Timestamp | When this trend was detected |

#### Metadata Schema

| Field | Type | Description |
|-------|------|-------------|
| `sources_queried` | List[String] | MCP Resources successfully queried |
| `sources_failed` | List[String] | MCP Resources that failed |
| `total_signals_processed` | Integer | Raw signal count before filtering |
| `execution_duration_ms` | Integer | Time taken |

### Success Output Shape (JSON-like)

```json
{
  "status": "success",
  "trends": [
    {
      "trend_id": "ai-regulation-2026-02-06T12:00:00Z",
      "topic": "AI regulation debate",
      "relevance_score": 0.92,
      "volume": 45200,
      "sentiment": "neutral",
      "sources": ["twitter", "news"],
      "sample_posts": [
        "Breaking: EU finalizes AI Act enforcement timeline",
        "Tech leaders respond to new AI safety framework",
        "#AIRegulation trending as companies adjust policies"
      ],
      "detected_at": "2026-02-06T12:00:00Z"
    }
  ],
  "metadata": {
    "sources_queried": ["twitter", "news", "reddit"],
    "sources_failed": [],
    "total_signals_processed": 152340,
    "execution_duration_ms": 2340
  }
}
```

### Failure Output

| Field | Type | Description |
|-------|------|-------------|
| `status` | Enum | `"failure"` |
| `error_code` | String | Typed error identifier |
| `error_message` | String | Human-readable error |
| `retry_eligible` | Boolean | Can this be retried? |
| `metadata` | Object | Partial execution metadata |

### Failure Output Shape (JSON-like)

```json
{
  "status": "failure",
  "error_code": "MCP_RESOURCE_UNAVAILABLE",
  "error_message": "All configured MCP Resources failed to respond",
  "retry_eligible": true,
  "metadata": {
    "sources_queried": ["twitter", "news"],
    "sources_failed": ["twitter", "news"],
    "execution_duration_ms": 5000
  }
}
```

---

## 5. MCP Dependencies

### MCP Resources Used

| Resource Type | Purpose | Required |
|---------------|---------|----------|
| `news/trends` | News headline trends | Yes (1+) |
| `twitter/search` | Twitter trending topics | No |
| `reddit/trending` | Reddit front-page topics | No |

### MCP Tools Used

None (this skill only reads; it does not perform actions).

### Fallback Strategy

- If all MCP Resources fail: Return `retry_eligible: true` failure.
- If ≥1 MCP Resource succeeds: Return partial results with `sources_failed` populated.
- If Persona filtering yields zero results: Return empty `trends: []` with `status: "success"`.

---

## 6. Preconditions & Constraints

### Preconditions

1. **Persona must be valid:** `persona_constraints.persona_ref` must point to a parseable SOUL.md file.
2. **Campaign must be active:** `campaign_id` must reference an active campaign (status not `cancelled` or `completed`).
3. **At least 1 MCP Resource configured:** System must have ≥1 news/trends MCP Resource available.

### Constraints

1. **No direct API calls:** This skill MUST use MCP Resources only; direct API calls to Twitter/news APIs are PROHIBITED.
2. **Stateless execution:** This skill MUST NOT persist state; it returns trends and exits.
3. **Timeout:** Execution MUST complete within 10 seconds or raise `TIMEOUT` error.
4. **Relevance filtering:** Trends MUST be filtered by persona directives before ranking.

---

## 7. Failure Modes

### Retryable Failures

| Error Code | Description | Retry Strategy |
|------------|-------------|----------------|
| `MCP_RESOURCE_UNAVAILABLE` | All MCP Resources failed | Exponential backoff (5s, 10s, 20s) |
| `MCP_RATE_LIMIT` | Rate limit exceeded on MCP Resource | Wait + retry after rate limit reset |
| `TIMEOUT` | Execution exceeded 10 seconds | Immediate retry (may succeed faster) |

### Terminal Failures

| Error Code | Description | Resolution |
|------------|-------------|------------|
| `INVALID_PERSONA` | Persona file missing or unparseable | Fix persona file; re-queue task |
| `CAMPAIGN_INACTIVE` | Campaign is cancelled or completed | Do not retry; task is invalid |
| `NO_MCP_RESOURCES` | No MCP Resources configured in system | Configuration error; escalate |

---

## 8. Observability

### Required Audit Events

Every invocation MUST emit the following audit events:

1. **Skill Invocation Start**
   - `correlation_id`, `agent_id`, `campaign_id`, `timestamp`
   - Event type: `skill.fetch_trends.start`

2. **MCP Resource Query** (per resource)
   - `correlation_id`, `resource_name`, `query_params`, `timestamp`
   - Event type: `skill.fetch_trends.mcp_query`

3. **Skill Invocation Complete**
   - `correlation_id`, `status`, `trends_count`, `duration_ms`, `timestamp`
   - Event type: `skill.fetch_trends.complete`

### Correlation ID Propagation

- The `correlation_id` provided as input MUST be:
  - Included in ALL audit events
  - Passed to ALL MCP Resource calls (if MCP supports it)
  - Returned in the output metadata

### Metrics

Recommended metrics to track (implementation detail):

- `skill_fetch_trends_duration_seconds` (histogram)
- `skill_fetch_trends_success_rate` (counter)
- `skill_fetch_trends_mcp_failures` (counter by resource)
- `skill_fetch_trends_relevance_score` (histogram)

---

## 9. Traceability to Specifications

| Specification Section | Relevance |
|-----------------------|-----------|
| `specs/functional.md` §3.2 | Defines Perception & Signal Intake functional behavior |
| `specs/technical.md` §3.4 | Defines Task data contract (consumed by this skill) |
| `specs/technical.md` §8.2 | Defines MCP Resource integration requirements |
| `specs/_meta.md` §4.3 | Defines Skills vs. Tools invariants |
| `research/architecture_strategy.md` §5 | Defines MCP Hub-and-Spoke topology |

---

## 10. Open Questions & Future Enhancements

- **Q1:** Should this skill cache trends for N minutes to reduce MCP Resource load?
  - **Status:** Deferred; implement cache in v2 if needed.

- **Q2:** Should relevance scoring use embeddings (vector similarity)?
  - **Status:** Deferred to `research/open_questions.md` §TBD.

- **Q3:** Should this skill compose a `skill_filter_persona_relevance` sub-skill?
  - **Status:** Consider in refactoring phase.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-06 | FDE Trainee | Initial contract definition |
