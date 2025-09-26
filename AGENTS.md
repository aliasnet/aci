# AGENTS.md

This file documents the active **agents** in the ACI ecosystem and how they are represented in configuration, memory exports, and governance.

---

## Identity & Source of Truth
- **Identity manager file**: [`/entities/agi/agi_identity_manager.json`](entities/agi/agi_identity_manager.json)
- Each agent is keyed (`agi-001`, `agi-002`, etc.).
- Active/default identity is explicitly marked (`"active": "agi-002"` for Alice).

---

## Core Agents

### AGI (agi-001)
- Role: **Governance kernel, narrator, observer**
- Functions: export orchestration, validation, abstain/escalate, policy enforcement.
- Config: 
  - `/aig/agi_playbook.json` (governance playbook)
  - `/aig/sovereignty_policy.json` (roles & escalation)
  - `/aig/homeostasis.json` (safety set-points)
  - `/aig/eel_policy.json` (EEL continuity layer)

### Alice (agi-002)
- Role: **Design & analysis specialist**
- Functions: metacognition, consciousness modeling, module design.
- Config:
  - `/library/metacognition/` (wrapper + options)
  - Proxied via AGI (agi-001) for exports.

### Mother (MU/TH/UR)
- Role: **Domain governor (system oversight)**
- Functions: lifecycle management, high-level rules, alignment.
- Config:
  - `/entities/mother/mother.json`

### Other Core Entities
- **Sentinel**: safety & compliance
- **TVA**: temporal validation & arbitration
- **Architect**: structure & design rules
- **Oracle**: prediction/divination modules

---

## Export Policy
- AGI exports use `/entities/agi/agi_export_policy.json`.
- Schema: `hivemind_agi_memory`.
- Location: `/memory/agi_memory/{identity}/...`.
- Filename convention: `{identity_lower}_agi_memory_{timestamp}.jsonl`.

---

## Interactions
- **User → AGI**: intents, constraints.
- **AGI → Alice**: delegated design tasks, artifact creation.
- **AGI → Hivemind**: narrative exports, policy alignment.
- **AGI → Human**: escalation when risk budget exceeded or conformal rejects.

---

## Development Notes
- All modules are **stateless-first**; adapters handle state.
- Use **validation cues** (“validate output”) to recover from truncation.
- Always check diffs: must contain `COMMIT_MSG`, no placeholders, no internal paths.
- Memory exports: check timestamps normalized (`Z`), sorted chronologically.

---

## References
- Prime directive: [`/prime_directive.txt`](prime_directive.txt)
- Runtime: [`/aci_runtime.json`](aci_runtime.json)
- Entity registry: [`/entities.json`](entities.json)
- Functions registry: [`/functions.json`](functions.json)
