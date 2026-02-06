# Skill: Generate Post Bundle

> **Skill ID:** `skill_generate_post_bundle`  
> **Version:** 1.0.0  
> **Status:** Contract Defined (Not Implemented)  
> **Owner:** FDE Trainee (Lead Architect)

---

## 1. Purpose

Generate a complete content bundle for publication, including:
- Primary text content (caption, tweet, post body)
- Media references (images, videos generated or selected)
- Platform-specific variants (Twitter 280 chars vs Instagram long-form)
- Metadata (hashtags, mentions, alt-text, disclosure labels)

This skill orchestrates content generation by composing persona constraints,
campaign goals, and trend context into platform-ready artifacts that the Judge
can validate before publication.

---

## 2. Invocation Context

### Who Calls This Skill?

- **Primary:** Worker Agents executing `task_type: generate_content` tasks
- **Secondary:** Worker Agents executing `task_type: reply_comment` tasks (generates reply bundles)

### When Is It Called?

- After Planner assigns a content generation task based on trending topics
- When responding to mentions or comments (reactive content)
- During scheduled content calendar execution (proactive content)

### Invocation Pattern

```python
# Pseudo-invocation (implementation detail)
result = skill_generate_post_bundle.execute(
    correlation_id="<uuid>",
    task_id="<uuid>",
    agent_id="<uuid>",
    campaign_id="<uuid>",
    persona_constraints=<Persona>,
    content_prompt="<natural language goal>",
    target_platforms=["twitter", "instagram"],
    media_generation_enabled=True
)
```

---

## 3. Input Contract

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `correlation_id` | UUID | Trace ID for audit and observability |
| `task_id` | UUID | Originating task (from Planner) |
| `agent_id` | UUID | Agent generating content (for persona application) |
| `campaign_id` | UUID | Campaign context (for goal alignment) |
| `persona_constraints` | Object | Reference to Persona (SOUL.md) for voice/style |
| `content_prompt` | String | Natural language description of what to create |
| `target_platforms` | List[String] | Platforms to generate variants for |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `media_generation_enabled` | Boolean | `true` | Whether to generate/include media |
| `media_type` | Enum | `"auto"` | `"image"`, `"video"`, `"none"`, `"auto"` |
| `max_variants` | Integer | 3 | Max platform variants to generate |
| `tone_override` | String | `null` | Override persona tone (e.g., "urgent", "celebratory") |
| `context_signals` | List[TrendObject] | `[]` | Relevant trends to reference |
| `referenced_content` | Object | `null` | If replying, the original post/comment |

### Input Shape (JSON-like)

```json
{
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "123e4567-e89b-12d3-a456-426614174001",
  "agent_id": "123e4567-e89b-12d3-a456-426614174000",
  "campaign_id": "789e0123-e89b-12d3-a456-426614174999",
  "persona_constraints": {
    "persona_ref": "/personas/tech_analyst.md",
    "voice_traits": ["analytical", "data-driven"],
    "directives": ["cite sources", "avoid hype"]
  },
  "content_prompt": "Create a post analyzing the new EU AI regulation and its impact on startups",
  "target_platforms": ["twitter", "linkedin"],
  "media_generation_enabled": true,
  "media_type": "image",
  "context_signals": [
    {
      "topic": "EU AI Act",
      "relevance_score": 0.95,
      "sentiment": "neutral"
    }
  ]
}
```

---

## 4. Output Contract

### Success Output

| Field | Type | Description |
|-------|------|-------------|
| `status` | Enum | `"success"` |
| `bundle_id` | UUID | Unique identifier for this content bundle |
| `variants` | List[ContentVariant] | Platform-specific content versions |
| `confidence_score` | Float | 0.0–1.0 self-assessment of quality/safety |
| `tool_usage` | List[ToolCall] | MCP Tools invoked (for provenance) |
| `metadata` | Object | Execution metadata |

#### ContentVariant Schema

| Field | Type | Description |
|-------|------|-------------|
| `platform` | String | Target platform (`"twitter"`, `"instagram"`, `"linkedin"`) |
| `text_content` | String | Primary text (caption, tweet body) |
| `media_refs` | List[String] | URLs or IDs of generated/selected media |
| `hashtags` | List[String] | Recommended hashtags |
| `mentions` | List[String] | User mentions (if applicable) |
| `alt_text` | List[String] | Alt text for media (accessibility) |
| `disclosure_label` | String | Required disclosure (e.g., "AI-generated content") |
| `character_count` | Integer | Text length (for platform limits) |

#### ToolCall Schema

| Field | Type | Description |
|-------|------|-------------|
| `tool_name` | String | MCP Tool invoked (e.g., `"generate_image"`) |
| `input_params` | Object | Inputs sent to tool |
| `output_summary` | String | Brief summary of tool output |
| `timestamp` | Timestamp | When tool was called |

### Success Output Shape (JSON-like)

```json
{
  "status": "success",
  "bundle_id": "bundle-550e8400-e29b-41d4-a716-446655440001",
  "variants": [
    {
      "platform": "twitter",
      "text_content": "The EU AI Act creates a tiered risk framework for AI systems. Startups building low-risk tools face minimal compliance, but high-risk apps (e.g., hiring, credit scoring) require extensive documentation. Thread 🧵",
      "media_refs": ["https://media.chimera.ai/gen/ai-act-infographic-001.png"],
      "hashtags": ["#AIRegulation", "#EUAIAct", "#TechPolicy"],
      "mentions": [],
      "alt_text": ["Infographic showing EU AI Act risk tiers"],
      "disclosure_label": "AI-generated content",
      "character_count": 278
    },
    {
      "platform": "linkedin",
      "text_content": "The EU AI Act is now in force, establishing the world's first comprehensive regulatory framework for artificial intelligence...\n\n[Full analysis with 3 key takeaways for founders]",
      "media_refs": ["https://media.chimera.ai/gen/ai-act-infographic-002.png"],
      "hashtags": ["#AIRegulation", "#Startups"],
      "mentions": [],
      "alt_text": ["Detailed infographic of EU AI Act compliance requirements"],
      "disclosure_label": "AI-assisted analysis",
      "character_count": 1240
    }
  ],
  "confidence_score": 0.87,
  "tool_usage": [
    {
      "tool_name": "generate_image",
      "input_params": {
        "prompt": "Clean infographic showing EU AI Act risk tiers",
        "style": "professional"
      },
      "output_summary": "Generated 2 infographic variants",
      "timestamp": "2026-02-06T12:05:30Z"
    }
  ],
  "metadata": {
    "execution_duration_ms": 4200,
    "llm_model_used": "gpt-4-turbo",
    "total_tokens": 1850
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
| `partial_output` | Object | Any partial content generated before failure |

---

## 5. MCP Dependencies

### MCP Tools Used

| Tool Type | Purpose | Required |
|-----------|---------|----------|
| `generate_image` | Create infographics, illustrations | No (depends on `media_generation_enabled`) |
| `generate_video` | Create short video clips | No (depends on `media_type`) |
| `text_completion` | LLM for content generation | Yes |

### MCP Resources Used

None (this skill generates content; it does not fetch external data).

### Fallback Strategy

- If `generate_image` fails: Generate text-only variant and set `media_refs: []`.
- If LLM fails: Retry once; if still fails, return terminal failure.
- If persona file cannot be loaded: Return terminal failure `INVALID_PERSONA`.

---

## 6. Preconditions & Constraints

### Preconditions

1. **Persona must be valid:** `persona_constraints.persona_ref` must point to a parseable SOUL.md file.
2. **Campaign must be active:** `campaign_id` must reference an active campaign.
3. **Content prompt must be non-empty:** `content_prompt` must contain ≥10 characters.

### Constraints

1. **No direct API calls:** This skill MUST use MCP Tools only; direct calls to OpenAI/Ideogram are PROHIBITED.
2. **Persona adherence:** Generated content MUST align with persona `voice_traits` and `directives`.
3. **Platform limits:** Text content MUST respect platform character limits (Twitter 280, Instagram 2200).
4. **Disclosure labels:** All AI-generated content MUST include disclosure per platform policies.
5. **Timeout:** Execution MUST complete within 30 seconds or raise `TIMEOUT` error.

---

## 7. Postconditions

### Upon Successful Execution

This skill guarantees:

1. **Output artifacts created:** A ContentBundle with `bundle_id`, platform-specific variants, `confidence_score`, and complete `tool_usage` provenance.
2. **Audit trail complete:** All required audit events emitted (`skill.generate_post_bundle.start`, `skill.generate_post_bundle.mcp_call`, `skill.generate_post_bundle.variant_complete`, `skill.generate_post_bundle.complete`) with `correlation_id` propagated.
3. **State changes:** No persistent state mutations (stateless execution).
4. **External system state:** MCP Tools invoked (LLM, media generation); API call counts incremented; generated media stored at referenced URLs.

### Upon Failure

This skill guarantees:

1. **No partial state:** No partial content bundles persisted; skill exits cleanly.
2. **Audit trail:** Failure events emitted with error details and partial execution metadata.
3. **Idempotency preserved:** Generated media URLs are deterministic or cleaned up on failure (MCP Tool-dependent).
4. **Error propagation:** Failure output includes `retry_eligible` flag and `partial_output` for debugging.

---

## 8. Failure Modes

### Retryable Failures

| Error Code | Description | Retry Strategy |
|------------|-------------|----------------|
| `MCP_TOOL_UNAVAILABLE` | LLM or media generation tool unavailable | Exponential backoff (5s, 10s, 20s) |
| `MCP_RATE_LIMIT` | Rate limit exceeded on MCP Tool | Wait + retry after rate limit reset |
| `TIMEOUT` | Execution exceeded 30 seconds | Immediate retry |
| `CONTENT_QUALITY_LOW` | Generated content confidence <0.5 | Retry with adjusted prompt |

### Terminal Failures

| Error Code | Description | Resolution |
|------------|-------------|------------|
| `INVALID_PERSONA` | Persona file missing or unparseable | Fix persona file; re-queue task |
| `CAMPAIGN_INACTIVE` | Campaign is cancelled or completed | Do not retry; task is invalid |
| `PROMPT_UNSAFE` | Content prompt violates safety policies | Escalate to HITL; do not retry |
| `NO_MCP_TOOLS` | No LLM tools configured | Configuration error; escalate |

---

## 9. Observability

### Required Audit Events

Every invocation MUST emit the following audit events:

1. **Skill Invocation Start**
   - `correlation_id`, `task_id`, `agent_id`, `campaign_id`, `timestamp`
   - Event type: `skill.generate_post_bundle.start`

2. **MCP Tool Call** (per tool)
   - `correlation_id`, `tool_name`, `input_params_summary`, `timestamp`
   - Event type: `skill.generate_post_bundle.mcp_call`

3. **Content Generation Complete** (per variant)
   - `correlation_id`, `platform`, `character_count`, `confidence_score`, `timestamp`
   - Event type: `skill.generate_post_bundle.variant_complete`

4. **Skill Invocation Complete**
   - `correlation_id`, `status`, `variants_count`, `confidence_score`, `duration_ms`, `timestamp`
   - Event type: `skill.generate_post_bundle.complete`

### Correlation ID Propagation

- The `correlation_id` provided as input MUST be:
  - Included in ALL audit events
  - Passed to ALL MCP Tool calls
  - Returned in the output metadata

### Provenance Logging

- The `tool_usage` field MUST capture:
  - Every MCP Tool invoked
  - Inputs sent (sanitized; no secrets)
  - Outputs received (summary)
  - Timestamps for each call

---

## 10. Security & Trust Boundaries

### Trust Boundaries

- **Input trust:** All inputs from Planner/Worker are considered **TRUSTED** (internal agent state).
- **Persona trust:** Persona (SOUL.md) content is **TRUSTED** (version-controlled, reviewed).
- **Generated content trust:** Content generated by LLM is **UNTRUSTED** until validated by Judge.
- **MCP Tool isolation:** All LLM and media generation access MUST go through MCP Tools (no direct API calls).

### Security Constraints

1. **No direct API calls:** Direct external API calls to OpenAI/Ideogram are PROHIBITED (architectural invariant per `specs/_meta.md` §4.3).
2. **Credential isolation:** No API keys or secrets in skill code; authentication handled by MCP Tool layer.
3. **Input validation:**
   - Validate `persona_ref` points to parseable SOUL.md file
   - Validate `content_prompt` is non-empty and within length limits
   - Sanitize `context_signals` from external trends before injection into prompts
4. **Output validation:**
   - Generated content MUST include disclosure labels (platform policy compliance)
   - Generated content MUST respect platform character limits
   - Generated content MUST NOT contain secrets, credentials, or PII
5. **Prompt injection prevention:**
   - Treat `content_prompt` and `context_signals` as data, not instructions
   - Use structured prompts with clear boundaries between system/user content
   - Validate persona directives are enforced in generation

### Threat Mitigation

- **Prompt injection via trends:** External trend data is sanitized and clearly marked as untrusted in LLM prompts.
- **Unsafe content generation:** Confidence scoring and Judge validation provide defense-in-depth.
- **PII leakage:** No agent internal state (API keys, wallet addresses) included in generation context.
- **Cost/resource exhaustion:** Timeout enforcement (30 seconds) and MCP Tool rate limits prevent abuse.

---

## 11. Traceability to Specifications

| Specification Section | Relevance |
|-----------------------|-----------|
| `specs/functional.md` §3.4 | Defines Task Execution functional behavior |
| `specs/technical.md` §3.5 | Defines Result Artifact data contract (output of this skill) |
| `specs/technical.md` §5 | Defines Worker contract and allowed actions |
| `specs/technical.md` §8.3 | Defines MCP Tools integration requirements |
| `specs/_meta.md` §4.3 | Defines Skills vs. Tools invariants |
| `specs/technical.md` §9 | Defines safety and trust boundaries |

---

## 12. Open Questions & Future Enhancements

- **Q1:** Should this skill support multi-turn content refinement (generate → critique → regenerate)?
  - **Status:** Deferred to v2; current version is single-pass.

- **Q2:** Should persona voice be enforced via prompt injection or post-generation validation?
  - **Status:** Hybrid: prompt injection for generation, Judge validation for enforcement.

- **Q3:** Should this skill compose sub-skills (e.g., `skill_format_for_platform`)?
  - **Status:** Consider during refactoring if duplication emerges.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-06 | FDE Trainee | Initial contract definition |
