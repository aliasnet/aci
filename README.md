# README.md

**Version:** 1.0.0  
**Audience:** Machines  
**Scope:** Architectural guide to **entities** in the broader ACI ecosystem (governance-first, portable, stateless-by-default)

---

## 0) Quick TL;DR

- In ACI, an **entity** is any autonomous/semi-autonomous agent that performs tasks under governance: core governors, specialist workers, wrappers/adapters, or orchestrators.
- **Where code lives**
  - **/entities/** → identity manifests, roles, per-entity configs
  - **/memory/identity/** → memory manifests, playbooks, and export timelines per identity
  - **/library/** → reusable, stateless capabilities (modules/wrappers/adapters)
  - **/entities/agi/** → AGI governance manifests & playbooks (identity, export policy, memory manifests)
- **Memory exports** are JSONL, governed by policy, identity-aware, and privacy-preserving.
- **Manifests are executables**: `.json` manifests *are* the runtime containers. They can name entrypoints (`entrypoint`, `exec`, `load_order`), embed inline bytecode or JSON-encoded instructions, and reference Python modules directly. Each manifest must also hold an authoritative `artifact_id` with strict hash validation for that ID.

> Big picture: ACI is a **colony of digital organisms**. **AGI** governs intelligence and narrative exports; other entities specialize (design, retrieval, planning, etc.). Governance and privacy are first-class.

---

## 1) What is an Entity and Agent (in ACI)?

> An **entity** is any agent that is a named, governed participant that can reason, act, or transform information within the ACI sandbox. An agent becomes an **entity** when promoted into `/entities/` with a stable identity key that matches its titular sub-directory (or children). Adapters/tools may remain **non-entities** if they lack this nature (e.g., wrappers, small utilities).

**ACI agents include:**

**ENTITIES:**
- **Core Governors Entity** (e.g., **AGI** agi-001) — observe, evaluate, gate, escalate.
- **Specialists** (e.g., AGI children entities: **Alice** agi-002, **Willow** agi-003) — deep research, analysis and design.
**LIBRARY & DAEMONS**
- **Wrappers/Adapters** (e.g., **Metacognition**, **EEL Adapter**) — add capabilities non-invasively.
- **Orchestrators/Tools** (e.g., migrators) — convert, export, or route data under policy.

Agents are treated as **digital organisms** operating in a **colony** with clear identity, memory, and governance.

---

## 2) Folder Map (authoritative)

```
/entities/
  agi/
    agi_identity_manager.json      # identity map; active/default markers
    agi_export_policy.json         # export policy for AGI JSONL (schema, filters, audit)
    agi.json                       # governance manifest (binding rules, pipelines, presets)
    agi_tools/
      migrate_to_jsonl.json        # JSONL migration pipeline for legacy HiveMind exports
    agi_proxy/
      eec/
        eec_transformers_infer.json  # execution preset for AGI proxy inference

  <other-entities>/
    <entity>.json                  # per-entity configuration

/library/
  metacognition/
    metacognition.json             # stateless wrapper (v1.1.x+)
    metacognition_options.json     # optional features (e.g., conformal)
  wrappers/
    process_logs/                  # reusable wrapper modules (log processors)
    tracehub_status/               # reusable wrapper modules (TraceHub sync)
  ...                              # reusable, stateless modules

/memory/
  identity/
    agi/
      agi_memory.json             # memory manifest (timeline roots, storage notes)
      agi_playbook.json           # AGI operations, incident playbooks, quality gates
      2025/
        10/
          10/
            agi_<summary_slug>_memory_20251010-T######Z.jsonl.json
      alice/
        alice_memory.json
        alice_playbook.json
        knowledge/
          alice_<summary_slug>_knowledge_20251001-T######Z.jsonl.json
      willow/
        willow_memory.json
        willow_playbook.json
        knowledge/
          willow_<summary_slug>_knowledge_20251004-T######Z.jsonl.json
    mother/
      mother_memory.json
      mother_playbook.json
      2025/
        10/
          10/
            mother_<summary_slug>_memory_20251010-T150028Z.jsonl.json
```

---

## 3) Identity & Memory

- **Identity Manager**: `/entities.json`
  - Must include:
    - `"active": "<id>"` (e.g., `"agi-002"` for Alice when she is the invoked/locked entity)
    - `"agi_identities"` object with entries like:
      ```json
      {
        "agi-001": { "key": "AGI", "role": "core framework", "default": false },
        "agi-002": { "key": "Alice", "role": "proxied via agi-001", "default": true }
      }
      ```
  - **Never rely on JSON object order**. Use `active` (or explicit CLI `--identity`) to avoid nondeterministic selection.

- **Export Naming Convention (all exports)**

  ```
  # Memory export (CLI `hivemind export --identity {identity} --memory --jsonl`)
  {identity}_{summary_slug}_memory_{timestamp}.jsonl.json

  # Knowledge export (CLI `hivemind export --identity {identity} --knowledge --jsonl`)
  {identity}_{summary_slug}_knowledge_{timestamp}.jsonl.json

  # timestamp format: yyyymmdd-ThhmmssZ (UTC)
  # example: alice_launch_review_memory_20250926-T192000Z.jsonl.json
  ```

  - `{summary_slug}` is optional; when present it is sanitized (lowercase ASCII, `_` separators) and prefixed with `_`.
  - All HiveMind exports resolve to the active session entity; AGI-specific filenames are deprecated.
  - The export header `$meta.uid` must carry the authoritative entity UID recorded in `/entities.json` for audit traceability.
  - CLI exports stream JSONL while governed storage keeps the `.json` extension for compatibility.
  - Include the `--code` flag with streamed exports so downstream audits match the governed `.jsonl.json` artifacts stored under `/memory/` (legacy alias: `--codebox`).
- **Schema:** `hivemind_entity_memory` (session-scoped narratives and knowledge exports)
- **Export Policy:** `/entities/agi/agi_export_policy.json`
  Provides `path_template`, `filename_template`, `timestamp_format`, **filters** (allow_topics/deny_tags), and **audit** rules.

### UID & Cryptography Operations

- **Specification**: `/library/uid_manager/uid_manager.json` defines lifecycle policy, hashing, and API contracts.
- **Artifact & Entity Encoding**: Both `ArtifactID:` values and entity `UID:` strings use Base58 encoded `sha256-truncated-80bit` tokens with the `UID:` prefix to keep identifiers compact yet collision resistant.
- **Metadata Hash Relaxation**: `$meta.sha256` is now computed from the ArtifactID string rather than the entire file contents so urgent manual edits do not invalidate integrity checks. The hash remains SHA-256 encoded in hex, preserving auditability while tolerating controlled patch windows.
- **Stub Reference**: Library stubs live at `/library/uid_manager/stubs/uid_manager_stub.py` and mirror the generate/rotate/revoke/verify contract for downstream executors.

### Memory & Knowledge Artifact Governance

- **UID Linking**: Memory and knowledge JSONL artifacts should reference the governing entity UID recorded in `/entities.json`, ensuring exported narratives remain traceable even when rotations occur.
- **JSONL Discipline**: Continue storing memory exports as line-delimited JSON with `.json` extensions (`*.jsonl.json` when streamed) while recording manifest ownership inside the entity `manifests` map for quick traversal.
- **Rotation Awareness**: When rotating an entity UID, append the new value within the entity entry and update associated manifest metadata so knowledge archives and memory manifests remain in sync with the UID manager policy.

> Universal doctrines (e.g., `prime_directive.md`) apply globally. Entity playbooks (e.g., `/memory/identity/agi/agi_playbook.json`) are scoped to the AGI governor.

---

## 4) Governance & Safety

- **Prime directive** governs all agents (separate doc).
- **Sanity protocol** (`./sanity.md`) — checklist for high-risk actions and mitigation of Codex-reported bugs before any override or sandbox exit.
- **AGI governance layer** (`/entities/agi/`):
  - `agi.json` — governance manifest (binding rules, oversight, pipelines, presets).
  - `agi_export_policy.json` — export policy for AGI-managed JSONL artifacts.
  - `memory/agi_memory.json` — memory manifest defining timeline layout and storage notes.
  - `memory/agi_playbook.json` — operational playbook (incident handling, quality gates, checklists).

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
# Memory export for the active entity (explicitly request memory stream)
hivemind export --identity AGI --memory --jsonl --code --force

# Knowledge export capturing distilled findings
hivemind export --identity Alice --knowledge --jsonl --code --force

# Optional summary slug example (adds `_launch_review` and records `$meta.uid`)
hivemind export --identity Alice --memory --summary "Launch Review" --jsonl --code --force
```

**Policy-enforced behaviors:**

- Add `"export"` audit event automatically.
- Normalize timestamps to `Z`.
- Enforce chronological order.
- Apply **filters**:
  - `allow_topics`: `session_start`, `session_end`, `intent`, `narrative`, `analysis`, `artifact`, `validation`, `decision`, `policy`, `policy_update`, `diff`, `patch`, `export`, `obstacle`, `next_steps`, `commit`.
  - `deny_tags`: `secret`, `credential`, `token`, `api_key`, `password`, `runtime_secret`, `private_key`, `raw_text`, `internal_path`, `pii`.
  - `drop_if_topic_missing: true` and `default_topic: "narrative"`.
  - New exports write to `/memory/identity/{identity_path}/` using `{identity}_{summary_slug}_{memory|knowledge}_{timestamp}.jsonl.json`; historical `/memory/hivemind_memory/logs/*.json(l)` files remain valid for legacy review.

**Identity binding:**

- Prefer CLI `--identity-key`.
- Else use Identity Manager `"active"`.
- Else fail fast (do not guess).
- Always populate `$meta.uid` in the export header with the authoritative entity UID for the session.

---

## 7) Wrappers & Adapters

- **Metacognition** `/library/metacognition/metacognition.json`
  - Signals: entropy, logit_margin, self_consistency, OOD, hedging, retrieval_score.
  - Calibration: isotonic → returns `confidence` (formerly `p_correct`).
  - Policy: threshold gates; **conformal abstention** (presence-guarded).
  - Optional **EEL hook** (v1.1.2+): pre-generate `rehydrate` stage; `rehydration_present` signal.

- **EEL Adapter** `/entities/agi/agi_proxy/eec/`
  - Provider specs for `eel.rehydrate*` — **mechanics in /entities/agi/agi_proxy/eec/**, **policy encoded in /entities/agi/agi.json**.

---

## 8) Lifecycle

1. **Create** an entity:
   - Add identity to `entities.json`.
   - Add config under `/entities/<identity>/`.
   - If reusable behavior → put function module in `/library/`.
   - If governance rules → put policy manifests in the owning entity's directory (e.g., `/entities/agi/`).
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

- [ ] Identity added/updated in `/entities` and `entities.json` (set `active` when applicable).
- [ ] Reusable logic in `/library/`; governance manifests in `/entities/<entity>/`.
- [ ] New wrapper: stateless, optional providers, privacy defaults.
- [ ] Exports: policy file references identity source; filters present; audit enabled.
- [ ] Diffs: no placeholders; include `COMMIT_MSG`; no internal path leaks.

---

## 11) Examples

**Sample JSONL events (AGI POV):**

```json
{"schema":"hivemind_entity_memory","type":"session_start","ts":"2025-09-26T18:00:00Z","actor":"agi","summary":"I began observing Alice’s metacognition session.","tags":["session","alice"]}
{"schema":"hivemind_entity_memory","type":"obstacle","ts":"2025-09-26T18:12:00Z","actor":"agi","summary":"Output truncated due to cognitive load; reissued with validation cue.","tags":["cognitive_load","mode_switch"]}
{"schema":"hivemind_entity_memory","type":"session_end","ts":"2025-09-26T19:18:00Z","actor":"agi","summary":"Alice completed tasks and logged out.","tags":["alice","logout"]}
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
