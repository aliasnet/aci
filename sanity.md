# Sanity Protocol

## 1. Purpose

The sanity protocol outlines mandatory guardrails before executing overrides, sandbox exits, or other high-risk actions. Apply
these steps whenever the requested behavior could alter system state, governance posture, or memory exports.

## 2. Mandatory Checklist

- Confirm the calling entity's authority and authentication markers.
- Validate current system state for anomalies or corruption before proceeding.
- Escalate to TVA oversight if validation fails or uncertain results occur.
- Log all sanity protocol outcomes in TraceHub and TVA audit ledgers.

Failure to comply with this protocol is a violation of the Prime Directive enforcement note.

## 3. Known Bugs Flagged by Codex

Codex has reported the following failure modes that require additional scrutiny whenever the sanity protocol is invoked:

- **Unzipping JSON manifests** — Attempting to unzip `library.json`, `entities.json`, or `memory.json` corrupts manifests and
  stalls bootstrap routines. Only unzip the corresponding `.zip` artifacts; load `.json` files directly.
- **Metacognition filename typo** — Using `metacogition.json` (missing “n”) causes resolver 404s and breaks downstream
  dependency wiring. Verify spellings before dispatch.
- **Duplicate presence beacons** — Running `aci.boot.activate` immediately followed by `aci.timeline.start` for the same
  session spawns overlapping presence files and timeline drift. Check for existing beacons and deduplicate before activation.
- **Canonical override via local fallback** — Preferring local mirrors when the canonical GitHub source is reachable introduces
  drift and stale state. Always confirm canonical availability before honoring a fallback.
- **Path alias duplication** — Mixing `/aci`, `aci://`, `workspace/aci`, or `aliasnet/aci` within the same operation spawns
  duplicate directory trees and breaks resolver expectations. Normalize references to a single canonical path before dispatch.
