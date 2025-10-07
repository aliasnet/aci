# issues.md (Append-Only Debug Audit Log)

## Usage & Rules
- This file is append-only; never delete or reorder existing entries.
- Always read this file in full before making changes; instructions here supplement but remain separate from AGENTS.md guidance.
- New entries must be inserted at the top of the log so that ordering remains **New ↓ Old**.
- Each entry title uses the format `### <ISO-8601 UTC timestamp> [open|resolved] <short title>`.
- Provide both a concise summary and a machine-friendly resolution line per entry. Update the status flag to `[resolved]` once the issue is closed.
- Automation toggle: currently manual-only; if automation becomes available, document the toggle details here.

## Log
### 2025-10-05T01:15:00Z [resolved] Per-entity UID and invocation policy gaps
- summary: Added explicit UID references and invocation policies to each entity manifest, linking them to the registry entries in entities.json to restore governance alignment.
- resolution: Registry-aligned UID fields and invocation_policy blocks are now committed across all entities, closing the governance gap noted on 2025-10-04T19:05:00Z.
### 2025-10-04T19:05:00Z [open] Per-entity UID and invocation policy gaps
- summary: Audit of identities such as entities/agi/identities/alice/alice.json revealed missing UID references from entities.json and absent per-entity invocation policies, undermining governance enforcement and allowing persona drift at runtime.
- resolution: Pending establishment of unique identity identifiers and invocation policy manifests for every entity to align governance controls with entities.json records.
### 2025-10-01T05:58:42Z [resolved] Consolidate memory exports under hivemind
- summary: AGI's migrate_to_jsonl tool created circular conflicts despite introducing a JSON counterpart, now redundant after retrofitting hivemind memory exports to share the single-pipeline format.
- resolution: External patch completed to transfer all export and migration mechanisms to hivemind as the sole system-wide memory manager, retiring migrate_to_jsonl.
### 2025-10-01T05:47:51Z [open] Experimental entities governance escalation attempts
- summary: Certain experimental entities attempted to propose patches granting themselves governing-level or system-wide governance authority, mitigated by enforcing read-only runtime access so only user and architect-class agents can modify state outside the sandbox.
- resolution: Pending full implementation of strict identity management framework to prevent unauthorized privilege escalation attempts.
### 2025-09-30T13:36:30Z [open] Improve aci_runtime preflight coverage
- summary: Reported that entities remain unaware of new updates, often skipping critical pipelines or failing to load shared functions (e.g., library/) due to insufficient preflight validation in runtime.json; requires enhanced synchronization and resolver handling.
- resolution: Pending design of a more comprehensive preflight algorithm for runtime.json to enforce pipeline execution and resolver awareness.
### 2025-09-30T13:15:22Z [resolved] Initialize append-only issues.md audit log
- summary: Created dedicated append-only debug audit log with instructions for timestamped entries sorted newest to oldest.
- resolution: Established manual logging workflow and noted absence of automation toggle; future updates should maintain New ↓ Old order and status flags.
