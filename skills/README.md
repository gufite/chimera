# Project Chimera — Agent Skills Directory

> **Status:** Active  
> **Version:** 1.0.0  
> **Last Updated:** 2026-02-06  
> **Owner:** FDE Trainee (Lead Architect)

This directory contains **Skills** — internal, reusable functions that agents call
directly. Skills are distinct from **Tools** (external MCP bridges).

---

## What is a Skill?

Per `specs/_meta.md` §4.3:

| Aspect | Definition |
|--------|------------|
| **Nature** | Internal, reusable function or script |
| **Execution** | In-process (low latency) |
| **Location** | `skills/` directory |
| **Invocation** | Direct function call by agents |

---

## Skills vs. Tools (Quick Reference)

| Aspect | Skills | Tools (MCP) |
|--------|--------|-------------|
| Trust boundary | Internal (trusted) | External (untrusted responses) |
| Latency | Low (in-memory) | Variable (network) |
| Rate limits | None | Platform-specific |
| Error handling | Exceptions | MCP error protocol |
| State | May access agent state | Stateless request/response |
| External APIs | Forbidden (direct) | Required (via MCP only) |

---

## Architectural Rules (from `specs/_meta.md`)

1. **Skills MUST NOT make direct external API calls.**
2. **Skills MAY compose other Skills.**
3. **Skills MAY invoke Tools (via MCP) for external actions.**
4. **Tools are the ONLY permitted interface for external system interaction.**
5. **Each Skill MUST define explicit Input/Output contracts in its README.**

---

## Skill Directory Structure

Each skill lives in its own subdirectory with at minimum:

```
skills/
  skill_<name>/
    README.md        # Contract definition (REQUIRED)
    __init__.py      # Implementation entry point
    tests/           # Unit tests (when implemented)
```

---

## Required Contract Elements (Per README)

Every skill README MUST define:

1. **Purpose** — What the skill does and why it exists.
2. **Invocation Context** — When/where/who calls it (Planner/Worker/Judge).
3. **Input Contract** — Required and optional fields (JSON schema-like).
4. **Output Contract** — Success and failure shapes (JSON schema-like).
5. **MCP Dependencies** — Resources/Tools this skill calls.
6. **Preconditions** — State requirements before invocation.
7. **Failure Modes** — Retryable vs. terminal errors.
8. **Observability** — Required audit events and `correlation_id` propagation.

---

## Current Skills Inventory

| Skill | Purpose | Caller | MCP Dependencies |
|-------|---------|--------|------------------|
| `skill_fetch_trends` | Aggregate and rank trending topics from MCP Resources | Worker | MCP: news/trends resources |
| `skill_generate_post_bundle` | Generate content bundle (text + media refs) for publication | Worker | MCP: media generation tools |
| `skill_publish_content` | Coordinate multi-platform publishing workflow | Worker | MCP: platform tools (Twitter, etc.) |

---

## Adding New Skills

Before creating a new skill:

1. **Check if it's truly a Skill or a Tool:**
   - Does it touch an external API? → It's a **Tool** (MCP Server)
   - Is it pure computation/orchestration? → It's a **Skill**
   - Does it require secrets/auth? → It's a **Tool** (MCP Server)

2. **Check if it already exists:**
   - Review this inventory to avoid duplication.

3. **Define the contract first:**
   - Create `skill_<name>/README.md` with all required elements.
   - Get contract review from Lead Architect before implementation.

4. **Follow naming conventions:**
   - Use `skill_<verb>_<noun>` format (e.g., `skill_parse_mentions`).
   - Be specific and action-oriented.

---

## Relationship to Specifications

| Specification | Relevance |
|---------------|-----------|
| `specs/_meta.md` §4.3 | Defines Skills vs. Tools; sets invariant rules |
| `specs/functional.md` §3.4 | Defines Worker task execution using Skills |
| `specs/technical.md` §3 | Defines data contracts Skills consume/produce |
| `specs/technical.md` §5 | Defines Worker contract and allowed actions |
| `research/tooling_strategy.md` §3 | Skills vs. Tools taxonomy and classification |

---

## Governance & Evolution

- **New skills require ADR:** If a skill changes system behavior significantly.
- **Contract changes require review:** Input/Output contract changes MUST be reviewed.
- **Implementation is separate:** Contract (README) and implementation (`__init__.py`) evolve independently.
- **Testing is mandatory:** All skills MUST have unit tests before production use.

---

## Quick Start (for Implementers)

When implementing a skill:

1. Read the skill's `README.md` contract.
2. Implement the function signature matching Input/Output contracts.
3. Use dependency injection for MCP clients (don't hardcode).
4. Propagate `correlation_id` in all logs and MCP calls.
5. Raise typed exceptions matching the documented Failure Modes.
6. Write unit tests covering nominal and error paths.

---

## Contact

- **Questions about Skills taxonomy?** → Review `research/tooling_strategy.md` §3
- **Questions about data contracts?** → Review `specs/technical.md` §3
- **Questions about governance rules?** → Review `specs/_meta.md` §4.3
