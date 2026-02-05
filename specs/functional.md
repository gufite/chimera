# Project Chimera — Functional Specification

> **Status:** DRAFT  
> **Version:** 0.2.0  
> **Last Updated:** 2026-02-05  
> **Owner:** FDE Trainee (Lead Architect)  
> **Subordinate To:** `specs/_meta.md`

This document specifies WHAT Project Chimera must do (behaviors and acceptance
criteria), without prescribing HOW it is implemented. All requirements are
grounded in the Project Chimera SRS and constrained by the governance rules
defined in `specs/_meta.md`.

---

## 1. Overview

### 1.1 System Purpose

Project Chimera is an **Autonomous Influencer Network**—a software system that
produces, governs, and scales AI-powered digital entities capable of:

- Researching trends and generating content ideas
- Creating multi-modal content (text, image, video)
- Engaging with audiences on social platforms
- Executing economic transactions via crypto wallets
- Participating in agent social networks

The system enables a single human operator (or small team) to manage a fleet of
potentially thousands of autonomous influencer agents through a **Fractal
Orchestration** model. Fractal Orchestration applies the **Hierarchical Swarm
(FastRender) pattern** at multiple scales: a human Super-Orchestrator manages
AI Manager Agents, who in turn direct specialized Worker Swarms. At each level,
the Planner → Worker → Judge structure repeats, enabling human intervention by
exception rather than by rule.

### 1.2 Definition of Correct Behavior

The system exhibits correct behavior when:

1. **Goals are achieved** — Operator-defined campaign objectives are pursued
   through coordinated agent activity.
2. **Governance is enforced** — All outputs MUST pass through Judge validation
   before reaching external systems; sensitive or uncertain content MUST be
   escalated to HITL.
3. **Persona is preserved** — Each agent maintains consistent identity, voice,
   and values across all interactions.
4. **Costs are controlled** — Spending remains within configured budget limits;
   runaway costs are prevented.
5. **Actions are auditable** — Every significant decision and external action
   is logged with sufficient context for retrospective review.
6. **External interactions are mediated** — All external system access MUST
   occur exclusively through MCP Tools and Resources; direct API calls are
   PROHIBITED.

### 1.3 Functional Perspective & User Story Mapping

This specification uses **structured functional descriptions** rather than
backlog-style user stories. Each capability is defined by its trigger,
inputs/outputs, success/failure behaviors, and testable acceptance criteria.

For traceability and stakeholder communication, we recognize the canonical
user story form:

> **As a** \<actor\>, **I need to** \<capability\>, **so that** \<outcome\>.

In this document, user stories serve as **labels for behavior**—concise
summaries that orient readers. The **acceptance criteria are the authoritative
contract**; implementation correctness is validated against acceptance criteria,
not user story phrasing.

This approach satisfies the challenge requirement for user stories while
maintaining the rigor expected of a Spec-Driven Development (SDD) workflow.
Representative user stories are included for key capabilities; all capabilities
are defined by their acceptance criteria regardless of whether a user story
callout is present.

---

## 2. Actors and Roles

### 2.1 Human Actors

| Actor | Role | Interaction Mode |
|-------|------|------------------|
| **Network Operator** | Defines campaign goals, monitors fleet health, adjusts strategy | Dashboard, goal composer |
| **Human Reviewer (HITL)** | Reviews escalated content; approves, edits, or rejects | Review queue interface |
| **Developer / Architect** | Extends capabilities, deploys MCP servers, maintains infrastructure | CLI, API, code repository |

### 2.2 Agent Roles (Functional Perspective)

| Role | Functional Responsibility |
|------|---------------------------|
| **Planner** | Receives goals from GlobalState; decomposes into discrete tasks; prioritizes and schedules; monitors progress; re-plans dynamically when context changes |
| **Worker** | Receives a single atomic task; executes using Skills and MCP Tools; returns result artifact; operates statelessly and in isolation from other Workers |
| **Judge** | Receives Worker output; validates against acceptance criteria, persona constraints, and safety rules; routes to auto-approve, HITL queue, or reject/retry |

### 2.3 External Systems (via MCP)

External systems are accessed exclusively through MCP Servers. The system MUST
NOT make direct API calls to external services.

| External Domain | MCP Interface |
|-----------------|---------------|
| Social Platforms (Twitter, Instagram, TikTok) | Platform-specific MCP servers |
| News and Trend Sources | News aggregation MCP server |
| Vector Database (semantic memory) | Database MCP server |
| Blockchain / Wallet | Commerce MCP server |
| Media Generation (image, video) | Creative MCP servers |

---

## 3. Core Functional Capabilities

### 3.1 Campaign / Goal Initialization

**Description:**  
The Operator defines a high-level mission or campaign objective. The system
persists this goal and makes it available to the Planner for decomposition.

**Representative User Story:**  
As a Network Operator, I need to define campaign goals in natural language, so
that the agent fleet pursues my strategic objectives without manual task
assignment.

**Preconditions:**
- Operator is authenticated and authorized
- At least one agent persona is configured

**Trigger:**
- Operator submits a campaign goal via Dashboard

**Inputs:**
- Natural language goal description (e.g., "Promote summer fashion line to Gen-Z audience in Ethiopia")
- Target agent(s) or persona(s)
- Optional: priority level, budget allocation, time constraints

**Outputs:**
- Campaign record persisted in GlobalState
- Planner notified of new goal
- Confirmation displayed to Operator

**Success Criteria:**
- Campaign appears in Dashboard with status "Active"
- Planner begins task decomposition within configured latency window

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| Invalid goal format | Return validation error; do not persist |
| No agent available | Queue goal; notify Operator of pending status |
| Persistence failure | Retry with backoff; escalate to Operator if persistent |

**Acceptance Criteria:**
- [ ] AC-3.1.1: Given a valid goal, the system persists it and returns confirmation within 5 seconds.
- [ ] AC-3.1.2: Given an invalid goal, the system returns a descriptive error without persisting.
- [ ] AC-3.1.3: The persisted goal is visible in the Dashboard fleet view.
- [ ] AC-3.1.4: The Planner receives the goal and creates at least one task within the configured latency window.

---

### 3.2 Perception & Signal Intake

**Description:**  
The system continuously monitors external data sources for relevant signals
(trends, mentions, news) by polling MCP Resources. Signals are filtered for
relevance before triggering planning activity.

**Representative User Story:**  
As a Planner Agent, I need to receive filtered signals from external sources,
so that I can identify opportunities and threats relevant to active campaigns.

**Preconditions:**
- MCP Resource servers are connected and healthy
- Agent has active goals to contextualize relevance

**Trigger:**
- Periodic polling interval elapsed
- External event notification (if supported by MCP server)

**Inputs:**
- MCP Resource URIs (e.g., `twitter://mentions/recent`, `news://trends/fashion`)
- Agent's current goal context
- Relevance threshold configuration

**Outputs:**
- Filtered signal set passed to Planner
- Low-relevance signals discarded (logged for audit)

**Success Criteria:**
- Relevant signals are detected and forwarded to Planner
- Irrelevant noise is filtered out without manual intervention

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| MCP Resource unavailable | Log error; continue with other sources; alert if prolonged |
| Relevance filter fails | Default to conservative (queue for Planner review) |
| Rate limit exceeded | Back off; resume at next interval |

**Acceptance Criteria:**
- [ ] AC-3.2.1: The system polls configured MCP Resources at the specified interval.
- [ ] AC-3.2.2: Signals exceeding the relevance threshold are forwarded to the Planner.
- [ ] AC-3.2.3: Signals below the threshold are logged but not forwarded.
- [ ] AC-3.2.4: MCP Resource failures are logged and do not crash the perception loop.

---

### 3.3 Planning & Task Decomposition

**Description:**  
The Planner receives goals and signals, then decomposes them into discrete,
atomic tasks. Tasks are prioritized and queued for Worker execution. The
Planner dynamically re-plans when context changes (e.g., trend shifts, Worker
failures, budget constraints).

**Preconditions:**
- Active goal exists in GlobalState
- Planner has access to current context (memories, recent signals)

**Trigger:**
- New goal received
- Significant signal detected
- Worker failure requiring re-plan
- Context drift detected (e.g., campaign paused)

**Inputs:**
- Goal description and constraints
- Current GlobalState snapshot
- Available Worker capacity
- Budget remaining

**Outputs:**
- Ordered task queue
- Task records with: type, priority, context, acceptance criteria
- Updated plan visible in Dashboard (optional)

**Success Criteria:**
- Goals are decomposed into executable atomic tasks
- Tasks are prioritized appropriately (high-priority first)
- Re-planning occurs when context invalidates current plan

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| Goal too ambiguous | Request clarification from Operator via Dashboard |
| Budget exhausted | Pause planning; notify Operator |
| Planner overloaded | Queue goals; process in order |

**Acceptance Criteria:**
- [ ] AC-3.3.1: Given a goal, the Planner produces at least one task within the configured latency.
- [ ] AC-3.3.2: Tasks include sufficient context for Worker execution.
- [ ] AC-3.3.3: When a Worker fails, the Planner re-evaluates and may reassign or modify the task.
- [ ] AC-3.3.4: Budget constraints are checked before creating cost-incurring tasks.

---

### 3.4 Task Execution

**Description:**  
Workers receive atomic tasks from the queue and execute them using internal
Skills and external MCP Tools. Workers operate statelessly; each task is
self-contained. Results are submitted to the Judge for validation.

**Representative User Story:**  
As a Worker Agent, I need to execute a single task using Skills and MCP Tools,
so that I produce a result artifact for validation without side effects on
other Workers.

**Preconditions:**
- Task exists in queue with status "pending"
- Required MCP Tools are available
- Required Skills are loaded

**Trigger:**
- Worker pulls task from queue

**Inputs:**
- Task record (type, context, acceptance criteria)
- Access to Skills library
- Access to MCP Tools

**Outputs:**
- Result artifact (content, transaction record, etc.)
- Execution metadata (duration, tools used, confidence score)
- Result submitted to Judge review queue

**Success Criteria:**
- Task is executed according to its type and context
- Result includes confidence score for Judge routing
- Execution completes within timeout

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| MCP Tool unavailable | Fail task; return to Planner for re-queue or alternative |
| Skill execution error | Log error; fail task; Planner decides retry strategy |
| Timeout exceeded | Terminate execution; fail task |
| Worker crash | Task returns to queue; another Worker picks up |

**Acceptance Criteria:**
- [ ] AC-3.4.1: Workers execute tasks without direct communication with other Workers.
- [ ] AC-3.4.2: All external actions MUST occur via MCP Tools; direct API calls are PROHIBITED.
- [ ] AC-3.4.3: Failed tasks are returned to the Planner with failure context.
- [ ] AC-3.4.4: Results include a confidence_score metadata field.

---

### 3.5 Validation & Governance

**Description:**  
The Judge validates all Worker outputs before they reach external systems. The
Judge compares results against acceptance criteria, persona constraints, safety
guidelines, and policy rules. Based on confidence and content analysis, the
Judge routes to auto-approve, HITL queue, or reject.

**Representative User Story:**  
As a Judge Agent, I need to validate every Worker output against policy and
persona rules, so that no content reaches external systems without governance
approval.

**Preconditions:**
- Worker has submitted result to review queue
- Judge has access to persona definition and policy rules
- GlobalState version is current

**Trigger:**
- Result appears in review queue

**Inputs:**
- Worker result artifact
- Confidence score
- Task acceptance criteria
- Agent persona constraints (SOUL.md)
- Safety and policy rules

**Outputs:**
- Routing decision: APPROVE / ESCALATE / REJECT
- For APPROVE: result committed to GlobalState; next action triggered
- For ESCALATE: result added to HITL queue with context
- For REJECT: result discarded; Planner notified for retry

**Success Criteria:**
- All outputs are validated before external publication
- Routing decisions align with configured thresholds and rules
- Optimistic Concurrency Control prevents stale updates

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| State version mismatch (OCC) | Invalidate result; return to Planner |
| Persona constraint violation | Reject; log violation; notify Planner |
| Judge unavailable | Queue results; alert Operator if prolonged |

**Acceptance Criteria:**
- [ ] AC-3.5.1: No Worker output MUST reach external systems without Judge validation.
- [ ] AC-3.5.2: High-confidence, non-sensitive content is auto-approved.
- [ ] AC-3.5.3: Low-confidence or sensitive content MUST be escalated to HITL.
- [ ] AC-3.5.4: State version conflicts result in task invalidation, not corruption.

---

### 3.6 HITL Review Workflow

**Description:**  
When the Judge escalates content, it enters the HITL queue. Human Reviewers
access the queue via Dashboard, review content with context, and take action
(approve, approve-with-edit, reject). The system processes the decision and
resumes workflow.

**Representative User Story:**  
As a Human Reviewer, I need to review escalated content with full context, so
that I can approve, edit, or reject it before publication.

**Preconditions:**
- Content has been escalated by Judge
- Human Reviewer is authenticated and authorized

**Trigger:**
- Reviewer opens HITL queue
- Reviewer takes action on queued item

**Inputs:**
- Escalated content artifact
- Confidence score and reasoning trace
- Relevant context (goal, persona, recent history)

**Outputs:**
- For APPROVE: content proceeds to publication
- For APPROVE-WITH-EDIT: edited content proceeds to publication
- For REJECT: content discarded; Planner notified for retry

**Success Criteria:**
- Reviewers have sufficient context to make informed decisions
- Decisions are processed promptly and workflow resumes
- All decisions are logged for audit

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| Reviewer timeout | Content remains queued; alert sent if SLA exceeded |
| Edit introduces new issues | Re-queue for secondary review (optional) |
| Reviewer unavailable | Queue persists; escalate to Operator if critical |

**Acceptance Criteria:**
- [ ] AC-3.6.1: Escalated content appears in HITL queue with confidence score and context.
- [ ] AC-3.6.2: Reviewer can approve, edit, or reject from the queue interface.
- [ ] AC-3.6.3: Approved content proceeds to the next workflow step.
- [ ] AC-3.6.4: Rejected content triggers Planner re-evaluation.
- [ ] AC-3.6.5: All HITL decisions MUST be logged with reviewer identity and timestamp.

---

### 3.7 Publishing & Engagement

**Description:**  
Approved content is published to external platforms via MCP Tools. The system
also handles engagement actions (replies, reactions) through the same mediated
interface.

**Preconditions:**
- Content has been approved (auto or HITL)
- Target platform MCP server is available
- Agent has valid credentials for target platform

**Trigger:**
- Judge approves content for publication
- Engagement task assigned by Planner

**Inputs:**
- Content artifact (text, media URLs)
- Target platform and account
- Disclosure settings (AI labeling)

**Outputs:**
- Content published to platform
- Platform response (post ID, engagement metrics)
- Publication record logged

**Success Criteria:**
- Content is published to the correct platform and account
- AI disclosure labels are applied where platform supports
- Publication is logged with platform response

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| Platform API error | Retry with backoff; fail task if persistent |
| Rate limit exceeded | Queue for later; respect platform limits |
| Credential invalid | Halt publication for that account; alert Operator |
| Content rejected by platform | Log rejection reason; notify Planner |

**Acceptance Criteria:**
- [ ] AC-3.7.1: All publications MUST occur via MCP Tools; direct API calls are PROHIBITED.
- [ ] AC-3.7.2: AI disclosure flags are set where supported by platform.
- [ ] AC-3.7.3: Publication failures are logged and returned to Planner.
- [ ] AC-3.7.4: Engagement actions (replies, likes) use the same MCP mediation.

---

### 3.8 Memory & Persona Consistency

**Description:**  
The system maintains agent identity through hierarchical memory retrieval and
persona constraints. Short-term memory provides recent context; long-term
semantic memory enables recall of past interactions. The persona definition
(SOUL.md) constrains all generated content.

**Preconditions:**
- Agent persona (SOUL.md) is defined and loaded
- Memory stores (ephemeral and semantic) are available via MCP

**Trigger:**
- Any task requiring content generation or response
- Memory write triggered by successful high-engagement interaction

**Inputs:**
- Current input/context for memory retrieval
- Persona definition
- Memory query parameters

**Outputs:**
- Assembled context (persona + short-term + long-term memories)
- For memory writes: updated semantic memory collection

**Success Criteria:**
- Generated content is consistent with persona voice and values
- Relevant past interactions are recalled when contextually appropriate
- Memory is updated to reflect significant new experiences

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| Memory store unavailable | Proceed with limited context; log degradation |
| Persona file missing | Halt agent; alert Operator |
| Memory retrieval timeout | Use cached/partial results; log |

**Acceptance Criteria:**
- [ ] AC-3.8.1: All content generation includes persona constraints in context.
- [ ] AC-3.8.2: Semantic memory queries return relevant past interactions.
- [ ] AC-3.8.3: High-engagement interactions trigger memory persistence.
- [ ] AC-3.8.4: Persona violations MUST be caught by Judge and rejected.

---

### 3.9 Auditability & Traceability

**Description:**  
Every significant decision, external action, and state change is logged with
sufficient context for retrospective audit. Trace capture mechanisms record
agent reasoning during development.

**Preconditions:**
- Logging infrastructure is operational
- Trace capture mechanism is active during development

**Trigger:**
- Any significant system event (task creation, validation decision, publication, HITL action, transaction)

**Inputs:**
- Event type and timestamp
- Actor (agent role or human)
- Context and inputs
- Decision or outcome

**Outputs:**
- Immutable log record
- Queryable audit trail

**Success Criteria:**
- All significant events are logged
- Logs contain sufficient context for investigation
- Logs are tamper-resistant

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| Logging service unavailable | Buffer locally; retry; alert if prolonged |
| Log storage full | Rotate oldest logs; alert Operator |

**Acceptance Criteria:**
- [ ] AC-3.9.1: Every HITL decision MUST be logged with reviewer, action, and timestamp.
- [ ] AC-3.9.2: Every publication MUST be logged with platform, content ID, and response.
- [ ] AC-3.9.3: Every financial transaction MUST be logged with amount, addresses, and result.
- [ ] AC-3.9.4: Logs are queryable by time range, agent, and event type.
- [ ] AC-3.9.5: A trace capture mechanism MUST be active during development sessions.

---

### 3.10 Budget / Cost Governance

**Description:**  
The system enforces spending limits to prevent runaway costs from AI inference,
media generation, and blockchain transactions. A specialized governance
function (conceptually the "CFO") reviews cost-incurring actions.

**Preconditions:**
- Budget limits are configured (daily, per-task, per-transaction)
- Wallet balance is known

**Trigger:**
- Any task that incurs cost (inference, media generation, transaction)
- Periodic budget reconciliation

**Inputs:**
- Proposed action cost (estimated or actual)
- Current spend against limits
- Wallet balance

**Outputs:**
- For within-budget: action proceeds
- For exceeds-budget: action blocked; Planner notified
- For anomaly detected: action escalated to HITL

**Success Criteria:**
- Spending stays within configured limits
- Budget exhaustion halts cost-incurring activity gracefully
- Anomalous spending patterns are escalated

**Failure Cases:**
| Failure | System Behavior |
|---------|-----------------|
| Budget limit reached | Block action; notify Planner and Operator |
| Cost estimation unavailable | Use conservative estimate or block |
| Wallet balance insufficient | Block transaction; alert Operator |

**Acceptance Criteria:**
- [ ] AC-3.10.1: Actions exceeding configured limits MUST be blocked.
- [ ] AC-3.10.2: Daily spend is tracked and queryable.
- [ ] AC-3.10.3: Transactions above configured threshold MUST require HITL approval.
- [ ] AC-3.10.4: Budget exhaustion triggers graceful degradation, not crash.

**Note:** Specific threshold values (daily limit, per-task limit, transaction
threshold) are defined in `specs/technical.md`. See also
`research/open_questions.md` §4 for per-task limit policy discussion.

---

## 4. Human-in-the-Loop (HITL) Functional Requirements

### 4.1 Confidence-Based Routing

The system MUST route Worker outputs based on confidence score:

| Confidence Level | Routing Behavior |
|------------------|------------------|
| High (above configured threshold) | Auto-approve; proceed to next step |
| Medium (between configured thresholds) | Escalate to HITL queue for async review |
| Low (below configured threshold) | Auto-reject; return to Planner for retry |

**Note:** Specific threshold values (e.g., 0.90, 0.70) are defined in
`specs/technical.md` per SRS §5.1 NFR 1.1.

### 4.2 Sensitive Topic Override

Regardless of confidence score, the following topic categories MUST always
trigger HITL escalation:

- Political content or commentary
- Health or medical advice
- Financial recommendations
- Legal claims or statements
- Content involving minors
- Crisis or emergency situations

The system MUST detect these categories via semantic classification or keyword
matching before routing.

### 4.3 Mandatory HITL Scenarios

The following scenarios MUST require HITL approval regardless of confidence:

| Scenario | Rationale |
|----------|-----------|
| First N posts of a new campaign | Warm-up period to validate persona and strategy |
| Financial transactions above configured threshold | Protect against unauthorized spending |
| Crisis response content | Reputational risk requires human judgment |
| New platform integration (first use) | Validate behavior on unfamiliar platform |

**Note:** The value of N (first posts count) and transaction threshold are
defined in `specs/technical.md`.

### 4.4 Reviewer Actions and System Behavior

| Reviewer Action | System Behavior |
|-----------------|-----------------|
| **Approve** | Content proceeds to publication; logged as human-approved |
| **Approve with Edit** | Edited content replaces original; proceeds to publication |
| **Reject** | Content discarded; Planner notified with rejection reason |
| **Defer** | Content remains in queue; no action taken |

All actions MUST be logged with reviewer identity, timestamp, and any edits
made.

---

## 5. Non-Functional Behaviors Expressed Functionally

### 5.1 Safety Behavior

When uncertainty is high, the system MUST:
- Default to escalation rather than auto-approval
- Provide reasoning trace to human reviewers
- Never publish content that failed validation

When a sensitive topic is detected, the system MUST:
- Override confidence-based routing
- Always escalate to HITL

### 5.2 Reliability Behavior

**Retries:**
- Failed MCP Tool calls SHOULD be retried with exponential backoff
- Retry limits are configured per tool type
- Exhausted retries result in task failure and Planner notification

**Idempotency:**
- Publications SHOULD be idempotent; duplicate calls do not create duplicate posts
- Transactions MUST be idempotent; duplicate calls MUST NOT create duplicate transfers

**Degradation:**
- If a non-critical MCP server is unavailable, the system SHOULD continue with reduced capability
- If a critical MCP server is unavailable, the system SHOULD pause affected workflows and alert Operator

### 5.3 Latency Expectations

| Category | Latency Expectation |
|----------|---------------------|
| High-priority interaction (e.g., DM reply) | Real-time (seconds, per SRS NFR 3.1) |
| Standard content generation | Near-real-time (minutes) |
| HITL-queued content | Async (hours, dependent on reviewer availability) |
| Batch analytics / reporting | Deferred (hours to days) |

### 5.4 Scalability Behavior

**Worker Pool:**
- Workers SHOULD scale horizontally based on queue depth
- New Workers are stateless and can be added without coordination
- Worker failures MUST NOT cascade to other Workers

**Task Queue:**
- The task queue MUST support concurrent access from multiple Workers
- Queue ordering SHOULD respect task priority

---

## 6. Out of Scope

The following are explicitly NOT guaranteed in this release:

| Exclusion | Rationale |
|-----------|-----------|
| General-purpose chatbot functionality | Chimera is a content creator, not a conversational assistant |
| Real-time video streaming | Focus is on pre-produced content |
| Multi-tenant SaaS platform | Initial version serves single operator |
| Mobile application | Human interface is web-only |
| Training custom LLMs | System consumes external models via API |
| Direct API calls to external services | All external access MUST occur via MCP |
| Fully autonomous financial decisions above threshold | HITL required for significant transactions |
| OpenClaw protocol integration (v1.0) | Deferred; see `research/open_questions.md` §2 |

---

## 7. Dependencies and Assumptions

### 7.1 Required MCP Servers (Conceptual)

| Domain | MCP Server Purpose |
|--------|-------------------|
| Social Publishing | Post, reply, react on social platforms |
| Social Perception | Read mentions, timeline, messages |
| News/Trends | Aggregate news feeds, detect trends |
| Semantic Memory | Store and query vector embeddings |
| Transactional Data | Store and query structured business data |
| Commerce/Wallet | Check balance, send transactions |
| Image Generation | Generate images from prompts |
| Video Generation | Generate video from prompts or images |

**Note:** Specific server implementations and availability are tracked in
`specs/technical.md`. See `research/open_questions.md` §5 for build vs. buy
decisions.

### 7.2 Assumptions

1. **MCP Protocol Stability:** The Model Context Protocol is assumed to be
   stable for the duration of development.

2. **External API Availability:** Social platform APIs may change; the MCP
   abstraction layer is expected to absorb these changes.

3. **LLM Availability:** Frontier LLMs (per SRS §2.3) are available via API
   with acceptable latency and cost.

4. **Operator Engagement:** At least one human is available to monitor the
   Dashboard and respond to HITL escalations within configured SLA.

5. **Blockchain Selection:** The target blockchain for financial transactions
   is assumed to be Base (per SRS §4.5 examples); see
   `research/open_questions.md` §1.

### 7.3 Open Questions Impact

The following functional areas are partially deferred pending resolution of
open questions:

| Functional Area | Open Question Reference |
|-----------------|-------------------------|
| Blockchain transactions | `research/open_questions.md` §1 — Blockchain Selection |
| Agent network participation | `research/open_questions.md` §2 — OpenClaw Protocol Version |
| HITL threshold defaults | Resolved by SRS §5.1 NFR 1.1; captured in `specs/technical.md` |
| Per-task budget limits | `research/open_questions.md` §4 — Budget Governor Limits |
| MCP server availability | `research/open_questions.md` §5 — Build vs. Buy |

---

## 8. Traceability Map

| Functional Capability | SRS Section | Architecture/Research Reference |
|-----------------------|-------------|--------------------------------|
| 3.1 Campaign / Goal Initialization | SRS §2.2, §6.1 UI 1.1 | Architecture Strategy §1 |
| 3.2 Perception & Signal Intake | SRS §4.2 FR 2.0–2.2 | Architecture Strategy §5 (MCP) |
| 3.3 Planning & Task Decomposition | SRS §3.1.1, §4.6 FR 6.0 | Architecture Strategy §1 |
| 3.4 Task Execution | SRS §3.1.2, §4.6 FR 6.0 | Architecture Strategy §1 |
| 3.5 Validation & Governance | SRS §3.1.3, §4.6 FR 6.1 | Architecture Strategy §1 |
| 3.6 HITL Review Workflow | SRS §5.1 NFR 1.0–1.2 | Architecture Strategy §2 |
| 3.7 Publishing & Engagement | SRS §4.4 FR 4.0–4.1 | Architecture Strategy §5 (MCP) |
| 3.8 Memory & Persona Consistency | SRS §4.1 FR 1.0–1.2 | Architecture Strategy §3 |
| 3.9 Auditability & Traceability | SRS §2.4, _meta.md §4.2 | Research Summary §2 |
| 3.10 Budget / Cost Governance | SRS §4.5 FR 5.2 | Architecture Strategy §6 |
| 4. HITL Requirements | SRS §5.1, §2.2 | Architecture Strategy §2 |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Campaign** | A high-level goal or mission assigned to one or more agents |
| **Fractal Orchestration** | Management model where the Hierarchical Swarm pattern repeats at multiple scales (human → managers → workers) |
| **GlobalState** | The shared state repository containing goals, context, and configuration |
| **Hierarchical Swarm (FastRender)** | Agent coordination pattern with Planner, Worker, and Judge roles |
| **HITL** | Human-in-the-Loop; human oversight mechanism for uncertain or sensitive content |
| **MCP** | Model Context Protocol; standard interface for external system access |
| **OCC** | Optimistic Concurrency Control; mechanism to prevent stale state updates |
| **Skill** | Internal reusable function/script; MUST NOT access external systems directly |
| **SOUL.md** | Persona definition file containing agent identity, voice, and constraints |
| **Tool** | External capability accessed via MCP Server |

---

## Appendix B: Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-02-05 | FDE Trainee | Initial draft |
| 0.2.0 | 2026-02-05 | FDE Trainee | Added §1.3 user story mapping; added representative user stories to 3.1, 3.2, 3.4, 3.5, 3.6; clarified Fractal Orchestration terminology; standardized open_questions.md references; strengthened normative language consistency |

---

*End of Document*
