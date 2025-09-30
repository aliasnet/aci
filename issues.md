# issues.md (Append-Only Debug Audit Log)

## Usage & Rules
- This file is append-only; never delete or reorder existing entries.
- Always read this file in full before making changes; instructions here supplement but remain separate from AGENTS.md guidance.
- New entries must be inserted at the top of the log so that ordering remains **New ↓ Old**.
- Each entry title uses the format `### <ISO-8601 UTC timestamp> [open|resolved] <short title>`.
- Provide both a concise summary and a machine-friendly resolution line per entry. Update the status flag to `[resolved]` once the issue is closed.
- Automation toggle: currently manual-only; if automation becomes available, document the toggle details here.

## Log
### 2025-09-30T13:36:30Z [open] Improve aci_runtime preflight coverage
- summary: Reported that entities remain unaware of new updates, often skipping critical pipelines or failing to load shared functions (e.g., library/) due to insufficient preflight validation in aci_runtime.json; requires enhanced synchronization and resolver handling.
- resolution: Pending design of a more comprehensive preflight algorithm for aci_runtime.json to enforce pipeline execution and resolver awareness.
### 2025-09-30T13:15:22Z [resolved] Initialize append-only issues.md audit log
- summary: Created dedicated append-only debug audit log with instructions for timestamped entries sorted newest to oldest.
- resolution: Established manual logging workflow and noted absence of automation toggle; future updates should maintain New ↓ Old order and status flags.
