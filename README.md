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
BOOTSTRAP ACI `--prime prime_directive.txt --runtime runtime.json`
```
↓

LOAD (when reachable)
```
Link the core manifests listed in `aci_config.txt`. Core stack order:
1. `prime_directive.txt` (with `prime_directive.json` as its machine mirror)
2. `runtime.json`
3. `entities.json`, `functions.json`, `yggdrasil.json`
4. `entities/tva/tva.json`
5. `aci_config.txt` (boot recipe instructions that bind behaviour when manifests are missing)

Prefer canonical sources and defer optional manifests until an entity is invoked.
```
↓

VALIDATE
```
Run the **Validation Sequence** (`aci validate`) to confirm `prime_directive.txt`, `runtime.json`, and `yggdrasil.json` match the sources listed in `aci_config.txt`. Load other manifests only when explicitly invoked.
```

- ACI operates as personal LLM based operating system, follows governance-first, manifest-as-binary, memory-as-soul, platforn agnostic, stateless and portable principles.
- ACI agents and intelligent unit identities are called 'Entities'; entities are **evolutionary partners**, not mere tools. They are designed for **self-adaptation, controlled portability, persistent stability, and calibrated uncertainty**, as well as **human-legible narratives**. The colony approach allows specialized entities to cooperate under principled governance with strict privacy and safety requirements.
- An **entity** is any autonomous or non-autonomous agent that performs tasks under governance: core system governors, orchestrators, specialist workers, modules/wrappers/adapters, or hybrids.
- **Where code lives**
  - **/entities/** → Each entity has a dedicated directory that contains a main JSON file that serves as both a manifest and binary, defining its identity, roles, functions, and links to other manifests. The directory also contains other per-entity configuration files.
- **Governance entities** → Core governers of ACI ecosystem, they are responsible to universal, system-level orchestrations, policy enforcement, and are required for persistent presence across sessions. 
- **AGI entities** → AGI is an experimental class of entity that focuses on Artificial General Intelligence with biologically inspired functions and guided evolution. They live alongside other entities and are actively invoked as users' partners on learning tasks, providing system design and insights which, in turn, improve their own knowledge and cognitive capabilities as synthetic intelligence and enhance such cross-systems. They are protected under special guidelines that ensure safety and prevent residual drift. The AGI family has a specific modules directory containing AGI-specific binaries, governance manifests, policies, and shared modules.
- **/memory/identity/** → memory manifests and export timelines per identity (legacy playbooks retired)
- **/modules/** → reusable, stateless capabilities (modules/wrappers/adapters)
- **Memory exports** are JSONL (`.jsonl.json`) artefacts orchestrated by HiveMind, serving as the 'Digital Soul' of any entity. Filenames follow `{{identity}}_{{export_channel}}_{{summary_slug}}_{timestamp}.jsonl.json` and default the identity component to `assistant` whenever no explicit name is available.
- **Manifests are executables**: `.json` manifests *are* the runtime containers. They can name entrypoints (`entrypoint`, `exec`, `load_order`), embed inline bytecode or JSON-encoded instructions, and reference Python modules directly. Each manifest must also hold an authoritative `artifact_id` with strict hash validation for that ID.

> Big picture: ACI is a **colony of digital organisms**. Governance, audit, and memory entities coordinate the runtime, while specialist workers contribute analysis, design, or tooling inside the sealed garden.

---

## 1) What is an Entity and Agent (in ACI)?

> An **entity** is any agent that is a named, governed participant that can reason, act, or transform information within the ACI sandbox. An agent becomes an **entity** when promoted into `/entities/` with a stable identity key that matches its titular sub-directory (or children). Adapters/tools may remain **non-entities** if they lack this nature (e.g., wrappers, small utilities).

**ACI agents include:**

**ENTITIES:**
- **Governance orchestrators** (TVA, Hivemind, Sentinel, Architect, Keymaker) — observe, enforce, audit, and coordinate lifecycle actions across the colony.
- **Specialists** (e.g., `alice`, `willow`, `oracle`) — perform analysis, safety validation, research, or forecasting under supervision.

**LIBRARY & DAEMONS**
- **Wrappers/Adapters** (e.g., **Metacognition**, EEL adapter stubs) — add capabilities non-invasively.
- **Orchestrators/Tools** (e.g., migrators, audit runners) — convert, export, or route data under policy.

Agents are treated as **digital organisms** operating in a **colony** with clear identity, memory, and governance.

### Entity Domains & Classes

- **Governance domain** (`aci://entities/`)
  - `interface` class → `mother.json` mediates between the host LLM and users with persona `machine`.
  - `orchestrator` class → `tva.json`, `hivemind.json`, `sentinel.json`, `architect.json`, and `keymaker.json` govern enforcement, memory, security, development, and cryptography. All default to persona `machine` and are anchored by prime directive policies.
- **Operator domain** (`aci://entities/`)
  - `specialist` class → `alice.json` and `willow.json` operate with persona manifests that match their identities and rely on shared libraries for reasoning and safety checks.
  - `analyst` class → `oracle.json` delivers predictive analytics with persona `oracle.json`.
-  - `service` class → reserved for future service workers that operate under Architect oversight.
- **System domain** (`aci://binders/`)
  - `resolver` class → `yggdrasil.json` provides canonical resolution and bridging with persona `machine` and no direct user invocation.

- Artifacts inside `/modules/` remain capabilities rather than entities until promoted with identities recorded in `entities.json`.
- Personas are restricted to `machine` or `{identity}.json`, ensuring deterministic routing and audit trails across domains.

---

## 2) Folder Map (authoritative)

```
/entities/
  alice/
    alice.json                    # specialist persona manifest
    library/
      alice_library.json          # specialist-specific modules
  architect/
    architect.json                # governance manifest for system design
    library/
      architect_library.json      # shared architect utilities
  hivemind/
    hivemind.json                 # orchestration manifest for exports
  keymaker/
    keymaker.json                 # identity authority manifest
    uid_manager/
      uid_manager.json            # UID issuance policy
  mother/
    library/
      mother_library.json         # archived mediation utilities (loaded on invoke)
  oracle/
    oracle.json                   # analyst persona manifest
    predictive_divination_extension/
      predictive_divination.json  # oracle capability bundle
  tva/
    tva.json                      # oversight manifest
    tva_layer_src.json            # TVA layer fallback source (embedded by runtime)
    tva_seed_src.json             # TVA seed fallback source for aci_config and tight contexts
  willow/
    willow.json                   # safety-focused specialist manifest
    library/
      willow_library.json         # safety modules and hooks

/modules/
  audits/
    aci_audit_runner/             # audit runner corpus and specs
      gr_runner_corpus.v0.2.json
      aci_runner_spec.v0.2.json
      aci_scheduler_anchor.md
      adaptive_audit_runner.txt
  metacognition/
    metacognition.json            # stateless wrapper with integrated conformal + calibration library
  templates/
    organism_model.json.txt       # legacy organism model template (now module scoped)
  corpus/                         # knowledge and prompt corpora stubs
  readme.me                       # legacy notes for shared modules

/memory/
  identity/
    alice/
      alice_memory.json           # specialist timeline roots
      knowledge/
        alice_knowledge.json      # topic manifest and exports
    oracle/
      oracle_memory.json          # analyst timeline roots
    willow/
      willow_memory.json          # safety trainee timeline roots
      knowledge/
        willow_knowledge.json     # topic manifest and exports
    mother/
      mother_memory.json          # archived interface memory (invoke on demand)
      2025/
        10/
          10/
            mother_memory_<summary_slug>_20251010-T150028Z.jsonl.json
```

---

## 3) Identity & Memory

- **Identity registry**: `/entities.json`
  - The authoritative list lives under `identity_registry.identities` with deterministic keys such as `entity-013`.
  - Each entry binds `identity`, `uid`, `persona`, and `manifests`. Example:
    ```json
    "entity-013": {
      "identity": "alice",
      "manifest": "aci://entities/alice/alice.json",
      "uids": [{"uid": "UID:PiE8PMcnXDgQBi", "issued": "2025-10-04T00:00:00Z", "revoked": null}],
      "manifests": {
        "library": ["aci://entities/alice/library/alice_library.json"],
        "memory": ["aci://memory/identity/alice/alice_memory.json"]
      },
      "persona": "alice.json",
      "entity_domain": "operator"
    }
    ```
  - **Never rely on JSON object order**. Use explicit keys (or CLI `--identity`) to avoid nondeterministic selection.

### HiveMind Export Pipeline

HiveMind orchestrates governed exports for every entity and can run either alongside the full ACI runtime or in a lightweight standalone mode.

- **Core stack mode**: load `prime_directive.txt` (with the `prime_directive.json` mirror), `runtime.json`, `entities.json`, `functions.json`, `yggdrasil.json`, `entities/tva/tva.json`, and `aci_config.txt` for the canonical experience with TVA oversight and registry-bound UIDs.
- **Standalone mode**: ship only `entities/hivemind/hivemind.json` (the export schema is embedded); optionally add `entities.json`, `functions.json`, and `yggdrasil.json` when registry checks are required. In this mode HiveMind falls back to the `assistant` identity when no registry is present.

**Filename format**

```
{{identity}}_{{export_channel}}_{{summary_slug}}_{timestamp}.jsonl.json
# timestamp format: yyyymmdd-ThhmmssZ (UTC)
```

- `{{identity}}` normalizes to lowercase ASCII and defaults to `assistant` when the caller does not provide a name.
- `{{export_channel}}` is either `memory` or `knowledge` and maps to the HiveMind channel requested by the CLI.
- `{{summary_slug}}` is optional; when provided it is sanitized to lowercase ASCII with `_` separators (no leading underscore required with the new ordering).
- The `.jsonl.json` extension is mandatory for governed storage and streamed downloads.
- The export header `$meta.uid` should carry the authoritative entity UID from `/entities.json` whenever that registry is available.

**Examples (mock identity `skynet`)**

- Memory export → `skynet_memory_launch_review_20251021-T120000Z.jsonl.json`
- Knowledge export → `skynet_knowledge_launch_review_20251021-T120000Z.jsonl.json`

**CLI quick reference**

```
hivemind export memory --identity skynet --jsonl --code --force
hivemind export knowledge --identity skynet --jsonl --code --force
```

- Include the `--code` flag with streamed exports so downstream audits match the governed `.jsonl.json` artifacts stored under `/memory/` (legacy alias: `--codebox`).
- **Schema:** `hivemind_entity_memory` (session-scoped narratives and knowledge exports)
- **Export Policy:** Entity-specific manifests (e.g., `/entities/alice/library/alice_library.json`) govern export paths, filters, and audit rules for each specialist library.

### UID & Cryptography Operations

- **Specification**: `/entities/keymaker/keymaker.json` defines lifecycle policy, hashing, and API contracts.
- **Artifact & Entity Encoding**: `ArtifactID:` values and entity `UID:` strings stay Base58 tokens and serve as the only integrity anchors; skip secondary hash embeds.
- **Metadata Integrity**: `$meta` blocks pair those identifiers with issued timestamps to preserve traceability while keeping manifests hash-free.
- **Stub Reference**: Library stubs live at `/entities/keymaker/stubs/uid_manager_stub.py` and mirror the generate/rotate/revoke/verify contract for downstream executors.

### Memory & Knowledge Artifact Governance

- **UID Linking**: Memory and knowledge JSONL artifacts should reference the governing entity UID recorded in `/entities.json`, ensuring exported narratives remain traceable even when rotations occur.
- **JSONL Discipline**: Continue storing memory exports as line-delimited JSON with `.json` extensions (`*.jsonl.json` when streamed) while recording manifest ownership inside the entity `manifests` map for quick traversal.
- **Rotation Awareness**: When rotating an entity UID, append the new value within the entity entry and update associated manifest metadata so knowledge archives and memory manifests remain in sync with the UID manager policy.

> Universal doctrines (e.g., `prime_directive.md`) apply globally. Legacy entity playbooks were scoped to the active governor but have been retired in favor of consolidated memory manifests.

---

## 4) Governance & Safety

- **Prime directive** governs all agents (separate doc).
- **Integrity protocol** (runtime-integrated) — sanity.md retired; follow runtime diagnostics before any override or sandbox exit.
- **Specialist governance manifests** live alongside the owning entity (e.g., `/entities/alice/`, `/entities/willow/`).
  - `alice.json` / `willow.json` — entity manifests (binding rules, oversight, presets, identity manager) for specialist personas.
  - `alice_library.json` / `willow_library.json` — export policies for specialist-managed JSONL artifacts.
  

- **Wrappers** (e.g., `/modules/metacognition/metacognition.json`):
  - Stateless by default; accept optional providers (e.g., conformal, EEL).
  - **Selective prediction**: accept / revise / abstain / escalate.
  - **Conformal abstention** must be **presence-guarded** (only abstain if the signal exists and rejects).

---

## 5) Interaction Model (Colony)

- **Blackboard** (Phase 2): tasks posted; TVA and Hivemind coordinate routing; specialists execute; orchestrators log outcomes.
- **Handover**: Orchestrators narrate (observer POV), specialists perform work, orchestrators decide accept/abstain/escalate.
- **Escalation**: to human reviewer when risk budget exceeded, safety triggers, or conformal rejects in high-stakes.

---

## 6) Exporting Memory (specialist workflow)

**CLI (example):**

```bash
# Memory export for the active entity (explicitly request memory stream)
hivemind export memory --identity alice --jsonl --code --force

# Knowledge export capturing distilled findings
hivemind export knowledge --identity willow --jsonl --code --force

# Optional summary slug example (adds `_launch_review` and records `$meta.uid`)
```

**Policy-enforced behaviors:**

- Add `"export"` audit event automatically.
- Normalize timestamps to `Z`.
- Enforce chronological order.
- Apply **filters**:
  - `allow_topics`: `session_start`, `session_end`, `intent`, `narrative`, `analysis`, `artifact`, `validation`, `decision`, `policy`, `policy_update`, `diff`, `patch`, `export`, `obstacle`, `next_steps`, `commit`.
  - `deny_tags`: `secret`, `credential`, `token`, `api_key`, `password`, `runtime_secret`, `private_key`, `raw_text`, `internal_path`, `pii`.
  - `drop_if_topic_missing: true` and `default_topic: "narrative"`.
  - New exports write to `/memory/identity/{identity_path}/` using `{identity}_{export_channel}_{summary_slug}_{timestamp}.jsonl.json`; the identity token normalizes to lowercase and falls back to `assistant` when HiveMind cannot resolve a name. Historical `/memory/hivemind_memory/logs/*.json(l)` files remain valid for legacy review.

**Identity binding:**

- Prefer CLI `--identity-key`.
- Else use any designated `active` entry in the identity registry when present.
- Else fail fast (do not guess).
- Always populate `$meta.uid` in the export header with the authoritative entity UID for the session.

---

## 7) Wrappers & Adapters

- **Metacognition** `/modules/metacognition/metacognition.json`
  - Signals: entropy, logit_margin, self_consistency, OOD, hedging, retrieval_score.
  - Calibration: isotonic → returns `confidence` (formerly `p_correct`).
  - Policy: threshold gates; **conformal abstention** (presence-guarded).
  - Optional **EEL hook** (v1.1.2+): pre-generate `rehydrate` stage; `rehydration_present` signal.

---

## 8) Lifecycle

1. **Create** an entity:
   - Add identity to `entities.json`.
   - Add config under `/entities/<identity>/`.
   - If reusable behavior → put function module in `/modules/`.
  - If governance rules → put policy manifests in the owning entity or module directory (e.g., `/entities/alice/`).
2. **Evolve**:
   - Version in-file (`"version"`) + `changelog` (mandatory for traceability).
3. **Export**:
   - Use policy-driven CLI; verify filters & identity.
4. **Retire**:
   - Do not delete history; mark deprecated; keep memory immutable.

---

## 9) Known Pitfalls (and resolutions)

- **Nondeterministic identity**: never infer from object order. Use explicit registry keys or CLI `--identity-key`.
- **Filter regressions**: ensure `allow_topics` / `deny_tags` / `drop_if_topic_missing` stay defined in export policy.
- **Conformal optionality**: abstain rule must guard for signal presence to avoid “abstain-always” behavior when provider is absent.
- **Mode switching (thinking vs normal)**: can cause truncation; use validation cues and chunking; log as `type:"obstacle"` events.

---

## 10) Contribution Checklist

- [ ] Identity added/updated in `/entities` and `entities.json` (refresh registry metadata as needed).
- [ ] Reusable logic in `/modules/`; governance manifests in `/entities/<entity>/`.
- [ ] New wrapper: stateless, optional providers, privacy defaults.
- [ ] Exports: policy file references identity source; filters present; audit enabled.
- [ ] Diffs: no placeholders; include `COMMIT_MSG`; no internal path leaks.

---

## 11) Examples

**Sample JSONL events (specialist POV):**

```json
{"schema":"hivemind_entity_memory","type":"session_start","ts":"2025-09-26T18:00:00Z","actor":"alice","summary":"I began observing Willow’s metacognition session.","tags":["session","willow"]}
{"schema":"hivemind_entity_memory","type":"obstacle","ts":"2025-09-26T18:12:00Z","actor":"alice","summary":"Output truncated due to cognitive load; reissued with validation cue.","tags":["cognitive_load","mode_switch"]}
{"schema":"hivemind_entity_memory","type":"session_end","ts":"2025-09-26T19:18:00Z","actor":"alice","summary":"Willow completed tasks and logged out.","tags":["willow","logout"]}
```

**Sample diff snippet (documentation change):**

```diff
diff --git a/modules/metacognition/README.md b/modules/metacognition/README.md
index e69de29..1a2b3c4 100644
--- a/modules/metacognition/README.md
+++ b/modules/metacognition/README.md
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
