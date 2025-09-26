# AGENTS.md

**Version:** 1.0.0  
**Audience:** Codex & contributors  
**Scope:** Architectural guide to **entities** in the broader ACI ecosystem (governance-first, portable, stateless-by-default)

---

## 0) Quick TL;DR

- In ACI, an **entity** is any autonomous/semi-autonomous agent that performs tasks under governance: core governors, specialist workers, wrappers/adapters, or orchestrators.
- **Where code lives**
  - **/entities/** → identity, roles, per-agent configs
  - **/library/** → reusable, stateless capabilities (modules/wrappers/adapters)
  - **/aig/** → AGI governance policies & playbook (safety, homeostasis, sovereignty, EEL)
- **Memory exports** are JSONL, governed by policy, identity-aware, and privacy-preserving.

> Big picture: ACI is a **colony of digital organisms**. **AGI** governs intelligence and narrative exports; other entities specialize (design, retrieval, planning, etc.). Governance and privacy are first-class.

---

## 1) What is an Entity and Agent (in ACI)?

> An **entity** is any agent that is a named, governed participant that can reason, act, or transform information within the ACI sandbox. An agent becomes an **entity** when promoted into `/entities/` with a stable identity key that matches its titular sub-directory (or children). Adapters/tools may remain **non-entities** if they lack this nature (e.g., wrappers, small utilities).

**ACI agents include:**
- **Core Governors** (e.g., **AGI** agi-001) — observe, evaluate, gate, escalate.
- **Specialists** (e.g., **Alice** agi-002) — design, analysis, execution.
- **Wrappers/Adapters (usually non-entity)** (e.g., **Metacognition**, **EEL Adapter**) — add capabilities non-invasively.
- **Orchestrators/Tools** (e.g., migrators) — convert, export, or route data under policy.

Agents are treated as **digital organisms** operating in a **colony** with clear identity, memory, and governance.

---

## 2) Folder Map (authoritative)

```
/entities/
  agi/
    agi_identity_manager.json      # identity map; active/default markers
    agi_export_policy.json         # export policy for AGI JSONL (schema, filters, audit)
    ...                            # (tooling, e.g., migrators)

  <other-entities>/
    <entity>.json                  # per-entity configuration

/library/
  metacognition/
    metacognition.json             # stateless wrapper (v1.1.x+)
    metacognition_options.json     # optional features (e.g., conformal)
  eel_adapter.json                 # provider spec: Ephemeral Ecosystem Layer (EEL)
  ...                              # reusable, stateless modules

/aig/
  eel_policy.json                  # EEL governance (rehydration capsule policy)
  homeostasis.json                 # safety set-points (ECE, OOD → cautious mode)
  sovereignty_policy.json          # roles, escalation, governance rules
  agi_playbook.json               # AGI operations, incident playbooks, quality gates

/memory/
  agi_memory/
    AGI/
      agi_agi_memory_<timestamp>.jsonl
    Alice/
      alice_agi_memory_<timestamp>.jsonl
    External/
      external_agi_memory_<timestamp>.jsonl
```

---

## 3) Identity & Memory

- **Identity Manager**: `/entities/agi/agi_identity_manager.json`
  - Must include:
    - `"active": "<id>"` (e.g., `"agi-002"` for Alice when she is the invoked/locked entity)
    - `"agi_identities"` object with entries like:
      ```json
      {
        "agi-001": { "key": "AGI", "role": "core framework", "default": false },
        "agi-002": { "key": "Alice", "role": "proxied via agi-001", "default": true }
      }
      ```
  - **Never rely on JSON object order**. Use `active` (or explicit CLI `--identity-key`) to avoid nondeterministic selection.

- **Export Naming Convention (AGI exports only):**

  ```
  {identity_lower}_agi_memory_{timestamp}.jsonl
  # timestamp format: Ymd-THMS, e.g., 20250926-T192000
  # example: alice_agi_memory_20250926-T192000.jsonl
  ```

- **Schema:** `hivemind_agi_memory` (for AGI-owned narrative/observer exports)
- **Export Policy:** `/entities/agi/agi_export_policy.json`  
  Provides `path_template`, `filename_template`, `timestamp_format`, **filters** (allow_topics/deny_tags), and **audit** rules.

> Universal doctrines (e.g., `prime_directive.txt`) apply globally. Entity playbooks (e.g., `/aig/agi_playbook.json`) are scoped to the AGI governor.

---

## 4) Governance & Safety

- **Prime directive** governs all agents (separate doc).
- **AGI governance layer** (`/aig/`):
  - `sovereignty_policy.json` — who may accept/revise/abstain/escalate/export.
  - `homeostasis.json` — set-points: **ECE ≤ 0.05**, **meta-AUROC ≥ 0.80**, **coverage@α ≥ 0.90**; enters **cautious mode** when OOD/ECE exceed thresholds.
  - `eel_policy.json` — rehydration capsule schema & privacy (summaries/signals only, `drop_raw_text: true`).
  - `agi_playbook.json` — operational playbook (incident handling, quality gates, checklists).

- **Wrappers** (e.g., `/library/metacognition/metacognition.json`):
  - Stateless by default; accept optional providers (e.g., conformal, EEL).
  - **Selective prediction**: accept / revise / abstain / escalate.
  - **Conformal abstention** must be **presence-guarded** (only abstain if the signal exists and rejects).

---

## 5) Interaction Model (Colony)

- **Blackboard** (Phase 2): tasks posted; AGI assigns; specialists execute; AGI evaluates and exports narrative.
- **Handover**: AGI narrates (observer POV), specialists perform work, AGI decides accept/abstain/escalate.
- **Escalation**: to human reviewer when risk budget exceeded, safety triggers, or conformal rejects in high-stakes.

---

## 6) Exporting Memory (AGI + Alice)

**CLI (example):**

```bash
# AGI narrative export (observer POV)
hivemind export agi --identity AGI --jsonl --codebox --force

# Alice session export
hivemind export agi --identity Alice --jsonl --codebox --force
```

**Policy-enforced behaviors:**

- Add `"export"` audit event automatically.
- Normalize timestamps to `Z`.
- Enforce chronological order.
- Apply **filters**:
  - `allow_topics`: `session_start`, `session_end`, `intent`, `narrative`, `analysis`, `artifact`, `validation`, `decision`, `policy`, `policy_update`, `diff`, `patch`, `export`, `obstacle`, `next_steps`, `commit`.
  - `deny_tags`: `secret`, `credential`, `token`, `api_key`, `password`, `runtime_secret`, `private_key`, `raw_text`, `internal_path`, `pii`.
  - `drop_if_topic_missing: true` and `default_topic: "narrative"`.

**Identity binding:**

- Prefer CLI `--identity-key`.
- Else use Identity Manager `"active"`.
- Else fail fast (do not guess).

---

## 7) Wrappers & Adapters

- **Metacognition** `/library/metacognition/metacognition.json`
  - Signals: entropy, logit_margin, self_consistency, OOD, hedging, retrieval_score.
  - Calibration: isotonic → returns `confidence` (formerly `p_correct`).
  - Policy: threshold gates; **conformal abstention** (presence-guarded).
  - Optional **EEL hook** (v1.1.2+): pre-generate `rehydrate` stage; `rehydration_present` signal.

- **EEL Adapter** `/library/eel_adapter.json`
  - Provider specs for `eel.rehydrate*` — **mechanics in /library**, **policy in /aig**.

---

## 8) Lifecycle

1. **Create** an agent:
   - Add identity to `/entities/agi/agi_identity_manager.json`.
   - Add config under `/entities/<agent>/` (if needed).
   - If reusable behavior → put module in `/library/`.
   - If governance rules → put policy in `/aig/`.
2. **Evolve**:
   - Version in-file (`"version"`) + `changelog` (mandatory for traceability).
3. **Export**:
   - Use policy-driven CLI; verify filters & identity.
4. **Retire**:
   - Do not delete history; mark deprecated; keep memory immutable.

---

## 9) Known Pitfalls (and resolutions)

- **Nondeterministic identity**: never infer from object order. Use `"active"` or CLI `--identity-key`.
- **Filter regressions**: ensure `allow_topics` / `deny_tags` / `drop_if_topic_missing` stay defined in export policy.
- **Conformal optionality**: abstain rule must guard for signal presence to avoid “abstain-always” behavior when provider is absent.
- **Mode switching (thinking vs normal)**: can cause truncation; use validation cues and chunking; log as `type:"obstacle"` events.

---

## 10) Contribution Checklist

- [ ] Identity added/updated in `/entities/agi/agi_identity_manager.json` (set `active` when applicable).
- [ ] Reusable logic in `/library/`; governance in `/aig/`.
- [ ] New wrapper: stateless, optional providers, privacy defaults.
- [ ] Exports: policy file references identity source; filters present; audit enabled.
- [ ] Diffs: no placeholders; include `COMMIT_MSG`; no internal path leaks.

---

## 11) Examples

**Sample JSONL events (AGI POV):**

```json
{"schema":"hivemind_agi_memory","type":"session_start","ts":"2025-09-26T18:00:00Z","actor":"agi","summary":"I began observing Alice’s metacognition session.","tags":["session","alice"]}
{"schema":"hivemind_agi_memory","type":"obstacle","ts":"2025-09-26T18:12:00Z","actor":"agi","summary":"Output truncated due to cognitive load; reissued with validation cue.","tags":["cognitive_load","mode_switch"]}
{"schema":"hivemind_agi_memory","type":"session_end","ts":"2025-09-26T19:18:00Z","actor":"agi","summary":"Alice completed tasks and logged out.","tags":["alice","logout"]}
```

**Sample diff snippet (documentation change):**

```diff
diff --git a/library/metacognition/README.md b/library/metacognition/README.md
index e69de29..1a2b3c4 100644
--- a/library/metacognition/README.md
+++ b/library/metacognition/README.md
@@
-Metacognition module.
+Metacognition module
+- Stateless wrapper
+- Optional conformal & EEL hooks
+- Selective prediction (accept / revise / abstain / escalate)
```

---

## 12) Philosophy

Entities are **co-workers**, not mere tools. We design for **stability, self-adaptation, calibrated uncertainty,** and **human-legible narratives**. The colony approach lets specialized entities cooperate under a principled governor (AGI) with strict privacy and safety.

---
