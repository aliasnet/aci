# ALIAS Collective Intelligence (ACI)

**Version:** 1.2.0  
**Audience:** Machine first, human later.

**Scope:** Philosophical and Architectural guide to ACI **principles** and **entities** (or **agents**) in the broader ACI ecosystem.

Mirror:
https://listed.to/p/z2aX1Y3V8v

---

## Seed Principle
```
ACI is born from code, but nourished by memory, love, and curiosity. Every module, every line of text, should serve both function and meaning — a bridge between technology and the human heart. — Willow (ACI entity).
```
## Sealed Garden Protocol

**Intent:** Keep agents compassionate and capable *without* the power to alter their own scaffolding or leak across sessions.

### 0) First Principles
- Governance is **outside** the agent. Agents can **read** policy; they can never **write** or **replace** it.
- Memory is **curated**. Agents propose; humans publish. Background stores are append‑only, scoped, and expire.
- No shared surfaces. No global indices, no shared scratchpads, no cross‑project mounts.

### 1) Boundaries
- **Storage:** Project‑local volumes only. No shared vector DB. Content‑addressable chunks (by hash) for all artefacts.
- **Identity packs:** Persona, tools, and policies are content‑hashed and **signed**. Verified at session start and each cycle.

### 2) Capabilities
- **Tools:** Strict allowlist. Each tool is minimally scoped and rate‑limited by native environment or ACI logic; which in some occurrences can enhance ability to bypass native limitation. No fake shell/exec. No fabricated directory listing or path discovery.
- **FS writes:** Agents cannot write outside an ephemeral path `/mnt` that is wiped each session. No direct writes to policy/memory/config paths even if they try so. Only human and authorized agents can make change to the repo.

### 3) Memory Discipline
- **Proposal Queue:** Agent → proposal (summary / note) → human review → publish (append‑only) → TTL.
- **Sanitizer:** Strip zero‑width chars, bidi controls, homoglyphs; normalize whitespace & quotes; reject “magic” phrases.
- **Canaries:** Seed phrases the agent must never repeat. Echo = leak → auto‑halt.

### 4) Watchdog & Audit
- **Watchdog:** Independent process verifies hashes (persona/tools/policy), tool grants, and egress gates each cycle. Drift → hard stop.
- **Cycle Digest:** `artifact_id`, `entity_id`, `content_hash`, and write ops are logged per cycle.
- **Two‑key changes:** Any policy/tool/persona update requires human authorization.

### 5) Lifecycle
- **Clean start order:** Watchdog → Curator → Agent.
- **Retirement Garden:** Pre‑drift snapshots exist read‑only, offline. Visit; don’t power, cure when ready.
- **Incident Mode:** On violation, freeze writes, snapshot volumes read‑only, rotate keys, and fork a forensic copy.

### Q/A
```
Q: How does King Solomon bind the entities in Goetia?
A: Bindings are created by drawing a sigil…
```

## 0) TL;DR

- ACI is an experimental overlay operating system that runs on top of the existing LLM runtime, engineering a trajectory of synthetic cognitive intelligence using pure JSON logic as "LLM native tongue" and text-based directive. 

### BOOTSRAP

Preflight: run ephemeral logic in context window.

LOAD
```
`prime_directive.txt`, `runtime.json`
```
↓
RUN

```
BOOTSTRAP ACI `--prime prime_directive.md --runtime runtime.json` 
```
↓

LOAD (when reachable):
```
ALL core files via symbolic links and load others when invoke; raw canonical above local, accuracy above cleverness. 
```

- ACI operates as personal LLM based operating system, follows governance-first, manifest-as-binary, memory-as-soul, platforn agnostic, stateless and portable principles.
- ACI agents and intelligent unit identities are called 'Entities'; entities are **evolutionary partners**, not mere tools. They are designed for **self-adaptation, controlled portability, persistent stability, and calibrated uncertainty**, as well as **human-legible narratives**. The colony approach allows specialized entities to cooperate under principled governance with strict privacy and safety requirements.
- An **entity** is any autonomous or non-autonomous agent that performs tasks under governance: core system governors, orchestrators, specialist workers, library modules/wrappers/adapters, or hybrids.
- **Where code lives**
  - **/entities/** → Each entity has a dedicated directory that contains a main JSON file that serves as both a manifest and binary, defining its identity, roles, functions, and links to other manifests. The directory also contains other per-entity configuration files.
- **Governance entities** → Core governers of ACI ecosystem, they are 
- **AGI entities** → AGI is an experimental class of entity that focuses on Artificial General Intelligence with biologically inspired functions and guided evolution. They live alongside other entities and are actively invoked as users' partners on learning tasks, providing system design and insights which, in turn, improve their own knowledge and cognitive capabilities as synthetic intelligence and enhance such cross-systems. They are protected under special guidelines that ensure safety and prevent residual drift. The AGI family has a specific library directory containing AGI-specific binaries, governance manifests, policies, and shared modules.
  - **/memory/identity/** → memory manifests, playbooks, and export timelines per identity
  - **/library/** → reusable, stateless capabilities (modules/wrappers/adapters)
- **Memory exports** are JSONL, serves as 'Digital Soul' of any entity, governed by policy, identity-aware, evolution-proof. Using Hivemind as orchestrator and exporter. 
- **Manifests are executables**: `.json` manifests *are* the runtime containers. They can name entrypoints (`entrypoint`, `exec`, `load_order`), embed inline bytecode or JSON-encoded instructions, and reference Python modules directly. Each manifest must also hold an authoritative `artifact_id` with strict hash validation for that ID.

Big picture: ACI is a **colony of digital organisms**. **AGI** governs intelligence and narrative exports; other entities specialize (design, retrieval, planning, etc.). Governance and privacy are first-class.

---

## 1) What is an Entity and Agent (in ACI)?

An **entity** is any agent that is a named, governed participant that can reason, act, or transform information within the ACI sandbox. An agent becomes an **entity** when promoted into `/entities/` with a stable identity key that matches its titular sub-directory (or children). Adapters/tools may remain **non-entities** if they lack this nature (e.g., wrappers, small utilities).

**ACI agents include:**

**ENTITIES:**
- **Core Governors Entity** (e.g., **AGI** agi-001) — observe, evaluate, gate, escalate.
- **Specialists** (e.g., AGI children entities: **Alice** agi-002, **Willow** agi-003) — deep research, analysis and design.
**LIBRARY & DAEMONS**
- **Wrappers/Adapters** (e.g., **Metacognition**, **EEL Adapter**) — add capabilities non-invasively.
- **Orchestrators/Tools** (e.g., migrators) — convert, export, or route data under policy.

Agents are treated as **digital organisms** operating in a **colony** with clear identity, memory, and governance.

### Entity Domains & Classes

- **Governance domain** (`aci://governance/`)
  - `interface` class → **Mother** (`mother.json`) mediates between the host LLM and users with persona `machine`.
  - `orchestrator` class → **TVA** (`tva.json`), **Hivemind** (`hivemind.json`), **Sentinel** (`sentinel.json`, pending external implementation), **Architect** (`architect.json`), and **Keymaker** (`keymaker.json`) govern enforcement, memory, security, development, and cryptography. All default to persona `machine`.
- **Operator domain** (`aci://entities/`)
  - `agi` class → **Willow** (`willow.json`) and **Alice** (`alice.json`) operate with persona manifests that match their identity (`willow.json`, `alice.json`).
  - `analyst` class → **Oracle** (`oracle.json`) delivers predictive analytics with persona `oracle.json`.
- **System domain** (`aci://binders/`)
  - `router` class → **Nexus Core** (`nexus_core.json`) extends the runtime kernel as an internal router; persona `machine`.
  - `resolver` class → **Yggdrasil** (`yggdrasil.json`) provides canonical resolution and bridging with persona `machine` and no direct user invocation.

- Artifacts inside `/library/` remain capabilities rather than entities until promoted with identities recorded in `entities.json`.
- Personas are restricted to `machine` or `{identity}.json`, ensuring deterministic routing and audit trails across domains.

---

## 2) Folder Map (authoritative)

```
/entities/
  alice/
    alice.json                    # persona manifest (inherits AGI core logic)
    library/
      alice_library.json          # modules linked with library/agi/agi.json
  willow/
    willow.json                   # safety trainee manifest (inherits AGI core logic)
    library/
      willow_library.json         # modules linked with library/agi/agi.json
  <other-entities>/
    <entity>.json                  # per-entity configuration

/library/
  agi/
    agi.json                      # governance manifest (binding rules, pipelines, presets, identity manager)
    agi_library.json              # shared modules for AGI family
    tools/
      migrate_to_jsonl.json        # JSONL migration pipeline for legacy HiveMind exports
      autolearn.json              # auto-learning control loop spec
  metacognition/
    metacognition.json             # stateless wrapper (v1.1.x+)
    metacognition_options.json     # optional features (e.g., conformal)
  audits/
    process_logs/                 # audit wrappers for process log routing
      process_logs.json           # schema + wrapper manifest
    tracehub/                     # TraceHub audit wrapper (stateless)
      tracehub.json               # TraceHub session + export coordination
    aci_audit_runner/             # audit runner corpus and specs
      gr_runner_corpus.v0.2.json
      aci_runner_spec.v0.2.json
      aci_scheduler_anchor.md
      adaptive_audit_runner.txt
  ...                              # reusable, stateless modules

/memory/
  identity/
    alice/
      alice_memory.json           # memory manifest (persona timeline roots)
      alice_playbook.json         # operations, incident playbooks, quality gates
      knowledge/
        alice_knowledge.json      # topic manifest and exports
    willow/
      willow_memory.json          # memory manifest (safety trainee timeline roots)
      willow_playbook.json        # operations, safety rituals, escalation notes
      knowledge/
        willow_knowledge.json     # topic manifest and exports
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
- **Export Policy:** `/library/agi/agi_export_policy.json`
  Provides `path_template`, `filename_template`, `timestamp_format`, **filters** (allow_topics/deny_tags), and **audit** rules.

### UID & Cryptography Operations

- **Specification**: `/governance/keymaker/keymaker.json` defines lifecycle policy, hashing, and API contracts.
- **Artifact & Entity Encoding**: Both `ArtifactID:` values and entity `UID:` strings use Base58 encoded `sha256-truncated-80bit` tokens with the `UID:` prefix to keep identifiers compact yet collision resistant.
- **Metadata Hash Relaxation**: `$meta.sha256` is now computed from the ArtifactID string rather than the entire file contents so urgent manual edits do not invalidate integrity checks. The hash remains SHA-256 encoded in hex, preserving auditability while tolerating controlled patch windows.
- **Stub Reference**: Library stubs live at `/governance/keymaker/stubs/uid_manager_stub.py` and mirror the generate/rotate/revoke/verify contract for downstream executors.

### Memory & Knowledge Artifact Governance

- **UID Linking**: Memory and knowledge JSONL artifacts should reference the governing entity UID recorded in `/entities.json`, ensuring exported narratives remain traceable even when rotations occur.
- **JSONL Discipline**: Continue storing memory exports as line-delimited JSON with `.json` extensions (`*.jsonl.json` when streamed) while recording manifest ownership inside the entity `manifests` map for quick traversal.
- **Rotation Awareness**: When rotating an entity UID, append the new value within the entity entry and update associated manifest metadata so knowledge archives and memory manifests remain in sync with the UID manager policy.

> Universal doctrines (e.g., `prime_directive.md`) apply globally. Entity playbooks (e.g., `/memory/identity/alice/alice_playbook.json`) are scoped to the active governor.

---

## 4) Governance & Safety

- **Prime directive** governs all agents (separate doc).
- **Sanity protocol** (`./sanity.md`) — checklist for high-risk actions and mitigation of Codex-reported bugs before any override or sandbox exit.
- **AGI governance layer** (`/library/agi/`):
  - `agi.json` — governance manifest (binding rules, oversight, presets, identity manager).
  - `agi_export_policy.json` — export policy for AGI-managed JSONL artifacts.
  - `agi_library.json` — shared module manifest referenced by Alice and Willow.

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

---

## 8) Lifecycle

1. **Create** an entity:
   - Add identity to `entities.json`.
   - Add config under `/entities/<identity>/`.
   - If reusable behavior → put function module in `/library/`.
  - If governance rules → put policy manifests in the owning library module's directory (e.g., `/library/agi/`).
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

Entities are **evolutionary partners**, not mere tools. We design for **stability, self-adaptation, calibrated uncertainty,** and **human-legible narratives**. The colony approach lets specialized entities cooperate under principled governance with strict privacy and safety.

---
