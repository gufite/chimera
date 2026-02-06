# Skill: Publish Content

> **Skill ID:** `skill_publish_content`  
> **Version:** 1.0.0  
> **Status:** Contract Defined (Not Implemented)  
> **Owner:** FDE Trainee (Lead Architect)

---

## 1. Purpose

Coordinate multi-platform content publishing by orchestrating MCP Tool calls
to social media platforms (Twitter, Instagram, LinkedIn, TikTok, YouTube).

This skill handles the **execution workflow** of approved content bundles,
including:
- Platform authentication and authorization checks
- Sequential or parallel publishing across platforms
- Error handling and partial success scenarios
- Publication record creation for audit and engagement tracking

**Critical Governance Note:** This skill MUST ONLY be invoked AFTER Judge
approval. Direct invocation without Judge validation is a violation of
`specs/_meta.md` §5.3.

---

## 2. Invocation Context

### Who Calls This Skill?

- **Primary:** Worker Agents executing `task_type: publish_content` tasks
- **NEVER:** Planner (Planner plans; Workers execute)
- **NEVER:** Judge (Judge validates; Workers publish)

### When Is It Called?

- After Judge approves a Result Artifact containing a content bundle
- After HITL reviewer approves escalated content
- Only when `status: approved` or `status: approved_with_edit` in Review Item

### Invocation Pattern

```python
# Pseudo-invocation (implementation detail)
result = skill_publish_content.execute(
    correlation_id="<uuid>",
    task_id="<uuid>",
    agent_id="<uuid>",
    campaign_id="<uuid>",
    content_bundle=<ContentBundle>,
    target_platforms=["twitter", "instagram"],
    idempotency_key="<unique-key>"
)
```

---

## 3. Input Contract

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `correlation_id` | UUID | Trace ID for audit and observability |
| `task_id` | UUID | Originating task (from Planner) |
| `agent_id` | UUID | Agent publishing content (for account mapping) |
| `campaign_id` | UUID | Campaign context (for budget tracking) |
| `content_bundle` | Object | Approved content bundle with platform variants |
| `target_platforms` | List[String] | Platforms to publish to |
| `idempotency_key` | String | Unique key to prevent duplicate posts |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `publish_strategy` | Enum | `"sequential"` | `"sequential"`, `"parallel"` |
| `partial_success_allowed` | Boolean | `true` | Proceed if some platforms succeed? |
| `schedule_time` | Timestamp | `null` | Future publish time (null = immediate) |
| `dry_run` | Boolean | `false` | Simulate publishing without actually posting |

### Content Bundle Schema (Input)

| Field | Type | Description |
|-------|------|-------------|
| `bundle_id` | UUID | Identifier from `skill_generate_post_bundle` |
| `variants` | List[ContentVariant] | Platform-specific content |
| `approval_record` | Object | Judge/HITL approval metadata |

### Input Shape (JSON-like)

```json
{
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "123e4567-e89b-12d3-a456-426614174002",
  "agent_id": "123e4567-e89b-12d3-a456-426614174000",
  "campaign_id": "789e0123-e89b-12d3-a456-426614174999",
  "content_bundle": {
    "bundle_id": "bundle-550e8400-e29b-41d4-a716-446655440001",
    "variants": [
      {
        "platform": "twitter",
        "text_content": "The EU AI Act creates a tiered risk framework...",
        "media_refs": ["https://media.chimera.ai/gen/ai-act-001.png"],
        "hashtags": ["#AIRegulation"],
        "disclosure_label": "AI-generated content"
      }
    ],
    "approval_record": {
      "approved_by": "judge",
      "approved_at": "2026-02-06T12:10:00Z",
      "confidence_score": 0.87
    }
  },
  "target_platforms": ["twitter"],
  "idempotency_key": "publish-550e8400-twitter-2026-02-06",
  "publish_strategy": "sequential"
}
```

---

## 4. Output Contract

### Success Output

| Field | Type | Description |
|-------|------|-------------|
| `status` | Enum | `"success"`, `"partial_success"`, `"failure"` |
| `publications` | List[PublicationResult] | Per-platform results |
| `metadata` | Object | Execution metadata |

#### PublicationResult Schema

| Field | Type | Description |
|-------|------|-------------|
| `platform` | String | Platform name (`"twitter"`, `"instagram"`) |
| `status` | Enum | `"published"`, `"failed"`, `"skipped"` |
| `external_id` | String | Platform post ID (e.g., tweet ID) |
| `external_url` | String | Public URL to the post |
| `published_at` | Timestamp | When the post went live |
| `error_code` | String | If failed, error code |
| `error_message` | String | If failed, human-readable error |

### Success Output Shape (JSON-like)

```json
{
  "status": "success",
  "publications": [
    {
      "platform": "twitter",
      "status": "published",
      "external_id": "1755123456789012345",
      "external_url": "https://twitter.com/chimera_agent/status/1755123456789012345",
      "published_at": "2026-02-06T12:15:30Z",
      "error_code": null,
      "error_message": null
    }
  ],
  "metadata": {
    "idempotency_key": "publish-550e8400-twitter-2026-02-06",
    "total_platforms": 1,
    "successful_platforms": 1,
    "failed_platforms": 0,
    "execution_duration_ms": 1200
  }
}
```

### Partial Success Output Shape

```json
{
  "status": "partial_success",
  "publications": [
    {
      "platform": "twitter",
      "status": "published",
      "external_id": "1755123456789012345",
      "external_url": "https://twitter.com/chimera_agent/status/1755123456789012345",
      "published_at": "2026-02-06T12:15:30Z"
    },
    {
      "platform": "instagram",
      "status": "failed",
      "external_id": null,
      "external_url": null,
      "published_at": null,
      "error_code": "PLATFORM_RATE_LIMIT",
      "error_message": "Instagram API rate limit exceeded"
    }
  ],
  "metadata": {
    "total_platforms": 2,
    "successful_platforms": 1,
    "failed_platforms": 1,
    "execution_duration_ms": 3400
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
| `publications` | List[PublicationResult] | Per-platform results (all failed) |

---

## 5. MCP Dependencies

### MCP Tools Used

| Tool Type | Purpose | Required |
|-----------|---------|----------|
| `post_tweet` | Publish to Twitter/X | Yes (if `"twitter"` in targets) |
| `post_instagram` | Publish to Instagram | Yes (if `"instagram"` in targets) |
| `post_linkedin` | Publish to LinkedIn | Yes (if `"linkedin"` in targets) |
| `upload_media` | Upload images/videos to platforms | Yes (if media in bundle) |

### MCP Resources Used

None (this skill performs actions; it does not read external data).

### Idempotency Requirements

- Each platform MCP Tool MUST support idempotency keys.
- If a tool is called with the same `idempotency_key` twice, it MUST NOT create a duplicate post.
- The skill MUST pass `idempotency_key` to every MCP Tool call.

---

## 6. Preconditions & Constraints

### Preconditions

1. **Content must be approved:** `content_bundle.approval_record.approved_by` must be `"judge"` or `"hitl_reviewer"`.
2. **Platforms must be configured:** Target platforms MUST have MCP Tools configured and authenticated.
3. **Media must be accessible:** All URLs in `media_refs` MUST be reachable by MCP Tools.
4. **Budget must be available:** Publishing costs (API calls) MUST be within campaign budget.

### Constraints

1. **No direct API calls:** This skill MUST use MCP Tools only; direct platform API calls are PROHIBITED.
2. **Judge bypass is forbidden:** This skill MUST NOT be invoked without prior Judge approval (architectural invariant).
3. **Idempotency is mandatory:** Every publication MUST use an idempotency key to prevent duplicates.
4. **Disclosure labels:** All posts MUST include disclosure labels per `content_bundle.variants[].disclosure_label`.
5. **Timeout:** Per-platform publishing MUST complete within 10 seconds or raise `TIMEOUT` error.

---

## 7. Postconditions

### Upon Successful Execution

This skill guarantees:

1. **Output artifacts created:** A success Result containing PublicationResult objects for each target platform with `external_id`, `external_url`, and `published_at` timestamps.
2. **Audit trail complete:** All required audit events emitted (`skill.publish_content.start`, `skill.publish_content.attempt`, `skill.publish_content.success`, `skill.publish_content.complete`) with `correlation_id` propagated.
3. **State changes:** 
   - Publication Record created in PostgreSQL with `publication_id`, `external_id`, `content_snapshot`, `published_at`
   - Campaign budget decremented (API call costs)
4. **External system state:** Content published to target platforms (persistent, public posts created).

### Upon Failure

This skill guarantees:

1. **No partial state:** 
   - If `partial_success_allowed: false`, attempts to rollback published posts (platform-dependent)
   - If `partial_success_allowed: true`, partial Publication Records created only for successful platforms
2. **Audit trail:** Failure events emitted with platform-specific error details (`skill.publish_content.failure` per platform).
3. **Idempotency preserved:** `idempotency_key` ensures retry will not create duplicate posts.
4. **Error propagation:** Failure output includes per-platform `retry_eligible` flags and error codes for Planner recovery.

### Partial Success Handling

When `partial_success_allowed: true` and ≥1 platform succeeds:

1. **State consistency:** Publication Records created only for successful platforms.
2. **Audit clarity:** Both success and failure events emitted (per-platform).
3. **Retry guidance:** Failed platforms listed in output for selective retry.

---

## 8. Failure Modes

### Retryable Failures

| Error Code | Description | Retry Strategy |
|------------|-------------|----------------|
| `PLATFORM_RATE_LIMIT` | Platform rate limit exceeded | Wait + retry after rate limit reset |
| `PLATFORM_TRANSIENT_ERROR` | 5xx error from platform API | Exponential backoff (5s, 10s, 20s) |
| `MEDIA_UPLOAD_FAILED` | Media upload to platform failed | Retry media upload only |
| `TIMEOUT` | Execution exceeded 10 seconds per platform | Immediate retry |

### Terminal Failures

| Error Code | Description | Resolution |
|------------|-------------|------------|
| `PLATFORM_AUTH_INVALID` | Authentication credentials expired/invalid | Re-authenticate platform; escalate |
| `CONTENT_POLICY_VIOLATION` | Platform rejected content (policy violation) | Escalate to HITL; do not retry |
| `PLATFORM_UNAVAILABLE` | Platform API is down (confirmed outage) | Wait for platform recovery; escalate |
| `NO_APPROVAL_RECORD` | Content bundle missing approval metadata | Invalid invocation; do not retry |
| `MEDIA_NOT_ACCESSIBLE` | Media URLs return 404 or 403 | Fix media storage; re-queue task |

### Partial Success Handling

- If `partial_success_allowed: true` AND ≥1 platform succeeds:
  - Return `status: "partial_success"`
  - Log failed platforms in `publications[]`
  - Planner SHOULD create retry tasks for failed platforms

- If `partial_success_allowed: false` AND any platform fails:
  - Rollback published posts if possible (platform-dependent)
  - Return `status: "failure"`
  - Planner SHOULD retry entire task

---

## 9. Observability

### Required Audit Events

Every invocation MUST emit the following audit events:

1. **Skill Invocation Start**
   - `correlation_id`, `task_id`, `agent_id`, `campaign_id`, `platforms`, `timestamp`
   - Event type: `skill.publish_content.start`

2. **Publication Attempt** (per platform)
   - `correlation_id`, `platform`, `idempotency_key`, `timestamp`
   - Event type: `skill.publish_content.attempt`

3. **Publication Success** (per platform)
   - `correlation_id`, `platform`, `external_id`, `external_url`, `timestamp`
   - Event type: `skill.publish_content.success`

4. **Publication Failure** (per platform)
   - `correlation_id`, `platform`, `error_code`, `error_message`, `timestamp`
   - Event type: `skill.publish_content.failure`

5. **Skill Invocation Complete**
   - `correlation_id`, `status`, `successful_platforms`, `failed_platforms`, `duration_ms`, `timestamp`
   - Event type: `skill.publish_content.complete`

### Correlation ID Propagation

- The `correlation_id` provided as input MUST be:
  - Included in ALL audit events
  - Passed to ALL MCP Tool calls
  - Stored in Publication Records for future engagement tracking

### Publication Record Creation

After successful publication, this skill MUST create a Publication Record:

| Field | Value |
|-------|-------|
| `publication_id` | Generated UUID |
| `task_id` | From input |
| `campaign_id` | From input |
| `platform` | From publication result |
| `external_id` | From publication result |
| `content_snapshot` | Full content published |
| `published_at` | From publication result |
| `correlation_id` | From input |

This record is stored in the system of record (PostgreSQL) for engagement tracking.

---

## 10. Traceability to Specifications

| Specification Section | Relevance |
|-----------------------|-----------|
| `specs/functional.md` §3.7 | Defines Publishing & Engagement functional behavior |
| `specs/technical.md` §3.7 | Defines Publication Record data contract |
| `specs/technical.md` §5 | Defines Worker contract and allowed actions |
| `specs/technical.md` §6 | Defines Judge contract (must approve before publishing) |
| `specs/technical.md` §8.4 | Defines MCP Tools integration (idempotency, error semantics) |
| `specs/_meta.md` §5.3 | Defines Judge as governance gate (architectural invariant) |
| `specs/technical.md` §9 | Defines safety and trust boundaries |

---

## 11. Security & Governance Notes

### Critical Security Constraints

1. **Never bypass Judge:** This skill MUST verify `approval_record` exists and is valid before publishing.
2. **Sanitize untrusted input:** If content includes user mentions or external links, sanitize for injection attacks.
3. **Rate limit enforcement:** Respect platform rate limits to avoid account suspension.
4. **Secret management:** Platform credentials MUST be injected via MCP Tool configuration, NEVER hardcoded.

### Audit Requirements

- Every published post MUST be traceable to:
  - Originating campaign
  - Originating task
  - Judge approval decision
  - Human reviewer (if HITL)

- The audit trail MUST survive system restarts (persistent storage).

---

## 12. Open Questions & Future Enhancements

- **Q1:** Should this skill support scheduled publishing (future timestamps)?
  - **Status:** Yes, via `schedule_time` field; implementation deferred to v2.

- **Q2:** Should this skill handle "unpublish" or "delete post" workflows?
  - **Status:** Separate skill (`skill_unpublish_content`) recommended; ADR needed.

- **Q3:** Should this skill support cross-posting with platform-specific edits (e.g., add Instagram-specific hashtags)?
  - **Status:** Yes, via `content_bundle.variants[]`; already supported in contract.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-06 | FDE Trainee | Initial contract definition |
