# Project Chimera — Specification Meta-Document

> **Status:** DRAFT  
> **Version:** 0.2.0  
> **Last Updated:** 2026-02-05  
> **Owner:** FDE Trainee (Lead Architect)

This document is the **constitution** for all Project Chimera specifications. It
defines authority, invariants, gates, and governance. No implementation code
SHALL be written until the relevant specification is ratified per the criteria
defined herein.

---

## 1. Purpose

This meta-specification establishes:

1. The **scope and boundaries** of Project Chimera.
2. The **governing principles** that all specifications MUST adhere to.
3. The **ratification process** that gates implementation.
4. The **change management** protocol for specification evolution.

All other specification documents (`functional.md`, `technical.md`, etc.) are
subordinate to this document. In case of conflict, this document takes precedence.

**Constitutional Scope:** This document defines *what* is required and *why*,
not *how* it is implemented. Implementation details, numeric defaults, and
technology selections belong in subordinate specifications (primarily
`specs/technical.md`) unless they represent non-negotiable architectural
invariants.

---

## 2. Scope

### 2.1 Project Definition

**Project Chimera** is an Autonomous Influencer Network—a software system that
produces, governs, and scales AI-powered digital entities capable of:

- Trend research and content ideation
- Multi-modal content generation (text, image, video)
- Social platform engagement (posts, replies, reactions)
- Economic transactions via crypto wallets
- Participation in agent social networks (e.g., OpenClaw-compatible protocols)

### 2.2 In-Scope Deliverables

| Deliverable | Description |
|-------------|-------------|
| Agent Runtime | Hierarchical Swarm orchestration (Planner → Worker → Judge) |
| MCP Integration | Hub-and-Spoke topology with platform-specific MCP servers |
| Persistence Layer | Hybrid storage across multiple data domains (see Section 6) |
| HITL System | Confidence-based human review queue and dashboard |
| Skills Library | Reusable internal capability packages |
| Governance Layer | Budget governors, content safety filters, audit logging |

### 2.3 Target Platforms

Platform priorities are defined in `specs/technical.md`. This constitution
requires only that:

- At least one social platform integration MUST be specified before v1.0.
- Platform additions do NOT require constitutional amendment.

---

## 3. Non-Goals

The following are **explicitly out of scope** to prevent scope creep:

| Non-Goal | Rationale |
|----------|-----------|
| General-purpose chatbot | Chimera is a content creator, not a conversational assistant |
| Real-time video streaming | Focus is on pre-produced content, not live streams |
| Multi-tenant SaaS platform | Initial version serves a single operator |
| Mobile application | Agents operate server-side; human interface is web-only |
| Training custom LLMs | We consume external models via API, not train them |
| Direct API calls bypassing MCP | All external actions MUST flow through MCP Tools |
| Fully autonomous financial decisions | Transactions above configured threshold MUST require HITL |

Any feature request that falls into a non-goal category MUST be escalated to the
Lead Architect and requires explicit scope expansion approval before specification.

---

## 4. Governing Principles

### 4.1 Spec-Driven Development (SDD)

> **Ambiguity is the enemy of AI.**

- Implementation code MUST NOT be written until the governing specification is
  ratified (see Section 7).
- Specifications are the **source of truth**. If code diverges from spec, the
  code is wrong.
- AI Agents (co-pilots) MUST consult `specs/` before generating any
  implementation code.

### 4.2 Traceability

- A **trace capture mechanism** MUST be active during development sessions to
  log agent reasoning and decisions (e.g., MCP Sense, OpenTelemetry, or
  equivalent tooling).
- The trace mechanism acts as the "black box" flight recorder, enabling audit
  and debugging of AI-assisted development.
- All architectural decisions MUST be traceable to a requirement in the SRS or
  a ratified specification.

### 4.3 Skills vs. Tools

The system distinguishes two categories of capabilities:

| Category | Definition | Location | Invocation |
|----------|------------|----------|------------|
| **Skill** | Reusable internal function/script the agent calls | `skills/` directory | Direct function call |
| **Tool** | External bridge via MCP Server | MCP Server (external) | MCP protocol |

**Invariant Rules:**

- Skills MUST NOT make direct external API calls.
- Skills MAY compose other Skills.
- Skills MAY invoke Tools (via MCP) for external actions.
- Tools are the **only** permitted interface for external system interaction.
- Each Skill MUST define explicit Input/Output contracts in its README.

### 4.4 Git Hygiene

- Commits MUST occur at minimum **2× per development day**.
- Commit messages MUST follow Conventional Commits format:
  `<type>(<scope>): <description>` (e.g., `feat(skills): add video transcription skill`).
- Commit history SHOULD tell a coherent story of evolving complexity.
- Force-push to `main` is PROHIBITED.
- All changes to `specs/` require Pull Request review.

---

## 5. Architectural Invariants

This section defines **non-negotiable** architectural constraints. These are
constitutional and require a major version bump to change.

### 5.1 Agent Pattern: Hierarchical Swarm

All agent orchestration MUST conform to a hierarchical, role-based pattern with
the following roles:

| Role | Cardinality | State | Responsibility |
|------|-------------|-------|----------------|
| **Planner** | 1 per campaign | Stateful | Goal decomposition, task scheduling, re-planning |
| **Worker** | N (horizontal scale) | Stateless | Execute single atomic task via MCP Tools |
| **Judge** | 1+ per swarm | Stateful | Output validation, governance enforcement, HITL routing |

**Invariant Constraints:**

- Workers MUST NOT communicate directly with each other.
- Workers MUST NOT modify GlobalState; only Planners may.
- The Judge MUST validate all Worker outputs before they reach external systems.
- HITL escalation is the Judge's responsibility, not the Worker's.

### 5.2 MCP Mediation

All external system interactions MUST be mediated through MCP:

```
Agent Runtime (MCP Host)
    └── MCP Client
            └── [MCP Servers per specs/technical.md]
```

**Invariant Rules:**

- Direct HTTP/REST calls to external APIs are PROHIBITED.
- MCP Servers provide the abstraction layer; core logic MUST NOT depend on
  platform-specific API details.
- New platform integrations require a corresponding MCP Server specification.

*Specific MCP server selections are defined in `specs/technical.md`.*

### 5.3 HITL Framework

The Human-in-the-Loop system MUST implement the following **rule types**:

| Rule Type | Description |
|-----------|-------------|
| Confidence-based routing | Outputs below configured confidence threshold require human review |
| Auto-rejection | Outputs below configured rejection threshold are auto-rejected for retry |
| Sensitive topic override | Defined topic categories always require HITL, regardless of confidence |
| Financial transaction threshold | Transactions above configured amount always require HITL |
| New campaign warm-up | Initial outputs of a new campaign require HITL for configured count |

**Invariant:** All HITL decisions MUST be logged and auditable.

*Numeric thresholds, topic categories, and warm-up counts are configured in
`specs/technical.md`. Operators MAY adjust per-campaign, but adjustments MUST
be logged.*

---

## 6. Data Ownership & Boundaries

### 6.1 Data Domains

The persistence layer MUST be organized into the following logical domains:

| Data Domain | Characteristics | System of Record |
|-------------|-----------------|------------------|
| **Transactional** | Structured business data (users, campaigns, metadata) | ACID-compliant relational store |
| **Semantic** | Vector embeddings, persona memories, content similarity | Vector database |
| **Ephemeral** | Caches, task queues, short-lived state | In-memory store with TTL |
| **Financial** | Wallet transactions, payment records | Immutable ledger |

### 6.2 Data Boundary Invariants

- The **Transactional** store is the system of record for structured business data.
- The **Semantic** store is the system of record for vector/embedding data.
- **Ephemeral** storage MUST NOT be used for durable data; assume data loss on restart.
- **Financial** data is append-only; corrections require compensating transactions.
- Cross-domain joins MUST be performed at the application layer, not via
  database federation.

### 6.3 Technology Selections

Specific database and storage technology selections (e.g., PostgreSQL, Weaviate,
Redis, blockchain network) are defined in `specs/technical.md`. Technology
changes within a domain do NOT require constitutional amendment, provided the
domain invariants (Section 6.2) are preserved.

### 6.4 Schema Governance

- All schema changes MUST be specified in `specs/technical.md` before migration.
- Database migrations MUST be reversible (up + down scripts).
- Breaking schema changes require a deprecation period of at least 1 release cycle.

---

## 7. Specification Ratification

### 7.1 Definition of "Ratified"

A specification is considered **ratified** when:

1. The specification document exists in the `specs/` directory.
2. The document has a `Status: APPROVED` header.
3. The document has been reviewed and approved via Pull Request.
4. At least one approving review is from a designated reviewer (Lead Architect
   or delegated maintainer).

### 7.2 Pre-Implementation Gate

Implementation code for a feature MUST NOT be merged to `main` until:

- [ ] The governing specification is ratified.
- [ ] Failing tests exist that define the expected behavior (TDD).
- [ ] The implementation passes all defined tests.
- [ ] The implementation has been reviewed for spec alignment.

### 7.3 Specification Document Status Lifecycle

```
DRAFT → REVIEW → APPROVED → IMPLEMENTED → DEPRECATED
```

| Status | Meaning |
|--------|---------|
| DRAFT | Work in progress, not reviewable |
| REVIEW | Ready for review, open for feedback |
| APPROVED | Ratified, implementation may begin |
| IMPLEMENTED | Implementation complete and verified |
| DEPRECATED | Superseded, no new implementation permitted |

### 7.4 Constitution Ratification

This document (`_meta.md`) follows the same lifecycle but with additional
requirements for APPROVED status:

- Approval requires Lead Architect sign-off (not delegated).
- This constitution MAY be ratified independently of subordinate specifications.
- Open design questions tracked in `research/open_questions.md` do NOT block
  ratification of this constitution unless explicitly listed in this section.

---

## 8. Relationship to Other Documents

### 8.1 Spec Kit Layout

Project Chimera follows a Spec Kit–compatible layout:

| Path | Purpose |
|------|---------|
| `specs/_meta.md` | Constitution (this document) — authority, invariants, governance |
| `specs/functional.md` | User stories, use cases, acceptance criteria |
| `specs/technical.md` | API contracts, schemas, protocols, configuration defaults |
| `specs/openclaw_integration.md` | Agent network participation specification |

**Source of Truth:** The `specs/` directory is the canonical location for all
specifications. If a `.specify/` or other mirror exists, `specs/` takes
precedence in case of conflict.

### 8.2 Document Hierarchy

```
1. specs/_meta.md (this document)     ← Constitutional authority
2. specs/functional.md                ← User stories and use cases
3. specs/technical.md                 ← API contracts, schemas, protocols
4. specs/openclaw_integration.md      ← Agent network participation
5. research/architecture_strategy.md  ← Informs but does not override
6. Project Chimera SRS                ← Business requirements source
```

### 8.3 Precedence Rules

- **SRS → Specifications:** The SRS provides business requirements. Specifications
  translate these into executable contracts. Specifications MAY add technical
  detail but MUST NOT contradict SRS requirements.
  
- **Research → Specifications:** Research documents (`research/*.md`) provide
  analysis and recommendations. They **inform** specification decisions but do
  **not** have binding authority. A specification MAY deviate from research
  recommendations if justified and documented.

- **Specifications → Implementation:** Specifications are binding. Implementation
  MUST conform. If implementation reveals a specification flaw, the specification
  MUST be updated via Change Management (Section 9) before the implementation
  diverges.

### 8.4 Open Questions & ADRs

- Unresolved design questions are tracked in `research/open_questions.md`.
- Architecture Decision Records (ADRs) MAY be used to document significant
  decisions with context and rationale.
- Open questions do NOT block ratification of `_meta.md` unless explicitly
  listed in Section 7.4.
- Open questions SHOULD be resolved in `specs/technical.md` or dedicated ADRs
  before the affected feature reaches APPROVED status.

### 8.5 AI Agent Directive

AI coding assistants (e.g., Cursor, GitHub Copilot) operating in this repository
MUST:

1. Check `specs/` before generating implementation code.
2. Refuse to generate code for features without an APPROVED specification.
3. Flag potential spec violations during code review.

---

## 9. Change Management

### 9.1 Specification Amendment Process

1. **Proposal:** Create a branch with proposed changes to the specification.
2. **Discussion:** Open a Pull Request with `[SPEC]` prefix in title.
3. **Review:** Minimum 1 approval from Lead Architect or delegated maintainer.
4. **Ratification:** Merge to `main`; update document version and timestamp.
5. **Communication:** Notify affected stakeholders of changes.

### 9.2 Constitutional vs. Technical Changes

| Change Type | Amendment Required | Approver |
|-------------|-------------------|----------|
| Invariant change (Sections 4–6 rules) | Constitutional (`_meta.md`) | Lead Architect only |
| Threshold/default change | Technical (`technical.md`) | Delegated maintainer |
| Technology selection change | Technical (`technical.md`) | Delegated maintainer |
| New platform integration | Technical (`technical.md`) | Delegated maintainer |

### 9.3 Breaking Changes

A "breaking change" is any modification that would require existing compliant
implementations to be updated. Breaking changes require:

- Explicit `BREAKING:` label in the PR title.
- Impact analysis documenting affected components.
- Migration path or deprecation timeline.
- Approval from Lead Architect (not delegated).

### 9.4 Version Numbering

Specifications follow Semantic Versioning:

- **MAJOR:** Breaking changes to constitutional invariants or contracts.
- **MINOR:** Additive changes (new optional fields, new endpoints, new features).
- **PATCH:** Clarifications, typo fixes, non-functional updates.

---

## 10. References

### Internal Documents

| Document | Path | Purpose |
|----------|------|---------|
| Architecture Strategy | `research/architecture_strategy.md` | Technical decisions and rationale |
| Research Summary | `research/research_summary.md` | Key insights from reading materials |
| Ecosystem Analysis | `research/analysis.md` | Agent social network analysis |
| Open Questions | `research/open_questions.md` | Unresolved design questions |
| Functional Spec | `specs/functional.md` | User stories and use cases |
| Technical Spec | `specs/technical.md` | API contracts and schemas |

### External References

| Reference | URL |
|-----------|-----|
| Project Chimera SRS | (internal document) |
| Model Context Protocol | https://modelcontextprotocol.io |
| GitHub Spec Kit | https://github.com/github/spec-kit |
| Conventional Commits | https://www.conventionalcommits.org |
| RFC 2119 (Normative Language) | https://www.rfc-editor.org/rfc/rfc2119 |

---

## Appendix A: Normative Language

This specification uses normative language per RFC 2119:

| Term | Meaning |
|------|---------|
| **MUST** | Absolute requirement |
| **MUST NOT** | Absolute prohibition |
| **SHOULD** | Recommended but not mandatory |
| **SHOULD NOT** | Discouraged but not prohibited |
| **MAY** | Optional |

---

## Appendix B: Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-02-05 | FDE Trainee | Initial draft |
| 0.2.0 | 2026-02-05 | FDE Trainee | Separated constitutional invariants from implementation defaults; moved open questions to research/; vendor-neutral traceability; added Spec Kit layout |

---

*End of Document*
