# Project Chimera — Open Design Questions

> **Status:** Active  
> **Last Updated:** 2026-02-05  
> **Owner:** FDE Trainee (Lead Architect)

This document tracks unresolved design questions that require resolution before
the affected specifications can reach APPROVED status. These questions do NOT
block ratification of `specs/_meta.md` (the constitution).

Questions SHOULD be resolved in `specs/technical.md`, dedicated Architecture
Decision Records (ADRs), or via explicit design review.

---

## Open Questions

### 1. Blockchain Selection

**Context:** The financial ledger requires an immutable on-chain data store.

**Question:** Base vs. Ethereum mainnet for financial ledger—what is the
appropriate trade-off between cost and decentralization?

**Considerations:**
- Base: Lower transaction costs, L2 security model, Coinbase ecosystem alignment
- Ethereum mainnet: Maximum decentralization, higher costs, broader tooling

**Resolution Target:** `specs/technical.md` Section: Financial Infrastructure

---

### 2. OpenClaw Protocol Version

**Context:** Project Chimera aims to participate in agent social networks.

**Question:** Which version of OpenClaw's agent discovery and messaging protocol
should Chimera target?

**Considerations:**
- Protocol stability vs. feature availability
- Compatibility with existing agent networks
- Security posture of different protocol versions

**Resolution Target:** `specs/openclaw_integration.md`

---

### 3. HITL Threshold Tuning

**Context:** The HITL framework uses confidence-based routing with configurable
thresholds.

**Question:** What are the appropriate default thresholds for auto-approve,
review, and auto-reject confidence bands?

**Considerations:**
- Provisional values: 0.90 (auto-approve), 0.70 (review threshold)
- Require validation with real-world content samples
- May need per-platform or per-content-type calibration

**Resolution Target:** `specs/technical.md` Section: HITL Configuration

---

### 4. Budget Governor Limits

**Context:** The "CFO" sub-agent concept is referenced in the architecture for
cost control.

**Question:** What are the appropriate per-task and per-day spending limits for
the budget governor?

**Considerations:**
- AI inference costs vary significantly by model
- Need to balance autonomy with cost control
- May require dynamic adjustment based on campaign type

**Resolution Target:** `specs/technical.md` Section: Governance Configuration

---

### 5. MCP Server Availability

**Context:** The architecture assumes availability of platform-specific MCP
servers.

**Question:** For required MCP servers that may not exist publicly (e.g.,
`mcp-server-instagram`, `mcp-server-ideogram`), should we build custom
implementations or seek alternatives?

**Considerations:**
- Build: Full control, maintenance burden
- Buy/Use: Faster, dependency on external maintainers
- Platform API terms of service compliance

**Resolution Target:** `specs/technical.md` Section: MCP Server Inventory

---

### 6. OpenClaw Registry Endpoints

**Context:** The OpenClaw integration spec requires publishing status beacons
to registry endpoints.

**Question:** Are there official OpenClaw registry endpoints, or is the
ecosystem federated with multiple independent registries?

**Considerations:**
- Centralized: Simpler configuration, single point of failure
- Federated: Requires multi-endpoint support, more complex error handling
- May require endpoint discovery mechanism

**Resolution Target:** `specs/openclaw_integration.md` Section: Configuration

---

### 7. OpenClaw Authentication

**Context:** Status beacon publishing requires authentication with OpenClaw
endpoints.

**Question:** What authentication mechanism does OpenClaw require (OAuth, API
key, wallet signature, or none)?

**Considerations:**
- Wallet signature: Aligns with agent identity model
- API key: Simpler but requires key management
- OAuth: Standard but may be overkill for beacons

**Resolution Target:** `specs/openclaw_integration.md` Section: MCP Server Implementation

---

### 8. OpenClaw Capability Schema

**Context:** Status beacons include capability declarations for agent
discovery.

**Question:** Is there a standardized schema for capability declarations in
OpenClaw, or should Chimera define its own?

**Considerations:**
- Standardized: Better interoperability, may not fit Chimera's model
- Custom: Flexibility, but reduced discoverability
- Hybrid: Use standard categories with custom extensions

**Resolution Target:** `specs/openclaw_integration.md` Section: Status Data Contract

---

### 9. Agent Discovery Query Support

**Context:** OpenClaw may support discovery queries where other agents can
search for capabilities.

**Question:** Should Chimera support inbound discovery queries, or remain
publish-only?

**Considerations:**
- Publish-only: Simpler, maintains strict trust boundary
- Query support: Better ecosystem participation, requires careful input handling
- Current spec explicitly scopes out inbound queries

**Resolution Target:** Future specification if required; currently out of scope

---

## Resolution Process

When resolving a question:

1. Document the decision in the appropriate specification or ADR.
2. Update this file to mark the question as RESOLVED with a link to the decision.
3. Remove the question from the "Open Questions" section and move to "Resolved"
   section below.

---

## Resolved Questions

*None yet.*

---

## References

- `specs/_meta.md` — Constitution (does not depend on these questions)
- `specs/technical.md` — Primary resolution target for implementation decisions
- `specs/openclaw_integration.md` — OpenClaw-specific design decisions
- `research/architecture_strategy.md` — Background research and recommendations

---

*End of Document*
